#!/usr/bin/env python3
"""Build a local quality-gate report for the built-in chart pipeline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pipeline_dir")
    args = parser.parse_args()

    pipeline_dir = Path(args.pipeline_dir).resolve()
    selection = json.loads((pipeline_dir / "selection.json").read_text(encoding="utf-8"))
    static_check = json.loads((pipeline_dir / "static-check.json").read_text(encoding="utf-8"))
    vqa = json.loads((pipeline_dir / "vqa.json").read_text(encoding="utf-8"))

    report = {
        "gate_a": {
            "route": selection["route"],
            "required_checks": static_check["checks"],
            "status": "needs-runtime-verification",
        },
        "gate_b": {
            "reviewers": vqa["reviewers"],
            "threshold": vqa["threshold"],
            "requires_real_feishu_export": vqa["requires_real_feishu_export"],
            "status": "needs-runtime-verification",
        },
        "degrade_rule": "if any blocker or score < 9, degrade to text guide",
    }
    out = pipeline_dir / "quality-gate-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
