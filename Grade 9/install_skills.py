#!/usr/bin/env python3
"""Install the Grade 9 skill family into a Codex/Agent Skills directory.

Examples:
  python "Grade 9/install_skills.py" --dest .agents/skills
  python "Grade 9/install_skills.py" --dest "$CODEX_HOME/skills" --force

This script copies only skill folders. Shared Grade 9 references remain in the
repository; install from the repository when you want cross-skill shared files.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKILLS = [
    "grade9",
    "grade9-source-grounding",
    "grade9-concept-architect",
    "grade9-question-bank",
    "grade9-learning-enrichment",
    "grade9-textbook-publisher",
    "grade9-math",
    "grade9-physics",
    "grade9-chemistry",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", required=True, help="Destination skills directory")
    parser.add_argument("--force", action="store_true", help="Replace existing skill folders")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    src_root = root / "skills"
    dest_root = Path(args.dest).expanduser().resolve()
    dest_root.mkdir(parents=True, exist_ok=True)

    for name in SKILLS:
        src = src_root / name
        dst = dest_root / name
        if not src.exists():
            raise SystemExit(f"Missing source skill: {src}")
        if dst.exists():
            if not args.force:
                raise SystemExit(f"Destination exists: {dst} (use --force to replace)")
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Installed {name} -> {dst}")

    print(f"Installed {len(SKILLS)} Grade 9 skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
