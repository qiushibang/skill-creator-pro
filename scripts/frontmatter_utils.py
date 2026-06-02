#!/usr/bin/env python3
"""Minimal YAML frontmatter parser for skill metadata.
Supports the subset used by installed skills: top-level key/value pairs,
quoted scalars, block strings (| or >), and nested metadata blocks.
"""
from __future__ import annotations

import re
from pathlib import Path

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")


class FrontmatterError(ValueError):
    pass


def extract_frontmatter_text(skill_md: Path) -> str:
    content = skill_md.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(content)
    if not match:
        raise FrontmatterError("Invalid frontmatter format")
    return match.group(1)


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")):
        return value[1:-1]
    return value


def parse_frontmatter_text(text: str) -> dict:
    result: dict[str, object] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise FrontmatterError(f"Unexpected indentation at line: {line}")
        m = _KEY_RE.match(line)
        if not m:
            raise FrontmatterError(f"Unsupported frontmatter line: {line}")
        key, raw = m.group(1), (m.group(2) or "")
        raw = raw.strip()

        if raw in {"|", ">"}:
            i += 1
            block = []
            while i < len(lines):
                nxt = lines[i]
                if nxt.startswith((" ", "\t")):
                    block.append(nxt[1:] if nxt.startswith(" ") else nxt.lstrip("\t"))
                    i += 1
                elif not nxt.strip():
                    block.append("")
                    i += 1
                else:
                    break
            result[key] = "\n".join(block).rstrip("\n")
            continue

        if raw == "":
            i += 1
            nested = {}
            while i < len(lines):
                nxt = lines[i]
                if not nxt.startswith((" ", "\t")):
                    break
                stripped = nxt[1:] if nxt.startswith(" ") else nxt.lstrip("\t")
                if not stripped.strip():
                    i += 1
                    continue
                m2 = _KEY_RE.match(stripped)
                if not m2:
                    raise FrontmatterError(f"Unsupported nested line: {nxt}")
                nested[m2.group(1)] = _unquote((m2.group(2) or "").strip())
                i += 1
            result[key] = nested
            continue

        result[key] = _unquote(raw)
        i += 1
    return result


def parse_frontmatter_file(skill_md: Path) -> dict:
    return parse_frontmatter_text(extract_frontmatter_text(skill_md))
