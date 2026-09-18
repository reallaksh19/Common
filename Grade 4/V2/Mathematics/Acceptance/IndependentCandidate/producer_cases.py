"""Producer-owned evidence for the frozen Primary Math V2 independent cases.

This module does NOT import or read BenchmarkAcceptance.  The case identities are
an integration contract; mathematical evidence and visual realization specs are
owned here by the Grade-4 producer and are independently checked downstream.
"""
from __future__ import annotations

from typing import Any, Dict, List


def visual(role: str, kind: str, params: Dict[str, Any], caption: str) -> Dict[str, Any]:
    return {"role": role, "kind": kind, "params": params, "caption": caption}


def evidence(
    case_id: str,
    title: str,
    scope_basis: str,
    representations: List[str],
    math_evidence: Dict[str, Any],
    visuals: List[Dict[str, Any]],
    *,
    authority_ref: str | None = None,
    work_evidence: Dict[str, Any] | None = None,
    diagnosis_evidence: Dict[str, Any] | None = None,
    product_evidence: Dict[str, Any] | None = None,
    hint_evidence: Dict[str, Any] | None = None,
    runtime_evidence: Dict[str, Any] | None = None,
    practice_prompt: str = "Try a fresh problem with the same structure, then check your reasoning.",
) -> Dict[str, Any]:
    scope: Dict[str, Any] = {"basis": scope_basis, "universal_grade_claim": False}
    if authority_ref:
        scope["authority_ref"] = authority_ref
    return {
        "case_id": case_id,
        "title": title,
        "scope": scope,
        "representations": representations,
        "math_evidence": math_evidence,
        "work_evidence": work_evidence,
        "diagnosis_evidence": diagnosis_evidence,
        "product_evidence": product_evidence,
        "hint_evidence": hint_evidence,
        "runtime_evidence": runtime_evidence,
        "practice_prompt": practice_prompt,
        "visuals": visuals,
    }


DIV366_STEPS = [
    {"type": "SUBTRACTION", "value": 36, "col": 1},
    {"type": "BRING_DOWN", "value": 6, "col": 2},
    {"type": "REMAINDER", "value": 6, "col": 2},
]
DIV7843_STEPS = [
    {"type": "SUBTRACTION", "value": 78, "col": 1},
    {"type": "BRING_DOWN", "value": 4, "col": 2},
    {"type": "SUBTRACTION", "value": 0, "col": 2},
    {"type": "BRING_DOWN", "value": 3, "col": 3},
    {"type": "SUBTRACTION", "value": 39, "col": 3},
    {"type": "REMAINDER", "value": 4, "col": 3},
]
DIV3496_STEPS = [
    {"type": "SUBTRACTION", "value": 23, "col": 1},
    {"type": "BRING_DOWN", "value": 119, "col": 2},
    {"type": "SUBTRACTION", "value": 115, "col": 2},
    {"type": "BRING_DOWN", "value": 46, "col": 3},
    {"type": "SUBTRACTION", "value": 46, "col": 3},
    {"type": "REMAINDER", "value": 0, "col": 3},
]


