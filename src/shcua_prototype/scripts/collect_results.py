from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    out = Path("results")
    out.mkdir(exist_ok=True)
    summary = {"note": "TODO: aggregate baseline/protected/backend-matrix outputs"}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
