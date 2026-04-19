# Diplomová práce — Marketingový výzkum pro vstup značky Berrie na český trh

**Bc. Catherine Zoë Meijer**
Panevropská univerzita, a.s. · Fakulta podnikání a práva
Navazující magisterský program: Marketingové komunikace
Vedoucí práce: doc. RNDr. Ivan TOMEK, CSc.

## Kompilace

### Požadavky

- [MacTeX](https://www.tug.org/mactex/) (obsahuje LuaLaTeX, Biber, Latexmk)

```bash
brew install --cask mactex
```

### Sestavení PDF

```bash
cd thesis
make pdf
```

Výstupní soubor: `thesis/Meijer_Catherine_Diplomova_Prace.pdf`

## Struktura projektu

```
frozen-fruit-market-entry/
├── thesis/              # LaTeX zdrojové soubory
│   ├── main.tex         # Hlavní soubor
│   ├── thesis.cls       # Třída dokumentu
│   ├── chapters/        # Kapitoly práce
│   ├── images/          # Obrázky a grafy
│   ├── literature.bib   # Bibliografie
│   └── Makefile         # Build systém
├── private/             # Citlivé soubory (vyloučeno z gitu)
└── README.md
```

## Akademický rok

2025/2026