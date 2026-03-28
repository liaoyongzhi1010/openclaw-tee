from __future__ import annotations

from shcua_prototype.config import load_deployment_config


def main() -> None:
    config = load_deployment_config()
    for plane_name, plane_cfg in config.get("planes", {}).items():
        for target_id, target_cfg in plane_cfg.get("targets", {}).items():
            backend = target_cfg.get("backend", "unknown")
            print(f"planned backend-matrix case: plane={plane_name} target={target_id} backend={backend}")


if __name__ == "__main__":
    main()
