#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_mathematics_engineering_workbench import load  # noqa: E402
from validate_engineered_domain_admission import (  # noqa: E402
    MathematicsEngineeredDomainAdmissionError,
    validate,
)

ADMISSION = load("fixtures/engineering-workbench/theory-equations-domain-admission.v1.json")
DOMAIN = load("golden/domain_registry/01-theory-of-equations-registry.json")
BINDING = load("fixtures/engineering-workbench/quad-equations-binding.v1.json")
TECH_REGISTRY = load("policies/mathematics-technical-engineering-gates.v1.json")
PROFILE = load("policies/mathematics-engineering-gate-invariants.v1.json")


class EngineeredDomainAdmissionTests(unittest.TestCase):
    def test_theory_of_equations_requires_current_engineering_closure(self):
        result = validate(
            ADMISSION,
            domain_registry=copy.deepcopy(DOMAIN),
            engineering_binding=copy.deepcopy(BINDING),
            technical_registry=copy.deepcopy(TECH_REGISTRY),
            invariant_profile=copy.deepcopy(PROFILE),
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["technical_authorization"], "ALLOWED")
        self.assertEqual(result["publication_authorization"], "NOT_IMPLIED")
        self.assertEqual(result["mapped_subtopic_count"], 1)

    def test_unmapped_domain_subtopic_fails(self):
        admission = copy.deepcopy(ADMISSION)
        admission["subtopic_gate_map"] = []
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=copy.deepcopy(DOMAIN), engineering_binding=copy.deepcopy(BINDING), technical_registry=copy.deepcopy(TECH_REGISTRY), invariant_profile=copy.deepcopy(PROFILE))
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_ADMISSION_SCHEMA")

    def test_gate_outside_engineering_closure_fails(self):
        admission = copy.deepcopy(ADMISSION)
        admission["subtopic_gate_map"][0]["engineering_gate_id"] = "MATH-GEO-CIRCLES"
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(admission, domain_registry=copy.deepcopy(DOMAIN), engineering_binding=copy.deepcopy(BINDING), technical_registry=copy.deepcopy(TECH_REGISTRY), invariant_profile=copy.deepcopy(PROFILE))
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_GATE_OUTSIDE_CLOSURE")

    def test_wrong_downstream_consumer_fails(self):
        binding = copy.deepcopy(BINDING)
        binding["downstream_consumer"] = "SDU"
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(ADMISSION, domain_registry=copy.deepcopy(DOMAIN), engineering_binding=binding, technical_registry=copy.deepcopy(TECH_REGISTRY), invariant_profile=copy.deepcopy(PROFILE))
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_WRONG_CONSUMER")

    def test_structurally_invalid_domain_registry_fails(self):
        domain = copy.deepcopy(DOMAIN)
        domain["assets"][0]["asset_id"] = domain["assets"][1]["asset_id"]
        with self.assertRaises(MathematicsEngineeredDomainAdmissionError) as ctx:
            validate(ADMISSION, domain_registry=domain, engineering_binding=copy.deepcopy(BINDING), technical_registry=copy.deepcopy(TECH_REGISTRY), invariant_profile=copy.deepcopy(PROFILE))
        self.assertEqual(ctx.exception.code, "MATH_ENG_DOMAIN_REGISTRY_INVALID")


if __name__ == "__main__":
    unittest.main()
