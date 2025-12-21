#!/usr/bin/env python3
"""
Multi-Broker Sensor Simulator (Optimized for mTLS)
- Supports MQTT over SSL/TLS (including mTLS with client certs)
- Auto-resolves certificate paths relative to config file
- Optimized logging and error handling
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
import ssl  # Added for TLS support
import atexit
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import paho.mqtt.client as mqtt

try:
    import yaml
except ImportError:
    yaml = None


def _looks_like_pem(text: Optional[str]) -> bool:
    if not text:
        return False
    return "-----BEGIN" in text


def _normalize_pem(text: str) -> str:
    normalized = text.strip().replace("\r\n", "\n") + "\n"
    return normalized


def _materialize_pem_bundle(
    *,
    ca_pem: Optional[str],
    cert_pem: Optional[str],
    key_pem: Optional[str],
    label: str,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Write inline PEM blobs to temp files and return their paths."""

    if not (ca_pem or cert_pem or key_pem):
        return None, None, None

    temp_dir = tempfile.mkdtemp(prefix=f"mqtt-certs-{label}-")
    atexit.register(shutil.rmtree, temp_dir, ignore_errors=True)

    def write_one(filename: str, pem_text: Optional[str]) -> Optional[str]:
        if not pem_text:
            return None
        file_path = Path(temp_dir) / filename
        file_path.write_text(_normalize_pem(pem_text), encoding="utf-8")
        try:
            os.chmod(file_path, 0o600)
        except Exception:
            # Best-effort; ignore on platforms where chmod is restricted.
            pass
        return str(file_path)

    return (
        write_one("ca.pem", ca_pem),
        write_one("client.pem", cert_pem),
        write_one("client.key", key_pem),
    )

