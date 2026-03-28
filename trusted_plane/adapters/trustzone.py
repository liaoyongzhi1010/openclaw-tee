from __future__ import annotations

from .base import TrustedPlaneAdapter


class TrustZoneTrustedAdapter(TrustedPlaneAdapter):
    def recv_request(self) -> dict:
        raise NotImplementedError("Integrate with TrustZone secure-world receiver")

    def send_decision(self, decision: dict) -> None:
        raise NotImplementedError("Integrate with TrustZone secure-world sender")

    def persist_evidence(self, evidence: dict) -> None:
        return None
