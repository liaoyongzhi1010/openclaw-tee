from __future__ import annotations

from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionType(str, Enum):
    DIRECT = "direct"
    TRUSTED = "trusted"
    NOTIFY = "notify"
    DENY = "deny"


class ActionType(str, Enum):
    READ = "read"
    MODIFY = "modify"
    DELETE = "delete"
    EXEC = "exec"
    EXPORT = "export"
