from __future__ import annotations

from .vsock_backend import VsockBackend


class SevBackend(VsockBackend):
    def name(self) -> str:
        return "sev"
