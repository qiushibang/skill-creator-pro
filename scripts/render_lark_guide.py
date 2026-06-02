#!/usr/bin/env python3
"""Render a Feishu-ready markdown guide and action artifacts from a JSON spec."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


SECTION_ORDER = [
    ("技能简介", "summary", "text"),
    ("适用场景", "scenarios", "bullet"),
    ("触发方式", "triggers", "bullet"),
    ("输入 / 输出", "io", "io"),
    ("使用步骤", "steps", "numbered"),
    ("限制与注意事项", "limitations", "bullet"),
    ("常见问题", "faq", "faq"),
]


def bullet(items):
    if not items:
        return "- 暂无"
    return "\n".join(f"- {item}" for item in items)


def numbered(items):
    if not items:
        return "1. 暂无"
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))


def faq_block(items):
    if not items:
        return "- 暂无"
    blocks = []
    for item in items:
        q = item.get("q", "未命名问题")
        a = item.get("a", "待补充")
        blocks.append(f"- **{q}**\n  - {a}")
    return "\n".join(blocks)


def render_markdown(template: str, spec: dict) -> str:
    return template.format(
        summary=spec.get("summary", "暂无简介"),
        scenarios=bullet(spec.get("scenarios", [])),
        triggers=bullet(spec.get("triggers", [])),
        inputs=bullet(spec.get("inputs", [])),
        outputs=bullet(spec.get("outputs", [])),
        steps=numbered(spec.get("steps", [])),
        limitations=bullet(spec.get("limitations", [])),
        faq=faq_block(spec.get("faq", [])),
    )


def build_embedded_board(normalized: dict) -> dict:
    return {
        "enabled": True,
        "board_type": "skill-overview-board",
        "audience": "end-user",
        "placement": {
            "after_section": "技能简介",
            "mode": "insert_after_section",
        },
        "focus": [
            "how_to_trigger",
            "how_it_progresses",
            "what_user_gets",
        ],
    }


def build_normalized_spec(spec: dict, markdown: str) -> dict:
    feishu = spec.get("feishu", {})
    title = feishu.get("title") or f"{spec.get('skill_name', '未命名技能')} 使用指南"
    normalized = {
        "skill_name": spec.get("skill_name", "未命名技能"),
        "title": title,
        "summary": spec.get("summary", "暂无简介"),
        "scenarios": spec.get("scenarios", []),
        "triggers": spec.get("triggers", []),
        "inputs": spec.get("inputs", []),
        "outputs": spec.get("outputs", []),
        "steps": spec.get("steps", []),
        "limitations": spec.get("limitations", []),
        "faq": spec.get("faq", []),
        "markdown": markdown,
        "sections": build_sections(spec),
        "feishu": {
            "title": title,
            "folder_token": feishu.get("folder_token"),
            "wiki_node": feishu.get("wiki_node"),
            "wiki_space": feishu.get("wiki_space"),
            "doc_id": feishu.get("doc_id"),
            "chunk_limit": int(feishu.get("chunk_limit", 1500)),
        },
    }
    normalized["embedded_board"] = build_embedded_board({
        "skill_name": normalized["skill_name"],
        "summary": normalized["summary"],
        "scenarios": normalized["scenarios"],
        "triggers": normalized["triggers"],
        "outputs": normalized["outputs"],
        "steps": normalized["steps"],
    })
    return normalized


def build_sections(spec: dict) -> list[dict]:
    sections = []
    for title, key, kind in SECTION_ORDER:
        if kind == "text":
            body = spec.get(key, "暂无简介")
        elif kind == "bullet":
            body = bullet(spec.get(key, []))
        elif kind == "numbered":
            body = numbered(spec.get(key, []))
        elif kind == "faq":
            body = faq_block(spec.get(key, []))
        elif kind == "io":
            body = "### 输入\n{inputs}\n\n### 输出\n{outputs}".format(
                inputs=bullet(spec.get("inputs", [])),
                outputs=bullet(spec.get("outputs", [])),
            )
        else:
            body = ""
        sections.append({"title": title, "markdown": f"## {title}\n\n{body}".strip()})
    return sections


def split_sections(sections: list[dict], chunk_limit: int) -> list[dict]:
    chunks = []
    current_parts = []
    current_titles = []
    current_len = 0
    for section in sections:
        text = section["markdown"].strip() + "\n"
        if current_parts and current_len + len(text) > chunk_limit:
            chunks.append({
                "section_titles": current_titles[:],
                "markdown": "\n\n".join(current_parts).strip(),
            })
            current_parts = []
            current_titles = []
            current_len = 0
        current_parts.append(section["markdown"].strip())
        current_titles.append(section["title"])
        current_len += len(text)
    if current_parts:
        chunks.append({
            "section_titles": current_titles[:],
            "markdown": "\n\n".join(current_parts).strip(),
        })
    return chunks


def build_action_plan(normalized: dict) -> dict:
    feishu = normalized["feishu"]
    create = {
        "title": feishu["title"],
        "markdown": normalized["markdown"],
    }
    for key in ("folder_token", "wiki_node", "wiki_space"):
        if feishu.get(key):
            create[key] = feishu[key]

    update = None
    if feishu.get("doc_id"):
        chunks = split_sections(normalized["sections"], max(80, feishu["chunk_limit"]))
        update = {
            "doc": feishu["doc_id"],
            "mode": "append",
            "chunks": [
                {
                    "index": idx,
                    "section_titles": chunk["section_titles"],
                    "markdown": chunk["markdown"],
                }
                for idx, chunk in enumerate(chunks, 1)
            ],
        }
    return {
        "create": create,
        "update": update,
        "board": {
            "enabled": True,
            "board_type": "skill-overview-board",
            "placement": {
                "after_section": "技能简介",
                "doc": feishu.get("doc_id"),
                "mode": "insert_after_section",
            },
            "insert_markdown": "<whiteboard type=\"blank\"></whiteboard>",
            "board_spec_path": "board/skill-overview-board.json",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parents[1]
    template = (skill_root / "assets/templates/guide/feishu-guide-template.md").read_text(encoding="utf-8")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    markdown = render_markdown(template, spec)
    normalized = build_normalized_spec(spec, markdown)
    action_plan = build_action_plan(normalized)

    title = normalized["title"]
    (out_dir / "feishu-guide.md").write_text(markdown, encoding="utf-8")
    (out_dir / "feishu-create-payload.json").write_text(
        json.dumps({"title": title, "markdown": markdown}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "guide-spec.normalized.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "feishu-action-plan.json").write_text(
        json.dumps(action_plan, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(out_dir / "feishu-guide.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
