from __future__ import annotations

from typing import Any

from .operation import OperationInstance


def execute_direct(op: OperationInstance) -> dict[str, Any]:
    return {"status": "ok", "mode": "direct", "op": op.to_dict()}


def execute_constrained(op: OperationInstance, decision_resp: dict[str, Any]) -> dict[str, Any]:
    if not decision_resp.get("allow", False):
        return {
            "status": "blocked",
            "mode": "constrained",
            "op": op.to_dict(),
            "reason": decision_resp.get("reason", "TEE denied"),
        }
    return {
        "status": "ok",
        "mode": "constrained",
        "op": op.to_dict(),
        "constraints": decision_resp.get("constraints", {}),
    }
