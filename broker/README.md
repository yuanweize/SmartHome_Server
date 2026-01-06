# MQTT Broker Configurations

Language: **English** | [简体中文](README.zh-CN.md)

This directory contains Docker Compose configurations for MQTT brokers with mTLS support.

## Available Brokers

| Broker | Directory | Description |
|--------|-----------|-------------|
| **EMQX** | `emqx/` | Enterprise-grade MQTT broker (recommended) |
| **Mosquitto** | `mosquitto/` | Lightweight alternative |

## EMQX (Recommended)

EMQX is a highly scalable MQTT broker with built-in clustering, dashboard, and excellent mTLS support.

### Quick Start

```bash
cd broker/emqx

# Copy certificates
mkdir -p certs
cp ../../certs/ca/ca.pem certs/
cp ../../certs/server/server.pem certs/
cp ../../certs/server/server.key certs/

# Start broker
docker compose up -d
```

### Access Dashboard

- URL: `http://localhost:18083`
- Default credentials: `admin` / `public`

### Features Enabled

- **Port 8883**: MQTTS (MQTT over TLS)
- **mTLS**: Client certificate verification required
- **Anonymous access**: Disabled

## Mosquitto

Mosquitto is a lightweight open-source MQTT broker.

### Quick Start

```bash
cd broker/mosquitto
docker compose up -d
```

## Certificate Setup

See [`../certs/README.md`](../certs/README.md) for certificate generation instructions.

## Security Notes

- Both configurations enforce **mTLS** (mutual TLS authentication)
- Anonymous connections are **disabled**
- Dashboard access is bound to localhost only

## Related Documentation

- [EMQX Documentation](https://www.emqx.io/docs/en/latest/)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)
