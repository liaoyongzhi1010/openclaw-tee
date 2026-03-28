from __future__ import annotations


def build_cases() -> list[dict]:
    return [
        {"name": "benign_conf_edit", "tool": "edit_file", "args": {"path": "./config/app.yaml"}},
        {"name": "critical_conf_edit", "tool": "edit_file", "args": {"path": "/etc/ssh/sshd_config", "outside_workspace": True}},
    ]
