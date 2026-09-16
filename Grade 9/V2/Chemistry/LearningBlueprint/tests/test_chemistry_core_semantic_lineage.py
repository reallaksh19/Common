import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_core_authority import ChemistryCoreAuthorityError, compile_core_authority  # noqa: E402
from compile_chemistry_semantic_projection import digest_without  # noqa: E402


def make_packet():
    obligations = [
        {
            "obligation_id": "CHEM-OBL-SYNTH-CONCEPT",
            "gate_id": "CHEM-SYNTH-ALPHA",
            "direct": True,
            "kind": "CONCEPT",
            "asset_ref": "CON-SYNTH-ALPHA",
            "authorized_modes": ["CORE1A", "CORE1B", "CORE2A", "CORE2B"],
            "required_realization_modes": ["CORE1A"],
            "source_authority_tier": "SOURCE-DEFINED",
            "payload": {"canonical_statement": "Synthetic governed concept."},
        },
        {
            "obligation_id": "CHEM-OBL-SYNTH-PROBLEM",
            "gate_id": "CHEM-SYNTH-ALPHA",
            "direct": True,
            "kind": "PROBLEM_FAMILY",
            "asset_ref": "PF-CHEM-SYNTH",
            "authorized_modes": ["CORE1A", "CORE1B", "CORE2A", "CORE2B"],
            "required_realization_modes": ["CORE1A"],
            "source_authority_tier": "SOURCE-DEFINED",
            "payload": {
                "family_id": "PF-CHEM-SYNTH",
                "name": "Synthetic family",
                "recognition_cues": "Identify the governed relationship.",
                "first_technical_move": "Write the governed relationship.",
                "common_fatal_error": "Reverse the relationship without evidence.",
                "typical_unknown": "The consistent conclusion.",
            },
        },
    ]
    packet = {
        "schema_version": "1.0.0",
        "packet_id": "CHEM-BP-OBL-CORE-SEMANTIC-TEST",
        "subject": "CHEMISTRY",
        "request_id": "CHEM-ENG-REQ-CORE-SEMANTIC-TEST",
        "manifest_id": "CHEM-ENG-MAN-CORE-SEMANTIC-TEST",
        "scope_ref": "TEST_ONLY",
        "engineering_binding_id": "CHEM-ENG-BIND-CORE-SEMANTIC-TEST",
        "engineering_binding_digest": "sha256:" + "1" * 64,
        "closure_receipt_id": "CHEM-ENG-CLOSURE-CORE-SEMANTIC-TEST",
        "closure_digest": "sha256:" + "2" * 64,
        "registry_ref": "policies/chemistry-technical-engineering-gates.v1.json",
        "registry_digest": "sha256:" + "3" * 64,
        "direct_gate_ids": ["CHEM-SYNTH-ALPHA"],
        "closure_gate_ids": ["CHEM-SYNTH-ALPHA"],
        "obligations": obligations,
        "counts": {
            "gate_count": 1,
            "direct_gate_count": 1,
            "obligation_count": 2,
            "required_by_mode": {"CORE1A": 2, "CORE1B": 0, "CORE2A": 0, "CORE2B": 0},
        },
        "status": "BLUEPRINT_OBLIGATIONS_READY",
        "packet_digest": "",
    }
    packet["packet_digest"] = digest_without(packet, "packet_digest")
    return packet


def payload():
    return {
        "manuscript": {
            "manuscript_id": "TEST-SEMANTIC-MANUSCRIPT",
            "buckets": [
                {"learning_atoms": [{"atom_id": "ATOM-SEMANTIC-1"}]}
            ],
        },
        "representation_bundle": {"bundle_id": "TEST-SEMANTIC-REP-BUNDLE"},
    }


class ChemistryCoreSemanticLineageTests(unittest.TestCase):
    def test_core_authority_recompiles_and_binds_semantic_projection(self):
        packet = make_packet()
        realized = [row["obligation_id"] for row in packet["obligations"]]
        authority = compile_core_authority(
            "CORE1A",
            "TEST_ONLY",
            payload(),
            packet,
            realized,
            authority_id="CHEM-CORE-AUTH-SEMANTIC-LINEAGE-TEST",
            payload_ref="tests/synthetic-core1a.json",
        )
        self.assertEqual(authority["semantic_closure"]["status"], "PASS")
        self.assertEqual(authority["semantic_projection_id"], "CHEM-BP-SEM-CORE-SEMANTIC-TEST")
        self.assertEqual(
            set(authority["semantic_closure"]["realized_source_obligation_ids"]),
            set(realized),
        )
        self.assertEqual(
            set(authority["semantic_closure"]["required_semantic_ids"]),
            set(authority["semantic_closure"]["realized_semantic_ids"]),
        )
        self.assertEqual(authority["semantic_closure"]["semantic_atom_count"], 5)

    def test_required_obligation_cannot_claim_core_realization_without_its_semantics(self):
        packet = make_packet()
        realized = [packet["obligations"][0]["obligation_id"]]
        with self.assertRaises(ChemistryCoreAuthorityError) as ctx:
            compile_core_authority(
                "CORE1A",
                "TEST_ONLY",
                payload(),
                packet,
                realized,
                authority_id="CHEM-CORE-AUTH-SEMANTIC-MISSING-TEST",
                payload_ref="tests/synthetic-core1a-missing.json",
            )
        self.assertEqual(ctx.exception.code, "CHEM_CORE_AUTH_REQUIRED_OBLIGATION_MISSING")

    def test_core_authority_contains_no_topic_selected_semantic_roles(self):
        text = (ENGINE / "compile_chemistry_core_authority.py").read_text(encoding="utf-8").lower()
        for forbidden in ("re" + "dox", "mn" + "o4", "perman" + "ganate", "thermo" + "dynamics"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
