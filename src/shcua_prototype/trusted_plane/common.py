from __future__ import annotations

from typing import Any


def handle_trusted_request(req: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    ttl_ms = int(req.get("ttl_ms", 0))
    if ttl_ms <= 0:
        return {"allow": False, "reason": "invalid ttl_ms", "constraints": {}}

    deny_levels = set(policy.get("deny_levels", ["critical"]))
    level = str(req.get("level", "low"))
    if level in deny_levels:
        return {"allow": False, "reason": f"level denied: {level}", "constraints": {}}

    scope = req.get("scope", {})
    return {
        "allow": True,
        "reason": "authorized",
        "constraints": {
            "target": scope.get("target"),
            "action": scope.get("action"),
            "restrictions": scope.get("restrictions", {}),
        },
    }
