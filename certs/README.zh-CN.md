# 智能家居 IoT 安全证书 (ECDSA P-256)

语言：**简体中文** | [English](README.md)

本目录包含智能家居 IoT 系统的 TLS 证书。系统采用 **mTLS（双向 TLS）** 机制保护 MQTT Broker（EMQX）、边缘节点（ESP32/ESP32-S3）与控制器（Home Assistant）之间的通信安全。

## ⚠️ 安全警告

* **私钥文件**（`.key`）**严禁**提交至 Git 或公开分享
* 确保本目录已添加至 `.gitignore`

## 目录结构

```
certs/
├── ca/         # 根证书颁发机构
│   ├── ca.pem      # CA 公钥证书（部署至所有设备）
│   └── ca.key      # CA 私钥（绝密 - 仅用于签发）
├── server/     # MQTT Broker (EMQX)
│   ├── server.pem  # 服务端证书
│   └── server.key  # 服务端私钥
├── client/     # IoT 设备 (ESP32)
│   ├── client.pem  # 客户端证书
│   └── client.key  # 客户端私钥
└── ha/         # Home Assistant 控制器
    ├── ha.pem      # HA 客户端证书
    └── ha.key      # HA 私钥
```

## 证书规格

| 证书 | 算法 | 曲线 | 有效期 | CN |
|------|------|------|--------|-----|
| 根 CA | ECDSA | P-256 | 10 年 | SmartHome Root CA |
| 服务端 | ECDSA | P-256 | 5 年 | (你的 MQTT 域名) |
| 客户端 (ESP32) | ECDSA | P-256 | 1 年 | esp-client |
| Home Assistant | ECDSA | P-256 | 5 年 | homeassistant |

## 证书生成

```bash
cd certs && mkdir -p ca server client ha

# 1. 根 CA（10 年）
openssl ecparam -name prime256v1 -genkey -noout -out ca/ca.key
openssl req -new -x509 -sha256 -days 3650 \
  -key ca/ca.key -out ca/ca.pem \
  -subj "/CN=SmartHome Root CA/O=CTU FEL/C=CZ"

# 2. 服务端证书（5 年）- 替换 YOUR_MQTT_DOMAIN 为你的域名
openssl ecparam -name prime256v1 -genkey -noout -out server/server.key
openssl req -new -key server/server.key -out server/server.csr \
  -subj "/CN=YOUR_MQTT_DOMAIN/O=SmartHome/OU=Broker"
openssl x509 -req -sha256 -days 1825 \
  -in server/server.csr -CA ca/ca.pem -CAkey ca/ca.key -CAcreateserial \
  -out server/server.pem

# 3. ESP32 客户端证书（1 年）
openssl ecparam -name prime256v1 -genkey -noout -out client/client.key
openssl req -new -key client/client.key -out client/client.csr \
  -subj "/CN=esp-client/O=SmartHome/OU=Sensors"
openssl x509 -req -sha256 -days 365 \
  -in client/client.csr -CA ca/ca.pem -CAkey ca/ca.key -CAcreateserial \
  -out client/client.pem

# 4. Home Assistant 证书（5 年）
openssl ecparam -name prime256v1 -genkey -noout -out ha/ha.key
openssl req -new -key ha/ha.key -out ha/ha.csr \
  -subj "/CN=homeassistant/O=SmartHome/OU=Controller"
openssl x509 -req -sha256 -days 1825 \
  -in ha/ha.csr -CA ca/ca.pem -CAkey ca/ca.key -CAcreateserial \
  -out ha/ha.pem

# 验证
openssl x509 -in ca/ca.pem -noout -subject -dates
openssl x509 -in server/server.pem -noout -subject -dates
openssl x509 -in client/client.pem -noout -subject -dates
openssl x509 -in ha/ha.pem -noout -subject -dates
```

## 使用方式

部署示例请参考：
- [broker/emqx/docker-compose.yml](../broker/emqx/docker-compose.yml) - EMQX mTLS 配置
- [esphome/*.yaml](../esphome/) - ESP32 客户端证书配置
- [sensors/brokers.example.yml](../sensors/brokers.example.yml) - 模拟器 TLS 配置

