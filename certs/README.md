# Smart Home IoT Security Certificates (ECDSA P-256)

Language: **English** | [简体中文](README.zh-CN.md)

This directory contains TLS certificates for the Smart Home IoT system.
The system uses **mTLS (Mutual TLS)** to secure communication between the MQTT broker (EMQX), edge nodes (ESP32/ESP32-S3), and the controller (Home Assistant).

## ⚠️ Security Warning

* **Private keys** (`.key` files) must **NEVER** be committed to Git or shared publicly.
* Ensure this directory is listed in `.gitignore`.

## Directory Structure

```
certs/
├── ca/         # Root Certificate Authority
│   ├── ca.pem      # CA public certificate (deploy to all devices)
│   └── ca.key      # CA private key (TOP SECRET - sign only)
├── server/     # MQTT Broker (EMQX)
│   ├── server.pem  # Server certificate
│   └── server.key  # Server private key
├── client/     # IoT Devices (ESP32)
│   ├── client.pem  # Client certificate
│   └── client.key  # Client private key
└── ha/         # Home Assistant Controller
    ├── ha.pem      # HA client certificate
    └── ha.key      # HA private key
```

## Certificate Specifications

| Certificate | Algorithm | Curve | Validity | CN |
|-------------|-----------|-------|----------|-----|
| Root CA | ECDSA | P-256 | 10 years | SmartHome Root CA |
| Server | ECDSA | P-256 | 5 years | (your MQTT domain) |
| Client (ESP32) | ECDSA | P-256 | 1 year | esp-client |
| Home Assistant | ECDSA | P-256 | 5 years | homeassistant |

## Certificate Generation

```bash
cd certs && mkdir -p ca server client ha

# 1. Root CA (10 years)
openssl ecparam -name prime256v1 -genkey -noout -out ca/ca.key
openssl req -new -x509 -sha256 -days 3650 \
  -key ca/ca.key -out ca/ca.pem \
  -subj "/CN=SmartHome Root CA/O=CTU FEL/C=CZ"

# 2. Server Certificate (5 years) - Replace YOUR_MQTT_DOMAIN
openssl ecparam -name prime256v1 -genkey -noout -out server/server.key
openssl req -new -key server/server.key -out server/server.csr \
  -subj "/CN=YOUR_MQTT_DOMAIN/O=SmartHome/OU=Broker"
openssl x509 -req -sha256 -days 1825 \
  -in server/server.csr -CA ca/ca.pem -CAkey ca/ca.key -CAcreateserial \
  -out server/server.pem

# 3. Client Certificate for ESP32 (1 year)
openssl ecparam -name prime256v1 -genkey -noout -out client/client.key
openssl req -new -key client/client.key -out client/client.csr \
  -subj "/CN=esp-client/O=SmartHome/OU=Sensors"
openssl x509 -req -sha256 -days 365 \
  -in client/client.csr -CA ca/ca.pem -CAkey ca/ca.key -CAcreateserial \
  -out client/client.pem

# 4. Home Assistant Certificate (5 years)
openssl ecparam -name prime256v1 -genkey -noout -out ha/ha.key
openssl req -new -key ha/ha.key -out ha/ha.csr \
  -subj "/CN=homeassistant/O=SmartHome/OU=Controller"
openssl x509 -req -sha256 -days 1825 \
  -in ha/ha.csr -CA ca/ca.pem -CAkey ca/ca.key -CAcreateserial \
  -out ha/ha.pem

# Verify
openssl x509 -in ca/ca.pem -noout -subject -dates
openssl x509 -in server/server.pem -noout -subject -dates
openssl x509 -in client/client.pem -noout -subject -dates
openssl x509 -in ha/ha.pem -noout -subject -dates
```

## Usage

For deployment examples, see:
- [broker/emqx/docker-compose.yml](../broker/emqx/docker-compose.yml) - EMQX mTLS configuration
- [esphome/*.yaml](../esphome/) - ESP32 client certificate configuration
- [sensors/brokers.example.yml](../sensors/brokers.example.yml) - Simulator TLS configuration

# [CodeRabbit Audit Trigger 1769364389]
