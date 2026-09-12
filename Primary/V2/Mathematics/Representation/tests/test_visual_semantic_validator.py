"""
Unit tests for Representation VisualSemanticValidator.
"""
import pytest
from Primary.V2.Mathematics.Representation.engine.validator import VisualSemanticValidator


@pytest.fixture
def validator():
    return VisualSemanticValidator()


def test_multiplication_area_mislabel_detected(validator):
    params = {
        "factors": [23, 6],
        "product": 138,
        "partitions": [
            {"length": 20, "height": 6, "area": 12},  # Error: 20*6=120, not 12
            {"length": 3, "height": 6, "area": 18}
        ]
    }
    errors = validator.validate_primitive("AREA_MODEL", params)
    assert "MULTIPLICATION_AREA_MODEL_MISLABEL" in errors


def test_division_internal_zero_dropped_detected(validator):
    params = {
        "dividend": 7843,
        "divisor": 13,
        "quotient": 63,  # Error: should be 603
        "remainder": 4
    }
    errors = validator.validate_primitive("LONG_DIVISION", params)
    assert "DIVISION_INTERNAL_QUOTIENT_ZERO_DROPPED" in errors


def test_division_check_equation_violated(validator):
    params = {
        "dividend": 366,
        "divisor": 12,
        "quotient": 30,
        "remainder": 5  # Error: 12*30 + 5 = 365 != 366
    }
    errors = validator.validate_primitive("LONG_DIVISION", params)
    assert "DIVISION_CHECK_EQUATION_VIOLATED" in errors


def test_fraction_unequal_partition_detected(validator):
    params = {
        "partitions": [
            {"size": 10},
            {"size": 15}  # Error: unequal sizes
        ]
    }
    errors = validator.validate_primitive("FRACTION_STRIP", params)
    assert "FRACTION_PARTITION_UNEQUAL" in errors


def test_data_grounding_catches_ignored_arguments(validator):
    params = {"factors": [23, 6], "product": 138}
    evidence = {
        "data_grounded": True,
        "element_count": 5,
        "labels": ["99", "88"]  # Error: neither 23 nor 6 appear in rendered labels
    }
    errors = validator.validate_data_grounding("AREA_MODEL", params, evidence)
    assert "RENDERED_EVIDENCE_ARGUMENTS_IGNORED" in errors
