# 06 - Writing Checklist: 4 天写作计划

## 📅 总体时间表

```
┌─────────────────────────────────────────────────────────────────┐
│  Day 1 (今天)     │  Day 2          │  Day 3        │  Day 4   │
├───────────────────┼─────────────────┼───────────────┼──────────┤
│  骨架 + 架构图    │  Implementation │  Evaluation   │  润色    │
│  + Introduction   │  + Background   │  + Comparison │  + 提交  │
└───────────────────┴─────────────────┴───────────────┴──────────┘
```

---

## 📋 Day 1: 骨架与架构（今天）

### 上午任务

- [ ] **确认 LaTeX 编译成功**
  - Overleaf 上传项目
  - 设置 Main File = `thesis-final.tex`
  - 设置 Compiler = LuaLaTeX
  - 点击 Recompile，确认出 PDF

- [ ] **填写元数据**
  - 确认 title/author/supervisor 正确
  - 确认 department/faculty 正确

### 下午任务

- [ ] **绘制架构图**
  - Figure 3.1: System Architecture Overview
  - Figure 3.2: Network Topology
  - 工具推荐: Draw.io / Excalidraw / Mermaid

- [ ] **完成 Chapter 1: Introduction**
  - 1.1 Background (200 词)
  - 1.2 Problem Statement (150 词)
  - 1.3 Objectives (100 词)
  - 1.4 Thesis Organization (100 词)

### 晚上任务

- [ ] **完成 Chapter 3: System Architecture**
  - 3.1 Overview (300 词 + Figure)
  - 3.2 Network Topology (300 词 + Figure)
  - 3.3 Communication (200 词)
  - 3.4 Security Architecture (200 词)

### Day 1 检查点 ✓
- [ ] PDF 能正常编译
- [ ] Chapter 1 完成
- [ ] Chapter 3 完成
- [ ] 至少 2 张架构图

---

## 📋 Day 2: 实现细节

### 上午任务

- [ ] **Chapter 4.1: Hardware Implementation**
  - 4.1.1 ESP32-S3 Node (300 词 + Table)
  - 4.1.2 ESP32 Node (300 词 + Table)
  - 4.1.3 Sensor Integration (200 词)
  - 准备 1 张硬件照片或接线图

- [ ] **Chapter 4.2: Software Implementation**
  - 4.2.1 ESPHome (300 词 + Code snippet)
  - 4.2.2 Python Simulator (300 词 + Code snippet)
  - 4.2.3 EMQX (200 词)

### 下午任务

- [ ] **Chapter 4.3-4.5**
  - 4.3 HA Integration (300 词)
  - 4.4 Data Pipeline (300 词 + Grafana 截图)
  - 4.5 Automation (200 词)

- [ ] **Chapter 2: Theoretical Background**
  - 2.1 Smart Home Overview (200 词)
  - 2.2 MQTT Protocol (400 词 + Figure)
  - 2.3 TLS/mTLS (300 词)
  - 2.4-2.6 HA/ESPHome/Edge (各 150 词)

### 晚上任务

- [ ] **收集引用**
  - 至少找 15 个引用源
  - 填入 `literature.bib`
  - IEEE/ACM 论文优先

### Day 2 检查点 ✓
- [ ] Chapter 2 完成
- [ ] Chapter 4 完成
- [ ] 至少 15 个引用
- [ ] 代码片段正确显示

---

## 📋 Day 3: 评估与对比

### 上午任务

- [ ] **运行测试并截图**
  - 跑一次 simulator 压力测试
  - 截图 EMQX Dashboard
  - 截图 Grafana 面板

- [ ] **Chapter 5: Evaluation**
  - 5.1 Test Environment (200 词 + Table)
  - 5.2.1 MQTT Latency (200 词 + Graph)
  - 5.2.2 TLS Handshake (200 词 + Table)
  - 5.2.3 Scalability (200 词 + Graph)
  - 5.3 Security Analysis (200 词)
  - 5.4 Reliability (150 词)

### 下午任务

- [ ] **Chapter 6: Commercial Comparison**
  - 6.1 Xiaomi (200 词)
  - 6.2 Alexa/Google (300 词，引用为主)
  - 6.3 Comparison Table
  - 6.4 Discussion (300 词)

