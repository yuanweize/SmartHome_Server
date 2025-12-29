# 传感器模拟器（Sensor Simulator）

语言：**简体中文** | [English](README.md)

这是一个面向 Home Assistant（HA）论文/演示环境的多 Broker MQTT 智能家居模拟器：

- 支持多个 MQTT Broker 同时发布
- 支持 Home Assistant MQTT Discovery（自动在 HA 中出现实体）
- 支持可控实体（switch/light）通过 MQTT command topic 控制
- 支持 TLS/mTLS（证书可用“文件路径”或“内联 PEM 文本”提供）
- 支持多进程 `--workers` 充分利用多核 CPU
- 支持“真实连接过程”的握手统计导出（JSONL + 统计汇总 JSON，可选生成统计图）

## 目录

- [相关文件](#相关文件)
- [环境要求](#环境要求)
- [配置说明](#配置说明)
- [快速开始](#快速开始)
- [TLS/mTLS 证书](#tlsmtls-证书)
- [实体与联动](#实体与联动)
- [命令行覆盖](#命令行覆盖)
- [HA 设备信息模板](#ha-设备信息模板)
- [握手统计（真实数据导出）](#握手统计真实数据导出)
- [排错建议](#排错建议)

## 相关文件

- `sensors/sensor_simulator.py`：主程序
- `sensors/brokers.example.yml`：配置示例（复制为 `sensors/brokers.yml` 使用）
- `sensors/docker-compose.yml`：Docker 运行入口（挂载配置/证书）
- `sensors/Dockerfile`：容器镜像
- `certs/README`：证书目录说明

## 环境要求

- macOS / Linux
- Python 3.8+（建议使用 venv）

安装依赖：

```bash
cd SmartHome_Server
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 配置说明

将 `sensors/brokers.example.yml` 复制为 `sensors/brokers.yml` 并修改。

该配置文件同时包含：

- `brokers`：MQTT Broker 列表（可启用 TLS/mTLS）
- `simulation`：模拟设备/实体/联动（以及 HA Discovery 行为）

注意：

- 支持 YAML / JSON。
- 不要把真实凭据提交到仓库；`sensors/brokers.yml` 默认应为 git-ignored。

## 快速开始

仅演练（不连接网络，只打印日志）：

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml --dry-run --log-level DEBUG
```

真实发布：

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml
```

多核压测（推荐 Linux 服务器）：

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.yml --workers 6 --log-level INFO
```

使用 CLI 覆盖部分配置（优先级：CLI > brokers.yml > 默认值）：

```bash
python sensors/sensor_simulator.py --config sensors/brokers.yml --devices 200 --qos 1 --log-level INFO
```

## TLS/mTLS 证书

模拟器支持两种提供证书材料的方式：

1) 在 `sensors/brokers.yml` 里提供“文件路径”（`ca_file`, `cert_file`, `key_file`）

- 路径会以配置文件所在目录为基准进行相对解析。
- Docker 下常见坑：如果证书在仓库根目录 `certs/`，而配置文件在 `sensors/`，那么 `./certs/...` 实际会解析为 `sensors/certs/...`。
  - 解决：用 `../certs/...`，或者把证书复制到 `sensors/certs/...`。

2) 在 `sensors/brokers.yml` 里直接写“内联 PEM 文本”（`ca_pem`, `cert_pem`, `key_pem`）

- 内联 PEM 优先级更高。
- 如果内联 TLS 配置失败且同时提供了文件路径，会自动回退到文件路径。

## 实体与联动

实体定义在 `simulation.entities` 中。

关键字段：

- `id`：实体基础 id（必填）。当 `count > 1` 时会展开为 `id_1`, `id_2`...
- `count`：每个 device 下该实体实例数量（可选，默认 1）
- `name`：支持 `{device_id}` 与 `{index}`（实例序号）

`kind` 支持：

- `sensor`：数值传感器
- `binary_sensor`：`ON/OFF`
- `switch`：可控（通过 `.../set` 下发命令）
- `light`：可控（通常是 JSON state）

联动在 `simulation.automation` 配置：

- `motion_entity` + `light_entity`：运动触发灯亮一段时间
- `switch_entity` + `sensor_entity`：开关改变传感器趋势（例如 heater 影响温度）

## 命令行覆盖

常用参数：

- `--config PATH`
- `--devices N`
- `--workers N`
- `--qos 0|1|2`
- `--retain`
- `--log-level DEBUG|INFO|WARNING|ERROR`

## HA 设备信息模板

MQTT Discovery 的 `device` 字段由 `simulation.device` 控制：

- `identifiers`（字符串数组）
- `name`
- `model`
- `manufacturer`

这些字段支持 `{device_id}`。

## 握手统计（真实数据导出）

为了满足论文/实验的“可复现 + 可追溯 + 严谨”，模拟器提供一个“真实 connect/disconnect 循环”，记录每次真实连接的端到端耗时（包含 TCP + TLS 握手 + MQTT CONNACK 等待）。

单进程：

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py \
  --config sensors/brokers.yml \
  --handshake-samples 200 \
  --handshake-interval 0.2 \
  --handshake-timeout 10 \
  --handshake-out sensors/handshake_metrics \
  --handshake-only
```

输出（本地文件，方便后续处理）：

- `sensors/handshake_metrics/handshake.w0.jsonl`：每次真实连接尝试一条 JSON 记录（成功/失败都会记录）
- `sensors/handshake_metrics/handshake.w0.summary.json`：从 JSONL 严格计算得到的统计结果（p50/p90/p95/p99、均值/标准差等，并注明所用方法）

可选绘图（需要 matplotlib）：

```bash
pip install matplotlib
python sensors/sensor_simulator.py --config sensors/brokers.yml --handshake-samples 200 --handshake-plot --handshake-only
```

多进程：

```bash
python sensors/sensor_simulator.py --config sensors/brokers.yml --workers 4 --handshake-samples 200 --handshake-only
```

说明：多进程模式下是“每个 worker 各跑 N 次 sample”。如果你要总样本数固定，请自行按 `workers` 分摊 N。

## 排错建议

- 依赖导入失败：确认已激活 venv 并安装 `requirements.txt`。
- EMQX 鉴权失败：检查 `brokers.yml` 中 `username/password`。
- TLS 无法连接：确认 broker 端口、`tls: true`、证书路径/内容是否正确。
- 建议 `--log-level DEBUG` 获取更细日志。

---

欢迎补充实验报告与对比数据。若你准备发布论文结果，建议一并公开：

- 使用的命令行
- 关键配置（脱敏后的 `sensors/brokers.yml`）
- 原始 JSONL 与 summary JSON（作为可追溯的“计算输入/输出”）
