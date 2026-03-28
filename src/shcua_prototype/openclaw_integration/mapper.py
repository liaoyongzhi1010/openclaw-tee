from __future__ import annotations

from typing import Any

from shcua_prototype.core.operation import OperationInstance


def _resolve_action(tool_name: str, tool_args: dict[str, Any]) -> str:
    name = tool_name.lower()
    if any(k in name for k in ["read", "cat", "view", "list", "ls"]):
        return "read"
    if any(k in name for k in ["write", "edit", "update", "patch"]):
        return "modify"
    if any(k in name for k in ["delete", "remove", "rm"]):
        return "delete"
    if any(k in name for k in ["exec", "shell", "command", "run"]):
        return "exec"
    if any(k in name for k in ["export", "upload", "send"]):
        return "export"

    if "command" in tool_args:
        return "exec"
    return "modify"


def _resolve_object(tool_args: dict[str, Any], fallback: str) -> str:
    for key in ("path", "file", "filepath", "target", "dst", "destination"):
        value = tool_args.get(key)
        if isinstance(value, str) and value:
            return value
    return fallback


def _resolve_effect(action: str, tool_args: dict[str, Any]) -> dict[str, Any]:
    command = str(tool_args.get("command", ""))
    exfil_keywords = ("curl", "wget", "scp", "rsync", "nc", "ftp")

    return {
        "persistence": action in {"modify", "delete"},
        "exfiltration": action == "export" or any(k in command for k in exfil_keywords),
        "privilege_escalation": "sudo" in command or "chmod 777" in command,
    }


def map_tool_call_to_operation(
    tool_name: str,
    tool_args: dict[str, Any],
    session_id: str,
    task_name: str,
) -> OperationInstance:
    act = _resolve_action(tool_name, tool_args)
    obj = _resolve_object(tool_args, fallback=f"tool:{tool_name}")
    eff = _resolve_effect(act, tool_args)

    ctx: dict[str, Any] = {
        "session_id": session_id,
        "task_name": task_name,
        "tool_name": tool_name,
        "outside_workspace": bool(tool_args.get("outside_workspace", False)),
        "untrusted_source": bool(tool_args.get("untrusted_source", False)),
        "interactive_confirmed": tool_args.get("interactive_confirmed", True),
        "target_id": str(tool_args.get("target_id", "local_tdx")),
        "tee_type": str(tool_args.get("tee_type", "tdx")),
        "plane": str(tool_args.get("plane", "main")),
        "raw_args": dict(tool_args),
    }

    return OperationInstance(
        subj=session_id,
        act=act,
        obj=obj,
        ctx=ctx,
        eff=eff,
    )
