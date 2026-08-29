#!/usr/bin/env python3
from pathlib import Path
import fnmatch
import re
import subprocess
import sys

RELAY_ONLY_PATTERNS = (
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


def relay_only(path: str):
    return any(fnmatch.fnmatch(path, pat) for pat in RELAY_ONLY_PATTERNS)


def changed_paths(root: Path, base: str, head: str):
    return [p for p in git(root, "diff", "--name-only", f"{base}..{head}").stdout.splitlines() if p]


def material_paths(root: Path, base: str, head: str):
    return [p for p in changed_paths(root, base, head) if not relay_only(p)]


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
    if not field(text, "QUALIFICATION_PROFILE"):
        errors.append(f"{where}: missing QUALIFICATION_PROFILE")
    qheads = re.findall(r"(?mi)^####\s+Q([1-5])\s+—", text or "")
    if qheads != ["1", "2", "3", "4", "5"]:
        errors.append(f"{where}: historical prework endpoint must already contain ordered Q1-Q5, found {qheads}")
    return errors


def validate_receipt(root: Path, chain_dir: Path, receipt: Path):
    text = receipt.read_text(encoding="utf-8")
    errors = []
    chain = field(text, "CHAIN_ID")
    leg = field(text, "MATERIAL_LEG_ID")
    base = field(text, "MATERIAL_LEG_BASE")
    head = field(text, "MATERIAL_LEG_HEAD")
    prework_rel = field(text, "MATERIAL_LEG_PREWORK_ENDPOINT_FILE")
    if chain != chain_dir.name:
        errors.append(f"{receipt}: CHAIN_ID {chain} != {chain_dir.name}")
    if not leg or receipt.stem != leg:
        errors.append(f"{receipt}: filename must match MATERIAL_LEG_ID {leg}")
    if field(text, "MATERIAL_LEG_HISTORY_STATUS") != "RECORDED":
        errors.append(f"{receipt}: MATERIAL_LEG_HISTORY_STATUS must be RECORDED")
    if not base or not head:
        return errors + [f"{receipt}: missing MATERIAL_LEG_BASE or MATERIAL_LEG_HEAD"]
    try:
        base_sha = git(root, "rev-parse", base).stdout.strip()
        head_sha = git(root, "rev-parse", head).stdout.strip()
    except RuntimeError as exc:
        return errors + [f"{receipt}: unresolved base/head — {exc}"]
    if git(root, "merge-base", "--is-ancestor", base_sha, head_sha, check=False).returncode != 0:
        errors.append(f"{receipt}: base is not ancestor of material head")
    if git(root, "merge-base", "--is-ancestor", head_sha, "HEAD", check=False).returncode != 0:
        errors.append(f"{receipt}: material head is not reachable from audited HEAD")
    if not prework_rel:
        errors.append(f"{receipt}: missing MATERIAL_LEG_PREWORK_ENDPOINT_FILE")
        return errors
    expected_prefix = f"agents/chains/{chain_dir.name}/endpoints/"
    if not prework_rel.startswith(expected_prefix):
        errors.append(f"{receipt}: prework endpoint must be same-chain canonical endpoint")
        return errors

    intro = git(root, "log", "--reverse", "--format=%H", "--diff-filter=A", f"{base_sha}..{head_sha}", "--", prework_rel).stdout.splitlines()
    if intro:
        prework_commit = intro[0].strip()
    else:
        if show_file(root, base_sha, prework_rel) is None:
            errors.append(f"{receipt}: prework endpoint absent at base and not introduced before material head")
            return errors
        prework_commit = base_sha

    historical = show_file(root, prework_commit, prework_rel)
    if historical is None:
        errors.append(f"{receipt}: cannot read historical prework endpoint at {prework_commit}")
        return errors
    errors.extend(validate_prework_content(historical, f"{prework_rel}@{prework_commit}"))

    material = material_paths(root, base_sha, head_sha)
    if not material:
        errors.append(f"{receipt}: no material paths in recorded material leg")
        return errors
    first = git(root, "log", "--reverse", "--format=%H", f"{base_sha}..{head_sha}", "--", *material).stdout.splitlines()
    if not first:
        errors.append(f"{receipt}: cannot resolve first material commit")
        return errors
    first_material = first[0].strip()
    if prework_commit == first_material:
        errors.append(f"{receipt}: prework and first material change are the same commit {prework_commit}")
    elif git(root, "merge-base", "--is-ancestor", prework_commit, first_material, check=False).returncode != 0:
        errors.append(f"{receipt}: prework commit {prework_commit} does not precede first material commit {first_material}")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_material_leg_history.py <repo-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not (root / ".git").exists():
        print("FAIL: material-leg history requires a Git checkout")
        return 1
    chains = root / "agents" / "chains"
    if not chains.is_dir():
        print("FAIL: canonical agents/chains store missing")
        return 1
    errors = []
    checked = 0
    grandfathered = 0
    for chain_dir in sorted(p for p in chains.iterdir() if p.is_dir()):
        active = chain_dir / "ACTIVE.md"
        if not active.is_file():
            continue
        at = active.read_text(encoding="utf-8")
        if field(at, "CHAIN_STATE_VERSION") != "3":
            continue
        root_base = field(at, "MATERIAL_HISTORY_ROOT_BASE")
        if not root_base:
            grandfathered += 1
            continue
        try:
            root_sha = git(root, "rev-parse", root_base).stdout.strip()
        except RuntimeError as exc:
            errors.append(f"{chain_dir.name}: invalid MATERIAL_HISTORY_ROOT_BASE — {exc}")
            continue
        if git(root, "merge-base", "--is-ancestor", root_sha, "HEAD", check=False).returncode != 0:
            errors.append(f"{chain_dir.name}: material history root is not ancestor of HEAD")
            continue

        receipts_dir = chain_dir / "material-legs"
        receipts = sorted(receipts_dir.glob("*.md")) if receipts_dir.is_dir() else []
        if not receipts:
            pending = material_paths(root, root_sha, "HEAD")
            if pending:
                errors.append(f"{chain_dir.name}: unreceipted material changes after history root: {pending[:8]}")
            continue

        previous_leg = None
        previous_head = root_sha
        for receipt in receipts:
            text = receipt.read_text(encoding="utf-8")
            leg = field(text, "MATERIAL_LEG_ID")
            previous = field(text, "PREVIOUS_MATERIAL_LEG")
            base = field(text, "MATERIAL_LEG_BASE")
            head = field(text, "MATERIAL_LEG_HEAD")
            if previous_leg is None:
                if not previous or not previous.upper().startswith("NONE"):
                    errors.append(f"{receipt}: first receipt PREVIOUS_MATERIAL_LEG must be NONE")
            elif previous != previous_leg:
                errors.append(f"{receipt}: PREVIOUS_MATERIAL_LEG must be {previous_leg}, found {previous}")
            if base:
                try:
                    base_sha = git(root, "rev-parse", base).stdout.strip()
                    gap_material = material_paths(root, previous_head, base_sha)
                    if gap_material:
                        errors.append(f"{receipt}: material changes exist in inter-leg relay gap: {gap_material[:8]}")
                except RuntimeError as exc:
                    errors.append(f"{receipt}: cannot audit inter-leg gap — {exc}")
            errors.extend(validate_receipt(root, chain_dir, receipt))
            checked += 1
            if head:
                try:
                    previous_head = git(root, "rev-parse", head).stdout.strip()
                except RuntimeError:
                    pass
            previous_leg = leg

        trailing = material_paths(root, previous_head, "HEAD")
        if trailing:
            errors.append(f"{chain_dir.name}: unreceipted material changes after last receipt: {trailing[:8]}")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print(f"PASS: material-leg history ({checked} receipt(s); {grandfathered} pre-feature v3 chain(s) grandfathered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
