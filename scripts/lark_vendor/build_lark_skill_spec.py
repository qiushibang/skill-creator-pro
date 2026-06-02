#!/usr/bin/env python3
"""Build a local Lark skill scaffold/spec from normalized automation requirements."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def bullet(items: list[str], default: str = "- 暂无") -> str:
    if not items:
        return default
    return "\n".join(f"- {item}" for item in items)


def render_command_block(commands: list[dict]) -> str:
    if not commands:
        return "# 暂无命令"
    lines = []
    for idx, cmd in enumerate(commands, 1):
        title = cmd.get("title") or f"Step {idx}"
        rationale = cmd.get("rationale") or "执行该步骤"
        command = " ".join(cmd.get("command", [])) if cmd.get("command") else "# 待补命令"
        lines.extend(
            [
                f"# Step {idx}: {title}",
                f"# {rationale}",
                command,
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def build_command_plan(spec: dict) -> list[dict]:
    commands = []
    for shortcut in as_list(spec.get("shortcut_commands")):
        if isinstance(shortcut, dict):
            commands.append(
                {
                    "title": shortcut.get("title", shortcut.get("name", "调用 shortcut")),
                    "type": "shortcut",
                    "rationale": shortcut.get("rationale", "优先使用已存在 shortcut"),
                    "command": shortcut.get("command", []),
                }
            )
        else:
            commands.append(
                {
                    "title": "调用 shortcut",
                    "type": "shortcut",
                    "rationale": "优先使用已存在 shortcut",
                    "command": ["lark-cli", *str(shortcut).split()],
                }
            )

    for registered in as_list(spec.get("registered_apis")):
        command = ["lark-cli"]
        service = registered.get("service", "<service>")
        resource = registered.get("resource", "<resource>")
        method = registered.get("method", "<method>")
        command.extend([service, resource, method])
        if registered.get("params"):
            command.extend(["--data", json.dumps(registered["params"], ensure_ascii=False)])
        commands.append(
            {
                "title": registered.get("title", f"{service}.{resource}.{method}"),
                "type": "registered_api",
                "rationale": registered.get("rationale", "使用已注册 API"),
                "command": command,
            }
        )

    for api in as_list(spec.get("openapi_calls")):
        method = str(api.get("method", "GET")).upper()
        path = api.get("path", "/open-apis/<path>")
        command = ["lark-cli", "api", method, path]
        if api.get("params"):
            command.extend(["--params", json.dumps(api["params"], ensure_ascii=False)])
        if api.get("data"):
            command.extend(["--data", json.dumps(api["data"], ensure_ascii=False)])
        commands.append(
            {
                "title": api.get("title", api.get("name", "调用原生 OpenAPI")),
                "type": "openapi",
                "rationale": api.get("rationale", "使用原生 OpenAPI 裸调"),
                "command": command,
            }
        )
    return commands


def render_skill_md(normalized: dict) -> str:
    name = normalized["name"]
    description = normalized["description"]
    title = normalized["title"]
    commands = normalized["command_plan"]
    scopes = normalized["scopes"]
    triggers = normalized["trigger_scenarios"]
    safety_rules = normalized["safety_rules"]
    orchestration = normalized["orchestration"]

    lines = [
        "---",
        f"name: {name}",
        "version: 1.0.0",
        f'description: "{description}"',
        "metadata:",
        "  requires:",
        '    bins: ["lark-cli"]',
        "---",
        "",
        f"# {title}",
        "",
        "> **前置条件：** 先阅读 `../lark-shared/SKILL.md`，确认认证、scope 和安全规则。",
        "",
        "## 触发场景",
        bullet(triggers),
        "",
        "## 命令",
        "```bash",
        render_command_block(commands),
        "```",
        "",
        "## 编排说明",
        bullet(orchestration),
        "",
        "## 权限",
    ]
    if scopes:
        lines.extend(
            [
                "| 操作 | 所需 scope |",
                "|---|---|",
                *[f"| {item.get('operation', '未命名操作')} | `{item.get('scope', '待补充')}` |" for item in scopes],
            ]
        )
    else:
        lines.append("- 待补充")

    lines.extend(
        [
            "",
            "## 安全规则",
            bullet(safety_rules),
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def normalize_spec(spec: dict) -> dict:
    name = spec.get("name", "lark-custom-skill")
    title = spec.get("title", name)
    trigger_scenarios = as_list(spec.get("trigger_scenarios"))
    command_plan = build_command_plan(spec)
    description = spec.get("description")
    if not description:
        trigger_hint = "、".join(trigger_scenarios[:3]) if trigger_scenarios else "相关飞书自动化场景"
        description = f"{spec.get('summary', '用于飞书自动化')}。当用户需要{trigger_hint}时使用。"

    normalized = {
        "name": name,
        "title": title,
        "summary": spec.get("summary", "用于飞书自动化"),
        "description": description,
        "trigger_scenarios": trigger_scenarios,
        "command_plan": command_plan,
        "scopes": as_list(spec.get("scopes")),
        "safety_rules": as_list(spec.get("safety_rules")) or [
            "写入或删除操作前必须确认用户意图",
            "优先使用 dry-run 或预览能力",
            "不要猜测 API 路径或参数",
        ],
        "orchestration": as_list(spec.get("orchestration")) or [
            "先检查 shortcut 和已注册 API，再回退到原生 OpenAPI",
            "多步流程要记录上一步输出并在下一步复用",
        ],
    }
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    normalized = normalize_spec(spec)
    skill_md = render_skill_md(normalized)

    (out_dir / "lark-skill-spec.normalized.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "lark-command-plan.json").write_text(
        json.dumps({"commands": normalized["command_plan"]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    print(out_dir / "SKILL.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