# ==========================
# Broker Model & Config
# ==========================
@dataclass
class Broker:
    host: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    tls: bool = False
    
    # New fields for mTLS
    ca_file: Optional[str] = None
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    ca_pem: Optional[str] = None
    cert_pem: Optional[str] = None
    key_pem: Optional[str] = None
    tls_insecure: bool = False
    
    keepalive: int = 60
    client_id: Optional[str] = None
    
    # Store the base path to resolve relative cert paths
    _config_dir: Path = Path(".")

    @classmethod
    def from_obj(cls, item: Any, config_path: Path) -> "Broker":
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
            
            # mTLS paths
            ca_file=item.get("ca_file"),
            cert_file=item.get("cert_file"),
            key_file=item.get("key_file"),

            # mTLS inline PEM (preferred if provided)
            ca_pem=item.get("ca_pem"),
            cert_pem=item.get("cert_pem"),
            key_pem=item.get("key_pem"),
            tls_insecure=bool(item.get("tls_insecure", False)),
            
            keepalive=int(item.get("keepalive", 60)),
            client_id=item.get("client_id"),
            _config_dir=config_path.parent
        )

    def _resolve_path(self, path_str: Optional[str]) -> Optional[str]:
        """Resolves relative paths based on config file location."""
        if not path_str:
            return None
        path = Path(path_str)
        if not path.is_absolute():
            path = self._config_dir / path
        return str(path)

    def _select_tls_material(self) -> Tuple[Dict[str, Optional[str]], Dict[str, Optional[str]]]:
        """Pick TLS material with priority and fallback.

        Priority rules:
        - Prefer inline PEM from brokers.yml (ca_pem/cert_pem/key_pem).
        - If a *_file field contains PEM text, treat it as inline PEM.
        - If primary selection fails, fallback to file-based paths (if present).
        """

        inline_ca = self.ca_pem or (self.ca_file if _looks_like_pem(self.ca_file) else None)
        inline_cert = self.cert_pem or (self.cert_file if _looks_like_pem(self.cert_file) else None)
        inline_key = self.key_pem or (self.key_file if _looks_like_pem(self.key_file) else None)

        file_ca = None if _looks_like_pem(self.ca_file) else self._resolve_path(self.ca_file)
        file_cert = None if _looks_like_pem(self.cert_file) else self._resolve_path(self.cert_file)
        file_key = None if _looks_like_pem(self.key_file) else self._resolve_path(self.key_file)

        primary = {
            "ca_pem": inline_ca,
            "cert_pem": inline_cert,
            "key_pem": inline_key,
            "ca_file": file_ca,
            "cert_file": file_cert,
            "key_file": file_key,
        }
        fallback = {
            "ca_file": file_ca,
            "cert_file": file_cert,
            "key_file": file_key,
        }

        return primary, fallback

    def create_client(self, client_id_prefix: Optional[str] = None) -> mqtt.Client:
        cid = self.client_id
        if not cid:
            # Generate a random ID if not provided, adding prefix if available
            suffix = f"{random.randint(1000,9999)}"
            cid = f"{client_id_prefix}-{suffix}" if client_id_prefix else f"sim-{suffix}"

        client = mqtt.Client(client_id=cid, clean_session=True)
        client.user_data_set({"broker_host": self.host})
        
        # Callbacks
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect

        # Auth
        if self.username is not None:
            client.username_pw_set(self.username, self.password)

        # TLS / mTLS Configuration
        if self.tls:
            logging.debug(f"[{self.host}] Configuring TLS...")

            primary, fallback = self._select_tls_material()

            # Build primary file paths (inline PEM materialized to temp files as needed)
            ca_temp, cert_temp, key_temp = _materialize_pem_bundle(
                ca_pem=primary.get("ca_pem"),
                cert_pem=primary.get("cert_pem"),
                key_pem=primary.get("key_pem"),
                label=self.host.replace("/", "_").replace(":", "_"),
            )

            ca_primary = ca_temp or primary.get("ca_file")
            cert_primary = cert_temp or primary.get("cert_file")
            key_primary = key_temp or primary.get("key_file")

            def warn_missing(path: Optional[str], label: str) -> None:
                if not path:
                    return
                if not Path(path).exists():
                    logging.warning(f"[{self.host}] {label} not found: {path}")

            # Warn only for file-based paths.
            if ca_primary and ca_primary == primary.get("ca_file"):
                warn_missing(ca_primary, "CA file")
            if cert_primary and cert_primary == primary.get("cert_file"):
                warn_missing(cert_primary, "Client cert file")
            if key_primary and key_primary == primary.get("key_file"):
                warn_missing(key_primary, "Client key file")

            def try_tls_set(label: str, ca_path: Optional[str], cert_path: Optional[str], key_path: Optional[str]) -> None:
                logging.debug(
                    f"[{self.host}] TLS material source={label} ca={bool(ca_path)} cert={bool(cert_path)} key={bool(key_path)}"
                )
                client.tls_set(
                    ca_certs=ca_path,
                    certfile=cert_path,
                    keyfile=key_path,
                    cert_reqs=ssl.CERT_REQUIRED if not self.tls_insecure else ssl.CERT_NONE,
                    tls_version=ssl.PROTOCOL_TLS_CLIENT,
                    ciphers=None,
                )

            # Primary attempt
            try:
                try_tls_set("primary", ca_primary, cert_primary, key_primary)
            except Exception as e:
                # If primary used inline PEM and we also have file paths, fallback to file.
                has_inline = bool(primary.get("ca_pem") or primary.get("cert_pem") or primary.get("key_pem"))
                has_files = bool(fallback.get("ca_file") or fallback.get("cert_file") or fallback.get("key_file"))
                if has_inline and has_files:
                    logging.warning(f"[{self.host}] TLS primary config failed: {e}; trying file-based fallback")
                    try_tls_set("fallback(file)", fallback.get("ca_file"), fallback.get("cert_file"), fallback.get("key_file"))
                else:
                    raise

            if self.tls_insecure:
                client.tls_insecure_set(True)
                logging.warning(f"[{self.host}] TLS Insecure Mode Enabled (Skipping Verify)")

        # Connection
        client.reconnect_delay_set(min_delay=1, max_delay=60)
        try:
            client.connect_async(self.host, self.port, keepalive=self.keepalive)
            client.loop_start()
        except Exception as e:
            logging.error(f"[{self.host}] Connection setup failed: {e}")
            
        return client