CASES: List[Dict[str, Any]] = [
    evidence(
        "PMV2-MUL-BRIDGE-23X6", "Build 23 × 6 through connected representations", "COMMON_G4_5_CAPABILITY",
        ["EQUAL_GROUPS", "ARRAY", "DISTRIBUTIVE_AREA", "PARTIAL_PRODUCTS", "WRITTEN_ALGORITHM", "CHECK"],
        {"a": 23, "b": 6, "split": [20, 3], "partial_products": [120, 18], "product": 138, "check_product": 138},
        [
            visual("EQUAL_GROUPS", "EQUAL_GROUPS", {"group_count": 6, "items_per_group": 23}, "Six equal groups of 23"),
            visual("ARRAY", "ARRAY", {"rows": 6, "cols": 23}, "The same multiplication as an array"),
            visual("DISTRIBUTIVE_AREA", "AREA_MODEL", {"factors": [23, 6], "partitions": [{"length": 20, "height": 6, "area": 120}, {"length": 3, "height": 6, "area": 18}]}, "Split 23 into 20 and 3"),
            visual("PARTIAL_PRODUCTS", "PARTIAL_PRODUCTS", {"factors": [23, 6], "partial_products": [120, 18], "product": 138}, "Put the partial products together"),
            visual("WRITTEN_ALGORITHM", "VERTICAL_MULTIPLICATION", {"factors": [23, 6], "partial_products": [18, 120], "total_product": 138, "tier": "AUTHORED_NOTEBOOK_EXAMPLE"}, "Written multiplication"),
            visual("CHECK", "ESTIMATE_CHECK", {"actual": 138, "estimate_expr": "20 × 6 = 120", "reasoning": "23 is a little more than 20, so 138 is reasonable."}, "Check the size of the answer"),
        ],
        product_evidence={"core1_ref": "C1-MUL-BRIDGE-23X6", "core2_practice_ref": "C2-MUL-BRIDGE-23X6", "raw_question_direct_render": False},
        practice_prompt="Use an area split to solve 34 × 5, then show a written check.",
    ),
    evidence(
        "PMV2-DIV-SHARE-GROUP-24-6", "Sharing and grouping are different division questions", "COMMON_G4_5_CAPABILITY",
        ["EQUAL_SHARE", "EQUAL_GROUP", "DIVISION_EQUATION"],
        {"sharing": {"total": 24, "group_count": 6, "group_size": 4, "unknown_role": "GROUP_SIZE"}, "grouping": {"total": 24, "group_size": 6, "group_count": 4, "unknown_role": "GROUP_COUNT"}},
        [
            visual("EQUAL_SHARE", "DIVISION_STRUCTURE", {"dividend": 24, "divisor": 6, "quotient": 4, "meaning": "SHARING"}, "Share 24 equally among 6 groups"),
            visual("EQUAL_GROUP", "DIVISION_STRUCTURE", {"dividend": 24, "divisor": 6, "quotient": 4, "meaning": "GROUPING"}, "Make groups of 6 from 24"),
            visual("DIVISION_EQUATION", "INVERSE_CHECK", {"expression": "24 ÷ 6 = 4 because 6 × 4 = 24"}, "Connect division to multiplication"),
        ],
        practice_prompt="Explain the difference between sharing 30 among 5 groups and making groups of 5 from 30.",
    ),
    evidence(
        "PMV2-DIV-ZERO-366-12", "Keep the zero place in 366 ÷ 12", "QUESTION_SET_OBSERVED",
        ["WRITTEN_DIVISION", "QUOTIENT_PLACE_SLOTS", "MULTIPLICATION_CHECK"],
        {"dividend": 366, "divisor": 12, "quotient": 30, "remainder": 6, "quotient_digits": [3, 0], "zero_place_preserved": True},
        [
            visual("WRITTEN_DIVISION", "LONG_DIVISION_WORKOUT", {"dividend": 366, "divisor": 12, "quotient": 30, "remainder": 6, "quotient_digits": ["3", "0"], "multiples_table": [12, 24, 36, 48, 60], "steps": DIV366_STEPS}, "Written division with the zero place visible"),
            visual("QUOTIENT_PLACE_SLOTS", "CUSTOM_SLOTS", {"digits": [3, 0], "labels": ["tens", "ones"]}, "Every quotient digit owns a place"),
            visual("MULTIPLICATION_CHECK", "INVERSE_CHECK", {"expression": "12 × 30 + 6 = 366"}, "Rebuild the dividend"),
        ],
        product_evidence={"core1_ref": "C1-DIV-ZERO-366-12", "core2_practice_ref": "C2-DIV-ZERO-366-12", "raw_question_direct_render": False},
        practice_prompt="Divide 488 by 12. If a quotient place has no groups, keep that place visible.",
    ),
    evidence(
        "PMV2-DIV-ZERO-7843-13", "Preserve the internal zero in 7843 ÷ 13", "QUESTION_SET_OBSERVED",
        ["WRITTEN_DIVISION", "QUOTIENT_PLACE_SLOTS", "MULTIPLICATION_CHECK"],
        {"dividend": 7843, "divisor": 13, "quotient": 603, "remainder": 4, "quotient_digits": [6, 0, 3], "zero_place_preserved": True},
        [
            visual("WRITTEN_DIVISION", "LONG_DIVISION_WORKOUT", {"dividend": 7843, "divisor": 13, "quotient": 603, "remainder": 4, "quotient_digits": ["6", "0", "3"], "multiples_table": [13, 26, 39, 52, 65, 78, 91, 104, 117, 130], "steps": DIV7843_STEPS}, "A zero quotient digit keeps the place value"),
            visual("QUOTIENT_PLACE_SLOTS", "CUSTOM_SLOTS", {"digits": [6, 0, 3], "labels": ["hundreds", "tens", "ones"]}, "Hundreds, tens and ones stay aligned"),
            visual("MULTIPLICATION_CHECK", "INVERSE_CHECK", {"expression": "13 × 603 + 4 = 7843"}, "Check the quotient and remainder"),
        ],
        work_evidence={"final_correctness": "INCORRECT", "steps": [{"id": "child-step-1", "status": "CORRECT"}, {"id": "child-step-2", "status": "AMBIGUOUS"}], "teacher_annotations": [{"actor": "TEACHER", "kind": "CORRECTION"}], "replay_provenance": "STRUCTURED_REPLAY"},
        practice_prompt="Divide 8428 by 14. Show every quotient place before the final check.",
    ),
    evidence(
        "PMV2-DIV-CONTRAST-3496-23", "A contrast case with no zero quotient place", "QUESTION_SET_OBSERVED",
        ["WRITTEN_DIVISION", "MULTIPLES_SUPPORT", "MULTIPLICATION_CHECK"],
        {"dividend": 3496, "divisor": 23, "quotient": 152, "remainder": 0, "quotient_digits": [1, 5, 2], "zero_place_preserved": False},
        [
            visual("WRITTEN_DIVISION", "LONG_DIVISION_WORKOUT", {"dividend": 3496, "divisor": 23, "quotient": 152, "remainder": 0, "quotient_digits": ["1", "5", "2"], "multiples_table": [23, 46, 69, 92, 115, 138], "steps": DIV3496_STEPS}, "Written division without a zero place"),
            visual("MULTIPLES_SUPPORT", "DIV_MULTIPLES_STRIP", {"divisor": 23, "comparisons": ["1 x 23 = 23", "2 x 23 = 46", "3 x 23 = 69", "4 x 23 = 92", "5 x 23 = 115"]}, "Use useful multiples instead of guessing"),
            visual("MULTIPLICATION_CHECK", "INVERSE_CHECK", {"expression": "23 × 152 = 3496"}, "Multiply to check"),
        ],
        practice_prompt="Use a multiples strip to plan 3910 ÷ 23 before writing the long division.",
    ),
    evidence(
        "PMV2-DIV-DIAGNOSTIC-ZERO-CONTRAST", "Contrast quotient-zero cases before making a diagnosis", "QUESTION_SET_OBSERVED",
        ["CONTRAST_SET", "DIAGNOSTIC_PROBE"], {},
        [
            visual("CONTRAST_SET", "CUSTOM_CONTRAST", {"positive": ["366 ÷ 12", "7843 ÷ 13"], "negative": ["3496 ÷ 23"], "feature": "a zero quotient place is required"}, "Compare cases that differ on one focal feature"),
            visual("DIAGNOSTIC_PROBE", "CUSTOM_PROBE", {"prompt": "Choose the quotient-place digit when the current partial dividend is smaller than the divisor.", "feature": "zero place"}, "Use the smallest probe that separates the hypotheses"),
        ],
        diagnosis_evidence={"focal_feature": "QUOTIENT_ZERO_REQUIRED", "positive_cases": ["PMV2-DIV-ZERO-366-12", "PMV2-DIV-ZERO-7843-13"], "negative_cases": ["PMV2-DIV-CONTRAST-3496-23"], "learner_label": None, "competing_hypotheses": [{"hypothesis_id": "H-DIV-GENERAL", "error_signature": "DIV_GENERAL_LONG_DIVISION_PROCEDURE", "durable_trait": False}, {"hypothesis_id": "H-DIV-ZERO", "error_signature": "DIV_QUOTIENT_ZERO_PLACE_VALUE", "durable_trait": False}], "probe": {"hypothesis_ids": ["H-DIV-GENERAL", "H-DIV-ZERO"], "manipulated_feature": "QUOTIENT_ZERO_REQUIRED", "controlled_load": {"language": "LOW", "representation_novelty": "LOW", "fact_retrieval_demand": "LOW"}, "outcome_rules": [{"no_zero": "CORRECT", "zero": "INCORRECT", "increase": "H-DIV-ZERO"}, {"no_zero": "INCORRECT", "zero": "INCORRECT", "keep_open": ["H-DIV-GENERAL", "H-DIV-ZERO"]}]}},
        practice_prompt="Use one new zero-place contrast item to decide which hypothesis remains plausible; do not label the learner broadly.",
    ),
    evidence(
        "PMV2-DIV-REMAINDER-CONTEXT", "A remainder changes meaning with the story", "COMMON_G4_5_CAPABILITY",
        ["REMAINDER_CONTEXT", "GROUP_MODEL", "ANSWER_FORM"],
        {"quotient": 4, "remainder": 5, "answer_form": "ROUND_UP_ONE_MORE_GROUP", "context_rule_explicit": True},
        [
            visual("REMAINDER_CONTEXT", "DIVISION_REMAINDER_CONTEXT", {"dividend": 29, "divisor": 6, "quotient": 4, "remainder": 5, "action": "ROUND_UP_ONE_MORE_GROUP", "final_answer": 5, "explanation": "Four full groups are not enough for all 29, so one more group is needed."}, "Interpret the remainder in context"),
            visual("GROUP_MODEL", "DIV_REMAINDER_CONTEXT", {"group_size": 6, "rendered_quantity": 4, "declared_quantity": 4, "leftover": 5, "continuation_marker": "4 full groups"}, "See full groups and leftovers"),
            visual("ANSWER_FORM", "CUSTOM_ANSWER_FORM", {"quotient": 4, "remainder": 5, "answer": 5, "reason": "round up one more group"}, "Choose the answer form the story needs"),
        ],
        product_evidence={"core2_practice_ref": "C2-DIV-REMAINDER-CONTEXT", "raw_question_direct_render": False},
        practice_prompt="29 learners travel in vehicles holding 6 each. How many vehicles are needed, and why is the remainder important?",
    ),
    evidence(
        "PMV2-UNIT-DOZEN-MONEY", "Follow a dozen → eggs → money unit chain", "QUESTION_SET_OBSERVED",
        ["QUANTITY_STRUCTURE", "UNIT_CHAIN", "MULTI_STEP_EQUATION"],
        {"source_quantity": 23, "source_unit": "DOZEN", "conversion_factor": 12, "converted_quantity": 276, "target_unit": "EGG", "rate": 6, "result": 1656},
        [
            visual("QUANTITY_STRUCTURE", "QUANTITY_STRUCTURE_MAP", {"branches": ["23 dozen", "12 eggs per dozen", "6 currency per egg"]}, "Name the quantities and their roles"),
            visual("UNIT_CHAIN", "MEASUREMENT_CONVERSION", {"from_value": 23, "from_unit": "DOZEN", "factor": 12, "to_value": 276, "to_unit": "EGG"}, "Convert dozens to eggs first"),
            visual("MULTI_STEP_EQUATION", "INVERSE_CHECK", {"expression": "23 × 12 = 276; 276 × 6 = 1656"}, "Keep both steps visible"),
        ],
        practice_prompt="Convert 15 dozen items to single items, then find the total cost at 4 currency units each.",
    ),
    evidence(
        "PMV2-FRAC-EQUIV-1-2", "Equivalent fractions name the same amount", "COMMON_G4_5_CAPABILITY",
        ["EQUAL_PARTITION", "FRACTION_STRIP", "NUMBER_LINE", "EQUIVALENCE_BRIDGE"],
        {"fractions": [[1, 2], [2, 4], [4, 8]], "equal_partitions": True},
        [
            visual("EQUAL_PARTITION", "FRACTION_STRIP", {"numerator": 1, "denominator": 2, "label": "1/2"}, "Start with one half"),
            visual("FRACTION_STRIP", "FRACTION_STRIP", {"numerator": 2, "denominator": 4, "label": "2/4 = 1/2"}, "Partition the same whole into fourths"),
            visual("NUMBER_LINE", "CUSTOM_FRACTION_NUMBER_LINE", {"fractions": [[1, 2], [2, 4], [4, 8]]}, "Equivalent fractions land at the same point"),
            visual("EQUIVALENCE_BRIDGE", "CUSTOM_EQUATION", {"text": "1/2 = 2/4 = 4/8"}, "Connect the representations symbolically"),
        ],
        practice_prompt="Show two fractions equivalent to 3/4 using a strip and a number line.",
    ),
    evidence(
        "PMV2-FRAC-ADD-1-2-1-4", "Repartition before adding unlike fractional parts", "CURRICULUM_OVERLAY",
        ["REPARTITION", "EQUIVALENT_FRACTION", "FRACTION_ADDITION"],
        {"left": [1, 2], "right": [1, 4], "result": [3, 4], "repartition_or_equivalence_explicit": True},
        [
            visual("REPARTITION", "FRACTION_STRIP", {"numerator": 2, "denominator": 4, "label": "1/2 = 2/4"}, "Repartition one half as two fourths"),
            visual("EQUIVALENT_FRACTION", "CUSTOM_EQUATION", {"text": "1/2 → 2/4"}, "Make equal-sized parts"),
            visual("FRACTION_ADDITION", "FRACTION_ADDITION", {"num1": 2, "den1": 4, "num2": 1, "den2": 4, "res_num": 3, "res_den": 4}, "Add fourths after repartitioning"),
        ],
        authority_ref="GRADE4_NON_NORMATIVE_OVERLAY",
        practice_prompt="Use equivalence to add 1/2 + 2/8 without adding unlike denominators directly.",
    ),
    evidence(
        "PMV2-PLACEVALUE-5043", "A zero still holds a place in 5,043", "COMMON_G4_5_CAPABILITY",
        ["PLACE_VALUE_CHART", "EXPANDED_FORM"],
        {"number": 5043, "digits": {"THOUSANDS": 5, "HUNDREDS": 0, "TENS": 4, "ONES": 3}, "expanded": [5000, 40, 3]},
        [
            visual("PLACE_VALUE_CHART", "PLACE_VALUE_BLOCKS", {"number": 5043, "expanded": [5000, 0, 40, 3]}, "The zero holds the hundreds place"),
            visual("EXPANDED_FORM", "QUANTITY_STRUCTURE_MAP", {"branches": ["5000", "40", "3"]}, "Expanded form uses the non-zero place values"),
        ],
        practice_prompt="Write 7,009 in expanded form and explain what each zero is doing.",
    ),
    evidence(
        "PMV2-DECIMAL-0-37", "Thirty-seven hundredths in three representations", "CURRICULUM_OVERLAY",
        ["HUNDRED_GRID", "DECIMAL_PLACE_VALUE", "NUMBER_LINE"],
        {"decimal": "0.37", "shaded_hundredths": 37},
        [
            visual("HUNDRED_GRID", "DECIMAL_HUNDRED_GRID", {"decimal_value": 0.37, "grid_shaded_cells": 37}, "Shade 37 of 100 equal cells"),
            visual("DECIMAL_PLACE_VALUE", "QUANTITY_STRUCTURE_MAP", {"branches": ["3 tenths", "7 hundredths"]}, "Read the decimal by place value"),
            visual("NUMBER_LINE", "DECIMAL_NUMBER_LINE", {"min_val": 0.0, "max_val": 1.0, "target_val": 0.37}, "Locate 0.37 between 0 and 1"),
        ],
        authority_ref="GRADE4_NON_NORMATIVE_OVERLAY",
        practice_prompt="Represent 0.62 on a hundred grid and number line.",
    ),
    evidence(
        "PMV2-MEASURE-M-TO-CM", "Convert metres to centimetres with a unit relationship", "COMMON_G4_5_CAPABILITY",
        ["UNIT_CHAIN", "MEASUREMENT_SCALE"],
        {"value": 3, "source_unit": "M", "target_unit": "CM", "factor": 100, "result": 300},
        [
            visual("UNIT_CHAIN", "MEASUREMENT_CONVERSION", {"from_value": 3, "from_unit": "M", "factor": 100, "to_value": 300, "to_unit": "CM"}, "Three metres contains three hundreds of centimetres"),
            visual("MEASUREMENT_SCALE", "CUSTOM_SCALE", {"left": "1 m", "right": "100 cm", "count": 3}, "Repeat the 1 m = 100 cm scale three times"),
        ],
        practice_prompt="Convert 7 m to centimetres and show the factor you used.",
    ),
    evidence(
        "PMV2-PERIMETER-AREA-RECT-6X4", "Perimeter follows the boundary; area covers the inside", "COMMON_G4_5_CAPABILITY",
        ["PERIMETER_PATH", "AREA_TILE_GRID"],
        {"perimeter": 20, "area": 24, "perimeter_semantics": "BOUNDARY", "area_semantics": "COVERING"},
        [
            visual("PERIMETER_PATH", "RECTILINEAR_PERIMETER_AREA", {"width": 6, "height": 4, "perimeter": 20, "area": 24, "unit": "cm"}, "Trace the 20 cm boundary"),
            visual("AREA_TILE_GRID", "RECTILINEAR_PERIMETER_AREA", {"width": 6, "height": 4, "perimeter": 20, "area": 24, "unit": "cm"}, "Cover the rectangle with 24 square centimetres"),
        ],
        practice_prompt="For an 8 cm by 3 cm rectangle, find perimeter and area and explain why their units differ.",
    ),
    evidence(
        "PMV2-VOLUME-3X2X4", "Volume counts unit cubes in layers", "CURRICULUM_OVERLAY",
        ["CUBE_LAYERS"],
        {"volume": 24, "cube_count": 24},
        [visual("CUBE_LAYERS", "VOLUME_CUBE_LAYERS", {"length": 3, "width": 2, "height": 4}, "Four layers of 3 × 2 unit cubes make 24")],
        authority_ref="GRADE4_NON_NORMATIVE_OVERLAY",
        practice_prompt="Find the volume of a 5 × 2 × 3 unit-cube prism by thinking in layers.",
    ),
    evidence(
        "PMV2-ANGLE-65", "A 65° angle is an acute turn", "CURRICULUM_OVERLAY",
        ["ANGLE_MODEL", "PROTRACTOR_OR_TURN"],
        {"declared_degrees": 65, "represented_degrees": 65},
        [
            visual("ANGLE_MODEL", "GEOMETRIC_ANGLE", {"angle_degrees": 65, "classification": "ACUTE"}, "Draw an opening of 65 degrees"),
            visual("PROTRACTOR_OR_TURN", "ANGLE_BENCHMARK_COMPARE", {"degrees": 65}, "Compare 65 degrees with a right angle"),
        ],
        authority_ref="GRADE4_NON_NORMATIVE_OVERLAY",
        practice_prompt="Draw an angle of about 40° and explain how it compares with 90°.",
    ),
    evidence(
        "PMV2-DATA-BAR-SCALE-5", "A bar chart must obey its scale", "COMMON_G4_5_CAPABILITY",
        ["DATA_TABLE", "BAR_CHART", "SCALE_KEY"],
        {"scale": 5, "data": {"A": 10, "B": 25, "C": 15}, "rendered_values": {"A": 10, "B": 25, "C": 15}},
        [
            visual("DATA_TABLE", "CUSTOM_TABLE", {"headers": ["Category", "Value"], "rows": [["A", 10], ["B", 25], ["C", 15]]}, "Read the exact data before drawing bars"),
            visual("BAR_CHART", "DATA_BAR_CHART", {"categories": ["A", "B", "C"], "values": [10, 25, 15], "scale_unit": 5}, "Bars show 10, 25 and 15"),
            visual("SCALE_KEY", "CUSTOM_SCALE_KEY", {"scale": 5, "text": "one interval = 5"}, "Use a scale of five per interval"),
        ],
        practice_prompt="Draw a bar chart for X=20, Y=5, Z=15 using a scale of 5.",
    ),
    evidence(
        "PMV2-WORK-PROVENANCE-MIXED-SUCCESS", "Preserve what the learner actually did", "SCHOOL_CLASSWORK_OBSERVED",
        ["STRUCTURED_REPLAY"], {},
        [visual("STRUCTURED_REPLAY", "CUSTOM_WORK_REPLAY", {"steps": [{"text": "correct fact", "status": "CORRECT"}, {"text": "unclear place-value mark", "status": "AMBIGUOUS"}, {"text": "incorrect subtraction", "status": "INCORRECT"}], "teacher_note": "teacher correction stays separate"}, "Correct, ambiguous and incorrect work stay distinguishable")],
        work_evidence={"final_correctness": "INCORRECT", "steps": [{"id": "WS-01", "kind": "FACT_RETRIEVAL", "status": "CORRECT", "actor": "CHILD"}, {"id": "WS-02", "kind": "PLACE_VALUE_WRITE", "status": "AMBIGUOUS", "actor": "CHILD"}, {"id": "WS-03", "kind": "SUBTRACTION", "status": "INCORRECT", "actor": "CHILD"}], "teacher_annotations": [{"actor": "TEACHER", "relation_to_step": "WS-02", "kind": "CORRECTION"}], "replay_provenance": "STRUCTURED_REPLAY"},
        practice_prompt="Review the work evidence without turning one error into a broad learner label.",
    ),
    evidence(
        "PMV2-HINT-FADE-FRESH-RETRY", "Support fades, then a fresh independent retry", "COMMON_G4_5_CAPABILITY",
        ["H1_NOTICE", "H2_REMEMBER", "H3_REPRESENT", "FRESH_INDEPENDENT_RETRY"], {},
        [
            visual("H1_NOTICE", "CUSTOM_HINT", {"level": "LOOK", "text": "Notice the quantity roles."}, "LOOK: reveal structure only"),
            visual("H2_REMEMBER", "CUSTOM_HINT", {"level": "REMEMBER", "text": "Recall the relationship."}, "REMEMBER: recall the relationship"),
            visual("H3_REPRESENT", "CUSTOM_HINT", {"level": "SHOW IT", "text": "Draw the first useful representation."}, "SHOW IT: change representation, not give the answer"),
            visual("FRESH_INDEPENDENT_RETRY", "CUSTOM_HINT", {"level": "TRY", "text": "Use a new item without inherited hints."}, "Fresh TRY: independent evidence"),
        ],
        hint_evidence={"sequence": ["H0", "H1", "H2", "H3", "FRESH_H0"], "supported_success_is_independent": False, "supported_item_id": "SUP-01", "fresh_retry_item_id": "IND-02"},
        practice_prompt="After support, solve a semantically equivalent new item without the supported visual.",
    ),
    evidence(
        "PMV2-ROUTE-CHANGE-AFTER-REPEAT-FAILURE", "Change the teaching route after repeated same-route failure", "COMMON_G4_5_CAPABILITY",
        ["TEACHER_MOVE_TRACE"], {},
        [visual("TEACHER_MOVE_TRACE", "CUSTOM_ROUTE_TRACE", {"attempts": ["symbolic", "symbolic"], "changed_to": "structural visual", "retry": "fresh independent"}, "Two same-route failures trigger a meaningful route change")],
        runtime_evidence={"same_route_failures": 2, "route_changed": True, "changed_dimension": "REPRESENTATION", "conceptual_support": "H3_REPRESENT", "access_adjustment": "NONE", "independent_retry_after_repair": True},
        practice_prompt="After two unsuccessful symbolic attempts, change representation before a fresh independent retry.",
    ),
]


EXPECTED_CASE_IDS = [case["case_id"] for case in CASES]
