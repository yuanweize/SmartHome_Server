"""Entity models and data classes for SmartHome Simulator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# Default light state template
DEFAULT_LIGHT_STATE = {
    "state": "OFF",
    "brightness": 255,
    "color": {"r": 255, "g": 255, "b": 255},
}


@dataclass
class EntityDef:
    """Entity definition from configuration."""
    
    id: str
    kind: str  # sensor | binary_sensor | switch | light
    name: str
    count: int = 1
    device_class: Optional[str] = None
    unit: Optional[str] = None
    interval: float = 5.0
    model: str = "drift"  # drift | uniform | sine | motion
    min: Optional[float] = None
    max: Optional[float] = None
    precision: int = 2
    state_payload: str = "json"  # json | plain
    initial: Any = None
    commandable: bool = False


@dataclass(frozen=True)
class EntityInstance:
    """A specific instance of an entity for a device."""
    
    base: EntityDef
    index: int
    entity_id: str


@dataclass
class MQTTContext:
    """Context passed to MQTT callbacks."""
    
    command_topics: List[str] = field(default_factory=list)
    command_handlers: Dict[str, Callable[[str], None]] = field(default_factory=dict)


@dataclass
class AutomationConfig:
    """Configuration for entity coupling automations."""
    
    # Motion → Light coupling
    motion_entity: Optional[str] = None
    light_entity: Optional[str] = None
    motion_hold_seconds: float = 30.0
    
    # Switch → Sensor coupling (e.g., heater affects temperature)
    switch_entity: Optional[str] = None
    sensor_entity: Optional[str] = None
    delta_per_minute_on: float = 1.0
    delta_per_minute_off: float = -0.2


def get_default_entities() -> List[EntityDef]:
    """Return default entity definitions when none are configured."""
    return [
        EntityDef(
            id="temperature", kind="sensor", name="Temperature",
            device_class="temperature", unit="°C", interval=5.0,
            model="drift", min=20.0, max=30.0, precision=2, state_payload="json"
        ),
        EntityDef(
            id="humidity", kind="sensor", name="Humidity",
            device_class="humidity", unit="%", interval=7.0,
            model="drift", min=35.0, max=65.0, precision=1, state_payload="json"
        ),
        EntityDef(
            id="motion", kind="binary_sensor", name="Motion",
            device_class="motion", interval=1.0, model="motion"
        ),
        EntityDef(
            id="heater", kind="switch", name="Heater",
            commandable=True, initial=False
        ),
        EntityDef(
            id="rgb_light", kind="light", name="RGB Light",
            commandable=True, initial=dict(DEFAULT_LIGHT_STATE)
        ),
    ]

