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


def draft(*, c1b="RELEASED", c2a="LEGAL_POOL_READY", c2b="READY", execution="PRODUCTION"):
    return {
        "execution_class": execution,
        "run_ref": RUN,
        "bundle_ref": BUNDLE,
        "assimilation_plan_ref": PLAN,
        "core1a_realization": {
            "artifact_ref": "core1a.pdf",
            "artifact_digest": DIGEST,
            "surface_manifest_ref": "core1a_surface_manifest.json",
            "surface_manifest_digest": DIGEST,
            "manifest_origin": "RENDERER_EMITTED" if execution == "PRODUCTION" else "TEST_FIXTURE",
            "semantic_binding": "SEMANTIC_COMPONENT_DIGESTS" if execution == "PRODUCTION" else "ARTIFACT_ONLY",
            "status": "REALIZED",
        },
        "core1b_lane": {
            "exposure_receipt_refs": ["C1B-EXP-1"] if c1b != "NOT_READY" else [],
            "learner_evidence_refs": ["C1B-EV-1"] if c1b in {"EVIDENCE_AVAILABLE", "RELEASED"} else [],
            "release_receipt_refs": ["C1B-REL-1"] if c1b == "RELEASED" else [],
            "repair_request_refs": [],
            "status": c1b,
        },
        "core2a_lane": {
            "legal_pool_ref": "C2A-POOL-1" if c2a == "LEGAL_POOL_READY" else None,
            "legal_pool_digest": DIGEST if c2a == "LEGAL_POOL_READY" else None,
            "status": c2a,
        },
        "core2b_lane": {
            "session_ref": "C2B-SESSION-1" if c2b in {"READY", "ACTIVE"} else None,
            "retrieval_state_refs": [],
            "repair_handoff_refs": [],
            "status": c2b,
        },
    }


class BLayerIntegrationTests(unittest.TestCase):
    def test_ready_requires_core1b_release_and_core2a_legal_pool(self):
        out = seal_b_layer_integration(draft())
        self.assertEqual(out["status"], "CORE2B_READY")
        validate_b_layer_integration(out)

    def test_core2a_can_compile_before_core1b_release(self):
        d = draft(c1b="EVIDENCE_AVAILABLE", c2a="LEGAL_POOL_READY", c2b="BLOCKED")
        out = seal_b_layer_integration(d)
        self.assertEqual(out["status"], "WAITING_FOR_CORE1B")

    def test_core2b_cannot_start_from_exposure_only(self):
        d = draft(c1b="EXPOSURE_VERIFIED", c2a="LEGAL_POOL_READY", c2b="READY")
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_CORE2B_WITHOUT_CORE1B_RELEASE"):
            seal_b_layer_integration(d)

    def test_core2b_cannot_start_without_bound_core2a_pool(self):
        d = draft(c1b="RELEASED", c2a="NOT_READY", c2b="READY")
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_CORE2B_WITHOUT_CORE2A_POOL"):
            seal_b_layer_integration(d)

    def test_production_rejects_hand_authored_surface_manifest(self):
        d = draft()
        d["core1a_realization"]["manifest_origin"] = "TEST_FIXTURE"
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_TEST_FIXTURE_MANIFEST_USED_IN_PRODUCTION"):
            seal_b_layer_integration(d)

    def test_production_requires_semantic_component_binding(self):
        d = draft()
        d["core1a_realization"]["semantic_binding"] = "ARTIFACT_ONLY"
        with self.assertRaisesRegex(ValueError, "MATH_B_LAYER_PRODUCTION_SURFACE_SEMANTIC_BINDING_MISSING"):
            seal_b_layer_integration(d)

    def test_test_fixture_may_use_fixture_manifest(self):
        out = seal_b_layer_integration(draft(execution="TEST_FIXTURE"))
        self.assertEqual(out["status"], "CORE2B_READY")

    def test_planned_realized_evidenced_and_legal_ready_are_distinct(self):
        out = seal_b_layer_integration(draft())
        inv = out["invariants"]
        self.assertTrue(inv["planned_not_realized"])
        self.assertTrue(inv["realized_not_evidenced"])
        self.assertTrue(inv["core2a_legality_not_core2b_readiness"])


if __name__ == "__main__":
    unittest.main()
