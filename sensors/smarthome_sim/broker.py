"""MQTT Broker connection and TLS/mTLS handling."""

from __future__ import annotations

import logging
import random
import ssl
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

import paho.mqtt.client as mqtt

from .utils import looks_like_pem, materialize_pem_bundle

if TYPE_CHECKING:
    from .entities import MQTTContext


@dataclass
class Broker:
    """MQTT broker configuration and client factory."""
    
    host: str
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    tls: bool = False
    
    # mTLS certificate paths
    ca_file: Optional[str] = None
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    
    # mTLS inline PEM (takes priority over file paths)
    ca_pem: Optional[str] = None
    cert_pem: Optional[str] = None
    key_pem: Optional[str] = None
    
    tls_insecure: bool = False
    keepalive: int = 60
    client_id: Optional[str] = None
    _config_dir: Path = Path(".")

    @classmethod
    def from_dict(cls, item: Dict[str, Any], config_path: Path) -> "Broker":
        """Create Broker from configuration dictionary."""
        host = item.get("host")
        if not host:
            raise ValueError("Broker entry missing 'host'")

        return cls(
            host=str(host),
            port=int(item.get("port", 1883)),
            username=item.get("username"),
            password=item.get("password"),
            tls=bool(item.get("tls", False)),
            ca_file=item.get("ca_file"),
            cert_file=item.get("cert_file"),
            key_file=item.get("key_file"),
            ca_pem=item.get("ca_pem"),
            cert_pem=item.get("cert_pem"),
            key_pem=item.get("key_pem"),
            tls_insecure=bool(item.get("tls_insecure", False)),
            keepalive=int(item.get("keepalive", 60)),
            client_id=item.get("client_id"),
            _config_dir=config_path.parent,
        )

    def _resolve_path(self, path_str: Optional[str]) -> Optional[str]:
        """Resolve relative paths based on config file location."""
        if not path_str:
            return None
        path = Path(path_str)
        if not path.is_absolute():
            path = self._config_dir / path
        return str(path)

    def _select_tls_material(self) -> Tuple[Dict[str, Optional[str]], Dict[str, Optional[str]]]:
        """Select TLS material with priority: inline PEM > file paths."""
        inline_ca = self.ca_pem or (self.ca_file if looks_like_pem(self.ca_file) else None)
        inline_cert = self.cert_pem or (self.cert_file if looks_like_pem(self.cert_file) else None)
        inline_key = self.key_pem or (self.key_file if looks_like_pem(self.key_file) else None)

        file_ca = None if looks_like_pem(self.ca_file) else self._resolve_path(self.ca_file)
        file_cert = None if looks_like_pem(self.cert_file) else self._resolve_path(self.cert_file)
        file_key = None if looks_like_pem(self.key_file) else self._resolve_path(self.key_file)

        primary = {
            "ca_pem": inline_ca, "cert_pem": inline_cert, "key_pem": inline_key,
            "ca_file": file_ca, "cert_file": file_cert, "key_file": file_key,
        }
        fallback = {"ca_file": file_ca, "cert_file": file_cert, "key_file": file_key}
        return primary, fallback

    def _configure_tls(self, client: mqtt.Client) -> None:
        """Configure TLS/mTLS on the MQTT client."""
        logging.debug(f"[{self.host}] Configuring TLS...")
        primary, fallback = self._select_tls_material()

        # Materialize inline PEM to temp files
        ca_temp, cert_temp, key_temp = materialize_pem_bundle(
            ca_pem=primary.get("ca_pem"),
            cert_pem=primary.get("cert_pem"),
            key_pem=primary.get("key_pem"),
            label=self.host.replace("/", "_").replace(":", "_"),
        )

        ca_primary = ca_temp or primary.get("ca_file")
        cert_primary = cert_temp or primary.get("cert_file")
        key_primary = key_temp or primary.get("key_file")

        # Warn about missing file-based paths
        for path, label in [(ca_primary, "CA"), (cert_primary, "Cert"), (key_primary, "Key")]:
            if path and path == primary.get(f"{label.lower()}_file") and not Path(path).exists():
                logging.warning(f"[{self.host}] {label} file not found: {path}")

        def apply_tls(label: str, ca: Optional[str], cert: Optional[str], key: Optional[str]) -> None:
            logging.debug(f"[{self.host}] TLS source={label} ca={bool(ca)} cert={bool(cert)} key={bool(key)}")
            client.tls_set(
                ca_certs=ca, certfile=cert, keyfile=key,
                cert_reqs=ssl.CERT_NONE if self.tls_insecure else ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS_CLIENT,
            )

        try:
            apply_tls("primary", ca_primary, cert_primary, key_primary)
        except Exception as e:
            has_inline = any(primary.get(k) for k in ("ca_pem", "cert_pem", "key_pem"))
            has_files = any(fallback.get(k) for k in ("ca_file", "cert_file", "key_file"))
            if has_inline and has_files:
                logging.warning(f"[{self.host}] TLS primary failed: {e}; trying file fallback")
                apply_tls("fallback", fallback.get("ca_file"), fallback.get("cert_file"), fallback.get("key_file"))
            else:
                raise

        if self.tls_insecure:
            client.tls_insecure_set(True)
            logging.warning(f"[{self.host}] TLS Insecure Mode (skipping verification)")

    def create_client(
        self,
        *,
        client_id_prefix: Optional[str],
        mqtt_context: "MQTTContext",
        on_connect,
        on_disconnect,
        on_message,
        auto_connect: bool = True,
        userdata_extra: Optional[Dict[str, Any]] = None,
    ) -> mqtt.Client:
        """Create and configure an MQTT client."""
        from .entities import MQTTContext
        
        cid = self.client_id or f"{client_id_prefix or 'sim'}-{random.randint(1000, 9999)}"
        client = mqtt.Client(client_id=cid, clean_session=True)

        userdata: Dict[str, Any] = {"broker_host": self.host, "ctx": mqtt_context}
        if userdata_extra:
            userdata.update(userdata_extra)
        client.user_data_set(userdata)

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        if self.username is not None:
            client.username_pw_set(self.username, self.password)

        if self.tls:
            self._configure_tls(client)

        client.reconnect_delay_set(min_delay=1, max_delay=60)

        if auto_connect:
            ud = client._userdata or {}
            if isinstance(ud, dict):
                ud.setdefault("connect_started_at", time.perf_counter())
            client.connect_async(self.host, self.port, keepalive=self.keepalive)
            client.loop_start()

        return client

