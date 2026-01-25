"""TLS handshake benchmark for thesis-grade measurements."""

from __future__ import annotations

import json
import logging
import math
import statistics
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .broker import Broker
from .entities import MQTTContext
from .utils import ensure_dir, iso_utc, percentile_sorted


class HandshakeRecorder:
    """Thread-safe recorder for connection attempts."""

    def __init__(self, out_jsonl_path: Path) -> None:
        self.out_jsonl_path = out_jsonl_path
        ensure_dir(out_jsonl_path.parent)
        self._lock = threading.Lock()

    def write(self, record: Dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False, sort_keys=True)
        with self._lock:
            with self.out_jsonl_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")


def _compute_stats(values: List[float]) -> Dict[str, Any]:
    """Compute statistical summary from latency values."""
    if not values:
        return {}
    
    values_sorted = sorted(values)
    n = len(values_sorted)
    mean = statistics.fmean(values_sorted)
    stdev = statistics.stdev(values_sorted) if n >= 2 else 0.0
    sem = stdev / math.sqrt(n) if n >= 2 else 0.0
    
    ci95 = None
    if n >= 30:
        z = 1.96
        ci95 = [mean - z * sem, mean + z * sem]
    
    return {
        "n": n,
        "min": values_sorted[0],
        "max": values_sorted[-1],
        "mean": mean,
        "stdev": stdev,
        "sem": sem,
        "ci95_mean_normal_approx": ci95,
        "p50": percentile_sorted(values_sorted, 50),
        "p90": percentile_sorted(values_sorted, 90),
        "p95": percentile_sorted(values_sorted, 95),
        "p99": percentile_sorted(values_sorted, 99),
    }


def summarize_handshake_jsonl(jsonl_path: Path) -> Dict[str, Any]:
    """Generate statistical summary from JSONL records."""
    latencies_ms: List[float] = []
    total, ok, failed = 0, 0, 0
    by_broker: Dict[str, Dict[str, Any]] = {}

    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                rec = json.loads(line)
            except Exception:
                failed += 1
                continue

            broker_key = str(rec.get("broker", {}).get("host", "?"))
            if broker_key not in by_broker:
                by_broker[broker_key] = {"total": 0, "ok": 0, "failed": 0, "latencies_ms": []}
            by_broker[broker_key]["total"] += 1

            latency = rec.get("connect_latency_ms")
            is_ok = (rec.get("rc") == 0) and (latency is not None)
            
            if is_ok:
                ok += 1
                by_broker[broker_key]["ok"] += 1
                lat = float(latency)
                latencies_ms.append(lat)
                by_broker[broker_key]["latencies_ms"].append(lat)
            else:
                failed += 1
                by_broker[broker_key]["failed"] += 1

    summary = {
        "schema": "smarthome.handshake.summary.v1",
        "source": str(jsonl_path),
        "generated_at_utc": iso_utc(),
        "records_total": total,
        "records_ok": ok,
        "records_failed": failed,
        "latency_unit": "ms",
        "percentile_method": "linear_interpolation_between_closest_ranks",
        "overall": _compute_stats(latencies_ms),
        "by_broker": {},
    }

    for broker_key, v in by_broker.items():
        summary["by_broker"][broker_key] = {
            "records_total": v["total"],
            "records_ok": v["ok"],
            "records_failed": v["failed"],
            "stats": _compute_stats(v["latencies_ms"]),
        }

    return summary


