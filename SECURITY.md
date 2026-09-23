# Security Policy

## Supported Versions

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| thesis-v26.x | :white_check_mark: | Current active release line |
| < thesis-v26 | :x:                | Archived / experimental builds |

## Security Architecture & IoT Hardening

SmartHome_Server is architected around mutual TLS (mTLS) cryptographic isolation for private home automation:

1. **Mutual TLS (mTLS) Enforcement**: MQTT broker traffic requires valid X.509 client and server certificates. Cleartext TCP MQTT connections are disabled by default.
2. **Credential & Secret Protection**: Sensitive credentials, broker passwords, Wi-Fi keys, and private keys (`*.key`, `secrets.yaml`) must never be committed to source control. Template files (`.example`) are provided for configuration.
3. **Network Boundary Isolation**: Microcontroller nodes (ESP32/ESP8266) communicate exclusively over isolated IoT VLANs or local subnetworks without requiring inbound public port forwarding.

## Reporting a Vulnerability

If you discover a security vulnerability, certificate handling issue, or network leak:

1. **Do NOT report security issues via public GitHub issues.**
2. Report privately via [GitHub Security Advisories](https://github.com/yuanweize/SmartHome_Server/security/advisories/new) or contact the maintainer directly at `yuanweize@users.noreply.github.com`.
3. Provide details on the affected component (Broker, ESPHome firmware, or Home Assistant integration) and reproduction steps.
4. We will acknowledge receipt within 48 hours.
