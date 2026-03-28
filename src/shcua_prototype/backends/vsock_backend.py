from __future__ import annotations

from typing import Any

from .base import TrustedBackend


class VsockBackend(TrustedBackend):
    def __init__(self, cid: int, port: int) -> None:
        self.cid = cid
        self.port = port

    def initialize(self) -> None:
        return None

    def send_request(self, req: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Implement vsock transport")

    def name(self) -> str:
        return "vsock"