def plot_handshake_jsonl(jsonl_path: Path, *, out_prefix: Path) -> List[str]:
    """Generate histogram and ECDF plots (requires matplotlib)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    latencies_ms: List[float] = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if rec.get("rc") == 0 and rec.get("connect_latency_ms") is not None:
                    latencies_ms.append(float(rec["connect_latency_ms"]))
            except Exception:
                continue

    if not latencies_ms:
        raise ValueError(f"No successful handshake records in {jsonl_path}")

    latencies_ms.sort()
    n = len(latencies_ms)
    out_files: List[str] = []

    # Histogram
    plt.figure(figsize=(10, 6))
    plt.hist(latencies_ms, bins=60)
    plt.title("MQTT Connect Latency (TLS handshake included)")
    plt.xlabel("Connect latency (ms)")
    plt.ylabel("Count")
    hist_path = out_prefix.with_name(out_prefix.name + ".hist.png")
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()
    out_files.append(str(hist_path))

    # ECDF
    plt.figure(figsize=(10, 6))
    y = [(i + 1) / n for i in range(n)]
    plt.step(latencies_ms, y, where="post")
    plt.title("ECDF of MQTT Connect Latency")
    plt.xlabel("Connect latency (ms)")
    plt.ylabel("ECDF")
    ecdf_path = out_prefix.with_name(out_prefix.name + ".ecdf.png")
    plt.tight_layout()
    plt.savefig(ecdf_path)
    plt.close()
    out_files.append(str(ecdf_path))

    return out_files


def _handshake_output_paths(out: str, *, worker_id: Optional[int]) -> Tuple[Path, Path, Path]:
    """Return (jsonl_path, summary_path, plot_prefix)."""
    base = Path(out).expanduser()
    
    if base.suffix.lower() == ".jsonl":
        jsonl_path = base
    elif base.suffix:
        jsonl_path = base.with_suffix(base.suffix + ".jsonl")
    else:
        ensure_dir(base)
        suffix = f"w{worker_id}" if worker_id is not None else "w0"
        jsonl_path = base / f"handshake.{suffix}.jsonl"

    return jsonl_path, jsonl_path.with_suffix(".summary.json"), jsonl_path.with_suffix("")


def run_handshake_benchmark(
    *,
    brokers: List[Broker],
    client_id_prefix: str,
    samples: int,
    interval_s: float,
    timeout_s: float,
    out: str,
    plot: bool,
    worker_id: Optional[int],
    on_connect,
    on_disconnect,
    on_message,
    warmup: int = 3,
) -> None:
    """Run connect/disconnect benchmark and record latencies.
    
    Note: Measures full MQTT CONNECT latency including:
    - TCP handshake
    - TLS handshake (if enabled)
    - MQTT CONNECT/CONNACK exchange
    
    Args:
        warmup: Number of warmup connections to perform (not recorded).
                Used to prime DNS cache and establish baseline.
    """
    if samples <= 0:
        return

    jsonl_path, summary_path, plot_prefix = _handshake_output_paths(out, worker_id=worker_id)
    recorder = HandshakeRecorder(jsonl_path)

    logging.info(f"Handshake benchmark: samples={samples}, warmup={warmup}, brokers={len(brokers)}, out={jsonl_path}")

    empty_ctx = MQTTContext(command_topics=[], command_handlers={})

    # Warmup phase: prime DNS cache and connection pools
    if warmup > 0:
        logging.info(f"Warmup: {warmup} connection(s) per broker (not recorded)")
        for _ in range(warmup):
            for broker in brokers:
                _do_single_connect(
                    broker=broker,
                    client_id_prefix=f"{client_id_prefix}-warmup",
                    empty_ctx=empty_ctx,
                    timeout_s=timeout_s,
                    on_connect=on_connect,
                    on_disconnect=on_disconnect,
                    on_message=on_message,
                    recorder=None,  # Don't record warmup
                    sample_idx=0,
                    worker_id=worker_id,
                )
                time.sleep(0.1)

    for sample_idx in range(1, samples + 1):
        for broker in brokers:
            _do_single_connect(
                broker=broker,
                client_id_prefix=f"{client_id_prefix}-hs{sample_idx}",
                empty_ctx=empty_ctx,
                timeout_s=timeout_s,
                on_connect=on_connect,
                on_disconnect=on_disconnect,
                on_message=on_message,
                recorder=recorder,
                sample_idx=sample_idx,
                worker_id=worker_id,
            )

        if interval_s > 0:
            time.sleep(interval_s)

    # Generate summary
    summary = summarize_handshake_jsonl(jsonl_path)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    logging.info(f"Handshake summary written: {summary_path}")

    # Generate plots
    if plot:
        try:
            out_files = plot_handshake_jsonl(jsonl_path, out_prefix=plot_prefix)
            logging.info(f"Handshake plots written: {', '.join(out_files)}")
        except ImportError:
            logging.warning("matplotlib not installed; pip install matplotlib")
        except Exception as e:
            logging.warning(f"Failed to generate plots: {e}")


def _do_single_connect(
    *,
    broker: Broker,
    client_id_prefix: str,
    empty_ctx: MQTTContext,
    timeout_s: float,
    on_connect,
    on_disconnect,
    on_message,
    recorder: Optional[HandshakeRecorder],
    sample_idx: int,
    worker_id: Optional[int],
) -> None:
    """Perform a single connect/disconnect cycle."""
    connect_event = threading.Event()
    disconnect_event = threading.Event()

    userdata_extra = {
        "connect_event": connect_event,
        "disconnect_event": disconnect_event,
        "connect_started_at": None,
        "handshake_recorder": recorder,
        "sample_index": sample_idx,
        "worker_id": worker_id,
        "broker_port": broker.port,
        "broker_tls": broker.tls,
    }

    client = broker.create_client(
        client_id_prefix=client_id_prefix,
        mqtt_context=empty_ctx,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        on_message=on_message,
        auto_connect=False,
        userdata_extra=userdata_extra,
    )

    error: Optional[str] = None
    try:
        if isinstance(getattr(client, "_userdata", None), dict):
            client._userdata["connect_started_at"] = time.perf_counter()
        client.connect_async(broker.host, broker.port, keepalive=broker.keepalive)
        client.loop_start()

        if not connect_event.wait(timeout=timeout_s):
            error = f"connect_timeout_{timeout_s}s"
    except Exception as e:
        error = f"connect_exception:{e}"
    finally:
        try:
            client.disconnect()
        except Exception:
            pass
        disconnect_event.wait(timeout=2.0)
        try:
            client.loop_stop(force=True)
        except (TypeError, Exception):
            try:
                client.loop_stop()
            except Exception:
                pass

    if error is not None and recorder is not None:
        recorder.write({
            "schema": "smarthome.handshake.record.v1",
            "ts_unix": time.time(),
            "ts_iso": iso_utc(),
            "worker_id": worker_id,
            "sample": sample_idx,
            "broker": {"host": broker.host, "port": broker.port, "tls": broker.tls},
            "client_id": None,
            "rc": None,
            "connect_latency_ms": None,
            "error": error,
        })

# [CodeRabbit Audit Trigger 1769364389]
