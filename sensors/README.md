# Sensor Simulator

Language: **English** | [简体中文](README.zh-CN.md)

A multi-broker MQTT smart-home simulator for Home Assistant.

This module is designed for a thesis/demo environment: it generates realistic sensor streams AND controllable actuator entities, so you can build meaningful HA automations even when hardware devices are limited.

## Contents

- [What it is](#what-it-is)
- [Repo files](#repo-files)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Quick start](#quick-start)
- [TLS / mTLS certificates](#tls--mtls-certificates)
- [Entities \& automations](#entities--automations)
- [CLI overrides](#cli-overrides)
- [Home Assistant device metadata](#home-assistant-device-metadata)
- [Handshake benchmark (real data export)](#handshake-benchmark-real-data-export)
- [Troubleshooting](#troubleshooting)

## What it is

- Publishes simulated sensor data to MQTT (supports multiple brokers).
- Optionally advertises entities via Home Assistant MQTT Discovery.
- Supports controllable entities (switch/light) via MQTT command topics.
- Supports TLS/mTLS via file paths or inline PEM.

## Repo files

- `sensors/sensor_simulator.py` — main simulator script
- `sensors/brokers.example.yml` — example configuration (copy to `sensors/brokers.yml` and edit)
- `sensors/docker-compose.yml` — Docker entry (mounts config/certs)
- `sensors/Dockerfile` — container image for server-side runs
- `certs/README` — certificate layout notes

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

Multi-core stress test (Linux server recommended):

```bash
. .venv/bin/activate
# Use multiple processes to utilize multi-core CPUs.
# Each worker handles a slice of device_id ranges.
python sensors/sensor_simulator.py --config sensors/brokers.yml --workers 6 --log-level INFO
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
- `--workers N` (use >1 to utilize multi-core)
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

## Handshake benchmark (real data export)

For thesis-grade measurements, the simulator can run a **real** connect/disconnect loop and record end-to-end MQTT connect latency (including TCP + TLS handshake + MQTT CONNACK time).

Single process:

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --handshake-samples 200 \
  --handshake-interval 0.2 \
  --handshake-timeout 10 \
  --handshake-out sensors/handshake_metrics \
  --handshake-only
```

Outputs (local files):
- `sensors/handshake_metrics/handshake.w0.jsonl`: one JSON record per real connection attempt
- `sensors/handshake_metrics/handshake.w0.summary.json`: computed statistics derived from JSONL (p50/p90/p95/p99, mean/stdev, etc.)

Data correctness notes:
- JSONL records are written from actual connection outcomes (including failures).
- Summary metrics are computed only from successful records (`rc == 0` and `connect_latency_ms` present).
- Percentiles use linear interpolation between closest ranks (documented in the summary).

Optional plots (requires matplotlib):

```bash
pip install matplotlib
python sensors/sensor_simulator.py --config sensors/brokers.yml --handshake-samples 200 --handshake-plot --handshake-only
```

Multi-process (runs samples **per worker**):

```bash
python sensors/sensor_simulator.py --config sensors/brokers.yml --workers 4 --handshake-samples 200 --handshake-only
```

## Troubleshooting

- If imports fail, ensure the virtual environment is active and dependencies are installed.
- For EMQX authentication errors, double-check `username`/`password` in `brokers.yml`.
- If you enable TLS on your brokers, set `tls: true` in the corresponding entry. By default, system CA certs are used.
- Use `--log-level DEBUG` to see connection and publish details.

\---

Contributions and experiment reports are welcome. If you publish results, include:
- config used (`sensors/brokers.yml` redacted)
- command line
- raw JSONL + summary JSON
