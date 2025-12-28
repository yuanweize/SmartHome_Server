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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import paho.mqtt.client as mqtt

try:
    import yaml
except ImportError:
    yaml = None

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
            tls_insecure=bool(item.get("tls_insecure", False)),
            
            keepalive=int(item.get("keepalive", 60)),
            client_id=item.get("client_id"),
            _config_dir=config_path.parent
        )

    def _resolve_path(self, path_str: str | None) -> str | None:
        """Resolves relative paths based on config file location."""
        if not path_str:
            return None
        path = Path(path_str)
        if not path.is_absolute():
            path = self._config_dir / path
        
        if not path.exists():
            logging.warning(f"Certificate file not found: {path}")
        return str(path)

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
            
            ca_path = self._resolve_path(self.ca_file)
            cert_path = self._resolve_path(self.cert_file)
            key_path = self._resolve_path(self.key_file)

            # Basic TLS (Server verification)
            # If no CA is provided, paho uses system defaults
            client.tls_set(
                ca_certs=ca_path,
                certfile=cert_path,
                keyfile=key_path,
                cert_reqs=ssl.CERT_REQUIRED if not self.tls_insecure else ssl.CERT_NONE,
                tls_version=ssl.PROTOCOL_TLS_CLIENT,
                ciphers=None
            )

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
        logging.info(f"[{host}] Connected via {client._ssl.version() if client._ssl else 'TCP'}")
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
def publish_ha_discovery(broker_clients, sensors, topic_temp, disc_prefix):
    """Publish Home Assistant Auto-Discovery Payloads (Retained)"""
    for i in range(1, sensors + 1):
        uid = f"sim_sensor_{i}"
        topic_state = topic_temp.format(sensor_id=i)
        
        # config payload
        payload = {
            "name": f"Simulated Sensor {i}",
            "unique_id": uid,
            "state_topic": topic_state,
            "device_class": "temperature",
            "unit_of_measurement": "°C",
            "value_template": "{{ value_json.value }}",
            "device": {
                "identifiers": [uid],
                "name": f"Sim Node {i}",
                "model": "Python Simulator",
                "manufacturer": "Eurun Lab"
            }
        }
        
        topic_config = f"{disc_prefix}/sensor/{uid}/config"
        pl_str = json.dumps(payload)
        
        for client, broker in broker_clients:
            if client and client.is_connected():
                client.publish(topic_config, pl_str, retain=True)

def sensor_worker(sensor_id, broker_clients, topic_temp, interval, stop_ev, 
                  temp_min, temp_max, model, dry_run):
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
        payload = json.dumps({
            "sensor_id": sensor_id,
            "value": val,
            "ts": int(time.time())
        })
        topic = topic_temp.format(sensor_id=sensor_id)

        # Publish
        for client, broker in broker_clients:
            if dry_run:
                logging.info(f"[DRY] {broker.host} -> {topic}: {val}")
                continue
                
            if client and client.is_connected():
                client.publish(topic, payload)
        
        # Sleep
        if stop_ev.wait(interval):
            break

# ==========================
# Main Entry
# ==========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="brokers.yml", help="Config file path")
    parser.add_argument("-n", "--sensors", type=int, default=10, help="Number of sensors")
    parser.add_argument("-i", "--interval", type=float, default=5.0, help="Interval seconds")
    parser.add_argument("--topic", default="sensor/{sensor_id}/data", help="Topic template")
    parser.add_argument("--ha-discovery", action="store_true", help="Enable HA Discovery")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    setup_logging("INFO")

    # Load Brokers
    try:
        brokers = load_brokers(args.config)
    except Exception as e:
        logging.error(f"Config Error: {e}")
        return

    # Init Clients
    broker_clients = []
    if not args.dry_run:
        for b in brokers:
            try:
                c = b.create_client(client_id_prefix="sim-runner")
                broker_clients.append((c, b))
            except Exception as e:
                logging.error(f"Failed to init broker {b.host}: {e}")
    else:
        broker_clients = [(None, b) for b in brokers]

    # HA Discovery
    if args.ha_discovery and not args.dry_run:
        logging.info("Waiting for connections to send HA discovery...")
        time.sleep(2) # Brief wait for connects
        publish_ha_discovery(broker_clients, args.sensors, args.topic, "homeassistant")

    # Start Threads
    stop_ev = threading.Event()
    threads = []
    
    logging.info(f"Starting {args.sensors} sensors, interval {args.interval}s...")
    
    for i in range(1, args.sensors + 1):
        t = threading.Thread(target=sensor_worker, args=(
            i, broker_clients, args.topic, args.interval, stop_ev, 
            20.0, 30.0, "drift", args.dry_run
        ), daemon=True)
        t.start()
        threads.append(t)

    # Loop until Ctrl+C
    try:
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