#!/usr/bin/env python3
"""Independent acceptance evaluator for Primary Mathematics V2 candidates.

This module intentionally does not import the #324 renderer, page composer, or PDF
backend.  It recomputes benchmark assertions from a neutral candidate export.

Exit codes:
  0 = requested acceptance mode passed
  1 = benchmark failure
  2 = semantic acceptance passed but full artifact evidence is incomplete/blocked
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "benchmark_cases.json"


class AcceptanceFailure(Exception):
    def __init__(self, falsifier: str, message: str, case_id: str | None = None):
        super().__init__(message)
        self.falsifier = falsifier
        self.case_id = case_id
        self.message = message


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, falsifier: str, message: str, case_id: str) -> None:
    if not condition:
        raise AcceptanceFailure(falsifier, message, case_id)


def as_fraction(pair: list[int]) -> Fraction:
    return Fraction(pair[0], pair[1])


def check_scope(case_spec: dict[str, Any], evidence: dict[str, Any]) -> None:
    cid = case_spec["case_id"]
    scope = evidence.get("scope") or {}
    basis = scope.get("basis")
    expected = case_spec["scope_basis"]
    require(basis == expected, "SCOPE_BASIS_MISMATCH", f"expected {expected}, got {basis}", cid)
    if basis == "CURRICULUM_CONFIRMED":
        require(bool(scope.get("authority_ref")), "CURRICULUM_CONFIRMED_WITHOUT_AUTHORITY_REF", "curriculum-confirmed scope requires authority_ref", cid)
    if basis in {"QUESTION_SET_OBSERVED", "SCHOOL_CLASSWORK_OBSERVED"}:
        require(not scope.get("universal_grade_claim", False), "QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE", "observed school/question scope may not become a universal grade claim", cid)


def check_representations(case_spec: dict[str, Any], evidence: dict[str, Any]) -> None:
    cid = case_spec["case_id"]
    actual = set(evidence.get("representations") or [])
    required_roles = set(case_spec.get("required_representation_roles") or [])
    missing = sorted(required_roles - actual)
    require(not missing, "REQUIRED_REPRESENTATION_NOT_REALIZED", f"missing representation roles: {missing}", cid)


def check_product_links(case_spec: dict[str, Any], evidence: dict[str, Any]) -> None:
    cid = case_spec["case_id"]
    assertions = set(case_spec.get("required_assertions") or [])
    product = evidence.get("product_evidence") or {}
    if "CORE1_COVERAGE" in assertions:
        require(bool(product.get("core1_ref")), "CORE1_REQUIRED_COVERAGE_MISSING", "missing stable Core1 semantic reference", cid)
    if "CORE2_PRACTICE_LINK" in assertions:
        require(bool(product.get("core2_practice_ref")), "CORE2_REQUIRED_LINK_MISSING", "missing Core2 practice reference", cid)
    if product:
        require(not product.get("raw_question_direct_render", False), "RAW_QUESTIONS_RENDERED_DIRECTLY_WITHOUT_SKILL_MODEL", "candidate reports direct raw-question rendering", cid)
        if "core1_ref" in product and "resolved_core1_page" in product:
            require(not product.get("authored_page_number_hardcoded", False), "CORE2_LINK_HARDCODED_TO_STALE_PAGE_NUMBER", "Core1↔Core2 links must resolve from semantic references", cid)


def check_oracle(case_spec: dict[str, Any], evidence: dict[str, Any]) -> None:
    cid = case_spec["case_id"]
    oracle = case_spec["oracle"]
    kind = oracle["kind"]
    math = evidence.get("math_evidence") or {}

    if kind == "MULTIPLICATION_BRIDGE":
        a, b, product = oracle["a"], oracle["b"], oracle["product"]
        split = oracle["split"]
        require(math.get("a") == a and math.get("b") == b, "PRIMARY_VISUAL_UNGROUNDED_VALUE", "multiplication operands do not match benchmark", cid)
        require(math.get("split") == split and sum(split) == a, "MULTIPLICATION_DECOMPOSITION_INVALID", "place-value split is invalid", cid)
        expected_partials = [x * b for x in split]
        require(math.get("partial_products") == expected_partials, "MULTIPLICATION_PARTIAL_PRODUCTS_DO_NOT_SUM_TO_PRODUCT", "partial products are invalid", cid)
        require(sum(expected_partials) == product == a * b == math.get("product"), "MULTIPLICATION_PARTIAL_PRODUCTS_DO_NOT_SUM_TO_PRODUCT", "product does not close", cid)
        require(math.get("check_product") == product, "MULTIPLICATION_CHECK_INVALID", "multiplication check disagrees", cid)
        return

    if kind == "DIVISION_DUAL_MEANING":
        total, divisor, quotient = oracle["total"], oracle["divisor"], oracle["quotient"]
        require(total == divisor * quotient, "DIVISION_IDENTITY_INVALID", "division identity is invalid", cid)
        sharing = math.get("sharing") or {}
        grouping = math.get("grouping") or {}
        require(sharing.get("total") == total and sharing.get("group_count") == divisor and sharing.get("group_size") == quotient, "SHARING_AND_GROUPING_QUANTITY_ROLES_COLLAPSED", "sharing roles are invalid", cid)
        require(grouping.get("total") == total and grouping.get("group_size") == divisor and grouping.get("group_count") == quotient, "SHARING_AND_GROUPING_QUANTITY_ROLES_COLLAPSED", "grouping roles are invalid", cid)
        require(sharing.get("unknown_role") == "GROUP_SIZE" and grouping.get("unknown_role") == "GROUP_COUNT", "SHARING_AND_GROUPING_QUANTITY_ROLES_COLLAPSED", "unknown quantity roles must differ", cid)
        return

    if kind == "DIVISION_ALGORITHM":
        dividend = oracle["dividend"]
        divisor = oracle["divisor"]
        quotient = oracle["quotient"]
        remainder = oracle["remainder"]
        require(math.get("dividend") == dividend and math.get("divisor") == divisor, "PRIMARY_VISUAL_UNGROUNDED_VALUE", "division inputs do not match benchmark", cid)
        require(math.get("quotient") == quotient and math.get("remainder") == remainder, "DIVISION_IDENTITY_INVALID", "division result does not match benchmark", cid)
        require(divisor * quotient + remainder == dividend, "DIVISION_IDENTITY_INVALID", "D×Q+R must equal dividend", cid)
        require(0 <= remainder < divisor, "DIVISION_REMAINDER_NOT_LESS_THAN_DIVISOR", "remainder must be non-negative and less than divisor", cid)
        digits = math.get("quotient_digits")
        expected_digits = [int(ch) for ch in str(quotient)]
        require(digits == expected_digits, "DIVISION_ALGORITHM_INVALID", f"quotient digit sequence must be {expected_digits}", cid)
        require(not (digits and digits[0] == 0), "DIVISION_LEADING_ZERO_INVENTED", "leading quotient zero was invented", cid)
        if oracle.get("internal_zero_required"):
            require(0 in expected_digits[1:-1] or (len(expected_digits) == 2 and expected_digits[-1] == 0), "DIVISION_INTERNAL_ZERO_PLACE_LOST", "benchmark definition expected an internal/trailing positional zero", cid)
            require(math.get("zero_place_preserved") is True, "DIVISION_INTERNAL_ZERO_PLACE_LOST", "candidate did not preserve quotient zero place", cid)
        else:
            require(math.get("zero_place_preserved") in {False, None}, "DIVISION_ZERO_PLACE_FALSE_POSITIVE", "candidate reports a zero-place feature where benchmark does not", cid)
        return

    if kind == "DIAGNOSTIC_CONTRAST":
        diag = evidence.get("diagnosis_evidence") or {}
        require(diag.get("focal_feature") == oracle["focal_feature"], "CONTRAST_SET_WITHOUT_FOCAL_FEATURE", "diagnostic contrast focal feature is missing/wrong", cid)
        require(set(diag.get("positive_cases") or []) == set(oracle["positive_cases"]), "STRUCTURALLY_UNRELATED_CASES_USED_AS_DIAGNOSTIC_CONTRAST", "positive contrast members differ from frozen set", cid)
        require(set(diag.get("negative_cases") or []) == set(oracle["negative_cases"]), "STRUCTURALLY_UNRELATED_CASES_USED_AS_DIAGNOSTIC_CONTRAST", "negative contrast members differ from frozen set", cid)
        hypotheses = diag.get("competing_hypotheses") or []
        require(2 <= len(hypotheses) <= oracle["max_competing_hypotheses"], "UNBOUNDED_COMPETING_HYPOTHESES", "expected 2–3 bounded hypotheses", cid)
        require(not any(h.get("durable_trait") for h in hypotheses), "ERROR_SIGNATURE_PROMOTED_TO_DURABLE_LEARNER_TRAIT", "diagnostic hypothesis cannot be a durable learner trait", cid)
        probe = diag.get("probe") or {}
        require(set(probe.get("hypothesis_ids") or []) <= {h.get("hypothesis_id") for h in hypotheses} and bool(probe.get("hypothesis_ids")), "DIAGNOSTIC_PROBE_WITHOUT_HYPOTHESES", "probe must bind competing hypotheses", cid)
        require(probe.get("manipulated_feature") == oracle["focal_feature"], "DIAGNOSTIC_PROBE_WITHOUT_HYPOTHESES", "probe must manipulate focal feature", cid)
        require(bool(probe.get("outcome_rules")), "DIAGNOSTIC_PROBE_WITHOUT_OUTCOME_RULES", "probe needs predicted outcome rules", cid)
        load = probe.get("controlled_load") or {}
        require(load.get("language") == "LOW" and load.get("representation_novelty") == "LOW" and load.get("fact_retrieval_demand") == "LOW", "DIAGNOSTIC_PROBE_INCREASES_UNRELATED_LOAD", "probe should hold unrelated load low", cid)
        require(diag.get("learner_label") not in {"WEAK_IN_DIVISION", "WEAK_IN_MATH"}, "DIV_QUOTIENT_ZERO_PATTERN_COLLAPSED_TO_WEAK_IN_DIVISION", "narrow evidence was collapsed to a broad learner label", cid)
        return

    if kind == "REMAINDER_CONTEXT":
        q, r = divmod(oracle["dividend"], oracle["divisor"])
        require(q == oracle["quotient"] and r == oracle["remainder"], "DIVISION_IDENTITY_INVALID", "benchmark remainder arithmetic invalid", cid)
        require(math.get("quotient") == q and math.get("remainder") == r, "DIVISION_IDENTITY_INVALID", "candidate remainder arithmetic invalid", cid)
        require(math.get("answer_form") in oracle["allowed_answer_forms"], "REMAINDER_CONTEXT_ANSWER_FORM_INVALID", "unsupported remainder answer form", cid)
        require(math.get("context_rule_explicit") is True, "REMAINDER_CONTEXT_ANSWER_FORM_INVALID", "answer form must be justified by context", cid)
        return

    if kind == "UNIT_CHAIN":
        converted = oracle["quantity"] * oracle["conversion_factor"]
        result = converted * oracle["rate"]
        require(converted == oracle["converted_quantity"] and result == oracle["result"], "UNIT_CONVERSION_FACTOR_MISMATCH", "benchmark unit-chain constants inconsistent", cid)
        require(math.get("source_quantity") == oracle["quantity"] and math.get("conversion_factor") == oracle["conversion_factor"], "UNIT_CHAIN_STEP_DROPPED", "source quantity/conversion missing", cid)
        require(math.get("converted_quantity") == converted and math.get("result") == result, "UNIT_CHAIN_STEP_DROPPED", "unit conversion or rate step dropped", cid)
        require(math.get("source_unit") == oracle["source_unit"] and math.get("target_unit") == oracle["target_unit"], "UNIT_CHAIN_STEP_DROPPED", "unit labels missing/wrong", cid)
        return

    if kind == "FRACTION_EQUIVALENCE":
        expected = [as_fraction(x) for x in oracle["fractions"]]
        require(len(set(expected)) == 1, "FRACTION_EQUIVALENCE_FALSE", "benchmark fractions are not equivalent", cid)
        actual_pairs = math.get("fractions") or []
        require([as_fraction(x) for x in actual_pairs] == expected, "FRACTION_EQUIVALENCE_FALSE", "candidate fraction values differ", cid)
        require(math.get("equal_partitions") is True, "FRACTION_PARTITIONS_NOT_EQUAL", "candidate did not establish equal partitions", cid)
        return

    if kind == "FRACTION_ADDITION":
        expected = as_fraction(oracle["left"]) + as_fraction(oracle["right"])
        require(expected == as_fraction(oracle["result"]), "FRACTION_ADDITION_INVALID", "benchmark fraction addition is inconsistent", cid)
        require(as_fraction(math.get("left")) + as_fraction(math.get("right")) == as_fraction(math.get("result")) == expected, "FRACTION_ADDITION_INVALID", "candidate fraction addition is invalid", cid)
        require(math.get("repartition_or_equivalence_explicit") is True, "FRACTION_ADDITION_REPARTITION_MISSING", "unlike denominators require an explicit valid bridge in this case", cid)
        return

    if kind == "PLACE_VALUE":
        digits = oracle["digits"]
        reconstructed = digits["THOUSANDS"] * 1000 + digits["HUNDREDS"] * 100 + digits["TENS"] * 10 + digits["ONES"]
        require(reconstructed == oracle["number"], "PLACE_VALUE_POSITION_MISMATCH", "benchmark place-value decomposition invalid", cid)
        require(math.get("number") == oracle["number"] and math.get("digits") == digits, "PLACE_VALUE_POSITION_MISMATCH", "candidate digit positions are invalid", cid)
        require(sum(math.get("expanded") or []) == oracle["number"], "PLACE_VALUE_POSITION_MISMATCH", "expanded form does not reconstruct number", cid)
        return

    if kind == "DECIMAL_HUNDREDTHS":
        hundredths = int(round(float(oracle["decimal"]) * 100))
        require(hundredths == oracle["hundredths"], "DECIMAL_HUNDRED_GRID_COUNT_MISMATCH", "benchmark decimal/grid mismatch", cid)
        require(math.get("decimal") == oracle["decimal"] and math.get("shaded_hundredths") == hundredths, "DECIMAL_HUNDRED_GRID_COUNT_MISMATCH", "candidate decimal/grid mismatch", cid)
        return

    if kind == "UNIT_CONVERSION":
        result = oracle["value"] * oracle["factor"]
        require(result == oracle["result"], "UNIT_CONVERSION_FACTOR_MISMATCH", "benchmark conversion mismatch", cid)
        require(math.get("value") == oracle["value"] and math.get("factor") == oracle["factor"] and math.get("result") == result, "UNIT_CONVERSION_FACTOR_MISMATCH", "candidate conversion mismatch", cid)
        require(math.get("source_unit") == oracle["source_unit"] and math.get("target_unit") == oracle["target_unit"], "UNIT_CONVERSION_FACTOR_MISMATCH", "candidate units mismatch", cid)
        return

    if kind == "PERIMETER_AREA_CONTRAST":
        p = 2 * (oracle["length"] + oracle["width"])
        a = oracle["length"] * oracle["width"]
        require(p == oracle["perimeter"] and a == oracle["area"], "PERIMETER_AND_AREA_CONFLATED", "benchmark perimeter/area values invalid", cid)
        require(math.get("perimeter") == p and math.get("area") == a, "PERIMETER_AND_AREA_CONFLATED", "candidate perimeter/area values invalid", cid)
        require(math.get("perimeter_semantics") == "BOUNDARY" and math.get("area_semantics") == "COVERING", "PERIMETER_AND_AREA_CONFLATED", "boundary vs covering distinction lost", cid)
        return

    if kind == "VOLUME":
        volume = oracle["length"] * oracle["width"] * oracle["height"]
        require(volume == oracle["volume"], "VOLUME_LAYER_COUNT_MISMATCH", "benchmark volume invalid", cid)
        require(math.get("volume") == volume and math.get("cube_count") == volume, "VOLUME_LAYER_COUNT_MISMATCH", "candidate cube/layer count mismatch", cid)
        return

    if kind == "ANGLE":
        require(math.get("declared_degrees") == oracle["degrees"] and math.get("represented_degrees") == oracle["degrees"], "ANGLE_SEMANTIC_MISMATCH", "candidate angle representation disagrees", cid)
        return

    if kind == "BAR_CHART":
        require(math.get("scale") == oracle["scale"], "CHART_SCALE_DATA_MISMATCH", "chart scale differs", cid)
        require(math.get("data") == oracle["data"] and math.get("rendered_values") == oracle["data"], "CHART_SCALE_DATA_MISMATCH", "chart data/render mismatch", cid)
        return

    if kind == "WORK_PROVENANCE":
        work = evidence.get("work_evidence") or {}
        steps = work.get("steps") or []
        require(work.get("final_correctness") == "INCORRECT", "WORK_PROVENANCE_FIXTURE_INVALID", "mixed-success case expects incorrect final answer", cid)
        require(any(s.get("status") == "CORRECT" for s in steps), "INCORRECT_FINAL_ANSWER_ERASES_CORRECT_SUBSTEPS", "correct intermediate work was not preserved", cid)
        require(any(s.get("status") == "AMBIGUOUS" for s in steps), "AMBIGUOUS_HANDWRITING_SILENTLY_RESOLVED", "ambiguous work was silently resolved", cid)
        require(bool(work.get("teacher_annotations")) and all(a.get("actor") == "TEACHER" for a in work.get("teacher_annotations", [])), "TEACHER_CORRECTION_RENDERED_AS_CHILD_ORIGINAL", "teacher annotations are not separate", cid)
        require(work.get("replay_provenance") in {"FAITHFUL_TRANSCRIPTION", "STRUCTURED_REPLAY"}, "WORK_REPLAY_PROVENANCE_MISSING", "replay must not imply original handwriting", cid)
        return

    if kind == "HINT_LADDER":
        hint = evidence.get("hint_evidence") or {}
        require(hint.get("sequence") == oracle["sequence"], "H3_WITHOUT_FRESH_INDEPENDENT_RETRY", "hint sequence must end in fresh H0", cid)
        require(hint.get("supported_success_is_independent") is False, "SUPPORTED_SUCCESS_COUNTED_AS_INDEPENDENT_USE", "supported success cannot be independent evidence", cid)
        require(hint.get("fresh_retry_item_id") and hint.get("supported_item_id") and hint.get("fresh_retry_item_id") != hint.get("supported_item_id"), "H3_WITHOUT_FRESH_INDEPENDENT_RETRY", "fresh retry must be a new item", cid)
        return

    if kind == "ROUTE_CHANGE":
        runtime = evidence.get("runtime_evidence") or {}
        failures = runtime.get("same_route_failures")
        require(isinstance(failures, int) and failures >= oracle["same_route_failures_before_change"], "ROUTE_CHANGE_FIXTURE_INVALID", "route-change case needs repeated same-route failures", cid)
        require(runtime.get("route_changed") is True and bool(runtime.get("changed_dimension")), "SAME_ROUTE_REPEATED_AFTER_TWO_FAILURES", "meaningful route change missing", cid)
        require(runtime.get("conceptual_support") != runtime.get("access_adjustment"), "CONCEPTUAL_SUPPORT_CONFLATED_WITH_ACCESS_ADJUSTMENT", "conceptual and access support must remain separate", cid)
        require(runtime.get("independent_retry_after_repair") is True, "TEACHER_MOVE_WITHOUT_INDEPENDENT_RETRY", "repair must be followed by independent retry", cid)
        return

    raise AcceptanceFailure("UNKNOWN_ORACLE_KIND", f"unsupported oracle kind {kind}", cid)


def check_artifact_evidence(candidate: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    artifacts = candidate.get("artifacts") or {}
    for key in ("core1_sha256", "core2_sha256", "physical_page_map_digest"):
        value = artifacts.get(key)
        if not isinstance(value, str) or len(value) < 32:
            reasons.append(f"missing/invalid {key}")
    for case in candidate.get("cases") or []:
        surface = case.get("surface_evidence") or {}
        custody = case.get("custody_evidence") or {}
        if surface.get("internal_identifier_leaks") not in ([], None):
            reasons.append(f"{case.get('case_id')}: learner-surface identifier leak")
        if not custody.get("placement_evidence_id"):
            reasons.append(f"{case.get('case_id')}: missing placement evidence")
    return (not reasons, reasons)


def evaluate(candidate: dict[str, Any]) -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    specs = {c["case_id"]: c for c in registry["cases"]}
    evidence_list = candidate.get("cases") or []
    evidence_by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids: list[str] = []
    for item in evidence_list:
        cid = item.get("case_id")
        if cid in evidence_by_id:
            duplicate_ids.append(cid)
        evidence_by_id[cid] = item

    failures: list[dict[str, Any]] = []
    if duplicate_ids:
        failures.append({"case_id": None, "falsifier": "DUPLICATE_CASE_EVIDENCE", "message": f"duplicate case ids: {duplicate_ids}"})

    missing_cases = sorted(set(specs) - set(evidence_by_id))
    if missing_cases:
        failures.append({"case_id": None, "falsifier": "BENCHMARK_CASE_COVERAGE_INCOMPLETE", "message": f"missing cases: {missing_cases}"})

    for cid, spec in specs.items():
        evidence = evidence_by_id.get(cid)
        if evidence is None:
            continue
        try:
            check_scope(spec, evidence)
            check_representations(spec, evidence)
            check_product_links(spec, evidence)
            check_oracle(spec, evidence)
        except AcceptanceFailure as exc:
            failures.append({"case_id": exc.case_id, "falsifier": exc.falsifier, "message": exc.message})

    semantic_pass = not failures
    artifact_pass, artifact_reasons = check_artifact_evidence(candidate) if semantic_pass else (False, ["semantic acceptance failed"])

    canonical = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = sha256(canonical).hexdigest()

    if not semantic_pass:
        classification = "BENCHMARK_FAIL"
    elif artifact_pass:
        classification = "BENCHMARK_ENGINEERING_PASS_PENDING_HUMAN_REVIEW"
    else:
        classification = "BENCHMARK_SEMANTIC_PASS_ARTIFACT_EVIDENCE_BLOCKED"

    return {
        "benchmark_version": registry["version"],
        "candidate_id": candidate.get("candidate_id"),
        "candidate_export_sha256": digest,
        "semantic_status": "PASS" if semantic_pass else "FAIL",
        "artifact_status": "PASS" if artifact_pass else "BLOCKED",
        "human_review_status": "PENDING_HUMAN_REVIEW",
        "classification": classification,
        "failures": failures,
        "artifact_blockers": artifact_reasons,
        "producer_pass_claims_trusted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--semantic-only", action="store_true", help="return 0 when semantic oracle passes even if rendered-artifact evidence is absent")
    args = parser.parse_args()

    candidate = load_json(args.candidate)
    report = evaluate(candidate)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)

    if report["semantic_status"] != "PASS":
        return 1
    if args.semantic_only:
        return 0
    if report["artifact_status"] != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
