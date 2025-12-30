# 📚 Bachelor Thesis Planning Hub

> **论文题目**: Application of Servers and Unix-like Systems for Sensor Control in Smart Homes  
> **作者**: Weize Yuan  
> **学校**: Czech Technical University in Prague, Faculty of Electrical Engineering  
> **系所**: Department of Microelectronics  
> **导师**: prof. Ing. Miroslav Husák, CSc.  
> **截止日期**: 4 天  

---

## 🗂️ 本目录文件索引

| 文件 | 内容 | 优先级 |
|------|------|--------|
| [00_MASTER_PLAN.md](00_MASTER_PLAN.md) | **总体规划与章节大纲**（先看这个） | ⭐⭐⭐ |
| [01_ESP32_SENSOR_DESIGN.md](01_ESP32_SENSOR_DESIGN.md) | ESP32/S3 硬件角色设计 + 传感器组合方案 | ⭐⭐⭐ |
| [02_NETWORK_ARCHITECTURE.md](02_NETWORK_ARCHITECTURE.md) | 网络架构详解（EMQX/HA/Tailscale 等） | ⭐⭐⭐ |
| [03_SECURITY_ANALYSIS.md](03_SECURITY_ANALYSIS.md) | mTLS/ECC/安全对比分析 | ⭐⭐ |
| [04_COMMERCIAL_COMPARISON.md](04_COMMERCIAL_COMPARISON.md) | 商用平台对比（小米/Alexa）+ 引用关键词 | ⭐⭐ |
| [05_TOOLS_INTEGRATION.md](05_TOOLS_INTEGRATION.md) | Grafana/InfluxDB/Node-RED 使用指南 | ⭐ |
| [06_WRITING_CHECKLIST.md](06_WRITING_CHECKLIST.md) | 4 天写作 Checklist + 每日任务 | ⭐⭐⭐ |

---

## 🎯 核心亮点（答辩加分项）

1. **真实硬件 + 软件模拟器双线并行**
   - ESP32/ESP32-S3 真实传感器节点（教授最爱）
   - Python 模拟器可扩展到 12000+ 设备压力测试

2. **分布式跨国部署**
   - EMQX @ 德国 Nuremberg
   - Home Assistant @ 布拉格 ESXi
   - 模拟器 @ 全球任意 VPS

3. **安全架构**
   - mTLS + ECC（非 RSA）
   - Tailscale 零信任组网

4. **边缘计算**
   - ESP32-S3 AI 指令集 + 本地振动/声音分析

5. **开源 vs 商用对比**
   - 数据主权、生态开放性、长期维护

---

## 🚀 Quick Start（4 天冲刺）

```
Day 1: 骨架 + 架构图 + 硬件设计
Day 2: 实现章节 + 实验数据
Day 3: 对比分析 + 结论
Day 4: 摘要 + 润色 + 提交
```

详见 [06_WRITING_CHECKLIST.md](06_WRITING_CHECKLIST.md)

---

## 📎 相关资源

- **LaTeX 模板**: `../CTU_FEL_THESIS/`（主入口：`thesis-final.tex`）
- **Overleaf / 写作工作流（中文）**: `./README.zh-CN.md`
- **ESPHome 配置**: `../../../esphome/`
- **模拟器代码**: `../../../sensors/smarthome_sim/`

---

## ✅ 编译与提交（最短路径）

- 你只需要编译 `../CTU_FEL_THESIS/thesis-final.tex`。
- 版式切换（草稿/最终双面装订）在 `thesis-final.tex` 第一行：
   - 默认：`\documentclass{phdthesis}`（oneside，阅读友好）
   - 最终打印：`\documentclass[print]{phdthesis}`（twoside，装订边）

更完整的构建/清理说明见：`docs/README` 和 `../CTU_FEL_THESIS/README.md`。

---

## 📊 预计论文结构

| 章节 | 预计页数 | 状态 |
|------|----------|------|
| Abstract | 1 | ⬜ |
| Introduction | 2 | ⬜ |
| Theoretical Background | 5-6 | ⬜ |
| System Architecture | 4 | ⬜ |
| Implementation | 8-10 | ⬜ |
| Evaluation | 5-6 | ⬜ |
| Commercial Comparison | 3 | ⬜ |
| Conclusion | 1-2 | ⬜ |
| **Total** | **30-35** | - |
