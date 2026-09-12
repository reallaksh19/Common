"""Curated semantic extraction fixture for The Pupil pages 97-99.

This file is intentionally explicit. It does not infer concepts or pedagogy from
keywords. Every source task has a unique concept key, typed capabilities/problem
families, grounded representation requirements, and a LearningDesign blueprint.
Source defects remain attached as source notes and are never silently repaired.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source.json"
FADES = ["FULL", "PARTIAL", "NONE"]


def _rep(qref: str, name: str, kind: str, params: Mapping[str, Any], *, role: str = "STRUCTURAL", validators: Iterable[str] = ("SOURCE_GROUNDED",)) -> Dict[str, Any]:
    return {
        "representation_id": f"REP-{qref}-{name}",
        "role": role,
        "primitive_kind": kind,
        "semantic_params": dict(params),
        "validator_refs": list(validators),
        "fade_modes": list(FADES),
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }


def _selection(ref: str, fidelity: str = "SCHEMATIC", fade: str = "PARTIAL") -> Dict[str, Any]:
    return {"representation_ref": ref, "fidelity": fidelity, "fade_mode": fade}


def _blueprint(
    *,
    prompt: str,
    task_kind: str,
    primary_ref: str,
    support_refs: list[str],
    representation_class: str = "STRUCTURAL",
    source_note: str | None = None,
    solution_tokens: Iterable[str] = (),
    allowed_support_solution_tokens: Iterable[str] = (),
    work_surface: Mapping[str, Any] | None = None,
    fresh_prompt: str,
    cues: tuple[str, str, str] | None = None,
) -> Dict[str, Any]:
    refs = (support_refs + [support_refs[-1]] * 4)[:4]
    h1, h2, h3 = cues or (
        "Look at the quantities and their roles.",
        "Remember the relationship shown by the visual.",
        "Show the first executable step only.",
    )
    out: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "task_kind": task_kind,
        "representation_class": representation_class,
        "learner_prompt": prompt,
        "solution_tokens": list(solution_tokens),
        "allowed_support_solution_tokens": list(allowed_support_solution_tokens),
        "primary": _selection(primary_ref, "SCHEMATIC", "FULL"),
        "hint_steps": [
            {
                "level": "H1", "semantic_role": "NOTICE", "child_label": "LOOK",
                **_selection(refs[0], "SCHEMATIC", "FULL"),
                "verbal_cue": h1,
                "learner_action": "Point to the important quantities or benchmark.",
                "information_revealed": ["STRUCTURE_ONLY"],
            },
            {
                "level": "H2", "semantic_role": "REMEMBER", "child_label": "REMEMBER",
                **_selection(refs[1], "SCHEMATIC", "PARTIAL"),
                "verbal_cue": h2,
                "learner_action": "Say the rule or relationship before calculating.",
                "information_revealed": ["RELATIONSHIP_ONLY"],
            },
            {
                "level": "H3", "semantic_role": "REPRESENT", "child_label": "SHOW IT",
                **_selection(refs[2], "SCHEMATIC", "PARTIAL"),
                "verbal_cue": h3,
                "learner_action": "Write or draw only the first step, then continue yourself.",
                "information_revealed": ["FIRST_STEP_ONLY"],
            },
        ],
        "thinking_path": [
            {
                "semantic_role": "INTERPRET", "child_label": "LOOK",
                **_selection(refs[0], "SCHEMATIC", "PARTIAL"),
                "one_line_action": "Read the quantities and roles."
            },
            {
                "semantic_role": "MODEL", "child_label": "SHOW IT",
                **_selection(refs[1], "SCHEMATIC", "PARTIAL"),
                "one_line_action": "Show the relationship."
            },
            {
                "semantic_role": "EXECUTE", "child_label": "WORK",
                **_selection(refs[2], "SCHEMATIC", "PARTIAL"),
                "one_line_action": "Do one step at a time."
            },
            {
                "semantic_role": "VERIFY", "child_label": "CHECK",
                **_selection(refs[3], "SCHEMATIC", "NONE"),
                "one_line_action": "Check the rule and the units."
            },
        ],
        "fresh_retry_prompt": fresh_prompt,
        "visual_language_key": {"structure": "BLUE", "action": "TEAL", "check": "GREEN"},
    }
    if source_note:
        out["source_note"] = source_note
    if work_surface is not None:
        out["work_surface_template"] = dict(work_surface)
    return out


def _long_division_surface(dividend: int, divisor: int, quotient: int, remainder: int, steps: list[Mapping[str, Any]]) -> Dict[str, Any]:
    return {
        "kind": "LONG_DIVISION_WORK",
        "semantic_params": {
            "dividend": dividend,
            "divisor": divisor,
            "quotient": quotient,
            "remainder": remainder,
            "quotient_places": [int(x) for x in str(quotient)],
            "steps": [dict(step) for step in steps],
            "check": {"identity_holds": divisor * quotient + remainder == dividend, "remainder_in_range": 0 <= remainder < divisor},
        },
        "validator_refs": ["DIVISION_IDENTITY_AND_STEPS", "REMAINDER_RANGE"],
        "provenance": "AUTHORED_NOTEBOOK_EXAMPLE",
    }


def _angle_surface(slots: int = 3) -> Dict[str, Any]:
    return {
        "kind": "ANGLE_DRAWING_WORKSPACE",
        "semantic_params": {"slots": slots},
        "validator_refs": ["ANGLE_GEOMETRY"],
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }


def _table_surface() -> Dict[str, Any]:
    return {
        "kind": "DIVISION_TABLE_WORKSPACE",
        "semantic_params": {
            "columns": [720, 480],
            "rows": [60, 15],
            "cells": [
                {"column": 720, "row": 60, "quotient": 12},
                {"column": 480, "row": 60, "quotient": 8},
                {"column": 720, "row": 15, "quotient": 48},
                {"column": 480, "row": 15, "quotient": 32},
            ],
        },
        "validator_refs": ["DIVISION_TABLE"],
        "provenance": "ENGINE_AUTHORED_VISUAL",
    }


def _source_index() -> Dict[str, Dict[str, Any]]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    return {row["question_ref"]: row for row in payload["questions"]}


def _specs() -> Dict[str, Dict[str, Any]]:
    specs: Dict[str, Dict[str, Any]] = {}

    def add(qref: str, *, title: str, caps: list[str], families: list[str], reps: list[Dict[str, Any]], blueprint: Dict[str, Any], quantity: Mapping[str, Any] | None = None):
        specs[qref] = {
            "title": title,
            "caps": caps,
            "families": families,
            "reps": reps,
            "blueprint": blueprint,
            "quantity": dict(quantity) if quantity else None,
        }

    q = "P97-Q1"
    r1 = _rep(q, "STRUCTURE", "QUANTITY_STRUCTURE_MAP", {"branches": ["25 x 30", "3 x 10 x 25"]})
    add(q, title="Equivalent multiplication products", caps=["MULT_DISTRIBUTIVE", "REASON_METHOD_COMPARE"], families=["PF_METHOD_COMPARE"], reps=[r1], blueprint=_blueprint(prompt="Which product is the same as 25 x 30? A. 3 x 10 x 25  B. (3 + 10) x 25  C. 30 x (25 x 10)", task_kind="EQUIVALENT_PRODUCT", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=["750"], fresh_prompt="Which expression is equivalent to 18 x 40? Explain the factor regrouping before calculating."))

    q = "P97-Q2"
    r1 = _rep(q, "SELF", "INVERSE_CHECK", {"expression": "23005 / 23005"})
    add(q, title="A non-zero number divided by itself", caps=["DIV_INVERSE_MULTIPLICATION"], families=["PF_UNKNOWN_EQUALITY"], reps=[r1], blueprint=_blueprint(prompt="23005 divided by 23005 is: A. 0  B. 23005  C. 1", task_kind="DIVISION_IDENTITY", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=["1"], fresh_prompt="Without long division, decide 807 divided by 807 and explain why."))

    q = "P97-Q3"
    r1 = _rep(q, "CHAIN", "QUANTITY_STRUCTURE_MAP", {"branches": ["3 hours", "60 min per hour", "60 sec per min"]})
    add(q, title="Convert hours to seconds", caps=["MEAS_TIME", "MEAS_UNIT_CHAIN"], families=["PF_RATE_UNIT_CHAIN"], reps=[r1], blueprint=_blueprint(prompt="How many seconds are there in 3 hours?", task_kind="UNIT_CHAIN", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=["10800"], fresh_prompt="How many seconds are there in 2 hours? Show the unit chain."))

    q = "P97-Q4"
    r1 = _rep(q, "REBUILD", "INVERSE_CHECK", {"expression": "18 x 179 + 28 = 3250"})
    r2 = _rep(q, "RULE", "QUANTITY_STRUCTURE_MAP", {"branches": ["remainder 28", "divisor 18"]})
    source_note = "DEFECTIVE_PRINTED_ITEM: the rebuild identity passes, but 28 is not smaller than divisor 18. No printed option states the complete standard remainder rule; actual division is 180 R10."
    add(q, title="Check quotient and remainder", caps=["DIV_ESTIMATE_CHECK", "REASON_ERROR_ANALYSIS", "REASON_INVERSE_CHECK"], families=["PF_ERROR_ANALYSIS", "PF_ESTIMATE_VERIFY"], reps=[r1, r2], blueprint=_blueprint(prompt="3250 divided by 18 is shown as quotient 179 and remainder 28. Which check can be used to find the mistake? A. quotient x divisor + remainder = dividend  B. remainder < dividend  C. remainder = divisor", task_kind="DIVISION_ERROR_ANALYSIS", primary_ref=r2["representation_id"], support_refs=[r1["representation_id"], r2["representation_id"]], source_note=source_note, fresh_prompt="A division result is shown as 214 / 9 = 23 R7. Check both the rebuild identity and the remainder bound."))

    q = "P97-Q5"
    r1 = _rep(q, "GROUPS", "EQUAL_GROUPS", {"group_count": 15, "items_per_group": 15}, role="PICTORIAL")
    add(q, title="Repeated addition as multiplication", caps=["MULT_EQUAL_GROUPS"], families=["PF_EQUAL_GROUPS"], reps=[r1], blueprint=_blueprint(prompt="15 added to itself 15 times can be written as which multiplication?", task_kind="REPEATED_ADDITION", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=["225"], fresh_prompt="Write 8 added to itself 6 times as multiplication, then calculate."))

    q = "P97-Q6"
    r1 = _rep(q, "GROUPS", "EQUAL_GROUPS", {"group_count": 9, "items_per_group": 109}, role="PICTORIAL")
    source_note = "SEMANTICALLY_INVALID_STORY: separate animal speeds are not added into one collective speed. The workbook's intended arithmetic is 9 equal groups of 109."
    add(q, title="Interpret the workbook's intended equal-groups arithmetic", caps=["MULT_EQUAL_GROUPS", "MODEL_QUANTITY_STRUCTURE"], families=["PF_EQUAL_GROUPS"], reps=[r1], blueprint=_blueprint(prompt="A sailfish can swim at 109 km/h. How fast can 9 sailfish swim?", task_kind="SOURCE_INTENT_EQUAL_GROUPS", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], source_note=source_note, solution_tokens=["981"], fresh_prompt="A valid combined-distance story has 7 cars each travel 84 km. Find the total distance travelled by all cars."))

    q = "P97-Q7"
    r1 = _rep(q, "REMAINDER", "DIV_REMAINDER_CONTEXT", {"group_size": 12, "leftover": 5})
    add(q, title="Remainder must be smaller than divisor", caps=["DIV_REMAINDER_CONTEXT"], families=["PF_REMAINDER_CONTEXT"], reps=[r1], blueprint=_blueprint(prompt="The remainder is always smaller than the divisor. True or False?", task_kind="REMAINDER_RULE", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=["True"], fresh_prompt="Can a remainder be 12 when the divisor is 12? Explain using the remainder rule."))

    q = "P97-Q8"
    r1 = _rep(q, "PLACE", "QUANTITY_STRUCTURE_MAP", {"branches": ["smallest 2-digit = 10", "smallest 3-digit = 100"]})
    add(q, title="Smallest two-digit times smallest three-digit", caps=["MULT_EQUAL_GROUPS", "PV_POWERS_OF_TEN"], families=["PF_EQUAL_GROUPS"], reps=[r1], blueprint=_blueprint(prompt="The product of the smallest two-digit number and the smallest three-digit number is: one thousand / the smallest four-digit number / 1000 / all of these.", task_kind="PLACE_VALUE_PRODUCT", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=["1000"], fresh_prompt="Find 10 x 200 and describe the place-value size of the product."))

    q = "P97-Q9"
    r1 = _rep(q, "ACUTE", "ANGLE_BENCHMARK_COMPARE", {"degrees": 45})
    r2 = _rep(q, "OBTUSE", "ANGLE_BENCHMARK_COMPARE", {"degrees": 120})
    r3 = _rep(q, "REFLEX", "ANGLE_RAYS_ARC", {"degrees": 240})
    source_note = "PHOTO_MAPPING_UNCERTAIN: exact source picture-to-name order is not asserted; clean benchmark geometry is used to teach acute/right/obtuse/straight/reflex classification."
    add(q, title="Classify acute, right, obtuse, straight and reflex angles", caps=["GEOM_ANGLE_MEASURE"], families=["PF_ANGLE_MEASURE"], reps=[r1, r2, r3], blueprint=_blueprint(prompt="Name the angles shown using: acute, right, obtuse, straight, reflex.", task_kind="GEOMETRY_ANGLE_CLASSIFY", primary_ref=r2["representation_id"], support_refs=[r1["representation_id"], r2["representation_id"], r3["representation_id"]], source_note=source_note, fresh_prompt="Classify 35 degrees, 90 degrees, 135 degrees, 180 degrees and 225 degrees by angle type."))

    division_specs = [
        ("P98-Q1", 2180, 2, 1090, 0, [
            {"partial_dividend": 2, "quotient_digit": 1, "product": 2, "subtraction_remainder": 0, "bring_down_digit": 1},
            {"partial_dividend": 1, "quotient_digit": 0, "product": 0, "subtraction_remainder": 1, "bring_down_digit": 8},
            {"partial_dividend": 18, "quotient_digit": 9, "product": 18, "subtraction_remainder": 0, "bring_down_digit": 0},
            {"partial_dividend": 0, "quotient_digit": 0, "product": 0, "subtraction_remainder": 0, "bring_down_digit": None},
        ], "Divide 2180 by 2.", "Divide 3240 by 2 using the same written structure."),
        ("P98-Q2", 7048, 24, 293, 16, [
            {"partial_dividend": 70, "quotient_digit": 2, "product": 48, "subtraction_remainder": 22, "bring_down_digit": 4},
            {"partial_dividend": 224, "quotient_digit": 9, "product": 216, "subtraction_remainder": 8, "bring_down_digit": 8},
            {"partial_dividend": 88, "quotient_digit": 3, "product": 72, "subtraction_remainder": 16, "bring_down_digit": None},
        ], "Divide 7048 by 24.", "Divide 724 by 24. Show the quotient and remainder, then check them."),
        ("P98-Q3", 888, 12, 74, 0, [
            {"partial_dividend": 88, "quotient_digit": 7, "product": 84, "subtraction_remainder": 4, "bring_down_digit": 8},
            {"partial_dividend": 48, "quotient_digit": 4, "product": 48, "subtraction_remainder": 0, "bring_down_digit": None},
        ], "Divide 888 by 12.", "Divide 972 by 12 using the same written structure."),
    ]
    for q, dividend, divisor, quotient, remainder, steps, prompt, fresh in division_specs:
        r1 = _rep(q, "ALGORITHM", "DIV_LONG_ALGORITHM", {"dividend": dividend, "divisor": divisor}, role="PROCEDURAL", validators=("DIVISION_SETUP",))
        add(q, title=f"Written division: {dividend} divided by {divisor}", caps=["DIV_WRITTEN_ONE_DIGIT_DIVISOR" if divisor < 10 else "DIV_WRITTEN_MULTI_DIGIT_DIVISOR", "DIV_ESTIMATE_CHECK"], families=["PF_MEASUREMENT_GROUPING", "PF_ESTIMATE_VERIFY"], reps=[r1], blueprint=_blueprint(prompt=prompt, task_kind="MULTI_DIGIT_DIVISION", representation_class="PROCEDURAL_WORK", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], solution_tokens=[str(quotient)] + ([str(remainder)] if remainder else []), work_surface=_long_division_surface(dividend, divisor, quotient, remainder, steps), fresh_prompt=fresh, cues=("Notice the divisor and where the quotient digits will sit.", "Estimate which multiple of the divisor fits the current partial dividend.", "Write only the first quotient digit and multiplication line.")))

    q = "P98-Q4"
    r1 = _rep(q, "BENCHMARK", "ANGLE_BENCHMARK_COMPARE", {"degrees": 45})
    add(q, title="Draw angles smaller than a right angle", caps=["GEOM_ANGLE_MEASURE"], families=["PF_ANGLE_MEASURE"], reps=[r1], blueprint=_blueprint(prompt="Using a known right angle, draw 3 items with angles smaller than a right angle.", task_kind="ANGLE_DRAW_ACUTE", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], work_surface=_angle_surface(3), fresh_prompt="Draw three different acute angles. Mark each vertex."))

    q = "P98-Q5"
    r1 = _rep(q, "BENCHMARK", "ANGLE_BENCHMARK_COMPARE", {"degrees": 120})
    add(q, title="Draw angles greater than a right angle", caps=["GEOM_ANGLE_MEASURE"], families=["PF_ANGLE_MEASURE"], reps=[r1], blueprint=_blueprint(prompt="Using a known right angle, draw 3 items with angles greater than a right angle.", task_kind="ANGLE_DRAW_OBTUSE", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"]], work_surface=_angle_surface(3), fresh_prompt="Draw three different obtuse angles. Mark each vertex."))

    q = "P99-Q1"
    r1 = _rep(q, "MONEY", "MONEY_MODEL", {"groups": [{"kind": "PEN", "count": 4, "unit_price": 50}, {"kind": "PENCIL", "count": 8, "unit_price": 40}]}, role="PICTORIAL", validators=("MONEY_STRUCTURE",))
    r2 = _rep(q, "BRANCHES", "QUANTITY_STRUCTURE_MAP", {"branches": ["4 x Rs50", "8 x Rs40"]})
    add(q, title="Two-part money total", caps=["MEAS_MONEY", "MODEL_MULTI_STEP"], families=["PF_MONEY_COMPOSE_CHANGE", "PF_MULTI_STEP_COMPOSITION"], reps=[r1, r2], blueprint=_blueprint(prompt="Saira buys 4 pens at Rs 50 each and 8 pencils at Rs 40 each. How much does she spend in all?", task_kind="MONEY_MULTI_PART", representation_class="CONCRETE_PICTORIAL", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"], r2["representation_id"]], solution_tokens=["520"], fresh_prompt="A child buys 3 notebooks at Rs 60 each and 5 erasers at Rs 20 each. Find the total cost."))

    q = "P99-Q2"
    r1 = _rep(q, "RATE", "RATE_COMPARE", {"base_amount": 120, "target_amount": 240})
    r2 = _rep(q, "SCALE", "SCALE_FACTOR_VIEW", {"scale_factor": 2})
    r3 = _rep(q, "COUNT", "OBJECT_GROUPS", {"groups": [{"kind": "HAT", "count": 3}]}, role="PICTORIAL")
    add(q, title="Scale a same-rate purchase", caps=["MODEL_QUANTITY_STRUCTURE", "MULT_EQUAL_GROUPS"], families=["PF_RATE_UNIT_CHAIN"], reps=[r1, r2, r3], blueprint=_blueprint(prompt="Tim buys 3 hats for Rs 120. At the same rate, how many hats can he buy for Rs 240?", task_kind="RATE_SCALE_REASONING", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"], r2["representation_id"], r3["representation_id"]], solution_tokens=["6"], fresh_prompt="4 identical tickets cost Rs 150. At the same rate, how many tickets correspond to Rs 300?"))

    q = "P99-Q3"
    r1 = _rep(q, "STRUCTURE", "QUANTITY_STRUCTURE_MAP", {"branches": ["475 cookies", "12 in each full box"]})
    r2 = _rep(q, "GROUP", "DIV_EQUAL_GROUP", {"group_size": 12})
    r3 = _rep(q, "MULTIPLES", "DIV_MULTIPLES_STRIP", {"divisor": 12})
    add(q, title="Full groups and a remainder", caps=["DIV_REMAINDER_CONTEXT", "DIV_PARTIAL_QUOTIENT"], families=["PF_REMAINDER_CONTEXT", "PF_MEASUREMENT_GROUPING"], reps=[r1, r2, r3], blueprint=_blueprint(prompt="Megha has 475 cookies. She packs 12 cookies in each box. How many full boxes can she fill and how many cookies are left?", task_kind="DIVISION_REMAINDER_CONTEXT", primary_ref=r1["representation_id"], support_refs=[r1["representation_id"], r2["representation_id"], r3["representation_id"]], solution_tokens=["39", "7"], fresh_prompt="289 beads are packed 12 per bag. Find the number of full bags and the leftover beads."))

    q = "P99-Q4"
    r1 = _rep(q, "TABLE", "DIVISION_TABLE_MODEL", {"columns": [720, 480], "rows": [60, 15]})
    r2 = _rep(q, "ROLES", "DIVISION_TABLE_ROLE_HIGHLIGHT", {"columns": [720, 480], "rows": [60, 15]})
    r3 = _rep(q, "CELL", "DIVISION_TABLE_CELL_MODEL", {"operation": "column/row"})
    add(q, title="Complete a division table", caps=["DIV_INVERSE_MULTIPLICATION", "DIV_ESTIMATE_CHECK"], families=["PF_ESTIMATE_VERIFY"], reps=[r1, r2, r3], blueprint=_blueprint(prompt="Complete the division table. Columns: 720, 480. Rows: 60, 15. Each cell is column divided by row.", task_kind="DIVISION_TABLE", primary_ref=r1["representation_id"], support_refs=[r2["representation_id"], r3["representation_id"], r1["representation_id"]], solution_tokens=["12", "8", "48", "32"], work_surface=_table_surface(), fresh_prompt="Complete a new 2 by 2 division table by dividing each column heading by each row heading."))

    return specs


def build_primary_input() -> Dict[str, Any]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    specs = _specs()
    questions = []
    for row in source["questions"]:
        qref = row["question_ref"]
        spec = specs[qref]
        ambiguity = []
        if row.get("source_issue"):
            ambiguity.append(str(row["source_issue"]))
        evidence = {
            "question_ref": qref,
            "source_ref": f"THE-PUPIL-P{row['page']}",
            "raw_text": row["raw_text"],
            "concept_key": f"WORKBOOK-{qref}",
            "concept_title": spec["title"],
            "scope_basis": "QUESTION_SET_OBSERVED",
            "authority_ref": None,
            "capability_refs": spec["caps"],
            "prerequisite_refs": [],
            "problem_family_refs": spec["families"],
            "translation_refs": [],
            "quantity_structure": spec["quantity"],
            "representation_requirements": spec["reps"],
            "learning_support_blueprint": spec["blueprint"],
            "ambiguity": ambiguity,
            "source_refs": [f"THE-PUPIL-P{row['page']}", qref],
        }
        questions.append({"question_ref": qref, "text": row["raw_text"], "evidence": evidence})

    return {
        "schema_version": "1.0.0",
        "input_id": "THE-PUPIL-P97-P99-CORE1",
        "question_set": {
            "source_ref": "THE-PUPIL-P97-P99",
            "questions": questions,
        },
        "topic_hints": ["Grade 4 workbook pages 97-99", "multiplication", "division", "angles", "money"],
    }


if __name__ == "__main__":
    print(json.dumps(build_primary_input(), indent=2))
