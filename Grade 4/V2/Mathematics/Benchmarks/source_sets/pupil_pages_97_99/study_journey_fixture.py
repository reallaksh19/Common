"""Source-anchored document-level StudyJourney for The Pupil pages 97-99."""
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


def _identity(ref: str) -> Dict[str, Any]:
    page, q = ref.split("-", 1)
    text = SOURCE_TEXT[ref]
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


def SQ(
    qid: str,
    ref: str,
    answer: str,
    *,
    route: str = "ANSWER_MAP",
    kind: str = "EXACT",
    policy: str = "NO_HINT",
    modality: str = "NONE",
    hint: str | None = None,
    visual_ref: str | None = None,
    extra: str = "",
) -> Dict[str, Any]:
    prompt = SOURCE_TEXT[ref] + (f" {extra}" if extra else "")
    return {
        "question_id": qid,
        "origin": "SOURCE",
        "display_ref": _display(ref),
        "prompt": prompt,
        "source_identity": _identity(ref),
        "task_support_policy": policy,
        "answer_contract": {"answer_kind": kind, "answer_text": answer, "check_route": route, "answer_ref": f"ANS-{qid}"},
        "hint_contract": {"modality": modality, "hint_text": hint, "visual_ref": visual_ref, "may_reveal_final_answer": False},
    }


def PQ(
    qid: str,
    label: str,
    prompt: str,
    answer: str,
    *,
    route: str = "ANSWER_MAP",
    kind: str = "EXACT",
    policy: str = "NO_HINT",
    modality: str = "NONE",
    hint: str | None = None,
    visual_ref: str | None = None,
) -> Dict[str, Any]:
    return {
        "question_id": qid,
        "origin": "GENERATED_PRACTICE",
        "display_ref": label,
        "prompt": prompt,
        "source_identity": None,
        "task_support_policy": policy,
        "answer_contract": {"answer_kind": kind, "answer_text": answer, "check_route": route, "answer_ref": f"ANS-{qid}"},
        "hint_contract": {"modality": modality, "hint_text": hint, "visual_ref": visual_ref, "may_reveal_final_answer": False},
    }


def B(
    block_id: str,
    block_type: str,
    title: str,
    body: str,
    *,
    visibility: str = "HIDDEN",
    refs: Iterable[str] = (),
    questions: Iterable[Dict[str, Any]] = (),
    solution_text: str = "",
    representation: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "block_id": block_id,
        "block_type": block_type,
        "title": title,
        "body": body,
        "answer_visibility": visibility,
        "source_refs": list(refs),
    }
    qs = list(questions)
    if qs:
        out["questions"] = qs
    if solution_text:
        out["solution_text"] = solution_text
    if representation is not None:
        out["representation"] = representation
    return out


