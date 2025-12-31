"""Core Simulator class for SmartHome Simulator."""

from __future__ import annotations

import heapq
import json
import logging
import math
import random
import signal
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import paho.mqtt.client as mqtt

from .broker import Broker
from .config import SimulationConfig
from .entities import DEFAULT_LIGHT_STATE, EntityDef, EntityInstance, MQTTContext
from .utils import convert, iso_utc, now_ts


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    """Handle MQTT connection events."""
    host = userdata.get("broker_host", "?")
    userdata["last_rc"] = rc

    # Record handshake latency
    started = userdata.get("connect_started_at")
    if started is not None:
        userdata["connect_latency_ms"] = (time.perf_counter() - float(started)) * 1000.0

    # Wake up benchmark waiters
    ev = userdata.get("connect_event")
    if ev:
        ev.set()

    # Record for benchmark export
    recorder = userdata.get("handshake_recorder")
    if recorder:
        try:
            recorder.write({
                "schema": "smarthome.handshake.record.v1",
                "ts_unix": time.time(),
                "ts_iso": iso_utc(),
                "worker_id": userdata.get("worker_id"),
                "sample": userdata.get("sample_index"),
                "broker": {"host": host, "port": userdata.get("broker_port"), "tls": userdata.get("broker_tls")},
                "client_id": getattr(client, "_client_id", b"").decode("utf-8", errors="replace") if getattr(client, "_client_id", None) else None,
                "rc": rc,
                "connect_latency_ms": userdata.get("connect_latency_ms"),
            })
        except Exception:
            pass

    if rc == 0:
        transport = "TLS" if getattr(client, "_ssl", None) else "TCP"
        logging.info(f"[{host}] Connected via {transport}")
        ctx: MQTTContext = userdata.get("ctx")
        if ctx:
            for topic in ctx.command_topics:
                try:
                    client.subscribe(topic)
                except Exception as e:
                    logging.warning(f"[{host}] Subscribe failed {topic}: {e}")
    else:
        rc_map = {1: "Protocol mismatch", 2: "Invalid ID", 3: "Server unavailable", 4: "Bad auth", 5: "Not authorized"}
        logging.warning(f"[{host}] Connection failed: {rc_map.get(rc, rc)}")


def on_disconnect(client, userdata, rc):
    """Handle MQTT disconnection events."""
    host = userdata.get("broker_host", "?")
    ev = userdata.get("disconnect_event")
    if ev:
        ev.set()
    if rc != 0:
        logging.warning(f"[{host}] Unexpected disconnect (rc={rc}), auto-reconnecting...")
    else:
        logging.info(f"[{host}] Disconnected")


def on_message(client, userdata, msg):
    """Handle incoming MQTT messages (commands)."""
    ctx: MQTTContext = userdata.get("ctx")
    if not ctx:
        return
    try:
        payload = msg.payload.decode("utf-8", errors="replace")
    except Exception:
        payload = ""
    handler = ctx.command_handlers.get(msg.topic)
    if handler:
        try:
            handler(payload)
        except Exception as e:
            logging.warning(f"[{userdata.get('broker_host', '?')}] Handler failed {msg.topic}: {e}")


