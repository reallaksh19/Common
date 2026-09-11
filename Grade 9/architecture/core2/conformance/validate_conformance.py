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

    retirement_required = [r for r in rows if r.get("retirement_required")]
    retirement_pending = [r for r in retirement_required if r.get("status") != "IMPLEMENTED"]

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

        structure = profile.get("study_guide_structure_requirements", {})
        for key in (
            "publication_structure_required",
            "product_first",
            "one_cognitive_job_per_page_intent",
            "new_relation_requires_model_or_notice_before_build",
            "high_baseline_may_compress_support_with_reason",
            "retrieval_check_required",
            "attempt_before_help",
            "bidirectional_navigation",
        ):
            if structure.get(key) is not True:
                errors.append(f"{name} weakens product-first structure requirement: {key}")
        if structure.get("static_hint_delivery") != "SEPARATE_HELP_SECTION":
            errors.append(f"{name} must spatially separate optional help in static PDFs")
        required_progression = ["WORKED_EXAMPLE", "GUIDED_1", "GUIDED_2_FADED", "INDEPENDENT_TRANSFER"]
        if structure.get("bridge_foundation_support_progression") != required_progression:
            errors.append(f"{name} must preserve worked -> guided -> faded -> independent progression")

        human = profile.get("human_review", {})
        if not human.get("required") or human.get("minimum_render_dpi", 0) < 200 or not human.get("all_pages") or not human.get("bind_exact_pdf_hashes"):
            errors.append(f"{name} weakens mature human visual-review binding")

    if errors:
        print("PR156_PR157_CONFORMANCE = FAIL")
        for e in errors:
            print("- " + e)
        return 1

    print("PR156_PR157_CONTRACT_CONFORMANCE = PASS")
    print(f"BLOCKING_INVARIANTS = {len(blocking)}")
    print("PHYSICS_PR156_PROFILE = PASS")
    print("CHEMISTRY_PR157_PROFILE = PASS")
    print("PRODUCT_FIRST_STRUCTURE_PROFILE = PASS")
    if retirement_pending:
        print("PR156_PR157_RETIREMENT = PENDING")
        for row in retirement_pending:
            print(f"- {row.get('id')} {row.get('status')}: {row.get('invariant')}")
    else:
        print("PR156_PR157_RETIREMENT = ELIGIBLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
