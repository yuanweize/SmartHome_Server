# Home Assistant 配置

语言：**简体中文** | [English](README.md)

本目录包含用于智能家居系统的 Home Assistant 配置参考和自动化模板。

## 目录结构

```
homeassistant/
├── docker-compose.yml          # 参考配置（用于容器安装）
└── fall_detection_nodered.json # Node-RED 跌倒检测通知流程模板
```

## 安装方式

Home Assistant 提供两种主要安装类型：

| 类型 | Add-ons 支持 | 自动更新 | 推荐 |
|------|-------------|----------|------|
| **Home Assistant OS** | ✅ 支持 | ✅ 支持 | ✅ 大多数用户 |
| **Home Assistant Container** | ❌ 不支持 | ❌ 手动 | 高级用户 |

> **本项目使用 Home Assistant OS**，部署于 ESXi（OVA 镜像），以支持 Node-RED 等 Add-ons。

### 方式一：Home Assistant OS（推荐）

适用于虚拟机（ESXi、Proxmox、VirtualBox 等）：

1. 从 [HA 安装页面](https://www.home-assistant.io/installation/) 下载 OVA/QCOW2 镜像
2. 导入至你的虚拟化平台
3. 访问 Web 界面：`http://<VM_IP>:8123`

### 方式二：Docker 容器

```bash
cd homeassistant
docker compose up -d
```

> ⚠️ **注意：** 容器安装**不支持** Add-ons（包括 Node-RED）。

## 配置 MQTT 集成

1. 进入 **设置 → 设备与服务 → 添加集成 → MQTT**
2. 配置 mTLS 连接：
   - Broker: 你的 MQTT 服务器地址
   - 端口: `8883`
   - 启用 TLS
   - 上传 `../certs/ha/` 目录下的证书

## Node-RED Add-on（仅限 HAOS）

Node-RED Add-on 仅在 **Home Assistant OS** 安装中可用。

### 安装 Node-RED Add-on

1. 进入 **设置 → 加载项 → 加载项商店**
2. 搜索 "Node-RED" 并安装
3. 启用「开机启动」和「看门狗」
4. 启动 Add-on 并打开 Web UI

### 导入跌倒检测流程

1. 在 Node-RED 中点击 **菜单 (☰) → 导入**
2. 粘贴 `fall_detection_nodered.json` 的内容
3. 更新占位符：
   - `YOUR_FALL_DETECTION_ENTITY` → 你的实际实体 ID（如 `binary_sensor.esp32_fall_detected`）
   - `YOUR_DEVICE` → 你的手机 App 设备名（如 `iphone_weize`）
4. 点击 **部署 (Deploy)**

## 文件说明

### docker-compose.yml

Home Assistant Container 的参考配置：
- 持久化配置存储
- 主机网络模式（便于设备发现）
- 自动重启策略

### fall_detection_nodered.json

跌倒检测通知的 Node-RED 流程模板：
- 监控二元传感器状态变化（`on` → 检测到跌倒）
- 发送带有可操作按钮的手机推送通知
- 依赖：`node-red-contrib-home-assistant-websocket`（Add-on 中已预装）

## 相关文档

- [Home Assistant 安装指南](https://www.home-assistant.io/installation/)
- [MQTT 集成](https://www.home-assistant.io/integrations/mqtt/)
- [Node-RED Add-on](https://github.com/hassio-addons/addon-node-red)

## 证书配置

mTLS 证书生成请参阅 [`../certs/README.zh-CN.md`](../certs/README.zh-CN.md)。

