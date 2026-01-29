"""Configuration loading and parsing for SmartHome Simulator."""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None

from .broker import Broker
from .entities import AutomationConfig, EntityDef, get_default_entities
from .utils import convert


@dataclass
class SimulationConfig:
    """Main simulation configuration."""
    
    devices: int = 10
    base_topic: str = "smarthome/sim"
    discovery_prefix: str = "homeassistant"
    publish_qos: int = 0
    retain_state: bool = False
    connect_timeout: float = 5.0
    client_id_prefix: str = "sim"
    ha_discovery: bool = False
    log_summary_interval: float = 30.0
    jitter: float = 0.0
    entities: List[EntityDef] = field(default_factory=list)
    automation: Optional[AutomationConfig] = None
    device: Dict[str, Any] = field(default_factory=dict)


def load_config(config_path: str) -> Tuple[Any, Path]:
    """Load configuration from YAML or JSON file."""
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
    """Load broker list and full config from file."""
    data, path = load_config(config_path)

    if isinstance(data, list):
        brokers_obj = data
        rest = None
    elif isinstance(data, dict):
        brokers_obj = data.get("brokers")
        rest = data
    else:
        raise ValueError("Config must be a list of brokers or an object with 'brokers'")

    if not isinstance(brokers_obj, list):
        raise ValueError("'brokers' must be a list")

    brokers = [Broker.from_dict(item, path) for item in brokers_obj]
    return brokers, rest, path


def _entity_from_dict(obj: Dict[str, Any], defaults: Dict[str, Any]) -> EntityDef:
    """Parse entity definition from config dict."""
    entity_id = str(obj.get("id", ""))
    if not entity_id:
        raise ValueError("entity missing id")
    
    return EntityDef(
        id=entity_id,
        kind=str(obj.get("kind", defaults.get("kind", "sensor"))),
        name=str(obj.get("name", defaults.get("name", entity_id))),
        count=convert(obj.get("count", defaults.get("count", 1)), int, 1),
        device_class=obj.get("device_class", defaults.get("device_class")),
        unit=obj.get("unit", defaults.get("unit")),
        interval=convert(obj.get("interval", defaults.get("interval", 5.0)), float, 5.0),
        model=str(obj.get("model", defaults.get("model", "drift"))),
        min=obj.get("min", defaults.get("min")),
        max=obj.get("max", defaults.get("max")),
        precision=convert(obj.get("precision", defaults.get("precision", 2)), int, 2),
        state_payload=str(obj.get("payload", defaults.get("payload", "json"))),
        initial=obj.get("initial", defaults.get("initial")),
        commandable=bool(obj.get("commandable", defaults.get("commandable", False))),
    )


def parse_simulation_config(rest: Any, cli: argparse.Namespace) -> SimulationConfig:
    """Parse simulation config from YAML data + CLI overrides."""
    cfg = SimulationConfig()

    sim_obj: Dict[str, Any] = {}
    if isinstance(rest, dict):
        sim_obj = rest.get("simulation") or {}
        if not isinstance(sim_obj, dict):
            sim_obj = {}

    # Load from YAML
    cfg.devices = convert(sim_obj.get("devices", cfg.devices), int, cfg.devices)
    cfg.base_topic = str(sim_obj.get("base_topic", cfg.base_topic))
    cfg.discovery_prefix = str(sim_obj.get("discovery_prefix", cfg.discovery_prefix))
    cfg.publish_qos = convert(sim_obj.get("qos", cfg.publish_qos), int, cfg.publish_qos)
    cfg.retain_state = bool(sim_obj.get("retain", cfg.retain_state))
    cfg.connect_timeout = convert(sim_obj.get("connect_timeout", cfg.connect_timeout), float, cfg.connect_timeout)
    cfg.client_id_prefix = str(sim_obj.get("client_id_prefix", cfg.client_id_prefix))
    cfg.ha_discovery = bool(sim_obj.get("ha_discovery", cfg.ha_discovery))
    cfg.log_summary_interval = convert(sim_obj.get("log_summary_interval", cfg.log_summary_interval), float, cfg.log_summary_interval)
    cfg.jitter = convert(sim_obj.get("jitter", cfg.jitter), float, cfg.jitter)

    # Device metadata
    device_obj = sim_obj.get("device") or {}
    cfg.device = {
        "identifiers": device_obj.get("identifiers", ["sim_device_{device_id}"]),
        "name": device_obj.get("name", "Sim Device {device_id}"),
        "model": device_obj.get("model", "SmartHome Simulator"),
        "manufacturer": device_obj.get("manufacturer", "Eurun Lab"),
    }

    # Parse entities
    defaults = sim_obj.get("defaults") or {}
    entities_obj = sim_obj.get("entities")
    if isinstance(entities_obj, list):
        cfg.entities = [_entity_from_dict(e, defaults) for e in entities_obj]
    
    if not cfg.entities:
        cfg.entities = get_default_entities()

    # Parse automation
    automation_obj = sim_obj.get("automation") or {}
    if automation_obj:
        cfg.automation = AutomationConfig(
            motion_entity=automation_obj.get("motion_entity"),
            light_entity=automation_obj.get("light_entity"),
            motion_hold_seconds=convert(automation_obj.get("motion_hold_seconds", 30.0), float, 30.0),
            switch_entity=automation_obj.get("switch_entity"),
            sensor_entity=automation_obj.get("sensor_entity"),
            delta_per_minute_on=convert(automation_obj.get("delta_per_minute_on", 1.0), float, 1.0),
            delta_per_minute_off=convert(automation_obj.get("delta_per_minute_off", -0.2), float, -0.2),
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
    if getattr(cli, "ha_discovery", False):
        cfg.ha_discovery = True
    if getattr(cli, "client_id_prefix", None):
        cfg.client_id_prefix = str(cli.client_id_prefix)

    return cfg


def setup_logging(level: str) -> None:
    """Configure logging with timestamp format."""
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

# [CodeRabbit Audit Trigger 1769364389]
