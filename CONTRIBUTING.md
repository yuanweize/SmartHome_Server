# Contributing to SmartHome_Server

Thank you for contributing to the SmartHome_Server project! Whether improving documentation, refining ESPHome device configurations, or enhancing MQTT security, your help is appreciated.

## Architecture Overview

SmartHome_Server comprises:
- **Broker (`broker/`)**: Mosquitto MQTT server with mTLS configuration and access control lists.
- **Certificates (`certs/`)**: Automated scripts for certificate authority (CA), server certificate, and client certificate generation.
- **ESPHome (`esphome/`)**: Firmware definitions and pinouts for ESP32/ESP8266 IoT sensors.
- **Home Assistant (`homeassistant/`)**: Integrations, automations, and dashboards.

## Contribution Guidelines

1. **Never Commit Secrets**:
   - Check `git status` carefully before staging files.
   - Do not commit private keys (`*.key`), production certificates, Wi-Fi SSIDs/passwords, or Home Assistant tokens.
   - Use `*.example` files to document new configuration variables.

2. **Validation & Testing**:
   - Validate YAML syntax before opening a PR (`esphome config <file>.yaml` or yamllint).
   - Test mTLS handshakes locally using self-signed test certificates.

3. **Pull Request Workflow**:
   - Create a feature branch (`git checkout -b feat/your-improvement`).
   - Use clear commit messages following Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
   - Submit a PR explaining the changes and testing performed.
