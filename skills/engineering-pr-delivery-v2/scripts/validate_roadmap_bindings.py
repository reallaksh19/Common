#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import sys

VALID_REVIEW_STATUS = {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}


def field_value(text: str, name: str):
    match = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*([^\n]+?)\s*$", text)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def parse_bindings(value: str):
    bindings = []
    for raw in value.split(";"):
        item = raw.strip()
        if not item:
            continue
        if "@" not in item:
            raise ValueError(f"roadmap binding lacks @<blob-sha>: {item}")
        path, blob = item.rsplit("@", 1)
        path = path.strip()
        blob = blob.strip().lower()
        if not path or not re.fullmatch(r"[0-9a-f]{40}", blob):
            raise ValueError(f"invalid roadmap binding: {item}")
        bindings.append((path, blob))
    if not bindings:
        raise ValueError("no roadmap bindings found")
    return bindings


def validate_chain(repo_root: Path, active_path: Path):
    errors = []
    text = active_path.read_text(encoding="utf-8")
    version = field_value(text, "CHAIN_STATE_VERSION")
    chain = field_value(text, "CHAIN_ID") or active_path.parent.name

    # Version 1 canonical chains predate roadmap binding. They remain readable
    # historical/compatibility state and must migrate before their next
    # material coding leg under the new policy.
    if version != "2":
        return errors

    roadmaps = field_value(text, "ROADMAPS")
    review = field_value(text, "ROADMAP_REVIEW_STATUS")
    if not roadmaps:
        errors.append(f"{chain}: ACTIVE.md missing ROADMAPS")
        return errors
    if review not in VALID_REVIEW_STATUS:
        errors.append(
            f"{chain}: ROADMAP_REVIEW_STATUS must be COMPLETE, NOT_APPLICABLE, or BLOCKED"
        )
        return errors

    active_endpoint_file = field_value(text, "ACTIVE_ENDPOINT_FILE")
    if not active_endpoint_file:
        errors.append(f"{chain}: ACTIVE.md missing ACTIVE_ENDPOINT_FILE")
        return errors
    endpoint_path = repo_root / active_endpoint_file
    if not endpoint_path.is_file():
        errors.append(f"{chain}: active endpoint missing: {active_endpoint_file}")
        return errors
    endpoint_text = endpoint_path.read_text(encoding="utf-8")
    endpoint_roadmaps = field_value(endpoint_text, "ROADMAPS")
    endpoint_review = field_value(endpoint_text, "ROADMAP_REVIEW_STATUS")
    if endpoint_roadmaps != roadmaps:
        errors.append(f"{chain}: ACTIVE.md ROADMAPS != active endpoint ROADMAPS")
    if endpoint_review != review:
        errors.append(
            f"{chain}: ACTIVE.md ROADMAP_REVIEW_STATUS != active endpoint status"
        )

    if roadmaps.upper().startswith("NONE"):
        if review != "NOT_APPLICABLE":
            errors.append(
                f"{chain}: ROADMAPS NONE requires ROADMAP_REVIEW_STATUS NOT_APPLICABLE"
            )
        return errors

    if review == "NOT_APPLICABLE":
        errors.append(
            f"{chain}: bound roadmaps cannot use ROADMAP_REVIEW_STATUS NOT_APPLICABLE"
        )

    try:
        bindings = parse_bindings(roadmaps)
    except ValueError as exc:
        errors.append(f"{chain}: {exc}")
        return errors

    for rel, expected_blob in bindings:
        rel_path = Path(rel)
        if rel_path.is_absolute() or ".." in rel_path.parts:
            errors.append(f"{chain}: unsafe roadmap path {rel}")
            continue
        roadmap_path = repo_root / rel_path
        if not roadmap_path.is_file():
            errors.append(f"{chain}: roadmap file missing: {rel}")
            continue
        actual_blob = git_blob_sha(roadmap_path)
        if actual_blob != expected_blob:
            errors.append(
                f"{chain}: roadmap binding stale for {rel}: expected {expected_blob}, actual {actual_blob}"
            )

    if review == "BLOCKED" and field_value(text, "STATE") != "BLOCKED":
        errors.append(
            f"{chain}: ROADMAP_REVIEW_STATUS BLOCKED requires chain STATE BLOCKED"
        )

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_roadmap_bindings.py <repo-root-or-agents/chains>", file=sys.stderr)
        return 2

    supplied = Path(sys.argv[1]).resolve()
    if supplied.name == "chains":
        chains_dir = supplied
        repo_root = supplied.parent.parent
    else:
        repo_root = supplied
        chains_dir = repo_root / "agents" / "chains"

    if not chains_dir.is_dir():
        print(f"FAIL: canonical chain store not found: {chains_dir}", file=sys.stderr)
        return 1

    errors = []
    checked = 0
    for chain_dir in sorted(path for path in chains_dir.iterdir() if path.is_dir()):
        active = chain_dir / "ACTIVE.md"
        if not active.is_file():
            continue
        version = field_value(active.read_text(encoding="utf-8"), "CHAIN_STATE_VERSION")
        if version == "2":
            checked += 1
            errors.extend(validate_chain(repo_root, active))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: roadmap bindings ({checked} version-2 chain(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
