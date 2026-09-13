"""Document-level study journey for The Pupil pages 97-99.

The journey groups source evidence into teaching concepts while keeping every
learner question explicit, answerable and source-addressable. Source-derived
questions retain their workbook reference and original values; generated
practice uses separate Practice/Fresh Try labels.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable

ALL_REFS = [
    "P97-Q1", "P97-Q2", "P97-Q3", "P97-Q4", "P97-Q5", "P97-Q6", "P97-Q7", "P97-Q8", "P97-Q9",
    "P98-Q1", "P98-Q2", "P98-Q3", "P98-Q4", "P98-Q5", "P99-Q1", "P99-Q2", "P99-Q3", "P99-Q4",
]

SOURCE_TEXT = {
    "P97-Q1": "Which product is the same as 25 x 30? A. 3 x 10 x 25  B. (3 + 10) x 25  C. 30 x (25 x 10)",
    "P97-Q2": "23005 divided by 23005 is: A. 0  B. 23005  C. 1",
    "P97-Q3": "How many seconds are there in 3 hours?",
    "P97-Q4": "3250 divided by 18 is shown as quotient 179 and remainder 28. Which check can be used to find the mistake? A. quotient x divisor + remainder = dividend  B. remainder < dividend  C. remainder = divisor",
    "P97-Q5": "15 added to itself 15 times can be written as which multiplication?",
    "P97-Q6": "A sailfish can swim at 109 km/h. How fast can 9 sailfish swim?",
    "P97-Q7": "The remainder is always smaller than the divisor. True or False?",
    "P97-Q8": "The product of the smallest two-digit number and the smallest three-digit number is: one thousand / the smallest four-digit number / 1000 / all of these.",
    "P97-Q9": "Name the angles shown using: acute, right, obtuse, straight, reflex.",
    "P98-Q1": "Divide 2180 by 2.",
    "P98-Q2": "Divide 7048 by 24.",
    "P98-Q3": "Divide 888 by 12.",
    "P98-Q4": "Using a known right angle, draw 3 items with angles smaller than a right angle.",
    "P98-Q5": "Using a known right angle, draw 3 items with angles greater than a right angle.",
    "P99-Q1": "Saira buys 4 pens at Rs 50 each and 8 pencils at Rs 40 each. How much does she spend in all?",
    "P99-Q2": "Tim buys 3 hats for Rs 120. At the same rate, how many hats can he buy for Rs 240?",
    "P99-Q3": "Megha has 475 cookies. She packs 12 cookies in each box. How many full boxes can she fill and how many cookies are left?",
    "P99-Q4": "Complete the division table. Columns: 720, 480. Rows: 60, 15. Each cell is column divided by row.",
}

SOURCE_ISSUE = {
    "P97-Q4": "DEFECTIVE_PRINTED_ITEM: no printed option states the complete standard remainder rule; actual result is 180 R10.",
    "P97-Q6": "SEMANTICALLY_INVALID_STORY: separate animal speeds are not normally added as one collective speed.",
    "P97-Q9": "PHOTO_MAPPING_UNCERTAIN: exact picture-to-name order is not asserted.",
}

_NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _display(ref: str) -> str:
    page, q = ref.split("-", 1)
    return f"Page {page[1:]} {q}"


def _source_identity(ref: str) -> Dict[str, Any]:
    text = SOURCE_TEXT[ref]
    page, q = ref.split("-", 1)
    return {
        "source_ref": ref,
        "source_display_ref": _display(ref),
        "source_text": text,
        "source_numeric_tokens": list(dict.fromkeys(_NUM_RE.findall(text))),
        "source_asset_ref": None,
        "source_page_or_image_index": int(page[1:]),
        "source_section_label": None,
        "source_item_label": q,
        "source_issue": SOURCE_ISSUE.get(ref),
    }


def source_q(
    question_id: str,
    ref: str,
    answer_text: str,
    *,
    answer_kind: str = "EXACT",
    check_route: str = "ANSWER_MAP",
    support_policy: str = "NO_HINT",
    hint_modality: str = "NONE",
    hint_text: str | None = None,
    visual_ref: str | None = None,
    extra_prompt: str = "",
) -> Dict[str, Any]:
    prompt = SOURCE_TEXT[ref]
    if extra_prompt:
        prompt = f"{prompt} {extra_prompt}"
    return {
        "question_id": question_id,
        "origin": "SOURCE",
        "display_ref": _display(ref),
        "prompt": prompt,
        "source_identity": _source_identity(ref),
        "task_support_policy": support_policy,
        "answer_contract": {
            "answer_kind": answer_kind,
            "answer_text": answer_text,
            "check_route": check_route,
            "answer_ref": f"ANS-{question_id}",
        },
        "hint_contract": {
            "modality": hint_modality,
            "hint_text": hint_text,
            "visual_ref": visual_ref,
            "may_reveal_final_answer": False,
        },
    }


def practice_q(
    question_id: str,
    display_ref: str,
    prompt: str,
    answer_text: str,
    *,
    answer_kind: str = "EXACT",
    check_route: str = "ANSWER_MAP",
    support_policy: str = "NO_HINT",
    hint_modality: str = "NONE",
    hint_text: str | None = None,
    visual_ref: str | None = None,
) -> Dict[str, Any]:
    return {
        "question_id": question_id,
        "origin": "GENERATED_PRACTICE",
        "display_ref": display_ref,
        "prompt": prompt,
        "source_identity": None,
        "task_support_policy": support_policy,
        "answer_contract": {
            "answer_kind": answer_kind,
            "answer_text": answer_text,
            "check_route": check_route,
            "answer_ref": f"ANS-{question_id}",
        },
        "hint_contract": {
            "modality": hint_modality,
            "hint_text": hint_text,
            "visual_ref": visual_ref,
            "may_reveal_final_answer": False,
        },
    }


def B(
    block_id: str,
    block_type: str,
    title: str,
    body: str,
    *,
    visibility: str = "HIDDEN",
    refs: Iterable[str] = (),
    representation=None,
    solution_text: str = "",
    questions: Iterable[Dict[str, Any]] = (),
) -> Dict[str, Any]:
    out = {
        "block_id": block_id,
        "block_type": block_type,
        "title": title,
        "body": body,
        "answer_visibility": visibility,
        "source_refs": list(refs),
    }
    if representation is not None:
        out["representation"] = representation
    qs = list(questions)
    if qs:
        out["questions"] = qs
    if solution_text:
        out["solution_text"] = solution_text
    return out


def build_study_journey() -> Dict[str, Any]:
    modules = [
        {
            "module_id": "M1-MULTIPLICATIVE-STRUCTURE",
            "title": "Multiplication patterns and equivalent products",
            "learning_goal": "See repeated addition, factor regrouping and place-value products as connected multiplication structures.",
            "source_refs": ["P97-Q1", "P97-Q5", "P97-Q6", "P97-Q8"],
            "concept_refs": ["MULT_EQUAL_GROUPS", "MULT_DISTRIBUTIVE", "PV_POWERS_OF_TEN"],
            "prerequisite_bridges": [{"bridge_id": "BR-M1-FACTORS", "statement": "Regrouping factors changes the route, not the product.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["confusing addition with factor regrouping", "treating an invalid story as a valid physical quantity"],
            "blocks": [
                B("M1-SEE", "SEE_DISCOVER", "See the structure", "15 added 15 times is 15 equal groups of 15. 25 x 30 can be regrouped because 30 = 3 x 10.", refs=["P97-Q1", "P97-Q5"]),
                B("M1-WORKED", "WORKED_EXAMPLE", "Worked example: equivalent product", "Regroup the factors before calculating.", visibility="WORKED_EXAMPLE", refs=["P97-Q1"], solution_text="25 x 30 = 25 x (3 x 10) = 3 x 10 x 25 = 750.", questions=[source_q("M1-W-Q1", "P97-Q1", "A. 3 x 10 x 25; the product is 750.", check_route="INLINE")]),
                B("M1-NOTICE", "NOTICE", "Source meaning matters", "The sailfish item is treated only as the workbook's intended equal-groups arithmetic; separate animal speeds are not one combined speed.", refs=["P97-Q6"]),
                B("M1-INDEPENDENT", "INDEPENDENT_TRY", "Try without support", "Choose the structure and explain why it works.", refs=["P97-Q1", "P97-Q8"], questions=[practice_q("M1-P-A", "Practice A", "Which expression is equivalent to 18 x 40? Then find 10 x 100 and describe the size of the product.", "18 x 40 = 18 x 4 x 10 = 720; 10 x 100 = 1000.")]),
            ],
            "mastery_evidence": ["identifies equal groups", "regroups factors without changing values", "uses powers of ten deliberately"],
        },
        {
            "module_id": "M2-DIVISION-RULES",
            "title": "Division rules: inverse facts and remainders",
            "learning_goal": "Use multiplication to check division and apply the remainder bound correctly.",
            "source_refs": ["P97-Q2", "P97-Q4", "P97-Q7"],
            "concept_refs": ["DIV_INVERSE_MULTIPLICATION", "DIV_ESTIMATE_CHECK", "DIV_REMAINDER_CONTEXT"],
            "prerequisite_bridges": [{"bridge_id": "BR-M2-CHECK", "statement": "A valid division with remainder satisfies divisor x quotient + remainder = dividend and 0 <= remainder < divisor.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["checking only the rebuild identity", "comparing remainder with dividend instead of divisor"],
            "blocks": [
                B("M2-CONNECT", "CONNECT", "Multiplication is division's check", "If a non-zero number is divided by itself, the quotient is 1. Rebuild a division answer with divisor x quotient + remainder.", refs=["P97-Q2", "P97-Q4"]),
                B("M2-WORKED", "WORKED_EXAMPLE", "Error detective", "The printed pair rebuilds 3250, but the remainder rule still fails.", visibility="WORKED_EXAMPLE", refs=["P97-Q4"], solution_text="18 x 179 + 28 = 3250, but 28 is not smaller than 18. The valid result is 180 R10.", questions=[source_q("M2-W-Q4", "P97-Q4", "No printed option states the complete standard rule. The remainder must be smaller than 18; the valid result is 180 R10.", answer_kind="SOURCE_DEFECT_RESOLUTION", check_route="INLINE")]),
                B("M2-GUIDED", "GUIDED_TRY", "Check both rules", "Do not stop after one successful check.", visibility="PARTIAL", refs=["P97-Q7"], questions=[practice_q("M2-P-A", "Practice A", "For 214 / 9 = 23 R7, check the rebuild identity and the remainder bound.", "9 x 23 + 7 = 214 and 7 < 9, so the result is valid.", check_route="CHECK_AFTER_TRY", support_policy="NUMERIC_FIRST", hint_modality="NUMERIC", hint_text="Start with 9 x 23 + 7. Then compare 7 with 9.")]),
                B("M2-INDEPENDENT", "INDEPENDENT_TRY", "Fresh check", "Decide whether a new quotient-remainder pair is valid.", refs=["P97-Q7"], questions=[practice_q("M2-P-B", "Fresh Try A", "Can a remainder be 12 when the divisor is 12? Explain using the rule.", "No. A remainder must be smaller than the divisor, so it must be less than 12.")]),
            ],
            "mastery_evidence": ["uses both division checks", "rejects a remainder equal to or larger than the divisor"],
        },
        {
            "module_id": "M3-WRITTEN-DIVISION",
            "title": "Written division: keep the place values visible",
            "learning_goal": "Use the divide-multiply-subtract-bring-down cycle and preserve quotient place value.",
            "source_refs": ["P98-Q1", "P98-Q2", "P98-Q3"],
            "concept_refs": ["DIV_WRITTEN_ONE_DIGIT_DIVISOR", "DIV_WRITTEN_MULTI_DIGIT_DIVISOR", "DIV_ESTIMATE_CHECK"],
            "prerequisite_bridges": [{"bridge_id": "BR-M3-MULTIPLES", "statement": "For a two-digit divisor, a small multiples strip helps choose quotient digits without guessing.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["missing quotient-place zero", "guessing a quotient digit", "stopping before checking the remainder"],
            "blocks": [
                B("M3-SEE", "SEE_DISCOVER", "The 5-move routine", "DIVIDE -> MULTIPLY -> SUBTRACT -> BRING DOWN -> CHECK. Every quotient digit owns a place.", refs=["P98-Q1", "P98-Q2", "P98-Q3"]),
                B("M3-WORKED", "WORKED_EXAMPLE", "Worked example: 2180 / 2", "Follow the written structure one place at a time.", visibility="WORKED_EXAMPLE", refs=["P98-Q1"], solution_text="2180 / 2 = 1090 R0. The zero in the quotient preserves place structure.", questions=[source_q("M3-W-Q1", "P98-Q1", "1090", check_route="INLINE")]),
                B("M3-GUIDED", "GUIDED_TRY", "Guided example: 888 / 12", "Estimate first, then choose a multiple of 12 for each partial dividend.", visibility="PARTIAL", refs=["P98-Q3"], questions=[source_q("M3-G-Q3", "P98-Q3", "74", check_route="CHECK_AFTER_TRY", support_policy="NUMERIC_FIRST", hint_modality="NUMERIC", hint_text="12 x 7 = 84. After subtracting 84 from 88, bring down the last 8.", extra_prompt="Set it up as written division and use multiples of 12.")]),
                B("M3-INDEPENDENT", "INDEPENDENT_TRY", "Independent division", "Use the full long-division workspace and check the final remainder.", refs=["P98-Q2"], questions=[source_q("M3-I-Q2", "P98-Q2", "293 R16", extra_prompt="Estimate first, show the written work, then verify divisor x quotient + remainder.")]),
            ],
            "mastery_evidence": ["aligns quotient digits", "uses divisor multiples", "checks the remainder"],
        },
        {
            "module_id": "M4-TIME-UNITS",
            "title": "Unit chains: hours to seconds",
            "learning_goal": "Convert through connected units before calculating.",
            "source_refs": ["P97-Q3"],
            "concept_refs": ["MEAS_TIME", "MEAS_UNIT_CHAIN"],
            "prerequisite_bridges": [{"bridge_id": "BR-M4-UNITS", "statement": "Keep the unit beside each factor so the chain can be checked.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["using one conversion factor instead of two"],
            "blocks": [
                B("M4-SEE", "SEE_DISCOVER", "Follow the unit chain", "hours -> minutes -> seconds", refs=["P97-Q3"]),
                B("M4-WORKED", "WORKED_EXAMPLE", "Worked conversion", "Use both conversion steps.", visibility="WORKED_EXAMPLE", refs=["P97-Q3"], solution_text="3 hours x 60 minutes/hour x 60 seconds/minute = 10,800 seconds.", questions=[source_q("M4-W-Q3", "P97-Q3", "10,800 seconds", check_route="INLINE")]),
                B("M4-INDEPENDENT", "INDEPENDENT_TRY", "Fresh conversion", "Show the unit chain, not only the final number.", refs=["P97-Q3"], questions=[practice_q("M4-P-A", "Fresh Try A", "How many seconds are there in 2 hours?", "7,200 seconds")]),
            ],
            "mastery_evidence": ["writes both conversion factors", "keeps units connected"],
        },
        {
            "module_id": "M5-ANGLES",
            "title": "Angles: compare every turn with a right angle",
            "learning_goal": "Classify benchmark angle types and draw angles smaller or greater than a right angle.",
            "source_refs": ["P97-Q9", "P98-Q4", "P98-Q5"],
            "concept_refs": ["GEOM_ANGLE_MEASURE"],
            "prerequisite_bridges": [{"bridge_id": "BR-M5-BENCHMARK", "statement": "Use 90 degrees as the main comparison benchmark; straight is 180 degrees and reflex is greater than 180 degrees.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["judging ray length instead of opening", "confusing obtuse and reflex"],
            "blocks": [
                B("M5-SEE", "SEE_DISCOVER", "Five benchmark openings", "Acute < 90, right = 90, obtuse is between 90 and 180, straight = 180, reflex > 180.", refs=["P97-Q9"]),
                B("M5-GUIDED", "GUIDED_TRY", "Draw smaller turns", "Use a right-angle corner as your comparison tool.", visibility="PARTIAL", refs=["P98-Q4"], representation={"kind":"ANGLE_BENCHMARK_COMPARE","params":{"benchmark_degrees":90},"fidelity":"SCHEMATIC"}, questions=[source_q("M5-G-Q4", "P98-Q4", "Any three valid acute-angle drawings, each smaller than 90 degrees.", answer_kind="RUBRIC", check_route="CHECK_AFTER_TRY", support_policy="VISUAL_FIRST", hint_modality="VISUAL", hint_text="Compare each opening with the right-angle benchmark.", visual_ref="M5-GUIDED")]),
                B("M5-INDEPENDENT", "INDEPENDENT_TRY", "Draw greater turns", "Draw, label the vertex, and compare the opening with 90 degrees.", refs=["P98-Q5"], questions=[source_q("M5-I-Q5", "P98-Q5", "Any three valid obtuse-angle drawings, each greater than 90 degrees and less than 180 degrees.", answer_kind="RUBRIC")]),
            ],
            "mastery_evidence": ["classifies five angle types", "uses the opening not ray length", "draws acute/obtuse examples"],
        },
        {
            "module_id": "M6-MONEY-RATE",
            "title": "Money and same-rate scaling",
            "learning_goal": "Separate subtotals, then use a scale relationship when price and count change together.",
            "source_refs": ["P99-Q1", "P99-Q2"],
            "concept_refs": ["MEAS_MONEY", "MODEL_MULTI_STEP", "MODEL_QUANTITY_STRUCTURE"],
            "prerequisite_bridges": [{"bridge_id": "BR-M6-RATE", "statement": "At the same rate, if the money amount is multiplied by a factor, the item count is multiplied by the same factor.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["adding unit prices without multiplying by counts", "scaling money but not item count"],
            "blocks": [
                B("M6-WORKED", "WORKED_EXAMPLE", "Worked example: two-part money total", "Find each subtotal before adding.", visibility="WORKED_EXAMPLE", refs=["P99-Q1"], solution_text="4 x Rs50 = Rs200 and 8 x Rs40 = Rs320, so the total is Rs520.", questions=[source_q("M6-W-Q1", "P99-Q1", "Rs 520", check_route="INLINE")]),
                B("M6-SEE", "SEE_DISCOVER", "Same-rate scale", "3 hats correspond to Rs120. Rs240 is twice the money, so the count must use the same scale factor.", refs=["P99-Q2"]),
                B("M6-INDEPENDENT", "INDEPENDENT_TRY", "Fresh rate problem", "Write the scale factor before calculating the new count.", refs=["P99-Q2"], questions=[practice_q("M6-P-A", "Fresh Try A", "4 identical tickets cost Rs150. At the same rate, how many tickets correspond to Rs300?", "8 tickets")]),
            ],
            "mastery_evidence": ["forms subtotals", "identifies a scale factor", "applies the same factor to count and money"],
        },
        {
            "module_id": "M7-REMAINDER-TABLE",
            "title": "Full groups, leftovers and division tables",
            "learning_goal": "Interpret quotient/remainder in context and complete structured division tables.",
            "source_refs": ["P99-Q3", "P99-Q4"],
            "concept_refs": ["DIV_REMAINDER_CONTEXT", "DIV_INVERSE_MULTIPLICATION"],
            "prerequisite_bridges": [{"bridge_id": "BR-M7-GROUPS", "statement": "The quotient counts complete groups; the remainder is what cannot make another full group.", "provenance": "PEDAGOGICAL_BRIDGE"}],
            "misconception_targets": ["reporting quotient without interpreting leftover", "reversing row and column roles in a division table"],
            "blocks": [
                B("M7-WORKED", "WORKED_EXAMPLE", "Worked context: cookies in boxes", "Find the largest complete multiple of 12 below 475, then interpret the leftover.", visibility="WORKED_EXAMPLE", refs=["P99-Q3"], solution_text="12 x 39 = 468, so there are 39 full boxes and 7 cookies left.", questions=[source_q("M7-W-Q3", "P99-Q3", "39 full boxes and 7 cookies left", check_route="INLINE")]),
                B("M7-CONNECT", "CONNECT", "Read the division table", "Each cell is column heading divided by row heading.", refs=["P99-Q4"]),
                B("M7-INDEPENDENT", "INDEPENDENT_TRY", "Complete the table", "Estimate each cell and use multiplication to check.", refs=["P99-Q4"], questions=[source_q("M7-I-Q4", "P99-Q4", "720/60=12; 480/60=8; 720/15=48; 480/15=32.")]),
            ],
            "mastery_evidence": ["interprets full groups and leftover", "uses row/column roles correctly", "checks a quotient with multiplication"],
        },
        {
            "module_id": "M8-RETRIEVE-TRANSFER",
            "title": "Mixed retrieval, error analysis and transfer",
            "learning_goal": "Choose the structure without being told the topic, explain mistakes precisely, and finish with independent evidence.",
            "source_refs": ALL_REFS,
            "concept_refs": ["MIXED_RETRIEVAL"],
            "prerequisite_bridges": [],
            "misconception_targets": ["operation by keyword", "answer without units/check", "supported success mistaken for independence"],
            "blocks": [
                B("M8-ERROR", "ERROR_ANALYSIS", "Error detective", "Name the exact broken rule rather than saying only 'careless mistake'.", refs=["P97-Q4", "P97-Q6", "P98-Q2", "P99-Q2"], questions=[
                    practice_q("M8-E-A", "Practice A", "A learner says 3250 / 18 = 179 R28 because 18 x 179 + 28 = 3250. What exact rule is still broken?", "The remainder rule is broken: 28 is not smaller than 18.", answer_kind="EXEMPLAR"),
                    practice_q("M8-E-B", "Practice B", "A learner says nine sailfish swimming at 109 km/h have one combined speed of 981 km/h. What is wrong with the story meaning?", "Speeds of separate animals are not added to make one collective speed.", answer_kind="EXEMPLAR"),
                    practice_q("M8-E-C", "Practice C", "A learner divides 7048 by 24 but does not check the remainder. What check should be added?", "Check 24 x quotient + remainder = 7048 and remainder < 24.", answer_kind="EXEMPLAR"),
                ]),
                B("M8-RETRIEVAL", "RETRIEVAL", "Mixed independent check", "Solve without hints. Mark the structure you used beside each item.", refs=ALL_REFS, questions=[
                    practice_q("M8-R-A", "Check A", "18 x 40: write an equivalent product.", "18 x 4 x 10 = 720."),
                    practice_q("M8-R-B", "Check B", "3240 / 2.", "1620."),
                    practice_q("M8-R-C", "Check C", "Classify 35, 90, 135, 180, 225 degrees.", "acute, right, obtuse, straight, reflex."),
                    practice_q("M8-R-D", "Check D", "289 beads are packed 12 per bag. How many full bags and how many beads left?", "24 full bags and 1 bead left."),
                    practice_q("M8-R-E", "Check E", "4 tickets cost Rs150. At the same rate, how many tickets correspond to Rs300?", "8 tickets."),
                ]),
                B("M8-SELF", "SELF_CHECK", "My learning check", "Circle the exact skill to revisit: factor structure, division check, quotient place, unit chain, angle benchmark, rate scale, remainder meaning, or table roles.", refs=ALL_REFS),
                B("M8-ANSWERS", "REFERENCE", "Answer check", "Use only after the mixed independent check. Every learner question has an answer contract and stable answer reference.", visibility="ANSWER_KEY_ONLY", refs=ALL_REFS, solution_text="See the answer references printed beside each question."),
            ],
            "mastery_evidence": ["solves mixed tasks without topic labels", "names exact error mechanism", "uses independent retry as evidence"],
        },
    ]

    return {
        "schema_version": "1.0.0",
        "journey_id": "THE-PUPIL-P97-P99-STUDY-JOURNEY",
        "title": "Grade 4 Mathematics Revision Journey",
        "grade_level": 4,
        "topic": "Workbook pages 97-99",
        "modules": modules,
        "source_coverage": {"required_source_refs": ALL_REFS, "covered_source_refs": ALL_REFS},
    }
