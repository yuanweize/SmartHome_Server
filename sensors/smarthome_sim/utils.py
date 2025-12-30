"""Utility functions for SmartHome Simulator."""

from __future__ import annotations

import atexit
import json
import math
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def looks_like_pem(text: Optional[str]) -> bool:
    """Check if text looks like PEM-encoded data."""
    return bool(text and "-----BEGIN" in text)


def normalize_pem(text: str) -> str:
    """Normalize PEM text (strip, fix line endings, ensure trailing newline)."""
    return text.strip().replace("\r\n", "\n") + "\n"


def materialize_pem_bundle(
    *,
    ca_pem: Optional[str],
    cert_pem: Optional[str],
    key_pem: Optional[str],
    label: str,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Write inline PEM blobs to temp files and return their paths.
    
    Temp files are automatically cleaned up on process exit.
    """
    if not (ca_pem or cert_pem or key_pem):
        return None, None, None

    temp_dir = tempfile.mkdtemp(prefix=f"mqtt-certs-{label}-")
    atexit.register(shutil.rmtree, temp_dir, ignore_errors=True)

    def write_one(filename: str, pem_text: Optional[str]) -> Optional[str]:
        if not pem_text:
            return None
        file_path = Path(temp_dir) / filename
        file_path.write_text(normalize_pem(pem_text), encoding="utf-8")
        try:
            os.chmod(file_path, 0o600)
        except Exception:
            pass  # Best-effort on restricted platforms
        return str(file_path)

    return (
        write_one("ca.pem", ca_pem),
        write_one("client.pem", cert_pem),
        write_one("client.key", key_pem),
    )


def iso_utc(ts: Optional[float] = None) -> str:
    """Return ISO 8601 UTC timestamp string."""
    t = time.gmtime(ts if ts is not None else time.time())
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", t)


def ensure_dir(path: Path) -> None:
    """Create directory and parents if they don't exist."""
    path.mkdir(parents=True, exist_ok=True)


def percentile_sorted(values_sorted: List[float], q: float) -> float:
    """Calculate percentile with linear interpolation.
    
    Args:
        values_sorted: Non-empty, ascending-sorted list of values
        q: Percentile in range [0, 100]
    """
    if not values_sorted:
        raise ValueError("values_sorted must not be empty")
    if q <= 0:
        return values_sorted[0]
    if q >= 100:
        return values_sorted[-1]

    n = len(values_sorted)
    pos = (q / 100.0) * (n - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    if lo == hi:
        return values_sorted[lo]
    frac = pos - lo
    return values_sorted[lo] * (1.0 - frac) + values_sorted[hi] * frac


def convert(value: Any, typ: type, default: Any) -> Any:
    """Convert value to type, return default on failure."""
    try:
        return typ(value)
    except Exception:
        return default


def now_ts() -> int:
    """Return current Unix timestamp as integer."""
    return int(time.time())
