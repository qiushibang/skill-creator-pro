#!/usr/bin/env python3
"""Build local Lark doc create/update requests from normalized action inputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_json")
    parser.add_argument("--mode", choices=["create", "update"], required=True)
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    if args.mode == "create":
        payload = {
            "tool": "lark-doc-create",
            "title": spec["title"],
            "markdown": spec["markdown"],
            "folder_token": spec.get("folder_token"),
            "wiki_node": spec.get("wiki_node"),
            "wiki_space": spec.get("wiki_space"),
        }
    else:
        payload = {
            "tool": "lark-doc-update",
            "doc": spec["doc"],
            "mode": spec["mode"],
            "markdown": spec["markdown"],
            "selection_by_title": spec.get("selection_by_title"),
            "selection_with_ellipsis": spec.get("selection_with_ellipsis"),
        }

    out = Path(args.out_json).resolve()
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
