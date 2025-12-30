# SmartHome Simulator

Language: **English** | [简体中文](README.zh-CN.md)

A thesis-grade multi-broker MQTT smart-home simulator with mTLS support, designed for Home Assistant integration and stress testing.

## Features

- 🔌 **Multi-broker support** - Publish to multiple MQTT brokers simultaneously
- 🏠 **Home Assistant Discovery** - Auto-register entities in HA
- 🎮 **Controllable actuators** - Switch/light control via MQTT commands
- 🔐 **TLS/mTLS** - File paths or inline PEM certificates
- ⚡ **Multi-process scaling** - `--workers` for multi-core CPU utilization
- 📊 **Handshake benchmark** - Thesis-grade latency measurements with statistics

## Quick Start

```bash
# Install dependencies
cd SmartHome_Server
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# Copy and edit configuration
cp sensors/brokers.example.yml sensors/brokers.yml

# Dry-run test (no broker required)
python sensors/sensor_simulator.py --dry-run

# Connect to broker with Home Assistant discovery
python sensors/sensor_simulator.py --config sensors/brokers.yml --ha-discovery

# Stress test with 1000 devices across 4 workers
python sensors/sensor_simulator.py --config sensors/brokers.yml --devices 1000 --workers 4
```

## Package Structure

```
sensors/
├── sensor_simulator.py         # Entry point (with version check & error handling)
├── smarthome_sim/              # Python package
│   ├── __init__.py             # Version: 1.0.0, public API exports
│   ├── __main__.py             # `python -m smarthome_sim` entry
│   ├── cli.py                  # CLI argument parsing
│   ├── config.py               # Configuration loading (YAML/JSON)
│   ├── broker.py               # Broker class + TLS/mTLS handling
│   ├── simulator.py            # Core simulation logic
│   ├── entities.py             # Entity models (EntityDef, EntityInstance)
│   ├── benchmark.py            # TLS handshake benchmark
│   └── utils.py                # Utility functions
├── brokers.example.yml         # Example configuration
├── docker-compose.yml
└── Dockerfile
```

## Running the Simulator

Two equivalent ways to run:

```bash
# Method 1: Script entry (recommended for most users)
python sensors/sensor_simulator.py --config sensors/brokers.yml [options]

# Method 2: Package entry (Python standard)
python -m smarthome_sim --config sensors/brokers.yml [options]
```

## Configuration

Copy `sensors/brokers.example.yml` to `sensors/brokers.yml`:

```yaml
brokers:
  - host: mqtt.example.com
    port: 8883
    tls: true
    ca_file: "../certs/ca/ca.pem"      # Relative to config file
    cert_file: "../certs/client/client.pem"
    key_file: "../certs/client/client.key"
    # Or use inline PEM (takes priority):
    # ca_pem: |
    #   -----BEGIN CERTIFICATE-----
    #   ...
    #   -----END CERTIFICATE-----

simulation:
  devices: 10
  base_topic: "smarthome/sim"
  ha_discovery: false                   # Use --ha-discovery flag instead
  qos: 0
  
  entities:
    - id: temperature
      kind: sensor
      device_class: temperature
      unit: "°C"
      model: drift                      # drift | uniform | sine
      min: 18.0
      max: 28.0
      interval: 5.0
    
    - id: motion
      kind: binary_sensor
      device_class: motion
      model: motion
      interval: 1.0
    
    - id: light
      kind: light
      commandable: true
      initial: { state: "OFF", brightness: 255 }
```

## CLI Options

### Core Options

| Flag | Description | Default |
|------|-------------|---------|
| `-c, --config PATH` | Configuration file (YAML/JSON) | `sensors/brokers.yml` |
| `--devices N` | Number of simulated devices | 10 |
| `--base-topic TOPIC` | MQTT base topic | `smarthome/sim` |
| `--qos 0\|1\|2` | MQTT QoS level | 0 |
| `--retain` | Enable retained messages for state topics | off |
| `--ha-discovery` | Enable Home Assistant MQTT Discovery | off |
| `--discovery-prefix` | HA discovery prefix | `homeassistant` |

### Execution Modes

