from __future__ import annotations

from typing import Any

from shcua_prototype.backends.base import TrustedBackend
from shcua_prototype.backends.mock_backend import MockTrustedBackend
from shcua_prototype.config import load_deployment_config, load_policy_config
from shcua_prototype.openclaw_integration.backend_factory import build_router_from_config
from shcua_prototype.openclaw_integration.gate import guarded_tool_invoke


def _build_demo_backend(entry: dict[str, Any]) -> TrustedBackend:
    return MockTrustedBackend(backend_name=str(entry.get("backend", "mock_trusted")))


def main() -> None:
    router = build_router_from_config(
        load_deployment_config(),
        backend_builder=_build_demo_backend,
    )

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
        policy=load_policy_config(),
    )

    print(
        {
            "status": result.get("status"),
            "backend": result.get("backend"),
            "target_id": result.get("trusted_request", {}).get("target_id"),
            "plane": result.get("trusted_request", {}).get("plane"),
        }
    )


if __name__ == "__main__":
    main()
