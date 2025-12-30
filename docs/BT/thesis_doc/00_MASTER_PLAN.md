# 00 - Master Plan: 论文总体规划

## 📋 论文基本信息

| 项目 | 内容 |
|------|------|
| **题目** | Application of Servers and Unix-like Systems for Sensor Control in Smart Homes |
| **类型** | Bachelor Thesis (本科毕业论文) |
| **学校** | Czech Technical University in Prague |
| **学院** | Faculty of Electrical Engineering |
| **系所** | Department of Microelectronics |
| **作者** | Weize Yuan |
| **导师** | prof. Ing. Miroslav Husák, CSc. |
| **语言** | English |
| **预计页数** | 35-45 页（正文） |

---

## 🎯 研究目标（Three Objectives）

### 1. 分析目标 (Analytical)
> Analyze the role of servers and Unix-like systems in smart home sensor monitoring and control.

### 2. 设计目标 (Design)
> Design and implement a model smart home system using MQTT protocol and Home Assistant platform.

### 3. 评估目标 (Evaluation)
> Compare the implemented solution with commercial alternatives in terms of scalability, latency, privacy, and reliability.

---

## 📑 章节结构（Final Structure）

```
1. Introduction                                    [2 pages]
   1.1 Background and Motivation
   1.2 Problem Statement
   1.3 Research Objectives
   1.4 Thesis Organization

2. Theoretical Background                          [5-6 pages]
   2.1 Smart Home Systems Overview
   2.2 MQTT Protocol
       2.2.1 Publish/Subscribe Model
       2.2.2 Quality of Service Levels
       2.2.3 Topic Hierarchy
   2.3 Transport Layer Security
       2.3.1 TLS and mTLS
       2.3.2 ECC vs RSA Cryptography
   2.4 Home Assistant Platform
   2.5 ESPHome Framework
   2.6 Edge Computing in IoT

3. System Architecture                             [4 pages]
   3.1 Architecture Overview
   3.2 Network Topology
       3.2.1 Geographic Distribution
       3.2.2 Tailscale VPN Integration
   3.3 Communication Protocols
   3.4 Security Architecture

4. Implementation                                  [8-10 pages]
   4.1 Hardware Implementation
       4.1.1 ESP32-S3 Edge Intelligence Node
       4.1.2 ESP32 Environment Sensing Node
       4.1.3 Sensor Integration Details
   4.2 Software Implementation
       4.2.1 ESPHome Configuration
       4.2.2 Python Sensor Simulator
       4.2.3 EMQX Broker Deployment
   4.3 Home Assistant Integration
       4.3.1 MQTT Discovery
       4.3.2 Dashboard Configuration
   4.4 Data Pipeline
       4.4.1 InfluxDB Storage
       4.4.2 Grafana Visualization
   4.5 Automation Examples
       4.5.1 Home Assistant Automations
       4.5.2 Node-RED Flows

5. Evaluation and Results                          [5-6 pages]
   5.1 Test Environment
   5.2 Performance Metrics
       5.2.1 MQTT Message Latency
       5.2.2 TLS Handshake Comparison
       5.2.3 Scalability Testing
   5.3 Security Analysis
   5.4 Reliability Assessment

6. Comparison with Commercial Solutions            [3 pages]
   6.1 Xiaomi Mi Home
   6.2 Amazon Alexa and Google Home
   6.3 Comparative Analysis
   6.4 Discussion

7. Conclusion                                      [1-2 pages]
   7.1 Summary of Contributions
   7.2 Limitations
   7.3 Future Work

References                                         [2 pages]

Appendix A: ESPHome Configuration Files
Appendix B: Python Simulator Code Excerpts
Appendix C: Certificate Generation
```

---

## 🔑 关键技术栈

| 层次 | 技术 | 用途 |
|------|------|------|
| **硬件层** | ESP32, ESP32-S3 | 真实传感器节点 |
| **传感器** | BMP180, MPU6050, TCS34725, MQ-2, SR602, KY-037 | 环境感知 |
| **通信层** | MQTT (EMQX), Native API | 消息传输 |
| **安全层** | mTLS, ECC, Tailscale | 加密与组网 |
| **控制层** | Home Assistant, Node-RED | 自动化与控制 |
| **存储层** | InfluxDB | 时序数据 |
| **可视化** | Grafana, HA Dashboard | 数据展示 |
| **模拟层** | Python smarthome_sim | 压力测试 |

---

## 📊 预期成果

1. **完整的智能家居系统实现**
   - 2个真实硬件节点
   - 软件模拟器支持 12000+ 设备

2. **性能基准数据**
   - MQTT 延迟测试
   - TLS 握手时间对比（ECC vs RSA）
   - 可扩展性测试结果

3. **安全分析报告**
   - mTLS 实现细节
   - 零信任网络架构

4. **商业对比分析**
   - 开源 vs 闭源生态系统对比

---

## ⚠️ 注意事项

1. **引用要求**: 本科论文通常需要 15-30 个引用
2. **图表要求**: 每章至少 1-2 个图或表
3. **代码展示**: 正文只放关键片段，完整代码放附录
4. **摘要**: 最后写，250 词左右
