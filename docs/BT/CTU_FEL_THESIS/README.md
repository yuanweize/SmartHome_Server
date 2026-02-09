# CTU/FEL Thesis Template (LuaLaTeX)

This folder is the canonical LaTeX thesis template for this repo.

## What to compile

- Main entry (use this): `thesis-final.tex`
- Template class (layout + title pages): `bachelorthesis.cls`

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

Tip: `latexmkrc` sets a default main file, so in this folder you can also just run:

```bash
latexmk -lualatex
```

## Draft vs print layout

Default is **draft-friendly oneside** (no left/right margin swapping).

For final double-sided printing with binding margins, change the first line of `thesis-final.tex` to:

```tex
\documentclass[print]{bachelorthesis}
```

## Acronyms / glossary

- Acronyms are defined in `acronyms.tex`.
- The template uses **no-index glossaries**, so you do **not** need `makeglossaries`.
- Add an acronym via `\newacronym{...}{...}{...}` and use it in text with `\gls{...}`.

## Overleaf

1) Upload this folder as a project.
2) Set **Main file** to `thesis-final.tex`.
3) Set **Compiler** to **LuaLaTeX**.
4) Set **Bibliography** to **Biber**.

If you see errors like `output.bbl not found`, `Empty bibliography`, or many `Citation '...' undefined`, it usually means **biber did not run**. Use “Recompile from scratch”.

## Clean

If you use `latexmk`:

```bash
latexmk -c   # keep PDF
latexmk -C   # remove PDF too
```

If your build artifacts are named `output.*` (common when compiling with `-jobname=output`, as Overleaf sometimes does), clean them explicitly:

```bash
latexmk -C -jobname=output thesis-final.tex
```

If you accidentally created `acronyms.*` artifacts by running latexmk on `acronyms.tex`, clean them explicitly:

```bash
latexmk -C acronyms.tex
```

Or manual:

```bash
rm -f *.aux *.bbl *.bcf *.blg *.run.xml *.toc *.lof *.lot *.out *.log \
	*.fls *.fdb_latexmk *.synctex.gz

# If you also have Overleaf-style artifacts:
rm -f output.*
```

## Notes

- Some Czech words remain where they are official names.
- Logo/image assets are optional; missing assets should not break compilation.

