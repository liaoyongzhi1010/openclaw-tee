from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .operation import OperationInstance
from .risk import RiskAssessment

DEFAULT_LEVEL_TO_DECISION = {
    "low": "direct",
    "medium": "notify",
    "high": "trusted",
    "critical": "deny",
}


@dataclass(slots=True)
class EnforcementDecision:
    decision: str
    need_trusted_path: bool
    need_notification: bool
    rationale: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "need_trusted_path": self.need_trusted_path,
            "need_notification": self.need_notification,
            "rationale": self.rationale,
        }


def derive_decision(
    op: OperationInstance,
    risk: RiskAssessment,
    policy: dict[str, Any],
) -> EnforcementDecision:
    rationale: list[str] = [f"risk level={risk.level}"]
    level_to_decision = policy.get("level_to_decision", DEFAULT_LEVEL_TO_DECISION)

    forced_trusted_actions = set(policy.get("force_trusted_actions", []))
    if op.act in forced_trusted_actions:
        decision = "trusted"
        rationale.append(f"action forced to trusted path: {op.act}")
    else:
        decision = str(level_to_decision.get(risk.level, "trusted"))
        rationale.append(f"decision mapped from level: {risk.level} -> {decision}")

    deny_prefixes = policy.get("deny_object_prefixes", [])
    if any(op.obj.startswith(prefix) for prefix in deny_prefixes):
        decision = "deny"
        rationale.append("object matched deny_object_prefixes")

    need_trusted_path = decision == "trusted"
    need_notification = decision in {"notify", "deny"} or risk.level in set(
        policy.get("notify_levels", ["medium", "high", "critical"])
    )

    return EnforcementDecision(
        decision=decision,
        need_trusted_path=need_trusted_path,
        need_notification=need_notification,
        rationale=rationale,
    )
