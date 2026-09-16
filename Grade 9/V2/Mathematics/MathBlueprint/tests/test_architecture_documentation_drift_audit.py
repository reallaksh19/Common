from __future__ import annotations

import copy
import json
import unittest
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design"
AUDIT = DESIGN / "mathematics-architecture-documentation-drift-audit.json"
SCHEMA = DESIGN / "mathematics-architecture-documentation-drift-audit.schema.json"
CATALOG = DESIGN / "mathematics-architecture-catalog.candidate.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _check_path(rel: str, label: str, violations: list[str]) -> None:
    path = (ROOT / rel).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        violations.append(f"{label}: evidence path escapes MathBlueprint root: {rel}")
        return
    if not path.exists():
        violations.append(f"{label}: missing evidence path: {rel}")


def audit_invariant_violations(payload: dict, catalog: dict) -> list[str]:
    violations: list[str] = []
    findings = payload.get("findings", [])
    finding_ids = [row.get("finding_id") for row in findings]
    for finding_id, count in sorted(Counter(finding_ids).items()):
        if finding_id and count > 1:
            violations.append(f"duplicate finding_id: {finding_id}")

    for row in findings:
        finding_id = row.get("finding_id", "<missing>")
        for evidence in row.get("evidence", []):
            _check_path(evidence.get("path", ""), finding_id, violations)
        required = bool(row.get("owner_decision_required"))
        conflicted = row.get("classification") == "CONFLICTED / OWNER DECISION REQUIRED"
        if required != conflicted:
            violations.append(
                f"{finding_id}: owner_decision_required must match conflicted classification"
            )
        if row.get("classification") == "STALE" and len(row.get("evidence", [])) < 2:
            violations.append(f"{finding_id}: stale finding requires comparative evidence")

    doctrines = payload.get("confirmed_current_doctrine", [])
    doctrine_ids = [row.get("doctrine_id") for row in doctrines]
    for doctrine_id, count in sorted(Counter(doctrine_ids).items()):
        if doctrine_id and count > 1:
            violations.append(f"duplicate doctrine_id: {doctrine_id}")
    for row in doctrines:
        for rel in row.get("evidence_paths", []):
            _check_path(rel, row.get("doctrine_id", "<missing>"), violations)

    actual_owner_count = sum(bool(row.get("owner_decision_required")) for row in findings)
    if payload.get("owner_decision_required_count") != actual_owner_count:
        violations.append(
            "owner_decision_required_count does not equal finding-level owner-decision flags"
        )

    gate = payload.get("c2_gate", {})
    blockers = set(gate.get("blocking_finding_ids", []))
    actual_blockers = {
        row["finding_id"] for row in findings if row.get("owner_decision_required")
    }
    if blockers != actual_blockers:
        violations.append("c2 blocking_finding_ids do not equal owner-decision findings")
    if actual_blockers and gate.get("status") != "BLOCKED_OWNER_DECISION_REQUIRED":
        violations.append("C2 cannot be ready while owner-decision findings remain")
    if not actual_blockers and gate.get("status") != "READY_WITH_DOCUMENTATION_REMEDIATIONS":
        violations.append("C2 should be documentation-ready when no owner-decision blocker remains")

    comparison = payload.get("c1_catalog_comparison", {})
    catalog_ids = {row["component_id"] for row in catalog.get("components", [])}
    unsupported = set(comparison.get("unsupported_component_ids", []))
    if comparison.get("component_count") != len(catalog_ids):
        violations.append("C1 comparison component_count does not match catalog")
    if not unsupported.issubset(catalog_ids):
        violations.append("C1 comparison names unsupported component not present in catalog")
    expected_supported = len(catalog_ids) - len(unsupported)
    if comparison.get("supported_component_count") != expected_supported:
        violations.append("C1 supported_component_count is inconsistent")

    return violations


class ArchitectureDocumentationDriftAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load_json(AUDIT)
        cls.schema = load_json(SCHEMA)
        cls.catalog = load_json(CATALOG)
        cls.validator = Draft202012Validator(cls.schema)

    def test_audit_validates_against_non_normative_schema(self):
        errors = sorted(self.validator.iter_errors(self.audit), key=lambda e: list(e.path))
        self.assertEqual(
            errors,
            [],
            "C0 audit must satisfy its design-only schema: "
            + "; ".join(error.message for error in errors),
        )

    def test_audit_is_non_authoritative_and_semantically_noop(self):
        self.assertEqual(self.audit["status"], "C0_AUDIT_COMPLETE")
        self.assertEqual(self.audit["authority"], "NONE")
        self.assertEqual(self.audit["semantic_change"], "NONE")
        self.assertEqual(self.audit["audit_scope"], "ARCHITECTURE_AND_DOCUMENTATION_DRIFT")

    def test_method_is_executable_first_and_c1_independent(self):
        method = self.audit["method"]
        self.assertEqual(method["primary_basis"], "EXECUTABLE_FIRST")
        self.assertEqual(
            method["comparison_order"],
            "EXECUTABLE_MODEL_THEN_NORMATIVE_DOCS_THEN_C1_CATALOG",
        )
        self.assertFalse(method["c1_catalog_used_as_authority"])
        self.assertEqual(
            method["independence_scope"],
            "INDEPENDENT_OF_C1_CATALOG_NOT_EXTERNAL_THIRD_PARTY",
        )

    def test_findings_and_doctrine_are_repository_evidenced(self):
        self.assertGreaterEqual(len(self.audit["findings"]), 1)
        self.assertGreaterEqual(len(self.audit["confirmed_current_doctrine"]), 1)
        self.assertEqual(audit_invariant_violations(self.audit, self.catalog), [])

    def test_c1_comparison_occurs_only_after_independent_model(self):
        comparison = self.audit["c1_catalog_comparison"]
        self.assertEqual(comparison["catalog_authority"], "NONE")
        self.assertEqual(
            comparison["comparison_stage"], "AFTER_INDEPENDENT_EXECUTABLE_MODEL"
        )
        self.assertEqual(comparison["component_count"], len(self.catalog["components"]))
        self.assertEqual(comparison["supported_component_count"], len(self.catalog["components"]))
        self.assertEqual(comparison["unsupported_component_ids"], [])

    def test_c2_ready_state_requires_zero_owner_decision_blockers(self):
        self.assertEqual(self.audit["owner_decision_required_count"], 0)
        self.assertEqual(
            self.audit["c2_gate"]["status"], "READY_WITH_DOCUMENTATION_REMEDIATIONS"
        )
        self.assertEqual(self.audit["c2_gate"]["blocking_finding_ids"], [])
        self.assertTrue(self.audit["c2_gate"]["required_remediations"])

    def test_owner_decision_mutation_fails_readiness_consistency(self):
        mutated = copy.deepcopy(self.audit)
        mutated["findings"][0]["classification"] = "CONFLICTED / OWNER DECISION REQUIRED"
        mutated["findings"][0]["owner_decision_required"] = True
        mutated["owner_decision_required_count"] = 1
        violations = audit_invariant_violations(mutated, self.catalog)
        self.assertTrue(
            any("C2 cannot be ready" in message for message in violations), violations
        )
        self.assertTrue(
            any("blocking_finding_ids" in message for message in violations), violations
        )

    def test_schema_rejects_audit_authority_or_semantic_promotion(self):
        mutated = copy.deepcopy(self.audit)
        mutated["authority"] = "AUTHORITATIVE"
        mutated["semantic_change"] = "RUNTIME_CHANGED"
        mutated["method"]["c1_catalog_used_as_authority"] = True
        errors = list(self.validator.iter_errors(mutated))
        self.assertGreaterEqual(len(errors), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
