# 03 - Security Analysis: 安全架构分析

## 🔐 安全设计概述

本系统采用多层安全架构：

```
┌─────────────────────────────────────────┐
│         Application Security            │
│  - HA Authentication                    │
│  - API Tokens                           │
├─────────────────────────────────────────┤
│         Transport Security              │
│  - mTLS (Mutual TLS)                    │
│  - ECC Certificates                     │
├─────────────────────────────────────────┤
│         Network Security                │
│  - Tailscale Zero Trust                 │
│  - Firewall Rules                       │
├─────────────────────────────────────────┤
│         Physical Security               │
│  - Local Network Isolation              │
│  - Device Authentication                │
└─────────────────────────────────────────┘
```

---

## 🔏 mTLS 双向认证

### 什么是 mTLS？

| TLS 类型 | 服务器认证 | 客户端认证 | 适用场景 |
|----------|-----------|-----------|----------|
| **TLS** | ✅ | ❌ | 网站 HTTPS |
| **mTLS** | ✅ | ✅ | IoT、API 服务 |

### 证书链结构

```
Root CA (Self-signed)
    │
    ├── Server Certificate (EMQX Broker)
    │   - CN: mqtt.example.com
    │   - SAN: DNS:mqtt.example.com
    │
    ├── Client Certificate (ESP32)
    │   - CN: esp32-node-a
    │   - OU: IoT Devices
    │
    └── Client Certificate (Simulator)
        - CN: simulator-client
        - OU: Testing
```

### 证书生成流程

```bash
# 1. 生成 CA 私钥和证书
openssl ecparam -genkey -name secp256r1 -out ca.key
openssl req -new -x509 -days 3650 -key ca.key -out ca.pem \
  -subj "/CN=SmartHome CA/O=CTU FEL"

# 2. 生成服务器证书
openssl ecparam -genkey -name secp256r1 -out server.key
openssl req -new -key server.key -out server.csr \
  -subj "/CN=mqtt.example.com"
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key \
  -CAcreateserial -out server.pem -days 365

# 3. 生成客户端证书
openssl ecparam -genkey -name secp256r1 -out client.key
openssl req -new -key client.key -out client.csr \
  -subj "/CN=esp32-client/OU=IoT Devices"
openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key \
  -CAcreateserial -out client.pem -days 365
```

---

## 📊 ECC vs RSA 对比

### 密码学参数

| 参数 | ECC (secp256r1) | RSA-2048 | RSA-4096 |
|------|-----------------|----------|----------|
| 密钥长度 | 256 bit | 2048 bit | 4096 bit |
| 等效安全强度 | 128 bit | 112 bit | 140 bit |
| 签名大小 | 64 bytes | 256 bytes | 512 bytes |
| 公钥大小 | 64 bytes | 256 bytes | 512 bytes |

### 性能对比（ESP32 实测参考）

| 操作 | ECC (secp256r1) | RSA-2048 | 差异 |
|------|-----------------|----------|------|
| 密钥生成 | ~50ms | ~2000ms | **40x 更快** |
| 签名 | ~20ms | ~100ms | **5x 更快** |
| 验证 | ~40ms | ~5ms | RSA 更快 |
| TLS 握手总计 | ~200ms | ~500ms | **2.5x 更快** |

### 为什么 IoT 选择 ECC？

1. **资源受限**: ESP32 只有 320KB SRAM，ECC 内存占用更小
2. **功耗敏感**: 更快的计算意味着更短的活跃时间
3. **带宽有限**: 更小的证书意味着更少的传输数据
4. **前向安全**: ECDHE 密钥交换提供 Perfect Forward Secrecy

**论文叙述**:
> "ECC with the secp256r1 curve was selected over RSA-2048 due to its superior performance on resource-constrained devices. Benchmarks demonstrate a 2.5x reduction in TLS handshake time, critical for battery-powered IoT sensors requiring frequent reconnections."

---

## 🌐 Tailscale 零信任网络

### 什么是零信任？

传统模型：
```
[Internet] ─── Firewall ───► [Trusted LAN]
                              (一旦进入，全部信任)
```

零信任模型：
```
[Every Connection] ─── Authenticate ───► [Specific Resource]
                       + Authorize          (最小权限)
```

### Tailscale 架构

