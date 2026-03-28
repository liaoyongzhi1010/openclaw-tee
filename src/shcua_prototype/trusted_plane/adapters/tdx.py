from __future__ import annotations

from .base import TrustedPlaneAdapter


class TdxTrustedAdapter(TrustedPlaneAdapter):
    def recv_request(self) -> dict:
        raise NotImplementedError("Integrate with TDX vsock receiver")

    def send_decision(self, decision: dict) -> None:
        raise NotImplementedError("Integrate with TDX vsock sender")

    def persist_evidence(self, evidence: dict) -> None:
        return None
