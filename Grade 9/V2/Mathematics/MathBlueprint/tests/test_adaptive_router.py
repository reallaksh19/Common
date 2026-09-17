#!/usr/bin/env python3
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from blueprint_common import seal_ground_truth, seal_learning_run
from route_math_learning_run import (
    _build_bundles,
    apply_routing_plan,
    build_routing_plan,
    profile_decision,
    validate_routing_spec,
)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evidence(eid, etype, availability="PRESENT", *, conflicts=None):
    return {
        "evidence_id": eid,
        "evidence_type": etype,
        "authority_class": "AUTHORITATIVE_SOURCE" if etype in {"SYLLABUS", "AUTHORITATIVE_SOURCE"} else "ORIGINAL_EVIDENCE",
        "availability": availability,
        "ref": None if availability == "ABSENT" else f"fixture/{eid}",
        "digest": None if availability == "ABSENT" else (eid.encode().hex() + "0" * 64)[:64],
        "source_locator": "fixture",
        "scope_refs": ["TOPIC"],
        "notes": None,
        "conflict_refs": list(conflicts or []),
    }


def make_manifest(*items):
    return seal_ground_truth({
        "manifest_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "evidence_items": list(items),
        "manifest_digest": "",
    })


def make_run(manifest):
    return seal_learning_run({
        "run_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "ground_truth_ref": manifest["manifest_id"],
        "ground_truth_digest": manifest["manifest_digest"],
        "control_plane": {
            "learner_prior_percent": 50,
            "learning_purpose": "CONSOLIDATION",
            "product_mode": "PRACTICE",
            "owner_override_refs": [],
        },
        "current_state": "GT_READY",
        "state_history": [{"sequence": 0, "state": "GT_READY", "reason_code": "TEST"}],
        "routing_ref": None,
        "bundles": [],
        "publication_ref": None,
        "audit_ref": None,
        "run_digest": "",
    })


def dimension(score, reason, refs=None):
    return {"score": score, "reason_codes": [reason], "evidence_refs": list(refs or [])}


