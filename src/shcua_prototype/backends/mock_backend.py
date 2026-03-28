from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .base import TrustedBackend


class MockTrustedBackend(TrustedBackend):
    def __init__(self, backend_name: str = "mock_trusted", deny_levels: Iterable[str] = ("critical",)) -> None:
        self._backend_name = backend_name
        self._deny_levels = {str(level) for level in deny_levels}

    def initialize(self) -> None:
        return None

    def send_request(self, req: dict[str, Any]) -> dict[str, Any]:
        level = str(req.get("level", "low"))
        scope = req.get("scope", {})

        if level in self._deny_levels:
            return {
                "allow": False,
                "reason": f"mock policy denied level={level}",
                "constraints": {},
            }

        return {
            "allow": True,
            "reason": "mock policy authorized request",
            "constraints": {
                "target": scope.get("target"),
                "action": scope.get("action"),
                "restrictions": scope.get("restrictions", {}),
                "target_id": req.get("target_id"),
                "plane": req.get("plane"),
            },
        }

    def name(self) -> str:
        return self._backend_name
