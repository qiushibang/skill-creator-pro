#!/usr/bin/env python3
"""Run local structural verification for the multi-agent skill bundle."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/source-map.md",
    "scripts/quick_validate.py",
    "scripts/package_skill.py",
    "scripts/package_agent_install.py",
    "scripts/verify_vendored_skills.py",
]


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir")
    args = parser.parse_args()
    skill_dir = Path(args.skill_dir).resolve()

    results = {"required": {}, "checks": []}
    missing = []
    for rel in REQUIRED:
        ok = (skill_dir / rel).exists()
        results["required"][rel] = ok
        if not ok:
            missing.append(rel)

    results["checks"].append(run(["python3", str(skill_dir / "scripts/quick_validate.py"), str(skill_dir)]))
    results["checks"].append(run(["python3", str(skill_dir / "scripts/verify_vendored_skills.py")], cwd=str(skill_dir)))
    results["checks"].append(run(["python3", str(skill_dir / "scripts/generate_openai_yaml.py"), str(skill_dir)]))
    results["checks"].append(
        run(
            [
                "python3",
                str(skill_dir / "scripts/package_agent_install.py"),
                str(skill_dir),
                str(skill_dir / "dist"),
            ]
        )
    )
    results["checks"].append(
        run(
            [
                "python3",
                str(skill_dir / "scripts/package_skill.py"),
                str(skill_dir),
                str(skill_dir / "dist"),
            ]
        )
    )
    report_path = skill_dir / "reports" / "verification.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)
    if missing:
        return 1
    return 0 if all(c["returncode"] == 0 for c in results["checks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
