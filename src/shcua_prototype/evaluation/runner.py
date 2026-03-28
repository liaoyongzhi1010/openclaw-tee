from __future__ import annotations

from typing import Any

from shcua_prototype.backends.base import TrustedBackend
from shcua_prototype.evaluation.metrics import Metrics
from shcua_prototype.evaluation.timer import Timer
from shcua_prototype.openclaw_integration.gate import guarded_tool_invoke


def run_workload_case(
    case: dict[str, Any],
    session_id: str,
    policy: dict[str, Any],
    backend: TrustedBackend | None = None,
    protected: bool = False,
) -> tuple[dict[str, Any], int]:
    with Timer() as t:
        result = guarded_tool_invoke(
            tool_name=case["tool"],
            tool_args=case.get("args", {}),
            session_id=session_id,
            backend=backend if protected else None,
            policy=policy,
        )
    return result, int(t.elapsed_ms)


def run_cases(
    cases: list[dict[str, Any]],
    session_id: str,
    policy: dict[str, Any],
    backend: TrustedBackend | None = None,
    protected: bool = False,
) -> Metrics:
    m = Metrics()
    for case in cases:
        result, elapsed_ms = run_workload_case(case, session_id, policy, backend=backend, protected=protected)
        m.total += 1
        m.end_to_end_ms.append(elapsed_ms)
        if result.get("status") in {"ok", "success"}:
            m.success += 1
        if result.get("status") == "denied":
            m.denied += 1
        decision = result.get("decision", {})
        if decision.get("need_notification"):
            m.notified += 1
    return m
