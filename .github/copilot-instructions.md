# Copilot Instructions for SmartHome_Server

## Project Overview

A thesis-grade smart home platform for simulating and benchmarking IoT sensor/actuator traffic over MQTT with mTLS support. Designed for Home Assistant integration and stress testing.

## Architecture

```
┌─────────────────┐    MQTTS (8883)    ┌─────────────────┐
│  smarthome_sim  │ ◄─────────────────► │  EMQX/Mosquitto │
│  (Python pkg)   │                     │  (mTLS enforced)│
└─────────────────┘                     └─────────────────┘
       │ HA Discovery                          │
       └──────────► homeassistant ◄────────────┘
```

## Package Structure

```
sensors/
├── smarthome_sim/              # Python package (core code ~800 lines)
│   ├── __init__.py             # Version, public API exports
│   ├── __main__.py             # `python -m smarthome_sim` entry
│   ├── cli.py                  # CLI argument parsing
│   ├── broker.py               # Broker class + TLS/mTLS handling
│   ├── config.py               # Configuration loading & parsing
│   ├── simulator.py            # Simulator core class
│   ├── entities.py             # EntityDef, EntityInstance, MQTTContext
│   ├── benchmark.py            # Handshake benchmark (thesis feature)
│   └── utils.py                # Shared utilities
├── sensor_simulator.py         # Backward-compatible entry (16 lines)
├── brokers.example.yml         # Example config (copy to brokers.yml)
├── docker-compose.yml
└── Dockerfile

broker/emqx/                    # EMQX Docker config with mTLS
broker/mosquitto/               # Mosquitto Docker config
homeassistant/                  # Home Assistant container
esphome/                        # Real ESP32 firmware configs
certs/                          # TLS certificates (CA, server, client)
```

## Key Configuration

### `sensors/brokers.yml` (git-ignored)
Contains **both** broker connections AND simulation definitions:
```yaml
brokers:
  - host: mqtt.example.com
    port: 8883
    tls: true
    ca_file: "../certs/ca/ca.pem"  # Relative to config file!

simulation:
  devices: 10
  entities:
    - id: temperature
      kind: sensor  # sensor | binary_sensor | switch | light
      model: drift  # drift | uniform | sine | motion
```

## Common Workflows

```bash
# Quick start
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# Dry-run test
python sensors/sensor_simulator.py --config sensors/brokers.yml --dry-run

# Connect to Home Assistant
python sensors/sensor_simulator.py --config sensors/brokers.yml --ha-discovery

# Stress test (12000 devices, 6 workers)
python sensors/sensor_simulator.py --config sensors/brokers.yml --devices 12000 --workers 6 --qos 0

# TLS handshake benchmark
python sensors/sensor_simulator.py --config sensors/brokers.yml \
  --handshake-samples 200 --handshake-out sensors/handshake_metrics --handshake-only
```

## Code Patterns

### Editing the simulator
- Core logic is in `sensors/smarthome_sim/simulator.py`
- Entity models in `sensors/smarthome_sim/entities.py`
- Config parsing in `sensors/smarthome_sim/config.py`
- TLS/mTLS in `sensors/smarthome_sim/broker.py`

### CLI precedence
`CLI flags > brokers.yml > built-in defaults`

### MQTT topics
- State: `{base_topic}/device_{id}/{entity}/state`
- Command: `{base_topic}/device_{id}/{entity}/set`
- Discovery: `{discovery_prefix}/{kind}/device_{id}_{entity}/config`

## Dependencies

- **Runtime:** `paho-mqtt>=1.6,<2.0`, `PyYAML>=6.0`
- **Optional:** `matplotlib` (for handshake plots)

## Common Issues

1. **TLS path errors:** Paths in `brokers.yml` are relative to the config file
2. **HA Discovery not working:** Add `--ha-discovery` flag (disabled by default)
3. **Import errors:** Run from repo root with venv activated
