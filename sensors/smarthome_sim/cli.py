"""Command-line interface for SmartHome Simulator."""

from __future__ import annotations

import argparse
import logging
import multiprocessing as mp
import signal
from pathlib import Path
from typing import Any, Dict, List

from .benchmark import run_handshake_benchmark
from .broker import Broker
from .config import load_brokers, parse_simulation_config, setup_logging
from .simulator import Simulator, on_connect, on_disconnect, on_message


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser (legacy args removed)."""
    parser = argparse.ArgumentParser(
        prog="smarthome-sim",
        description="Multi-broker MQTT sensor/actuator simulator with mTLS support",
    )
    
    # Core options
    parser.add_argument("-c", "--config", default="sensors/brokers.yml",
                        help="Configuration file path (YAML or JSON)")
    parser.add_argument("--devices", type=int, help="Override device count")
    parser.add_argument("--base-topic", help="Override MQTT base topic")
    parser.add_argument("--discovery-prefix", help="Override HA discovery prefix")
    parser.add_argument("--qos", type=int, choices=[0, 1, 2], help="MQTT QoS level")
    parser.add_argument("--retain", action="store_true", help="Enable retained messages for state topics")
    parser.add_argument("--connect-timeout", type=float, help="Connection timeout (seconds)")
    parser.add_argument("--client-id-prefix", help="MQTT client ID prefix")
    parser.add_argument("--ha-discovery", action="store_true",
                        help="Enable Home Assistant MQTT Discovery")
    
    # Execution modes
    parser.add_argument("--dry-run", action="store_true", help="Simulate without publishing")
    parser.add_argument("--once", action="store_true", help="Run one cycle and exit")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of worker processes for multi-core scaling")
    
    # Handshake benchmark (thesis feature)
    parser.add_argument("--handshake-samples", type=int, default=0,
                        help="Run N handshake benchmark samples per worker")
    parser.add_argument("--handshake-interval", type=float, default=0.1,
                        help="Delay between samples (seconds)")
    parser.add_argument("--handshake-timeout", type=float, default=10.0,
                        help="Connection timeout for benchmark (seconds)")
    parser.add_argument("--handshake-out", default="sensors/handshake_metrics",
                        help="Output directory for benchmark results")
    parser.add_argument("--handshake-plot", action="store_true",
                        help="Generate plots (requires matplotlib)")
    parser.add_argument("--handshake-only", action="store_true",
                        help="Only run benchmark, skip simulation")
    
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Logging verbosity")
    
    return parser


def _run_worker(
    *,
    config_path: str,
    worker_id: int,
    start_id: int,
    end_id: int,
    cli_overrides: Dict[str, Any],
) -> None:
    """Worker process entry point for multi-process mode."""
    setup_logging(str(cli_overrides.get("log_level", "INFO")))

    brokers, rest, _ = load_brokers(config_path)
    cli = argparse.Namespace(**cli_overrides)
    sim = parse_simulation_config(rest, cli)
    sim.client_id_prefix = f"{sim.client_id_prefix}-w{worker_id}"

    hs_samples = cli_overrides.get("handshake_samples", 0) or 0
    if hs_samples > 0:
        run_handshake_benchmark(
            brokers=brokers,
            client_id_prefix=sim.client_id_prefix,
            samples=hs_samples,
            interval_s=cli_overrides.get("handshake_interval", 0.1),
            timeout_s=cli_overrides.get("handshake_timeout", 10.0),
            out=cli_overrides.get("handshake_out", "sensors/handshake_metrics"),
            plot=cli_overrides.get("handshake_plot", False),
            worker_id=worker_id,
            on_connect=on_connect,
            on_disconnect=on_disconnect,
            on_message=on_message,
        )
        if cli_overrides.get("handshake_only", False):
            return

    Simulator(
        brokers=brokers,
        sim=sim,
        dry_run=cli_overrides.get("dry_run", False),
        once=cli_overrides.get("once", False),
        device_id_start=start_id,
        device_id_end=end_id,
        worker_id=worker_id,
    ).run()


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.log_level)

    # Load configuration
    try:
        brokers, rest, _ = load_brokers(args.config)
    except FileNotFoundError as e:
        if args.dry_run and args.config == "sensors/brokers.yml":
            logging.warning(f"Config not found ({e}). Using defaults for --dry-run.")
            brokers = [Broker(host="dry-run", port=1883, tls=False)]
            rest = {}
        else:
            logging.error(f"Config error: {e}")
            raise SystemExit(2)
    except Exception as e:
        logging.error(f"Config error: {e}")
        raise SystemExit(2)

    logging.info(f"Loaded {len(brokers)} broker(s) from {args.config}")

    sim = parse_simulation_config(rest, args)
    workers = max(1, args.workers)

    # Single-process handshake benchmark
    hs_samples = args.handshake_samples or 0
    if workers == 1 and hs_samples > 0:
        run_handshake_benchmark(
            brokers=brokers,
            client_id_prefix=sim.client_id_prefix,
            samples=hs_samples,
            interval_s=args.handshake_interval,
            timeout_s=args.handshake_timeout,
            out=args.handshake_out,
            plot=args.handshake_plot,
            worker_id=None,
            on_connect=on_connect,
            on_disconnect=on_disconnect,
            on_message=on_message,
        )
        if args.handshake_only:
            return

    # Single-process simulation
    if workers == 1:
        Simulator(
            brokers=brokers,
            sim=sim,
            dry_run=args.dry_run,
            once=args.once,
        ).run()
        return

    # Multi-process mode
    total_devices = sim.devices
    chunk = (total_devices + workers - 1) // workers

    cli_overrides: Dict[str, Any] = {
        "log_level": args.log_level,
        "dry_run": args.dry_run,
        "once": args.once,
        "devices": args.devices,
        "base_topic": args.base_topic,
        "discovery_prefix": args.discovery_prefix,
        "connect_timeout": args.connect_timeout,
        "qos": args.qos,
        "retain": args.retain,
        "ha_discovery": args.ha_discovery,
        "client_id_prefix": args.client_id_prefix,
        "handshake_samples": hs_samples,
        "handshake_interval": args.handshake_interval,
        "handshake_timeout": args.handshake_timeout,
        "handshake_out": args.handshake_out,
        "handshake_plot": args.handshake_plot,
        "handshake_only": args.handshake_only,
    }

    procs: List[mp.Process] = []
    for wid in range(workers):
        start_id = wid * chunk + 1
        end_id = min((wid + 1) * chunk, total_devices)
        if start_id > end_id:
            continue
        p = mp.Process(
            target=_run_worker,
            kwargs={
                "config_path": args.config,
                "worker_id": wid,
                "start_id": start_id,
                "end_id": end_id,
                "cli_overrides": cli_overrides,
            },
        )
        p.start()
        procs.append(p)

    stop_requested = {"flag": False}
    prev_sigint = signal.getsignal(signal.SIGINT)

    def on_sigint(*_):
        if not stop_requested["flag"]:
            logging.info("Stopping workers...")
        stop_requested["flag"] = True
        for p in procs:
            if p.is_alive():
                p.terminate()

    try:
        signal.signal(signal.SIGINT, on_sigint)
        while any(p.is_alive() for p in procs):
            for p in procs:
                p.join(timeout=0.2)
            if stop_requested["flag"]:
                for p in procs:
                    if p.is_alive():
                        p.terminate()
    finally:
        try:
            signal.signal(signal.SIGINT, prev_sigint)
        except Exception:
            pass


if __name__ == "__main__":
    main()

