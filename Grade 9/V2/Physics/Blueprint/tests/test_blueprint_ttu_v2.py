#!/usr/bin/env python3
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from validate_technical_teaching_unit import validate_ttu_v2_semantics

GOLDEN = json.loads((ROOT / "fixtures" / "technical-ttu-v2" / "m2d-moving-launcher-frame-conversion.json").read_text())


def expect_failure(obj, code):
    try:
        validate_ttu_v2_semantics(obj)
    except AssertionError as exc:
        assert str(exc) == code
        return
    raise AssertionError("EXPECTED_TTU2_FAILURE_NOT_RAISED:" + code)


def test_golden_passes():
    validate_ttu_v2_semantics(deepcopy(GOLDEN))


def test_unknown_omission_fails():
    x = deepcopy(GOLDEN)
    x["reconstruction_contract"]["omissions"][0]["element_id"] = "E-NOT-CANONICAL"
    expect_failure(x, "TTU2_OMISSION_NOT_IN_CANONICAL_STATE")


def test_help_not_bound_to_omission_fails():
    x = deepcopy(GOLDEN)
    x["reconstruction_contract"]["fixed_help"]["steps"][0]["addresses_element_ids"] = ["E-COMP-Y"]
    expect_failure(x, "TTU2_HELP_NOT_BOUND_TO_OMISSION")


def test_hard_substantive_single_omission_fails():
    x = deepcopy(GOLDEN)
    x["reconstruction_contract"]["omissions"] = x["reconstruction_contract"]["omissions"][:1]
    # keep only help that points to that single omission, so the failure is specifically omission depth
    x["reconstruction_contract"]["fixed_help"]["steps"] = [
        {
            "help_id": "H1",
            "function": "NOTICE",
            "text": "Which vector is the ground-frame resultant?",
            "addresses_element_ids": ["E-RESULT-BG"]
        },
        {
            "help_id": "H2",
            "function": "REPRESENT",
            "text": "Draw the resultant from the original tail to the final head.",
            "addresses_element_ids": ["E-RESULT-BG"]
        },
        {
            "help_id": "H3",
            "function": "START",
            "text": "Write v_BG = v_BT + v_TG.",
            "addresses_element_ids": ["E-RESULT-BG"]
        }
    ]
    expect_failure(x, "TTU2_HARD_SUBSTANTIVE_NEEDS_TWO_MEANINGFUL_OMISSIONS")


def test_incomplete_help_function_set_fails():
    x = deepcopy(GOLDEN)
    x["reconstruction_contract"]["fixed_help"]["steps"][2]["function"] = "NOTICE"
    expect_failure(x, "TTU2_HARD_SUBSTANTIVE_HELP_FUNCTION_DRIFT")


def test_b_layer_without_reconstruction_fails():
    x = deepcopy(GOLDEN)
    b = next(r for r in x["layer_realizations"] if r["layer"] == "CORE1B")
    b["uses_reconstruction_contract"] = False
    expect_failure(x, "TTU2_B_LAYER_WITHOUT_RECONSTRUCTION")


if __name__ == "__main__":
    test_golden_passes()
    test_unknown_omission_fails()
    test_help_not_bound_to_omission_fails()
    test_hard_substantive_single_omission_fails()
    test_incomplete_help_function_set_fails()
    test_b_layer_without_reconstruction_fails()
    print("Physics TTU v2 falsifiers: PASS")