class Simulator:
    """Main simulator orchestrating device simulation and MQTT publishing."""

    def __init__(
        self,
        *,
        brokers: List[Broker],
        sim: SimulationConfig,
        dry_run: bool = False,
        once: bool = False,
        device_id_start: int = 1,
        device_id_end: Optional[int] = None,
        worker_id: Optional[int] = None,
    ) -> None:
        self.brokers = brokers
        self.sim = sim
        self.dry_run = dry_run
        self.once = once

        self.device_id_start = max(1, device_id_start)
        self.device_id_end = device_id_end if device_id_end else sim.devices
        self.worker_id = worker_id

        self._broker_clients: List[Tuple[Optional[mqtt.Client], Broker]] = []
        self._stop = False

        # State storage: (device_id, entity_id) -> state
        self.state: Dict[Tuple[int, str], Any] = {}
        self._motion_until: Dict[int, float] = {}
        self._publish_count = 0
        self._last_summary = time.monotonic()

        self.command_handlers: Dict[str, Callable[[str], None]] = {}
        self.command_topics: List[str] = []

        # Expand entity definitions
        self.entities: List[EntityInstance] = []
        for ent in (self.sim.entities or []):
            count = max(1, ent.count or 1)
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
        cfg = self.sim.device or {}
        identifiers = cfg.get("identifiers", ["sim_device_{device_id}"])
        if isinstance(identifiers, str):
            identifiers = [identifiers]
        return {
            "identifiers": [str(x).format(device_id=device_id) for x in identifiers],
            "name": str(cfg.get("name", "Sim Device {device_id}")).format(device_id=device_id),
            "model": str(cfg.get("model", "SmartHome Simulator")).format(device_id=device_id),
            "manufacturer": str(cfg.get("manufacturer", "Eurun Lab")).format(device_id=device_id),
        }

    def _resolve_entity_id(self, entity_id: str) -> str:
        existing = {e.entity_id for e in self.entities}
        if entity_id in existing:
            return entity_id
        candidate = f"{entity_id}_1"
        return candidate if candidate in existing else entity_id

    def _publish_all(self, topic: str, payload: str, *, qos: int, retain: bool) -> None:
        if self.dry_run:
            logging.debug(f"[DRY] {topic}: {payload[:120]}")
            return
        for client, _ in self._broker_clients:
            if client and client.is_connected():
                client.publish(topic, payload, qos=qos, retain=retain)
                self._publish_count += 1

    def _ensure_initial_state(self) -> None:
        for device_id in range(self.device_id_start, self.device_id_end + 1):
            for inst in self.entities:
                ent = inst.base
                key = (device_id, inst.entity_id)
                if key in self.state:
                    continue
                if ent.kind == "switch":
                    self.state[key] = bool(ent.initial) if ent.initial is not None else False
                elif ent.kind == "light":
                    if isinstance(ent.initial, dict):
                        initial = dict(ent.initial)
                        if isinstance(initial.get("state"), bool):
                            initial["state"] = "ON" if initial["state"] else "OFF"
                        self.state[key] = initial
                    else:
                        self.state[key] = dict(DEFAULT_LIGHT_STATE)
                elif ent.kind == "binary_sensor":
                    self.state[key] = False
                else:
                    self.state[key] = (ent.min + ent.max) / 2.0 if ent.min is not None and ent.max is not None else 0.0

    def _build_command_map(self) -> None:
        for device_id in range(self.device_id_start, self.device_id_end + 1):
            for inst in self.entities:
                if not inst.base.commandable:
                    continue
                topic = self._topic_set(device_id, inst.entity_id)
                self.command_topics.append(topic)

                def make_handler(did: int, ent: EntityDef, eid: str) -> Callable[[str], None]:
                    return lambda p: self._handle_command(did, ent, eid, p)

                self.command_handlers[topic] = make_handler(device_id, inst.base, inst.entity_id)

    def _handle_command(self, device_id: int, ent: EntityDef, entity_id: str, payload: str) -> None:
        key = (device_id, entity_id)
        
        if ent.kind == "switch":
            new_state = payload.strip().upper() in ("ON", "1", "TRUE", "YES")
            self.state[key] = new_state
            self._publish_state(device_id, ent, entity_id)
            logging.info(f"[CMD] device_{device_id} {entity_id}={new_state}")
            return

        if ent.kind == "light":
            try:
                obj = json.loads(payload)
                if not isinstance(obj, dict):
                    obj = {"state": payload.strip().upper()}
            except Exception:
                obj = {"state": payload.strip().upper()}

            cur = self.state.get(key)
            if not isinstance(cur, dict):
                cur = dict(DEFAULT_LIGHT_STATE)

            if "state" in obj:
                s = obj["state"]
                cur["state"] = "ON" if s is True else ("OFF" if s is False else str(s).upper())
            if "brightness" in obj:
                cur["brightness"] = convert(obj["brightness"], int, cur["brightness"])
            if "color" in obj and isinstance(obj["color"], dict):
                c = obj["color"]
                cur_c = cur.get("color", {})
                cur["color"] = {
                    "r": convert(c.get("r"), int, cur_c.get("r", 255)),
                    "g": convert(c.get("g"), int, cur_c.get("g", 255)),
                    "b": convert(c.get("b"), int, cur_c.get("b", 255)),
                }

            self.state[key] = cur
            self._publish_state(device_id, ent, entity_id)
            logging.info(f"[CMD] device_{device_id} {entity_id}={cur}")

    def _publish_discovery(self) -> None:
        if not self.sim.ha_discovery:
            return

        for device_id in range(self.device_id_start, self.device_id_end + 1):
            for inst in self.entities:
                ent = inst.base
                uid = self._unique_id(device_id, inst.entity_id)
                state_topic = self._topic_state(device_id, inst.entity_id)

                name = ent.name
                if "{index}" not in name and inst.index != 1:
                    name = f"{name} #{inst.index}"
                name = name.format(device_id=device_id, index=inst.index)

                payload: Dict[str, Any] = {
                    "name": name,
                    "unique_id": uid,
                    "state_topic": state_topic,
                    "device": self._device_payload(device_id),
                }
                if ent.device_class:
                    payload["device_class"] = ent.device_class
                if ent.unit and ent.kind == "sensor":
                    payload["unit_of_measurement"] = ent.unit
                if ent.kind == "sensor" and ent.state_payload == "json":
                    payload["value_template"] = "{{ value_json.value }}"
                if ent.kind in ("switch", "light"):
                    payload["command_topic"] = self._topic_set(device_id, inst.entity_id)

                disc_topic = f"{self.sim.discovery_prefix}/{ent.kind}/{uid}/config"
                self._publish_all(disc_topic, json.dumps(payload), qos=self.sim.publish_qos, retain=True)

    def _publish_state(self, device_id: int, ent: EntityDef, entity_id: str) -> None:
        key = (device_id, entity_id)
        value = self.state.get(key)
        topic = self._topic_state(device_id, entity_id)
        qos, retain = self.sim.publish_qos, self.sim.retain_state

        if ent.kind in ("binary_sensor", "switch"):
            self._publish_all(topic, "ON" if value else "OFF", qos=qos, retain=retain)
        elif ent.kind == "light":
            self._publish_all(topic, json.dumps(value or DEFAULT_LIGHT_STATE), qos=qos, retain=retain)
        elif ent.state_payload == "json":
            self._publish_all(topic, json.dumps({"value": value, "ts": now_ts(), "device_id": device_id, "entity": entity_id}), qos=qos, retain=retain)
        else:
            self._publish_all(topic, str(value), qos=qos, retain=retain)

    def _step_entity(self, device_id: int, ent: EntityDef, entity_id: str, dt: float) -> None:
        key = (device_id, entity_id)

        if ent.kind == "binary_sensor" and ent.model == "motion":
            cur = bool(self.state.get(key, False))
            if not cur and random.random() < 0.02:
                self.state[key] = True
                self._motion_until[device_id] = time.monotonic() + 3.0
            elif cur and time.monotonic() >= self._motion_until.get(device_id, 0.0):
                self.state[key] = False
            return

        if ent.kind == "sensor":
            current = float(self.state.get(key, 0.0))
            min_v = ent.min if ent.min is not None else current - 1000.0
            max_v = ent.max if ent.max is not None else current + 1000.0

            if ent.model == "uniform":
                nxt = random.uniform(min_v, max_v)
            elif ent.model == "sine":
                mid = (min_v + max_v) / 2.0
                amp = (max_v - min_v) / 2.0
                period = max(ent.interval * 20.0, 30.0)
                nxt = mid + amp * math.sin(2.0 * math.pi * time.time() / period) + random.gauss(0, 0.05)
            else:  # drift
                nxt = current + random.gauss(0, 0.05)

            # Switch affects sensor (e.g., heater → temperature)
            if self.sim.automation and self.sim.automation.switch_entity and self.sim.automation.sensor_entity:
                sensor_id = self._resolve_entity_id(self.sim.automation.sensor_entity)
                if entity_id == sensor_id:
                    sw_id = self._resolve_entity_id(self.sim.automation.switch_entity)
                    sw_on = bool(self.state.get((device_id, sw_id), False))
                    delta = self.sim.automation.delta_per_minute_on if sw_on else self.sim.automation.delta_per_minute_off
                    nxt += (delta * dt) / 60.0

            self.state[key] = round(max(min_v, min(max_v, nxt)), ent.precision)

    def _apply_automation(self) -> None:
        if not self.sim.automation or not self.sim.automation.motion_entity or not self.sim.automation.light_entity:
            return

        motion_id = self._resolve_entity_id(self.sim.automation.motion_entity)
        light_id = self._resolve_entity_id(self.sim.automation.light_entity)
        hold = self.sim.automation.motion_hold_seconds

        for device_id in range(self.device_id_start, self.device_id_end + 1):
            motion_key = (device_id, motion_id)
            light_key = (device_id, light_id)
            motion_on = bool(self.state.get(motion_key, False))

            if motion_on:
                self._motion_until[device_id] = max(self._motion_until.get(device_id, 0.0), time.monotonic() + hold)
                cur = self.state.get(light_key)
                if isinstance(cur, dict) and str(cur.get("state", "OFF")).upper() == "OFF":
                    cur["state"] = "ON"

            if time.monotonic() >= self._motion_until.get(device_id, 0.0):
                cur = self.state.get(light_key)
                if isinstance(cur, dict) and str(cur.get("state", "OFF")).upper() == "ON":
                    cur["state"] = "OFF"

    def run(self) -> None:
        """Run the simulation loop."""
        prev_sigint = signal.getsignal(signal.SIGINT)

        def handle_sigint(*_):
            self._stop = True

        try:
            signal.signal(signal.SIGINT, handle_sigint)
        except Exception:
            prev_sigint = None

        self._ensure_initial_state()
        self._build_command_map()
        ctx = MQTTContext(command_topics=self.command_topics, command_handlers=self.command_handlers)

        # Connect to brokers
        if not self.dry_run:
            for b in self.brokers:
                client = b.create_client(
                    client_id_prefix=self.sim.client_id_prefix,
                    mqtt_context=ctx,
                    on_connect=on_connect,
                    on_disconnect=on_disconnect,
                    on_message=on_message,
                )
                self._broker_clients.append((client, b))
        else:
            self._broker_clients = [(None, b) for b in self.brokers]

        # Wait for connection before sending discovery
        if self.sim.ha_discovery and not self.dry_run:
            logging.info("Waiting for MQTT connections...")
            deadline = time.time() + self.sim.connect_timeout
            while time.time() < deadline:
                if any(c and c.is_connected() for c, _ in self._broker_clients):
                    break
                time.sleep(0.2)

        self._publish_discovery()

        # Publish initial actuator states
        for device_id in range(self.device_id_start, self.device_id_end + 1):
            for inst in self.entities:
                if inst.base.kind in ("switch", "light"):
                    self._publish_state(device_id, inst.base, inst.entity_id)

        device_count = self.device_id_end - self.device_id_start + 1
        worker_tag = f" worker={self.worker_id}" if self.worker_id is not None else ""
        logging.info(f"Started {device_count} device(s){worker_tag}, entities={len(self.entities)}, topic={self.sim.base_topic}")

        # Build scheduler heap
        heap: List[Tuple[float, int, int]] = []
        start = time.monotonic()
        for device_id in range(self.device_id_start, self.device_id_end + 1):
            for idx, inst in enumerate(self.entities):
                if inst.base.kind in ("switch", "light"):
                    continue
                next_t = start + random.random() * min(inst.base.interval, 1.0)
                heapq.heappush(heap, (next_t, device_id, idx))

        last_time = time.monotonic()
        try:
            while not self._stop:
                if not heap:
                    time.sleep(0.2)
                    continue

                now = time.monotonic()
                next_t, device_id, idx = heap[0]
                if next_t - now > 0:
                    time.sleep(min(next_t - now, 0.5))
                    continue

                heapq.heappop(heap)
                inst = self.entities[idx]
                now2 = time.monotonic()
                dt = max(0.0, now2 - last_time)
                last_time = now2

                self._step_entity(device_id, inst.base, inst.entity_id, dt)
                self._apply_automation()
                self._publish_state(device_id, inst.base, inst.entity_id)

                # Reschedule
                interval = inst.base.interval
                if self.sim.jitter > 0:
                    interval *= 1.0 + random.uniform(-self.sim.jitter, self.sim.jitter)
                heapq.heappush(heap, (now2 + interval, device_id, idx))

                # Summary log
                if self.sim.log_summary_interval > 0 and (now2 - self._last_summary) >= self.sim.log_summary_interval:
                    connected = sum(1 for c, _ in self._broker_clients if c and c.is_connected())
                    logging.info(f"Publishes={self._publish_count}, connected={connected}/{len(self._broker_clients)}")
                    self._last_summary = now2

                if self.once and (now2 - start) > 1.0:
                    break

        except KeyboardInterrupt:
            logging.info("Stopping...")
        finally:
            if prev_sigint:
                try:
                    signal.signal(signal.SIGINT, prev_sigint)
                except Exception:
                    pass

            for c, _ in self._broker_clients:
                if c:
                    try:
                        c.disconnect()
                    except Exception:
                        pass
                    try:
                        c.loop_stop(force=True)
                    except (TypeError, Exception):
                        try:
                            c.loop_stop()
                        except Exception:
                            pass
