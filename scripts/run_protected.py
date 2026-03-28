from __future__ import annotations

from shcua_prototype.evaluation.runner import run_cases
from shcua_prototype.workloads.protected_config_modification import build_cases


class MockTrustedBackend:
    def initialize(self) -> None:
        pass

    def send_request(self, req: dict) -> dict:
        return {"allow": req.get("level") != "critical", "constraints": {"target": req.get("obj")}}

    def name(self) -> str:
        return "mock_trusted"


if __name__ == "__main__":
    policy = {
        "risk_thresholds": {"low": 0, "medium": 25, "high": 50, "critical": 80},
        "level_to_decision": {"low": "direct", "medium": "notify", "high": "trusted", "critical": "deny"},
    }
    metrics = run_cases(
        build_cases(),
        session_id="protected_session",
        policy=policy,
        backend=MockTrustedBackend(),
        protected=True,
    )
    print(metrics.as_dict())
