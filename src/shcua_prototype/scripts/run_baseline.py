from __future__ import annotations

from shcua_prototype.config import build_baseline_policy
from shcua_prototype.evaluation.runner import run_cases
from shcua_prototype.workloads.document_organization import build_cases


def main() -> None:
    metrics = run_cases(
        build_cases(),
        session_id="baseline_session",
        policy=build_baseline_policy(),
        protected=False,
    )
    print(metrics.as_dict())


if __name__ == "__main__":
    main()
