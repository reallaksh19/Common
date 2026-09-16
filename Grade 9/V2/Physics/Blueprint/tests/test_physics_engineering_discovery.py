#!/usr/bin/env python3
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_physics_engineering_discovery import (  # noqa: E402
    VOCABULARY_REL,
    PhysicsEngineeringDiscoveryError,
    discover_candidates,
    promote_explicit_selection,
    validate_discovery_vocabulary_catalog,
)
from compile_physics_engineering_workbench import (  # noqa: E402
    PhysicsEngineeringWorkbenchError,
    compile_closure,
    digest,
    load,
    resolve_manifest,
)

REGISTRY = load("policy/physics-technical-engineering-gates.v1.json")
VOCABULARY = load(VOCABULARY_REL)


def discovery_request(query: str, suffix: str = "TEST", max_candidates: int = 6, kinds: list[str] | None = None) -> dict:
    doc = {
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "discovery_request_id": f"PHY-ENG-DISC-REQ-{suffix}",
        "query": query,
        "hints": [],
        "max_candidates": max_candidates,
    }
    if kinds is not None:
        doc["candidate_kinds"] = kinds
    return doc


def selection_for(receipt: dict, row: dict, suffix: str = "TEST", depth: str = "STANDARD") -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "selection_id": f"PHY-ENG-DISC-SEL-{suffix}",
        "discovery_id": receipt["discovery_id"],
        "discovery_receipt_digest": digest(receipt),
        "selected_scope_kind": row["scope_kind"],
        "selected_scope_refs": [row["scope_ref"]],
        "engineering_depth": depth,
        "learning_purpose": "CBSE_EXAM",
        "explicit_selection_acknowledgement": "EXACT_IDENTITY_CONFIRMED",
    }


