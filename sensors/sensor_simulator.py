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
import time
import random
import ssl  # Added for TLS support
import atexit
import shutil
import tempfile
import heapq
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional, Callable

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

    def create_client(self, *, client_id_prefix: Optional[str], mqtt_context: "MQTTContext") -> mqtt.Client:
        cid = self.client_id
        if not cid:
            # Generate a random ID if not provided, adding prefix if available
            suffix = f"{random.randint(1000,9999)}"
            cid = f"{client_id_prefix}-{suffix}" if client_id_prefix else f"sim-{suffix}"

        client = mqtt.Client(client_id=cid, clean_session=True)
        client.user_data_set({"broker_host": self.host, "ctx": mqtt_context})
        
        # Callbacks
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

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
            client.connect_async(self.host, int(self.port), keepalive=int(self.keepalive))
            client.loop_start()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to broker {self.host}:{self.port}: {e}")

        return client

def load_config(config_path: str) -> Tuple[Any, Path]:
    path = Path(config_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    text = path.read_text(encoding="utf-8")
    data: Any = None

    if yaml is not None:
        try:
            data = yaml.safe_load(text)
        except Exception:
            data = None

    if data is None:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse config (YAML or JSON): {e}")

    return data, path


def load_brokers(config_path: str) -> Tuple[List[Broker], Any, Path]:
    data, path = load_config(config_path)

    brokers_obj: Any
    if isinstance(data, list):
        brokers_obj = data
        rest = None
    elif isinstance(data, dict):
        brokers_obj = data.get("brokers")
        rest = data
    else:
        raise ValueError("Config must be either a list of brokers or an object with 'brokers'")

    if not isinstance(brokers_obj, list):
        raise ValueError("'brokers' must be a list")

    brokers = [Broker.from_obj(item, path) for item in brokers_obj]
    return brokers, rest, path


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

        ctx: MQTTContext = userdata.get("ctx")
        if ctx is not None:
            for topic in ctx.command_topics:
                try:
                    client.subscribe(topic)
                except Exception as e:
                    logging.warning(f"[{host}] Subscribe failed {topic}: {e}")
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


def on_message(client, userdata, msg):
    ctx: MQTTContext = userdata.get("ctx")
    if ctx is None:
        return
    try:
        payload = msg.payload.decode("utf-8", errors="replace")
    except Exception:
        payload = ""

    handler = ctx.command_handlers.get(msg.topic)
    if handler is None:
        return
    try:
        handler(payload)
    except Exception as e:
        host = userdata.get("broker_host", "?")
        logging.warning(f"[{host}] Command handler failed topic={msg.topic}: {e}")


# ==========================
# Simulator Config
# ==========================
@dataclass
class EntityDef:
    id: str
    kind: str  # sensor | binary_sensor | switch | light
    name: str
    count: int = 1
    device_class: Optional[str] = None
    unit: Optional[str] = None
    interval: float = 5.0
    model: str = "drift"  # for sensors/binary sensors
    min: Optional[float] = None
    max: Optional[float] = None
    precision: int = 2
    state_payload: str = "json"  # json | plain
    initial: Any = None

    # Actuators
    commandable: bool = False


@dataclass
class AutomationConfig:
    motion_entity: Optional[str] = None
    light_entity: Optional[str] = None
    motion_hold_seconds: float = 30.0
    switch_entity: Optional[str] = None
    sensor_entity: Optional[str] = None
    delta_per_minute_on: float = 1.0
    delta_per_minute_off: float = -0.2


@dataclass
class SimulationConfig:
    devices: int = 10
    base_topic: str = "smarthome/sim"
    discovery_prefix: str = "homeassistant"
    publish_qos: int = 0
    retain_state: bool = False
    connect_timeout: float = 5.0
    client_id_prefix: str = "sim"
    ha_discovery: bool = True
    log_summary_interval: float = 30.0
    jitter: float = 0.0
    entities: List[EntityDef] = None
    automation: Optional[AutomationConfig] = None
    device: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class EntityInstance:
    base: EntityDef
    index: int
    entity_id: str


@dataclass
class MQTTContext:
    command_topics: List[str]
    command_handlers: Dict[str, Callable[[str], None]]


def _as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _entity_from_obj(obj: Any, defaults: Dict[str, Any]) -> EntityDef:
    if not isinstance(obj, dict):
        raise ValueError("entity must be an object")
    entity_id = str(obj.get("id"))
    if not entity_id:
        raise ValueError("entity missing id")
    kind = str(obj.get("kind", defaults.get("kind", "sensor")))
    name = str(obj.get("name", defaults.get("name", entity_id)))
    return EntityDef(
        id=entity_id,
        kind=kind,
        name=name,
        count=_as_int(obj.get("count", defaults.get("count", 1)), 1),
        device_class=obj.get("device_class", defaults.get("device_class")),
        unit=obj.get("unit", defaults.get("unit")),
        interval=_as_float(obj.get("interval", defaults.get("interval", 5.0)), 5.0),
        model=str(obj.get("model", defaults.get("model", "drift"))),
        min=obj.get("min", defaults.get("min")),
        max=obj.get("max", defaults.get("max")),
        precision=_as_int(obj.get("precision", defaults.get("precision", 2)), 2),
        state_payload=str(obj.get("payload", defaults.get("payload", "json"))),
        initial=obj.get("initial", defaults.get("initial")),
        commandable=bool(obj.get("commandable", defaults.get("commandable", False))),
    )


def parse_simulation_config(rest: Any, cli: argparse.Namespace) -> SimulationConfig:
    cfg = SimulationConfig()
    cfg.entities = []

    sim_obj: Dict[str, Any] = {}
    if isinstance(rest, dict):
        sim_obj = rest.get("simulation") or {}
        if not isinstance(sim_obj, dict):
            sim_obj = {}

    # YAML values
    cfg.devices = _as_int(sim_obj.get("devices", cfg.devices), cfg.devices)
    cfg.base_topic = str(sim_obj.get("base_topic", cfg.base_topic))
    cfg.discovery_prefix = str(sim_obj.get("discovery_prefix", cfg.discovery_prefix))
    cfg.publish_qos = _as_int(sim_obj.get("qos", cfg.publish_qos), cfg.publish_qos)
    cfg.retain_state = bool(sim_obj.get("retain", cfg.retain_state))
    cfg.connect_timeout = _as_float(sim_obj.get("connect_timeout", cfg.connect_timeout), cfg.connect_timeout)
    cfg.client_id_prefix = str(sim_obj.get("client_id_prefix", cfg.client_id_prefix))
    cfg.ha_discovery = bool(sim_obj.get("ha_discovery", cfg.ha_discovery))
    cfg.log_summary_interval = _as_float(sim_obj.get("log_summary_interval", cfg.log_summary_interval), cfg.log_summary_interval)
    cfg.jitter = _as_float(sim_obj.get("jitter", cfg.jitter), cfg.jitter)

    defaults = sim_obj.get("defaults") or {}
    if not isinstance(defaults, dict):
        defaults = {}

    device_obj = sim_obj.get("device") or {}
    if not isinstance(device_obj, dict):
        device_obj = {}

    # Device metadata for Home Assistant discovery. Values support {device_id}.
    # Defaults preserve the previous hard-coded payload.
    cfg.device = {
        "identifiers": device_obj.get("identifiers", ["sim_device_{device_id}"]),
        "name": device_obj.get("name", "Sim Device {device_id}"),
        "model": device_obj.get("model", "SmartHome Simulator"),
        "manufacturer": device_obj.get("manufacturer", "Eurun Lab"),
    }

    entities_obj = sim_obj.get("entities")
    if isinstance(entities_obj, list):
        cfg.entities = [_entity_from_obj(e, defaults) for e in entities_obj]

    # Provide a useful default set if none is specified.
    if not cfg.entities:
        cfg.entities = [
            EntityDef(id="temperature", kind="sensor", name="Temperature", count=1, device_class="temperature", unit="°C", interval=5.0, model="drift", min=20.0, max=30.0, precision=2, state_payload="json"),
            EntityDef(id="humidity", kind="sensor", name="Humidity", count=1, device_class="humidity", unit="%", interval=7.0, model="drift", min=35.0, max=65.0, precision=1, state_payload="json"),
            EntityDef(id="motion", kind="binary_sensor", name="Motion", count=1, device_class="motion", interval=1.0, model="motion"),
            EntityDef(id="heater", kind="switch", name="Heater", count=1, commandable=True, initial=False),
            EntityDef(id="rgb_light", kind="light", name="RGB Light", count=1, commandable=True, initial={"state": "OFF", "brightness": 255, "color": {"r": 255, "g": 255, "b": 255}}),
        ]

    automation_obj = sim_obj.get("automation") or {}
    if isinstance(automation_obj, dict) and automation_obj:
        cfg.automation = AutomationConfig(
            motion_entity=automation_obj.get("motion_entity"),
            light_entity=automation_obj.get("light_entity"),
            motion_hold_seconds=_as_float(automation_obj.get("motion_hold_seconds", 30.0), 30.0),
            switch_entity=automation_obj.get("switch_entity"),
            sensor_entity=automation_obj.get("sensor_entity"),
            delta_per_minute_on=_as_float(automation_obj.get("delta_per_minute_on", 1.0), 1.0),
            delta_per_minute_off=_as_float(automation_obj.get("delta_per_minute_off", -0.2), -0.2),
        )

    # CLI overrides (highest priority)
    if getattr(cli, "devices", None) is not None:
        cfg.devices = int(cli.devices)
    if getattr(cli, "base_topic", None):
        cfg.base_topic = str(cli.base_topic)
    if getattr(cli, "discovery_prefix", None):
        cfg.discovery_prefix = str(cli.discovery_prefix)
    if getattr(cli, "connect_timeout", None) is not None:
        cfg.connect_timeout = float(cli.connect_timeout)
    if getattr(cli, "qos", None) is not None:
        cfg.publish_qos = int(cli.qos)
    if getattr(cli, "retain", None):
        cfg.retain_state = True
    if getattr(cli, "no_ha_discovery", False):
        cfg.ha_discovery = False
    if getattr(cli, "ha_discovery", False):
        cfg.ha_discovery = True
    if getattr(cli, "client_id_prefix", None):
        cfg.client_id_prefix = str(cli.client_id_prefix)

    return cfg


def _render_name(template: str, device_id: int, index: int) -> str:
    if "{index}" not in template and index != 1:
        template = f"{template} #{index}"
    return template.format(device_id=device_id, index=index)


def _now_ts() -> int:
    return int(time.time())


class Simulator:
    def __init__(
        self,
        *,
        brokers: List[Broker],
        sim: SimulationConfig,
        dry_run: bool,
        once: bool,
        log_level: str,
    ) -> None:
        self.brokers = brokers
        self.sim = sim
        self.dry_run = dry_run
        self.once = once
        self.log_level = log_level

        self._broker_clients: List[Tuple[Optional[mqtt.Client], Broker]] = []
        self._stop = False

        # State storage: (device_id, entity_id) -> state
        self.state: Dict[Tuple[int, str], Any] = {}
        self._motion_until: Dict[int, float] = {}
        self._publish_count = 0
        self._last_summary = time.monotonic()

        self.command_handlers: Dict[str, Callable[[str], None]] = {}
        self.command_topics: List[str] = []

        self.entities: List[EntityInstance] = []
        for ent in (self.sim.entities or []):
            count = max(1, int(getattr(ent, "count", 1) or 1))
            for idx in range(1, count + 1):
                eid = ent.id if count == 1 else f"{ent.id}_{idx}"
                self.entities.append(EntityInstance(base=ent, index=idx, entity_id=eid))

    def _topic_state(self, device_id: int, entity_id: str) -> str:
        return f"{self.sim.base_topic}/device_{device_id}/{entity_id}/state"

    def _topic_set(self, device_id: int, entity_id: str) -> str:
        return f"{self.sim.base_topic}/device_{device_id}/{entity_id}/set"

    def _unique_id(self, device_id: int, entity_id: str) -> str:
        return f"sim_{device_id}_{entity_id}".lower()

    def _device_payload(self, device_id: int) -> Dict[str, Any]:
        device_cfg = self.sim.device or {}

        identifiers = device_cfg.get("identifiers", ["sim_device_{device_id}"])
        if isinstance(identifiers, str):
            identifiers_list = [identifiers]
        elif isinstance(identifiers, list):
            identifiers_list = identifiers
        else:
            identifiers_list = ["sim_device_{device_id}"]

        identifiers_list = [str(x).format(device_id=device_id) for x in identifiers_list]
        name = str(device_cfg.get("name", "Sim Device {device_id}")).format(device_id=device_id)
        model = str(device_cfg.get("model", "SmartHome Simulator")).format(device_id=device_id)
        manufacturer = str(device_cfg.get("manufacturer", "Eurun Lab")).format(device_id=device_id)

        return {
            "identifiers": identifiers_list,
            "name": name,
            "model": model,
            "manufacturer": manufacturer,
        }

    def _resolve_entity_id(self, entity_id: str) -> str:
        existing = {e.entity_id for e in self.entities}
        if entity_id in existing:
            return entity_id
        candidate = f"{entity_id}_1"
        if candidate in existing:
            return candidate
        return entity_id

    def _publish_all(self, topic: str, payload: str, *, qos: int, retain: bool) -> None:
        if self.dry_run:
            logging.debug(f"[DRY] publish {topic}: {payload[:120]}")
            return

        for client, broker in self._broker_clients:
            if client and client.is_connected():
                client.publish(topic, payload, qos=qos, retain=retain)
                self._publish_count += 1

    def _ensure_initial_state(self) -> None:
        for device_id in range(1, self.sim.devices + 1):
            for inst in self.entities:
                ent = inst.base
                key = (device_id, inst.entity_id)
                if key in self.state:
                    continue
                if ent.kind in {"switch"}:
                    self.state[key] = bool(ent.initial) if ent.initial is not None else False
                elif ent.kind in {"light"}:
                    if isinstance(ent.initial, dict):
                        self.state[key] = ent.initial
                    else:
                        self.state[key] = {"state": "OFF", "brightness": 255, "color": {"r": 255, "g": 255, "b": 255}}
                elif ent.kind == "binary_sensor":
                    self.state[key] = False
                else:
                    # Numeric sensors start in mid-range if defined
                    if ent.min is not None and ent.max is not None:
                        self.state[key] = float(ent.min + (ent.max - ent.min) / 2.0)
                    else:
                        self.state[key] = 0.0

    def _build_command_map(self) -> None:
        for device_id in range(1, self.sim.devices + 1):
            for inst in self.entities:
                ent = inst.base
                if not ent.commandable:
                    continue
                topic = self._topic_set(device_id, inst.entity_id)
                self.command_topics.append(topic)

                def make_handler(did: int, entity: EntityDef, entity_id: str) -> Callable[[str], None]:
                    def handler(payload_text: str) -> None:
                        self._handle_command(did, entity, entity_id, payload_text)
                    return handler

                self.command_handlers[topic] = make_handler(device_id, ent, inst.entity_id)

    def _handle_command(self, device_id: int, ent: EntityDef, entity_id: str, payload_text: str) -> None:
        key = (device_id, entity_id)
        if ent.kind == "switch":
            val = payload_text.strip().upper()
            new_state = val in {"ON", "1", "TRUE", "YES"}
            self.state[key] = new_state
            self._publish_state(device_id, ent, entity_id, index=1, force=True)
            logging.info(f"[CMD] device_{device_id} {entity_id}={new_state}")
            return

        if ent.kind == "light":
            # Accept HA-style JSON
            try:
                obj = json.loads(payload_text)
                if not isinstance(obj, dict):
                    raise ValueError("payload not object")
            except Exception:
                obj = {"state": payload_text.strip().upper()}

            cur = self.state.get(key)
            if not isinstance(cur, dict):
                cur = {"state": "OFF", "brightness": 255, "color": {"r": 255, "g": 255, "b": 255}}

            if "state" in obj:
                cur["state"] = str(obj.get("state", "OFF")).upper()
            if "brightness" in obj:
                try:
                    cur["brightness"] = int(obj.get("brightness"))
                except Exception:
                    pass
            if "color" in obj and isinstance(obj["color"], dict):
                color = obj["color"]
                cur["color"] = {
                    "r": int(color.get("r", cur.get("color", {}).get("r", 255))),
                    "g": int(color.get("g", cur.get("color", {}).get("g", 255))),
                    "b": int(color.get("b", cur.get("color", {}).get("b", 255))),
                }

            self.state[key] = cur
            self._publish_state(device_id, ent, entity_id, index=1, force=True)
            logging.info(f"[CMD] device_{device_id} {entity_id}={cur}")
            return

    def _publish_discovery(self) -> None:
        if not self.sim.ha_discovery:
            return

        for device_id in range(1, self.sim.devices + 1):
            for inst in self.entities:
                ent = inst.base
                uid = self._unique_id(device_id, inst.entity_id)
                state_topic = self._topic_state(device_id, inst.entity_id)
                device_payload = self._device_payload(device_id)

                kind = ent.kind
                disc_topic = f"{self.sim.discovery_prefix}/{kind}/{uid}/config"
                payload: Dict[str, Any] = {
                    "name": _render_name(ent.name, device_id, inst.index),
                    "unique_id": uid,
                    "state_topic": state_topic,
                    "device": device_payload,
                }
                if ent.device_class:
                    payload["device_class"] = ent.device_class
                if ent.unit and kind == "sensor":
                    payload["unit_of_measurement"] = ent.unit
                if kind == "sensor" and ent.state_payload == "json":
                    payload["value_template"] = "{{ value_json.value }}"

                if kind in {"switch", "light"}:
                    payload["command_topic"] = self._topic_set(device_id, inst.entity_id)

                self._publish_all(disc_topic, json.dumps(payload), qos=self.sim.publish_qos, retain=True)

    def _publish_state(self, device_id: int, ent: EntityDef, entity_id: str, *, index: int = 1, force: bool = False) -> None:
        key = (device_id, entity_id)
        value = self.state.get(key)
        topic = self._topic_state(device_id, entity_id)

        if ent.kind == "binary_sensor":
            payload = "ON" if bool(value) else "OFF"
            self._publish_all(topic, payload, qos=self.sim.publish_qos, retain=self.sim.retain_state)
            return

        if ent.kind == "switch":
            payload = "ON" if bool(value) else "OFF"
            self._publish_all(topic, payload, qos=self.sim.publish_qos, retain=self.sim.retain_state)
            return

        if ent.kind == "light":
            if not isinstance(value, dict):
                value = {"state": "OFF", "brightness": 255, "color": {"r": 255, "g": 255, "b": 255}}
            self._publish_all(topic, json.dumps(value), qos=self.sim.publish_qos, retain=self.sim.retain_state)
            return

        # Numeric sensor
        if ent.state_payload == "json":
            payload = json.dumps({"value": value, "ts": _now_ts(), "device_id": device_id, "entity": entity_id})
        else:
            payload = str(value)

        self._publish_all(topic, payload, qos=self.sim.publish_qos, retain=self.sim.retain_state)

    def _step_entity(self, device_id: int, ent: EntityDef, entity_id: str, dt: float) -> None:
        key = (device_id, entity_id)

        if ent.kind == "binary_sensor" and ent.model == "motion":
            # Simple motion bursts
            cur = bool(self.state.get(key, False))
            p = 0.02  # default event chance per tick
            if not cur and random.random() < p:
                self.state[key] = True
                self._motion_until[device_id] = time.monotonic() + 3.0
            elif cur and time.monotonic() >= self._motion_until.get(device_id, 0.0):
                self.state[key] = False
            return

        if ent.kind == "sensor":
            current = float(self.state.get(key, 0.0))

            # Clamp range
            min_v = ent.min if ent.min is not None else current - 1000.0
            max_v = ent.max if ent.max is not None else current + 1000.0

            # Base dynamics
            if ent.model == "uniform":
                nxt = random.uniform(min_v, max_v)
            elif ent.model == "sine":
                mid = min_v + (max_v - min_v) / 2.0
                amp = (max_v - min_v) / 2.0
                period = max(ent.interval * 20.0, 30.0)
                t = time.time()
                nxt = mid + amp * math.sin(2.0 * math.pi * t / period) + random.gauss(0.0, 0.05)
            else:
                # drift / random-walk
                nxt = current + random.gauss(0.0, 0.05)

            # Automation: switch affects a sensor (e.g., heater affects temperature)
            if self.sim.automation and self.sim.automation.switch_entity and self.sim.automation.sensor_entity:
                sensor_id = self._resolve_entity_id(self.sim.automation.sensor_entity)
                if entity_id == sensor_id:
                    sw_id = self._resolve_entity_id(self.sim.automation.switch_entity)
                    sw_key = (device_id, sw_id)
                    sw_on = bool(self.state.get(sw_key, False))
                    delta_per_min = self.sim.automation.delta_per_minute_on if sw_on else self.sim.automation.delta_per_minute_off
                    nxt += (delta_per_min * dt) / 60.0

            # Clamp and precision
            nxt = max(min_v, min(max_v, nxt))
            self.state[key] = round(nxt, ent.precision)
            return

    def _apply_automation_post_step(self) -> None:
        if not self.sim.automation:
            return
        if not (self.sim.automation.motion_entity and self.sim.automation.light_entity):
            return

        motion_id = self._resolve_entity_id(self.sim.automation.motion_entity)
        light_id = self._resolve_entity_id(self.sim.automation.light_entity)
        hold = float(self.sim.automation.motion_hold_seconds)

        for device_id in range(1, self.sim.devices + 1):
            motion_key = (device_id, motion_id)
            light_key = (device_id, light_id)
            motion_on = bool(self.state.get(motion_key, False))

            if motion_on:
                self._motion_until[device_id] = max(self._motion_until.get(device_id, 0.0), time.monotonic() + hold)
                # Turn on light if currently off
                cur = self.state.get(light_key)
                if isinstance(cur, dict) and str(cur.get("state", "OFF")).upper() == "OFF":
                    cur["state"] = "ON"
                    self.state[light_key] = cur

            # Turn off after hold
            if time.monotonic() >= self._motion_until.get(device_id, 0.0):
                cur = self.state.get(light_key)
                if isinstance(cur, dict) and str(cur.get("state", "OFF")).upper() == "ON":
                    cur["state"] = "OFF"
                    self.state[light_key] = cur

    def run(self) -> None:
        self._ensure_initial_state()
        self._build_command_map()
        ctx = MQTTContext(command_topics=self.command_topics, command_handlers=self.command_handlers)

        if not self.dry_run:
            for b in self.brokers:
                client = b.create_client(client_id_prefix=self.sim.client_id_prefix, mqtt_context=ctx)
                self._broker_clients.append((client, b))
        else:
            self._broker_clients = [(None, b) for b in self.brokers]

        if self.sim.ha_discovery and not self.dry_run:
            logging.info("Waiting for MQTT connections to send HA discovery...")
            deadline = time.time() + float(self.sim.connect_timeout)
            while time.time() < deadline:
                if any(c and c.is_connected() for c, _ in self._broker_clients):
                    break
                time.sleep(0.2)

        self._publish_discovery()

        # Publish initial actuator states
        for device_id in range(1, self.sim.devices + 1):
            for inst in self.entities:
                ent = inst.base
                if ent.kind in {"switch", "light"}:
                    self._publish_state(device_id, ent, inst.entity_id, index=inst.index, force=True)

        base_defs = len(self.sim.entities or [])
        expanded = len(self.entities)
        command_topics = len(self.command_topics)
        logging.info(
            "Started %s device(s), entities=%s defs -> %s instances, command_topics=%s, base_topic=%s",
            self.sim.devices,
            base_defs,
            expanded,
            command_topics,
            self.sim.base_topic,
        )

        # Scheduler heap: (next_time, device_id, entity_index)
        heap: List[Tuple[float, int, int]] = []
        start = time.monotonic()
        for device_id in range(1, self.sim.devices + 1):
            for idx, inst in enumerate(self.entities):
                ent = inst.base
                if ent.kind in {"switch", "light"}:
                    continue
                next_t = start + random.random() * min(ent.interval, 1.0)
                heapq.heappush(heap, (next_t, device_id, idx))

        last_time = time.monotonic()
        try:
            while True:
                if not heap:
                    time.sleep(0.2)
                    continue

                now = time.monotonic()
                next_t, device_id, idx = heap[0]
                sleep_for = next_t - now
                if sleep_for > 0:
                    time.sleep(min(sleep_for, 0.5))
                    continue

                heapq.heappop(heap)
                inst = self.entities[idx]
                ent = inst.base
                now2 = time.monotonic()
                dt = max(0.0, now2 - last_time)
                last_time = now2

                # Step entity + publish
                self._step_entity(device_id, ent, inst.entity_id, dt)
                self._apply_automation_post_step()
                self._publish_state(device_id, ent, inst.entity_id, index=inst.index)

                # Reschedule
                jitter = 1.0
                if self.sim.jitter and self.sim.jitter > 0:
                    jitter = 1.0 + random.uniform(-self.sim.jitter, self.sim.jitter)
                heapq.heappush(heap, (now2 + ent.interval * jitter, device_id, idx))

                # Summary
                if self.sim.log_summary_interval > 0 and (now2 - self._last_summary) >= self.sim.log_summary_interval:
                    connected = sum(1 for c, _ in self._broker_clients if c and c.is_connected())
                    logging.info(f"Publish count={self._publish_count}, connected_brokers={connected}/{len(self._broker_clients)}")
                    self._last_summary = now2

                if self.once and (now2 - start) > 1.0:
                    break

        except KeyboardInterrupt:
            logging.info("Stopping...")
        finally:
            for c, _ in self._broker_clients:
                if c:
                    try:
                        c.loop_stop()
                        c.disconnect()
                    except Exception:
                        pass


# ==========================
# Main Entry
# ==========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="sensors/brokers.yml", help="Config file path")
    parser.add_argument("--devices", type=int, default=None, help="Override simulation.devices")
    parser.add_argument("--base-topic", default=None, help="Override simulation.base_topic")
    parser.add_argument("--discovery-prefix", default=None, help="Override simulation.discovery_prefix")
    parser.add_argument("--qos", type=int, choices=[0, 1, 2], default=None, help="Override simulation.qos")
    parser.add_argument("--retain", action="store_true", help="Override simulation.retain=true")
    parser.add_argument("--connect-timeout", type=float, default=None, help="Override simulation.connect_timeout")
    parser.add_argument("--client-id-prefix", default=None, help="Override simulation.client_id_prefix")
    parser.add_argument("--ha-discovery", action="store_true", help="Override simulation.ha_discovery=true")
    parser.add_argument("--no-ha-discovery", action="store_true", help="Override simulation.ha_discovery=false")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()

    setup_logging(args.log_level)

    # Load Brokers
    try:
        brokers, rest, _path = load_brokers(args.config)
    except Exception as e:
        logging.error(f"Config Error: {e}")
        raise SystemExit(2)

    logging.info(f"Loaded {len(brokers)} broker(s) from {args.config}")

    sim = parse_simulation_config(rest, args)
    simulator = Simulator(
        brokers=brokers,
        sim=sim,
        dry_run=bool(args.dry_run),
        once=bool(args.once),
        log_level=str(args.log_level),
    )
    simulator.run()

if __name__ == "__main__":
    main()