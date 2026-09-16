#!/usr/bin/env python3
from __future__ import annotations

import copy
import runpy
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
    assert result["exact_v3_count"] == 14
    assert result["mapped_v3_target_count"] == 12
    assert result["migration_required_count"] == 24
    assert result["v3_native_or_refined_count"] == 5
    assert result["canonical_v3_gate_count"] == 26
    assert result["case_artifacts_role"] == "STRESS_TEST_ONLY"
    assert result["readiness_rule"] == "DERIVED_BY_PRODUCTION_V3_VALIDATOR"

    grav = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-GRAV-UNIVERSAL-LAW")
    assert grav["disposition"] == "MAPPED_V3"
    assert grav["v3_gate_ids"] == ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
    assert grav["mapping_review_ref"] == "provenance/pr383/mapping-reviews/PHY-GRAV-UNIVERSAL-LAW.v1.json"

    free_fall = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-GRAV-FREE-FALL")
    assert free_fall["disposition"] == "MAPPED_V3"
    assert free_fall["v3_gate_ids"] == [
        "PHY-GRAV-FORCE",
        "PHY-GRAV-FIELD",
        "PHY-M2D-PROJECTILE-COMPONENTS",
        "PHY-M2D-SHARED-CLOCK",
        "PHY-M2D-VELOCITY-EVOLUTION",
        "PHY-M2D-SAME-HEIGHT-VELOCITY",
    ]
    assert free_fall["mapping_review_ref"] == "provenance/pr383/mapping-reviews/PHY-GRAV-FREE-FALL.v1.json"

    newton = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-FORCE-NEWTON-LAWS")
    assert newton["disposition"] == "MAPPED_V3"
    assert newton["v3_gate_ids"] == [
        "PHY-NLM-INTERACTION",
        "PHY-NLM-FBD",
        "PHY-NLM-FIRST-LAW",
        "PHY-NLM-SECOND-LAW",
        "PHY-NLM-THIRD-LAW",
    ]
    assert newton["mapping_review_ref"] == "provenance/pr383/mapping-reviews/PHY-FORCE-NEWTON-LAWS.v1.json"

    projectile = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-KIN-2D-PROJECTILE")
    assert projectile["disposition"] == "MAPPED_V3"
    assert projectile["v3_gate_ids"] == [
        "PHY-M2D-PROJECTILE-COMPONENTS",
        "PHY-M2D-SHARED-CLOCK",
        "PHY-M2D-VELOCITY-EVOLUTION",
    ]
    assert projectile["mapping_review_ref"] == "provenance/pr383/mapping-reviews/PHY-KIN-2D-PROJECTILE.v1.json"

    relative = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-KIN-RELATIVE-2D")
    assert relative["disposition"] == "MAPPED_V3"
    assert relative["v3_gate_ids"] == ["PHY-M2D-RELATIVE-VELOCITY"]
    assert relative["mapping_review_ref"] == "provenance/pr383/mapping-reviews/PHY-KIN-RELATIVE-2D.v1.json"

    work = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-WORK-ENERGY-POWER")
    conservation = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-ENERGY-CONSERVATION-LAW")
    variable = next(x for x in catalog["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-WEP-VARIABLE-FORCE")
    assert work["disposition"] == "EXACT_V3_ID" and work["v3_gate_ids"] == ["PHY-WORK-ENERGY-POWER"]
    assert conservation["disposition"] == "EXACT_V3_ID" and conservation["v3_gate_ids"] == ["PHY-ENERGY-CONSERVATION-LAW"]
    assert variable["disposition"] == "MIGRATION_REQUIRED" and variable["v3_gate_ids"] == []

    exact_ids = {
        row["discovery_gate_id"]
        for row in catalog["discovered_subtopics"]
        if row["disposition"] == "EXACT_V3_ID"
    }
    assert set(newton["v3_gate_ids"]).issubset(exact_ids)

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
    row = next(x for x in bad["discovered_subtopics"] if x["discovery_gate_id"] == "PHY-GRAV-FREE-FALL")
    row["v3_gate_ids"] = ["PHY-GRAV-FORCE", "PHY-GRAV-FIELD"]
    expect_code(bad, "E_ENG_DISCOVERY_MAPPING_REVIEW_INVALID")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-GRAV-FORCE")
    expect_code(bad, "E_ENG_DISCOVERY_DOUBLE_CLASSIFIED")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-NLM-SECOND-LAW")
    expect_code(bad, "E_ENG_DISCOVERY_DOUBLE_CLASSIFIED")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-M2D-PROJECTILE-COMPONENTS")
    expect_code(bad, "E_ENG_DISCOVERY_DOUBLE_CLASSIFIED")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-M2D-RELATIVE-VELOCITY")
    expect_code(bad, "E_ENG_DISCOVERY_DOUBLE_CLASSIFIED")

    bad = copy.deepcopy(catalog)
    bad["v3_native_or_refined_gate_ids"].append("PHY-M2D-SAME-HEIGHT-VELOCITY")
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

    integration = runpy.run_path(str(ROOT / "tests" / "test_pr402_observability_integration.py"))
    integration["main"]()

    print("Physics engineering discovery reconciliation: PASS")
    print(result)


if __name__ == "__main__":
    main()
