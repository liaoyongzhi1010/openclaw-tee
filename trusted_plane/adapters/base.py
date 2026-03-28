from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TrustedPlaneAdapter(ABC):
    @abstractmethod
    def recv_request(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def send_decision(self, decision: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def persist_evidence(self, evidence: dict[str, Any]) -> None:
        raise NotImplementedError
