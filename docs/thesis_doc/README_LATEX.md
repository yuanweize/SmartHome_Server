# CTU/FEL 本科论文 LaTeX 模板（Overleaf + 本地编译指南，中文为主）

面向：你需要**尽快写完论文并稳定出 PDF**。

这份文档聚焦三件事：
1) Overleaf 从 0 到能编译
2) 本项目“正确入口”和文件结构（以当前模板为准）
3) 最常用功能：图/表/参考文献/缩略语 + 最终打印版式

---

## 0. Overleaf 是什么？为什么学术论文都爱用？

**Overleaf = 在线 LaTeX 编辑与编译平台**。

你可以把它理解成：
- 一个“网页版 VS Code + LaTeX 编译器”，
- 不用在自己电脑装 TeX Live/MacTeX 也能编译出 PDF（当然你本地也可以装）。

它为什么好用（对你这种“只有 4 天”的情况尤其友好）：
- **零环境折腾**：你只要上传项目，点 Recompile 就出 PDF。
- **编译错误更好定位**：日志会直接跳到行号。
- **版本历史**：改坏了可以回滚。
- **协作**：导师/同学可以直接在线批注或一起改。

Overleaf 通常用在：
- 学术论文（Bachelor/Master/PhD thesis）
- 会议论文/期刊（IEEE/ACM）
- 需要很多公式、图表、引用的技术文档

---

## 1. 你这个项目的“正确入口”是什么？

本模板目录：
- `docs/BT/CTU_FEL_THESIS/`

当前模板只有一个推荐入口：

### `thesis-final.tex`（主入口：写作 + 最终提交都用它）
- 使用模板类 `bachelorthesis.cls`（封面/版式/元信息）。
- 正文内容拆分在 `chapters/*.tex`，你主要写章节文件即可。

结论：
- **编译**：编译 `thesis-final.tex`
- **写作**：编辑 `chapters/*.tex`

---

## 2. Overleaf：从 0 到能编译出 PDF（按这个做就行）

### Step 1：创建项目
1) 打开 https://www.overleaf.com/ 注册/登录。
2) New Project → **Upload Project**。

### Step 2：上传你的模板
你可以用两种方式：

**方式 1（推荐）**：上传 zip
- 在本地把 `docs/BT/CTU_FEL_THESIS/` 整个文件夹打包成 zip。
- Overleaf Upload Project 选择这个 zip。

**方式 2**：上传多个文件
- Overleaf 里 New Project 后，逐个上传文件/文件夹（不推荐，容易漏）。

### Step 3：设置 Main file（非常关键）
Overleaf 左侧文件树里：

- 右键 `thesis-final.tex` → **Set as Main File**

> 你看到“怎么编译都不对、目录不更新、PDF 空白”等，80% 是 Main file 没设对。

### Step 4：设置编译器为 LuaLaTeX
Overleaf 菜单 → Settings：
- Compiler: **LuaLaTeX**

> 本模板是 LuaLaTeX 优先（UTF-8 更自然）。

### Step 5：点 Recompile
- 点 Recompile → 右侧出 PDF。
- 出错就看 Logs（Overleaf 会给行号）。

### Step 6（常见问题）：目录/缩略语/引用没更新怎么办？
- Overleaf 菜单里点 **Recompile from scratch**（从头编译）。
- 或者连点两次 Recompile（有些辅助文件需要第二轮）。

---

## 3. 本项目文件结构：每个文件是干什么的（你只需要记住这几个）

目录 `docs/BT/CTU_FEL_THESIS/`：

- `bachelorthesis.cls`
  - **模板类文件**（封面、声明页、超链接样式、bibliography 后端选择等）。
  - 一般情况下你不需要改它。

- `thesis-final.tex`
  - **主文件**：封面、目录、图表清单、正文、附录、参考文献。
  - 通过 `\input{chapters/...}` 引入各章节。

- `chapters/`
  - 论文正文都在这里（你主要编辑这里的文件）。
  - 常见文件：`abstract.tex`、`introduction.tex`、`methods_results.tex`、`appendix.tex` 等。

- `acronyms.tex`
  - 你论文里出现的缩略语在这里定义（例如 MQTT, TLS, HA 等）。

- `literature.bib`
  - 参考文献数据库（BibTeX 格式的 `.bib` 文件）。你只需要往里加条目。

- `latexmkrc`
  - 本地用 `latexmk` 编译时的配置文件。

- `images/`
  - 存放图片（建议你把论文插图都放这里）。
  - 模板封面会尝试找 `images/LogoCVUT.pdf`（没有也能编译）。

---

## 4. 论文最常用功能：图（Figure）怎么放？怎么引用？

### 4.1 图文件放哪里？用什么格式？
建议：
- 放在 `images/` 目录里，例如：
  - `images/arch.pdf`
  - `images/mqtt-flow.png`

格式建议：
- **矢量图**：优先 `PDF`（结构图、流程图、示意图）
- **截图/照片**：`PNG`（尽量别用 JPG，除非是照片）

命名建议（省心）：
- 全小写 + `-`：`system-architecture.pdf`

### 4.2 代码模板（直接复制用）
在你的章节文件里（例如 `chapters/introduction.tex`）写：

