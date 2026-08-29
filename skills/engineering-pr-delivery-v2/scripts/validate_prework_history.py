#!/usr/bin/env python3
from pathlib import Path
import fnmatch
import re
import subprocess
import sys

NON_MATERIAL_PATTERNS = (
    "agents/chains/**",
    "agents/qualifications/**",
    "agents/PR*_workreport.md",
    "agents/status/**",
    "agents/claims/**",
)


def git(root: Path, *args, check=True):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or f"git {' '.join(args)} failed")
    return r


def field(text: str, name: str):
    m = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text or "")
    return m.group(1).strip().strip('`') if m else None


def material_path(path: str):
    return not any(fnmatch.fnmatch(path, pat) for pat in NON_MATERIAL_PATTERNS)


def show_file(root: Path, commit: str, rel: str):
    r = git(root, "show", f"{commit}:{rel}", check=False)
    return r.stdout if r.returncode == 0 else None


def validate_prework_content(text: str, where: str):
    errors = []
    expected = {
        "PREWORK_QUALIFICATION_READY": "TRUE",
        "COMMON_PROTOCOL": "engineering-pr-delivery-v2",
        "COMMON_PROTOCOL_STATUS": "CURRENT",
        "QUALIFICATION_PROTOCOL_VERSION": "3",
        "QUESTION_SET_STATUS": "CURRENT",
        "QUESTION_SET_ADMISSION_REQUIREMENT": "REQUIRED_ON_TAKEOVER",
    }
    for name, wanted in expected.items():
        if field(text, name) != wanted:
            errors.append(f"{where}: {name} expected {wanted}, found {field(text, name)}")
    profile = field(text, "QUALIFICATION_PROFILE")
    if not profile:
        errors.append(f"{where}: missing QUALIFICATION_PROFILE")
    qheads = re.findall(r"(?mi)^####\s+Q([1-5])\s+—", text or "")
    if qheads != ["1", "2", "3", "4", "5"]:
        errors.append(f"{where}: historical prework endpoint must already contain ordered Q1-Q5, found {qheads}")
    return errors


def main():
    if len(sys.argv) != 5:
        print("Usage: validate_prework_history.py <repo-root> <base-ref> <head-ref> <active.md>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    base_ref, head_ref = sys.argv[2], sys.argv[3]
    active = Path(sys.argv[4]).resolve()
    try:
        if not (root / ".git").exists():
            raise RuntimeError("repository Git history unavailable")
        base = git(root, "rev-parse", base_ref).stdout.strip()
        head = git(root, "rev-parse", head_ref).stdout.strip()
        if git(root, "merge-base", "--is-ancestor", base, head, check=False).returncode != 0:
            raise RuntimeError(f"base {base_ref} is not an ancestor of {head_ref}")
        if not active.is_file():
            raise RuntimeError(f"ACTIVE.md missing: {active}")
        at = active.read_text(encoding="utf-8")
        prework_rel = field(at, "MATERIAL_LEG_PREWORK_ENDPOINT_FILE")
        if not prework_rel:
            raise RuntimeError("ACTIVE missing MATERIAL_LEG_PREWORK_ENDPOINT_FILE")
        prework_path = root / prework_rel
        try:
            prework_path.relative_to(root / "agents" / "chains")
        except ValueError:
            raise RuntimeError("MATERIAL_LEG_PREWORK_ENDPOINT_FILE must be under agents/chains/**")

        intro = git(root, "log", "--reverse", "--format=%H", "--diff-filter=A", f"{base}..{head}", "--", prework_rel).stdout.splitlines()
        if intro:
            prework_commit = intro[0].strip()
        else:
            existing = show_file(root, base, prework_rel)
            if existing is None:
                raise RuntimeError("prework endpoint was neither present at base nor introduced in the leg")
            prework_commit = base

        historical = show_file(root, prework_commit, prework_rel)
        if historical is None:
            raise RuntimeError(f"cannot read prework endpoint at {prework_commit}")
        errors = validate_prework_content(historical, f"{prework_rel}@{prework_commit}")

        changed = git(root, "diff", "--name-only", f"{base}..{head}").stdout.splitlines()
        material = [p for p in changed if p and material_path(p)]
        if not material:
            if errors:
                for e in errors:
                    print("FAIL:", e)
                return 1
            print(f"PASS: prework endpoint historically valid; no material paths in {base_ref}..{head_ref}")
            return 0

        first_material_lines = git(root, "log", "--reverse", "--format=%H", f"{base}..{head}", "--", *material).stdout.splitlines()
        if not first_material_lines:
            raise RuntimeError("material paths changed but first material commit could not be resolved")
        first_material = first_material_lines[0].strip()
        if prework_commit == first_material:
            errors.append(f"prework endpoint and first material change occur in the same commit {prework_commit}")
        elif git(root, "merge-base", "--is-ancestor", prework_commit, first_material, check=False).returncode != 0:
            errors.append(f"prework commit {prework_commit} does not precede first material commit {first_material}")

        if errors:
            for e in errors:
                print("FAIL:", e)
            return 1
        print(f"PASS: prework endpoint {prework_rel}@{prework_commit} precedes first material commit {first_material}")
        return 0
    except RuntimeError as exc:
        print(f"FAIL: PREWORK_HISTORY_STATUS INVALID_OR_UNPROVEN — {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
