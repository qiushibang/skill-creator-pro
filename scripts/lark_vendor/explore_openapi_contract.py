#!/usr/bin/env python3
"""Build a local OpenAPI exploration contract and CLI call plan for Lark/Feishu."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def dedupe(seq):
    seen = set()
    out = []
    for item in seq:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def cli_help_commands(service_candidates: list[str]) -> list[list[str]]:
    commands = []
    for service in service_candidates:
        commands.append(["lark-cli", service, "--help"])
    return commands or [["lark-cli", "--help"]]


def build_discovery_steps(spec: dict, brand_host: str) -> list[dict]:
    service_candidates = spec.get("service_candidates", [])
    requirement = spec.get("requirement", "未命名需求")
    keywords = spec.get("keywords", [])
    keyword_hint = " / ".join(keywords) if keywords else requirement

    steps = [
        {
            "step": 1,
            "name": "check-existing-cli-capabilities",
            "purpose": "先检查是否已有 shortcut 或已注册 API，避免不必要的 OpenAPI 挖掘",
            "commands": cli_help_commands(service_candidates),
        },
        {
            "step": 2,
            "name": "locate-module-index",
            "purpose": "从顶层 llms 索引定位相关模块文档",
            "web_fetch": {
                "url": f"https://{brand_host}/llms.txt",
                "question": f"列出与“{keyword_hint}”相关的模块文档链接",
            },
        },
        {
            "step": 3,
            "name": "locate-api-doc",
            "purpose": "从模块文档定位具体 API 说明",
            "web_fetch": {
                "url_template": f"https://{brand_host}/llms-docs/zh-CN/llms-<module>.txt",
                "question": f"找出与“{requirement}”相关的 API 文档链接、方法、路径与权限",
            },
        },
        {
            "step": 4,
            "name": "extract-api-contract",
            "purpose": "抽取 API 的方法、路径、参数、响应、scope 与错误码",
            "web_fetch": {
                "url_template": f"https://{brand_host}/document/server-docs/.../<api>.md",
                "question": "返回完整 API 规范：HTTP 方法、URL 路径、参数、请求体、响应字段、所需权限、错误码",
            },
        },
    ]
    return steps


def build_api_calls(api_candidates: list[dict]) -> list[dict]:
    calls = []
    for candidate in api_candidates:
        method = str(candidate.get("method", "GET")).upper()
        path = candidate.get("path", "/open-apis/<path>")
        params = candidate.get("params") or {}
        data = candidate.get("data") or {}
        command = ["lark-cli", "api", method, path]
        if params:
            command.extend(["--params", json.dumps(params, ensure_ascii=False)])
        if data:
            command.extend(["--data", json.dumps(data, ensure_ascii=False)])
        calls.append(
            {
                "name": candidate.get("name", "未命名 API"),
                "method": method,
                "path": path,
                "required_scopes": candidate.get("required_scopes", []),
                "notes": candidate.get("notes", []),
                "command": command,
                "path_params": candidate.get("path_params", []),
                "query_params": candidate.get("query_params", []),
                "body_fields": candidate.get("body_fields", []),
            }
        )
    return calls


def build_contract(spec: dict) -> dict:
    brand = str(spec.get("brand", "feishu")).lower()
    brand_host = "open.larksuite.com" if brand == "lark" else "open.feishu.cn"
    service_candidates = dedupe(spec.get("service_candidates", []))
    write_operation = bool(spec.get("write_operation"))
    api_candidates = build_api_calls(spec.get("api_candidates", []))

    scopes = dedupe(
        scope
        for candidate in api_candidates
        for scope in candidate.get("required_scopes", [])
    )
    scopes = list(scopes)
    if spec.get("required_scopes"):
        scopes = dedupe(scopes + list(spec.get("required_scopes", [])))

    contract = {
        "brand": "lark" if brand == "lark" else "feishu",
        "brand_host": brand_host,
        "requirement": spec.get("requirement", "未命名需求"),
        "keywords": spec.get("keywords", []),
        "service_candidates": service_candidates,
        "discovery_strategy": "shortcut > registered api > openapi docs > lark-cli api",
        "discovery_steps": build_discovery_steps(spec, brand_host),
        "api_candidates": api_candidates,
        "required_scopes": scopes,
        "write_operation": write_operation,
        "safety_gates": {
            "confirm_before_write": write_operation,
            "dry_run_first": bool(spec.get("dry_run_first", True)),
            "no_guessing_paths": True,
            "sensitive_operation_notice": write_operation,
        },
        "response_expectations": spec.get("response_expectations", []),
        "fallback": {
            "when_no_registered_api": "继续按 discovery_steps 挖掘 llms 文档并使用 lark-cli api 裸调",
            "when_missing_scope": "先补充权限并重新认证，再执行命令",
        },
    }
    return contract


def build_execution_plan(contract: dict) -> dict:
    first_call = contract["api_candidates"][0] if contract["api_candidates"] else None
    execution = {
        "preflight": {
            "commands": cli_help_commands(contract.get("service_candidates", [])),
            "requires_scope_check": bool(contract.get("required_scopes")),
        },
        "discovery": contract["discovery_steps"],
        "call_examples": contract["api_candidates"],
        "recommended_first_call": first_call,
        "user_confirmation_required": contract["safety_gates"]["confirm_before_write"],
    }
    return execution


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    contract = build_contract(spec)
    execution = build_execution_plan(contract)

    (out_dir / "openapi-exploration-contract.json").write_text(
        json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "openapi-call-plan.json").write_text(
        json.dumps(execution, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(out_dir / "openapi-exploration-contract.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
