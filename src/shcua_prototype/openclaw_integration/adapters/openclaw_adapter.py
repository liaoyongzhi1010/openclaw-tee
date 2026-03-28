from __future__ import annotations

from typing import Any

from .base import OpenClawAdapter


class LocalOpenClawAdapter(OpenClawAdapter):
    def invoke_tool(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Bind this adapter to the real OpenClaw dispatcher hook")