class PhysicsEngineeringDiscoveryTests(unittest.TestCase):
    def test_discovery_is_ranked_but_non_authoritative(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "NONAUTH", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertGreater(receipt["candidate_count"], 0)
        self.assertEqual(receipt["candidates"][0]["scope_ref"], target["subtopic_id"])
        self.assertEqual(receipt["authority"], "CANDIDATE_DISCOVERY_ONLY")
        self.assertEqual(receipt["technical_authorization"], "NOT_EVALUATED")
        self.assertFalse(receipt["automatic_selection"])
        self.assertTrue(receipt["requires_explicit_exact_selection"])
        self.assertEqual(receipt["publication_authorization"], "NOT_IMPLIED")

    def test_approximate_discovery_does_not_weaken_exact_resolver(self):
        target = REGISTRY["subtopic_gates"][0]
        approximate = target["learner_title"].lower().replace("&", "and")
        request = discovery_request(approximate, "APPROX", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertIn(target["subtopic_id"], [row["scope_ref"] for row in receipt["candidates"]])

        forged_authoritative_request = {
            "schema_version": "1.0.0",
            "subject": "PHYSICS",
            "request_id": "PHY-ENG-REQ-APPROX_FORBIDDEN",
            "scope_kind": "ENGINEERING_GATE",
            "scope_refs": [approximate],
            "engineering_depth": "STANDARD",
            "learning_purpose": "CBSE_EXAM",
            "owner_decision_ref": None,
        }
        with self.assertRaises(PhysicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(forged_authoritative_request, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "PHY_ENG_SCOPE_UNMAPPED")

    def test_explicit_exact_selection_enters_existing_authoritative_path(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "PROMOTE", kinds=["ENGINEERING_GATE"])
        registry = copy.deepcopy(REGISTRY)
        receipt = discover_candidates(request, registry)
        row = next(candidate for candidate in receipt["candidates"] if candidate["scope_ref"] == target["subtopic_id"])
        selection = selection_for(receipt, row, "PROMOTE")
        engineering_request = promote_explicit_selection(request, receipt, selection, registry)
        self.assertEqual(engineering_request["scope_refs"], [target["subtopic_id"]])
        self.assertEqual(engineering_request["owner_decision_ref"], selection["selection_id"])

        manifest = resolve_manifest(engineering_request, registry)
        self.assertEqual(manifest["resolution_mode"], "GATE_IDENTITY")
        self.assertEqual(manifest["direct_gate_ids"], [target["subtopic_id"]])
        closure = compile_closure(engineering_request, manifest, registry)
        self.assertEqual(closure["technical_authorization"], "ALLOWED")

    def test_selection_must_be_in_exact_bound_candidate_set(self):
        gates = REGISTRY["subtopic_gates"]
        request = discovery_request(gates[0]["learner_title"], "BOUND", max_candidates=1, kinds=["ENGINEERING_GATE"])
        registry = copy.deepcopy(REGISTRY)
        receipt = discover_candidates(request, registry)
        selected = dict(receipt["candidates"][0])
        selection = selection_for(receipt, selected, "BOUND")
        other = next(gate for gate in gates if gate["subtopic_id"] != selected["scope_ref"])
        selection["selected_scope_refs"] = [other["subtopic_id"]]
        with self.assertRaises(PhysicsEngineeringDiscoveryError) as ctx:
            promote_explicit_selection(request, receipt, selection, registry)
        self.assertEqual(ctx.exception.code, "PHY_ENG_DISCOVERY_SELECTION_NOT_CANDIDATE")

    def test_selection_is_digest_bound_and_receipt_tamper_fails(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "DIGEST", kinds=["ENGINEERING_GATE"])
        registry = copy.deepcopy(REGISTRY)
        receipt = discover_candidates(request, registry)
        row = receipt["candidates"][0]
        selection = selection_for(receipt, row, "DIGEST")

        tampered = copy.deepcopy(receipt)
        tampered["candidates"][0]["learner_label"] += " altered"
        selection["discovery_receipt_digest"] = digest(tampered)
        with self.assertRaises(PhysicsEngineeringDiscoveryError) as ctx:
            promote_explicit_selection(request, tampered, selection, registry)
        self.assertEqual(ctx.exception.code, "PHY_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED")

    def test_registry_change_stales_discovery_receipt(self):
        target = REGISTRY["subtopic_gates"][0]
        request = discovery_request(target["learner_title"], "STALE", kinds=["ENGINEERING_GATE"])
        registry_a = copy.deepcopy(REGISTRY)
        receipt = discover_candidates(request, registry_a, VOCABULARY)
        selection = selection_for(receipt, receipt["candidates"][0], "STALE")

        registry_b = copy.deepcopy(REGISTRY)
        registry_b["subtopic_gates"][0]["learner_title"] += " revised"
        with self.assertRaises(PhysicsEngineeringDiscoveryError) as ctx:
            promote_explicit_selection(request, receipt, selection, registry_b, VOCABULARY)
        self.assertEqual(ctx.exception.code, "PHY_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED")

    def test_discovery_can_surface_held_candidate_but_authority_still_blocks(self):
        registry = copy.deepcopy(REGISTRY)
        target = registry["subtopic_gates"][0]
        target["provenance"]["source_scope"] = "HELD_SCOPE"
        request = discovery_request(target["learner_title"], "HELD", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, registry, VOCABULARY)
        row = next(candidate for candidate in receipt["candidates"] if candidate["scope_ref"] == target["subtopic_id"])
        self.assertEqual(row["source_scope"], "HELD_SCOPE")
        self.assertEqual(receipt["technical_authorization"], "NOT_EVALUATED")

        selection = selection_for(receipt, row, "HELD")
        engineering_request = promote_explicit_selection(request, receipt, selection, registry, VOCABULARY)
        manifest = resolve_manifest(engineering_request, registry)
        closure = compile_closure(engineering_request, manifest, registry)
        self.assertEqual(closure["technical_authorization"], "BLOCKED")
        state = next(item for item in closure["gate_states"] if item["gate_id"] == target["subtopic_id"])
        self.assertIn("PHY_ENG_SOURCE_SCOPE_HELD", state["failure_codes"])

    def test_bucket_candidate_requires_exact_bucket_selection_before_authority(self):
        gate = next(row for row in REGISTRY["subtopic_gates"] if row.get("linked_buckets"))
        bucket_id = gate["linked_buckets"][0]
        request = discovery_request(bucket_id.lower(), "BUCKET", kinds=["BUCKET"])
        registry = copy.deepcopy(REGISTRY)
        receipt = discover_candidates(request, registry)
        row = next(candidate for candidate in receipt["candidates"] if candidate["scope_ref"] == bucket_id)
        selection = selection_for(receipt, row, "BUCKET")
        engineering_request = promote_explicit_selection(request, receipt, selection, registry)
        self.assertEqual(engineering_request["scope_kind"], "BUCKET")
        self.assertEqual(engineering_request["scope_refs"], [bucket_id])
        manifest = resolve_manifest(engineering_request, registry)
        self.assertEqual(manifest["resolution_mode"], "REGISTRY_LINKED_BUCKET")
        self.assertTrue(manifest["direct_gate_ids"])

    def test_curated_alias_discovers_exact_gate_but_is_not_authority(self):
        request = discovery_request("prakshepya gati", "VOCAB", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertEqual(receipt["candidates"][0]["scope_ref"], "PHY-KIN-2D-PROJECTILE")
        self.assertIn("VOCABULARY_EXACT", receipt["candidates"][0]["match_basis"])
        self.assertIn("prakshepya gati", receipt["candidates"][0]["matched_vocabulary_terms"])
        self.assertEqual(receipt["technical_authorization"], "NOT_EVALUATED")

        forged_request = {
            "schema_version": "1.0.0",
            "subject": "PHYSICS",
            "request_id": "PHY-ENG-REQ-VOCAB_FORBIDDEN",
            "scope_kind": "ENGINEERING_GATE",
            "scope_refs": ["prakshepya gati"],
            "engineering_depth": "STANDARD",
            "learning_purpose": "CBSE_EXAM",
            "owner_decision_ref": None,
        }
        with self.assertRaises(PhysicsEngineeringWorkbenchError) as ctx:
            resolve_manifest(forged_request, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "PHY_ENG_SCOPE_UNMAPPED")

    def test_receipt_binds_catalog_and_generated_index(self):
        request = discovery_request("kinematics", "INDEX", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, copy.deepcopy(REGISTRY))
        self.assertEqual(receipt["schema_version"], "1.1.0")
        self.assertEqual(receipt["vocabulary_catalog_id"], VOCABULARY["catalog_id"])
        self.assertEqual(receipt["vocabulary_catalog_digest"], digest(VOCABULARY))
        self.assertTrue(receipt["discovery_index_digest"].startswith("sha256:"))
        self.assertGreaterEqual(receipt["discovery_index_entry_count"], len(REGISTRY["subtopic_gates"]))

    def test_unknown_vocabulary_target_fails_closed(self):
        catalog = copy.deepcopy(VOCABULARY)
        catalog["entries"][0]["target_scope_ref"] = "PHY-NOT-A-REAL-GATE"
        with self.assertRaises(PhysicsEngineeringDiscoveryError) as ctx:
            validate_discovery_vocabulary_catalog(catalog, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "PHY_ENG_DISCOVERY_VOCABULARY_UNKNOWN_TARGET")

    def test_duplicate_normalized_vocabulary_term_fails_closed(self):
        catalog = copy.deepcopy(VOCABULARY)
        phrase = catalog["entries"][0]["terms"][0]["phrase"]
        catalog["entries"][0]["terms"].append(
            {"phrase": phrase.upper() + "!!!", "term_class": "LEARNER_ALIAS"}
        )
        with self.assertRaises(PhysicsEngineeringDiscoveryError) as ctx:
            validate_discovery_vocabulary_catalog(catalog, copy.deepcopy(REGISTRY))
        self.assertEqual(ctx.exception.code, "PHY_ENG_DISCOVERY_VOCABULARY_DUPLICATE_TERM")

    def test_unrelated_registry_change_does_not_require_catalog_edit(self):
        registry = copy.deepcopy(REGISTRY)
        synthetic = copy.deepcopy(registry["subtopic_gates"][0])
        synthetic["subtopic_id"] = "PHY-TEST-SYNTHETIC-EXT"
        synthetic["learner_title"] = "Synthetic gate not in catalog"
        registry["subtopic_gates"].append(synthetic)
        validation = validate_discovery_vocabulary_catalog(copy.deepcopy(VOCABULARY), registry)
        self.assertEqual(validation["status"], "PASS")
        request = discovery_request("kinematics", "LOOSE_COUPLING", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, registry, copy.deepcopy(VOCABULARY))
        self.assertEqual(receipt["vocabulary_catalog_digest"], digest(VOCABULARY))
        self.assertEqual(receipt["registry_digest"], digest(registry))

    def test_vocabulary_mutation_stales_bound_selection(self):
        registry = copy.deepcopy(REGISTRY)
        catalog_a = copy.deepcopy(VOCABULARY)
        request = discovery_request("projectile motion", "VOCAB_STALE", kinds=["ENGINEERING_GATE"])
        receipt = discover_candidates(request, registry, catalog_a)
        row = receipt["candidates"][0]
        selection = selection_for(receipt, row, "VOCAB_STALE")

        catalog_b = copy.deepcopy(catalog_a)
        target = next(entry for entry in catalog_b["entries"] if entry["target_scope_ref"] == "PHY-KIN-2D-PROJECTILE")
        target["terms"].append({"phrase": "projectile 2d flight trajectory", "term_class": "COMPETITION_TERM"})
        with self.assertRaises(PhysicsEngineeringDiscoveryError) as ctx:
            promote_explicit_selection(request, receipt, selection, registry, catalog_b)
        self.assertEqual(ctx.exception.code, "PHY_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
