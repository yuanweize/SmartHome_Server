# Diplomová práce – Marketingový výzkum a vstup na trh (Značka Berrie)

Tento repozitář obsahuje kompletní zdrojové kódy a strukturu pro diplomovou práci v oboru Marketingové komunikace na Panevropské univerzitě. 

**Téma:** Marketingový výzkum pro vstup nové značky mraženého ovoce v čokoládě na český trh  
**Značka:** Berrie  
**Autor:** Bc. Catherine Zoë Meijer  

---

## 📂 Struktura repozitáře

Repozitář je navržen tak, aby striktně odděloval zdrojové kódy práce od vygenerovaných souborů a citlivých dat.

- `thesis/` — Zdrojové soubory diplomové práce (LaTeX).
  - `main.tex` — Hlavní soubor práce (spojuje všechny kapitoly).
  - `thesis.cls` — Šablona práce přizpůsobená pro Panevropskou univerzitu (obsahuje formátování a APA 7).
  - `literature.bib` — Seznam literatury a zdrojů (BibLaTeX).
  - `acronyms.tex` — Seznam zkratek.
  - `Makefile` a `latexmkrc` — Skripty pro automatickou kompilaci PDF.
  - `chapters/` — Jednotlivé kapitoly práce (Úvod, Teorie, Metodologie, Výzkum, Výsledky, Závěr, Abstrakt).
  - `images/` — Obrázky použité v práci (např. logo univerzity).
- `private/` — Složka pro citlivé dokumenty (zadání práce, podklady k výzkumu). Tato složka je ignorována Githem, aby nedošlo k úniku dat na GitHub.
- `dst/` — Složka, do které se automaticky uloží výsledné zkompilované PDF (`Meijer_Catherine_Diplomova_Prace.pdf`).
- `.gitignore` — Konfigurace Gitu, která ignoruje složky `dst/`, `private/` a dočasné kompilační soubory z `thesis/build/`.

---

## 🛠 Jak zkompilovat PDF

Pro kompilaci dokumentu do formátu PDF se používá plnohodnotná instalace **MacTeX**. K překladu se používá engine `LuaLaTeX` a pro bibliografii nástroj `Biber`.

### 1. Požadavky a instalace (macOS)

Pokud na počítači nemáte nainstalovaný LaTeX, nainstalujte distribuci MacTeX:

```bash
# Instalace MacTeX přes Homebrew
brew install --cask mactex
```

*(Poznámka: Po dokončení instalace MacTeXu je obvykle nutné restartovat terminál, aby se aktualizovaly systémové cesty.)*

### 2. Kompilace práce

Pro vygenerování PDF stačí vstoupit do složky `thesis` a spustit `make pdf`.

```bash
cd thesis
make pdf
```

Tento příkaz spustí `latexmk`, který provede všechny potřebné kroky (včetně překladu citací přes Biber a tvorby seznamu zkratek) a finální PDF s názvem `Meijer_Catherine_Diplomova_Prace.pdf` umístí do složky `dst/` v kořenovém adresáři repozitáře. 

Všechny dočasné kompilační soubory (jako `.aux`, `.log`, `.toc` atd.) jsou ukládány izolovaně do složky `thesis/build/`, takže zdrojová složka zůstane čistá.

### 3. Čištění dočasných souborů

Pro smazání dočasných kompilačních souborů a vyčištění složky `build/` spusťte:

```bash
cd thesis
make clean
```
Tento příkaz navíc smaže i staré PDF ze složky `dst/`.