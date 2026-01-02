#!/usr/bin/env python3
"""
SmartHome Simulator - Multi-broker MQTT sensor/actuator simulator with mTLS support.

A thesis-grade smart home platform for simulating and benchmarking IoT sensor/actuator
traffic over MQTT with mTLS support. Designed for Home Assistant integration and stress testing.

Usage:
    python sensor_simulator.py --config brokers.yml [options]
    python -m smarthome_sim --config brokers.yml [options]

Quick Start:
    # Dry-run test (no broker required)
    python sensor_simulator.py --dry-run

    # Connect to broker with Home Assistant discovery
    python sensor_simulator.py --config brokers.yml --ha-discovery

    # Stress test with 1000 devices
    python sensor_simulator.py --config brokers.yml --devices 1000 --workers 4

    # TLS handshake benchmark
    python sensor_simulator.py --config brokers.yml --handshake-samples 100 --handshake-only

For full documentation, see: sensors/README.md
"""

from __future__ import annotations

import sys
from pathlib import Path

# Minimum Python version check
MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
    sys.exit(f"Error: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required (current: {sys.version_info.major}.{sys.version_info.minor})")

# Ensure package is importable when running from sensors/ directory
_pkg_dir = Path(__file__).parent / "smarthome_sim"
if _pkg_dir.exists() and str(_pkg_dir.parent) not in sys.path:
    sys.path.insert(0, str(_pkg_dir.parent))


def main() -> None:
    """Entry point with graceful error handling."""
    try:
        from smarthome_sim.cli import main as cli_main
        cli_main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except ImportError as e:
        req_file = Path(__file__).with_name("requirements.txt")
        sys.exit(f"Import error: {e}\nRun: pip install -r {req_file}")
    except FileNotFoundError as e:
        sys.exit(f"File not found: {e}")
    except Exception as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
