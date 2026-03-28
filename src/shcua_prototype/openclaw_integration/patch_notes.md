# OpenClaw Integration Notes

- Hook point target: tool dispatcher entry before side effects.
- Intercept each call and route through `guarded_tool_invoke`.
- Preserve original tool schema in `tool_args["raw_args"]` for audit/replay.
