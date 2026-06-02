#!/usr/bin/env python3
"""Build local whiteboard insertion/fill requests from board action plans."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("board_action")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    board = json.loads(Path(args.board_action).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    insert_request = {
        "tool": "lark-doc-update",
        "doc": board["placement"].get("doc"),
        "mode": "insert_after",
        "selection_by_title": f"## {board['placement'].get('after_section', '技能简介')}",
        "markdown": board["insert_markdown"],
    }
    fill_request = {
        "tool": "lark-doc-whiteboard-update",
        "board_type": board["board_type"],
        "board_spec_path": board["board_spec_path"],
        "requires_board_token_from_update": True,
        "dry_run_first": True,
    }

    (out_dir / "whiteboard-insert-request.json").write_text(
        json.dumps(insert_request, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "whiteboard-fill-request.json").write_text(
        json.dumps(fill_request, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(out_dir / "whiteboard-fill-request.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
