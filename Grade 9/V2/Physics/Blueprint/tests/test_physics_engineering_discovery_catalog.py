#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from validate_engineering_discovery_catalog import DiscoveryCatalogError, load, validate  # noqa: E402


def expect_code(catalog: dict, code: str) -> None:
    try:
        validate(catalog)
    except DiscoveryCatalogError as exc:
        if exc.code != code:
            raise AssertionError(f"expected {code}, got {exc.code}: {exc.message}") from exc
        return
    raise AssertionError(f"expected rejection with {code}")


def main() -> None:
    catalog = load("policy/physics-engineering-discovery-catalog.pr383.v1.json")
    result = validate(catalog)

    assert result["status"] == "PASS"
    assert result["discovered_subtopic_count"] == 43
    assert result["exact_v3_count"] == 12
    assert result["mapped_v3_target_count"] == 2
    assert result["migration_required_count"] == 30
    assert result["v3_native_or_refined_count"] == 9
    assert result["canonical_v3_gate_count"] == 23
    assert result["case_artifacts_role"] == "STRESS_TEST_ONLY"
    assert result["readiness_rule"] == "DERIVED_BY_PRODUCTION_V3_VALIDATOR"

    grav = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-GRAV-UNIVERSAL-LAW")
    assert grav["disposition"] == "MAPPED_V3"
    assert grav["v3_gate_ids"] == ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
    assert grav["mapping_review_ref"] == "provenance/pr383/mapping-reviews/PHY-GRAV-UNIVERSAL-LAW.v1.json"

    bad = copy.deepcopy(catalog)
    bad["discovered_subtopics"].pop()
    expect_code(bad, "E_ENG_DISCOVERY_COUNT_MISMATCH")

    bad = copy.deepcopy(catalog)
    row = next(x for x in bad["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-VEC-BASICS")
    row["disposition"] = "MIGRATION_REQUIRED"
    row["v3_gate_ids"] = []
    expect_code(bad, "E_ENG_DISCOVERY_STALE_MIGRATION_HOLD")

    bad = copy.deepcopy(catalog)
    row = next(x for x in bad["discovered_subtopics"] if x["disposition"] == "MIGRATION_REQUIRED")
    row["disposition"] = "EXACT_V3_ID"
    row["v3_gate_ids"] = [row["discovery_gate_id"]]
    expect_code(bad, "E_ENG_DISCOVERY_EXACT_ID_MISSING")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].remove("PHY-M2D-MOVING-LAUNCHER")
    expect_code(bad, "E_ENG_DISCOVERY_V3_UNRECONCILED")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-FAKE-NOT-A-GATE")
    expect_code(bad, "E_ENG_DISCOVERY_NATIVE_GATE_MISSING")

    bad = copy.deepcopy(catalog)
    row = next(x for x in bad["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-GRAV-UNIVERSAL-LAW")
    row["mapping_review_ref"] = "provenance/pr383/mapping-reviews/DOES-NOT-EXIST.json"
    expect_code(bad, "E_ENG_DISCOVERY_MAPPING_REVIEW_INVALID")

    bad = copy.deepcopy(catalog)
    row = next(x for x in bad["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-GRAV-UNIVERSAL-LAW")
    row["v3_gate_ids"] = ["PHY-GRAV-FORCE"]
    expect_code(bad, "E_ENG_DISCOVERY_MAPPING_REVIEW_INVALID")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-GRAV-FORCE")
    expect_code(bad, "E_ENG_DISCOVERY_DOUBLE_CLASSIFIED")

    bad = copy.deepcopy(catalog)
    row = next(x for x in bad["discovered_subtopics"] if x["disposition"] == "MIGRATION_REQUIRED")
    row["disposition"] = "MAPPED_V3"
    row["v3_gate_ids"] = ["PHY-M2D-PROJECTILE-COMPONENTS"]
    expect_code(bad, "E_ENG_DISCOVERY_SCHEMA")

    bad = copy.deepcopy(catalog)
    bad["discovered_subtopics"][0]["stress_test_ref"] = "Q15"
    expect_code(bad, "E_ENG_DISCOVERY_SCHEMA")

    bad = copy.deepcopy(catalog)
    bad["stress_test_policy"]["may_define_gate_logic"] = True
    expect_code(bad, "E_ENG_DISCOVERY_SCHEMA")

    bad = copy.deepcopy(catalog)
    bad["stress_test_policy"]["may_promote_source_custody"] = True
    expect_code(bad, "E_ENG_DISCOVERY_SCHEMA")

    print("Physics engineering discovery reconciliation: PASS")
    print(result)


if __name__ == "__main__":
    main()
