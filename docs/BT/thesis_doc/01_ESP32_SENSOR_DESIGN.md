# 01 - ESP32 Sensor Design: 硬件角色设计

## 🎯 设计理念

两个 ESP32 节点承担不同角色，展示 IoT 系统中的两种典型应用模式：

1. **ESP32-S3**: 边缘智能节点（Edge Intelligence）- 复杂计算
2. **ESP32**: 环境感知节点（Environment Sensing）- 传统采集

---

## 📱 Node A: ESP32-S3 — Edge Intelligence Node

### 角色定位
> 智能边缘网关：利用 S3 的 AI 向量指令集进行本地数据处理，减少云端依赖。

### 传感器配置

| 传感器 | 型号 | 功能 | 论文价值 |
|--------|------|------|----------|
| 气压温度 | BMP180 | 温度 + 大气压 | 环境监测基础 |
| 六轴运动 | MPU6050 (GY-521) | 加速度 + 陀螺仪 | **边缘计算示例** |
| 声音检测 | KY-037 | 声音强度 ADC | **声音事件检测** |

### 边缘计算功能

```yaml
# 已在 esphome/esp32s3.yaml 中实现
sensor:
  - platform: template
    name: "Resultant G-Force"
    # 计算合成加速度: sqrt(ax² + ay² + az²)
    
  - platform: template
    name: "Dynamic Vibration Component"
    # 动态振动分量: |G - 1.0|
    
binary_sensor:
  - platform: template
    name: "Acoustic Peak Event"
    # 声音峰值检测: ADC > 阈值
```

### 为什么用 S3？

| 特性 | ESP32-S3 | 普通 ESP32 |
|------|----------|------------|
| AI 指令集 | ✅ SIMD 向量指令 | ❌ |
| 适合计算 | FFT、滤波、模式识别 | 简单采集 |
| 内存 | 512KB SRAM | 320KB SRAM |
| USB | 原生 USB-OTG | 需外部芯片 |

**论文叙述**:
> "The ESP32-S3 features vector instructions optimized for neural network inference and signal processing, enabling edge computing capabilities such as vibration analysis and acoustic event detection without cloud dependency."

---

## 📱 Node B: ESP32 — Environment Sensing Node

### 角色定位
> 传统环境感知节点：采集多种环境数据，演示传感器集成和本地自动化。

### 传感器配置

| 传感器 | 型号 | 功能 | 论文价值 |
|--------|------|------|----------|
| 颜色光照 | TCS34725 | RGB + 环境光 | 智能照明场景 |
| 烟雾燃气 | MQ-2 | 可燃气体浓度 | **安全监控** |
| 人体感应 | SR602 | PIR 红外检测 | 占用检测 |
| 状态指示 | RGB LED | 视觉反馈 | 设备状态展示 |

### 本地自动化

```yaml
# 已在 esphome/esp32.yaml 中实现
automation:
  - trigger:
      platform: numeric_state
      above: 2.5  # 烟雾超过阈值
    action:
      - light.turn_on:
          id: status_led
          effect: "Fast Pulse"
          red: 100%
          green: 0%
          blue: 0%
```

### 安全场景设计

```
触发条件              →  响应动作
─────────────────────────────────────
MQ-2 > 2.5V          →  红色 LED 快闪 + MQTT 告警
SR602 检测到人       →  绿色 LED 亮起
SR602 无人 + 超时    →  LED 关闭
```

**论文叙述**:
> "The environment sensing node demonstrates local automation capabilities, where smoke detection triggers immediate visual alerts without requiring cloud connectivity, ensuring safety-critical responses."

---

## 🔄 两节点对比（论文表格素材）

| 对比项 | ESP32-S3 (Node A) | ESP32 (Node B) |
|--------|-------------------|----------------|
| **角色** | 边缘智能 | 环境感知 |
| **计算能力** | AI 指令集加速 | 标准处理 |
| **传感器数** | 3 | 4 |
| **计算复杂度** | 高（FFT、向量运算） | 低（ADC 读取） |
| **功耗** | 较高 | 较低 |
| **成本** | ~$8 | ~$5 |
| **适用场景** | 振动监测、声音分析 | 环境监测、安全告警 |

---

## 📡 连接方式

两个节点都采用 **双连接模式**：

### 1. Native API（局域网直连）
```yaml
api:
  encryption:
    key: "xxx"
```
- 用途：Home Assistant 直接控制、OTA 更新
- 优点：低延迟、双向通信

### 2. MQTT（跨网络通信）
```yaml
mqtt:
  broker: mqtt.example.com
  port: 8883
  certificate_authority: /path/to/ca.pem
  client_certificate: /path/to/client.pem
  client_key: /path/to/client.key
```
- 用途：远程监控、多订阅者、模拟器集成
- 优点：跨网络、可靠性高

**论文叙述**:
> "A dual-connection architecture is employed: Native API provides low-latency local control and OTA updates, while MQTT enables cross-network communication with mTLS encryption for remote monitoring and integration with the Python simulator."

---

## 🔧 传感器调换建议（如果需要）

### 方案 A（当前，推荐）
- S3: BMP180 + MPU6050 + KY-037（计算密集型）
- ESP32: TCS34725 + MQ-2 + SR602 + LED（采集型）

### 方案 B（声音换到 ESP32）
- S3: BMP180 + MPU6050（纯运动分析）
- ESP32: TCS34725 + MQ-2 + SR602 + KY-037 + LED

### 方案 C（颜色换到 S3）
- S3: BMP180 + MPU6050 + TCS34725（可做颜色 AI 识别）
- ESP32: MQ-2 + SR602 + KY-037 + LED

**建议保持方案 A**：功能划分清晰，答辩时容易解释。

---

## 📝 论文中如何描述

### Implementation 章节示例段落

> Two ESP32-based nodes were implemented to demonstrate different IoT paradigms. The ESP32-S3 node serves as an edge intelligence gateway, leveraging its vector instruction set for local signal processing. It integrates an MPU6050 accelerometer for vibration analysis and a KY-037 microphone for acoustic event detection. The standard ESP32 node functions as an environment sensing unit, collecting data from a TCS34725 color sensor, MQ-2 smoke detector, and SR602 PIR sensor, with local automation rules for safety alerts.

### 配图建议

1. **Figure: Hardware Setup** - 两个节点的实物照片
2. **Figure: Sensor Wiring Diagram** - 接线示意图
3. **Table: Sensor Specifications** - 传感器参数表
4. **Figure: Edge Computing Flow** - S3 边缘计算流程图
