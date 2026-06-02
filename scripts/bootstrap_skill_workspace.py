#!/usr/bin/env python3
"""Instantiate planning templates into a task workspace."""
from __future__ import annotations
import argparse
from pathlib import Path

TEMPLATES = {
    "task_plan.md": "assets/templates/task_plan.md",
    "findings.md": "assets/templates/findings.md",
    "progress.md": "assets/templates/progress.md",
    "clarification-summary.md": "assets/templates/clarification-summary.md",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Target workspace directory")
    parser.add_argument("--skill-root", default=Path(__file__).resolve().parents[1], help="Skill root")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve()
    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    for name, rel in TEMPLATES.items():
        src = skill_root / rel
        dst = workspace / name
        if not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"created {dst}")
        else:
            print(f"exists {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
