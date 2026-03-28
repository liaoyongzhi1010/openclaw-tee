from __future__ import annotations

import hashlib
import json
import os
import uuid
from typing import Any


def normalize_path(path: str) -> str:
    return os.path.normpath(path)


def stable_hash(data: dict[str, Any]) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"
