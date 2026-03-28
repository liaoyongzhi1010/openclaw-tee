from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .base import TrustedBackend


class HttpTrustedBackend(TrustedBackend):
    """Send TrustedRequest to a remote endpoint service over HTTP."""

    def __init__(self, endpoint_url: str, backend_name: str, timeout_sec: float = 5.0) -> None:
        self.endpoint_url = endpoint_url
        self.backend_name = backend_name
        self.timeout_sec = timeout_sec

    def initialize(self) -> None:
        return None

    def send_request(self, req: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps(req).encode("utf-8")
        http_req = urllib.request.Request(
            self.endpoint_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(http_req, timeout=self.timeout_sec) as resp:
                body = resp.read().decode("utf-8")
                if not body:
                    return {"allow": False, "reason": "empty response", "constraints": {}}
                return json.loads(body)
        except urllib.error.URLError as exc:
            return {
                "allow": False,
                "reason": f"transport error: {exc}",
                "constraints": {},
            }

    def name(self) -> str:
        return self.backend_name
