#!/usr/bin/env python3
"""Render a lightweight documentation chart from a JSON spec."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path


def sanitize(node_id: str) -> str:
    val = re.sub(r"[^A-Za-z0-9_]", "_", node_id)
    return val or "node"


def flowchart_body(spec: dict) -> str:
    nodes = []
    seen = set()
    for item in spec.get("nodes", []):
        node_id = sanitize(item["id"])
        label = item.get("label", item["id"])
        if node_id not in seen:
            nodes.append(f'{node_id}[{label}]')
            seen.add(node_id)
    edges = []
    for src, dst in spec.get("edges", []):
        edges.append(f'{sanitize(src)} --> {sanitize(dst)}')
    return "\n".join(nodes + edges) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parents[1]
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    chart_type = spec.get("chart_type", "flowchart")
    if chart_type != "flowchart":
        raise SystemExit(f"Unsupported chart_type: {chart_type}")
    template = (skill_root / "assets/templates/chart/flowchart.mmd.tpl").read_text(encoding="utf-8")
    body = flowchart_body(spec)
    diagram = template.format(body=body)
    (out_dir / "diagram.mmd").write_text(diagram, encoding="utf-8")
    (out_dir / "chart-manifest.json").write_text(
        json.dumps(
            {
                "title": spec.get("title", "未命名图表"),
                "chart_type": chart_type,
                "deliverable": "diagram.mmd",
                "node_count": len(spec.get("nodes", [])),
                "edge_count": len(spec.get("edges", [])),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(out_dir / "diagram.mmd")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
