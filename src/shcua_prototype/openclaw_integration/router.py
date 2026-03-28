from __future__ import annotations

from dataclasses import dataclass

from shcua_prototype.backends.base import TrustedBackend


@dataclass(slots=True)
class BackendRoute:
    plane: str
    target_id: str


class BackendRouter:
    """Resolve backend by (plane, target_id) to support centralized OpenClaw orchestration."""

    def __init__(self, mapping: dict[tuple[str, str], TrustedBackend], fallback: TrustedBackend | None = None) -> None:
        self._mapping = mapping
        self._fallback = fallback

    def resolve(self, plane: str, target_id: str) -> TrustedBackend:
        key = (plane, target_id)
        backend = self._mapping.get(key)
        if backend is not None:
            return backend
        if self._fallback is not None:
            return self._fallback
        raise KeyError(f"no backend for plane={plane}, target_id={target_id}")
