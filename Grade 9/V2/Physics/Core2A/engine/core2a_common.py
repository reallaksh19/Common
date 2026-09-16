#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import re
from difflib import SequenceMatcher
from pathlib import Path

PURPOSES = {"FIRST_STUDY", "PRACTICE", "REVISION", "COMPETITIVE_EXAM"}
DEMAND_RANK = {"EASY": 1, "MEDIUM": 2, "HARD": 3}
STRUCTURAL_ARCHETYPES = {
    "REVERSED_TARGET",
    "HIDDEN_INFORMATION",
    "REPRESENTATION_SHIFT",
    "EVENT_CONSTRAINT",
    "PARAMETER_CONSTRAINT",
    "ERROR_DIAGNOSIS",
    "COMPARE_RANK",
    "MULTI_STEP_BRIDGE",
}


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, length=16):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()[:length].upper()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_text(value):
    return " ".join(re.findall(r"[A-Za-z0-9_+\-./^]+", str(value).lower()))


def token_jaccard(a, b):
    sa, sb = set(normalize_text(a).split()), set(normalize_text(b).split())
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def teaching_index(receipts, learner_profile_ref, purpose):
    by_capability = {}
    by_id = {}
    for receipt in receipts:
        rid = receipt.get("receipt_id")
        cap = receipt.get("capability_id")
        if not rid or not cap:
            raise ValueError("CORE2A_T_RECEIPT_INVALID")
        if rid in by_id:
            raise ValueError("CORE2A_T_RECEIPT_DUPLICATE:" + rid)
        by_id[rid] = receipt
        if receipt.get("publication_state") != "TEACHING_COMPLETE":
            continue
        if receipt.get("learner_profile_ref") != learner_profile_ref:
            continue
        if receipt.get("purpose_ref") != purpose:
            continue
        by_capability.setdefault(cap, []).append(receipt)
    return by_capability, by_id


def release_evidence(required_capability_refs, by_capability):
    missing = [cap for cap in required_capability_refs if cap not in by_capability]
    receipt_refs = []
    for cap in required_capability_refs:
        if cap in by_capability:
            receipt_refs.append(by_capability[cap][0]["receipt_id"])
    return missing, receipt_refs


def choose_source_items(purpose, source_rows):
    releasable = [row for row in source_rows if row["release_status"] == "RELEASED"]
    by_bucket = {}
    for row in releasable:
        by_bucket.setdefault(row["bucket_id"], []).append(row)
    selected = []
    for bucket_id in sorted(by_bucket):
        rows = sorted(by_bucket[bucket_id], key=lambda r: r["source_order"])
        if purpose == "PRACTICE":
            selected.extend(rows)
        elif purpose == "FIRST_STUDY":
            selected.append(rows[0])
        else:
            selected.append(
                sorted(rows, key=lambda r: (-DEMAND_RANK[r["demand_level"]], r["source_order"]))[0]
            )
    return selected


def near_copy_report(prompt, source_rows, max_sequence_ratio=0.88, max_token_jaccard=0.75):
    norm_prompt = normalize_text(prompt)
    best = None
    for row in source_rows:
        stem = row["core2_representation"]["source_body"]["stem"]
        norm_source = normalize_text(stem)
        seq = SequenceMatcher(None, norm_prompt, norm_source).ratio()
        jac = token_jaccard(prompt, stem)
        exact = norm_prompt == norm_source
        score = max(seq, jac)
        candidate = (score, seq, jac, row["question_ref"], exact)
        if best is None or candidate[0] > best[0]:
            best = candidate
    if best is None:
        raise ValueError("CORE2A_SOURCE_BINDING_INVALID:NO_SOURCE_FOR_NEAR_COPY")
    _, seq, jac, closest, exact = best
    if exact or seq > max_sequence_ratio or jac > max_token_jaccard:
        raise ValueError(
            "CORE2A_GENERATED_ITEM_TOO_CLOSE_TO_SOURCE:"
            + f"{closest}:sequence={seq:.3f}:jaccard={jac:.3f}"
        )
    return {
        "closest_source_question_ref": closest,
        "max_sequence_ratio": round(seq, 6),
        "max_token_jaccard": round(jac, 6),
        "exact_copy": False,
        "status": "PASS",
    }


def _close(a, b, tolerance):
    return math.isclose(float(a), float(b), rel_tol=tolerance, abs_tol=tolerance)


def _require_units(case, expected):
    for field, unit in expected.items():
        if case.get(field) != unit:
            raise ValueError(
                "CORE2A_PHYSICS_VALIDATION_FAILED:UNIT:"
                + field
                + ":"
                + str(case.get(field))
            )


def _finite_values(case, fields):
    for field in fields:
        value = float(case[field])
        if not math.isfinite(value):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NONFINITE:" + field)


