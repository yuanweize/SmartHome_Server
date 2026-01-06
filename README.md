# SmartHome Server

Language: **English** | [简体中文](README.zh-CN.md)

A thesis-grade smart home IoT platform for simulating and benchmarking sensor/actuator traffic over MQTT with mTLS support. Designed for Home Assistant integration, security research, and scalability testing.

> **Academic Project:** This repository accompanies the bachelor thesis *"Application of Servers and Unix-like Systems for Sensor Control in Smart Homes"* at Czech Technical University in Prague, Faculty of Electrical Engineering.

## Architecture

```
┌─────────────────┐    MQTTS (8883)    ┌─────────────────┐
│  smarthome_sim  │ ◄─────────────────► │  EMQX/Mosquitto │
│  (Python pkg)   │                     │  (mTLS enforced)│
└─────────────────┘                     └─────────────────┘
       │ HA Discovery                          │
       └──────────► Home Assistant ◄───────────┘
```

## Repository Structure

```
SmartHome_Server/
├── sensors/                # Python MQTT simulator package
│   └── smarthome_sim/      # Core library (~800 lines)
├── broker/                 # MQTT broker configurations
│   ├── emqx/               # EMQX Docker with mTLS
│   └── mosquitto/          # Mosquitto Docker alternative
├── homeassistant/          # Home Assistant Docker + automation templates
├── esphome/                # ESP32/ESP32-S3 firmware configurations
├── certs/                  # TLS/mTLS certificate templates
└── docs/                   # Thesis documentation (LaTeX)
```

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/IYUANWEIZE/SmartHome_Server.git
cd SmartHome_Server
python3 -m venv .venv && source .venv/bin/activate
pip install -r sensors/requirements.txt
```

### 2. Configure and Run Simulator

```bash
cp sensors/brokers.example.yml sensors/brokers.yml
# Edit brokers.yml with your MQTT broker details

# Dry-run (no broker required)
python sensors/sensor_simulator.py --dry-run

# With Home Assistant discovery
python sensors/sensor_simulator.py --ha-discovery
```

### 3. Deploy MQTT Broker (Optional)

```bash
cd broker/emqx && docker compose up -d
```

## Features

| Component | Description |
|-----------|-------------|
| **smarthome_sim** | Multi-broker MQTT simulator with entity models (drift, sine, motion) |
| **mTLS Security** | ECDSA P-256 certificates for mutual authentication |
| **HA Integration** | Auto-discovery of sensors, switches, and lights |
| **Benchmarking** | TLS handshake latency measurement with statistical analysis |
| **Scalability** | Multi-process workers for 10,000+ simulated devices |

## Documentation

| Directory | Description |
|-----------|-------------|
| [sensors/README.md](sensors/README.md) | Simulator usage and configuration |
| [certs/README](certs/README) | Certificate generation guide |
| [homeassistant/README.md](homeassistant/README.md) | Home Assistant setup |
| [docs/README.md](docs/README.md) | Thesis LaTeX source |

## Requirements

- Python 3.8+
- Docker & Docker Compose (for broker/HA deployment)
- OpenSSL (for certificate generation)

## License

This project is licensed under the [MIT License](LICENSE).

## Citation

If you use this project in academic work, please cite:

```bibtex
@thesis{yuan2026smarthome,
    author  = {Yuan, Weize},
    title   = {Application of Servers and Unix-like Systems for Sensor Control in Smart Homes},
    school  = {Czech Technical University in Prague, Faculty of Electrical Engineering},
    year    = {2026},
    type    = {Bachelor's Thesis}
}
```

## Acknowledgments

This project was developed under the supervision of [Prof. Miroslav Husák](https://fel.cvut.cz/en/faculty/people/966-miroslav-husak) at the Department of Microelectronics, CTU FEL.

## Author

**Weize Yuan** - B.Sc. in Electrical Engineering and Computer Science (EECS)  
Czech Technical University in Prague, Faculty of Electrical Engineering  
GitHub: [@IYUANWEIZE](https://github.com/IYUANWEIZE)
