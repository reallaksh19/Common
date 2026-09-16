from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
RECEIPT = DESIGN / "mathematics-normative-root-consolidation.json"
SCHEMA = DESIGN / "mathematics-normative-root-consolidation.schema.json"
AUDIT = DESIGN / "mathematics-architecture-documentation-drift-audit.json"
CANONICAL = ROOT / "CANONICAL_ARCHITECTURE.md"
DUAL_TRACK = ROOT / "DUAL_TRACK_PRODUCT_MODEL.md"
SDU_LAU_COMPILER = ROOT / "engine" / "compile_sdu_lau_generation_spec.py"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class NormativeRootConsolidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = load_json(RECEIPT)
        cls.schema = load_json(SCHEMA)
        cls.audit = load_json(AUDIT)
        cls.validator = Draft202012Validator(cls.schema)
        cls.canonical = CANONICAL.read_text(encoding="utf-8")
        cls.dual_track = DUAL_TRACK.read_text(encoding="utf-8")
        cls.compiler = SDU_LAU_COMPILER.read_text(encoding="utf-8")

    def test_c2_receipt_is_non_authoritative_and_schema_valid(self):
        errors = sorted(self.validator.iter_errors(self.receipt), key=lambda e: list(e.path))
        self.assertEqual(errors, [], "; ".join(error.message for error in errors))
        self.assertEqual(self.receipt["status"], "C2_NORMATIVE_ROOT_CONSOLIDATED")
        self.assertEqual(self.receipt["authority"], "NONE")
        self.assertEqual(self.receipt["semantic_change"], "NONE")

    def test_every_c0_finding_has_exactly_one_c2_disposition(self):
        audit_ids = {row["finding_id"] for row in self.audit["findings"]}
        rows = self.receipt["finding_dispositions"]
        receipt_ids = [row["finding_id"] for row in rows]
        self.assertEqual(len(receipt_ids), len(set(receipt_ids)))
        self.assertEqual(set(receipt_ids), audit_ids)
        by_id = {row["finding_id"]: row for row in rows}
        self.assertEqual(by_id["C0-F007"]["disposition"], "PRESERVED_DOCUMENTED_ONLY")
        for finding_id in audit_ids - {"C0-F007"}:
            self.assertEqual(by_id[finding_id]["disposition"], "RESOLVED_DOCUMENTATION")

    def test_canonical_root_contains_current_authority_and_publication_topology(self):
        required = [
            "Engineering is upstream technical mathematical authority",
            "A discovery candidate, rank-1 result, vocabulary match",
            "Core1 is compact semantic reconstruction/basic orientation",
            "CURRENT + DOCUMENTED ONLY — C0-F007",
            "publication_authorization = NOT_IMPLIED",
            "semantic_source = LEARNER_PUBLICATION_BUNDLE_ONLY",
            "Semantic learner publication bundle",
        ]
        for marker in required:
            self.assertIn(marker, self.canonical)

        stale = [
            "Core1 determines semantic authority.",
            "EASY   -> no pedagogy-enrichment web research by default",
            "validated Core realization + TTUs + lineage + provenance\n-> LearnerPageBlueprint\n-> deterministic typesetting",
        ]
        for marker in stale:
            self.assertNotIn(marker, self.canonical)

    def test_dual_track_no_longer_prohibits_easy_research_or_uses_legacy_publication_path(self):
        self.assertIn("EASY   → up to 10 pages; pedagogy-enrichment research OPTIONAL", self.dual_track)
        self.assertIn("CURRENT + DOCUMENTED ONLY", self.dual_track)
        self.assertIn("semantic_source = LEARNER_PUBLICATION_BUNDLE_ONLY", self.dual_track)
        self.assertIn("publication_authorization = NOT_IMPLIED", self.dual_track)
        self.assertNotIn("EASY   → up to 10 pages; no pedagogy-enrichment web research", self.dual_track)
        self.assertNotIn("validated LearnerPageBlueprint\n      ↓\nPublication", self.dual_track)

    def test_f007_is_not_falsely_upgraded_during_c2(self):
        gap = self.receipt["tracked_runtime_gap"]
        self.assertEqual(gap["finding_id"], "C0-F007")
        self.assertEqual(gap["classification"], "CURRENT + DOCUMENTED ONLY")
        self.assertTrue(gap["migration_required"])
        self.assertTrue(gap["must_not_claim_executable"])
        self.assertIn(
            'non_easy = [row for row in rows if row["difficulty_badge"] != "EASY"]',
            self.compiler,
        )
        self.assertIn("for row in non_easy:", self.compiler)

    def test_c3_readiness_requires_zero_owner_decision_blockers(self):
        self.assertEqual(self.audit["owner_decision_required_count"], 0)
        self.assertEqual(self.receipt["owner_decision_required_count"], 0)
        self.assertEqual(self.receipt["next_stage"], "C3_GENERATED_REFERENCES_READY")

    def test_schema_rejects_authority_or_semantic_promotion_inside_c2_receipt(self):
        mutated = copy.deepcopy(self.receipt)
        mutated["authority"] = "AUTHORITATIVE"
        mutated["semantic_change"] = "RUNTIME_CHANGED"
        mutated["tracked_runtime_gap"]["classification"] = "CURRENT + EXECUTABLE"
        errors = list(self.validator.iter_errors(mutated))
        self.assertGreaterEqual(len(errors), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
