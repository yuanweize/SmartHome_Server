# MQTT Broker 配置

语言：**简体中文** | [English](README.md)

本目录包含支持 mTLS 的 MQTT Broker Docker Compose 配置。

## 可用 Broker

| Broker | 目录 | 描述 |
|--------|------|------|
| **EMQX** | `emqx/` | 企业级 MQTT Broker（推荐） |
| **Mosquitto** | `mosquitto/` | 轻量级备选方案 |

## EMQX（推荐）

EMQX 是高度可扩展的 MQTT Broker，内置集群、仪表盘及出色的 mTLS 支持。

### 快速开始

```bash
cd broker/emqx

# 复制证书
mkdir -p certs
cp ../../certs/ca/ca.pem certs/
cp ../../certs/server/server.pem certs/
cp ../../certs/server/server.key certs/

# 启动 Broker
docker compose up -d
```

### 访问仪表盘

- 地址：`http://localhost:18083`
- 默认凭证：`admin` / `public`

### 已启用功能

- **端口 8883**：MQTTS（MQTT over TLS）
- **mTLS**：要求客户端证书验证
- **匿名访问**：已禁用

## Mosquitto

Mosquitto 是一款轻量级开源 MQTT Broker。

### 快速开始

```bash
cd broker/mosquitto
docker compose up -d
```

## 证书配置

证书生成说明请参阅 [`../certs/README.zh-CN.md`](../certs/README.zh-CN.md)。

## 安全说明

- 两种配置均强制启用 **mTLS**（双向 TLS 认证）
- **已禁用**匿名连接
- 仪表盘仅绑定至 localhost

## 相关文档

- [EMQX 文档](https://www.emqx.io/docs/zh/latest/)
- [Mosquitto 文档](https://mosquitto.org/documentation/)
