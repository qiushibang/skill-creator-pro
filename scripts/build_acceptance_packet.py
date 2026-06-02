#!/usr/bin/env python3
"""Bundle review/test/security evidence for the final acceptance gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else "(missing)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    reports = workspace / "reports"
    packet = {
        "artifacts": {
            "test_summary": "reports/test-summary.md",
            "review_summary": "reports/review-summary.md",
            "security_summary": "reports/security-summary.md",
        },
        "snippets": {
            "test_summary": read_text(reports / "test-summary.md")[:1200],
            "review_summary": read_text(reports / "review-summary.md")[:1200],
            "security_summary": read_text(reports / "security-summary.md")[:1200],
        },
        "required_confirmation": [
            "skill 目录结构与关键文件说明",
            "测试摘要",
            "评审摘要",
            "安全摘要",
            "zip 包路径",
        ],
    }
    out = workspace / "acceptance-packet.json"
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
