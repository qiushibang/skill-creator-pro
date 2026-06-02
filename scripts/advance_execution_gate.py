#!/usr/bin/env python3
"""Advance built-in execution phases and emit gate summaries."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


GATE_TO_PHASE = {
    "gate_1": ("planning", "gate_1", "implementation"),
    "gate_2": ("implementation", "gate_2", "delivery"),
}


def bullet(items: list[str], empty: str = "- 暂无") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def render_summary(template: str, *, gate_name: str, status: str, current_phase: str, completed_items: list[str], approval_items: list[str], next_steps: list[str]) -> str:
    return template.format(
        gate_name=gate_name,
        status=status,
        current_phase=current_phase,
        completed_items=bullet(completed_items),
        approval_items=bullet(approval_items),
        next_steps=bullet(next_steps),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("gate", choices=["gate_1", "gate_2"])
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--completed-item", action="append", default=[])
    parser.add_argument("--approval-item", action="append", default=[])
    parser.add_argument("--next-step", action="append", default=[])
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    state_path = workspace / "execution-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    _, gate_phase, next_phase = GATE_TO_PHASE[args.gate]
    skill_root = Path(__file__).resolve().parents[1]
    template = (skill_root / "assets/templates/execution/gate-summary.md").read_text(encoding="utf-8")

    for phase in state["phases"]:
        if phase["id"] == gate_phase:
            phase["status"] = "complete" if args.approve else "in_progress"
        elif phase["id"] == next_phase and args.approve:
            phase["status"] = "in_progress"
            state["current_phase"] = next_phase
        elif phase["id"] == state["current_phase"] and phase["id"] != next_phase and args.approve:
            phase["status"] = "complete"

    summary_text = render_summary(
        template,
        gate_name="闸门 1：plan 确认" if args.gate == "gate_1" else "闸门 2：最终验收",
        status="approved" if args.approve else "awaiting_approval",
        current_phase=state["current_phase"],
        completed_items=args.completed_item,
        approval_items=args.approval_item,
        next_steps=args.next_step or (["等待用户确认"] if not args.approve else [f"进入 {next_phase}"]),
    )
    summary_path = workspace / f"{args.gate}-summary.md"
    summary_path.write_text(summary_text, encoding="utf-8")

    state["gates"][args.gate]["approved"] = bool(args.approve)
    state["gates"][args.gate]["summary_path"] = str(summary_path)
    state["history"].append(
        {
            "gate": args.gate,
            "approved": bool(args.approve),
            "summary_path": str(summary_path),
        }
    )
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
