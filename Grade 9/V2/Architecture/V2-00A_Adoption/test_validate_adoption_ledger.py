import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("validate_adoption_ledger", ROOT / "validate_adoption_ledger.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def load(name):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


class AdoptionLedgerValidationTests(unittest.TestCase):
    def test_seeded_ledger_passes(self):
        doc = json.loads((ROOT / "adoption_ledger.json").read_text(encoding="utf-8"))
        self.assertEqual([], MODULE.validate_document(doc))

    def test_valid_minimal_passes(self):
        self.assertEqual([], MODULE.validate_document(load("valid_minimal.json")))

    def test_benchmark_leak_fails(self):
        errors = MODULE.validate_document(load("invalid_benchmark_leak.json"))
        self.assertTrue(any("benchmark" in e.lower() or "PR #156/#157" in e for e in errors), errors)

    def test_old_branch_runtime_dependency_fails(self):
        errors = MODULE.validate_document(load("invalid_runtime_dependency.json"))
        self.assertTrue(any("runtime dependency" in e.lower() or "old branch" in e.lower() for e in errors), errors)

    def test_pr168_synthetic_fixture_must_be_test_only(self):
        doc = load("valid_minimal.json")
        entry = doc["entries"][0]
        entry.update({
            "id": "A-INVALID-PR168-SYNTHETIC",
            "source_pr_or_issue": "PR #168",
            "source_path_or_artifact": "synthetic answer-sheet fixture",
            "source_authority_class": "EVIDENCE",
            "v2_action": "ADAPT",
            "v2_owner": "LEARNER_INTELLIGENCE",
            "status": "PLANNED",
        })
        errors = MODULE.validate_document(doc)
        self.assertTrue(any("synthetic fixtures" in e.lower() for e in errors), errors)

    def test_inference_cannot_become_core1_truth(self):
        doc = load("valid_minimal.json")
        entry = doc["entries"][0]
        entry.update({
            "id": "A-INVALID-INFERENCE-CORE1",
            "source_authority_class": "INFERENCE",
            "v2_owner": "CORE1_CANONICAL_AUTHORITY",
        })
        errors = MODULE.validate_document(doc)
        self.assertTrue(any("core1 canonical truth" in e.lower() for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
