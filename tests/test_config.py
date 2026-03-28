from __future__ import annotations

from shcua_prototype.backends.mock_backend import MockTrustedBackend
from shcua_prototype.config import build_baseline_policy, load_deployment_config, load_policy_config
from shcua_prototype.openclaw_integration.backend_factory import build_router_from_config


def test_build_baseline_policy_disables_enforcement() -> None:
    policy = build_baseline_policy()

    assert set(policy["level_to_decision"].values()) == {"direct"}
    assert policy["force_trusted_actions"] == []
    assert policy["notify_levels"] == []
    assert policy["deny_object_prefixes"] == []


def test_load_policy_config_contains_thresholds() -> None:
    policy = load_policy_config()

    assert policy["risk_thresholds"]["critical"] == 80
    assert policy["level_to_decision"]["high"] == "trusted"


def test_build_router_from_config_uses_targets() -> None:
    router = build_router_from_config(
        load_deployment_config(),
        backend_builder=lambda entry: MockTrustedBackend(str(entry["backend"])),
    )

    assert router.resolve("main", "rpi_trustzone").name() == "trustzone"
    assert router.resolve("parallel_sev", "local_sev").name() == "sev"
