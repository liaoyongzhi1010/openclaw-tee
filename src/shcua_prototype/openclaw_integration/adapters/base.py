from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class OpenClawAdapter(ABC):
    @abstractmethod
    def invoke_tool(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
