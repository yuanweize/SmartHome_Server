# Documentation Hub

Language: **English** | [简体中文](README.zh-CN.md)

This directory contains all thesis documentation, LaTeX sources, and supporting materials.

## Directory Structure

```
docs/
├── BT/
│   ├── CTU_FEL_THESIS/      # LaTeX thesis template (main)
│   │   ├── thesis-final.tex # Entry file (compile this)
│   │   ├── chapters/        # Chapter source files
│   │   └── images/          # Figures and diagrams
│   ├── thesis_doc/          # Planning notes and drafts
│   └── FIG/                 # Additional figures
└── README.md                # This file
```

## Thesis Compilation

The template uses **LuaLaTeX** with **biblatex/biber**.

### Quick Build

```bash
cd docs/BT/CTU_FEL_THESIS
make          # Auto-bump version + compile
make pdf      # Compile only (no version bump)
```

Output: `bachelor_thesis_Yuan_vX.X.pdf` (auto-versioned)

### Manual Build

```bash
cd docs/BT/CTU_FEL_THESIS
lualatex -jobname=thesis thesis-final.tex
biber thesis
lualatex -jobname=thesis thesis-final.tex
lualatex -jobname=thesis thesis-final.tex
```

### VS Code Task

Use the pre-configured task: `thesis: make pdf`

### Draft vs Print Mode

Default: **oneside** mode (no margin swapping, suitable for screen reading).

For double-sided printing with binding margins:

```tex
% Change first line of thesis-final.tex
\documentclass[print]{bachelorthesis}
```

## Clean Build Artifacts

```bash
cd docs/BT/CTU_FEL_THESIS
make clean      # Keep PDF
make distclean  # Remove PDF too
```

Or with latexmk:

```bash
latexmk -c   # Keep PDF
latexmk -C   # Remove PDF
```

## Key Files

| File | Description |
|------|-------------|
| `thesis-final.tex` | Main document entry point |
| `bachelorthesis.cls` | CTU FEL thesis class (title pages, layout) |
| `literature.bib` | Bibliography database |
| `chapters/*.tex` | Individual chapter sources |

## Related Documentation

- [CTU FEL Thesis Template (Overleaf)](https://www.overleaf.com/latex/templates/sablona-pro-psani-disertacni-prace-na-cvut-fel/ptpvbxhsjdmg)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
