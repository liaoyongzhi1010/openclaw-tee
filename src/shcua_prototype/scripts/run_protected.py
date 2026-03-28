from __future__ import annotations

from shcua_prototype.backends.mock_backend import MockTrustedBackend
from shcua_prototype.config import load_policy_config
from shcua_prototype.evaluation.runner import run_cases
from shcua_prototype.workloads.protected_config_modification import build_cases


def main() -> None:
    metrics = run_cases(
        build_cases(),
        session_id="protected_session",
        policy=load_policy_config(),
        backend=MockTrustedBackend(),
        protected=True,
    )
    print(metrics.as_dict())


if __name__ == "__main__":
    main()
