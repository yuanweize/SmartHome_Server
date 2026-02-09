# Home Assistant Configuration

Language: **English** | [简体中文](README.zh-CN.md)

This directory contains configuration references and automation templates for Home Assistant integration with the Smart Home IoT system.

## Directory Contents

```
homeassistant/
├── docker-compose.yml          # Reference config (for Container installs)
└── fall_detection_nodered.json # Node-RED flow template for fall alerts
```

## Installation Methods

Home Assistant offers two main installation types:

| Type | Add-ons | Auto-updates | Recommended |
|------|---------|--------------|-------------|
| **Home Assistant OS** | ✅ Yes | ✅ Yes | ✅ Most users |
| **Home Assistant Container** | ❌ No | ❌ Manual | Advanced users |

> **This project uses Home Assistant OS** on ESXi (OVA image) to enable Add-ons like Node-RED.

### Option 1: Home Assistant OS (Recommended)

For virtual machines (ESXi, Proxmox, VirtualBox, etc.):

1. Download the OVA/QCOW2 image from [HA Installation](https://www.home-assistant.io/installation/)
2. Import into your hypervisor
3. Access web UI at `http://<VM_IP>:8123`

### Option 2: Docker Container

```bash
cd homeassistant
docker compose up -d
```

> ⚠️ **Note:** Container installs do NOT support Add-ons (including Node-RED).

## Configure MQTT Integration

1. Go to **Settings → Devices & Services → Add Integration → MQTT**
2. Configure with mTLS:
   - Broker: your MQTT server address
   - Port: `8883`
   - Enable TLS
   - Upload certificates from `../certs/ha/`

## Node-RED Add-on (HAOS Only)

Node-RED Add-on is only available on **Home Assistant OS** installations.

### Install Node-RED Add-on

1. Go to **Settings → Add-ons → Add-on Store**
2. Search for "Node-RED" and install
3. Enable "Start on boot" and "Watchdog"
4. Start the add-on and open Web UI

### Import Fall Detection Flow

1. In Node-RED, click **Menu (☰) → Import**
2. Paste contents of `fall_detection_nodered.json`
3. Update placeholder values:
   - `YOUR_FALL_DETECTION_ENTITY` → your actual entity ID (e.g., `binary_sensor.esp32_fall_detected`)
   - `YOUR_DEVICE` → your mobile app device name (e.g., `iphone_weize`)
4. Click **Deploy**

## Files

### docker-compose.yml

Reference configuration for Home Assistant Container:
- Persistent configuration storage
- Host network mode for device discovery
- Auto-restart policy

### fall_detection_nodered.json

Node-RED flow template for fall detection notifications:
- Monitors binary sensor state changes (`on` → fall detected)
- Sends mobile push notifications with actionable alerts
- Requires: `node-red-contrib-home-assistant-websocket` (pre-installed in Add-on)

## Related Documentation

- [Home Assistant Installation](https://www.home-assistant.io/installation/)
- [MQTT Integration](https://www.home-assistant.io/integrations/mqtt/)
- [Node-RED Add-on](https://github.com/hassio-addons/addon-node-red)

## Certificate Setup

See [`../certs/README.md`](../certs/README.md) for mTLS certificate generation.

