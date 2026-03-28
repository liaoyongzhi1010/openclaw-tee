from __future__ import annotations

from shcua_prototype.backends.mock_backend import MockTrustedBackend
from shcua_prototype.config import load_policy_config
from shcua_prototype.openclaw_integration.gate import guarded_tool_invoke


def test_guarded_tool_invoke_uses_trusted_backend_for_exec() -> None:
    result = guarded_tool_invoke(
        tool_name="run_command",
        tool_args={
            "command": "ls -la",
            "plane": "main",
            "target_id": "local_tdx",
            "tee_type": "tdx",
        },
        session_id="session_exec_001",
        backend=MockTrustedBackend("tdx"),
        policy=load_policy_config(),
    )

    assert result["status"] == "ok"
    assert result["decision"]["decision"] == "trusted"
    assert result["backend"] == "tdx"
    assert result["trusted_request"]["plane"] == "main"
    assert result["trusted_request"]["target_id"] == "local_tdx"


def test_guarded_tool_invoke_denies_protected_prefix() -> None:
    result = guarded_tool_invoke(
        tool_name="edit_file",
        tool_args={
            "path": "/root/.ssh/config",
            "outside_workspace": True,
        },
        session_id="session_deny_001",
        backend=None,
        policy=load_policy_config(),
    )

    assert result["status"] == "denied"
    assert result["decision"]["decision"] == "deny"
    assert result["operation"]["obj"] == "/root/.ssh/config"
