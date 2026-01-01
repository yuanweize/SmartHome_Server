# CTU/FEL Thesis Template (LuaLaTeX)

This folder is the canonical LaTeX thesis template for this repo.

## What to compile

- Main entry (use this): `thesis-final.tex`
- Template class (layout + title pages): `phdthesis.cls`

Chapters live in `chapters/` and are included from `thesis-final.tex`.

## Build (local)

This template uses **LuaLaTeX + biblatex/biber**.

From this folder:

```bash
lualatex thesis-final.tex
biber thesis-final
lualatex thesis-final.tex
lualatex thesis-final.tex
```

If you use `latexmk` (recommended), `latexmkrc` is provided:

```bash
latexmk -lualatex thesis-final.tex
```

## Draft vs print layout

Default is **draft-friendly oneside** (no left/right margin swapping).

For final double-sided printing with binding margins, change the first line of `thesis-final.tex` to:

```tex
\documentclass[print]{phdthesis}
```

## Acronyms / glossary

- Acronyms are defined in `acronyms.tex`.
- The template uses **no-index glossaries**, so you do **not** need `makeglossaries`.
- Add an acronym via `\newacronym{...}{...}{...}` and use it in text with `\gls{...}`.

## Overleaf

1) Upload this folder as a project.
2) Set **Main file** to `thesis-final.tex`.
3) Set compiler to **LuaLaTeX**.

If references/acronyms look stale, use “Recompile from scratch” or compile twice.

## Clean

If you use `latexmk`:

```bash
latexmk -c   # keep PDF
latexmk -C   # remove PDF too
```

Or manual:

```bash
rm -f *.aux *.bbl *.bcf *.blg *.run.xml *.toc *.lof *.lot *.out *.log \
	*.fls *.fdb_latexmk *.synctex.gz
```

## Notes

- Some Czech words remain where they are official names.
- Logo/image assets are optional; missing assets should not break compilation.
