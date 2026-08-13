#!/usr/bin/env python3
"""Validate the Grade 9 Agent Skills package using only the Python stdlib.

Checks:
- folder name matches SKILL.md frontmatter name
- frontmatter contains only name + description
- skill names are lowercase letters/digits/hyphens and <=64 chars
- agents/openai.yaml exists
- interface display_name, short_description, default_prompt are present
- default_prompt mentions $<skill-name>

Usage:
  python "Grade 9/validate_skills.py"
"""

from __future__ import annotations

import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    block = text[4:end]
    result: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def main() -> int:
    root = Path(__file__).resolve().parent / "skills"
    errors: list[str] = []
    skills = sorted(p for p in root.iterdir() if p.is_dir())

    for folder in skills:
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{folder.name}: missing SKILL.md")
            continue
        try:
            meta = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{folder.name}: {exc}")
            continue

        if set(meta) != {"name", "description"}:
            errors.append(f"{folder.name}: frontmatter keys must be exactly name, description")
        name = meta.get("name", "")
        if name != folder.name:
            errors.append(f"{folder.name}: frontmatter name is {name!r}")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{folder.name}: invalid skill name")
        if not meta.get("description"):
            errors.append(f"{folder.name}: empty description")

        ui = folder / "agents" / "openai.yaml"
        if not ui.exists():
            errors.append(f"{folder.name}: missing agents/openai.yaml")
        else:
            ui_text = ui.read_text(encoding="utf-8")
            for key in ("display_name:", "short_description:", "default_prompt:"):
                if key not in ui_text:
                    errors.append(f"{folder.name}: openai.yaml missing {key[:-1]}")
            if f"${name}" not in ui_text:
                errors.append(f"{folder.name}: default_prompt should mention ${name}")

    if errors:
        print("GRADE 9 SKILL VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"GRADE 9 SKILL VALIDATION: PASS ({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
