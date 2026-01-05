# ESPHome 固件配置

语言：**简体中文** | [English](README.md)

本目录包含智能家居 IoT 系统中 ESP32 和 ESP32-S3 边缘节点的 ESPHome YAML 配置。

## 设备配置

| 文件 | 目标设备 | 描述 |
|------|----------|------|
| `esp32.yaml` | ESP32 DevKit | 环境传感器节点 (Node B) |
| `esp32s3.yaml` | ESP32-S3 | 高级节点（支持 USB/PSRAM） |
| `secrets.yaml` | - | 凭证与证书（已 git 忽略） |

## 快速开始

### 1. 配置 Secrets

```bash
cp secrets.example.yaml secrets.yaml
# 编辑 secrets.yaml，填入你的凭证和证书
```

### 2. 烧录设备

```bash
# 使用 ESPHome CLI
pip install esphome
esphome run esp32.yaml

# 或使用 ESPHome 仪表盘
esphome dashboard .
```

## 配置结构

### secrets.yaml（模板）

```yaml
# WiFi
wifi_ssid: "你的SSID"
wifi_password: "你的密码"

# MQTT Broker
mqtt_broker: "mqtt.example.com"
mqtt_port: "8883"

# OTA & API 密钥
ota_password: "你的OTA密码"
api_key_esp32: "你的API密钥"

# TLS 证书（内联 PEM）
mqtt_ca_cert: |
  -----BEGIN CERTIFICATE-----
  (粘贴 ca.pem 内容)
  -----END CERTIFICATE-----

mqtt_client_cert: |
  -----BEGIN CERTIFICATE-----
  (粘贴 client.pem 内容)
  -----END CERTIFICATE-----

mqtt_client_key: |
  -----BEGIN EC PRIVATE KEY-----
  (粘贴 client.key 内容)
  -----END EC PRIVATE KEY-----
```

## 安全特性

- **mTLS**：基于 ECDSA P-256 证书的双向 TLS 认证
- **TLS 1.3**：通过 ESP-IDF mbedtls 配置启用
- **加密 API**：原生 API 使用加密密钥
- **OTA 保护**：密码保护的空中升级

## 硬件支持

### ESP32 (esp32.yaml)
- 框架：ESP-IDF
- 加密：硬件加速 ECDSA P-256
- 用途：环境监测（温度、湿度、运动）

### ESP32-S3 (esp32s3.yaml)
- 框架：ESP-IDF
- 特性：USB-OTG、PSRAM 支持
- 用途：高级边缘计算（摄像头/机器学习）

## 相关文档

- [ESPHome MQTT 组件](https://esphome.io/components/mqtt.html)
- [ESP32 数据手册](https://www.espressif.com/zh-hans/products/socs/esp32)
- [ESP32-S3 数据手册](https://www.espressif.com/zh-hans/products/socs/esp32-s3)
- [证书配置](../certs/README.zh-CN.md)
