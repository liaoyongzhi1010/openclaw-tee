from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AuditRecord:
    req_id: str
    audit_id: str
    op_summary: dict[str, Any]
    risk_level: str
    decision: str
    result: dict[str, Any]
    ts_ms: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "req_id": self.req_id,
            "audit_id": self.audit_id,
            "op_summary": self.op_summary,
            "risk_level": self.risk_level,
            "decision": self.decision,
            "result": self.result,
            "ts_ms": self.ts_ms,
        }
