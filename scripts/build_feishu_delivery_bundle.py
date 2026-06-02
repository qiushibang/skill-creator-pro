#!/usr/bin/env python3
"""Build the built-in Feishu delivery bundle: guide + board + command plan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_lark_doc_commands import (
    build_board_commands,
    build_create_command,
    build_update_commands,
    render_markdown as render_command_markdown,
)
from render_lark_guide import build_action_plan, build_normalized_spec, render_markdown
from render_skill_overview_board import build_board_spec, render_template


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    out_dir = Path(args.out_dir).resolve()
    guide_dir = out_dir / "guide"
    board_dir = out_dir / "board"
    commands_dir = out_dir / "guide-commands"
    guide_dir.mkdir(parents=True, exist_ok=True)
    board_dir.mkdir(parents=True, exist_ok=True)
    commands_dir.mkdir(parents=True, exist_ok=True)

    skill_root = Path(__file__).resolve().parents[1]
    template = (skill_root / "assets/templates/guide/feishu-guide-template.md").read_text(encoding="utf-8")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    markdown = render_markdown(template, spec)
    normalized = build_normalized_spec(spec, markdown)
    action_plan = build_action_plan(normalized)

    (guide_dir / "feishu-guide.md").write_text(markdown, encoding="utf-8")
    (guide_dir / "feishu-create-payload.json").write_text(
        json.dumps({"title": normalized["title"], "markdown": markdown}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (guide_dir / "guide-spec.normalized.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (guide_dir / "feishu-action-plan.json").write_text(
        json.dumps(action_plan, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    board_spec = build_board_spec(normalized)
    board_json = json.loads(render_template(skill_root, board_spec))
    (board_dir / "skill-overview-board.json").write_text(
        json.dumps(board_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (board_dir / "skill-overview-board.manifest.json").write_text(
        json.dumps(
            {
                "board_type": board_spec["board_type"],
                "deliverable": "skill-overview-board.json",
                "source": "built-in-delivery-bundle",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    command_plan = {
        "create": build_create_command(action_plan["create"]),
        "update": build_update_commands(action_plan.get("update")),
        "board": build_board_commands(action_plan.get("board")),
    }
    (commands_dir / "lark-doc-commands.json").write_text(
        json.dumps(command_plan, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (commands_dir / "lark-doc-commands.md").write_text(
        render_command_markdown(command_plan), encoding="utf-8"
    )

    manifest = {
        "modules": {
            "clarification": "built-in",
            "execution": "built-in",
            "lark_delivery": "built-in",
            "chart_delivery": "built-in",
        },
        "deliverables": {
            "guide_markdown": str((guide_dir / "feishu-guide.md").relative_to(out_dir)),
            "normalized_spec": str((guide_dir / "guide-spec.normalized.json").relative_to(out_dir)),
            "action_plan": str((guide_dir / "feishu-action-plan.json").relative_to(out_dir)),
            "board_spec": str((board_dir / "skill-overview-board.json").relative_to(out_dir)),
            "command_plan": str((commands_dir / "lark-doc-commands.json").relative_to(out_dir)),
        },
    }
    (out_dir / "delivery-bundle.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(out_dir / "delivery-bundle.manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
