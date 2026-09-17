import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
TESTS = ROOT / "tests"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(TESTS))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_core_representation_bundle import (  # noqa: E402
    ChemistryCoreRepresentationError,
    compile_core_representation_bundle,
)
from compile_chemistry_representation_intent import (  # noqa: E402
    compile_representation_intent,
    digest_without as intent_digest_without,
)
from test_chemistry_four_core_compilation import (  # noqa: E402
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
)


class ChemistryCoreRepresentationBundleTests(unittest.TestCase):
    def setUp(self):
        self.gate = REGISTRY["subtopic_gates"][0]
        self.audit_ref = "tests/in-memory-representation-bundle-audit.json"
        self.audit = make_production_audit(self.gate)
        self.packet = compile_blueprint_obligations(
            make_request(),
            make_manifest(self.gate, self.audit_ref),
            registry=REGISTRY,
            source_audit_payloads={self.audit_ref: self.audit},
        )
        self.intent = compile_representation_intent("CORE1A", self.packet)
        self.intent_ids = [row["intent_id"] for row in self.intent["intents"]]
        self.engineering_rep = self.gate["representations"][0]["representation_id"]

    def compile(self, realized=None, intent=None):
        return compile_core_representation_bundle(
            "CORE1A",
            self.packet,
            intent or self.intent,
            self.intent_ids if realized is None else realized,
            representation_extensions=[],
            representation_intent_extensions=[],
            bundle_id="CHEM-REP-BUNDLE-TEST",
        )

    def test_governed_intent_compiles_without_adapter_primitive_or_semantic_payload(self):
        bundle, bindings = self.compile()
        self.assertEqual(bundle["summary"]["renderer_selection_allowed"], False)
        self.assertEqual(bundle["summary"]["adapter_primitive_selection_allowed"], False)
        self.assertEqual(bundle["summary"]["adapter_scientific_semantics_allowed"], False)
        self.assertEqual(bundle["summary"]["required_intent_count"], 1)
        self.assertEqual(bundle["representations"][0]["primitive_id"], "MACRO_PARTICLE_SYMBOLIC_BRIDGE")
        self.assertEqual(bindings[0]["engineering_representation_refs"], [self.engineering_rep])
        self.assertEqual(bindings[0]["intent_ref"], self.intent_ids[0])

    def test_required_governed_intent_cannot_be_omitted(self):
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile([])
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_REQUIRED_INTENT_MISSING")

    def test_unknown_intent_reference_fails_closed(self):
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile(["CHEM-REP-INTENT-NOT-AUTHORIZED"])
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_INTENT_UNKNOWN")

    def test_tampered_primitive_in_intent_packet_fails_recompile_validation(self):
        bad = copy.deepcopy(self.intent)
        bad["intents"][0]["primitive_id"] = "CONSERVATION_LEDGER"
        bad["intent_packet_digest"] = intent_digest_without(bad, "intent_packet_digest")
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile(intent=bad)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_INTENT_PACKET_INVALID")

    def test_tampered_scientific_semantics_in_intent_packet_fails_recompile_validation(self):
        bad = copy.deepcopy(self.intent)
        bad["intents"][0]["scientific_semantics"]["chemistry_encoded"] = "adapter replacement"
        bad["intent_packet_digest"] = intent_digest_without(bad, "intent_packet_digest")
        with self.assertRaises(ChemistryCoreRepresentationError) as ctx:
            self.compile(intent=bad)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_REP_INTENT_PACKET_INVALID")

    def test_generic_representation_compiler_has_no_adapter_plan_or_topic_branch(self):
        text = (ENGINE / "compile_chemistry_core_representation_bundle.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate", "representation_plan", "source_semantic_data"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
