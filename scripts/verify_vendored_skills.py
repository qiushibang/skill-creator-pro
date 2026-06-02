#!/usr/bin/env python3
"""Verify that all skill docs/resources claimed as vendored are present locally."""
from __future__ import annotations

import json
from pathlib import Path


REQUIRED = [
    "references/brainstorming/SKILL.md",
    "references/find-skills/SKILL.md",
    "references/planning-with-files/SKILL.md",
    "references/skill-creator-vendor/SKILL.md",
    "references/system-skill-creator/SKILL.md",
    "references/design-lark-chart/SKILL.md",
    "references/lark-doc/SKILL.md",
    "references/lark-whiteboard/SKILL.md",
    "references/lark-shared/SKILL.md",
    "references/lark-openapi-explorer/SKILL.md",
    "references/lark-skill-maker/SKILL.md",
    "references/superpowers/writing-plans/SKILL.md",
    "references/superpowers/executing-plans/SKILL.md",
    "references/superpowers/test-driven-development/SKILL.md",
    "references/superpowers/verification-before-completion/SKILL.md",
    "references/superpowers/requesting-code-review/SKILL.md",
    "references/superpowers/requesting-code-review/code-reviewer.md",
    "references/superpowers/brainstorming/visual-companion.md",
    "references/superpowers/using-superpowers/SKILL.md",
    "references/superpowers/README.md",
    "references/design-lark-chart/01-pipeline.md",
    "references/lark-doc/lark-doc-create.md",
    "references/lark-whiteboard/schema.md",
    "scripts/lark_vendor/explore_openapi_contract.py",
    "scripts/lark_vendor/build_lark_skill_spec.py",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = {rel: (root / rel).exists() for rel in REQUIRED}
    out = root / "reports" / "vendored-skills-verification.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    return 0 if all(result.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
