from __future__ import annotations

from typing import Any

from .common import handle_trusted_request


def trusted_server_once(adapter: Any, policy: dict[str, Any]) -> None:
    req = adapter.recv_request()
    resp = handle_trusted_request(req, policy)
    adapter.persist_evidence({"req": req, "resp": resp})
    adapter.send_decision(resp)
