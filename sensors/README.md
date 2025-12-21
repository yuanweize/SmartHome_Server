# Sensor Simulator

A simple multi-broker MQTT sensor simulator used to demonstrate smart home sensor publishing for Home Assistant via Mosquitto and EMQX. It can publish the same virtual sensor data to multiple brokers concurrently.

Files:
- `sensor_simulator.py` — main simulator script
- `brokers.example.yml` — example broker configuration; copy to `brokers.yml` and edit

## Prerequisites

- macOS or Linux with Python 3.8+
- Recommended: virtual environment (venv, uv)

Install dependencies in a local venv (zsh):

```bash
cd SmartHome_Server
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create `sensors/brokers.yml` based on `sensors/brokers.example.yml`:

```yaml
- host: chi.google.com
  port: 1883
  username: null
  password: null
  tls: false
  keepalive: 60

- host: sgp.google.com
  port: 1883
  username: your_emqx_user
  password: your_emqx_pass
  tls: false
  keepalive: 60
```

Notes:
- YAML and JSON are both supported. Use `--config` to specify a custom path.
- Credentials should not be committed. `sensors/brokers.yml` is git-ignored.

## Quick start

Dry-run (no network publishes, logs only):

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --dry-run -n 5 -i 1 --payload json --log-level DEBUG
```

Publish to both brokers using `sensors/brokers.yml`:

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py -n 50 -i 5 --payload json --qos 1
```

Use a custom config file:

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py --config sensors/brokers.dev.yml -n 10 -i 2
```

Home Assistant MQTT Discovery (no YAML needed):

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py -n 20 -i 5 --payload json --ha-discovery
```

## TLS / mTLS certificates

The simulator supports two ways to provide TLS materials:

1) **File paths** in `sensors/brokers.yml` (`ca_file`, `cert_file`, `key_file`).
  - Paths are resolved **relative to the brokers config file**.
  - With Docker, this matches `sensors/docker-compose.yml` mounting `./certs` into the container.
  - Common pitfall: if your certs are stored at repo root `certs/`, then a path like `./certs/...` inside `sensors/brokers.yml` refers to `sensors/certs/...`.
    Use `../certs/...` or copy certs under `sensors/certs/...`.

2) **Inline PEM text** in `sensors/brokers.yml` (`ca_pem`, `cert_pem`, `key_pem`).
  - Inline PEM takes priority over file paths.
  - If inline TLS setup fails, it will fall back to file paths (if present).

Drift model with noise and jitter:

```bash
. .venv/bin/activate
python sensors/sensor_simulator.py -n 10 -i 2 --payload json \
  --model drift --drift-per-minute 0.5 --noise-sd 0.1 --jitter 0.1
```

## Options (summary)

- `-c, --config` Path to brokers config (YAML/JSON). Default: `sensors/brokers.yml`
- `-n, --sensors` Number of virtual sensors. Default: 50
- `-i, --interval` Seconds between publishes. Default: 5
- `-t, --topic-template` MQTT topic template. Default: `sensor/{sensor_id}/data`
- `--payload` Payload format: `plain` or `json`. Default: `json`
- `--qos` QoS level: 0, 1, or 2. Default: 0
- `--retain` Set MQTT retain flag
- `--min` / `--max` Value range for generated temperature. Default: 20.0 / 30.0
- `--client-id-prefix` Prefix for MQTT client IDs (optional)
- `--connect-timeout` Seconds to wait for MQTT connections before publishing. Default: 5.0
- `--ha-discovery` Publish Home Assistant MQTT Discovery config (retained)
- `--discovery-prefix` HA discovery prefix. Default: `homeassistant`
- `--model` Temperature model: `uniform` or `drift`. Default: `drift`
- `--noise-sd` Std dev of Gaussian noise per publish when `--model drift`. Default: 0.2
- `--drift-per-minute` Linear drift in value per minute when `--model drift`. Default: 0.0
- `--jitter` Sleep jitter as fraction of interval (e.g., 0.1 = ±10%). Default: 0.0
- `--seed` Global RNG seed for deterministic runs (overrides per-sensor seeding)
- `--dry-run` Do not connect/publish; log only
- `--once` Publish one cycle then exit
- `--log-level` Logging level (DEBUG, INFO, WARNING, ERROR). Default: INFO

## Troubleshooting

- If imports fail, ensure the virtual environment is active and dependencies are installed.
- For EMQX authentication errors, double-check `username`/`password` in `brokers.yml`.
- If you enable TLS on your brokers, set `tls: true` in the corresponding entry. By default, system CA certs are used.
- Use `--log-level DEBUG` to see connection and publish details.
