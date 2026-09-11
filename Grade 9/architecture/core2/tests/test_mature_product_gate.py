#!/usr/bin/env python3
"""Regression checks for the mature Core (2) LearningDesign execution gate."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

GRADE9 = Path(__file__).resolve().parents[3]
SCRIPTS = GRADE9 / "skills" / "grade9-core2-publisher" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import mature_product as mature  # noqa: E402


def fixture():
    plan = {
        "publication_plan_id": "PP-1",
        "research_bundle_id": "RB-1",
        "research_package_digest": "a" * 64,
        "learner_profile_id": "LP-1",
        "publication_target_id": "PT-1",
        "subject": "MATHEMATICS",
        "topic_id": "TOPIC-1",
        "delivery_contract": "STUDY_GUIDE_ONLY",
        "sections": [
            {
                "section_id": "SEC-1",
                "concept_id": "CONCEPT-1",
                "instructional_profile": "BRIDGE",
            }
        ],
    }
    design = {
        "mode": "MATURE_LEARNER_PRODUCT",
        **{k: plan[k] for k in (
            "publication_plan_id", "research_bundle_id", "research_package_digest",
            "learner_profile_id", "publication_target_id", "subject", "topic_id",
        )},
        "learning_units": [
            {
                "unit_id": "LU-1",
                "concept_ids": ["CONCEPT-1"],
                "instructional_profile": "BRIDGE",
                "learner_capabilities": [
                    {"capability_id": "LC-1", "type": "EXPLAIN", "required": True},
                    {"capability_id": "LC-2", "type": "TRANSFER", "required": True},
                ],
            }
        ],
    }
    study = {
        "publication_plan_id": "PP-1",
        "product_identity": {"delivery_contract": "STUDY_GUIDE_ONLY", "role": "CORE_STUDY_GUIDE"},
        "main_sections": [
            {
                "section_id": "SEC-1",
                "concept_id": "CONCEPT-1",
                "instructional_profile": "BRIDGE",
                "items": [
                    {
                        "item_id": "ITEM-1",
                        "traceability_class": "MATERIAL",
                        "learning_design_refs": ["LC-1"],
                    },
                    {
                        "item_id": "ITEM-2",
                        "traceability_class": "MATERIAL",
                        "learning_design_refs": ["LC-2"],
                    },
                ],
            }
        ],
        "appendix_A": {"items": []},
        "appendix_B": {"items": []},
        "appendix_C": {"items": []},
    }
    target = {"requested_products": {"study_guide": True, "transfer_book": False}}
    return plan, design, study, target


def main() -> int:
    plan, design, study, target = fixture()

    reference_path = GRADE9 / "architecture" / "core2" / "contracts" / "v1" / "examples" / "learning-design.permutations-bridge.example.json"
    reference = mature.load(reference_path)
    assert mature.validate_learning_design_contract(reference) == []

    missing_design = mature.preflight_errors(
        ["run_core2.py", "--mature-product", "--target", "target.json"],
        target,
        None,
    )
    assert any("--learning-design" in e for e in missing_design), missing_design

    missing_authored = mature.preflight_errors(
        ["run_core2.py", "--learning-design", "ld.json", "--target", "target.json"],
        target,
        design,
    )
    assert any("--study-model" in e for e in missing_authored), missing_authored
    assert any("--publication-structure" in e for e in missing_authored), missing_authored

    complete_argv = [
        "run_core2.py", "--learning-design", "ld.json", "--study-model", "study.json",
        "--publication-structure", "structure.json", "--target", "target.json",
    ]
    assert mature.preflight_errors(complete_argv, target, design) == []
    assert mature.learning_design_binding_errors(design, plan) == []
    assert mature.study_learning_binding_errors(study, plan, design) == []

    no_lineage = copy.deepcopy(study)
    del no_lineage["main_sections"][0]["items"][0]["learning_design_refs"]
    errors = mature.study_learning_binding_errors(no_lineage, plan, design)
    assert any("requires learning_design_refs" in e for e in errors), errors

    unknown_lineage = copy.deepcopy(study)
    unknown_lineage["main_sections"][0]["items"][0]["learning_design_refs"] = ["LC-NOT-REAL"]
    errors = mature.study_learning_binding_errors(unknown_lineage, plan, design)
    assert any("unknown learning_design_refs" in e for e in errors), errors

    uncovered = copy.deepcopy(study)
    uncovered["main_sections"][0]["items"] = uncovered["main_sections"][0]["items"][:1]
    errors = mature.study_learning_binding_errors(uncovered, plan, design)
    assert any("required LearningDesign capabilities have no MATERIAL implementation" in e for e in errors), errors

    drifted_design = copy.deepcopy(design)
    drifted_design["learning_units"][0]["instructional_profile"] = "REFERENCE"
    errors = mature.learning_design_binding_errors(drifted_design, plan)
    assert any("instructional_profile" in e for e in errors), errors

    engineering_argv = ["run_core2.py", "--target", "target.json"]
    assert mature.preflight_errors(engineering_argv, target, None) == []
    assert mature.mature_requested(engineering_argv, None) is False

    accidental_authored = ["run_core2.py", "--target", "target.json", "--study-model", "study.json"]
    errors = mature.preflight_errors(accidental_authored, target, None)
    assert any("only valid for MATURE_LEARNER_PRODUCT" in e for e in errors), errors

    print("CORE2_MATURE_PRODUCT_GATE_REGRESSION = PASS")
    print("MATURE_REQUIRES_LEARNING_DESIGN = PASS")
    print("MATURE_REQUIRES_AUTHORED_STUDY_AND_STRUCTURE = PASS")
    print("LEARNING_DESIGN_TO_MATERIAL_CUSTODY = PASS")
    print("REQUIRED_CAPABILITY_IMPLEMENTATION = PASS")
    print("ENGINEERING_REPLAY_COMPATIBILITY = PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
