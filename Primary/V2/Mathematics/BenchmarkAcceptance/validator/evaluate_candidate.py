"""
Independent Benchmark Acceptance Evaluator for Primary Mathematics V2.
Evaluates candidate export against frozen benchmark specifications and falsifiers.
Does not import candidate renderer, page composer, or ReportLab.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple


class BenchmarkEvaluator:
    def __init__(self, benchmark_dir: Path | None = None) -> None:
        if benchmark_dir is None:
            benchmark_dir = Path(__file__).resolve().parent.parent
        self.benchmark_dir = benchmark_dir
        self.falsifiers_path = benchmark_dir / "registry" / "falsifier_catalog.json"
        self.cases_path = benchmark_dir / "registry" / "benchmark_cases.json"
        self.schema_path = benchmark_dir / "contracts" / "candidate_export.schema.json"

        with open(self.falsifiers_path, "r", encoding="utf-8") as f:
            self.falsifier_catalog = json.load(f)["falsifiers"]
            self.falsifier_codes = {item["code"]: item for item in self.falsifier_catalog}

        with open(self.cases_path, "r", encoding="utf-8") as f:
            self.benchmark_cases = {c["case_id"]: c for c in json.load(f)["cases"]}

    def evaluate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a candidate export payload."""
        results: Dict[str, Any] = {
            "candidate_id": candidate_data.get("candidate_id", "UNKNOWN"),
            "machine_gates": {
                "CORPUS_INTEGRITY": "PASS",
                "SEMANTIC_CONSISTENCY": "PASS",
                "SCOPE_PROVENANCE_CONSISTENCY": "PASS",
                "REPRESENTATION_EVIDENCE_PRESENT": "PASS",
                "WORK_PROVENANCE_CONSISTENCY": "PASS",
                "CORE1_CORE2_LINKAGE": "PASS",
                "HINT_RETRY_CONTRACT": "PASS",
                "LEARNER_SURFACE_GUARD": "PASS",
                "ARTIFACT_CUSTODY": "PASS"
            },
            "human_review_status": {
                "SUBJECT_CORRECTNESS_HUMAN_REVIEW": "PENDING_HUMAN_REVIEW",
                "PEDAGOGICAL_DESIGN_HUMAN_REVIEW": "PENDING_HUMAN_REVIEW",
                "ASSESSMENT_DESIGN_HUMAN_REVIEW": "PENDING_HUMAN_REVIEW",
                "VISUAL_USABILITY_HUMAN_REVIEW": "PENDING_HUMAN_REVIEW",
                "CHILD_USABILITY_HUMAN_REVIEW": "PENDING_HUMAN_REVIEW",
                "MATURE_DESIGN_QUALITY_HUMAN_REVIEW": "PENDING_HUMAN_REVIEW"
            },
            "total_cases_evaluated": 0,
            "passed_cases": 0,
            "failed_cases": 0,
            "triggered_falsifiers": [],
            "case_evaluations": {}
        }

        cases = candidate_data.get("cases", [])
        results["total_cases_evaluated"] = len(cases)

        for case in cases:
            case_id = case.get("case_id")
            case_falsifiers = self._evaluate_case(case)
            case_passed = len(case_falsifiers) == 0

            if case_passed:
                results["passed_cases"] += 1
            else:
                results["failed_cases"] += 1
                for f_code in case_falsifiers:
                    if f_code not in results["triggered_falsifiers"]:
                        results["triggered_falsifiers"].append(f_code)

            results["case_evaluations"][case_id] = {
                "pass": case_passed,
                "falsifiers": case_falsifiers
            }

        # Update machine gates based on triggered falsifiers
        if any(f in results["triggered_falsifiers"] for f in [
            "QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE",
            "RAW_QUESTIONS_RENDERED_DIRECTLY_WITHOUT_SKILL_MODEL"
        ]):
            results["machine_gates"]["SCOPE_PROVENANCE_CONSISTENCY"] = "FAIL"

        if any(f in results["triggered_falsifiers"] for f in [
            "MULTIPLICATION_AREA_MODEL_MISLABEL",
            "MULTIPLICATION_PARTIAL_PRODUCTS_OMISSION",
            "MULTIPLICATION_PRODUCT_SUM_MISMATCH",
            "DIVISION_SHARING_GROUPING_COLLAPSE",
            "DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED",
            "DIVISION_CHECK_EQUATION_VIOLATED",
            "DIVISION_REMAINDER_EXCEEDS_DIVISOR",
            "DIVISION_REMAINDER_CONTEXT_UNHANDLED",
            "QUANTITY_UNIT_CHAIN_COLLAPSED",
            "FRACTION_COMPARISON_UNGROUNDED",
            "FRACTION_ADDITION_DENOMINATOR_SUMMED",
            "PLACE_VALUE_DECOMPOSITION_POSITION_ERROR",
            "MEASUREMENT_UNIT_CONVERSION_FACTOR_INVALID",
            "PERIMETER_AREA_CONFLATED",
            "VOLUME_CUBE_COUNT_MISMATCH",
            "GEOMETRY_ANGLE_INCONSISTENCY",
            "DATA_CHART_SCALE_MISMATCH",
            "WORD_PROBLEM_QUANTITY_STRUCTURE_MISSING"
        ]):
            results["machine_gates"]["SEMANTIC_CONSISTENCY"] = "FAIL"

        if any(f in results["triggered_falsifiers"] for f in [
            "RENDERED_EVIDENCE_ARGUMENTS_IGNORED",
            "MULTIPLICATION_ALGORITHM_DISCONNECTED_FROM_PLACE_VALUE",
            "FRACTION_PARTITION_UNEQUAL",
            "FRACTION_SHADING_MISMATCH",
            "DECIMAL_HUNDRED_GRID_MISMATCH",
            "DECIMAL_NUMBER_LINE_MISMATCH"
        ]):
            results["machine_gates"]["REPRESENTATION_EVIDENCE_PRESENT"] = "FAIL"

        if any(f in results["triggered_falsifiers"] for f in [
            "NOTEBOOK_REPLAY_CLAIMED_AS_ORIGINAL_HANDWRITING",
            "NOTEBOOK_PLACE_VALUE_COLUMNS_MISALIGNED",
            "NOTEBOOK_TEACHER_CORRECTION_CONFLATED_WITH_CHILD_WORK",
            "NOTEBOOK_AMBIGUITY_SILENTLY_RESOLVED",
            "NOTEBOOK_CORRECT_INTERMEDIATE_WORK_ERASED",
            "ERROR_ANALYSIS_SILENT_NORMALIZATION"
        ]):
            results["machine_gates"]["WORK_PROVENANCE_CONSISTENCY"] = "FAIL"

        if any(f in results["triggered_falsifiers"] for f in [
            "CORE1_REPRESENTATION_BRIDGE_MISSING",
            "CORE1_PEDAGOGICAL_SEQUENCE_INCOMPLETE",
            "CORE2_PRACTICE_ROLE_UNDECLARED",
            "CORE2_APPENDIX_C_IS_PROSE_CRAM_SHEET",
            "CORE2_HARDCODED_PAGE_NUMBER_REFERENCE"
        ]):
            results["machine_gates"]["CORE1_CORE2_LINKAGE"] = "FAIL"

        if "CORE2_HINT_LADDER_CONTRACT_VIOLATED" in results["triggered_falsifiers"]:
            results["machine_gates"]["HINT_RETRY_CONTRACT"] = "FAIL"

        if "LEARNER_SURFACE_LEAK_DETECTED" in results["triggered_falsifiers"]:
            results["machine_gates"]["LEARNER_SURFACE_GUARD"] = "FAIL"

        if "CHILD_READABILITY_FONT_SIZE_VIOLATED" in results["triggered_falsifiers"]:
            results["machine_gates"]["ARTIFACT_CUSTODY"] = "FAIL"

        results["overall_machine_pass"] = all(v == "PASS" for v in results["machine_gates"].values())
        return results

    def _evaluate_case(self, case: Dict[str, Any]) -> List[str]:
        falsifiers: List[str] = []
        case_id = case.get("case_id")
        scope = case.get("scope_provenance", {})
        math = case.get("math_invariants", {})
        reps = case.get("representations", [])
        work = case.get("work_provenance", {})
        c1 = case.get("core1_refs", {})
        c2 = case.get("core2_refs", {})
        guard = case.get("learner_surface_guard", {})
        layout = case.get("layout_custody", {})

        # 1. Scope checks
        if scope.get("universal_grade_scope_claimed") and scope.get("scope_basis") in ["QUESTION_SET_OBSERVED", "SCHOOL_CLASSWORK_OBSERVED", "SOURCE_NOT_PROVIDED"]:
            falsifiers.append("QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE")
        if scope.get("scope_basis") == "CURRICULUM_CONFIRMED" and not scope.get("authority_ref"):
            falsifiers.append("QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE")

        # 2. Representations check (PR #310 defect detector)
        if not reps:
            falsifiers.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")
        for r in reps:
            ev = r.get("rendered_evidence", {})
            if not ev.get("data_grounded") or ev.get("element_count", 0) <= 0:
                falsifiers.append("RENDERED_EVIDENCE_ARGUMENTS_IGNORED")

        # 3. Math invariants
        op = math.get("operation")
        operands = math.get("operands", [])
        res = math.get("result")
        rem = math.get("remainder", 0)

        if op == "MULTIPLICATION":
            decomp = math.get("decomposition", [])
            partials = math.get("partial_steps", [])
            # Check 23 x 6 deep case
            if operands == [23, 6]:
                # Check area model partition values
                for d in decomp:
                    expr = d.get("expression", "").replace(" ", "")
                    val = d.get("value")
                    if "20*6" in expr and val != 120:
                        falsifiers.append("MULTIPLICATION_AREA_MODEL_MISLABEL")
                    if "3*6" in expr and val != 18:
                        falsifiers.append("MULTIPLICATION_AREA_MODEL_MISLABEL")
                
                # Check partial product omission
                p_vals = [p.get("partial_value") for p in partials]
                if 18 not in p_vals or 120 not in p_vals or len(partials) < 2:
                    falsifiers.append("MULTIPLICATION_PARTIAL_PRODUCTS_OMISSION")
                
                # Check product sum mismatch
                if p_vals and sum(p_vals) != res:
                    falsifiers.append("MULTIPLICATION_PRODUCT_SUM_MISMATCH")

            # Check general product
            if operands and len(operands) == 2:
                if operands[0] * operands[1] != res:
                    falsifiers.append("MULTIPLICATION_PRODUCT_SUM_MISMATCH")

        elif op == "DIVISION":
            if operands and len(operands) == 2:
                dend, dsor = operands[0], operands[1]
                if dsor > 0:
                    if dsor * res + rem != dend:
                        falsifiers.append("DIVISION_CHECK_EQUATION_VIOLATED")
                    if rem < 0 or rem >= dsor:
                        falsifiers.append("DIVISION_REMAINDER_EXCEEDS_DIVISOR")

                    # Check internal quotient zero for 366/12 and 7843/13
                    if dend == 366 and dsor == 12 and res != 30:
                        falsifiers.append("DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED")
                    if dend == 7843 and dsor == 13 and res != 603:
                        falsifiers.append("DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED")

            # Check sharing vs grouping distinction
            qs = math.get("quantity_structure", {})
            if case_id == "BENCH-DEEP-DIV-01" and qs.get("meaning") not in ["SHARING", "GROUPING"]:
                falsifiers.append("DIVISION_SHARING_GROUPING_COLLAPSE")

            # Check remainder interpretation
            if case_id == "BENCH-DEEP-DIV-05":
                scenarios = math.get("context_scenarios", [])
                for s in scenarios:
                    if s.get("context") == "BUS_CAPACITY" and s.get("action") != "ROUND_UP_ONE_MORE_GROUP":
                        falsifiers.append("DIVISION_REMAINDER_CONTEXT_UNHANDLED")

        elif op == "UNIT_CONVERSION":
            steps = math.get("unit_steps", [])
            for s in steps:
                if s.get("unit") == "DOZEN_EGGS" and s.get("multiplier") != 12:
                    falsifiers.append("QUANTITY_UNIT_CHAIN_COLLAPSED")

        elif op == "FRACTION_OPERATION":
            if math.get("added_denominators"):
                falsifiers.append("FRACTION_ADDITION_DENOMINATOR_SUMMED")
            if math.get("ungrounded_comparison"):
                falsifiers.append("FRACTION_COMPARISON_UNGROUNDED")

        # 4. Work Provenance & Alignment
        if work:
            tier = work.get("tier")
            if tier == "STRUCTURED_REPLAY" and work.get("actor") == "CHILD" and work.get("claims_original_handwriting"):
                falsifiers.append("NOTEBOOK_REPLAY_CLAIMED_AS_ORIGINAL_HANDWRITING")
            
            invariants = work.get("alignment_invariants", {})
            if invariants.get("place_value_aligned") is False:
                falsifiers.append("NOTEBOOK_PLACE_VALUE_COLUMNS_MISALIGNED")
            if invariants.get("intermediate_work_preserved") is False:
                falsifiers.append("NOTEBOOK_CORRECT_INTERMEDIATE_WORK_ERASED")

            annotations = work.get("teacher_annotations", [])
            for ann in annotations:
                if ann.get("attributed_to_child"):
                    falsifiers.append("NOTEBOOK_TEACHER_CORRECTION_CONFLATED_WITH_CHILD_WORK")

            if work.get("has_ambiguity") and work.get("ambiguity_silently_resolved"):
                falsifiers.append("NOTEBOOK_AMBIGUITY_SILENTLY_RESOLVED")

        # 5. Core 1 / Core 2 contracts
        if c1:
            seq = c1.get("pedagogical_sequence", [])
            required_seq_steps = ["NOTICE", "MODEL", "WORKED", "SUPPORTED", "INDEPENDENT"]
            if not all(any(req.lower() in s.lower() for s in seq) for req in required_seq_steps):
                falsifiers.append("CORE1_PEDAGOGICAL_SEQUENCE_INCOMPLETE")
            if not c1.get("representation_bridge") and not c1.get("dominant_representation"):
                falsifiers.append("CORE1_REPRESENTATION_BRIDGE_MISSING")

        if c2:
            batches = c2.get("appendix_a_batches", [])
            for b in batches:
                if not b.get("practice_role"):
                    falsifiers.append("CORE2_PRACTICE_ROLE_UNDECLARED")

            ladder = c2.get("appendix_b_ladder", {})
            if not (ladder.get("H1_notice") and ladder.get("H2_remember") and ladder.get("H3_represent") and ladder.get("fresh_independent_retry_H0")):
                falsifiers.append("CORE2_HINT_LADDER_CONTRACT_VIOLATED")

            app_c = c2.get("appendix_c_ref", {})
            if app_c.get("is_prose_cram_sheet"):
                falsifiers.append("CORE2_APPENDIX_C_IS_PROSE_CRAM_SHEET")

            if c2.get("references_physical_page_number"):
                falsifiers.append("CORE2_HARDCODED_PAGE_NUMBER_REFERENCE")

        # 6. Learner surface guard
        if guard:
            if not guard.get("pass") or len(guard.get("detected_internal_tokens", [])) > 0:
                falsifiers.append("LEARNER_SURFACE_LEAK_DETECTED")

        # 7. Layout custody & readability
        if layout:
            geom = layout.get("child_first_geometry", {})
            if geom.get("min_body_font_pt", 14.0) < 12.0:
                falsifiers.append("CHILD_READABILITY_FONT_SIZE_VIOLATED")

        return list(dict.fromkeys(falsifiers))


def run_evaluation_cli() -> None:
    if len(sys.argv) < 2:
        print("Usage: python evaluate_candidate.py <candidate_export.json> [output_report.json]")
        sys.exit(1)

    candidate_file = Path(sys.argv[1])
    with open(candidate_file, "r", encoding="utf-8") as f:
        candidate_data = json.load(f)

    evaluator = BenchmarkEvaluator()
    report = evaluator.evaluate(candidate_data)

    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else candidate_file.parent / "acceptance_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Evaluation complete. Pass: {report['overall_machine_pass']}. Triggered falsifiers: {len(report['triggered_falsifiers'])}")
    if not report['overall_machine_pass']:
        print(f"Triggered: {report['triggered_falsifiers']}")
        sys.exit(2)


if __name__ == "__main__":
    run_evaluation_cli()
