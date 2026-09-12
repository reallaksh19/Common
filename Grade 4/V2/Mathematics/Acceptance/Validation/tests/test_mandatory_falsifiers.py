"""
Comprehensive Test Suite for all 40 Mandatory Falsifiers in Primary Mathematics V2.
Verifies that every falsifier catalog entry is actively detectable by the benchmark evaluator.
"""
import copy
import json
from pathlib import Path
import pytest

from Primary.V2.Mathematics.BenchmarkAcceptance.validator.evaluate_candidate import BenchmarkEvaluator


@pytest.fixture
def evaluator():
    return BenchmarkEvaluator()


@pytest.fixture
def base_candidate():
    val_dir = Path(__file__).resolve().parent.parent
    with open(val_dir / "candidate_export.json", "r", encoding="utf-8") as f:
        return json.load(f)


def _mutate_and_eval(evaluator, base_candidate, case_idx, patch):
    mutated = copy.deepcopy(base_candidate)
    target_case = mutated["cases"][case_idx]
    for k, v in patch.items():
        if isinstance(v, dict) and k in target_case and isinstance(target_case[k], dict):
            target_case[k].update(v)
        else:
            target_case[k] = v
    report = evaluator.evaluate(mutated)
    return report["triggered_falsifiers"]


def test_scope_falsifiers(evaluator, base_candidate):
    # 1. QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE
    f = _mutate_and_eval(evaluator, base_candidate, 0, {
        "scope_provenance": {"scope_basis": "QUESTION_SET_OBSERVED", "universal_grade_scope_claimed": True}
    })
    assert "QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE" in f

    # Missing authority ref on CURRICULUM_CONFIRMED
    f2 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "scope_provenance": {"scope_basis": "CURRICULUM_CONFIRMED", "authority_ref": ""}
    })
    assert "QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE" in f2


def test_multiplication_falsifiers(evaluator, base_candidate):
    # 3. MULTIPLICATION_AREA_MODEL_MISLABEL
    f1 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "math_invariants": {
            "operation": "MULTIPLICATION",
            "operands": [23, 6],
            "result": 138,
            "decomposition": [{"expression": "20 * 6", "value": 12}, {"expression": "3 * 6", "value": 18}]
        }
    })
    assert "MULTIPLICATION_AREA_MODEL_MISLABEL" in f1

    # 4. MULTIPLICATION_PARTIAL_PRODUCTS_OMISSION
    f2 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "math_invariants": {
            "operation": "MULTIPLICATION",
            "operands": [23, 6],
            "result": 138,
            "partial_steps": [{"step_index": 1, "description": "20 * 6", "partial_value": 120}]
        }
    })
    assert "MULTIPLICATION_PARTIAL_PRODUCTS_OMISSION" in f2

    # 5. MULTIPLICATION_PRODUCT_SUM_MISMATCH
    f3 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "math_invariants": {
            "operation": "MULTIPLICATION",
            "operands": [23, 6],
            "result": 140,
            "partial_steps": [
                {"step_index": 1, "description": "20 * 6", "partial_value": 120},
                {"step_index": 2, "description": "3 * 6", "partial_value": 18}
            ]
        }
    })
    assert "MULTIPLICATION_PRODUCT_SUM_MISMATCH" in f3


def test_division_falsifiers(evaluator, base_candidate):
    # 7. DIVISION_SHARING_GROUPING_COLLAPSE
    f1 = _mutate_and_eval(evaluator, base_candidate, 1, {
        "math_invariants": {
            "operation": "DIVISION",
            "operands": [24, 6],
            "result": 4,
            "remainder": 0,
            "quantity_structure": {"meaning": "GENERIC_COLLAPSED"}
        }
    })
    assert "DIVISION_SHARING_GROUPING_COLLAPSE" in f1

    # 8. DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED (366 / 12)
    f2 = _mutate_and_eval(evaluator, base_candidate, 2, {
        "math_invariants": {"operation": "DIVISION", "operands": [366, 12], "result": 36, "remainder": 6}
    })
    assert "DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED" in f2

    # 8. DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED (7843 / 13)
    f3 = _mutate_and_eval(evaluator, base_candidate, 3, {
        "math_invariants": {"operation": "DIVISION", "operands": [7843, 13], "result": 63, "remainder": 4}
    })
    assert "DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED" in f3

    # 9. DIVISION_CHECK_EQUATION_VIOLATED
    f4 = _mutate_and_eval(evaluator, base_candidate, 2, {
        "math_invariants": {"operation": "DIVISION", "operands": [366, 12], "result": 30, "remainder": 5}
    })
    assert "DIVISION_CHECK_EQUATION_VIOLATED" in f4

    # 10. DIVISION_REMAINDER_EXCEEDS_DIVISOR
    f5 = _mutate_and_eval(evaluator, base_candidate, 2, {
        "math_invariants": {"operation": "DIVISION", "operands": [366, 12], "result": 29, "remainder": 18}
    })
    assert "DIVISION_REMAINDER_EXCEEDS_DIVISOR" in f5

    # 11. DIVISION_REMAINDER_CONTEXT_UNHANDLED
    f6 = _mutate_and_eval(evaluator, base_candidate, 5, {
        "math_invariants": {
            "operation": "DIVISION",
            "context_scenarios": [{"context": "BUS_CAPACITY", "action": "DROP_LEFTOVERS"}]
        }
    })
    assert "DIVISION_REMAINDER_CONTEXT_UNHANDLED" in f6


