#!/usr/bin/env python3
"""Render a built-in clarification summary before planning or implementation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def bullet(items: list[str], empty: str = "- 暂无") -> str:
    if not items:
        return empty
    return "\n".join(f"- {item}" for item in items)


def infer_scope(spec: dict) -> str:
    dependencies = " ".join(as_list(spec.get("dependencies"))).lower()
    outputs = " ".join(as_list(spec.get("outputs"))).lower()
    request = " ".join(
        [
            str(spec.get("request", "")),
            str(spec.get("goal", "")),
            " ".join(as_list(spec.get("constraints"))),
        ]
    ).lower()
    complex_tokens = (
        "lark",
        "feishu",
        "openapi",
        "图",
        "whiteboard",
        "board",
        "doc",
        "文档",
        "guide",
        "diagram",
        "chart",
    )
    if any(token in dependencies or token in outputs or token in request for token in complex_tokens):
        return "complex"
    return spec.get("scope", "simple")


def build_normalized(spec: dict) -> dict:
    goal = str(spec.get("goal") or spec.get("request") or "待补充目标").strip()
    target_users = as_list(spec.get("target_users"))
    inputs = as_list(spec.get("inputs"))
    outputs = as_list(spec.get("outputs"))
    dependencies = as_list(spec.get("dependencies"))
    acceptance = as_list(spec.get("acceptance_criteria"))
    constraints = as_list(spec.get("constraints"))
    assumptions = as_list(spec.get("assumptions"))
    open_questions = as_list(spec.get("open_questions"))
    scope = infer_scope(spec)

    if not target_users:
        open_questions.append("目标用户尚未明确，默认按‘最终使用者’处理。")
    if not outputs:
        open_questions.append("最终交付物尚未明确，需确认是仅交付 skill 目录还是同时交付文档/图表/zip。")
    if not acceptance:
        open_questions.append("验收标准尚未明确，需确认以结构校验、示例验证还是端到端结果为准。")

    if not assumptions:
        assumptions.append("若用户未补充更多信息，先按最小可用闭环推进，并在关键闸门等待确认。")
    if not constraints:
        constraints.append("默认遵守 Agent 安装包要求、双确认闸门与未验证不得宣称完成。")

    recommended_path = "complex" if scope == "complex" else "simple"
    needs_visual_delivery = "是" if recommended_path == "complex" else "否"
    next_steps = [
        "将本摘要写入 workspace，并向用户展示已知信息、假设与待确认项。",
        "如仍有关键缺失，最多补 1~3 个高价值问题；否则直接进入计划生成。",
        "在 plan 生成后停在闸门 1，等待用户确认。",
    ]

    return {
        "request": str(spec.get("request") or goal),
        "goal": goal,
        "target_users": target_users or ["最终使用者（默认）"],
        "inputs": inputs or ["待确认输入"],
        "outputs": outputs or ["待确认输出"],
        "dependencies": dependencies or ["无强制依赖（待确认）"],
        "acceptance_criteria": acceptance or ["待确认验收标准"],
        "constraints": constraints,
        "assumptions": assumptions,
        "open_questions": open_questions or ["暂无"],
        "scope": scope,
        "recommended_path": recommended_path,
        "needs_visual_delivery": needs_visual_delivery,
        "next_steps": next_steps,
    }


def render_markdown(template: str, normalized: dict) -> str:
    return template.format(
        request=normalized["request"],
        goal=normalized["goal"],
        target_users=bullet(normalized["target_users"]),
        inputs=bullet(normalized["inputs"]),
        outputs=bullet(normalized["outputs"]),
        dependencies=bullet(normalized["dependencies"]),
        acceptance=bullet(normalized["acceptance_criteria"]),
        constraints=bullet(normalized["constraints"]),
        assumptions=bullet(normalized["assumptions"]),
        open_questions=bullet(normalized["open_questions"]),
        scope=normalized["scope"],
        recommended_path=normalized["recommended_path"],
        needs_visual_delivery=normalized["needs_visual_delivery"],
        next_steps=bullet(normalized["next_steps"]),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parents[1]
    template = (skill_root / "assets/templates/clarification-summary.md").read_text(encoding="utf-8")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    normalized = build_normalized(spec)
    markdown = render_markdown(template, normalized)

    (out_dir / "clarification-summary.md").write_text(markdown, encoding="utf-8")
    (out_dir / "clarification.normalized.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(out_dir / "clarification-summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