```tex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.95\textwidth]{images/system-architecture}
  \caption{Overall system architecture of the smart home simulator.}
  \label{fig:arch}
\end{figure}
```

引用这张图：
```tex
As shown in Figure~\ref{fig:arch}, ...
```

注意点：
- `\label{...}` 放在 `\caption{...}` 后面（最佳实践）。
- `images/system-architecture` **不写扩展名**通常也行（LaTeX 会找 pdf/png/jpg）。

---

## 5. 表格（Table）怎么写？（论文里最常用的两种）

本模板已启用了 `booktabs`，写表更好看。

### 5.1 普通表（最常用）
```tex
\begin{table}[htbp]
  \centering
  \caption{Benchmark settings.}
  \label{tab:settings}
  \begin{tabular}{ll}
    \toprule
    Item & Value \\
    \midrule
    Devices & 12000 \\
    QoS & 0 \\
    Workers & 6 \\
    \bottomrule
  \end{tabular}
\end{table}
```

引用：
```tex
See Table~\ref{tab:settings}.
```

### 5.2 表格太宽怎么办？（紧急省事版）
- 先把列内容写短一点（学术写作里更常见）。
- 或者先用 `\small`：

```tex
{\small
\begin{tabular}{...}
...
\end{tabular}
}
```

（更专业的 `tabularx`/`longtable` 也能做，但你只有 4 天，先用最稳的方式。）

---

## 6. 参考文献（BibLaTeX + Biber）：怎么加？怎么引用？

本模板使用：
- `biblatex`（样式 IEEE）
- 后端 `biber`

你主要要做两件事：

### 6.1 把文献条目加进 `literature.bib`
示例条目：
```bibtex
@misc{mqtt_spec,
  title        = {MQTT Version 5.0},
  year         = {2019},
  howpublished = {OASIS Standard},
  url          = {https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html}
}
```

### 6.2 在正文里引用
在正文里：
```tex
MQTT is widely used in IoT systems \cite{mqtt_spec}.
```

最后 `thesis-final.tex` 会 `\printbibliography` 输出参考文献。

常见坑：
- “引用显示 [??]”：通常是没有跑到 biber 或需要再编译一次。
- Overleaf：多点一次 Recompile 或 Recompile from scratch。

---

## 7. 缩略语（Acronyms / Glossaries）：MQTT、TLS、HA 这种怎么自动生成列表？

你在 `acronyms.tex` 里定义：

```tex
\newacronym{mqtt}{MQTT}{Message Queuing Telemetry Transport}
\newacronym{tls}{TLS}{Transport Layer Security}
\newacronym{ha}{HA}{Home Assistant}
```

在正文里第一次出现写：
```tex
\gls{mqtt}
```
- 第一次会展开成“Message Queuing Telemetry Transport (MQTT)”（取决于 glossaries 设置）
- 后面再用会只显示 “MQTT”

`thesis-final.tex` 里已经有：
（已配置为 **no-index glossaries**）会自动生成缩略语列表。

你不需要额外运行 `makeglossaries`；Overleaf/本地多编译一次即可。

## 8. 草稿 vs 最终打印版式（oneside / print）

默认是**阅读友好**的 oneside（左右页边距不交换）。

需要最终双面打印并留装订边时，把 `thesis-final.tex` 第一行改为：

```tex
\documentclass[print]{bachelorthesis}
```

---

## 9. 本地编译（不用 Overleaf 时）

在 `docs/BT/CTU_FEL_THESIS/` 下运行：

```bash
lualatex thesis-final.tex
biber thesis-final
lualatex thesis-final.tex
lualatex thesis-final.tex
```

如果你用 `latexmk`：

```bash
latexmk -lualatex thesis-final.tex
```

清理中间文件：

```bash
latexmk -c   # 保留 PDF
latexmk -C   # 连 PDF 一起删
```

## 10. 只有 4 天：推荐工作流（最重要）

### Day 1：把骨架搭好（不要追求完美排版）
- Main file 固定用：`thesis-final.tex`
- 先把 `chapters/` 里每章都写 5–10 行，保证结构完整

### Day 2：填核心内容（与你主题最相关）
你的题目是：
> Application of Servers and Unix-like Systems for Sensor Control in Smart Homes

优先写这些（高分项）：
- 系统架构图（Figure 1）
- MQTT 主题结构、数据流、mTLS/安全方案
- 实验设置：设备数量、QoS、并发、指标
- 结果表格：吞吐、延迟、CPU、连接建立时间等

### Day 3：补齐引用 + 图表说明 + 摘要
- 每个关键论断都要有 citation
- 图表 caption 要讲清楚“图在证明什么”

### Day 4：通读、修错误、统一术语
- 统一术语：device/entity/broker/worker
- 清理 TODO
- Overleaf 上 Recompile from scratch，确认目录/引用/缩略语都对

---

## 11. 你现在要我下一步帮你什么？

我可以继续帮你做两类“最快提分”的事情：
1) 按你论文主题，给你一个 **章节大纲 + 每章应该放的图/表/实验指标清单**（非常实用）。
2) 你把你要放的第一张架构图/一段实验结果贴出来，我帮你直接写成论文里可用的 Figure/Table + 英文段落。
