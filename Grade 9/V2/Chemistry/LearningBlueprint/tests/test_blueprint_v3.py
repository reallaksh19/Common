from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from common import BlueprintError
from compile_transfer_eligibility import compile_transfer_eligibility
from run_blueprint_v3 import run_v3


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class BlueprintV3TransferTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = load(ROOT / "golden" / "v3-transfer-goldens.json")["fixtures"]
        cls.schemas = {
            name: load(ROOT / "contracts" / name)
            for name in [
                "transfer-envelope.schema.json",
                "transfer-request.schema.json",
                "transfer-eligibility.schema.json",
            ]
        }

    def compile(self, fixture):
        return compile_transfer_eligibility(
            copy.deepcopy(fixture["assimilation"]),
            copy.deepcopy(fixture["taught_state"]),
            copy.deepcopy(fixture["envelope"]),
            copy.deepcopy(fixture["request"]),
        )

    def test_goldens_cover_all_purposes_and_expected_release_sets(self):
        purposes = set()
        for fixture in self.fixtures:
            jsonschema.Draft202012Validator(self.schemas["transfer-envelope.schema.json"]).validate(fixture["envelope"])
            jsonschema.Draft202012Validator(self.schemas["transfer-request.schema.json"]).validate(fixture["request"])
            out = self.compile(fixture)
            jsonschema.Draft202012Validator(self.schemas["transfer-eligibility.schema.json"]).validate(out)
            purposes.add(out["purpose_mode"])
            self.assertEqual(out["eligible_item_ids"], fixture["expected"]["eligible"])
            self.assertEqual(out["blocked_item_ids"], fixture["expected"]["blocked"])
        self.assertEqual(purposes, {"FIRST_STUDY", "REVISION", "COMPETITIVE_EXAM"})

    def test_first_study_hinted_may_release_before_independent_receipt(self):
        fixture = self.fixtures[0]
        out = self.compile(fixture)
        self.assertEqual(out["decisions"][0]["status"], "ELIGIBLE")
        self.assertEqual(out["decisions"][1]["status"], "BLOCKED")
        self.assertIn("TAUGHT_STATE_INCOMPLETE", out["decisions"][1]["reason_codes"])

    def test_revision_cannot_bypass_incomplete_taught_state(self):
        fixture = copy.deepcopy(self.fixtures[1])
        fixture["taught_state"]["capabilities"][0]["checked"] = False
        fixture["taught_state"]["capabilities"][0]["evidence_refs"].pop("checked", None)
        out = self.compile(fixture)
        self.assertEqual(out["decisions"][0]["status"], "BLOCKED")
        self.assertIn("TAUGHT_STATE_INCOMPLETE", out["decisions"][0]["reason_codes"])
        self.assertFalse(out["decisions"][0]["intersection"]["taught_state"])

    def test_competitive_exam_does_not_authorize_new_semantics(self):
        out = self.compile(self.fixtures[2])
        blocked = next(row for row in out["decisions"] if row["item_id"] == "CE-NEW-SEMANTIC")
        self.assertIn("NEW_SEMANTICS_FORBIDDEN", blocked["reason_codes"])
        self.assertFalse(blocked["intersection"]["validated_semantic_scope"])

    def test_transfer_envelope_may_not_expand_semantic_scope(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["envelope"]["capabilities"].append({
            "capability_ref": "CAP-UNTaught-EXTRA",
            "allowed_question_families": ["QF-X"],
            "max_novelty_level": "SAME_STRUCTURE",
            "allowed_combination_with": [],
        })
        with self.assertRaises(BlueprintError) as ctx:
            self.compile(fixture)
        self.assertEqual(ctx.exception.code, "TRANSFER_ENVELOPE_EXPANDS_SEMANTIC_SCOPE")

    def test_candidate_outside_narrowed_envelope_is_blocked(self):
        fixture = copy.deepcopy(self.fixtures[1])
        second = fixture["assimilation"]["capability_treatments"][1]["capability_ref"]
        first = fixture["assimilation"]["capability_treatments"][0]["capability_ref"]
        fixture["envelope"]["capabilities"] = [{
            "capability_ref": first,
            "allowed_question_families": ["QF-CHANGE-EVIDENCE-CLASSIFICATION"],
            "max_novelty_level": "INTERLEAVED_TRANSFER",
            "allowed_combination_with": [],
        }]
        fixture["request"]["candidates"] = [{
            "item_id": "OUTSIDE-D",
            "primary_capability_ref": second,
            "required_capability_refs": [second],
            "question_family": "QF-OBSERVATION-INFERENCE",
            "novelty_level": "SAME_STRUCTURE",
            "support_mode": "INDEPENDENT",
            "new_semantic_claims": [],
        }]
        out = self.compile(fixture)
        self.assertEqual(out["eligible_item_ids"], [])
        self.assertIn("OUTSIDE_TRANSFER_ENVELOPE", out["decisions"][0]["reason_codes"])

    def test_question_family_must_be_authorized_by_primary_capability(self):
        fixture = copy.deepcopy(self.fixtures[2])
        fixture["request"]["candidates"] = [copy.deepcopy(fixture["request"]["candidates"][0])]
        fixture["request"]["candidates"][0]["question_family"] = "QF-NOT-AUTHORIZED"
        out = self.compile(fixture)
        self.assertIn("QUESTION_FAMILY_NOT_AUTHORIZED", out["decisions"][0]["reason_codes"])
        self.assertFalse(out["decisions"][0]["intersection"]["transfer_envelope"])

    def test_purpose_caps_capability_combination_width(self):
        fixture = copy.deepcopy(self.fixtures[0])
        cap2 = "CAP-SPECIES-ROLE"
        fixture["assimilation"]["capability_treatments"].append({"capability_ref": cap2})
        fixture["taught_state"]["capabilities"].append({
            "capability_ref": cap2,
            "taught": True, "represented": True, "worked": True,
            "faded": False, "independent": False, "checked": False,
            "evidence_refs": {"taught":["E2-T"],"represented":["E2-R"],"worked":["E2-W"]},
        })
        fixture["envelope"]["capabilities"][0]["allowed_combination_with"] = [cap2]
        fixture["envelope"]["capabilities"].append({
            "capability_ref": cap2,
            "allowed_question_families": ["QF-SPECIES-ROLE"],
            "max_novelty_level": "NEAR_TRANSFER",
            "allowed_combination_with": ["CAP-CHARGE-BALANCE"],
        })
        fixture["request"]["candidates"] = [{
            "item_id": "FS-TWO-CAP",
            "primary_capability_ref": "CAP-CHARGE-BALANCE",
            "required_capability_refs": ["CAP-CHARGE-BALANCE", cap2],
            "question_family": "PF-FORMULA-CHARGE-PARSE",
            "novelty_level": "NEAR_TRANSFER",
            "support_mode": "HINTED",
            "new_semantic_claims": [],
        }]
        out = self.compile(fixture)
        self.assertIn("CAPABILITY_COMBINATION_EXCEEDS_PURPOSE", out["decisions"][0]["reason_codes"])
        self.assertFalse(out["decisions"][0]["intersection"]["purpose"])

    def test_revision_rejects_hinted_support_mode(self):
        fixture = copy.deepcopy(self.fixtures[1])
        fixture["request"]["candidates"] = [copy.deepcopy(fixture["request"]["candidates"][0])]
        fixture["request"]["candidates"][0]["support_mode"] = "HINTED"
        out = self.compile(fixture)
        self.assertIn("SUPPORT_MODE_NOT_ALLOWED_FOR_PURPOSE", out["decisions"][0]["reason_codes"])
        self.assertFalse(out["decisions"][0]["intersection"]["purpose"])

    def test_taught_state_must_bind_exact_assimilation_digest(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["taught_state"]["assimilation_digest"] = "wrong"
        with self.assertRaises(BlueprintError) as ctx:
            self.compile(fixture)
        self.assertEqual(ctx.exception.code, "TRANSFER_TAUGHT_STATE_ASSIMILATION_DIGEST_MISMATCH")

    def test_taught_state_capability_coverage_is_exact(self):
        fixture = copy.deepcopy(self.fixtures[1])
        fixture["taught_state"]["capabilities"].pop()
        with self.assertRaises(BlueprintError) as ctx:
            self.compile(fixture)
        self.assertEqual(ctx.exception.code, "TRANSFER_TAUGHT_STATE_CAPABILITY_COVERAGE_MISMATCH")

    def test_envelope_combination_refs_cannot_escape_envelope(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["envelope"]["capabilities"][0]["allowed_combination_with"] = ["CAP-NOT-IN-ENVELOPE"]
        with self.assertRaises(BlueprintError) as ctx:
            self.compile(fixture)
        self.assertEqual(ctx.exception.code, "TRANSFER_ENVELOPE_COMBINATION_OUTSIDE_ENVELOPE")

    def test_duplicate_candidate_ids_fail_closed(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["request"]["candidates"][1]["item_id"] = fixture["request"]["candidates"][0]["item_id"]
        with self.assertRaises(BlueprintError) as ctx:
            self.compile(fixture)
        self.assertEqual(ctx.exception.code, "TRANSFER_CANDIDATE_IDS_INVALID")

    def test_blocked_items_never_appear_in_release_list(self):
        out = self.compile(self.fixtures[1])
        self.assertTrue(set(out["eligible_item_ids"]).isdisjoint(out["blocked_item_ids"]))
        for row in out["decisions"]:
            if row["status"] == "BLOCKED":
                self.assertNotIn(row["item_id"], out["eligible_item_ids"])

    def test_run_v3_manifest_reports_release_counts(self):
        fixture = self.fixtures[2]
        result = run_v3(
            copy.deepcopy(fixture["assimilation"]),
            copy.deepcopy(fixture["taught_state"]),
            copy.deepcopy(fixture["envelope"]),
            copy.deepcopy(fixture["request"]),
        )
        self.assertEqual(result["manifest"]["blueprint_version"], "v3")
        self.assertEqual(result["manifest"]["eligible_item_count"], 1)
        self.assertEqual(result["manifest"]["blocked_item_count"], 1)
        self.assertEqual(result["manifest"]["status"], "PASS_TRANSFER_ITEMS_RELEASED")

    def test_compilation_is_deterministic(self):
        first = self.compile(self.fixtures[2])
        second = self.compile(self.fixtures[2])
        self.assertEqual(first["digest"], second["digest"])


if __name__ == "__main__":
    unittest.main()