| Flag | Description |
|------|-------------|
| `--dry-run` | Simulate without publishing (log only) |
| `--once` | Run one publish cycle and exit |
| `--workers N` | Number of worker processes (default: 1) |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR |

### Handshake Benchmark (Thesis Feature)

| Flag | Description | Default |
|------|-------------|---------|
| `--handshake-samples N` | Number of connection samples | 0 (disabled) |
| `--handshake-interval SEC` | Delay between samples | 0.1 |
| `--handshake-timeout SEC` | Connection timeout | 10.0 |
| `--handshake-out PATH` | Output directory | `sensors/handshake_metrics` |
| `--handshake-plot` | Generate histogram/ECDF plots | off |
| `--handshake-only` | Skip simulation, only benchmark | off |

## TLS/mTLS Certificates

Two ways to provide TLS materials:

### 1. File Paths (relative to config file)

```yaml
brokers:
  - host: mqtt.example.com
    tls: true
    ca_file: "../certs/ca/ca.pem"
    cert_file: "../certs/client/client.pem"
    key_file: "../certs/client/client.key"
```

### 2. Inline PEM (takes priority)

```yaml
brokers:
  - host: mqtt.example.com
    tls: true
    ca_pem: |
      -----BEGIN CERTIFICATE-----
      MIIBkTCB+wIJAK...
      -----END CERTIFICATE-----
```

## Entities & Automations

### Entity Types

| Kind | Description | Controllable |
|------|-------------|--------------|
| `sensor` | Numeric values (temperature, humidity) | No |
| `binary_sensor` | ON/OFF states (motion, door) | No |
| `switch` | Controllable switch | Yes (ON/OFF commands) |
| `light` | RGB light with brightness | Yes (JSON commands) |

### Simulation Models

| Model | Description | For |
|-------|-------------|-----|
| `drift` | Random walk within [min, max] | sensor |
| `uniform` | Uniform random in [min, max] | sensor |
| `sine` | Sine wave + noise | sensor |
| `motion` | Random ON/OFF bursts | binary_sensor |

### Automation Coupling

```yaml
simulation:
  automation:
    # Motion triggers light for 30 seconds
    motion_entity: motion
    light_entity: light
    motion_hold_seconds: 30
    
    # Heater affects temperature (+1.5°/min ON, -0.3°/min OFF)
    switch_entity: heater
    sensor_entity: temperature
    delta_per_minute_on: 1.5
    delta_per_minute_off: -0.3
```

## Handshake Benchmark

For thesis-grade TLS handshake latency measurements:

```bash
# Single process, 200 samples
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --handshake-samples 200 \
  --handshake-out sensors/handshake_metrics \
  --handshake-only

# Multi-process (each worker runs N samples)
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --workers 4 \
  --handshake-samples 200 \
  --handshake-only

# With plots (requires matplotlib)
pip install matplotlib
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --handshake-samples 200 \
  --handshake-plot \
  --handshake-only
```

**Outputs:**
- `handshake.w0.jsonl` - Raw records (one JSON per connection)
- `handshake.w0.summary.json` - Statistics (p50/p90/p95/p99, mean, stdev, CI)
- `handshake.w0.hist.png` - Histogram (if `--handshake-plot`)
- `handshake.w0.ecdf.png` - ECDF plot (if `--handshake-plot`)

## Home Assistant Device Metadata

Configure device info shown in HA via `simulation.device`:

```yaml
simulation:
  device:
    identifiers: ["sim_device_{device_id}"]
    name: "Sim Device {device_id}"
    model: "SmartHome Simulator"
    manufacturer: "Eurun Lab"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Activate venv: `. .venv/bin/activate` |
| EMQX auth failed | Check `username`/`password` in `brokers.yml` |
| TLS connection failed | Verify `tls: true`, port (usually 8883), cert paths |
| HA entities not appearing | Add `--ha-discovery` flag |
| High CPU usage | Reduce `--devices` or increase entity `interval` |

Debug mode:
```bash
python sensors/sensor_simulator.py --config sensors/brokers.yml --log-level DEBUG
```

---

**Requirements:** Python 3.8+ | paho-mqtt>=1.6,<2.0 | PyYAML>=6.0 | matplotlib (optional)
