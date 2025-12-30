# 05 - Tools Integration: 工具集成指南

## 📊 Grafana + InfluxDB 数据可视化

### 架构

```
ESP32/Simulator
      │
      │ MQTT
      ▼
Home Assistant
      │
      │ InfluxDB Integration
      ▼
InfluxDB (时序数据库)
      │
      │ Data Source
      ▼
Grafana (可视化面板)
```

### InfluxDB 配置（HA integration）

```yaml
# configuration.yaml
influxdb:
  host: localhost
  port: 8086
  database: homeassistant
  default_measurement: state
  include:
    domains:
      - sensor
      - binary_sensor
    entity_globs:
      - sensor.esp32_*
      - sensor.simulator_*
```

### Grafana 查询示例

```sql
-- 温度时序曲线
SELECT mean("value")
FROM "sensor"
WHERE ("entity_id" = 'esp32_temperature')
AND time >= now() - 24h
GROUP BY time(5m) fill(null)
```

### 论文可用的面板类型

1. **Time Series**: 温度/湿度变化曲线
2. **Gauge**: 当前传感器值
3. **Stat**: 设备在线数量
4. **Bar Chart**: 消息吞吐量对比

### 论文截图建议

- 24 小时温度曲线
- MQTT 消息率面板
- 多传感器对比视图

**论文叙述**:
> "Sensor data persistence is handled by InfluxDB, a time-series database optimized for IoT workloads. Grafana dashboards provide real-time visualization and historical analysis capabilities, enabling anomaly detection and trend monitoring across all connected sensors."

---

## 🔴 Node-RED 自动化流程

### 什么是 Node-RED？

> Node-RED 是一个基于流的可视化编程工具，特别适合 IoT 和事件驱动的自动化。

### 基本界面

```
┌────────────────────────────────────────────────────────┐
│  Node-RED Flow Editor                                  │
├────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────┐            │
│  │  MQTT   │───►│Function │───►│  HA     │            │
│  │   In    │    │  Node   │    │ Service │            │
│  └─────────┘    └─────────┘    └─────────┘            │
│                                                        │
│  Palette (左侧)    Flow (中间)    Debug (右侧)         │
└────────────────────────────────────────────────────────┘
```

### 示例流程：烟雾告警

```json
[
  {
    "id": "mqtt_smoke",
    "type": "mqtt in",
    "topic": "smarthome/+/smoke/state",
    "broker": "emqx"
  },
  {
    "id": "check_threshold",
    "type": "function",
    "func": "if (msg.payload > 2.5) { return msg; }",
    "wires": [["notify"]]
  },
  {
    "id": "notify",
    "type": "ha-call-service",
    "service": "notify.mobile_app",
    "data": "{\"message\": \"Smoke detected!\"}"
  }
]
```

### 流程图（ASCII）

```
[MQTT In: smoke/state]
        │
        ▼
[Function: payload > 2.5?]
        │
        ├─ Yes ─► [HA Call Service: notify]
        │
        └─ No ─► (end)
```

### 论文价值

虽然你还没深度使用 Node-RED，但可以在论文中展示：
1. 它作为 HA 自动化的补充
2. 复杂条件逻辑的可视化实现
3. 跨系统集成能力（MQTT → HA → 通知）

**论文叙述**:
> "Node-RED complements Home Assistant's native automation engine by providing a visual flow-based programming interface. Complex automation scenarios involving multiple conditions, data transformations, and cross-platform integrations can be implemented without writing traditional code."

---

## 📱 Home Assistant 自动化

### YAML 自动化示例

```yaml
# automations.yaml
automation:
  - alias: "Smoke Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.esp32_smoke
        above: 2.5
    action:
      - service: notify.mobile_app_iphone
        data:
          title: "⚠️ Smoke Detected"
          message: "Smoke level: {{ states('sensor.esp32_smoke') }}V"
      - service: light.turn_on
        target:
          entity_id: light.warning_light
        data:
          color_name: red
          brightness: 255
```

### UI 自动化

HA 也支持图形化创建自动化，适合简单场景。

### 论文叙述

> "Home Assistant's automation engine supports both declarative YAML configuration and a graphical editor. Automations can trigger based on state changes, time schedules, or external events, executing sequences of actions including device control, notifications, and service calls."

---

## 🔧 ESPHome OTA 更新

### 工作流程

```
Developer PC                    ESP32 Device
     │                              │
     │ esphome run config.yaml      │
     │ ─────────────────────────────►
     │                              │
     │         mDNS Discovery       │
     │ ◄─────────────────────────── │
     │                              │
     │      Upload New Firmware     │
     │ ═════════════════════════════►
     │         (Over WiFi)          │
     │                              │
     │       Reboot & Reconnect     │
     │ ◄═════════════════════════════
     │                              │
```

### 配置

```yaml
ota:
  password: !secret ota_password
  safe_mode: true
  # 如果更新失败，设备会进入安全模式
```

### 论文价值

> "ESPHome's Over-The-Air (OTA) update capability enables remote firmware deployment without physical access to devices. This feature is critical for maintaining distributed IoT installations, allowing security patches and feature updates to be deployed across the network from a central location."

---

## 📈 性能监控

### HA 内置监控

```yaml
# configuration.yaml
sensor:
  - platform: systemmonitor
    resources:
      - type: processor_use
      - type: memory_use_percent
      - type: disk_use_percent
```

### EMQX Dashboard

EMQX 提供内置管理界面：
- 连接数统计
- 消息吞吐量
- 订阅主题列表
- 客户端在线状态

**截图建议**: EMQX Dashboard 显示连接数和消息率

---

## 📝 论文中如何描述这些工具

### Implementation 章节

> **4.4 Data Pipeline**
>
> **4.4.1 InfluxDB Storage**
>
> InfluxDB serves as the time-series database for persisting sensor measurements. Home Assistant's native InfluxDB integration automatically writes entity state changes to the database, enabling long-term data retention and analysis. The database schema organizes data by measurement type and entity identifier, supporting efficient queries for historical trends.
>
> **4.4.2 Grafana Visualization**
>
> Grafana provides a flexible dashboard framework for visualizing time-series data. Custom dashboards were created to monitor system health, including sensor readings, MQTT message rates, and device connectivity status. Figure 4.X shows the main monitoring dashboard displaying temperature trends across all sensor nodes.

### Automation 章节

> **4.5 Automation Examples**
>
> **4.5.1 Home Assistant Automations**
>
> Native Home Assistant automations handle time-critical responses such as safety alerts. When the MQ-2 smoke sensor exceeds the configured threshold of 2.5V, an automation triggers immediate notification to the user's mobile device and activates visual warning indicators.
>
> **4.5.2 Node-RED Flows**
>
> Node-RED extends automation capabilities through visual flow programming. Complex scenarios involving data transformation, conditional branching, and cross-platform integration are implemented as interconnected nodes, providing flexibility beyond Home Assistant's declarative automation syntax.

---

## 📊 工具对比表（可放论文）

| 工具 | 用途 | 优势 | 限制 |
|------|------|------|------|
| **Home Assistant** | 控制中心 | 集成丰富、社区活跃 | 学习曲线 |
| **InfluxDB** | 时序存储 | 高写入性能 | 需要空间 |
| **Grafana** | 可视化 | 灵活美观 | 配置复杂 |
| **Node-RED** | 流程编排 | 可视化编程 | 调试困难 |
| **ESPHome** | 固件开发 | YAML 配置 | 仅限 ESP |
| **EMQX** | 消息代理 | 高性能、集群 | 资源占用 |
