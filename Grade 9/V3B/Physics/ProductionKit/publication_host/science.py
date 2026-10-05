"""Use the existing Physics calculation owner; compare the displayed candidate."""

import math
import re
from xml.etree import ElementTree as ET

from validator import recompute
from v3b.contracts import digest, require, strings, text

RESULT_UNITS = {
    "SPEED_FROM_COMPONENTS": "m/s", "CONSTANT_ACCELERATION_VELOCITY": "m/s",
    "CONSTANT_ACCELERATION_INITIAL_VELOCITY": "m/s", "CONSTANT_ACCELERATION_EVENT_TIME": "s",
}
MATH_TAGS = {"math", "mrow", "mi", "mn", "mo", "mfrac", "msqrt", "msup", "msub",
             "msubsup", "mover", "munder", "munderover", "mtable", "mtr", "mtd", "mtext"}


def numeric_atom(ctx, atom_id, unit=None):
    require(atom_id in ctx["atoms"], "NUMERIC_ATOM_UNKNOWN", atom_id)
    atom = ctx["atoms"][atom_id]
    value = atom["value"]
    require(type(value) in {int, float} and math.isfinite(value), "NUMERIC_ATOM_INVALID", atom_id)
    require(isinstance(atom.get("unit"), str) and bool(atom["unit"]), "ATOM_UNIT_REQUIRED", atom_id)
    if unit is not None:
        require(atom["unit"] == unit, "ATOM_UNIT_MISMATCH", atom_id)
    return value


def numeric_expectation(ctx, block):
    source = ctx["questions"][(block["source_id"], block["source_question_id"])]
    rule = source.get("verification")
    candidate = block["answer"].get("numeric")
    if rule is None:
        return None if candidate is None else unverified_candidate(candidate, "NUMERIC_EVALUATOR_MISSING")
    kind = rule["validator_id"]
    require(isinstance(candidate, dict), "NUMERIC_CANDIDATE_REQUIRED", block["id"])
    if kind not in RESULT_UNITS:
        return unverified_candidate(candidate, "NUMERIC_EVALUATOR_UNSUPPORTED")
    case = {"validator_id": kind, "units": {}}
    for key in ("model", "axis_convention"):
        if key in rule:
            case[key] = rule[key]
    for variable, atom_id in rule["bindings"].items():
        require(variable not in {"validator_id", "model", "units", "axis_convention"},
                "CASE_BINDING_RESERVED")
        require(atom_id in block["source_atom_ids"], "ANSWER_SOURCE_BINDING_MISSING")
        case[variable] = numeric_atom(ctx, atom_id)
        case["units"][variable] = ctx["atoms"][atom_id]["unit"]
    value = recompute(case)
    compare_candidate(candidate["value"], candidate["unit"], value, RESULT_UNITS[kind])
    return {"value": value, "unit": RESULT_UNITS[kind], "case": case,
            "status": "VERIFIED_BY_SUPPORTED_EVALUATOR",
            "oracle": "EXISTING_PHYSICS_VALIDATOR_SOURCE_BOUND"}


def finite_candidate(value):
    if isinstance(value, str):
        require(bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", value.strip())),
                "PUBLISHED_NUMBER_INVALID")
        value = float(value)
    require(type(value) in {int, float} and math.isfinite(value), "NUMERIC_CANDIDATE_INVALID")
    return value


def unverified_candidate(candidate, code):
    require(isinstance(candidate, dict), "NUMERIC_CANDIDATE_REQUIRED")
    value = finite_candidate(candidate.get("value"))
    unit = text(candidate.get("unit"), "ANSWER_UNIT_REQUIRED")
    return {"status": "SCIENTIFIC_REVIEW_REQUIRED", "code": code, "value": value, "unit": unit,
            "oracle": "NONE", "blocking_scope": "LEARNER_READY_ONLY"}


def compare_candidate(value, unit, expected, expected_unit):
    value = finite_candidate(value)
    require(unit == expected_unit, "ANSWER_UNIT_MISMATCH")
    require(math.isclose(value, expected, rel_tol=1e-9, abs_tol=1e-9), "PUBLISHED_ANSWER_MISMATCH")


def equation_mathml(ctx, block):
    mathml = block["mathml"]
    equation_review(ctx, block)
    require("<!" not in mathml, "MATHML_DECLARATION_FORBIDDEN")
    root = ET.fromstring(mathml)
    require(root.tag.split("}")[-1] == "math", "MATHML_ROOT_REQUIRED")
    for node in root.iter():
        require(node.tag.split("}")[-1] in MATH_TAGS, "MATHML_TAG_UNSUPPORTED")
        require(set(node.attrib) <= {"display", "mathvariant"}, "MATHML_ATTRIBUTE_UNSUPPORTED")
    return mathml


def equation_review(ctx, block):
    sources = {a: ctx["atoms"][a] for a in block["source_atom_ids"]
               if ctx["atoms"][a].get("kind") == "EQUATION"}
    if block["mathml"] in [a["value"] for a in sources.values()]:
        return None
    change = block.get("transformation")
    require(isinstance(change, dict), "EQUATION_SOURCE_MISMATCH", block["id"])
    origin = change.get("source_atom_id")
    require(origin in sources, "EQUATION_TRANSFORMATION_SOURCE_INVALID")
    text(change.get("reason"), "EQUATION_TRANSFORMATION_REASON_REQUIRED")
    strings(change.get("steps"), "EQUATION_TRANSFORMATION_STEPS_REQUIRED")
    return {"status": "SCIENTIFIC_REVIEW_REQUIRED", "code": "EQUATION_TRANSFORMATION",
            "source_atom_id": origin, "source_digest": digest(sources[origin]),
            "candidate_digest": digest(block), "blocking_scope": "LEARNER_READY_ONLY"}
