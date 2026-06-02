#!/usr/bin/env python3
"""Render executable Lark doc command plans from a Feishu action plan."""
from __future__ import annotations
import argparse
import json
import shlex
from pathlib import Path


def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def build_create_command(create: dict) -> dict:
    command = ["lark-cli", "docs", "+create", "--title", create["title"], "--markdown", create["markdown"]]
    for key, flag in (("folder_token", "--folder-token"), ("wiki_node", "--wiki-node"), ("wiki_space", "--wiki-space")):
        if create.get(key):
            command.extend([flag, create[key]])
    return {
        "command": command,
        "shell": shell_join(command),
    }


def build_update_commands(update: dict | None) -> list[dict]:
    if not update:
        return []
    result = []
    mode = update.get("mode", "append")
    doc = update["doc"]
    for chunk in update.get("chunks", []):
        command = [
            "lark-cli",
            "docs",
            "+update",
            "--doc",
            doc,
            "--mode",
            mode,
            "--markdown",
            chunk["markdown"],
        ]
        result.append(
            {
                "chunk_index": chunk.get("index"),
                "section_titles": chunk.get("section_titles", []),
                "command": command,
                "shell": shell_join(command),
            }
        )
    return result


def build_board_commands(board: dict | None) -> dict | None:
    if not board or not board.get("enabled"):
        return None
    placement = board.get("placement", {})
    doc = placement.get("doc")
    after_section = placement.get("after_section", "技能简介")
    insert_command = [
        "lark-cli",
        "docs",
        "+update",
        "--doc",
        doc,
        "--mode",
        "insert_after",
        "--selection-by-title",
        f"## {after_section}",
        "--markdown",
        board["insert_markdown"],
    ]
    return {
        "insert": {
            "command": insert_command,
            "shell": shell_join(insert_command),
        },
        "fill": {
            "note": "After docs +update returns board_tokens, apply board_spec_path with embedded whiteboard pipeline.",
            "board_spec_path": board["board_spec_path"],
            "board_type": board["board_type"],
        },
    }


def render_markdown(command_plan: dict) -> str:
    lines = ["# Lark Doc Commands", "", "## docs +create", "", "```bash", command_plan["create"]["shell"], "```"]
    updates = command_plan.get("update", [])
    if updates:
        lines.extend(["", "## docs +update", ""])
        for item in updates:
            title = ", ".join(item.get("section_titles", [])) or "未命名分块"
            lines.extend([
                f"### Chunk {item['chunk_index']}: {title}",
                "",
                "```bash",
                item["shell"],
                "```",
                "",
            ])
    board = command_plan.get("board")
    if board:
        lines.extend([
            "",
            "## whiteboard insert",
            "",
            "```bash",
            board["insert"]["shell"],
            "```",
            "",
            "## whiteboard fill",
            "",
            f"- board_type: `{board['fill']['board_type']}`",
            f"- board_spec_path: `{board['fill']['board_spec_path']}`",
            f"- note: {board['fill']['note']}",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action_plan")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    action_plan_path = Path(args.action_plan).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    action_plan = json.loads(action_plan_path.read_text(encoding="utf-8"))

    command_plan = {
        "create": build_create_command(action_plan["create"]),
        "update": build_update_commands(action_plan.get("update")),
        "board": build_board_commands(action_plan.get("board")),
    }

    (out_dir / "lark-doc-commands.json").write_text(
        json.dumps(command_plan, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "lark-doc-commands.md").write_text(render_markdown(command_plan), encoding="utf-8")
    print(out_dir / "lark-doc-commands.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
