# SmartHome 模拟器

语言：**简体中文** | [English](README.md)

面向论文/实验的多 Broker MQTT 智能家居模拟器，支持 mTLS，可与 Home Assistant 集成及压力测试。

## 功能特性

- 🔌 **多 Broker 支持** - 同时向多个 MQTT Broker 发布
- 🏠 **Home Assistant Discovery** - 自动在 HA 中注册实体
- 🎮 **可控执行器** - 通过 MQTT 命令控制开关/灯光
- 🔐 **TLS/mTLS** - 支持文件路径或内联 PEM 证书
- ⚡ **多进程扩展** - `--workers` 充分利用多核 CPU
- 📊 **握手统计** - 论文级延迟测量与统计分析

## 快速开始

```bash
# 安装依赖
cd SmartHome_Server
python3 -m venv .venv && . .venv/bin/activate
pip install -r sensors/requirements.txt

# 复制并编辑配置
cp sensors/brokers.example.yml sensors/brokers.yml

# 演练模式（无需 Broker）
python sensors/sensor_simulator.py --dry-run

# 连接 Broker 并启用 Home Assistant Discovery
python sensors/sensor_simulator.py --config sensors/brokers.yml --ha-discovery

# 压力测试：1000 设备，4 进程
python sensors/sensor_simulator.py --config sensors/brokers.yml --devices 1000 --workers 4
```

## 包结构

```
sensors/
├── sensor_simulator.py         # 入口脚本（含版本检查和错误处理）
├── smarthome_sim/              # Python 包
│   ├── __init__.py             # 版本：1.0.0，公共 API 导出
│   ├── __main__.py             # `python -m smarthome_sim` 入口
│   ├── cli.py                  # CLI 参数解析
│   ├── config.py               # 配置加载（YAML/JSON）
│   ├── broker.py               # Broker 类 + TLS/mTLS 处理
│   ├── simulator.py            # 核心模拟逻辑
│   ├── entities.py             # 实体模型（EntityDef, EntityInstance）
│   ├── benchmark.py            # TLS 握手基准测试
│   └── utils.py                # 工具函数
├── brokers.example.yml         # 配置示例
├── docker-compose.yml
└── Dockerfile
```

## 运行方式

两种等效的运行方式：

```bash
# 方式 1：脚本入口（推荐大多数用户）
python sensors/sensor_simulator.py --config sensors/brokers.yml [选项]

# 方式 2：包入口（Python 标准）
python -m smarthome_sim --config sensors/brokers.yml [选项]
```

## Docker Compose

`sensors/docker-compose.yml` 提供两种模式：

```bash
# 默认：开启 Home Assistant MQTT Discovery
cd sensors
docker compose up -d --build

# Bench/压力测试：关闭 Discovery
docker compose --profile bench up -d --build simulator_bench
```

## 配置说明

将 `sensors/brokers.example.yml` 复制为 `sensors/brokers.yml`：

```yaml
brokers:
  - host: mqtt.example.com
    port: 8883
    tls: true
    ca_file: "../certs/ca/ca.pem"      # 相对于配置文件
    cert_file: "../certs/client/client.pem"
    key_file: "../certs/client/client.key"
    # 或使用内联 PEM（优先级更高）：
    # ca_pem: |
    #   -----BEGIN CERTIFICATE-----
    #   ...
    #   -----END CERTIFICATE-----

simulation:
  devices: 10
  base_topic: "smarthome/sim"
  ha_discovery: false                   # 建议用 --ha-discovery 参数
  qos: 0
  
  entities:
    - id: temperature
      kind: sensor
      device_class: temperature
      unit: "°C"
      model: drift                      # drift | uniform | sine
      min: 18.0
      max: 28.0
      interval: 5.0
    
    - id: motion
      kind: binary_sensor
      device_class: motion
      model: motion
      interval: 1.0
    
    - id: light
      kind: light
      commandable: true
      initial: { state: "OFF", brightness: 255 }
```

## CLI 选项

### 核心选项

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `-c, --config PATH` | 配置文件（YAML/JSON） | `sensors/brokers.yml` |
| `--devices N` | 模拟设备数量 | 10 |
| `--base-topic TOPIC` | MQTT 基础主题 | `smarthome/sim` |
| `--qos 0\|1\|2` | MQTT QoS 级别 | 0 |
| `--retain` | 对状态主题启用 retained | 关闭 |
| `--ha-discovery` | 启用 Home Assistant MQTT Discovery | 关闭 |
| `--discovery-prefix` | HA discovery 前缀 | `homeassistant` |

### 运行模式