def load_brokers(config_path: str) -> List[Broker]:
    path = Path(config_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    text = path.read_text(encoding="utf-8")
    data: Any = None

    # Load YAML or JSON
    if yaml is not None:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            pass
    
    if data is None:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse config (YAML or JSON): {e}")

    if not isinstance(data, list):
        raise ValueError("Config must be a list of broker objects")

    return [Broker.from_obj(item, path) for item in data]


def setup_logging(level: str) -> None:
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


# ==========================
# MQTT Callbacks
# ==========================
def on_connect(client, userdata, flags, rc):
    host = userdata.get("broker_host", "?")
    if rc == 0:
        transport = "TLS" if getattr(client, "_ssl", None) else "TCP"
        logging.info(f"[{host}] Connected via {transport}")
    else:
        # Paho return codes mapping
        rc_map = {1: "Protocol ver mismatch", 2: "Invalid ID", 3: "Server unavailable", 4: "Bad auth", 5: "Not authorized"}
        logging.warning(f"[{host}] Connection failed: {rc_map.get(rc, rc)}")


def on_disconnect(client, userdata, rc):
    host = userdata.get("broker_host", "?")
    if rc != 0:
        logging.warning(f"[{host}] Unexpected disconnect (rc={rc}), auto-reconnecting...")
    else:
        logging.info(f"[{host}] Disconnected")


# ==========================
# Simulation Logic
# ==========================
def publish_ha_discovery(
    broker_clients,
    sensors: int,
    topic_temp: str,
    disc_prefix: str,
    payload_format: str,
    qos: int,
) -> None:
    """Publish Home Assistant MQTT Discovery payloads (retained)."""
    for i in range(1, sensors + 1):
        uid = f"sim_sensor_{i}"
        topic_state = topic_temp.format(sensor_id=i)
        
        # config payload
        payload: Dict[str, Any] = {
            "name": f"Simulated Sensor {i}",
            "unique_id": uid,
            "state_topic": topic_state,
            "device_class": "temperature",
            "unit_of_measurement": "°C",
            "device": {
                "identifiers": [uid],
                "name": f"Sim Node {i}",
                "model": "Python Simulator",
                "manufacturer": "Eurun Lab"
            }
        }

        if payload_format == "json":
            payload["value_template"] = "{{ value_json.value }}"
        
        topic_config = f"{disc_prefix}/sensor/{uid}/config"
        pl_str = json.dumps(payload)
        
        any_published = False
        for client, broker in broker_clients:
            if client and client.is_connected():
                client.publish(topic_config, pl_str, qos=qos, retain=True)
                any_published = True
            else:
                logging.debug(f"[HA] broker not connected yet: {broker.host}")

        if not any_published:
            logging.warning(f"[HA] Discovery not published for sensor {i} (no broker connected)")

def sensor_worker(
    sensor_id: int,
    broker_clients,
    topic_temp: str,
    interval: float,
    stop_ev: threading.Event,
    temp_min: float,
    temp_max: float,
    model: str,
    dry_run: bool,
    payload_format: str,
    qos: int,
    retain: bool,
    once: bool,
):
    """Worker thread for a single sensor"""
    rng = random.Random(sensor_id)
    current_val = (temp_min + temp_max) / 2
    
    while not stop_ev.is_set():
        # Generate value
        if model == "uniform":
            val = rng.uniform(temp_min, temp_max)
        else:
            # Simple random walk
            current_val += rng.uniform(-0.5, 0.5)
            current_val = max(temp_min, min(temp_max, current_val))
            val = current_val

        val = round(val, 2)
        
        # Payload
        if payload_format == "json":
            payload = json.dumps({
                "sensor_id": sensor_id,
                "value": val,
                "ts": int(time.time())
            })
        else:
            payload = str(val)
        topic = topic_temp.format(sensor_id=sensor_id)

        # Publish
        for client, broker in broker_clients:
            if dry_run:
                logging.info(f"[DRY] {broker.host} -> {topic}: {val}")
                continue
                
            if client and client.is_connected():
                client.publish(topic, payload, qos=qos, retain=retain)
            else:
                logging.debug(f"[{broker.host}] Skip publish: not connected")
        
        # Sleep
        if once:
            break
        if stop_ev.wait(interval):
            break


# ==========================
# Main Entry
# ==========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="sensors/brokers.yml", help="Config file path")
    parser.add_argument("-n", "--sensors", type=int, default=50, help="Number of sensors")
    parser.add_argument("-i", "--interval", type=float, default=5.0, help="Interval seconds")
    parser.add_argument("-t", "--topic-template", dest="topic", default="sensor/{sensor_id}/data", help="Topic template")
    parser.add_argument("--payload", choices=["plain", "json"], default="json", help="Payload format")
    parser.add_argument("--qos", type=int, choices=[0, 1, 2], default=0, help="MQTT QoS")
    parser.add_argument("--retain", action="store_true", help="Set retain flag on state publishes")
    parser.add_argument("--min", dest="temp_min", type=float, default=20.0, help="Min temperature")
    parser.add_argument("--max", dest="temp_max", type=float, default=30.0, help="Max temperature")
    parser.add_argument("--model", choices=["uniform", "drift"], default="drift")
    parser.add_argument("--client-id-prefix", default="sim-runner")
    parser.add_argument("--connect-timeout", type=float, default=5.0)
    parser.add_argument("--ha-discovery", action="store_true", help="Enable HA Discovery")
    parser.add_argument("--discovery-prefix", default="homeassistant")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true", help="Publish one cycle then exit")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()

    setup_logging(args.log_level)

    # Load Brokers
    try:
        brokers = load_brokers(args.config)
    except Exception as e:
        logging.error(f"Config Error: {e}")
        raise SystemExit(2)

    logging.info(f"Loaded {len(brokers)} broker(s) from {args.config}")

    # Init Clients
    broker_clients = []
    if not args.dry_run:
        for b in brokers:
            try:
                c = b.create_client(client_id_prefix=args.client_id_prefix)
                broker_clients.append((c, b))
            except Exception as e:
                logging.error(f"Failed to init broker {b.host}: {e}")
    else:
        broker_clients = [(None, b) for b in brokers]

    # HA Discovery
    if args.ha_discovery and not args.dry_run:
        logging.info("Waiting for MQTT connections to send HA discovery...")
        deadline = time.time() + float(args.connect_timeout)
        while time.time() < deadline:
            if any(c and c.is_connected() for c, _ in broker_clients):
                break
            time.sleep(0.2)

        publish_ha_discovery(
            broker_clients,
            args.sensors,
            args.topic,
            args.discovery_prefix,
            args.payload,
            args.qos,
        )

    # Start Threads
    stop_ev = threading.Event()
    threads = []
    
    logging.info(
        f"Started {args.sensors} sensors, publishing every {args.interval}s to {len(brokers)} broker(s)."
    )
    
    for i in range(1, args.sensors + 1):
        t = threading.Thread(target=sensor_worker, args=(
            i, broker_clients, args.topic, args.interval, stop_ev, 
            args.temp_min, args.temp_max, args.model, args.dry_run,
            args.payload, args.qos, args.retain, args.once,
        ), daemon=True)
        t.start()
        threads.append(t)

    # Loop until Ctrl+C (or once)
    try:
        if args.once:
            stop_ev.set()
            for t in threads:
                t.join()
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping...")
        stop_ev.set()
        for t in threads:
            t.join()
        for c, _ in broker_clients:
            if c: c.loop_stop(); c.disconnect()

if __name__ == "__main__":
    main()