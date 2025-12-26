# Sensor Simulator

A multi-broker MQTT smart-home simulator for Home Assistant.

This module is designed for a thesis/demo environment: it generates realistic sensor streams AND controllable actuator entities, so you can build meaningful HA automations even when hardware devices are limited.

Files:
- `sensor_simulator.py` — main simulator script
- `brokers.example.yml` — example broker configuration; copy to `brokers.yml` and edit

## Prerequisites

- macOS or Linux with Python 3.8+
- Recommended: virtual environment (venv, uv)

Install dependencies in a local venv (zsh):

```bash
cd SmartHome_Server
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy `sensors/brokers.example.yml` to `sensors/brokers.yml` and edit it.

The config file contains BOTH:
- `brokers`: MQTT broker list (TLS/mTLS supported)
- `simulation`: devices/entities/automations shown in Home Assistant

Notes:
- YAML and JSON are both supported. Use `--config` to specify a custom path.
- Credentials should not be committed. `sensors/brokers.yml` is git-ignored.

## Quick start

Dry-run (no network publishes, logs only):

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml --dry-run --log-level DEBUG
```

Publish using `sensors/brokers.yml`:

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml
```

Override some settings from CLI (CLI > brokers.yml > defaults):

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml --devices 200 --qos 1 --log-level INFO
```

Home Assistant MQTT Discovery:

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml
```

## TLS / mTLS certificates

The simulator supports two ways to provide TLS materials:

1) **File paths** in `sensors/brokers.yml` (`ca_file`, `cert_file`, `key_file`).
  - Paths are resolved **relative to the brokers config file**.
  - With Docker, this matches `sensors/docker-compose.yml` mounting `./certs` into the container.
  - Common pitfall: if your certs are stored at repo root `certs/`, then a path like `./certs/...` inside `sensors/brokers.yml` refers to `sensors/certs/...`.
    Use `../certs/...` or copy certs under `sensors/certs/...`.

2) **Inline PEM text** in `sensors/brokers.yml` (`ca_pem`, `cert_pem`, `key_pem`).
  - Inline PEM takes priority over file paths.
  - If inline TLS setup fails, it will fall back to file paths (if present).

## Entities & automations

All entities are defined in `simulation.entities`.

Entity fields:
- `id`: base id (required). If `count > 1`, instances become `id_1`, `id_2`, ...
- `count`: optional, default `1` (per-device instance count)
- `name`: supports `{device_id}` and `{index}` (instance index)

Supported kinds:
- `sensor`: publishes numeric values
- `binary_sensor`: publishes `ON`/`OFF`
- `switch`: controllable from HA via MQTT command topic
- `light`: controllable from HA via MQTT command topic (JSON state)

Meaningful couplings can be configured via `simulation.automation`:
- `motion_entity` + `light_entity`: motion turns on light for `motion_hold_seconds`
- `switch_entity` + `sensor_entity`: switch affects sensor trend (e.g., heater affects temperature)

## CLI overrides

The design goal is to keep Docker usage simple: `--config` is enough.

If you do use CLI flags, the precedence is:
1) CLI flags
2) `sensors/brokers.yml`
3) built-in defaults

Common flags:
- `--config PATH`
- `--devices N`
- `--qos 0|1|2`
- `--retain`
- `--log-level DEBUG|INFO|WARNING|ERROR`

## Home Assistant device metadata

The MQTT Discovery payload includes a Home Assistant `device` object, configured in `simulation.device`:
- `identifiers` (string list)
- `name`
- `model`
- `manufacturer`

These fields support `{device_id}`.

## Troubleshooting

- If imports fail, ensure the virtual environment is active and dependencies are installed.
- For EMQX authentication errors, double-check `username`/`password` in `brokers.yml`.
- If you enable TLS on your brokers, set `tls: true` in the corresponding entry. By default, system CA certs are used.
- Use `--log-level DEBUG` to see connection and publish details.