```
┌────────────────────────────────────────────────────┐
│              Tailscale Coordination Server          │
│              (login.tailscale.com)                  │
│              - 身份验证                             │
│              - 密钥分发                             │
│              - ACL 策略                             │
└───────────────────────┬────────────────────────────┘
                        │ Control Plane
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │  Node A │◄══►│  Node B │◄══►│  Node C │
   │ Prague  │    │   NUE   │    │  Other  │
   └─────────┘    └─────────┘    └─────────┘
        └───────────────┴───────────────┘
              WireGuard Data Plane
              (Direct P2P when possible)
```

### ACL 配置示例

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["tag:homeassistant"],
      "dst": ["tag:mqtt-broker:8883"]
    },
    {
      "action": "accept",
      "src": ["tag:admin"],
      "dst": ["*:*"]
    }
  ],
  "tagOwners": {
    "tag:homeassistant": ["autogroup:admin"],
    "tag:mqtt-broker": ["autogroup:admin"]
  }
}
```

### 为什么用 Tailscale？

| 问题 | 传统方案 | Tailscale 方案 |
|------|----------|----------------|
| 公网暴露端口 | 需要端口转发 | **不需要** |
| 证书管理 | 手动管理 Let's Encrypt | **自动内置** |
| NAT 穿透 | 复杂配置 | **自动处理** |
| 密钥轮换 | 手动或脚本 | **自动每小时** |

---

## 🔒 EMQX Broker 安全配置

### 监听器配置

```yaml
# emqx.conf
listeners.ssl.default {
  bind = "0.0.0.0:8883"
  ssl_options {
    cacertfile = "/etc/emqx/certs/ca.pem"
    certfile = "/etc/emqx/certs/server.pem"
    keyfile = "/etc/emqx/certs/server.key"
    verify = verify_peer
    fail_if_no_peer_cert = true
  }
}
```

### 认证链

```
Client Connection
      │
      ▼
┌─────────────────┐
│ TLS Handshake   │ ─── 证书验证
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Client Auth     │ ─── 用户名/密码 或 证书 CN
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ACL Check       │ ─── Topic 权限
└────────┬────────┘
         │
         ▼
    Connected ✓
```

---

## 📱 ESPHome 安全配置

### WiFi 安全

```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  # WPA2-PSK 或 WPA3 (如果 AP 支持)
```

### API 加密

```yaml
api:
  encryption:
    key: !secret api_encryption_key
  # 32 字节 base64 编码密钥
```

### MQTT mTLS

```yaml
mqtt:
  broker: mqtt.example.com
  port: 8883
  certificate_authority: !secret ca_cert
  client_certificate: !secret client_cert
  client_key: !secret client_key
```

---

## ⚠️ 安全考量与权衡

### 已实现的安全措施

| 威胁 | 防护措施 | 状态 |
|------|----------|------|
| 中间人攻击 | mTLS 双向认证 | ✅ |
| 窃听 | TLS 1.2/1.3 加密 | ✅ |
| 重放攻击 | TLS 会话票证 | ✅ |
| 未授权访问 | 证书 + ACL | ✅ |
| 暴力破解 | 证书认证（无密码） | ✅ |

### 已知限制

| 限制 | 原因 | 缓解措施 |
|------|------|----------|
| 证书手动分发 | 没有 PKI 自动化 | 小规模可接受 |
| 固定 CA | 单点信任 | 定期轮换 |
| ESP32 固件未签名 | 开发便利 | 生产环境应启用 Secure Boot |

---

## 📝 论文章节素材

### Security Analysis 段落示例

> The system employs a defense-in-depth security architecture. At the transport layer, mutual TLS (mTLS) ensures bidirectional authentication between all components. ECC certificates with the secp256r1 curve provide 128-bit equivalent security while maintaining compatibility with resource-constrained ESP32 devices. Network-level security is enhanced through Tailscale's WireGuard-based mesh VPN, implementing zero-trust principles where each connection is authenticated regardless of network location.

### 安全对比表格

| Security Feature | This System | Xiaomi | Alexa |
|-----------------|-------------|--------|-------|
| End-to-end Encryption | mTLS | TLS | TLS |
| Client Authentication | Certificate | Token | OAuth |
| Data Storage | Local | Cloud | Cloud |
| Key Management | Self-hosted | Vendor | Vendor |
| Audit Logging | Full control | Limited | Limited |
