#!/usr/bin/env python3
"""
Multi-Broker Sensor Simulator
- Simulates multiple virtual sensors
- Publishes data to multiple MQTT brokers (Mosquitto / EMQX)
- Supports multithreading and adjustable publishing interval
- Loads broker configuration from an external YAML/JSON file
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import sys
import threading
import time
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import paho.mqtt.client as mqtt

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None  # Lazy error if YAML actually needed



# ==========================
# Broker model & Config Loading
# ==========================
@dataclass
class Broker:
    host: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    tls: bool = False
    keepalive: int = 60
    client_id: Optional[str] = None

    @classmethod
    def from_obj(cls, item: Any) -> "Broker":
        if not isinstance(item, dict):
            raise ValueError("Broker entry must be an object")
        host = item.get("host")
        if not host:
            raise ValueError("Broker entry missing 'host'")
        return cls(
            host=str(host),
            port=int(item.get("port", 1883)),
            username=item.get("username"),
            password=item.get("password"),
            tls=bool(item.get("tls", False)),
            keepalive=int(item.get("keepalive", 60)),
            client_id=item.get("client_id"),
        )

    def create_client(self, client_id_prefix: Optional[str] = None) -> mqtt.Client:
        cid = self.client_id
        if not cid and client_id_prefix:
            cid = f"{client_id_prefix}-{self.host}"

        client = mqtt.Client(client_id=cid, clean_session=True)
        client.user_data_set({"broker": {
            "host": self.host,
            "port": self.port,
            "tls": self.tls,
        }})
        client.enable_logger(logging.getLogger("paho"))
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect

        if self.username is not None:
            client.username_pw_set(self.username, self.password)

        if self.tls:
            client.tls_set()  # default system CA

        client.reconnect_delay_set(min_delay=1, max_delay=60)
        client.connect_async(self.host, self.port, keepalive=self.keepalive)
        client.loop_start()
        return client


def load_brokers(config_path: str) -> List[Broker]:
    """Load broker configuration from YAML or JSON.

    Expected structure (list of brokers):
    - host: chi.yuanweize.win
      port: 1883
      username: null
      password: null
      tls: false  # optional
      keepalive: 60  # optional
    """
    path = Path(config_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    text = path.read_text(encoding="utf-8")

    data: Any
    # Try YAML first if available
    if yaml is not None and path.suffix.lower() in {".yml", ".yaml"}:
        data = yaml.safe_load(text)
    else:
        # Fallback to JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            # If YAML lib exists, try YAML regardless of extension
            if yaml is not None:
                data = yaml.safe_load(text)
            else:
                raise ValueError(f"Failed to parse config as JSON and YAML is unavailable: {e}")

    if not isinstance(data, list):
        raise ValueError("Config must be a list of broker objects")

    brokers: List[Broker] = []
    for i, item in enumerate(data, start=1):
        try:
            brokers.append(Broker.from_obj(item))
        except Exception as e:
            raise ValueError(f"Invalid broker #{i}: {e}") from e
    return brokers


def setup_logging(level: str) -> None:
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


# ==========================
# MQTT Client Setup
# ==========================
def on_connect(client: mqtt.Client, userdata: Dict[str, Any], flags, rc):  # type: ignore[override]
    broker = userdata.get("broker")
    host = broker.get("host") if isinstance(broker, dict) else "?"
    if rc == 0:
        logging.info(f"[{host}] Connected")
    else:
        logging.warning(f"[{host}] Connection failed rc={rc}")


def on_disconnect(client: mqtt.Client, userdata: Dict[str, Any], rc):  # type: ignore[override]
    broker = userdata.get("broker")
    host = broker.get("host") if isinstance(broker, dict) else "?"
    if rc != 0:
        logging.warning(f"[{host}] Unexpected disconnect rc={rc}; will auto-reconnect")
    else:
        logging.info(f"[{host}] Disconnected")


def create_client(broker: Broker, client_id_prefix: Optional[str] = None) -> mqtt.Client:
    """Back-compat wrapper to create a client from a Broker instance."""
    return broker.create_client(client_id_prefix)


def publish_ha_discovery(
    broker_clients: List[Tuple[mqtt.Client, Broker]],
    sensors: int,
    topic_template: str,
    discovery_prefix: str,
    payload_format: str,
) -> None:
    """Publish Home Assistant MQTT Discovery configs (retained).

    Note: Works best with payload_format='json'.
    """
    if payload_format != "json":
        logging.warning("HA Discovery expects JSON payloads; set --payload json")

    for sensor_id in range(1, sensors + 1):
        state_topic = topic_template.format(sensor_id=sensor_id)
        unique_id = f"sim_sensor_{sensor_id}_temperature"
        cfg_topic = f"{discovery_prefix}/sensor/{unique_id}/config"
        cfg_payload = {
            "name": f"Sensor {sensor_id} Temperature",
            "unique_id": unique_id,
            "state_topic": state_topic,
            "device_class": "temperature",
            "unit_of_measurement": "°C",
            "state_class": "measurement",
            "value_template": "{{ value_json.value }}",
            "device": {
                "identifiers": [f"sim_sensor_{sensor_id}"],
                "manufacturer": "SmartHome Simulator",
                "model": "Virtual Sensor",
                "name": f"Virtual Sensor {sensor_id}",
            },
        }
        payload_str = json.dumps(cfg_payload, separators=(",", ":"))
        for client, broker in broker_clients:
            host = broker.host
            try:
                if hasattr(client, "is_connected") and not client.is_connected():  # type: ignore[attr-defined]
                    logging.debug(f"[{host}] Not connected yet; skip HA discovery for sensor {sensor_id}")
                    continue
                client.publish(cfg_topic, payload_str, qos=0, retain=True)
                logging.debug(f"[{host}] HA discovery -> {cfg_topic}: {payload_str}")
            except Exception as e:
                logging.error(f"[{host}] ERROR HA discovery for sensor {sensor_id}: {e}")


def sensor_worker(
    sensor_id: int,
    broker_clients: List[Tuple[mqtt.Client, Broker]],
    topic_template: str,
    publish_interval: float,
    stop_event: threading.Event,
    qos: int = 0,
    retain: bool = False,
    payload_format: str = "plain",
    temp_min: float = 20.0,
    temp_max: float = 30.0,
    dry_run: bool = False,
    model: str = "uniform",
    noise_sd: float = 0.2,
    drift_per_minute: float = 0.0,
    jitter: float = 0.0,
    seed: int | None = None,
) -> None:
    """Thread function for each virtual sensor"""
    rng = random.Random(seed if seed is not None else sensor_id)

    # Initialize value for drift model at midpoint
    current_value = (temp_min + temp_max) / 2.0

    while not stop_event.is_set():
        if model == "uniform":
            value = round(rng.uniform(temp_min, temp_max), 2)
        else:
            # Gaussian noise and linear drift per minute scaled to interval
            # Convert drift per minute to per-interval increment
            drift_per_second = drift_per_minute / 60.0
            # Value update: drift + noise
            current_value += drift_per_second * max(1e-6, publish_interval)
            current_value += rng.gauss(0.0, noise_sd)
            # Clamp to [min, max]
            current_value = max(temp_min, min(temp_max, current_value))
            value = round(current_value, 2)
        topic = topic_template.format(sensor_id=sensor_id)

        if payload_format == "json":
            payload: Any = {
                "sensor_id": sensor_id,
                "value": value,
                "ts": int(time.time()),
            }
            payload_str = json.dumps(payload, separators=(",", ":"))
        else:
            payload_str = str(value)

        for client, broker in broker_clients:
            host = broker.host
            if dry_run:
                logging.info(f"[DRY-RUN][{host}] Sensor {sensor_id} -> {topic}: {payload_str}")
                continue
            try:
                # Skip publish if the client has not connected yet
                if hasattr(client, "is_connected") and not client.is_connected():  # type: ignore[attr-defined]
                    logging.debug(f"[{host}] Not connected yet; skipping publish for sensor {sensor_id}")
                    continue
                info = client.publish(topic, payload_str, qos=qos, retain=retain)
                # Optionally, wait for publish to complete for QoS>0
                if qos > 0:
                    info.wait_for_publish(timeout=10)
                logging.debug(f"[{host}] Sensor {sensor_id} -> {topic}: {payload_str}")
            except Exception as e:
                logging.error(f"[{host}] ERROR Sensor {sensor_id}: {e}")

        # Sleep with optional jitter and interruption support
        sleep_time = publish_interval
        if jitter and publish_interval > 0:
            # jitter is a fraction of interval; choose in [1-jitter, 1+jitter] * interval
            low = max(0.0, 1.0 - max(0.0, jitter))
            high = 1.0 + max(0.0, jitter)
            sleep_time = publish_interval * rng.uniform(low, high)
        if stop_event.wait(timeout=sleep_time):
            break


# ==========================
# Main
# ==========================
def parse_args(argv: List[str]) -> argparse.Namespace:
    default_config = Path(__file__).with_name("brokers.yml")
    parser = argparse.ArgumentParser(description="Multi-broker sensor simulator")
    parser.add_argument("-c", "--config", default=str(default_config), help="Path to brokers config (YAML/JSON)")
    parser.add_argument("-n", "--sensors", type=int, default=50, help="Number of virtual sensors")
    parser.add_argument("-i", "--interval", type=float, default=5.0, help="Seconds between publishing")
    parser.add_argument("-t", "--topic-template", default="sensor/{sensor_id}/temperature", help="MQTT topic template")
    parser.add_argument("--qos", type=int, choices=[0, 1, 2], default=0, help="MQTT QoS level")
    parser.add_argument("--retain", action="store_true", help="Publish with retain flag")
    parser.add_argument("--payload", choices=["plain", "json"], default="plain", help="Payload format")
    parser.add_argument("--min", dest="temp_min", type=float, default=20.0, help="Min temperature value")
    parser.add_argument("--max", dest="temp_max", type=float, default=30.0, help="Max temperature value")
    parser.add_argument("--client-id-prefix", default=None, help="Client ID prefix for MQTT connections")
    parser.add_argument("--connect-timeout", type=float, default=5.0, help="Seconds to wait for MQTT connections before starting publishing")
    parser.add_argument("--ha-discovery", action="store_true", help="Publish Home Assistant MQTT Discovery config before publishing")
    parser.add_argument("--discovery-prefix", default="homeassistant", help="Home Assistant discovery prefix")
    parser.add_argument("--model", choices=["uniform", "drift"], default="uniform", help="Temperature model: uniform random or drifting")
    parser.add_argument("--noise-sd", type=float, default=0.2, help="Std dev of Gaussian noise per publish when model=drift")
    parser.add_argument("--drift-per-minute", type=float, default=0.0, help="Deterministic drift per minute when model=drift (positive warms up)")
    parser.add_argument("--jitter", type=float, default=0.0, help="Sleep jitter as a fraction of interval (e.g., 0.1 = ±10%)")
    parser.add_argument("--seed", type=int, default=None, help="Global seed for deterministic runs (overrides per-sensor seeding)")
    parser.add_argument("--dry-run", action="store_true", help="Do not connect/publish, just log events")
    parser.add_argument("--once", action="store_true", help="Publish once and exit")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    setup_logging(args.log_level)

    try:
        brokers = load_brokers(args.config)
    except Exception as e:
        logging.error(f"Failed to load brokers: {e}")
        return 2

    if args.temp_min >= args.temp_max:
        logging.error("--min must be less than --max")
        return 2

    # Initialize clients for all brokers
    broker_clients: List[Tuple[mqtt.Client, Broker]] = []
    if not args.dry_run:
        for b in brokers:
            try:
                client = create_client(b, client_id_prefix=args.client_id_prefix)
                broker_clients.append((client, b))
            except Exception as e:
                logging.error(f"[{b.host}] Failed to create/connect client: {e}")
    else:
        broker_clients = [(None, b) for b in brokers]  # type: ignore

    stop_event = threading.Event()

    def handle_signal(signum, frame):  # noqa: ARG001
        logging.info("Stopping simulator...")
        stop_event.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # Wait briefly for connections before starting threads
    if not args.dry_run and broker_clients:
        deadline = time.time() + max(0.0, getattr(args, "connect_timeout", 5.0))
        while time.time() < deadline:
            try:
                if all(getattr(c, "is_connected", lambda: False)() for c, _ in broker_clients):
                    break
            except Exception:
                pass
            time.sleep(0.1)

    # Publish Home Assistant discovery configs once (retained)
    if not args.dry_run and args.ha_discovery and broker_clients:
        publish_ha_discovery(
            broker_clients=broker_clients,
            sensors=args.sensors,
            topic_template=args.topic_template,
            discovery_prefix=args.discovery_prefix,
            payload_format=args.payload,
        )

    threads: List[threading.Thread] = []
    for sensor_id in range(1, args.sensors + 1):
        t = threading.Thread(
            target=sensor_worker,
            args=(
                sensor_id,
                broker_clients,
                args.topic_template,
                args.interval,
                stop_event,
            ),
            kwargs={
                "qos": args.qos,
                "retain": args.retain,
                "payload_format": args.payload,
                "temp_min": args.temp_min,
                "temp_max": args.temp_max,
                "dry_run": args.dry_run,
                "model": args.model,
                "noise_sd": args.noise_sd,
                "drift_per_minute": args.drift_per_minute,
                "jitter": args.jitter,
                "seed": args.seed,
            },
            daemon=True,
        )
        t.start()
        threads.append(t)

    logging.info(
        f"Started {args.sensors} sensors, publishing every {args.interval}s to {len(brokers)} broker(s)."
    )

    # For --once, publish once and exit cleanly
    if args.once:
        time.sleep(max(0.1, args.interval))
        stop_event.set()

    # Keep main thread alive until stop
    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    finally:
        # Cleanup
        for t in threads:
            t.join(timeout=2)
        if not args.dry_run:
            for client, b in broker_clients:
                try:
                    client.loop_stop()
                    client.disconnect()
                except Exception:
                    pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
