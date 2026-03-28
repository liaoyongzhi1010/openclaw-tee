from __future__ import annotations

from .base import TrustedPlaneAdapter


class SevTrustedAdapter(TrustedPlaneAdapter):
    def recv_request(self) -> dict:
        raise NotImplementedError("Integrate with SEV vsock receiver")

    def send_decision(self, decision: dict) -> None:
        raise NotImplementedError("Integrate with SEV vsock sender")

    def persist_evidence(self, evidence: dict) -> None:
        return None