class AdaptiveRouterTests(unittest.TestCase):
    def test_three_routing_goldens(self):
        paths = sorted((ROOT / "golden" / "routing").glob("*.json"))
        self.assertEqual(len(paths), 3)
        for path in paths:
            fixture = load(path)
            got = profile_decision(fixture["subtopic"])
            exp = fixture["expected"]
            self.assertEqual(got["system_action"], exp["system_action"], path.name)
            self.assertEqual(got["eligible_roles"], exp["eligible_roles"], path.name)
            self.assertEqual(got["final_action"], exp["final_action"], path.name)

    def test_strong_semantic_and_question_evidence_still_core1_first(self):
        g = load(ROOT / "golden" / "routing" / "01-core1-first.json")
        d = profile_decision(g["subtopic"])
        self.assertEqual(d["system_action"], "CORE1_FIRST")
        self.assertEqual(d["eligible_roles"], ["CORE1", "CORE2"])

    def test_missing_syllabus_rich_questions_core2_first(self):
        g = load(ROOT / "golden" / "routing" / "02-core2-first.json")
        d = profile_decision(g["subtopic"])
        self.assertEqual(d["system_action"], "CORE2_FIRST")
        self.assertEqual(d["first_role"], "CORE2")

    def test_conflict_is_preserved_as_block(self):
        g = load(ROOT / "golden" / "routing" / "03-block-conflict.json")
        d = profile_decision(g["subtopic"])
        self.assertEqual(d["system_action"], "BLOCK_CONFLICT")
        self.assertIsNone(d["first_role"])
        self.assertEqual(d["conflict_refs"], ["CONFLICT-ANSWER-01"])

    def test_soft_override_cannot_force_ineligible_role(self):
        row = load(ROOT / "golden" / "routing" / "02-core2-first.json")["subtopic"]
        d = profile_decision(row, override={
            "override_id": "OVR-soft",
            "target_type": "FIRST_ROLE",
            "target_ref": row["subtopic_ref"],
            "mode": "SOFT",
            "requested_action": "CORE1_FIRST",
            "owner_reason": "Prefer semantic start",
            "ground_truth_changed": False,
        })
        self.assertEqual(d["system_action"], "CORE2_FIRST")
        self.assertEqual(d["final_action"], "CORE2_FIRST")
        self.assertIsNone(d["applied_override_ref"])
        self.assertIn("SOFT_OWNER_OVERRIDE_NOT_ADMISSIBLE", d["reason_codes"])

    def test_hard_override_changes_action_not_system_finding(self):
        row = load(ROOT / "golden" / "routing" / "03-block-conflict.json")["subtopic"]
        d = profile_decision(row, override={
            "override_id": "OVR-hard",
            "target_type": "FIRST_ROLE",
            "target_ref": row["subtopic_ref"],
            "mode": "HARD",
            "requested_action": "CORE1_FIRST",
            "owner_reason": "Owner accepts risk and wants semantic pass first",
            "ground_truth_changed": False,
        })
        self.assertEqual(d["system_action"], "BLOCK_CONFLICT")
        self.assertEqual(d["final_action"], "CORE1_FIRST")
        self.assertEqual(d["first_role"], "CORE1")
        self.assertEqual(d["applied_override_ref"], "OVR-hard")

    def test_bundle_transport_limit_chunks_without_losing_subtopics(self):
        decisions = []
        for i in range(7):
            decisions.append({
                "subtopic_ref": f"S{i}", "display_name": f"S{i}", "sequence": i,
                "coherence_group": "G", "semantic_strength": 4, "assessment_strength": 1,
                "eligible_roles": ["CORE1"], "system_action": "CORE1_FIRST", "final_action": "CORE1_FIRST",
                "first_role": "CORE1", "reason_codes": ["STRONG_SEMANTIC_AUTHORITY"],
                "evidence_profile_digest": "1" * 64, "applied_override_ref": None, "override_mode": None,
                "unresolved_issue_refs": [], "conflict_refs": []
            })
        bundles = _build_bundles(decisions)
        self.assertEqual([len(x["subtopic_refs"]) for x in bundles], [3, 3, 1])
        self.assertEqual([s for b in bundles for s in b["subtopic_refs"]], [f"S{i}" for i in range(7)])

    def test_routing_spec_cannot_use_absent_evidence_as_support(self):
        absent = evidence("GT-SYLLABUS-aaaaaaaaaaaaaaaa", "SYLLABUS", "ABSENT")
        q = evidence("GT-QUESTION_CORPUS-bbbbbbbbbbbbbbbb", "QUESTION_CORPUS")
        manifest = make_manifest(absent, q)
        row = {
            "subtopic_ref": "S", "display_name": "S", "sequence": 0, "coherence_group": "G",
            "scope_authority": dimension(3, "CLAIM", [absent["evidence_id"]]),
            "semantic_source_strength": dimension(0, "NONE"),
            "question_evidence": dimension(4, "RICH", [q["evidence_id"]]),
            "question_resolution": dimension(4, "RESOLVED", [q["evidence_id"]]),
            "uncertainty": dimension(0, "LOW"),
            "conflict_index": dimension(0, "NONE"),
            "unresolved_issue_refs": [], "conflict_refs": []
        }
        spec = {"schema_version": "1.0.0", "subject": "MATHEMATICS", "ground_truth_ref": manifest["manifest_id"], "ground_truth_digest": manifest["manifest_digest"], "candidate_subtopics": [row]}
        with self.assertRaisesRegex(ValueError, "ROUTING_ABSENT_EVIDENCE_REFERENCED_AS_SUPPORT"):
            validate_routing_spec(spec, manifest)

    def test_apply_routing_preserves_run_identity(self):
        syllabus = evidence("GT-SYLLABUS-aaaaaaaaaaaaaaaa", "SYLLABUS")
        source = evidence("GT-AUTHORITATIVE_SOURCE-bbbbbbbbbbbbbbbb", "AUTHORITATIVE_SOURCE")
        q = evidence("GT-QUESTION_CORPUS-cccccccccccccccc", "QUESTION_CORPUS")
        manifest = make_manifest(syllabus, source, q)
        run = make_run(manifest)
        row = {
            "subtopic_ref": "S", "display_name": "S", "sequence": 0, "coherence_group": "G",
            "scope_authority": dimension(4, "SCOPE", [syllabus["evidence_id"]]),
            "semantic_source_strength": dimension(4, "SOURCE", [source["evidence_id"]]),
            "question_evidence": dimension(4, "QUESTIONS", [q["evidence_id"]]),
            "question_resolution": dimension(4, "RESOLVED", [q["evidence_id"]]),
            "uncertainty": dimension(0, "NONE"), "conflict_index": dimension(0, "NONE"),
            "unresolved_issue_refs": [], "conflict_refs": []
        }
        spec = {"schema_version": "1.0.0", "subject": "MATHEMATICS", "ground_truth_ref": manifest["manifest_id"], "ground_truth_digest": manifest["manifest_digest"], "candidate_subtopics": [row]}
        plan = build_routing_plan(manifest, run, spec)
        updated = apply_routing_plan(run, plan)
        self.assertEqual(updated["run_id"], run["run_id"])
        self.assertEqual(updated["current_state"], "ROUTED")
        self.assertEqual(updated["bundles"][0]["first_role"], "CORE1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
