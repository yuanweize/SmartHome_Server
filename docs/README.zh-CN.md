# 文档中心

语言：**简体中文** | [English](README.md)

本目录包含论文文档、LaTeX 源码及相关材料。

## 目录结构

```
docs/
├── BT/
│   ├── CTU_FEL_THESIS/      # LaTeX 论文模板（主目录）
│   │   ├── thesis-final.tex # 入口文件（编译此文件）
│   │   ├── chapters/        # 章节源文件
│   │   └── images/          # 图表
│   ├── thesis_doc/          # 规划笔记与草稿
│   └── FIG/                 # 附加图表
└── README.md                # 本文件
```

## 论文编译

模板使用 **LuaLaTeX** + **biblatex/biber**。

### 快速编译

```bash
cd docs/BT/CTU_FEL_THESIS
make pdf
```

### 手动编译

```bash
cd docs/BT/CTU_FEL_THESIS
lualatex thesis-final.tex
biber thesis-final
lualatex thesis-final.tex
lualatex thesis-final.tex
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

- [CTU FEL 论文模板](https://github.com/tohecz/ctuthesis)
- [LaTeX 教程](https://en.wikibooks.org/wiki/LaTeX)
