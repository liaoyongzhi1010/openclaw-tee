from __future__ import annotations

from copy import deepcopy
from importlib.resources import files
from typing import Any

import yaml


def load_yaml_config(filename: str) -> dict[str, Any]:
    resource = files("shcua_prototype").joinpath("configs", filename)
    data = yaml.safe_load(resource.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise TypeError(f"config {filename} must contain a mapping at the top level")
    return data


def load_policy_config() -> dict[str, Any]:
    return load_yaml_config("policy_default.yaml")


def load_deployment_config() -> dict[str, Any]:
    return load_yaml_config("deployment_planes.yaml")


def load_platform_config() -> dict[str, Any]:
    return load_yaml_config("platforms.yaml")


def load_workload_config() -> dict[str, Any]:
    return load_yaml_config("workloads.yaml")


def build_baseline_policy() -> dict[str, Any]:
    policy = deepcopy(load_policy_config())
    levels = policy.get("risk_thresholds", {})
    policy["level_to_decision"] = {str(level): "direct" for level in levels} or {
        "low": "direct",
        "medium": "direct",
        "high": "direct",
        "critical": "direct",
    }
    policy["force_trusted_actions"] = []
    policy["notify_levels"] = []
    policy["deny_object_prefixes"] = []
    return policy
