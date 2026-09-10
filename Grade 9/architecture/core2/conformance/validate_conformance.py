#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str):
    with (ROOT / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    errors: list[str] = []
    matrix = load("pr156-pr157-conformance.v1.json")
    rows = matrix.get("rows", [])
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate conformance row id")
    blocking = [r for r in rows if r.get("blocking")]
    incomplete = [r for r in blocking if r.get("status") != "IMPLEMENTED"]
    if incomplete:
        errors.extend(f"blocking invariant not implemented: {r.get('id')} {r.get('invariant')}" for r in incomplete)
    for name, subject, ancestor in (
        ("physics-pr156.profile.json", "PHYSICS", "PR156"),
        ("chemistry-pr157.profile.json", "CHEMISTRY", "PR157"),
    ):
        profile = load(name)
        if profile.get("subject") != subject or profile.get("inherits_from") != ancestor:
            errors.append(f"invalid subject profile identity: {name}")
        if profile.get("delivery_contract") != "FULL_TOPIC_PAIR":
            errors.append(f"{name} must require FULL_TOPIC_PAIR")
        if set(profile.get("required_products", [])) != {"CORE_STUDY_GUIDE", "EXAMSIDE_SOLUTION_TRANSFER"}:
            errors.append(f"{name} must require the mature two-product pair")
        human = profile.get("human_review", {})
        if not human.get("required") or human.get("minimum_render_dpi", 0) < 200 or not human.get("all_pages") or not human.get("bind_exact_pdf_hashes"):
            errors.append(f"{name} weakens mature human visual-review binding")
    if errors:
        print("PR156_PR157_CONFORMANCE = FAIL")
        for e in errors:
            print("- " + e)
        return 1
    print("PR156_PR157_CONFORMANCE = PASS")
    print(f"BLOCKING_INVARIANTS = {len(blocking)}")
    print("PHYSICS_PR156_PROFILE = PASS")
    print("CHEMISTRY_PR157_PROFILE = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