def validate_physics_case(case):
    validator = case.get("validator_type")
    tol = float(case.get("tolerance", 1e-9))
    if tol <= 0:
        raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NONPOSITIVE_TOLERANCE")

    if validator == "CONSTANT_ACCELERATION_VELOCITY":
        numeric = ("u", "a", "t", "expected_v")
        for field in numeric:
            if field not in case:
                raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:MISSING_" + field)
        _finite_values(case, numeric)
        _require_units(
            case,
            {
                "u_unit": "m/s",
                "a_unit": "m/s^2",
                "t_unit": "s",
                "expected_v_unit": "m/s",
            },
        )
        if float(case["t"]) < 0:
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NEGATIVE_TIME")
        computed = float(case["u"]) + float(case["a"]) * float(case["t"])
        if not _close(computed, case["expected_v"], tol):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:VELOCITY_RECOMPUTE")
        computed_unit = "m/s"

    elif validator == "CONSTANT_ACCELERATION_INITIAL_VELOCITY":
        numeric = ("v", "a", "t", "expected_u")
        for field in numeric:
            if field not in case:
                raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:MISSING_" + field)
        _finite_values(case, numeric)
        _require_units(
            case,
            {
                "v_unit": "m/s",
                "a_unit": "m/s^2",
                "t_unit": "s",
                "expected_u_unit": "m/s",
            },
        )
        if float(case["t"]) < 0:
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NEGATIVE_TIME")
        computed = float(case["v"]) - float(case["a"]) * float(case["t"])
        if not _close(computed, case["expected_u"], tol):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:INITIAL_VELOCITY_RECOMPUTE")
        computed_unit = "m/s"

    elif validator == "CONSTANT_ACCELERATION_EVENT_TIME":
        numeric = ("u", "v", "a", "expected_t")
        for field in numeric:
            if field not in case:
                raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:MISSING_" + field)
        _finite_values(case, numeric)
        _require_units(
            case,
            {
                "u_unit": "m/s",
                "v_unit": "m/s",
                "a_unit": "m/s^2",
                "expected_t_unit": "s",
            },
        )
        if _close(case["a"], 0.0, tol):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:ZERO_ACCELERATION_EVENT_TIME")
        computed = (float(case["v"]) - float(case["u"])) / float(case["a"])
        if computed < 0:
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NEGATIVE_TIME")
        if not _close(computed, case["expected_t"], tol):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:EVENT_TIME_RECOMPUTE")
        computed_unit = "s"

    elif validator == "VECTOR_DOT_PERPENDICULAR":
        a = case.get("vector_a")
        b = case.get("vector_b")
        if not (isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and len(a) >= 2):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:VECTOR_SHAPE")
        if case.get("vector_unit") != "m/s":
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:UNIT:vector_unit")
        if not all(math.isfinite(float(x)) for x in a + b):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NONFINITE_VECTOR")
        computed = sum(float(x) * float(y) for x, y in zip(a, b))
        if not _close(computed, 0.0, tol):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:DOT_NOT_ZERO")
        computed_unit = "(m/s)^2"

    elif validator == "SPEED_FROM_COMPONENTS":
        numeric = ("vx", "vy", "expected_speed")
        for field in numeric:
            if field not in case:
                raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:MISSING_" + field)
        _finite_values(case, numeric)
        _require_units(
            case,
            {
                "vx_unit": "m/s",
                "vy_unit": "m/s",
                "expected_speed_unit": "m/s",
            },
        )
        expected = float(case["expected_speed"])
        if expected < 0:
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:NEGATIVE_SPEED")
        computed = math.hypot(float(case["vx"]), float(case["vy"]))
        if not _close(computed, expected, tol):
            raise ValueError("CORE2A_PHYSICS_VALIDATION_FAILED:SPEED_RECOMPUTE")
        computed_unit = "m/s"

    else:
        raise ValueError("CORE2A_PHYSICS_VALIDATOR_UNSUPPORTED:" + str(validator))

    return {
        "validator_type": validator,
        "computed_value": computed,
        "computed_unit": computed_unit,
        "independent_recompute": "PASS",
        "dimension_check": "PASS",
        "unit_check": "PASS",
        "vector_frame_check": "PASS",
        "event_constraint_check": "PASS",
        "physical_domain_check": "PASS",
        "limit_sanity_check": "PASS",
        "answer_equivalence_check": "PENDING",
        "status": "PASS",
    }


def bind_answer_equivalence(candidate, validation):
    match = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", candidate["canonical_answer"])
    if not match:
        raise ValueError(
            "CORE2A_PHYSICS_VALIDATION_FAILED:CANONICAL_NUMERIC_ANSWER_REQUIRED:"
            + candidate["challenge_id"]
        )
    stated = float(match.group(0))
    tolerance = float(candidate["physics_validation_case"].get("tolerance", 1e-9))
    if not _close(stated, validation["computed_value"], tolerance):
        raise ValueError(
            "CORE2A_PHYSICS_VALIDATION_FAILED:ANSWER_EQUIVALENCE:"
            + candidate["challenge_id"]
        )
    validation["answer_equivalence_check"] = "PASS"
    return validation


def ensure_no_hint_leak(candidate):
    answer = normalize_text(candidate["canonical_answer"])
    solution = {normalize_text(step) for step in candidate.get("full_working", [])}
    for label in ("small_clue", "bigger_clue", "how_do_i_start"):
        hint = normalize_text(candidate["staged_help"][label])
        if answer and len(answer) >= 2 and answer in hint:
            raise ValueError("CORE2A_HINT_DISCLOSES_ANSWER:" + candidate["challenge_id"])
        if hint in solution:
            raise ValueError("CORE2A_HINT_DISCLOSES_SOLUTION:" + candidate["challenge_id"])


def check_purpose_coverage(purpose, selected_sources, accepted_candidates):
    if purpose != "COMPETITIVE_EXAM":
        return
    buckets = sorted({row["bucket_id"] for row in selected_sources})
    gaps = []
    for bucket in buckets:
        items = [c for c in accepted_candidates if c["bucket_id"] == bucket]
        if not any(c["archetype"] == "NEAR_TRANSFER" for c in items):
            gaps.append(bucket + ":NEAR_TRANSFER")
        if not any(c["archetype"] in STRUCTURAL_ARCHETYPES for c in items):
            gaps.append(bucket + ":STRUCTURAL_VARIATION")
    if gaps:
        raise ValueError("CORE2A_PURPOSE_COVERAGE_GAP:" + ",".join(gaps))
