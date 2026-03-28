from __future__ import annotations

from shcua_prototype.openclaw_integration.gate import guarded_tool_invoke
from shcua_prototype.openclaw_integration.router import BackendRouter


class MockBackend:
    def __init__(self, backend_name: str) -> None:
        self._backend_name = backend_name

    def initialize(self) -> None:
        pass

    def send_request(self, req: dict) -> dict:
        return {
            "allow": req.get("level") != "critical",
            "constraints": {
                "target_id": req.get("target_id"),
                "plane": req.get("plane"),
            },
        }

    def name(self) -> str:
        return self._backend_name


if __name__ == "__main__":
    router = BackendRouter(
        mapping={
            ("main", "rpi_trustzone"): MockBackend("trustzone"),
            ("main", "u74_keystone"): MockBackend("keystone"),
            ("parallel_sev", "local_sev"): MockBackend("sev"),
        }
    )

    policy = {
        "risk_thresholds": {"low": 0, "medium": 25, "high": 50, "critical": 80},
        "level_to_decision": {"low": "direct", "medium": "notify", "high": "trusted", "critical": "deny"},
    }

    result = guarded_tool_invoke(
        tool_name="run_command",
        tool_args={
            "command": "ls -la",
            "task_name": "board_inspect",
            "plane": "main",
            "target_id": "rpi_trustzone",
            "tee_type": "trustzone",
        },
        session_id="session_main_001",
        backend=None,
        backend_resolver=router.resolve,
        policy=policy,
    )

    print(
        {
            "status": result.get("status"),
            "backend": result.get("backend"),
            "target_id": result.get("trusted_request", {}).get("target_id"),
            "plane": result.get("trusted_request", {}).get("plane"),
        }
    )
