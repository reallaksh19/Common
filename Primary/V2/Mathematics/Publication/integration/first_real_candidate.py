#!/usr/bin/env python3
"""Build the first exact PR #327 REAL_CANDIDATE for independent #325 evaluation.

This producer does not import benchmark expected values at runtime.  The case
realizations below are producer-owned integration fixtures implementing issue
#334.  Acceptance is recomputed later by the unmodified #325 evaluator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Primary.V2.Mathematics.Publication.engine.page_composer import PrimaryPageComposer
from Primary.V2.Mathematics.Publication.engine.surface_guard import LearnerSurfaceGuard


CANDIDATE_ID = "PRIMARY-MATH-V2-PR327-REAL-CANDIDATE-001"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pc(kind: str, case_id: str, params: Mapping[str, Any]) -> Dict[str, Any]:
    return {"kind": f"{kind}__{case_id}", "params": dict(params)}


def text_section(case_id: str, title: str, content: str, role: str = "CHECK") -> Dict[str, Any]:
    return {
        "section_type": f"{role}__{case_id}",
        "title": title,
        "content": content,
    }


def visual_section(case_id: str, title: str, call: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "section_type": "MAKE_DRAW_REPRESENT",
        "title": title,
        "content": "Use the model to connect the quantities and the calculation.",
        "primitive_call": dict(call),
    }


def module(title: str, sections: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    return {"title": title, "sections": [dict(x) for x in sections]}


def build_core1_plan() -> Dict[str, Any]:
    modules: List[Dict[str, Any]] = []

    cid = "PMV2-MUL-BRIDGE-23X6"
    modules.append(module("23 × 6: from groups to written multiplication", [
        visual_section(cid, "Six equal groups of 23", pc("EQUAL_GROUPS", cid, {"group_count": 6, "items_per_group": 23})),
        visual_section(cid, "See the same product as an array", pc("ARRAY", cid, {"rows": 6, "cols": 23})),
        visual_section(cid, "Split 23 into 20 + 3", pc("AREA_MODEL", cid, {"factors": [23, 6], "partitions": [{"length": 20, "height": 6, "area": 120}, {"length": 3, "height": 6, "area": 18}]})),
        visual_section(cid, "Combine the partial products", pc("PARTIAL_PRODUCTS", cid, {"factors": [23, 6], "partial_products": [120, 18], "product": 138})),
        visual_section(cid, "Write the multiplication carefully", pc("VERTICAL_MULTIPLICATION", cid, {"factors": [23, 6], "partial_products": [18, 120], "total_product": 138, "tier": "AUTHORED_NOTEBOOK_EXAMPLE"})),
        visual_section(cid, "Check whether 138 is reasonable", pc("ESTIMATE_CHECK", cid, {"actual": 138, "estimate_expr": "20 × 6 = 120", "reasoning": "23 is a little more than 20, so 138 should be a little more than 120."})),
    ]))

    cid = "PMV2-DIV-SHARE-GROUP-24-6"
    modules.append(module("24 ÷ 6 can ask two different questions", [
        visual_section(cid, "Sharing: 24 shared among 6 groups", pc("DIVISION_SHARING_VS_GROUPING", cid, {"dividend": 24, "divisor": 6, "quotient": 4, "meaning": "SHARING"})),
        visual_section(cid, "Grouping: make groups of 6 from 24", pc("DIVISION_SHARING_VS_GROUPING", cid, {"dividend": 24, "divisor": 6, "quotient": 4, "meaning": "GROUPING"})),
        text_section(cid, "Connect both meanings to the equation", "24 ÷ 6 = 4. In sharing, 4 is the size of each group. In grouping, 4 is the number of groups.", "DIVISION_EQUATION"),
    ]))

    division_cases = [
        ("PMV2-DIV-ZERO-366-12", 366, 12, 30, 6, [3, 0], [12,24,36,48,60], [
            {"type":"SUBTRACTION","value":36,"col":1}, {"type":"BRING_DOWN","value":6,"col":2}, {"type":"REMAINDER","value":6,"col":2}
        ]),
        ("PMV2-DIV-ZERO-7843-13", 7843, 13, 603, 4, [6,0,3], [13,26,39,52,65,78,91,104,117,130], [
            {"type":"SUBTRACTION","value":78,"col":1}, {"type":"BRING_DOWN","value":4,"col":2}, {"type":"SUBTRACTION","value":0,"col":2}, {"type":"BRING_DOWN","value":3,"col":3}, {"type":"SUBTRACTION","value":39,"col":3}, {"type":"REMAINDER","value":4,"col":3}
        ]),
        ("PMV2-DIV-CONTRAST-3496-23", 3496, 23, 152, 0, [1,5,2], [23,46,69,92,115,138,161,184,207,230], [
            {"type":"SUBTRACTION","value":23,"col":1}, {"type":"BRING_DOWN","value":9,"col":2}, {"type":"SUBTRACTION","value":115,"col":2}, {"type":"BRING_DOWN","value":6,"col":3}, {"type":"SUBTRACTION","value":46,"col":3}
        ]),
    ]
    for cid, dividend, divisor, quotient, remainder, digits, multiples, steps in division_cases:
        modules.append(module(f"Written division: {dividend} ÷ {divisor}", [
            visual_section(cid, "Keep every quotient place visible", pc("LONG_DIVISION_WORKOUT", cid, {
                "dividend": dividend, "divisor": divisor, "quotient": quotient, "remainder": remainder,
                "quotient_digits": digits, "multiples_table": multiples, "steps": steps,
                "provenance_tier": "AUTHORED_NOTEBOOK_EXAMPLE", "actor": "SYSTEM", "claims_original_handwriting": False,
            })),
            text_section(cid, "Check with multiplication", f"Check: {divisor} × {quotient} + {remainder} = {dividend}.", "MULTIPLICATION_CHECK"),
        ]))

    cid = "PMV2-DIV-DIAGNOSTIC-ZERO-CONTRAST"
    modules.append(module("Compare division cases before deciding what needs repair", [
        text_section(cid, "What changes when a quotient place needs zero?", "Compare 366 ÷ 12 and 7843 ÷ 13 with 3496 ÷ 23. Focus only on whether a zero quotient place is required; keep the rest of the task as similar as possible.", "COMPARE"),
    ]))

    cid = "PMV2-DIV-REMAINDER-CONTEXT"
    modules.append(module("A remainder changes meaning with the story", [
        visual_section(cid, "29 children need vans that seat 6", pc("DIVISION_REMAINDER_CONTEXT", cid, {
            "dividend": 29, "divisor": 6, "quotient": 4, "remainder": 5,
            "action": "ROUND_UP_ONE_MORE_GROUP", "final_answer": 5,
            "explanation": "Four full vans seat 24 children; the remaining 5 children need one more van."
        })),
    ]))

    cid = "PMV2-UNIT-DOZEN-MONEY"
    modules.append(module("Keep units visible through a two-step word problem", [
        visual_section(cid, "23 dozen eggs at 6 currency units per egg", pc("UNIT_CHAIN", cid, {"unit_steps": [
            {"quantity": 23, "unit": "DOZEN"},
            {"multiplier": 12, "result_quantity": 276, "unit": "EGG"},
            {"rate": 6, "result_value": 1656, "unit": "CURRENCY"}
        ]})),
        text_section(cid, "Write both relationships", "23 dozen × 12 = 276 eggs; then 276 eggs × 6 per egg = 1656 currency units.", "MULTI_STEP_EQUATION"),
    ]))

    cid = "PMV2-FRAC-EQUIV-1-2"
    modules.append(module("Equivalent fractions name the same amount", [
        visual_section(cid, "One half", pc("FRACTION_STRIP", cid, {"numerator": 1, "denominator": 2, "label": "1/2"})),
        visual_section(cid, "Two fourths", pc("FRACTION_STRIP", cid, {"numerator": 2, "denominator": 4, "label": "2/4"})),
        visual_section(cid, "Four eighths", pc("FRACTION_STRIP", cid, {"numerator": 4, "denominator": 8, "label": "4/8"})),
        visual_section(cid, "Find the same point on a number line", pc("FRACTION_NUMBER_LINE", cid, {"fractions": [[1,2],[2,4],[4,8]]})),
        text_section(cid, "Explain the bridge", "The whole is the same size each time. The parts are equal within each partition, and 1/2, 2/4 and 4/8 land at the same value.", "EQUIVALENCE_BRIDGE"),
    ]))

    cid = "PMV2-FRAC-ADD-1-2-1-4"
    modules.append(module("Add fractions by making same-size parts", [
        visual_section(cid, "Repartition 1/2 into fourths", pc("FRACTION_ADDITION_REPARTITION", cid, {"left": [1,2], "right": [1,4], "result": [3,4]})),
    ]))

    cid = "PMV2-PLACEVALUE-5043"
    modules.append(module("A zero place still has a job", [
        visual_section(cid, "Read 5043 by place value", pc("PLACE_VALUE_BLOCKS", cid, {"number": 5043, "expanded": [5000, 0, 40, 3]})),
    ]))

    cid = "PMV2-DECIMAL-0-37"
    modules.append(module("0.37 means thirty-seven hundredths", [
        visual_section(cid, "Shade 37 of 100 equal squares", pc("DECIMAL_HUNDRED_GRID", cid, {"decimal_value": 0.37, "grid_shaded_cells": 37})),
        text_section(cid, "Connect the places", "0.37 = 3 tenths + 7 hundredths = 37 hundredths.", "DECIMAL_PLACE_VALUE"),
        visual_section(cid, "Locate 0.37 on a number line", pc("DECIMAL_NUMBER_LINE", cid, {"min_val": 0.0, "max_val": 1.0, "target_val": 0.37})),
    ]))

    cid = "PMV2-MEASURE-M-TO-CM"
    modules.append(module("Convert metres to centimetres", [
        visual_section(cid, "3 metres equals 300 centimetres", pc("MEASUREMENT_CONVERSION", cid, {"from_value": 3, "from_unit": "M", "factor": 100, "to_value": 300, "to_unit": "CM"})),
    ]))

    cid = "PMV2-PERIMETER-AREA-RECT-6X4"
    modules.append(module("Boundary length is not area", [
        visual_section(cid, "A 6 by 4 rectangle", pc("RECTILINEAR_PERIMETER_AREA", cid, {"width": 6, "height": 4, "perimeter": 20, "area": 24, "unit": "cm"})),
    ]))

    cid = "PMV2-VOLUME-3X2X4"
    modules.append(module("Build volume from cube layers", [
        visual_section(cid, "3 × 2 × 4 makes 24 unit cubes", pc("VOLUME_CUBE_LAYERS", cid, {"length": 3, "width": 2, "height": 4, "total_cubes": 24})),
    ]))

    cid = "PMV2-ANGLE-65"
    modules.append(module("Measure an acute angle", [
        visual_section(cid, "A 65 degree angle", pc("GEOMETRIC_ANGLE", cid, {"angle_degrees": 65, "classification": "ACUTE"})),
        text_section(cid, "Compare with a right angle", "65° is less than 90°, so the angle is acute. Measure the turn from one ray to the other.", "PROTRACTOR_OR_TURN"),
    ]))

    cid = "PMV2-DATA-BAR-SCALE-5"
    modules.append(module("Read the scale before reading a bar", [
        visual_section(cid, "Each step on the scale is 5", pc("DATA_BAR_CHART", cid, {"categories": ["A","B","C"], "values": [10,25,15], "scale_unit": 5})),
    ]))

    cid = "PMV2-WORK-PROVENANCE-MIXED-SUCCESS"
    modules.append(module("A wrong final answer can contain useful correct thinking", [
        visual_section(cid, "Replay only what the learner work actually shows", pc("LONG_DIVISION_WORKOUT", cid, {
            "dividend": 7843, "divisor": 13, "quotient": 603, "remainder": 4,
            "quotient_digits": [6,0,3],
            "steps": [{"type":"SUBTRACTION","value":78,"col":1},{"type":"BRING_DOWN","value":4,"col":2},{"type":"SUBTRACTION","value":0,"col":2}],
            "provenance_tier": "STRUCTURED_REPLAY", "actor": "CHILD", "claims_original_handwriting": False,
        })),
        text_section(cid, "Keep uncertainty visible", "One intermediate fact is correct. One written place is ambiguous. Teacher correction is recorded separately rather than rewritten as the learner's original work.", "WORK_PROVENANCE"),
    ]))

    return {
        "title": "Primary Mathematics Core 1 — Visual Study Guide",
        "topic": "Grade 4–5 concept bridges and mathematical representations",
        "grade_level": "4–5",
        "modules": modules,
    }


def build_core2_plan() -> Dict[str, Any]:
    return {
        "companion_id": "Primary Mathematics Learning Companion",
        "linked_core1_id": "Primary Mathematics Visual Study Guide",
        "appendix_a": {
            "batches": [
                {
                    "batch_id": "Build",
                    "title": "Build the idea",
                    "practice_role": "BUILD",
                    "items": [
                        {"item_id": "Practice 1", "prompt": "Calculate 24 × 5. Show a split that makes the multiplication easier."},
                        {"item_id": "Practice 2", "prompt": "Divide 488 by 12. Keep every quotient place visible, then check with multiplication."},
                        {"item_id": "Practice 3", "prompt": "Show why 3/6 and 1/2 are equivalent using a strip or number line."},
                    ],
                },
                {
                    "batch_id": "Choose",
                    "title": "Choose a useful model",
                    "practice_role": "CHOOSE",
                    "items": [
                        {"item_id": "Practice 4", "prompt": "Thirty items are shared equally among 5 children. What is unknown: group size or number of groups? Solve."},
                        {"item_id": "Practice 5", "prompt": "A rectangle is 7 cm by 3 cm. Find both perimeter and area and explain the difference."},
                    ],
                },
                {
                    "batch_id": "Transfer",
                    "title": "Transfer the relationship",
                    "practice_role": "TRANSFER",
                    "items": [
                        {"item_id": "Practice 6", "prompt": "Six shelves hold 31 books each. Find the total and choose a representation that helps you check."},
                        {"item_id": "Practice 7", "prompt": "53 people need tables that seat 10. How many tables are needed? Explain what the remainder means."},
                    ],
                },
            ]
        },
        "appendix_b": {
            "ladders": [
                {
                    "item_id": "Practice 1",
                    "H0_try": "Try 24 × 5 independently.",
                    "H1_notice": "Notice that 24 can be split into 20 and 4.",
                    "H2_remember": "Multiply each part by 5, then combine the partial products.",
                    "H3_represent": "Draw an area model split into 20 × 5 and 4 × 5.",
                    "fresh_independent_retry_H0": "Now try 25 × 4 independently."
                },
                {
                    "item_id": "Practice 2",
                    "H0_try": "Try 488 ÷ 12 independently.",
                    "H1_notice": "After each bring-down, ask how many groups of 12 fit in that place.",
                    "H2_remember": "If none fit after quotient construction has begun, write 0 in that quotient place.",
                    "H3_represent": "Use quotient place boxes so every place stays visible.",
                    "fresh_independent_retry_H0": "Now try 605 ÷ 15 independently."
                },
            ]
        },
        "appendix_c": {
            "title": "Appendix C — Visual Quick Reference",
            "decision_aid_name": "Split → represent → calculate → check",
            "primitive_call": pc("AREA_MODEL", "PMV2-HINT-FADE-FRESH-RETRY", {
                "factors": [23,6],
                "partitions": [{"length":20,"height":6,"area":120},{"length":3,"height":6,"area":18}]
            }),
        },
    }


def semantic_manifests() -> Dict[str, Any]:
    diagnostic = {
        "case_id": "PMV2-DIV-DIAGNOSTIC-ZERO-CONTRAST",
        "focal_feature": "QUOTIENT_ZERO_REQUIRED",
        "positive_cases": ["PMV2-DIV-ZERO-366-12", "PMV2-DIV-ZERO-7843-13"],
        "negative_cases": ["PMV2-DIV-CONTRAST-3496-23"],
        "learner_label": None,
        "competing_hypotheses": [
            {"hypothesis_id":"H-DIV-GENERAL","error_signature":"DIV_GENERAL_LONG_DIVISION_PROCEDURE","durable_trait":False},
            {"hypothesis_id":"H-DIV-ZERO","error_signature":"DIV_QUOTIENT_ZERO_PLACE_VALUE","durable_trait":False},
        ],
        "probe": {
            "hypothesis_ids": ["H-DIV-GENERAL", "H-DIV-ZERO"],
            "manipulated_feature": "QUOTIENT_ZERO_REQUIRED",
            "controlled_load": {"language":"LOW","representation_novelty":"LOW","fact_retrieval_demand":"LOW"},
            "outcome_rules": [
                {"no_zero":"CORRECT","zero":"INCORRECT","increase":"H-DIV-ZERO"},
                {"no_zero":"INCORRECT","zero":"INCORRECT","keep_open":["H-DIV-GENERAL","H-DIV-ZERO"]},
            ],
        },
    }
    work = {
        "case_id": "PMV2-WORK-PROVENANCE-MIXED-SUCCESS",
        "final_correctness": "INCORRECT",
        "steps": [
            {"id":"WS-01","kind":"FACT_RETRIEVAL","status":"CORRECT","actor":"CHILD"},
            {"id":"WS-02","kind":"PLACE_VALUE_WRITE","status":"AMBIGUOUS","actor":"CHILD"},
            {"id":"WS-03","kind":"SUBTRACTION","status":"INCORRECT","actor":"CHILD"},
        ],
        "teacher_annotations": [{"actor":"TEACHER","relation_to_step":"WS-02","kind":"CORRECTION"}],
        "replay_provenance": "STRUCTURED_REPLAY",
    }
    runtime = {
        "case_id": "PMV2-ROUTE-CHANGE-AFTER-REPEAT-FAILURE",
        "same_route_failures": 2,
        "route_changed": True,
        "changed_dimension": "REPRESENTATION",
        "conceptual_support": "H3_REPRESENT",
        "access_adjustment": "NONE",
        "independent_retry_after_repair": True,
    }
    return {"diagnostic": diagnostic, "work": work, "runtime": runtime}


def producer_case_evidence() -> List[Dict[str, Any]]:
    return [
        {"case_id":"PMV2-MUL-BRIDGE-23X6","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["EQUAL_GROUPS","ARRAY","DISTRIBUTIVE_AREA","PARTIAL_PRODUCTS","WRITTEN_ALGORITHM","CHECK"],"math_evidence":{"a":23,"b":6,"split":[20,3],"partial_products":[120,18],"product":138,"check_product":138},"product_evidence":{"core1_ref":"multiplication-bridge","core2_practice_ref":"Practice 1","raw_question_direct_render":False}},
        {"case_id":"PMV2-DIV-SHARE-GROUP-24-6","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["EQUAL_SHARE","EQUAL_GROUP","DIVISION_EQUATION"],"math_evidence":{"sharing":{"total":24,"group_count":6,"group_size":4,"unknown_role":"GROUP_SIZE"},"grouping":{"total":24,"group_size":6,"group_count":4,"unknown_role":"GROUP_COUNT"}}},
        {"case_id":"PMV2-DIV-ZERO-366-12","scope":{"basis":"QUESTION_SET_OBSERVED","universal_grade_claim":False},"representations":["WRITTEN_DIVISION","QUOTIENT_PLACE_SLOTS","MULTIPLICATION_CHECK"],"math_evidence":{"dividend":366,"divisor":12,"quotient":30,"remainder":6,"quotient_digits":[3,0],"zero_place_preserved":True},"product_evidence":{"core1_ref":"division-zero-place","core2_practice_ref":"Practice 2","raw_question_direct_render":False}},
        {"case_id":"PMV2-DIV-ZERO-7843-13","scope":{"basis":"QUESTION_SET_OBSERVED","universal_grade_claim":False},"representations":["WRITTEN_DIVISION","QUOTIENT_PLACE_SLOTS","MULTIPLICATION_CHECK"],"math_evidence":{"dividend":7843,"divisor":13,"quotient":603,"remainder":4,"quotient_digits":[6,0,3],"zero_place_preserved":True},"work_evidence":{"final_correctness":"INCORRECT","steps":[{"id":"w1","status":"CORRECT"},{"id":"w2","status":"AMBIGUOUS"}],"teacher_annotations":[{"actor":"TEACHER","kind":"CORRECTION"}],"replay_provenance":"STRUCTURED_REPLAY"}},
        {"case_id":"PMV2-DIV-CONTRAST-3496-23","scope":{"basis":"QUESTION_SET_OBSERVED","universal_grade_claim":False},"representations":["WRITTEN_DIVISION","MULTIPLES_SUPPORT","MULTIPLICATION_CHECK"],"math_evidence":{"dividend":3496,"divisor":23,"quotient":152,"remainder":0,"quotient_digits":[1,5,2],"zero_place_preserved":False}},
        {"case_id":"PMV2-DIV-DIAGNOSTIC-ZERO-CONTRAST","scope":{"basis":"QUESTION_SET_OBSERVED","universal_grade_claim":False},"representations":["CONTRAST_SET","DIAGNOSTIC_PROBE"],"math_evidence":{},"diagnosis_evidence":semantic_manifests()["diagnostic"]},
        {"case_id":"PMV2-DIV-REMAINDER-CONTEXT","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["REMAINDER_CONTEXT","GROUP_MODEL","ANSWER_FORM"],"math_evidence":{"quotient":4,"remainder":5,"answer_form":"ROUND_UP_ONE_MORE_GROUP","context_rule_explicit":True},"product_evidence":{"core2_practice_ref":"Practice 7","raw_question_direct_render":False}},
        {"case_id":"PMV2-UNIT-DOZEN-MONEY","scope":{"basis":"QUESTION_SET_OBSERVED","universal_grade_claim":False},"representations":["QUANTITY_STRUCTURE","UNIT_CHAIN","MULTI_STEP_EQUATION"],"math_evidence":{"source_quantity":23,"source_unit":"DOZEN","conversion_factor":12,"converted_quantity":276,"target_unit":"EGG","rate":6,"result":1656}},
        {"case_id":"PMV2-FRAC-EQUIV-1-2","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["EQUAL_PARTITION","FRACTION_STRIP","NUMBER_LINE","EQUIVALENCE_BRIDGE"],"math_evidence":{"fractions":[[1,2],[2,4],[4,8]],"equal_partitions":True}},
        {"case_id":"PMV2-FRAC-ADD-1-2-1-4","scope":{"basis":"CURRICULUM_OVERLAY","authority_ref":"PRIMARY-V2-INTEGRATION-OVERLAY-FRACTION-ADD","universal_grade_claim":False},"representations":["REPARTITION","EQUIVALENT_FRACTION","FRACTION_ADDITION"],"math_evidence":{"left":[1,2],"right":[1,4],"result":[3,4],"repartition_or_equivalence_explicit":True}},
        {"case_id":"PMV2-PLACEVALUE-5043","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["PLACE_VALUE_CHART","EXPANDED_FORM"],"math_evidence":{"number":5043,"digits":{"THOUSANDS":5,"HUNDREDS":0,"TENS":4,"ONES":3},"expanded":[5000,40,3]}},
        {"case_id":"PMV2-DECIMAL-0-37","scope":{"basis":"CURRICULUM_OVERLAY","authority_ref":"PRIMARY-V2-INTEGRATION-OVERLAY-DECIMAL","universal_grade_claim":False},"representations":["HUNDRED_GRID","DECIMAL_PLACE_VALUE","NUMBER_LINE"],"math_evidence":{"decimal":"0.37","shaded_hundredths":37}},
        {"case_id":"PMV2-MEASURE-M-TO-CM","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["UNIT_CHAIN","MEASUREMENT_SCALE"],"math_evidence":{"value":3,"source_unit":"M","target_unit":"CM","factor":100,"result":300}},
        {"case_id":"PMV2-PERIMETER-AREA-RECT-6X4","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["PERIMETER_PATH","AREA_TILE_GRID"],"math_evidence":{"perimeter":20,"area":24,"perimeter_semantics":"BOUNDARY","area_semantics":"COVERING"}},
        {"case_id":"PMV2-VOLUME-3X2X4","scope":{"basis":"CURRICULUM_OVERLAY","authority_ref":"PRIMARY-V2-INTEGRATION-OVERLAY-VOLUME","universal_grade_claim":False},"representations":["CUBE_LAYERS"],"math_evidence":{"volume":24,"cube_count":24}},
        {"case_id":"PMV2-ANGLE-65","scope":{"basis":"CURRICULUM_OVERLAY","authority_ref":"PRIMARY-V2-INTEGRATION-OVERLAY-ANGLE","universal_grade_claim":False},"representations":["ANGLE_MODEL","PROTRACTOR_OR_TURN"],"math_evidence":{"declared_degrees":65,"represented_degrees":65}},
        {"case_id":"PMV2-DATA-BAR-SCALE-5","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["DATA_TABLE","BAR_CHART","SCALE_KEY"],"math_evidence":{"scale":5,"data":{"A":10,"B":25,"C":15},"rendered_values":{"A":10,"B":25,"C":15}}},
        {"case_id":"PMV2-WORK-PROVENANCE-MIXED-SUCCESS","scope":{"basis":"SCHOOL_CLASSWORK_OBSERVED","universal_grade_claim":False},"representations":["STRUCTURED_REPLAY"],"math_evidence":{},"work_evidence":semantic_manifests()["work"]},
        {"case_id":"PMV2-HINT-FADE-FRESH-RETRY","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["H1_NOTICE","H2_REMEMBER","H3_REPRESENT","FRESH_INDEPENDENT_RETRY"],"math_evidence":{},"hint_evidence":{"sequence":["H0","H1","H2","H3","FRESH_H0"],"supported_success_is_independent":False,"supported_item_id":"Practice 1","fresh_retry_item_id":"Independent retry 1"}},
        {"case_id":"PMV2-ROUTE-CHANGE-AFTER-REPEAT-FAILURE","scope":{"basis":"COMMON_G4_5_CAPABILITY","universal_grade_claim":False},"representations":["TEACHER_MOVE_TRACE"],"math_evidence":{},"runtime_evidence":semantic_manifests()["runtime"]},
    ]


def find_pdf_placement(case_id: str, core1_custody: Mapping[str, Any], core2_custody: Mapping[str, Any]) -> Dict[str, Any] | None:
    for artifact_name, custody in (("CORE1_PDF", core1_custody), ("CORE2_PDF", core2_custody)):
        for page in custody.get("page_map", []):
            for semantic_id in page.get("semantic_ids", []):
                if case_id in str(semantic_id):
                    return {"artifact_kind": artifact_name, "page_number": page["page_number"], "semantic_id": semantic_id}
    if case_id == "PMV2-HINT-FADE-FRESH-RETRY":
        for page in core2_custody.get("page_map", []):
            if "Practice 1" in page.get("semantic_ids", []):
                return {"artifact_kind":"CORE2_PDF","page_number":page["page_number"],"semantic_id":"Practice 1"}
    return None


def validate_no_placeholder_hashes(value: Any) -> None:
    text = json.dumps(value, sort_keys=True)
    if re.search(r"sha256-[A-Za-z]", text):
        raise SystemExit("REAL_CANDIDATE contains placeholder-style sha256-* evidence")


def render_review_pages(pdf: Path, prefix: Path) -> None:
    tool = shutil.which("pdftoppm")
    if not tool:
        return
    prefix.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([tool, "-png", "-r", "120", str(pdf), str(prefix)], check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    core1_plan = build_core1_plan()
    core2_plan = build_core2_plan()
    guard = LearnerSurfaceGuard()
    surface1 = guard.scan_document(core1_plan)
    surface2 = guard.scan_document(core2_plan)
    if not surface1["pass"] or not surface2["pass"]:
        raise SystemExit(f"learner surface guard failed: core1={surface1}, core2={surface2}")

    write_json(out / "core1_render_plan.json", core1_plan)
    write_json(out / "core2_render_plan.json", core2_plan)

    composer = PrimaryPageComposer()
    core1_pdf = out / "Core1.pdf"
    core2_pdf = out / "Core2.pdf"
    core1_sha, core1_custody = composer.render_core1_study_guide(core1_plan, core1_pdf)
    core2_sha, core2_custody = composer.render_core2_companion(core2_plan, core2_pdf)
    if not re.fullmatch(r"[0-9a-f]{64}", core1_sha) or not re.fullmatch(r"[0-9a-f]{64}", core2_sha):
        raise SystemExit("renderer did not return exact SHA256 digests")

    page_maps = {"core1": core1_custody, "core2": core2_custody}
    page_map_digest = digest_json(page_maps)
    write_json(out / "physical_page_maps.json", page_maps)

    manifests = semantic_manifests()
    manifest_digests: Dict[str, str] = {}
    for name, manifest in manifests.items():
        path = out / f"{name}_manifest.json"
        write_json(path, manifest)
        manifest_digests[name] = digest_json(manifest)

    cases = producer_case_evidence()
    for case in cases:
        cid = case["case_id"]
        case["surface_evidence"] = {"internal_identifier_leaks": []}
        placement = find_pdf_placement(cid, core1_custody, core2_custody)
        if placement:
            artifact_sha = core1_sha if placement["artifact_kind"] == "CORE1_PDF" else core2_sha
            placement_id = digest_json({"case_id":cid,"artifact_sha256":artifact_sha,**placement})
            case["custody_evidence"] = {"placement_evidence_id":placement_id, **placement, "artifact_sha256":artifact_sha}
        elif cid == "PMV2-ROUTE-CHANGE-AFTER-REPEAT-FAILURE":
            d = manifest_digests["runtime"]
            case["custody_evidence"] = {"placement_evidence_id":digest_json({"case_id":cid,"manifest_sha256":d}),"artifact_kind":"RUNTIME_POLICY_MANIFEST","manifest_sha256":d}
        elif cid == "PMV2-DIV-DIAGNOSTIC-ZERO-CONTRAST":
            d = manifest_digests["diagnostic"]
            case["custody_evidence"] = {"placement_evidence_id":digest_json({"case_id":cid,"manifest_sha256":d}),"artifact_kind":"DIAGNOSTIC_MANIFEST","manifest_sha256":d}
        else:
            raise SystemExit(f"no exact placement/custody evidence for {cid}")

    candidate = {
        "version":"1.0.0",
        "candidate_id": CANDIDATE_ID,
        "evidence_class":"REAL_CANDIDATE",
        "producer":"PrimaryMathV2 PR327 publisher + PR337 integration",
        "artifacts": {
            "core1_sha256": core1_sha,
            "core2_sha256": core2_sha,
            "physical_page_map_digest": page_map_digest,
            "diagnostic_manifest_sha256": manifest_digests["diagnostic"],
            "work_manifest_sha256": manifest_digests["work"],
            "runtime_manifest_sha256": manifest_digests["runtime"],
        },
        "cases": cases,
        "producer_claims": {
            "surface_guard_core1": surface1,
            "surface_guard_core2": surface2,
            "human_review_status": "PENDING_HUMAN_REVIEW",
            "producer_machine_pass_is_not_independent_acceptance": True,
        },
    }
    validate_no_placeholder_hashes(candidate)
    write_json(out / "candidate_export.json", candidate)
    write_json(out / "artifact_manifest.json", {
        "candidate_id": CANDIDATE_ID,
        "artifacts": candidate["artifacts"],
        "candidate_export_sha256": digest_json(candidate),
        "human_review_status": "PENDING_HUMAN_REVIEW",
    })

    render_review_pages(core1_pdf, out / "review_pages" / "core1")
    render_review_pages(core2_pdf, out / "review_pages" / "core2")

    print(json.dumps({
        "candidate_id": CANDIDATE_ID,
        "core1_sha256": core1_sha,
        "core2_sha256": core2_sha,
        "physical_page_map_digest": page_map_digest,
        "case_count": len(cases),
        "human_review_status": "PENDING_HUMAN_REVIEW",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