### 晚上任务

- [ ] **Chapter 7: Conclusion**
  - 7.1 Summary (200 词)
  - 7.2 Limitations (100 词)
  - 7.3 Future Work (150 词)

- [ ] **检查所有引用**
  - 确保每个 `\cite{}` 都有对应 bib 条目
  - 确保没有 [??] 显示

### Day 3 检查点 ✓
- [ ] Chapter 5 完成
- [ ] Chapter 6 完成
- [ ] Chapter 7 完成
- [ ] 所有引用正确

---

## 📋 Day 4: 润色与提交

### 上午任务

- [ ] **Abstract** (最后写!)
  - 250 词左右
  - 覆盖: 问题 → 方法 → 结果 → 结论

- [ ] **Acknowledgements**
  - 感谢导师
  - 感谢学校/实验室

- [ ] **检查缩略语**
  - 确保 `acronyms.tex` 包含所有用到的缩略语
  - MQTT, TLS, mTLS, HA, IoT, ECC, RSA, API, OTA, etc.

### 下午任务

- [ ] **全文检查**
  - 拼写检查 (Overleaf 内置)
  - 语法检查 (Grammarly / LanguageTool)
  - 图表编号连续性
  - 引用完整性

- [ ] **格式检查**
  - 目录正确
  - 图表清单正确
  - 页码正确
  - 缩略语表正确

### 晚上任务

- [ ] **最终编译**
  - Overleaf: Recompile from scratch
  - 下载 PDF
  - 检查所有页面

- [ ] **提交**
  - 按学校要求提交
  - 保存最终版本备份

### Day 4 检查点 ✓
- [ ] Abstract 完成
- [ ] 无拼写/语法错误
- [ ] 格式正确
- [ ] 已提交

---

## ⚡ 快速写作技巧

### 1. 先写骨架再填充
```
\section{Hardware Implementation}
% TODO: Describe ESP32-S3 setup
% Key points: sensors, edge computing, mTLS
```

### 2. 使用 TODO 标记
```latex
\todo{Add figure here}
\todo{Need citation for this claim}
```

### 3. 图表先占位
```latex
\begin{figure}[htbp]
  \centering
  % \includegraphics[width=0.8\textwidth]{images/architecture}
  \fbox{\parbox{0.8\textwidth}{\centering [Architecture Diagram Placeholder]}}
  \caption{System architecture overview.}
  \label{fig:arch}
\end{figure}
```

### 4. 引用先标记后补
```latex
MQTT is widely used in IoT systems~\cite{TODO_mqtt_paper}.
```

---

## 📊 字数/页数估算

| 章节 | 目标词数 | 预计页数 |
|------|----------|----------|
| Abstract | 250 | 1 |
| Ch1 Introduction | 600 | 2 |
| Ch2 Background | 1200 | 5 |
| Ch3 Architecture | 1000 | 4 |
| Ch4 Implementation | 2000 | 8 |
| Ch5 Evaluation | 1200 | 5 |
| Ch6 Comparison | 800 | 3 |
| Ch7 Conclusion | 450 | 2 |
| **Total** | **~7500** | **~30** |

加上封面、目录、图表清单、附录 → **预计 40-45 页**

---

## 🆘 遇到困难怎么办

### 编译错误
1. 看 Overleaf 日志找行号
2. 检查 `{` `}` 配对
3. 检查 `\begin` `\end` 配对

### 引用显示 [??]
1. 检查 `literature.bib` 中是否有该条目
2. Recompile from scratch
3. 检查 bib key 拼写

### 图片不显示
1. 确认图片在 `images/` 目录
2. 确认文件名无空格/特殊字符
3. 尝试带扩展名: `images/arch.pdf`

### 写不出来
1. 先写中文再翻译
2. 用 AI 辅助生成初稿
3. 参考本目录下的示例段落

---

## 🎯 最重要的三件事

1. **先完成再完美** - 有内容比没内容强
2. **图表 > 文字** - 好图抵千言
3. **保持编译成功** - 随时能出 PDF
