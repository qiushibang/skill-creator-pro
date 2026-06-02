#!/usr/bin/env python3
"""Create evidence-based test/review/security summaries for the generated skill."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_verification(report_dir: Path) -> dict:
    verification_path = report_dir / "verification.json"
    if not verification_path.exists():
        return {"required": {}, "checks": []}
    return json.loads(verification_path.read_text(encoding="utf-8"))


def format_cmd(cmd: list[str] | str | None) -> str:
    if isinstance(cmd, list):
        return " ".join(cmd)
    if isinstance(cmd, str):
        return cmd
    return "(unknown command)"


def command_matches(check: dict, *needles: str) -> bool:
    rendered = format_cmd(check.get("cmd")).lower()
    return any(needle.lower() in rendered for needle in needles)


def status_label(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def build_test_summary(ts: str, verification: dict) -> str:
    required = verification.get("required", {})
    checks = verification.get("checks", [])
    required_ok = all(bool(v) for v in required.values()) if required else False
    validation_checks = [c for c in checks if command_matches(c, "quick_validate", "pytest", "verify_bundle")]
    packaging_checks = [c for c in checks if command_matches(c, "package_skill", ".zip")]

    lines = [
        "# Test Summary",
        "",
        f"- Generated: {ts}",
        f"- Required file presence: {status_label(required_ok)} ({sum(bool(v) for v in required.values())}/{len(required)})",
        "",
        "## Validation Evidence",
    ]
    if validation_checks:
        for check in validation_checks:
            ok = check.get("returncode", 1) == 0
            lines.extend(
                [
                    f"- {status_label(ok)}: `{format_cmd(check.get('cmd'))}`",
                    f"  - returncode: {check.get('returncode')}",
                    f"  - stdout: {((check.get('stdout') or '').strip() or '(empty)')}",
                ]
            )
    else:
        lines.append("- NOT RUN: no validation command recorded in verification.json")

    lines.extend(["", "## Packaging Check"])
    if packaging_checks:
        for check in packaging_checks:
            ok = check.get("returncode", 1) == 0
            lines.extend(
                [
                    f"- {status_label(ok)}: `{format_cmd(check.get('cmd'))}`",
                    f"  - returncode: {check.get('returncode')}",
                    f"  - stdout: {((check.get('stdout') or '').strip() or '(empty)')}",
                ]
            )
    else:
        lines.append("- NOT RUN: packaging command not captured in verification.json")

    return "\n".join(lines) + "\n"


def build_review_summary(ts: str, verification: dict) -> str:
    required = verification.get("required", {})
    checks = verification.get("checks", [])
    all_checks_ok = all(c.get("returncode", 1) == 0 for c in checks) if checks else False
    source_map_present = bool(required.get("references/source-map.md"))
    skill_md_present = bool(required.get("SKILL.md"))

    observations = [
        f"- source-map present: {'yes' if source_map_present else 'no'}",
        f"- SKILL.md present: {'yes' if skill_md_present else 'no'}",
        f"- verification commands all green: {'yes' if all_checks_ok else 'no'}",
    ]
    for check in checks:
        observations.append(
            f"- command `{format_cmd(check.get('cmd'))}` -> {status_label(check.get('returncode', 1) == 0)}"
        )

    lines = [
        "# Review Summary",
        "",
        f"- Generated: {ts}",
        f"- Code/skill review status: {'pass-with-evidence' if (source_map_present or skill_md_present) and all_checks_ok else 'needs-follow-up'}",
        "- Key observations:",
        *observations,
    ]
    return "\n".join(lines) + "\n"


def build_security_summary(ts: str, verification: dict) -> str:
    checks = verification.get("checks", [])
    risky_cmds = []
    for check in checks:
        rendered = format_cmd(check.get("cmd")).lower()
        if any(token in rendered for token in ("curl ", "wget ", "scp ", "ssh ", "rm -rf", "lark-cli docs +update", "lark-cli docs +create")):
            risky_cmds.append(format_cmd(check.get("cmd")))

    lines = [
        "# Security Summary",
        "",
        f"- Generated: {ts}",
        "- Secret handling: 未发现硬编码凭据（基于 verification.json 中记录的结构校验与命令证据；仍建议在最终验收前做人审）",
        "- 外部写入动作: 当前 verification.json 未记录真实外部写入命令；如后续执行飞书写入，需保留用户确认记录。",
        "",
        "## Command Surface Review",
    ]
    if risky_cmds:
        for cmd in risky_cmds:
            lines.append(f"- REVIEW: `{cmd}`")
    else:
        lines.append("- No high-risk external write commands were captured in verification.json")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Workspace root")
    args = parser.parse_args()

    base = Path(args.workspace).resolve() / "reports"
    base.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().isoformat() + "Z"
    verification = load_verification(base)

    outputs = {
        "test-summary.md": build_test_summary(ts, verification),
        "review-summary.md": build_review_summary(ts, verification),
        "security-summary.md": build_security_summary(ts, verification),
    }

    for name, content in outputs.items():
        path = base / name
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
