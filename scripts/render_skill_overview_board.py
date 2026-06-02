#!/usr/bin/env python3
"""Render a fixed three-zone skill overview board spec from normalized guide spec."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


DEFAULT_PROGRESS_ITEMS = [
    "描述场景",
    "澄清需求",
    "检查可复用来源",
    "判断 simple / complex",
    "生成 plan",
    "确认 plan",
    "开发与验证",
    "最终验收",
    "生成飞书指南/画板",
    "输出 Agent 安装包",
]

DEFAULT_HIGHLIGHTS = ["确认 plan", "最终验收"]


def build_board_spec(normalized: dict) -> dict:
    embedded = normalized.get("embedded_board", {})
    return {
        "board_type": "skill-overview-board",
        "audience": embedded.get("audience", "end-user"),
        "placement": embedded.get("placement", {}),
        "title": normalized.get("skill_name", "未命名技能"),
        "subtitle": normalized.get("summary", "暂无简介"),
        "zones": [
            {
                "id": "when-to-use",
                "title": "什么时候使用这个技能",
                "items": normalized.get("scenarios", []),
            },
            {
                "id": "how-it-works",
                "title": "它会怎么帮你推进",
                "items": DEFAULT_PROGRESS_ITEMS,
            },
            {
                "id": "deliverables",
                "title": "最终交付物",
                "items": normalized.get("outputs", []),
            },
        ],
        "highlights": DEFAULT_HIGHLIGHTS,
    }


def render_template(skill_root: Path, board_spec: dict) -> str:
    template = (skill_root / "assets/templates/chart/skill-overview-board.json.tpl").read_text(encoding="utf-8")
    return template.format(
        audience=board_spec["audience"],
        placement=json.dumps(board_spec["placement"], ensure_ascii=False),
        title=board_spec["title"],
        subtitle=board_spec["subtitle"],
        when_to_use_items=json.dumps(board_spec["zones"][0]["items"], ensure_ascii=False),
        how_it_works_items=json.dumps(board_spec["zones"][1]["items"], ensure_ascii=False),
        deliverables_items=json.dumps(board_spec["zones"][2]["items"], ensure_ascii=False),
        highlights=json.dumps(board_spec["highlights"], ensure_ascii=False),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("normalized_spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec_path = Path(args.normalized_spec).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parents[1]

    normalized = json.loads(spec_path.read_text(encoding="utf-8"))
    board_spec = build_board_spec(normalized)
    rendered = render_template(skill_root, board_spec)
    parsed = json.loads(rendered)

    (out_dir / "skill-overview-board.json").write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "skill-overview-board.manifest.json").write_text(
        json.dumps(
            {
                "board_type": parsed["board_type"],
                "deliverable": "skill-overview-board.json",
                "zone_count": len(parsed.get("zones", [])),
                "highlight_count": len(parsed.get("highlights", [])),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(out_dir / "skill-overview-board.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
