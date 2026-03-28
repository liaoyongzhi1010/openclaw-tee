from __future__ import annotations

from typing import Any, Callable, Protocol

from shcua_prototype.core.decision import derive_decision
from shcua_prototype.core.request import build_trusted_request
from shcua_prototype.core.risk import assess_risk
from shcua_prototype.openclaw_integration.mapper import map_tool_call_to_operation


class TrustedBackend(Protocol):
    def initialize(self) -> None: ...

    def send_request(self, req: dict[str, Any]) -> dict[str, Any]: ...

    def name(self) -> str: ...


def _default_direct_executor(tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "ok",
        "mode": "direct",
        "tool_name": tool_name,
        "tool_args": tool_args,
        "note": "default direct executor does not perform real side effects",
    }


def _default_constrained_executor(
    tool_name: str,
    tool_args: dict[str, Any],
    tee_decision: dict[str, Any],
) -> dict[str, Any]:
    allowed = bool(tee_decision.get("allow", False))
    if not allowed:
        return {
            "status": "blocked",
            "mode": "constrained",
            "tool_name": tool_name,
            "reason": tee_decision.get("reason", "TEE denied request"),
            "tee_decision": tee_decision,
        }

    return {
        "status": "ok",
        "mode": "constrained",
        "tool_name": tool_name,
        "tool_args": tool_args,
        "applied_constraints": tee_decision.get("constraints", {}),
        "tee_decision": tee_decision,
        "note": "default constrained executor does not perform real side effects",
    }


def _resolve_backend(
    op_ctx: dict[str, Any],
    backend: TrustedBackend | None,
    backend_resolver: Callable[[str, str], TrustedBackend] | None,
) -> TrustedBackend:
    if backend is not None:
        return backend

    if backend_resolver is None:
        raise ValueError("backend is required when decision needs trusted path")

    plane = str(op_ctx.get("plane", "main"))
    target_id = str(op_ctx.get("target_id", "local_tdx"))
    return backend_resolver(plane, target_id)


def guarded_tool_invoke(
    tool_name: str,
    tool_args: dict[str, Any],
    session_id: str,
    backend: TrustedBackend | None,
    policy: dict[str, Any],
    direct_executor: Callable[[str, dict[str, Any]], dict[str, Any]] | None = None,
    constrained_executor: Callable[[str, dict[str, Any], dict[str, Any]], dict[str, Any]] | None = None,
    backend_resolver: Callable[[str, str], TrustedBackend] | None = None,
    seq: int = 0,
    ttl_ms: int = 5000,
) -> dict[str, Any]:
    """Main model chain: tool call -> O -> rho(O) -> eta(O) -> A."""

    direct_executor = direct_executor or _default_direct_executor
    constrained_executor = constrained_executor or _default_constrained_executor

    op = map_tool_call_to_operation(
        tool_name=tool_name,
        tool_args=tool_args,
        session_id=session_id,
        task_name=str(tool_args.get("task_name", "unknown_task")),
    )

    risk = assess_risk(op, policy)
    decision = derive_decision(op, risk, policy)

    if decision.decision == "deny":
        return {
            "status": "denied",
            "decision": decision.to_dict(),
            "risk": risk.to_dict(),
            "operation": op.to_dict(),
        }

    if decision.decision in {"direct", "notify"} and not decision.need_trusted_path:
        exec_result = direct_executor(tool_name, tool_args)
        return {
            "status": exec_result.get("status", "ok"),
            "execution": exec_result,
            "decision": decision.to_dict(),
            "risk": risk.to_dict(),
            "operation": op.to_dict(),
        }

    selected_backend = _resolve_backend(op.ctx, backend, backend_resolver)

    req = build_trusted_request(
        op=op,
        risk=risk,
        decision=decision,
        seq=seq,
        ttl_ms=ttl_ms,
    )

    tee_resp = selected_backend.send_request(req.to_dict())
    exec_result = constrained_executor(tool_name, tool_args, tee_resp)

    return {
        "status": exec_result.get("status", "ok"),
        "execution": exec_result,
        "trusted_request": req.to_dict(),
        "decision": decision.to_dict(),
        "risk": risk.to_dict(),
        "operation": op.to_dict(),
        "backend": selected_backend.name(),
    }
