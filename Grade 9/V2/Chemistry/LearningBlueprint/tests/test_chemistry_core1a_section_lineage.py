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
from compile_chemistry_core_authority import ChemistryCoreAuthorityError, compile_core_authority  # noqa: E402
from test_chemistry_four_core_compilation import (  # noqa: E402
    REGISTRY,
    make_manifest,
    make_production_audit,
    make_request,
    payloads,
)


class ChemistryCore1ASectionLineageTests(unittest.TestCase):
    def setUp(self):
        self.gate = REGISTRY["subtopic_gates"][0]
        self.audit_ref = "tests/in-memory-core1a-lineage-audit.json"
        self.audit = make_production_audit(self.gate)
        self.request = make_request()
        self.manifest = make_manifest(self.gate, self.audit_ref)
        self.packet = compile_blueprint_obligations(
            self.request,
            self.manifest,
            registry=REGISTRY,
            source_audit_payloads={self.audit_ref: self.audit},
        )
        self.realized = [
            row["obligation_id"]
            for row in self.packet["obligations"]
            if "CORE1A" in row["authorized_modes"]
        ]

    def compile(self, payload):
        return compile_core_authority(
            "CORE1A",
            "TEST_ONLY",
            payload,
            self.packet,
            self.realized,
            authority_id="CHEM-CORE-AUTH-CORE1A-LINEAGE-TEST",
            payload_ref="tests/core1a-lineage.json",
        )

    def test_ordered_section_lineage_is_recorded_in_core_authority(self):
        authority = self.compile(payloads(self.gate)["CORE1A"])
        lineage = authority["validation_evidence"]["section_lineage"]
        self.assertEqual(lineage["status"], "PASS")
        self.assertEqual(lineage["lineage_mode"], "ORDERED_LEARNING_ATOM")
        self.assertEqual(lineage["learning_atom_count"], lineage["teaching_section_count"])

    def test_section_count_cannot_drift_from_learning_atom_denominator(self):
        payload = copy.deepcopy(payloads(self.gate)["CORE1A"])
        payload["manuscript"]["buckets"][0]["teaching_sections"].append(
            {"representation_refs": []}
        )
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            self.compile(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_AUTH_CORE1A_SECTION_ATOM_COUNT_MISMATCH")

    def test_learning_atom_ids_must_be_unique(self):
        payload = copy.deepcopy(payloads(self.gate)["CORE1A"])
        bucket = payload["manuscript"]["buckets"][0]
        bucket["learning_atoms"].append(copy.deepcopy(bucket["learning_atoms"][0]))
        bucket["teaching_sections"].append(copy.deepcopy(bucket["teaching_sections"][0]))
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            self.compile(payload)
        self.assertEqual(ctx.exception.code, "CHEM_CORE_AUTH_CORE1A_LEARNING_ATOM_DUPLICATE")


if __name__ == "__main__":
    unittest.main()
