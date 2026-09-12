"""Document-level study journey for The Pupil pages 97-99.

Unlike task-level fixtures, this groups evidence into teaching concepts.  The
sequence is intentionally teach-first: discover -> connect -> worked example ->
guided practice -> independent evidence -> retrieval/transfer.
"""
from __future__ import annotations

from typing import Any, Dict

ALL_REFS = [
    "P97-Q1", "P97-Q2", "P97-Q3", "P97-Q4", "P97-Q5", "P97-Q6", "P97-Q7", "P97-Q8", "P97-Q9",
    "P98-Q1", "P98-Q2", "P98-Q3", "P98-Q4", "P98-Q5", "P99-Q1", "P99-Q2", "P99-Q3", "P99-Q4",
]


def B(block_id: str, block_type: str, title: str, body: str, *, visibility: str = "HIDDEN", refs=(), representation=None, learner_prompt: str = "", solution_text: str = "") -> Dict[str, Any]:
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
    if learner_prompt:
        out["learner_prompt"] = learner_prompt
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
                B("M1-WORKED", "WORKED_EXAMPLE", "Worked example: equivalent product", "Regroup the factors before calculating.", visibility="WORKED_EXAMPLE", refs=["P97-Q1"], solution_text="25 x 30 = 25 x (3 x 10) = 3 x 10 x 25 = 750."),
                B("M1-NOTICE", "NOTICE", "Source meaning matters", "The sailfish item is treated only as the workbook's intended equal-groups arithmetic; separate animal speeds are not one combined speed.", refs=["P97-Q6"]),
                B("M1-INDEPENDENT", "INDEPENDENT_TRY", "Try without support", "Choose the equivalent product and explain why the factors still represent the same product.", refs=["P97-Q1", "P97-Q8"], learner_prompt="Which expression is equivalent to 18 x 40? Then find 10 x 100 and describe the size of the product."),
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
                B("M2-WORKED", "WORKED_EXAMPLE", "Error detective", "The printed pair 179 R28 rebuilds 3250, but the remainder rule still fails.", visibility="WORKED_EXAMPLE", refs=["P97-Q4"], solution_text="18 x 179 + 28 = 3250, but 28 is not smaller than 18. The valid result is 180 R10."),
                B("M2-GUIDED", "GUIDED_TRY", "Check both rules", "Do not stop after one successful check.", visibility="PARTIAL", refs=["P97-Q7"], learner_prompt="For 214 / 9 = 23 R7, check the rebuild identity and the remainder bound."),
                B("M2-INDEPENDENT", "INDEPENDENT_TRY", "Fresh check", "Decide whether a new quotient-remainder pair is valid.", refs=["P97-Q7"], learner_prompt="Can a remainder be 12 when the divisor is 12? Explain using the rule."),
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
                B("M3-WORKED", "WORKED_EXAMPLE", "Worked example: 2180 / 2", "Follow the written structure one place at a time.", visibility="WORKED_EXAMPLE", refs=["P98-Q1"], solution_text="2180 / 2 = 1090 R0. The zero in the quotient preserves the tens/ones place structure."),
                B("M3-GUIDED", "GUIDED_TRY", "Guided example: 888 / 12", "Estimate first, then choose a multiple of 12 for each partial dividend.", visibility="PARTIAL", refs=["P98-Q3"], learner_prompt="Set up 888 / 12. Use multiples of 12 to choose the first quotient digit."),
                B("M3-INDEPENDENT", "INDEPENDENT_TRY", "Independent division", "Use the full long-division workspace and check the final remainder.", refs=["P98-Q2"], learner_prompt="Divide 7048 by 24. Estimate first, show the written work, then verify divisor x quotient + remainder."),
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
                B("M4-WORKED", "WORKED_EXAMPLE", "Worked conversion", "Use both conversion steps.", visibility="WORKED_EXAMPLE", refs=["P97-Q3"], solution_text="3 hours x 60 minutes/hour x 60 seconds/minute = 10,800 seconds."),
                B("M4-INDEPENDENT", "INDEPENDENT_TRY", "Fresh conversion", "Show the unit chain, not only the final number.", refs=["P97-Q3"], learner_prompt="How many seconds are there in 2 hours?"),
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
                B("M5-GUIDED", "GUIDED_TRY", "Draw smaller turns", "Use a right-angle corner as your comparison tool.", visibility="PARTIAL", refs=["P98-Q4"], learner_prompt="Draw three different angles smaller than a right angle."),
                B("M5-INDEPENDENT", "INDEPENDENT_TRY", "Draw greater turns", "Draw, label the vertex, and compare the opening with 90 degrees.", refs=["P98-Q5"], learner_prompt="Draw three different angles greater than a right angle but less than a straight angle."),
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
                B("M6-WORKED", "WORKED_EXAMPLE", "Worked example: two-part money total", "Find each subtotal before adding.", visibility="WORKED_EXAMPLE", refs=["P99-Q1"], solution_text="4 x Rs50 = Rs200 and 8 x Rs40 = Rs320, so the total is Rs520."),
                B("M6-SEE", "SEE_DISCOVER", "Same-rate scale", "3 hats correspond to Rs120. Rs240 is twice the money, so the count must use the same scale factor.", refs=["P99-Q2"]),
                B("M6-INDEPENDENT", "INDEPENDENT_TRY", "Fresh rate problem", "Write the scale factor before calculating the new count.", refs=["P99-Q2"], learner_prompt="4 identical tickets cost Rs150. At the same rate, how many tickets correspond to Rs300?"),
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
                B("M7-WORKED", "WORKED_EXAMPLE", "Worked context: cookies in boxes", "Find the largest complete multiple of 12 below 475, then interpret the leftover.", visibility="WORKED_EXAMPLE", refs=["P99-Q3"], solution_text="12 x 39 = 468, so there are 39 full boxes and 7 cookies left."),
                B("M7-CONNECT", "CONNECT", "Read the division table", "Each cell is column heading divided by row heading.", refs=["P99-Q4"]),
                B("M7-INDEPENDENT", "INDEPENDENT_TRY", "Complete the table", "Estimate each cell and use multiplication to check.", refs=["P99-Q4"], learner_prompt="Complete the table with columns 720 and 480 and rows 60 and 15."),
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
                B("M8-ERROR", "ERROR_ANALYSIS", "Error detective", "Name the exact broken rule: operation choice, unit chain, quotient place, remainder bound, or scale relationship.", refs=["P97-Q4", "P97-Q6", "P98-Q2", "P99-Q2"]),
                B("M8-RETRIEVAL", "RETRIEVAL", "Mixed independent check", "Solve without hints. Mark the structure you used beside each item.", refs=ALL_REFS, learner_prompt="1) 18 x 40: write an equivalent product. 2) 3240 / 2. 3) Classify 35, 90, 135, 180, 225 degrees. 4) 289 beads packed 12 per bag. 5) 4 tickets cost Rs150; same rate for Rs300."),
                B("M8-SELF", "SELF_CHECK", "My learning check", "Circle the exact skill to revisit: factor structure, division check, quotient place, unit chain, angle benchmark, rate scale, remainder meaning, or table roles.", refs=ALL_REFS),
                B("M8-ANSWERS", "REFERENCE", "Answer check", "Use only after the mixed independent check.", visibility="ANSWER_KEY_ONLY", refs=ALL_REFS, solution_text="Fresh checks: 18 x 40 can be 18 x 4 x 10; 3240 / 2 = 1620; angles are acute/right/obtuse/straight/reflex; 289 / 12 = 24 R1; tickets = 8."),
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
