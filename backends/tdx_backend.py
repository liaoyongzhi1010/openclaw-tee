from __future__ import annotations

from .vsock_backend import VsockBackend


class TdxBackend(VsockBackend):
    def name(self) -> str:
        return "tdx"
