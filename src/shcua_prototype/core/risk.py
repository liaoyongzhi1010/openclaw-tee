from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .operation import OperationInstance


DEFAULT_LEVEL_THRESHOLDS = {
    "low": 0,
    "medium": 25,
    "high": 50,
    "critical": 80,
}

DEFAULT_ACTION_SCORES = {
    "read": 5,
    "list": 5,
    "write": 25,
    "modify": 40,
    "delete": 65,
    "exec": 70,
    "export": 80,
    "network": 60,
}


@dataclass(slots=True)
class RiskAssessment:
    level: str
    action_score: int
    object_score: int
    context_score: int
    effect_score: int
    reasons: list[str] = field(default_factory=list)

    @property
    def total_score(self) -> int:
        return self.action_score + self.object_score + self.context_score + self.effect_score

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "action_score": self.action_score,
            "object_score": self.object_score,
            "context_score": self.context_score,
            "effect_score": self.effect_score,
            "total_score": self.total_score,
            "reasons": self.reasons,
        }


def _score_object(obj: str, policy: dict[str, Any], reasons: list[str]) -> int:
    score = 0
    for rule in policy.get("object_rules", []):
        prefix = str(rule.get("prefix", ""))
        bonus = int(rule.get("score", 0))
        if prefix and obj.startswith(prefix):
            score += bonus
            reasons.append(f"object matched protected prefix: {prefix} (+{bonus})")
    return score


def _score_context(op: OperationInstance, policy: dict[str, Any], reasons: list[str]) -> int:
    score = 0
    ctx = op.ctx or {}

    if ctx.get("outside_workspace"):
        bonus = int(policy.get("context_scores", {}).get("outside_workspace", 25))
        score += bonus
        reasons.append(f"context outside workspace (+{bonus})")

    if ctx.get("untrusted_source"):
        bonus = int(policy.get("context_scores", {}).get("untrusted_source", 20))
        score += bonus
        reasons.append(f"context untrusted source (+{bonus})")

    if ctx.get("interactive_confirmed") is False:
        bonus = int(policy.get("context_scores", {}).get("no_user_confirmation", 10))
        score += bonus
        reasons.append(f"context no user confirmation (+{bonus})")

    return score


def _score_effect(op: OperationInstance, policy: dict[str, Any], reasons: list[str]) -> int:
    score = 0
    eff = op.eff or {}

    if eff.get("persistence"):
        bonus = int(policy.get("effect_scores", {}).get("persistence", 15))
        score += bonus
        reasons.append(f"effect persistence (+{bonus})")

    if eff.get("exfiltration"):
        bonus = int(policy.get("effect_scores", {}).get("exfiltration", 35))
        score += bonus
        reasons.append(f"effect exfiltration (+{bonus})")

    if eff.get("privilege_escalation"):
        bonus = int(policy.get("effect_scores", {}).get("privilege_escalation", 35))
        score += bonus
        reasons.append(f"effect privilege escalation (+{bonus})")

    return score


def _resolve_level(total: int, thresholds: dict[str, int]) -> str:
    ordered = sorted(thresholds.items(), key=lambda item: item[1])
    level = "low"
    for label, t in ordered:
        if total >= int(t):
            level = label
    return level


def assess_risk(op: OperationInstance, policy: dict[str, Any]) -> RiskAssessment:
    reasons: list[str] = []
    action_scores = policy.get("action_scores", DEFAULT_ACTION_SCORES)
    thresholds = policy.get("risk_thresholds", DEFAULT_LEVEL_THRESHOLDS)

    action_score = int(action_scores.get(op.act, action_scores.get("modify", 40)))
    reasons.append(f"action={op.act} (+{action_score})")

    object_score = _score_object(op.obj, policy, reasons)
    context_score = _score_context(op, policy, reasons)
    effect_score = _score_effect(op, policy, reasons)

    total = action_score + object_score + context_score + effect_score
    level = _resolve_level(total, thresholds)
    reasons.append(f"total score={total}, resolved level={level}")

    return RiskAssessment(
        level=level,
        action_score=action_score,
        object_score=object_score,
        context_score=context_score,
        effect_score=effect_score,
        reasons=reasons,
    )
