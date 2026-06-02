#!/usr/bin/env python3
"""Build an agent-install-friendly staging directory and zip for the skill."""
from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from quick_validate import validate_skill
from frontmatter_utils import parse_frontmatter_file


INCLUDED_ROOTS = [
    "SKILL.md",
    "agents/openai.yaml",
    "assets",
    "references",
    "scripts",
]


def copy_root(skill_dir: Path, staging_skill_dir: Path, rel: str, copied: list[str]) -> None:
    src = skill_dir / rel
    dst = staging_skill_dir / rel
    if not src.exists():
        return
    if src.is_dir():
        shutil.copytree(src, dst)
        copied.append(f"{rel}/")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)


def zip_tree(staging_root: Path, zip_path: Path) -> int:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in staging_root.rglob("*"):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(staging_root.parent))
    return zip_path.stat().st_size


def build_install_bundle(skill_dir: Path, dist_dir: Path) -> tuple[Path, Path]:
    valid, message = validate_skill(skill_dir)
    if not valid:
        raise SystemExit(f"Validation failed: {message}")

    frontmatter = parse_frontmatter_file(skill_dir / "SKILL.md")
    bundle_name = str(frontmatter.get("name") or skill_dir.name).strip() or skill_dir.name
    staging_root = dist_dir / "_agent_install_staging"
    staging_skill_dir = staging_root / bundle_name
    if staging_root.exists():
        shutil.rmtree(staging_root)
    staging_skill_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for rel in INCLUDED_ROOTS:
        copy_root(skill_dir, staging_skill_dir, rel, copied)

    zip_path = dist_dir / f"{bundle_name}-agent-install.zip"
    if zip_path.exists():
        zip_path.unlink()
    size_bytes = zip_tree(staging_skill_dir, zip_path)

    manifest = {
        "zip": str(zip_path),
        "included_roots": INCLUDED_ROOTS,
        "copied": copied,
        "size_bytes": size_bytes,
    }
    manifest_path = dist_dir / "agent-install-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return zip_path, manifest_path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python package_agent_install.py <skill_dir> [dist_dir]")
        return 1
    skill_dir = Path(sys.argv[1]).resolve()
    dist_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else skill_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    zip_path, manifest_path = build_install_bundle(skill_dir, dist_dir)
    print(zip_path)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
