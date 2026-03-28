from __future__ import annotations

from .base import TrustedPlaneAdapter


class KeystoneTrustedAdapter(TrustedPlaneAdapter):
    def recv_request(self) -> dict:
        raise NotImplementedError("Integrate with Keystone enclave receiver")

    def send_decision(self, decision: dict) -> None:
        raise NotImplementedError("Integrate with Keystone enclave sender")

    def persist_evidence(self, evidence: dict) -> None:
        return None
