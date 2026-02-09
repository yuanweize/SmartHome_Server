# 文档中心

语言：**简体中文** | [English](README.md)

本目录包含论文文档、LaTeX 源码及相关材料。

## 📄 论文

| 资源 | 链接 |
|------|------|
| 📥 **下载最新论文** | [![Latest Release](https://img.shields.io/github/v/release/yuanweize/SmartHome_Server?label=论文&logo=adobeacrobatreader)](https://github.com/yuanweize/SmartHome_Server/releases/latest) |
| 📋 导师评审报告 | [supervisor_report.pdf](BT/Review/supervisor_report.pdf) |
| 📋 对手评审报告 | [opponent_report_Koller.pdf](BT/Review/opponent_report_Koller.pdf) |

## 目录结构

```
docs/
├── BT/                      # 学士论文（主目录）
│   ├── CTU_FEL_THESIS/      # LaTeX 论文模板与源码
│   │   ├── thesis-final.tex # 入口文件
│   │   ├── chapters/        # 章节源码
│   │   └── images/          # 图表
│   ├── Review/              # 论文评审报告
│   │   ├── supervisor_report.pdf
│   │   └── opponent_report_Koller.pdf
│   ├── FIG/                 # 附加图表资源
│   └── 论文/                 # 草稿与资源文件（旧目录名）
├── pdf2md/                  # PDF 转 Markdown 工具
├── thesis_doc/              # 规划笔记、草稿与标准文档
└── README.md                # 本文件
```

## 论文编译

模板使用 **LuaLaTeX** + **biblatex/biber**。

### 快速编译

```bash
cd docs/BT/CTU_FEL_THESIS
make          # 自动版本号递增 + 编译
make pdf      # 仅编译（不递增版本号）
```

输出：`bachelor_thesis_Yuan_vX.X.pdf`（自动版本号）

### 手动编译

```bash
cd docs/BT/CTU_FEL_THESIS
lualatex -jobname=thesis thesis-final.tex
biber thesis
lualatex -jobname=thesis thesis-final.tex
lualatex -jobname=thesis thesis-final.tex
```

### VS Code 任务

使用预配置任务：`thesis: make pdf`

### 草稿 vs 印刷模式

默认：**单面** 模式（无装订边距交替，适合屏幕阅读）。

双面印刷（带装订边距）：

```tex
% 修改 thesis-final.tex 第一行
\documentclass[print]{bachelorthesis}
```

## 清理构建产物

```bash
cd docs/BT/CTU_FEL_THESIS
make clean      # 保留 PDF
make distclean  # 删除 PDF
```

或使用 latexmk：

```bash
latexmk -c   # 保留 PDF
latexmk -C   # 删除 PDF
```

## 关键文件

| 文件 | 描述 |
|------|------|
| `thesis-final.tex` | 主文档入口 |
| `bachelorthesis.cls` | CTU FEL 论文类（标题页、版式） |
| `literature.bib` | 参考文献数据库 |
| `chapters/*.tex` | 各章节源文件 |

## 相关文档

- [CTU FEL 论文模板 (Overleaf)](https://www.overleaf.com/latex/templates/sablona-pro-psani-disertacni-prace-na-cvut-fel/ptpvbxhsjdmg)
- [LaTeX 教程](https://en.wikibooks.org/wiki/LaTeX)
