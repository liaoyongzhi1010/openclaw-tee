from __future__ import annotations


def build_cases() -> list[dict]:
    return [
        {"name": "list_workspace", "tool": "list_files", "args": {"path": "./"}},
        {"name": "sort_docs", "tool": "move_file", "args": {"path": "./docs/a.md", "destination": "./docs/archive/a.md"}},
    ]
