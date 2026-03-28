from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OperationInstance:
    """Operation model: O = <subj, act, obj, ctx, eff>."""

    subj: str
    act: str
    obj: str
    ctx: dict[str, Any] = field(default_factory=dict)
    eff: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "subj": self.subj,
            "act": self.act,
            "obj": self.obj,
            "ctx": self.ctx,
            "eff": self.eff,
        }
