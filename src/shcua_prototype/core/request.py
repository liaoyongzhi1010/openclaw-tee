from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from .decision import EnforcementDecision
from .operation import OperationInstance
from .risk import RiskAssessment


@dataclass(slots=True)
class TrustedRequest:
    req_id: str
    sid: str
    act: str
    obj: str
    scope: dict[str, Any]
    ctx: dict[str, Any]
    level: str
    seq: int
    ttl_ms: int
    target_id: str
    tee_type: str
    plane: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "req_id": self.req_id,
            "sid": self.sid,
            "act": self.act,
            "obj": self.obj,
            "scope": self.scope,
            "ctx": self.ctx,
            "level": self.level,
            "seq": self.seq,
            "ttl_ms": self.ttl_ms,
            "target_id": self.target_id,
            "tee_type": self.tee_type,
            "plane": self.plane,
            "payload": self.payload,
        }


def build_trusted_request(
    op: OperationInstance,
    risk: RiskAssessment,
    decision: EnforcementDecision,
    seq: int,
    ttl_ms: int,
) -> TrustedRequest:
    if not decision.need_trusted_path:
        raise ValueError("trusted request can only be built for trusted-path decisions")

    sid = str(op.ctx.get("session_id") or op.ctx.get("sid") or "anonymous")
    req_id = str(uuid.uuid4())

    target_id = str(op.ctx.get("target_id", "local"))
    tee_type = str(op.ctx.get("tee_type", "unknown"))
    plane = str(op.ctx.get("plane", "main"))

    scope = {
        "target": op.obj,
        "action": op.act,
        "restrictions": {
            "allow_outside_workspace": bool(op.ctx.get("outside_workspace", False)),
            "max_file_size_kb": int(op.ctx.get("max_file_size_kb", 1024)),
        },
    }

    payload = {
        "op": op.to_dict(),
        "risk": risk.to_dict(),
        "decision": decision.to_dict(),
    }

    return TrustedRequest(
        req_id=req_id,
        sid=sid,
        act=op.act,
        obj=op.obj,
        scope=scope,
        ctx=dict(op.ctx),
        level=risk.level,
        seq=int(seq),
        ttl_ms=int(ttl_ms),
        target_id=target_id,
        tee_type=tee_type,
        plane=plane,
        payload=payload,
    )
