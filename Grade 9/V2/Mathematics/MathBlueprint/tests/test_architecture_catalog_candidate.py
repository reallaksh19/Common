from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
CATALOG = DESIGN / "mathematics-architecture-catalog.candidate.json"
SCHEMA = DESIGN / "mathematics-architecture-catalog.candidate.schema.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def catalog_invariant_violations(payload: dict) -> list[str]:
    violations: list[str] = []
    components = payload.get("components", [])

    ids = [row.get("component_id") for row in components]
    for component_id, count in sorted(Counter(ids).items()):
        if component_id and count > 1:
            violations.append(f"duplicate component_id: {component_id}")

    for row in components:
        component_id = row.get("component_id", "<missing>")
        for rel in row.get("evidence_paths", []):
            path = (ROOT / rel).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                violations.append(f"{component_id}: evidence path escapes MathBlueprint root: {rel}")
                continue
            if not path.exists():
                violations.append(f"{component_id}: missing evidence path: {rel}")

        if row.get("catalog_basis") != "REPOSITORY_DERIVED":
            violations.append(f"{component_id}: catalog_basis must remain REPOSITORY_DERIVED")
        if row.get("audit_status") != "PENDING_INDEPENDENT_AUDIT":
            violations.append(f"{component_id}: audit status cannot be upgraded by C1 inventory")
        if row.get("semantic_change") != "NONE":
            violations.append(f"{component_id}: C1 inventory may not claim semantic change")

        if row.get("primary_authority_class") == "DESIGN_ONLY":
            if row.get("runtime_authority_effect") != "NONE_DESIGN_ONLY":
                violations.append(f"{component_id}: design-only component claims runtime authority")
            if row.get("publication_authority_effect") != "NONE":
                violations.append(f"{component_id}: design-only component claims publication authority")

    return violations


class ArchitectureCatalogCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_json(CATALOG)
        cls.schema = load_json(SCHEMA)
        cls.validator = Draft202012Validator(cls.schema)

    def test_candidate_validates_against_design_schema(self):
        errors = sorted(self.validator.iter_errors(self.catalog), key=lambda e: list(e.path))
        self.assertEqual(
            errors,
            [],
            "Architecture catalog candidate must satisfy its non-normative design schema: "
            + "; ".join(error.message for error in errors),
        )

    def test_candidate_is_explicitly_non_authoritative_and_c2_blocked(self):
        self.assertEqual(self.catalog["status"], "DESIGN_NON_NORMATIVE_CANDIDATE")
        self.assertEqual(self.catalog["authority"], "NONE")
        self.assertEqual(self.catalog["semantic_change"], "NONE")
        self.assertEqual(self.catalog["catalog_basis"], "REPOSITORY_INVENTORY_ONLY")
        self.assertEqual(
            self.catalog["independent_audit_status"], "PENDING_INDEPENDENT_AUDIT"
        )
        self.assertEqual(
            self.catalog["core_spec_consolidation_status"],
            "BLOCKED_PENDING_INDEPENDENT_AUDIT",
        )

    def test_component_identity_and_evidence_paths_are_repository_backed(self):
        self.assertGreaterEqual(len(self.catalog["components"]), 1)
        self.assertEqual(catalog_invariant_violations(self.catalog), [])

    def test_all_components_remain_repository_derived_pending_audit_noop(self):
        for row in self.catalog["components"]:
            with self.subTest(component_id=row["component_id"]):
                self.assertEqual(row["catalog_basis"], "REPOSITORY_DERIVED")
                self.assertEqual(row["audit_status"], "PENDING_INDEPENDENT_AUDIT")
                self.assertEqual(row["semantic_change"], "NONE")

    def test_design_only_component_cannot_claim_runtime_or_publication_authority(self):
        design_rows = [
            row
            for row in self.catalog["components"]
            if row["primary_authority_class"] == "DESIGN_ONLY"
        ]
        self.assertTrue(design_rows, "candidate must explicitly classify its design workspace")
        for row in design_rows:
            with self.subTest(component_id=row["component_id"]):
                self.assertEqual(row["runtime_authority_effect"], "NONE_DESIGN_ONLY")
                self.assertEqual(row["publication_authority_effect"], "NONE")

    def test_duplicate_component_identity_is_falsified(self):
        mutated = copy.deepcopy(self.catalog)
        mutated["components"].append(copy.deepcopy(mutated["components"][0]))
        violations = catalog_invariant_violations(mutated)
        self.assertTrue(
            any("duplicate component_id" in message for message in violations),
            violations,
        )

    def test_missing_or_escaping_evidence_path_is_falsified(self):
        mutated = copy.deepcopy(self.catalog)
        mutated["components"][0]["evidence_paths"] = [
            "engine/definitely-not-a-real-architecture-file.py",
            "../../outside-mathblueprint.txt",
        ]
        violations = catalog_invariant_violations(mutated)
        self.assertTrue(any("missing evidence path" in message for message in violations), violations)
        self.assertTrue(any("escapes MathBlueprint root" in message for message in violations), violations)

    def test_schema_rejects_authority_or_audit_promotion_inside_c1(self):
        mutated = copy.deepcopy(self.catalog)
        mutated["authority"] = "AUTHORITATIVE"
        mutated["independent_audit_status"] = "PASSED"
        mutated["core_spec_consolidation_status"] = "READY"
        errors = list(self.validator.iter_errors(mutated))
        self.assertGreaterEqual(len(errors), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
