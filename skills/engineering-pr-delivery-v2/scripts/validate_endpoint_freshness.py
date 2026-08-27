#!/usr/bin/env python3
from pathlib import Path
import argparse
import re


def field(text: str, name: str):
    vals = [v.strip() for v in re.findall(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n#]+)", text)]
    if len(vals) != 1:
        return None, len(vals)
    return vals[0], 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("endpoint")
    p.add_argument("current_material_head")
    p.add_argument("--metadata-only", action="store_true")
    args = p.parse_args()

    text = Path(args.endpoint).read_text(encoding="utf-8")
    basis, basis_count = field(text, "QUALIFICATION_BASIS_HEAD")
    status, status_count = field(text, "QUESTION_SET_STATUS")
    errors = []
    if basis_count != 1:
        errors.append(f"QUALIFICATION_BASIS_HEAD must appear exactly once; found {basis_count}")
    if status_count != 1:
        errors.append(f"QUESTION_SET_STATUS must appear exactly once; found {status_count}")
    if status == "CURRENT" and basis and basis != args.current_material_head and not args.metadata_only:
        errors.append(
            f"CURRENT question set is stale: basis={basis} current_material_head={args.current_material_head}"
        )
    if status == "CURRENT" and args.metadata_only:
        print("PASS: metadata-only drift does not invalidate material qualification basis")
        return 0 if not errors else 1
    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: qualification freshness is consistent with current material head")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
