from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class TrustedBackend(ABC):
    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_request(self, req: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
