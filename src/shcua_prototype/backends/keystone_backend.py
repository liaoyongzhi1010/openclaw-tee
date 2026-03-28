from __future__ import annotations

from .http_backend import HttpTrustedBackend


class KeystoneBackend(HttpTrustedBackend):
    def __init__(self, endpoint_url: str = "http://127.0.0.1:19002/trusted-request") -> None:
        super().__init__(endpoint_url=endpoint_url, backend_name="keystone")
