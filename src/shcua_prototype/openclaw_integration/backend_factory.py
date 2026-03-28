from __future__ import annotations

from collections.abc import Callable
from typing import Any

from shcua_prototype.backends.base import TrustedBackend
from shcua_prototype.backends.http_backend import HttpTrustedBackend
from shcua_prototype.backends.keystone_backend import KeystoneBackend
from shcua_prototype.backends.sev_backend import SevBackend
from shcua_prototype.backends.tdx_backend import TdxBackend
from shcua_prototype.backends.trustzone_backend import TrustZoneBackend
from shcua_prototype.openclaw_integration.router import BackendRouter


def _build_backend(entry: dict[str, Any]) -> TrustedBackend:
    backend_type = str(entry.get("backend", "http"))

    if backend_type == "tdx":
        return TdxBackend(cid=int(entry.get("cid", 3)), port=int(entry.get("port", 5001)))
    if backend_type == "sev":
        return SevBackend(cid=int(entry.get("cid", 4)), port=int(entry.get("port", 5001)))
    if backend_type == "trustzone":
        return TrustZoneBackend(endpoint_url=str(entry.get("endpoint_url", "http://127.0.0.1:19001/trusted-request")))
    if backend_type == "keystone":
        return KeystoneBackend(endpoint_url=str(entry.get("endpoint_url", "http://127.0.0.1:19002/trusted-request")))
    if backend_type == "http":
        return HttpTrustedBackend(
            endpoint_url=str(entry["endpoint_url"]),
            backend_name=str(entry.get("name", "http")),
        )

    raise ValueError(f"unsupported backend type: {backend_type}")


def build_router_from_config(
    config: dict[str, Any],
    backend_builder: Callable[[dict[str, Any]], TrustedBackend] | None = None,
) -> BackendRouter:
    mapping: dict[tuple[str, str], TrustedBackend] = {}
    builder = backend_builder or _build_backend

    for plane_name, plane_cfg in config.get("planes", {}).items():
        targets = plane_cfg.get("targets", {})
        for target_id, target_entry in targets.items():
            mapping[(plane_name, target_id)] = builder(target_entry)

    return BackendRouter(mapping=mapping)
