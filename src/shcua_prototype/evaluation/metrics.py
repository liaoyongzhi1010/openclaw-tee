from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Metrics:
    total: int = 0
    success: int = 0
    denied: int = 0
    notified: int = 0
    end_to_end_ms: list[int] = field(default_factory=list)
    trusted_rtt_ms: list[int] = field(default_factory=list)

    def as_dict(self) -> dict:
        avg = lambda xs: (sum(xs) / len(xs)) if xs else 0.0
        return {
            "total": self.total,
            "success": self.success,
            "denied": self.denied,
            "notified": self.notified,
            "avg_e2e_ms": avg(self.end_to_end_ms),
            "avg_trusted_rtt_ms": avg(self.trusted_rtt_ms),
        }