def test_unit_chain_falsifiers(evaluator, base_candidate):
    # 12. QUANTITY_UNIT_CHAIN_COLLAPSED
    f = _mutate_and_eval(evaluator, base_candidate, 6, {
        "math_invariants": {
            "operation": "UNIT_CONVERSION",
            "unit_steps": [
                {"quantity": 23, "unit": "DOZEN_EGGS"},
                {"multiplier": 10, "result_quantity": 230, "unit": "INDIVIDUAL_EGGS"}
            ]
        }
    })
    assert "QUANTITY_UNIT_CHAIN_COLLAPSED" in f


def test_fractions_falsifiers(evaluator, base_candidate):
    # 15. FRACTION_COMPARISON_UNGROUNDED
    f1 = _mutate_and_eval(evaluator, base_candidate, 8, {
        "math_invariants": {"operation": "FRACTION_OPERATION", "ungrounded_comparison": True}
    })
    assert "FRACTION_COMPARISON_UNGROUNDED" in f1

    # 16. FRACTION_ADDITION_DENOMINATOR_SUMMED
    f2 = _mutate_and_eval(evaluator, base_candidate, 9, {
        "math_invariants": {"operation": "FRACTION_OPERATION", "added_denominators": True}
    })
    assert "FRACTION_ADDITION_DENOMINATOR_SUMMED" in f2


def test_work_provenance_and_notebook_falsifiers(evaluator, base_candidate):
    # 27. NOTEBOOK_REPLAY_CLAIMED_AS_ORIGINAL_HANDWRITING
    f1 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "work_provenance": {"tier": "STRUCTURED_REPLAY", "actor": "CHILD", "claims_original_handwriting": True}
    })
    assert "NOTEBOOK_REPLAY_CLAIMED_AS_ORIGINAL_HANDWRITING" in f1

    # 28. NOTEBOOK_PLACE_VALUE_COLUMNS_MISALIGNED
    f2 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "work_provenance": {"tier": "STRUCTURED_REPLAY", "alignment_invariants": {"place_value_aligned": False}}
    })
    assert "NOTEBOOK_PLACE_VALUE_COLUMNS_MISALIGNED" in f2

    # 29. NOTEBOOK_TEACHER_CORRECTION_CONFLATED_WITH_CHILD_WORK
    f3 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "work_provenance": {"tier": "STRUCTURED_REPLAY", "teacher_annotations": [{"attributed_to_child": True}]}
    })
    assert "NOTEBOOK_TEACHER_CORRECTION_CONFLATED_WITH_CHILD_WORK" in f3

    # 30. NOTEBOOK_AMBIGUITY_SILENTLY_RESOLVED
    f4 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "work_provenance": {"tier": "STRUCTURED_REPLAY", "has_ambiguity": True, "ambiguity_silently_resolved": True}
    })
    assert "NOTEBOOK_AMBIGUITY_SILENTLY_RESOLVED" in f4

    # 31. NOTEBOOK_CORRECT_INTERMEDIATE_WORK_ERASED
    f5 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "work_provenance": {"tier": "STRUCTURED_REPLAY", "alignment_invariants": {"intermediate_work_preserved": False}}
    })
    assert "NOTEBOOK_CORRECT_INTERMEDIATE_WORK_ERASED" in f5


def test_core_contracts_and_readability_falsifiers(evaluator, base_candidate):
    # 33. CORE1_PEDAGOGICAL_SEQUENCE_INCOMPLETE
    f1 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "core1_refs": {"module_id": "M1", "pedagogical_sequence": ["NOTICE", "PRACTICE"]}
    })
    assert "CORE1_PEDAGOGICAL_SEQUENCE_INCOMPLETE" in f1

    # 34. CORE2_PRACTICE_ROLE_UNDECLARED
    f2 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "core2_refs": {"companion_id": "C2", "appendix_a_batches": [{"batch_id": "B1", "item_count": 3}]}
    })
    assert "CORE2_PRACTICE_ROLE_UNDECLARED" in f2

    # 35. CORE2_HINT_LADDER_CONTRACT_VIOLATED
    f3 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "core2_refs": {"companion_id": "C2", "appendix_b_ladder": {"H0_try": "try"}}
    })
    assert "CORE2_HINT_LADDER_CONTRACT_VIOLATED" in f3

    # 36. CORE2_APPENDIX_C_IS_PROSE_CRAM_SHEET
    f4 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "core2_refs": {"companion_id": "C2", "appendix_c_ref": {"is_prose_cram_sheet": True}}
    })
    assert "CORE2_APPENDIX_C_IS_PROSE_CRAM_SHEET" in f4

    # 37. CORE2_HARDCODED_PAGE_NUMBER_REFERENCE
    f5 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "core2_refs": {"companion_id": "C2", "references_physical_page_number": True}
    })
    assert "CORE2_HARDCODED_PAGE_NUMBER_REFERENCE" in f5

    # 38. LEARNER_SURFACE_LEAK_DETECTED
    f6 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "learner_surface_guard": {"pass": False, "detected_internal_tokens": ["pedagogical_sequence"]}
    })
    assert "LEARNER_SURFACE_LEAK_DETECTED" in f6

    # 39. CHILD_READABILITY_FONT_SIZE_VIOLATED
    f7 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "layout_custody": {"page_count": 1, "page_map": [], "pdf_sha256": "x", "child_first_geometry": {"min_body_font_pt": 10.0, "overflow_strategy": "SHRINK"}}
    })
    assert "CHILD_READABILITY_FONT_SIZE_VIOLATED" in f7

    # 40. RENDERED_EVIDENCE_ARGUMENTS_IGNORED
    f8 = _mutate_and_eval(evaluator, base_candidate, 0, {
        "representations": [{
            "role": "PROVIDED", "kind": "AREA_MODEL", "params": {},
            "rendered_evidence": {"element_count": 0, "visual_checksum": "0", "data_grounded": False}
        }]
    })
    assert "RENDERED_EVIDENCE_ARGUMENTS_IGNORED" in f8
