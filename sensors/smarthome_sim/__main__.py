"""
Entry point for `python -m smarthome_sim`.

This module enables running the simulator as a package:
    python -m smarthome_sim --config brokers.yml [options]

For standalone script usage, see: sensor_simulator.py
"""

from .cli import main

if __name__ == "__main__":
    main()

