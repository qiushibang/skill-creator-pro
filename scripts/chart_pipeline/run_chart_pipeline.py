#!/usr/bin/env python3
"""Run a built-in, local version of the design-lark-chart pipeline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


CODE_NATIVE_TYPES = {"flowchart", "mindmap", "sequence", "state-machine", "er-diagram"}
SVG_TYPES = {"system-architecture", "matrix-quadrant", "sketch-architecture"}


def infer_chart_type(spec: dict) -> str:
    requested = spec.get("chart_type")
    if requested:
        return requested
    text = " ".join(spec.get("keywords", []) + [spec.get("title", "")]).lower()
    if "sequence" in text or "时序" in text:
        return "sequence"
    if "mind" in text or "导图" in text:
        return "mindmap"
    if "状态" in text:
        return "state-machine"
    return "flowchart"


def normalize(spec: dict) -> dict:
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])
    return {
        "title": spec.get("title", "未命名图表"),
        "summary": spec.get("summary", ""),
        "chart_type": infer_chart_type(spec),
        "nodes": nodes,
        "edges": edges,
        "groups": groups,
        "annotations": spec.get("annotations", []),
    }


def select_route(normalized: dict) -> dict:
    chart_type = normalized["chart_type"]
    if chart_type in CODE_NATIVE_TYPES:
        route = "code-native"
    elif chart_type in SVG_TYPES:
        route = "svg-openapi"
    else:
        route = "dsl"
    return {"chart_type": chart_type, "route": route}


def load_style_budget(skill_root: Path, chart_type: str) -> dict:
    path = skill_root / "assets/style-tokens" / f"{chart_type}.json"
    if not path.exists():
        path = skill_root / "assets/style-tokens" / "_catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "source": str(path.relative_to(skill_root)),
        "raw": data,
    }


def build_plan(normalized: dict, selection: dict, style_budget: dict) -> dict:
    return {
        "version": "1.0",
        "chart_type": selection["chart_type"],
        "title": normalized["title"],
        "subtitle": normalized.get("summary", ""),
        "nodes": normalized.get("nodes", []),
        "groups": normalized.get("groups", []),
        "edges": [
            {
                "from": src,
                "to": dst,
                "label": None,
                "kind": "sequence",
                "semantic": "normal",
            }
            for src, dst in normalized.get("edges", [])
        ],
        "style_budget": style_budget,
        "style_profile": {
            "route_preference": selection["route"],
            "visual_anchor": selection["chart_type"],
            "layout_signature": ["built-in-local-pipeline"],
            "must_have": ["style-tokens"],
            "must_not": ["hardcoded-coordinates", "fabricated-content"],
        },
        "density_hint": {
            "node_count": len(normalized.get("nodes", [])),
            "edge_count": len(normalized.get("edges", [])),
            "group_count": len(normalized.get("groups", [])),
        },
    }


def build_layout(plan: dict) -> dict:
    return {
        "route": plan["style_profile"]["route_preference"],
        "node_count": len(plan.get("nodes", [])),
        "edge_count": len(plan.get("edges", [])),
        "group_count": len(plan.get("groups", [])),
        "layout_signature": ["no-hardcoded-coordinates", "derived-from-node-count"],
    }


def build_render_manifest(selection: dict, plan: dict) -> dict:
    deliverable = {
        "code-native": "diagram.mmd",
        "dsl": "board.json",
        "svg-openapi": "diagram.svg",
    }[selection["route"]]
    return {
        "route": selection["route"],
        "chart_type": selection["chart_type"],
        "deliverable": deliverable,
        "quality_gate_required": True,
    }


def build_static_check(selection: dict, render_manifest: dict) -> dict:
    if selection["route"] == "code-native":
        checks = ["round-trip-code", "feishu-export-image"]
    elif selection["route"] == "svg-openapi":
        checks = ["svg-check", "premium-style-lint", "openapi-convert"]
    else:
        checks = ["whiteboard-cli-check"]
    return {"route": selection["route"], "checks": checks, "blocking": True}


def build_vqa(selection: dict) -> dict:
    return {
        "route": selection["route"],
        "reviewers": 2,
        "threshold": 9,
        "requires_real_feishu_export": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[2]
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    normalized = normalize(spec)
    selection = select_route(normalized)
    style_budget = load_style_budget(skill_root, selection["chart_type"])
    plan = build_plan(normalized, selection, style_budget)
    layout = build_layout(plan)
    render_manifest = build_render_manifest(selection, plan)
    static_check = build_static_check(selection, render_manifest)
    vqa = build_vqa(selection)
    delivery = {
        "deliverable": render_manifest["deliverable"],
        "route": selection["route"],
        "requires_quality_gate": True,
        "requires_degrade_to_text_on_failure": True,
    }

    outputs = {
        "normalized.json": normalized,
        "selection.json": selection,
        "plan.json": plan,
        "layout.json": layout,
        "render-manifest.json": render_manifest,
        "static-check.json": static_check,
        "vqa.json": vqa,
        "delivery.json": delivery,
    }
    for name, data in outputs.items():
        (out_dir / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_dir / "delivery.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
