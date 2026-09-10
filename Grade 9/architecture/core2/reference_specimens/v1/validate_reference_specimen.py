#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def canonical_sha256(obj) -> str:
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def walk(obj, path="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def main() -> int:
    errors: list[str] = []
    c1 = load("core1-reference.example.json")
    c2 = load("core2-reference.example.json")
    cov = load("coverage-checklist.json")

    for name, obj in (("core1", c1), ("core2", c2)):
        meta = obj.get("specimen_metadata", {})
        if meta.get("artifact_class") != "REFERENCE_EXAMPLE":
            errors.append(f"{name}: artifact_class must be REFERENCE_EXAMPLE")
        if meta.get("placeholder_policy") != "NO_PLACEHOLDERS_IN_MATERIAL_FIELDS":
            errors.append(f"{name}: placeholder policy missing")
        if meta.get("normative_contract") is not False:
            errors.append(f"{name}: reference example must not claim normative-contract status")
        for path, value in walk(obj):
            if isinstance(value, str) and value.strip().upper() in {"TODO", "TBD", "PLACEHOLDER"}:
                errors.append(f"{name}: forbidden placeholder token at {path}")

    rb = c1.get("research_bundle", {})
    manifest = c1.get("manifest", {})
    computed_semantic = canonical_sha256(rb)
    if manifest.get("semantic_digest") != computed_semantic:
        errors.append("core1: semantic_digest does not match canonical reference ResearchBundle")

    expected_package = hashlib.sha256((computed_semantic + "|SL-REF-MOTION-V3").encode("utf-8")).hexdigest()
    if manifest.get("package_digest") != expected_package:
        errors.append("core1: reference package_digest is inconsistent")

    meta2 = c2.get("specimen_metadata", {})
    if meta2.get("research_bundle_id") != rb.get("research_bundle_id"):
        errors.append("core2: ResearchBundle ID differs from Core1 reference")
    if meta2.get("research_package_digest") != manifest.get("package_digest"):
        errors.append("core2: package digest differs from Core1 reference")
    if not c2.get("b40_structure", {}).get("same_research_package") or not c2.get("b90_structure", {}).get("same_research_package"):
        errors.append("core2: B40/B90 must explicitly reuse the same frozen ResearchPackage")

    b40_arcs = [u.get("arc_roles") for u in c2.get("b40_structure", {}).get("learning_units", [])]
    b90_arcs = [u.get("arc_roles") for u in c2.get("b90_structure", {}).get("learning_units", [])]
    if not b40_arcs or not b90_arcs or b40_arcs == b90_arcs:
        errors.append("core2: B40/B90 morphology must differ materially")

    topo = c2.get("transfer_book_excerpt", {})
    if topo.get("section_order") != ["ATTEMPTS", "OPTIONAL_HELP", "COMPLETE_SOLUTIONS", "MIXED_DIAGNOSIS"]:
        errors.append("core2: transfer section order is not mature product-first topology")
    if topo.get("hint_tiers") != ["H1_NOTICE", "H2_MODEL", "H3_START"]:
        errors.append("core2: typed hint ladder is incomplete")

    coverage_states = set(cov.get("specimen_metadata", {}).get("coverage_states", []))
    if coverage_states != {"COVERED", "PARTIAL", "NOT_EXERCISED"}:
        errors.append("coverage checklist has invalid state vocabulary")
    rows = cov.get("features", [])
    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("coverage checklist contains duplicate feature IDs")
    for row in rows:
        if row.get("coverage") not in coverage_states:
            errors.append(f"coverage row {row.get('id')} uses unsupported state")

    if errors:
        print("REFERENCE_SPECIMEN = FAIL")
        for error in errors:
            print("- " + error)
        return 1

    counts = {state: sum(1 for r in rows if r.get("coverage") == state) for state in sorted(coverage_states)}
    print("REFERENCE_SPECIMEN = PASS")
    print(f"CORE1_SEMANTIC_DIGEST = {computed_semantic}")
    print(f"CORE1_PACKAGE_DIGEST = {expected_package}")
    print("B40_B90_SAME_RESEARCH_PACKAGE = PASS")
    print("B40_B90_MORPHOLOGY_DIFFERENCE = PASS")
    print("NO_MATERIAL_PLACEHOLDERS = PASS")
    print("COVERAGE = " + ", ".join(f"{k}:{v}" for k, v in counts.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
