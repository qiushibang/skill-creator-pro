#!/usr/bin/env python3
"""Initialize built-in execution state for the autobuilder workflow."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_PHASES = [
    {"id": "clarification", "label": "需求澄清", "status": "pending"},
    {"id": "planning", "label": "计划生成", "status": "pending"},
    {"id": "gate_1", "label": "闸门 1：plan 确认", "status": "pending"},
    {"id": "implementation", "label": "开发与验证", "status": "pending"},
    {"id": "gate_2", "label": "闸门 2：最终验收", "status": "pending"},
    {"id": "delivery", "label": "飞书图文交付与打包", "status": "pending"},
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--goal", default="待补充目标")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    state = {
        "goal": args.goal,
        "current_phase": "clarification",
        "phases": DEFAULT_PHASES,
        "history": [],
        "gates": {
            "gate_1": {"approved": False, "summary_path": None},
            "gate_2": {"approved": False, "summary_path": None},
        },
    }
    phase = state["phases"][0]
    phase["status"] = "in_progress"
    state_path = workspace / "execution-state.json"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(state_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
