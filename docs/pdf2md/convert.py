#!/usr/bin/env python3
"""
PDF to Markdown Converter using pymupdf4llm

Features:
  - Convert local PDF files
  - Download and convert PDFs from URLs
  - Batch conversion support
  - Skip already downloaded/converted files (MD5 cache)

Usage:
  python convert.py                    # Convert all PDFs in input/
  python convert.py file.pdf           # Convert specific local file
  python convert.py --urls             # Download & convert URLs from urls.txt
  python convert.py --url <URL>        # Download & convert single URL
  python convert.py --force            # Force re-download and re-convert
"""

import sys
import re
import json
import hashlib
import urllib.request
from pathlib import Path
from urllib.parse import urlparse, unquote

import pymupdf4llm

SCRIPT_DIR = Path(__file__).parent
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "output"
URLS_FILE = SCRIPT_DIR / "urls.txt"
CACHE_FILE = SCRIPT_DIR / ".cache.json"


def load_cache() -> dict:
    """Load cache from file."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except:
            pass
    return {"downloads": {}, "conversions": {}}


def save_cache(cache: dict):
    """Save cache to file."""
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def file_md5(path: Path) -> str:
    """Calculate MD5 hash of a file."""
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def sanitize_filename(name: str) -> str:
    """Remove invalid characters from filename."""
    name = unquote(name)  # URL decode
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name[:200]  # Limit length


def download_pdf(url: str, cache: dict, force: bool = False) -> Path | None:
    """Download PDF from URL to input directory."""
    # Extract filename from URL
    parsed = urlparse(url)
    filename = Path(parsed.path).name
    if not filename.endswith('.pdf'):
        filename = sanitize_filename(parsed.path.split('/')[-1]) + '.pdf'
    filename = sanitize_filename(filename)
    
    output_path = INPUT_DIR / filename
    
    # Check cache - skip if already downloaded from same URL
    if not force and output_path.exists():
        cached_url = cache["downloads"].get(str(output_path))
        if cached_url == url:
            print(f"Skipping download (cached): {filename}")
            return output_path
    
    print(f"Downloading: {url[:80]}...")
    
    try:
        # Download with headers to avoid 403
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        
        with urllib.request.urlopen(req, timeout=60) as response:
            output_path.write_bytes(response.read())
        
        # Update cache
        cache["downloads"][str(output_path)] = url
        save_cache(cache)
        
        print(f"  → Saved: {filename}")
        return output_path
        
    except Exception as e:
        print(f"  Error downloading: {e}")
        return None


def convert_pdf(pdf_path: Path, cache: dict, force: bool = False) -> Path | None:
    """Convert a single PDF to Markdown."""
    output_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
    
    # Calculate input file MD5
    input_md5 = file_md5(pdf_path)
    
    # Check cache - skip if input file unchanged
    if not force and output_path.exists():
        cached_md5 = cache["conversions"].get(str(output_path))
        if cached_md5 == input_md5:
            print(f"Skipping conversion (cached): {pdf_path.name}")
            return output_path
    
    print(f"Converting: {pdf_path.name}")
    
    try:
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        
        output_path.write_text(md_text, encoding="utf-8")
        
        # Update cache with input file MD5
        cache["conversions"][str(output_path)] = input_md5
        save_cache(cache)
        
        print(f"  → {output_path.name} ({len(md_text):,} chars)")
        return output_path
        
    except Exception as e:
        print(f"  Error converting: {e}")
        return None


def load_urls() -> list[str]:
    """Load URLs from urls.txt file."""
    if not URLS_FILE.exists():
        # Create template file
        URLS_FILE.write_text(
            "# PDF URLs (one per line)\n"
            "# Lines starting with # are comments\n"
            "# Example:\n"
            "# https://example.com/document.pdf\n"
        )
        print(f"Created template: {URLS_FILE}")
        return []
    
    urls = []
    for line in URLS_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            urls.append(line)
    return urls


def main():
    # Ensure directories exist
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    args = sys.argv[1:]
    force = '--force' in args
    if force:
        args.remove('--force')
    
    # Load cache
    cache = load_cache()
    
    # Mode: Download from URLs file
    if '--urls' in args:
        urls = load_urls()
        if not urls:
            print(f"No URLs found. Add URLs to: {URLS_FILE}")
            return
        
        print(f"Found {len(urls)} URL(s)\n")
        for url in urls:
            pdf_path = download_pdf(url, cache, force)
            if pdf_path:
                convert_pdf(pdf_path, cache, force)
            print()
    
    # Mode: Download single URL
    elif '--url' in args:
        idx = args.index('--url')
        if idx + 1 >= len(args):
            print("Usage: python convert.py --url <URL>")
            return
        url = args[idx + 1]
        pdf_path = download_pdf(url, cache, force)
        if pdf_path:
            convert_pdf(pdf_path, cache, force)
    
    # Mode: Convert local files
    else:
        if args:
            # Convert specific file(s)
            pdf_files = [Path(f) for f in args if not f.startswith('-')]
        else:
            # Convert all PDFs in input directory
            pdf_files = list(INPUT_DIR.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found.")
            print(f"  - Place PDFs in: {INPUT_DIR}")
            print(f"  - Or add URLs to: {URLS_FILE}")
            return
        
        print(f"Found {len(pdf_files)} PDF(s)\n")
        
        for pdf in pdf_files:
            if not pdf.exists():
                # Check if it's in input dir
                pdf_in_input = INPUT_DIR / pdf.name
                if pdf_in_input.exists():
                    pdf = pdf_in_input
                else:
                    print(f"Not found: {pdf}")
                    continue
            
            convert_pdf(pdf, cache, force)
    
    print(f"\nDone! Output in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

# [CodeRabbit Audit Trigger 1769364389]
