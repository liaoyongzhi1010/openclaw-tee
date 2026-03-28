# SHCUA Prototype Skeleton

This prototype now supports the scenario:

- Centralized OpenClaw orchestrator on server side
- Distributed trusted endpoints (TDX local, TrustZone board, Keystone board)
- Parallel SEV plane for mirrored comparison

Core model chain:

`OperationInstance -> RiskAssessment -> EnforcementDecision -> TrustedRequest`

## Implemented core path

- `src/shcua_prototype/core/operation.py`
- `src/shcua_prototype/core/risk.py`
- `src/shcua_prototype/core/decision.py`
- `src/shcua_prototype/core/request.py`
- `src/shcua_prototype/openclaw_integration/mapper.py`
- `src/shcua_prototype/openclaw_integration/gate.py`

## Distributed orchestration additions

- `src/shcua_prototype/openclaw_integration/router.py`
- `src/shcua_prototype/openclaw_integration/backend_factory.py`
- `src/shcua_prototype/configs/deployment_planes.yaml`
- `src/shcua_prototype/backends/http_backend.py`
- `src/shcua_prototype/scripts/run_distributed_demo.py`

## Notes

- `gate.guarded_tool_invoke` now supports backend dynamic resolution by `(plane, target_id)`.
- `TrustedRequest` now carries `target_id`, `tee_type`, and `plane` to align with cross-platform routing and audit.
- TDX/SEV transport backends are still stubs for real vsock integration.

## Setup

Create and activate a virtual environment, then install the local package:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Layout

- `src/shcua_prototype/core`: operation, risk, decision, and trusted-request domain models
- `src/shcua_prototype/openclaw_integration`: tool-call mapping, routing, and backend selection
- `src/shcua_prototype/backends`: transport backends, including HTTP, vsock stubs, and mock backend
- `src/shcua_prototype/trusted_plane`: trusted-side request handling
- `src/shcua_prototype/workloads`: example workload cases
- `src/shcua_prototype/configs`: packaged YAML policy and deployment config
- `tests`: basic regression coverage for config loading and guarded execution flow

## Run

Recommended entry points:

```bash
python -m shcua_prototype.scripts.run_baseline
python -m shcua_prototype.scripts.run_protected
python -m shcua_prototype.scripts.run_distributed_demo
```

## Test

```bash
python -m pytest
```
