# ESPHome Firmware Configurations

Language: **English** | [简体中文](README.zh-CN.md)

This directory contains ESPHome YAML configurations for ESP32 and ESP32-S3 edge nodes in the Smart Home IoT system.

## Device Configurations

| File | Target | Description |
|------|--------|-------------|
| `esp32.yaml` | ESP32 DevKit | Environment sensor node (Node B) |
| `esp32s3.yaml` | ESP32-S3 | Advanced node with USB/PSRAM support |
| `secrets.yaml` | - | Credentials and certificates (git-ignored) |

## Quick Start

### 1. Setup Secrets

```bash
cp secrets.example.yaml secrets.yaml
# Edit secrets.yaml with your credentials and certificates
```

### 2. Flash Device

```bash
# Using ESPHome CLI
pip install esphome
esphome run esp32.yaml

# Or using ESPHome Dashboard
esphome dashboard .
```

## Configuration Structure

### secrets.yaml (Template)

```yaml
# WiFi
wifi_ssid: "YOUR_SSID"
wifi_password: "YOUR_PASSWORD"

# MQTT Broker
mqtt_broker: "mqtt.example.com"
mqtt_port: "8883"

# OTA & API Keys
ota_password: "YOUR_OTA_PASSWORD"
api_key_esp32: "YOUR_API_KEY"

# TLS Certificates (inline PEM)
mqtt_ca_cert: |
  -----BEGIN CERTIFICATE-----
  (paste ca.pem content)
  -----END CERTIFICATE-----

mqtt_client_cert: |
  -----BEGIN CERTIFICATE-----
  (paste client.pem content)
  -----END CERTIFICATE-----

mqtt_client_key: |
  -----BEGIN EC PRIVATE KEY-----
  (paste client.key content)
  -----END EC PRIVATE KEY-----
```

## Security Features

- **mTLS**: Mutual TLS authentication with ECDSA P-256 certificates
- **TLS 1.3**: Enabled via ESP-IDF mbedtls configuration
- **Encrypted API**: Native API with encryption key
- **OTA Protection**: Password-protected over-the-air updates

## Hardware Support

### ESP32 (esp32.yaml)
- Framework: ESP-IDF
- Crypto: Hardware-accelerated ECDSA P-256
- Use case: Environmental monitoring (temperature, humidity, motion)

### ESP32-S3 (esp32s3.yaml)
- Framework: ESP-IDF
- Features: USB-OTG, PSRAM support
- Use case: Advanced edge computing with camera/ML

## Related Documentation

- [ESPHome MQTT Component](https://esphome.io/components/mqtt.html)
- [ESP32 Datasheet](https://www.espressif.com/en/products/socs/esp32)
- [ESP32-S3 Datasheet](https://www.espressif.com/en/products/socs/esp32-s3)
- [Certificate Setup](../certs/README.md)

# [CodeRabbit Audit Trigger 1769364389]
