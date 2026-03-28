# SHCUA Prototype Skeleton

This prototype now supports the scenario:

- Centralized OpenClaw orchestrator on server side
- Distributed trusted endpoints (TDX local, TrustZone board, Keystone board)
- Parallel SEV plane for mirrored comparison

Core model chain:

`OperationInstance -> RiskAssessment -> EnforcementDecision -> TrustedRequest`

## Implemented core path

- `core/operation.py`
- `core/risk.py`
- `core/decision.py`
- `core/request.py`
- `openclaw_integration/mapper.py`
- `openclaw_integration/gate.py`

## Distributed orchestration additions

- `openclaw_integration/router.py`
- `openclaw_integration/backend_factory.py`
- `configs/deployment_planes.yaml`
- `backends/http_backend.py`
- `scripts/run_distributed_demo.py`

## Notes

- `gate.guarded_tool_invoke` now supports backend dynamic resolution by `(plane, target_id)`.
- `TrustedRequest` now carries `target_id`, `tee_type`, and `plane` to align with cross-platform routing and audit.
- TDX/SEV transport backends are still stubs for real vsock integration.