| 参数 | 描述 |
|------|------|
| `--dry-run` | 演练模式（仅日志，不发布） |
| `--once` | 运行一次发布循环后退出 |
| `--workers N` | 工作进程数（默认：1） |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR |

### 握手基准测试（论文功能）

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--handshake-samples N` | 连接采样次数 | 0（禁用） |
| `--handshake-interval SEC` | 采样间隔 | 0.1 |
| `--handshake-timeout SEC` | 连接超时 | 10.0 |
| `--handshake-out PATH` | 输出目录 | `sensors/handshake_metrics` |
| `--handshake-plot` | 生成直方图/ECDF 图 | 关闭 |
| `--handshake-only` | 仅运行基准测试，跳过模拟 | 关闭 |

## TLS/mTLS 证书

两种提供 TLS 材料的方式：

### 1. 文件路径（相对于配置文件）

```yaml
brokers:
  - host: mqtt.example.com
    tls: true
    ca_file: "../certs/ca/ca.pem"
    cert_file: "../certs/client/client.pem"
    key_file: "../certs/client/client.key"
```

### 2. 内联 PEM（优先级更高）

```yaml
brokers:
  - host: mqtt.example.com
    tls: true
    ca_pem: |
      -----BEGIN CERTIFICATE-----
      MIIBkTCB+wIJAK...
      -----END CERTIFICATE-----
```

## 实体与联动

### 实体类型

| Kind | 描述 | 可控 |
|------|------|------|
| `sensor` | 数值传感器（温度、湿度） | 否 |
| `binary_sensor` | ON/OFF 状态（运动、门窗） | 否 |
| `switch` | 可控开关 | 是（ON/OFF 命令） |
| `light` | RGB 灯光 | 是（JSON 命令） |

### 模拟模型

| Model | 描述 | 适用 |
|-------|------|------|
| `drift` | 在 [min, max] 内随机漂移 | sensor |
| `uniform` | 在 [min, max] 内均匀随机 | sensor |
| `sine` | 正弦波 + 噪声 | sensor |
| `motion` | 随机 ON/OFF 触发 | binary_sensor |

### 联动配置

```yaml
simulation:
  automation:
    # 运动触发灯光亮 30 秒
    motion_entity: motion
    light_entity: light
    motion_hold_seconds: 30
    
    # 加热器影响温度（开启 +1.5°/分钟，关闭 -0.3°/分钟）
    switch_entity: heater
    sensor_entity: temperature
    delta_per_minute_on: 1.5
    delta_per_minute_off: -0.3
```

## 握手基准测试

用于论文级 TLS 握手延迟测量：

```bash
# 单进程，200 次采样
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --handshake-samples 200 \
  --handshake-out sensors/handshake_metrics \
  --handshake-only

# 多进程（每个 worker 各跑 N 次采样）
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --workers 4 \
  --handshake-samples 200 \
  --handshake-only

# 生成图表（需要 matplotlib）
pip install matplotlib
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --handshake-samples 200 \
  --handshake-plot \
  --handshake-only
```

**输出文件：**
- `handshake.w0.jsonl` - 原始记录（每次连接一条 JSON）
- `handshake.w0.summary.json` - 统计结果（p50/p90/p95/p99、均值、标准差、置信区间）
- `handshake.w0.hist.png` - 直方图（启用 `--handshake-plot`）
- `handshake.w0.ecdf.png` - ECDF 图（启用 `--handshake-plot`）

## Home Assistant 设备元数据

通过 `simulation.device` 配置 HA 中显示的设备信息：

```yaml
simulation:
  device:
    identifiers: ["sim_device_{device_id}"]
    name: "Sim Device {device_id}"
    model: "SmartHome Simulator"
    manufacturer: "Eurun Lab"
```

## 排错指南

| 问题 | 解决方案 |
|------|----------|
| 导入错误 | 激活虚拟环境：`. .venv/bin/activate` |
| EMQX 鉴权失败 | 检查 `brokers.yml` 中的 `username`/`password` |
| TLS 连接失败 | 确认 `tls: true`、端口（通常 8883）、证书路径 |
| HA 中看不到实体 | 添加 `--ha-discovery` 参数 |
| CPU 占用过高 | 减少 `--devices` 或增大实体 `interval` |

调试模式：
```bash
python sensors/sensor_simulator.py --config sensors/brokers.yml --log-level DEBUG
```

---

**环境要求：** Python 3.8+ | paho-mqtt>=1.6,<2.0 | PyYAML>=6.0 | matplotlib（可选）

## 许可证

MIT 许可证 - 详见 [LICENSE](../LICENSE)

## 引用

本模拟器是捷克理工大学学士论文《基于边缘计算的智能家居》的组成部分。引用信息请参阅 [主 README](../README.zh-CN.md)。