def module(module_id: str, title: str, goal: str, refs: list[str], concepts: list[str], blocks: list[Dict[str, Any]], mastery: list[str], misconceptions: list[str] | None = None, bridges: list[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    return {
        "module_id": module_id,
        "title": title,
        "learning_goal": goal,
        "source_refs": refs,
        "concept_refs": concepts,
        "prerequisite_bridges": bridges or [],
        "misconception_targets": misconceptions or [],
        "blocks": blocks,
        "mastery_evidence": mastery,
    }


def build_study_journey() -> Dict[str, Any]:
    modules = [
        module(
            "M1-MULTIPLICATIVE-STRUCTURE",
            "Multiplication patterns and equivalent products",
            "Connect repeated addition, factor regrouping and powers of ten.",
            ["P97-Q1", "P97-Q5", "P97-Q6", "P97-Q8"],
            ["MULT_EQUAL_GROUPS", "MULT_DISTRIBUTIVE", "PV_POWERS_OF_TEN"],
            [
                B("M1-SEE", "SEE_DISCOVER", "See the structure", "Regrouping factors changes the route, not the product.", refs=["P97-Q1", "P97-Q5"]),
                B("M1-W", "WORKED_EXAMPLE", "Worked equivalent product", "Watch one complete source item.", visibility="WORKED_EXAMPLE", refs=["P97-Q1"], solution_text="25 x 30 = 25 x (3 x 10) = 3 x 10 x 25 = 750.", questions=[SQ("M1-Q1", "P97-Q1", "A. 3 x 10 x 25; product 750.", route="INLINE")]),
                B("M1-G", "GUIDED_TRY", "Repeated addition", "Use equal groups.", visibility="PARTIAL", refs=["P97-Q5"], questions=[SQ("M1-Q5", "P97-Q5", "15 x 15", route="CHECK_AFTER_TRY", policy="NUMERIC_FIRST", modality="NUMERIC", hint="15 repeated 15 times means 15 groups of 15.")]),
                B("M1-I", "INDEPENDENT_TRY", "Source check", "Keep source meaning separate from intended arithmetic.", refs=["P97-Q6", "P97-Q8"], questions=[
                    SQ("M1-Q6", "P97-Q6", "The intended arithmetic is 9 x 109 = 981, but the story is physically invalid as a combined speed.", kind="SOURCE_DEFECT_RESOLUTION"),
                    SQ("M1-Q8", "P97-Q8", "All of these; 10 x 100 = 1000, the smallest four-digit number."),
                ]),
            ],
            ["regroups factors", "recognizes equal groups", "uses powers of ten"],
            ["confusing story meaning with arithmetic intent"],
        ),
        module(
            "M2-DIVISION-RULES",
            "Division rules: inverse facts and remainders",
            "Use inverse multiplication and the remainder bound.",
            ["P97-Q2", "P97-Q4", "P97-Q7"],
            ["DIV_INVERSE_MULTIPLICATION", "DIV_REMAINDER_CONTEXT"],
            [
                B("M2-CONNECT", "CONNECT", "Two checks", "Rebuild the dividend and compare the remainder with the divisor.", refs=["P97-Q2", "P97-Q4", "P97-Q7"]),
                B("M2-W", "WORKED_EXAMPLE", "Defective printed item", "One printed check is insufficient.", visibility="WORKED_EXAMPLE", refs=["P97-Q4"], solution_text="18 x 179 + 28 = 3250, but 28 is not smaller than 18. Correct result: 180 R10.", questions=[SQ("M2-Q4", "P97-Q4", "No option states the complete rule; valid result is 180 R10.", route="INLINE", kind="SOURCE_DEFECT_RESOLUTION")]),
                B("M2-G", "GUIDED_TRY", "Identity fact", "Use the inverse relationship.", visibility="PARTIAL", refs=["P97-Q2"], questions=[SQ("M2-Q2", "P97-Q2", "C. 1", route="CHECK_AFTER_TRY", policy="NUMERIC_FIRST", modality="NUMERIC", hint="23005 = 1 x 23005.")]),
                B("M2-I", "INDEPENDENT_TRY", "Remainder rule", "State the rule precisely.", refs=["P97-Q7"], questions=[SQ("M2-Q7", "P97-Q7", "True; 0 <= remainder < divisor.")]),
            ],
            ["checks division", "uses remainder bound"],
        ),
        module(
            "M3-WRITTEN-DIVISION",
            "Written division: keep the place values visible",
            "Use divide-multiply-subtract-bring-down and preserve quotient place value.",
            ["P98-Q1", "P98-Q2", "P98-Q3"],
            ["DIV_WRITTEN_ONE_DIGIT_DIVISOR", "DIV_WRITTEN_MULTI_DIGIT_DIVISOR"],
            [
                B("M3-SEE", "SEE_DISCOVER", "The 5-move routine", "DIVIDE -> MULTIPLY -> SUBTRACT -> BRING DOWN -> CHECK.", refs=["P98-Q1", "P98-Q2", "P98-Q3"]),
                B("M3-W", "WORKED_EXAMPLE", "Worked division", "Watch the place values.", visibility="WORKED_EXAMPLE", refs=["P98-Q1"], solution_text="2180 / 2 = 1090.", questions=[SQ("M3-Q1", "P98-Q1", "1090", route="INLINE")]),
                B("M3-G", "GUIDED_TRY", "Use multiples", "Choose quotient digits without guessing.", visibility="PARTIAL", refs=["P98-Q3"], questions=[SQ("M3-Q3", "P98-Q3", "74", route="CHECK_AFTER_TRY", policy="NUMERIC_FIRST", modality="NUMERIC", hint="12 x 7 = 84. Subtract 84 from 88, then bring down 8.")]),
                B("M3-I", "INDEPENDENT_TRY", "Independent long division", "Estimate, solve, then check.", refs=["P98-Q2"], questions=[SQ("M3-Q2", "P98-Q2", "293 R16")]),
            ],
            ["aligns quotient digits", "checks remainder"],
            ["skipping quotient places"],
        ),
        module(
            "M4-TIME-UNITS",
            "Unit chains: hours to seconds",
            "Convert through connected units before calculating.",
            ["P97-Q3"],
            ["MEAS_TIME", "MEAS_UNIT_CHAIN"],
            [
                B("M4-SEE", "SEE_DISCOVER", "Follow the unit chain", "hours -> minutes -> seconds", refs=["P97-Q3"]),
                B("M4-W", "WORKED_EXAMPLE", "Worked conversion", "Use both conversion factors.", visibility="WORKED_EXAMPLE", refs=["P97-Q3"], solution_text="3 x 60 x 60 = 10,800 seconds.", questions=[SQ("M4-Q3", "P97-Q3", "10,800 seconds", route="INLINE")]),
                B("M4-I", "INDEPENDENT_TRY", "Fresh conversion", "Keep units beside values.", refs=["P97-Q3"], questions=[PQ("M4-P-A", "Fresh Try A", "How many seconds are there in 2 hours?", "7,200 seconds")]),
            ],
            ["writes both conversion factors"],
        ),
        module(
            "M5-ANGLES",
            "Angles: compare every turn with a right angle",
            "Classify benchmark angles and draw smaller/greater openings.",
            ["P97-Q9", "P98-Q4", "P98-Q5"],
            ["GEOM_ANGLE_MEASURE"],
            [
                B("M5-SEE", "SEE_DISCOVER", "Use 90 degrees as a benchmark", "Acute < 90; right = 90; obtuse < 180; straight = 180; reflex > 180.", refs=["P97-Q9", "P98-Q4", "P98-Q5"]),
                B("M5-G1", "GUIDED_TRY", "Classify the source angles", "Use the openings, not ray lengths.", visibility="PARTIAL", refs=["P97-Q9"], representation={"kind": "ANGLE_CLASSIFICATION_SET", "params": {"angles": [45, 90, 135, 180, 225]}, "fidelity": "SCHEMATIC"}, questions=[SQ("M5-Q9", "P97-Q9", "acute, right, obtuse, straight, reflex", kind="RUBRIC", route="CHECK_AFTER_TRY", policy="VISUAL_FIRST", modality="VISUAL", hint="Compare each opening with a right angle.", visual_ref="M5-G1")]),
                B("M5-G2", "GUIDED_TRY", "Draw smaller turns", "Compare each drawing with 90 degrees.", visibility="PARTIAL", refs=["P98-Q4"], questions=[SQ("M5-Q4", "P98-Q4", "Any three valid acute-angle examples.", kind="RUBRIC", route="CHECK_AFTER_TRY", policy="VISUAL_FIRST", modality="VISUAL", hint="Use the right-angle benchmark below.", visual_ref="M5-G1")]),
                B("M5-I", "INDEPENDENT_TRY", "Draw greater turns", "Draw without support.", refs=["P98-Q5"], questions=[SQ("M5-Q5", "P98-Q5", "Any three valid obtuse-angle examples less than 180 degrees.", kind="RUBRIC")]),
            ],
            ["classifies angle types", "draws acute and obtuse examples"],
        ),
        module(
            "M6-MONEY-RATE",
            "Money and same-rate scaling",
            "Build subtotals and preserve the same rate.",
            ["P99-Q1", "P99-Q2"],
            ["MEAS_MONEY", "MODEL_QUANTITY_STRUCTURE"],
            [
                B("M6-W", "WORKED_EXAMPLE", "Two-part money total", "Find each subtotal first.", visibility="WORKED_EXAMPLE", refs=["P99-Q1"], solution_text="4 x 50 = 200; 8 x 40 = 320; total = Rs520.", questions=[SQ("M6-Q1", "P99-Q1", "Rs 520", route="INLINE")]),
                B("M6-SEE", "SEE_DISCOVER", "Same-rate scale", "If money doubles at the same rate, count doubles.", refs=["P99-Q2"]),
                B("M6-I", "INDEPENDENT_TRY", "Source rate problem", "Write the scale factor before the answer.", refs=["P99-Q2"], questions=[SQ("M6-Q2", "P99-Q2", "6 hats")]),
            ],
            ["forms subtotals", "uses same-rate scaling"],
        ),
        module(
            "M7-REMAINDER-TABLE",
            "Full groups, leftovers and division tables",
            "Interpret remainders and read row/column roles.",
            ["P99-Q3", "P99-Q4"],
            ["DIV_REMAINDER_CONTEXT", "DIV_INVERSE_MULTIPLICATION"],
            [
                B("M7-W", "WORKED_EXAMPLE", "Cookies in boxes", "Find complete groups and leftovers.", visibility="WORKED_EXAMPLE", refs=["P99-Q3"], solution_text="12 x 39 = 468; 7 cookies remain.", questions=[SQ("M7-Q3", "P99-Q3", "39 full boxes and 7 cookies left", route="INLINE")]),
                B("M7-CONNECT", "CONNECT", "Read the table", "Each cell is column heading divided by row heading.", refs=["P99-Q4"]),
                B("M7-I", "INDEPENDENT_TRY", "Complete the source table", "Use multiplication to check each cell.", refs=["P99-Q4"], questions=[SQ("M7-Q4", "P99-Q4", "720/60=12; 480/60=8; 720/15=48; 480/15=32.")]),
            ],
            ["interprets leftover", "uses table roles"],
        ),
        module(
            "M8-RETRIEVE-TRANSFER",
            "Mixed retrieval, error analysis and transfer",
            "Choose structures, diagnose exact mistakes and finish independently.",
            ALL_REFS,
            ["MIXED_RETRIEVAL"],
            [
                B("M8-ERROR", "ERROR_ANALYSIS", "Error detective", "Name the exact broken rule.", refs=["P97-Q4", "P97-Q6", "P98-Q2", "P99-Q2"], questions=[
                    PQ("M8-E-A", "Practice A", "A learner says 3250 / 18 = 179 R28 because 18 x 179 + 28 = 3250. What exact rule is broken?", "The remainder rule: 28 is not smaller than 18.", kind="EXEMPLAR"),
                    PQ("M8-E-B", "Practice B", "A learner treats nine sailfish at 109 km/h as one speed of 981 km/h. What is wrong with the story meaning?", "Separate animal speeds are not added into one collective speed.", kind="EXEMPLAR"),
                ]),
                B("M8-RETRIEVAL", "RETRIEVAL", "Mixed independent check", "Solve without hints.", refs=ALL_REFS, questions=[
                    PQ("M8-R-A", "Check A", "18 x 40: write an equivalent product.", "18 x 4 x 10 = 720."),
                    PQ("M8-R-B", "Check B", "3240 / 2.", "1620."),
                    PQ("M8-R-C", "Check C", "Classify 35, 90, 135, 180, 225 degrees.", "acute, right, obtuse, straight, reflex."),
                    PQ("M8-R-D", "Check D", "289 beads are packed 12 per bag. How many full bags and how many left?", "24 full bags and 1 bead left."),
                    PQ("M8-R-E", "Check E", "4 tickets cost Rs150. At the same rate, how many tickets correspond to Rs300?", "8 tickets."),
                ]),
                B("M8-SELF", "SELF_CHECK", "My learning check", "Circle the exact skill to revisit.", refs=ALL_REFS),
                B("M8-ANSWERS", "REFERENCE", "Answer check", "Every learner question has a stable answer reference.", visibility="ANSWER_KEY_ONLY", refs=ALL_REFS, solution_text="Use the answer references printed with each learner question."),
            ],
            ["solves mixed tasks", "names exact error mechanism", "uses independent evidence"],
        ),
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
