from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from validate_b_layer_integration import seal_b_layer_integration, validate_b_layer_integration


RUN = "MATH-MLR-0123456789abcdef"
BUNDLE = "MATH-HB-0123456789abcdef"
PLAN = "MATH-AP-0123456789abcdef"
DIGEST = "a" * 64


def draft(*, c1b="NOT_COMPILED", c2a="LEGAL_POOL_READY", c2b="NOT_COMPILED", ceiling="M2_REPRESENTATION_TRANSFER"):
    return {
        "run_ref": RUN,
        "bundle_ref": BUNDLE,
        "assimilation_plan_ref": PLAN,
        "core1a_authority": {
            "authority_ref": "C1A-AUTH-1",
            "authority_digest": DIGEST,
            "approved_capability_refs": ["CAP-1", "CAP-2"],
            "learner_treatment_ref": "MF-TREATMENT-1",
            "status": "AUTHORITY_READY",
        },
        "core1b_lane": {
            "compiled_plan_ref": "MATH-C1B-PLAN-1" if c1b == "COMPILED" else None,
            "compiled_plan_digest": DIGEST if c1b == "COMPILED" else None,
            "delivery_mode": "STATIC" if c1b == "COMPILED" else None,
            "status": c1b,
        },
        "core2a_lane": {
            "legal_pool_ref": "C2A-POOL-1" if c2a == "LEGAL_POOL_READY" else None,
            "legal_pool_digest": DIGEST if c2a == "LEGAL_POOL_READY" else None,
            "purpose": "PRACTICE" if c2a == "LEGAL_POOL_READY" else None,
            "status": c2a,
        },
        "core2b_compile_ceiling": {
            "max_demand_level": ceiling,
            "source_ref": "UPSTREAM-CEILING-1" if ceiling else None,
            "source_class": "OTHER_GOVERNED_UPSTREAM" if ceiling else None,
        },
        "core2b_lane": {
            "compiled_plan_ref": "MATH-C2B-PLAN-1" if c2b == "COMPILED" else None,
            "compiled_plan_digest": DIGEST if c2b == "COMPILED" else None,
            "delivery_mode": "STATIC" if c2b == "COMPILED" else None,
            "status": c2b,
        },
    }


class BLayerIntegrationTests(unittest.TestCase):
    def test_ready_to_compile_does_not_require_core1b_first(self):
        out = seal_b_layer_integration(draft())
        self.assertEqual(out["status"], "READY_TO_COMPILE")
        validate_b_layer_integration(out)

    def test_core2b_can_compile_without_core1b_product(self):
        out = seal_b_layer_integration(draft(c1b="NOT_COMPILED", c2b="COMPILED"))
        self.assertEqual(out["status"], "PARTIALLY_COMPILED")
        self.assertTrue(out["invariants"]["core2b_does_not_require_core1b_product"])

    def test_core1b_can_compile_before_core2a_is_ready(self):
        out = seal_b_layer_integration(draft(c1b="COMPILED", c2a="NOT_READY", c2b="NOT_COMPILED", ceiling=None))
        self.assertEqual(out["status"], "PARTIALLY_COMPILED")

    def test_core2b_requires_bound_core2a_pool(self):
        d = draft(c1b="NOT_COMPILED", c2a="NOT_READY", c2b="COMPILED")
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_CORE2B_WITHOUT_CORE2A_POOL"):
            seal_b_layer_integration(d)

    def test_core2b_requires_upstream_compile_ceiling(self):
        d = draft(c2b="COMPILED", ceiling=None)
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_CORE2B_COMPILE_CEILING_MISSING"):
            seal_b_layer_integration(d)

    def test_core1b_must_be_static_when_compiled(self):
        d = draft(c1b="COMPILED")
        d["core1b_lane"]["delivery_mode"] = None
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_CORE1B_NONSTATIC_DELIVERY|MATH_B_LAYER_CORE1B_PRODUCT_BINDING_INCOMPLETE"):
            seal_b_layer_integration(d)

    def test_core2b_must_be_static_when_compiled(self):
        d = draft(c2b="COMPILED")
        d["core2b_lane"]["delivery_mode"] = None
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_CORE2B_NONSTATIC_DELIVERY|MATH_B_LAYER_CORE2B_PRODUCT_BINDING_INCOMPLETE"):
            seal_b_layer_integration(d)

    def test_compiled_products_do_not_claim_learner_evidence(self):
        out = seal_b_layer_integration(draft(c1b="COMPILED", c2b="COMPILED"))
        self.assertEqual(out["status"], "COMPILED")
        inv = out["invariants"]
        self.assertTrue(inv["compiled_product_not_learner_evidence"])
        self.assertTrue(inv["b_layers_do_not_ingest_learner_responses"])
        self.assertTrue(inv["b_layers_do_not_emit_learner_state_transitions"])

    def test_runtime_fields_are_not_part_of_integration_contract(self):
        d = draft()
        d["core2b_lane"]["retrieval_state_refs"] = []
        with self.assertRaises(Exception):
            seal_b_layer_integration(d)


if __name__ == "__main__":
    unittest.main()
