#!/usr/bin/env python3
"""Validate canonical Primary Math V2 registries and Grade 4/5 overlays."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "registry"
OVER = ROOT / "overlays"


def fail(msg: str) -> None:
    raise SystemExit(f"Primary Math V2 registry validation failed: {msg}")


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def unique_ids(items, label: str) -> set[str]:
    ids = [item.get("id") for item in items]
    if any(not value for value in ids):
        fail(f"{label} contains missing/empty id")
    if len(ids) != len(set(ids)):
        fail(f"{label} contains duplicate canonical IDs")
    return set(ids)


def main() -> int:
    capabilities_doc = load(REG / "capability_registry.json")
    problems_doc = load(REG / "problem_family_registry.json")
    translations_doc = load(REG / "representation_translation_registry.json")
    grade4 = load(OVER / "generic_grade4.json")
    grade5 = load(OVER / "generic_grade5.json")

    capabilities = capabilities_doc.get("capabilities") or []
    problems = problems_doc.get("problem_families") or []
    translations = translations_doc.get("translations") or []

    cap_ids = unique_ids(capabilities, "capability registry")
    unique_ids(problems, "problem-family registry")
    unique_ids(translations, "representation-translation registry")

    required_domains = {
        "NUMBER_PLACE_VALUE", "ADDITION_SUBTRACTION", "MULTIPLICATION", "DIVISION",
        "FACTORS_MULTIPLES", "FRACTIONS", "DECIMALS", "DECIMAL_PERCENT_RATIO",
        "PATTERNS_EQUALITY", "MEASUREMENT", "MENSURATION", "GEOMETRY", "DATA",
        "WORD_PROBLEMS_MODELLING", "REASONING_TRANSFER",
    }
    domains = {item.get("domain") for item in capabilities}
    missing_domains = sorted(required_domains - domains)
    if missing_domains:
        fail(f"capability envelope missing domains: {missing_domains}")

    for item in translations:
        refs = item.get("capability_refs") or []
        if not refs:
            fail(f"translation {item['id']} has no capability refs")
        dangling = sorted(set(refs) - cap_ids)
        if dangling:
            fail(f"translation {item['id']} has dangling capability refs: {dangling}")
        if not item.get("from") or not item.get("to") or item["from"] == item["to"]:
            fail(f"translation {item['id']} must have distinct source/target representations")

    if "keyword" not in (problems_doc.get("rule") or "").lower():
        fail("problem-family registry must explicitly reject keyword-only operation routing")

    for overlay in (grade4, grade5):
        oid = overlay.get("overlay_id")
        if overlay.get("profile_status") != "NON_NORMATIVE_REFERENCE_PROFILE":
            fail(f"{oid} must remain a non-normative reference profile")
        if "capabilities" in overlay:
            fail(f"{oid} clones capability objects instead of referencing canonical IDs")
        common = overlay.get("common_reference") or []
        sensitive = overlay.get("scope_sensitive") or []
        all_refs = common + sensitive
        if len(all_refs) != len(set(all_refs)):
            fail(f"{oid} repeats a capability across activation states")
        dangling = sorted(set(all_refs) - cap_ids)
        if dangling:
            fail(f"{oid} has dangling capability refs: {dangling}")
        if not overlay.get("rule") or "authoritative" not in overlay["rule"].lower():
            fail(f"{oid} must state that project curriculum/source/question scope remains authoritative")

    # Deep benchmark seams must exist regardless of overlay activation.
    required_deep = {
        "MULT_EQUAL_GROUPS", "MULT_ARRAY", "MULT_DISTRIBUTIVE", "MULT_PARTIAL_PRODUCTS", "MULT_WRITTEN_ALGORITHM",
        "DIV_SHARE_GROUP_DISTINCTION", "DIV_ARRAY_BAR", "DIV_PLACE_VALUE_DECOMPOSITION", "DIV_PARTIAL_QUOTIENT",
        "DIV_WRITTEN_MULTI_DIGIT_DIVISOR", "DIV_QUOTIENT_ZERO_PLACE", "DIV_REMAINDER_CONTEXT",
        "FRAC_PART_WHOLE", "FRAC_NUMBER_LINE", "FRAC_EQUIVALENCE",
        "MODEL_QUANTITY_STRUCTURE", "REASON_ERROR_ANALYSIS",
    }
    missing_deep = sorted(required_deep - cap_ids)
    if missing_deep:
        fail(f"deep benchmark capabilities missing: {missing_deep}")

    print(f"Primary Math V2 registries: PASS ({len(cap_ids)} capabilities, {len(problems)} problem families, {len(translations)} translations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
