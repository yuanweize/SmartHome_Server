# Diplomová práce – Build systém
BASENAME = Meijer_Catherine_Diplomova_Prace
DST_DIR = ../dst
BUILD_DIR = build

.PHONY: pdf clean

pdf:
	mkdir -p $(DST_DIR)
	latexmk -lualatex -interaction=nonstopmode main.tex
	@cp $(BUILD_DIR)/main.pdf $(DST_DIR)/$(BASENAME).pdf 2>/dev/null || true
	@echo "✅ Výstup: $(DST_DIR)/$(BASENAME).pdf"

clean:
	latexmk -C
	rm -rf $(BUILD_DIR)
	rm -f $(DST_DIR)/$(BASENAME).pdf
	@echo "🧹 Vyčištěno"
