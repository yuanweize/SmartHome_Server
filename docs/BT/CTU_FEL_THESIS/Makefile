# Thesis build with auto-versioning
BASENAME = bachelor_thesis_Yuan
VERSION_FILE = .version
VERSION = $(shell cat $(VERSION_FILE) 2>/dev/null || echo "1.0")
JOBNAME = $(BASENAME)_v$(VERSION)

.PHONY: all pdf bump clean

# 默认: bump + pdf
all: bump pdf

pdf:
	lualatex -interaction=nonstopmode -jobname=$(JOBNAME) thesis-final.tex
	biber $(JOBNAME)
	lualatex -interaction=nonstopmode -jobname=$(JOBNAME) thesis-final.tex
	lualatex -interaction=nonstopmode -jobname=$(JOBNAME) thesis-final.tex
	@if grep -q "^!" $(JOBNAME).log 2>/dev/null; then \
		echo "❌ LaTeX errors found:"; \
		grep "^!" $(JOBNAME).log; \
		exit 1; \
	else \
		echo "✅ Output: $(JOBNAME).pdf"; \
	fi

bump:
	@if [ ! -f $(VERSION_FILE) ]; then echo "1.0" > $(VERSION_FILE); fi
	@NEW_VER=$$(awk 'BEGIN{printf "%.1f", '$(VERSION)'+0.1}'); \
	echo "$$NEW_VER" > $(VERSION_FILE); \
	echo "📌 Version: $(VERSION) → $$NEW_VER"

clean:
	latexmk -C
	rm -f $(BASENAME)_v*.aux $(BASENAME)_v*.bbl $(BASENAME)_v*.bcf \
	      $(BASENAME)_v*.blg $(BASENAME)_v*.log $(BASENAME)_v*.out \
	      $(BASENAME)_v*.run.xml $(BASENAME)_v*.lof $(BASENAME)_v*.lot \
	      $(BASENAME)_v*.toc $(BASENAME)_v*.pdf