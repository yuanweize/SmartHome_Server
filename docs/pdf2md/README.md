# PDF to Markdown Converter

Convert PDF documents to Markdown format using `pymupdf4llm`. Useful for feeding PDF content to LLMs.

## Structure

```
docs/pdf2md/
├── convert.py        # Main script
├── urls.example.txt  # Example URL list (copy to urls.txt)
├── urls.txt          # Your PDF URLs (git-ignored)
├── .cache.json       # Download/conversion cache (git-ignored)
├── input/            # Downloaded/local PDFs (git-ignored)
└── output/           # Converted Markdown files (git-ignored)
```

## Installation

```bash
pip install pymupdf4llm
```

## Quick Start

```bash
cd docs/pdf2md
cp urls.example.txt urls.txt
# Edit urls.txt with your PDF URLs
python convert.py --urls
```

## Usage

### Convert Local PDFs

```bash
# Convert all PDFs in input/ folder
python convert.py

# Convert specific file
python convert.py input/document.pdf
```

### Download & Convert from URL

```bash
# Single URL
python convert.py --url https://example.com/document.pdf

# Multiple URLs from urls.txt
python convert.py --urls
```

### Force Re-download/Re-convert

```bash
# Skip cache, re-download and re-convert everything
python convert.py --urls --force
```

## Caching

The script caches:
- **Downloads**: Skips if same URL already downloaded
- **Conversions**: Skips if input PDF unchanged (MD5 check)

Cache is stored in `.cache.json`. Use `--force` to bypass.

## Output

Converted Markdown files are saved to `output/` with the same name as the source PDF.
