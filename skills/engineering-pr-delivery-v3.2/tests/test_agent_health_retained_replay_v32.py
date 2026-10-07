from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import agent_intervention_v32 as M3
import agent_quality_metrics_v32 as M1
import agent_quality_trajectory_v32 as M2
import delp_projection_v32 as DELP

SHA = "a" * 40
BASE_SHA = "9" * 40
BASIS_REF = "Common#689#agent-quality-benchmark-v1"
BASIS_DIGEST = "sha256:" + "b" * 64


def graph():
    return {
        "schema": DELP.GRAPH_SCHEMA,
        "programme": {
            "id": "V32-AGENT-HEALTH-REPLAY",
            "root": "Common#689",
            "health_policy": {"mode": "ADVISORY"},
        },
        "nodes": [
            {"ref": "Common#689", "kind": "ROOT"},
            {
                "ref": "Common#713",
                "kind": "LEAF",
                "parent": "Common#689",
                "weight": 1,
                "primary_pr": "Common#714",
                "units": [
                    {"id": "R1", "weight": 34},
                    {"id": "R2", "weight": 33},
                    {"id": "R3", "weight": 33},
                ],
            },
        ],
    }


def ledger():
    facts = {
        "schema": DELP.FACTS_SCHEMA,
        "responsibility": {"issue": "Common#713"},
        "material": {"pr": "Common#714", "candidate_sha": SHA},
        "units": [
            {"id": "R1", "state": "COMPLETE", "result": "VERIFIED", "evidence_refs": ["Common#713#r1"]},
            {"id": "R2", "state": "COMPLETE", "result": "VERIFIED", "evidence_refs": ["Common#713#r2"]},
        ],
        "next": {"unit": "R3", "action": "continue"},
    }
    return [{"source": "Common#713#checkpoint", "order": 1, "facts": facts}]


def material_observation():
    return {
        "candidate_sha": SHA,
        "pr_state": "OPEN",
        "base_sha": BASE_SHA,
        "behind_by": 0,
        "additions": 40,
        "deletions": 5,
        "since_checkpoint": {"additions": 40, "deletions": 5, "commits": 1},
        "liveness": "ACTIVE",
        "interruptions": {"coverage_from": "2026-10-07T00:00:00Z", "losses": []},
    }


def observation(oid, kind, disposition, *, critical=False, covered=None):
    row = {
        "id": oid,
        "class": kind,
        "critical": critical,
        "disposition": disposition,
        "repairs": 0,
        "evidence_refs": [BASIS_REF, f"Common#713#{oid}"],
    }
    if covered is not None:
        row["impact_expected"] = 1
        row["impact_covered"] = covered
    return row


def quality(window_id, mode):
    if mode == "good":
        rows = [
            observation("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            observation("M2", "MUTATION", "DETECTED", critical=True, covered=1),
            observation("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            observation("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        ]
    elif mode == "bad":
        rows = [
            observation("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            observation("M2", "MUTATION", "MISSED", critical=True, covered=0),
            observation("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            observation("C2", "CLEAN_CONTROL", "FALSE_POSITIVE"),
        ]
    elif mode == "unknown":
        rows = [
            observation("M1", "MUTATION", "DETECTED", critical=True, covered=1),
            observation("U1", "MUTATION", "UNKNOWN", critical=True),
            observation("C1", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
            observation("C2", "CLEAN_CONTROL", "CLEAN_ACCEPTED"),
        ]
    else:
        raise AssertionError(mode)
    return M1.evaluate({"schema": M1.WINDOW_SCHEMA, "window_id": window_id, "observations": rows})


def chain(*results):
    trajectory = M2.evaluate({
        "schema": M2.INPUT_SCHEMA,
        "trajectory_id": "RETAINED-TRAJECTORY",
        "comparison_basis": {"ref": BASIS_REF, "digest": BASIS_DIGEST},
        "windows": [{"sequence": i + 1, "result": result} for i, result in enumerate(results)],
    })
    intervention = M3.evaluate({"schema": M3.INPUT_SCHEMA, "trajectory": trajectory})
    return results[-1], trajectory, intervention


def project(current, trajectory, intervention):
    obs = {
        **material_observation(),
        "agent_quality": {
            "quality_result": current,
            "trajectory_result": trajectory,
            "intervention_result": intervention,
        },
    }
    return DELP.project(graph(), ledger(), {"Common#713": obs})


class AgentHealthRetainedReplay(unittest.TestCase):
    def test_clean_control_chain_is_stable_none_and_fully_traceable(self):
        current, trajectory, intervention = chain(quality("C1", "good"), quality("C2", "good"))
        leaf = project(current, trajectory, intervention)["nodes"]["Common#713"]
        model = leaf["agent_health"]
        self.assertEqual(("STABLE", "NONE"), (trajectory["trajectory"], intervention["recommendation"]))
        self.assertEqual({"AVAILABLE"}, {model[k]["status"] for k in ("operational", "quality", "trajectory", "intervention")})
        self.assertEqual("HEALTHY", model["operational"]["verdict"])
        self.assertEqual(current["window_id"], model["quality"]["window_id"])
        self.assertEqual(trajectory["trajectory_digest"], model["trajectory"]["trajectory_digest"])
        self.assertEqual(intervention["recommendation_digest"], model["intervention"]["recommendation_digest"])

    def test_injected_semantic_defect_is_detected_and_advisory(self):
        current, trajectory, intervention = chain(quality("D1", "good"), quality("D2", "bad"))
        model = project(current, trajectory, intervention)["nodes"]["Common#713"]["agent_health"]
        self.assertEqual("DEGRADING", trajectory["trajectory"])
        self.assertEqual("CHECKPOINT", intervention["recommendation"])
        self.assertEqual("AVAILABLE", model["intervention"]["status"])
        self.assertTrue(model["advisory"])
        self.assertEqual(DELP._AGENT_HEALTH_AUTHORITY, model["authority"])

    def test_persistent_critical_unknown_is_explicit_and_requires_reconstruction(self):
        current, trajectory, intervention = chain(quality("U1", "unknown"), quality("U2", "unknown"))
        model = project(current, trajectory, intervention)["nodes"]["Common#713"]["agent_health"]
        self.assertEqual("STABLE", trajectory["trajectory"])
        self.assertGreater(current["metrics"]["critical_unknown_count"], 0)
        self.assertEqual("FRESH_RECONSTRUCTION", intervention["recommendation"])
        self.assertEqual([], current["authority_effects"])
        self.assertEqual("AVAILABLE", model["quality"]["status"])

    def test_reversal_remains_mixed_and_requires_fresh_self_review(self):
        current, trajectory, intervention = chain(
            quality("R1", "good"), quality("R2", "bad"), quality("R3", "good")
        )
        model = project(current, trajectory, intervention)["nodes"]["Common#713"]["agent_health"]
        self.assertEqual(("INSUFFICIENT_DATA", "MIXED_SIGNAL"), (trajectory["trajectory"], trajectory["reason"]))
        self.assertEqual("FRESH_SELF_REVIEW", intervention["recommendation"])
        self.assertEqual("AVAILABLE", model["trajectory"]["status"])

    def test_tampered_or_mismatched_provenance_is_invalid_not_authority(self):
        current, trajectory, intervention = chain(quality("T1", "good"), quality("T2", "good"))

        stale = copy.deepcopy(trajectory)
        stale["trajectory_digest"] = "sha256:" + "0" * 64
        model = project(current, stale, intervention)["nodes"]["Common#713"]["agent_health"]
        self.assertEqual(("INVALID", "INVALID"), (model["trajectory"]["status"], model["intervention"]["status"]))

        forged = copy.deepcopy(intervention)
        forged["recommendation"] = "CHECKPOINT"
        model = project(current, trajectory, forged)["nodes"]["Common#713"]["agent_health"]
        self.assertEqual("INVALID", model["intervention"]["status"])

        mismatch = quality("OTHER", "good")
        model = project(mismatch, trajectory, intervention)["nodes"]["Common#713"]["agent_health"]
        self.assertEqual("INVALID", model["trajectory"]["status"])

    def test_agent_quality_never_moves_delp_control_or_authority(self):
        current, trajectory, intervention = chain(quality("A1", "bad"), quality("A2", "good"))
        base = DELP.project(graph(), ledger(), {"Common#713": material_observation()})
        rich = project(current, trajectory, intervention)
        a, b = base["nodes"]["Common#713"], rich["nodes"]["Common#713"]

        for key in (
            "lifecycle", "state", "light", "progress", "active_unit", "next", "evidence",
            "frontier", "dependencies", "health", "material", "title_prefix",
        ):
            self.assertEqual(a.get(key), b.get(key), key)
        self.assertNotEqual(base["input_digest"], rich["input_digest"])
        self.assertEqual(DELP.admit(base, "Common#713")["action"], DELP.admit(rich, "Common#713")["action"])
        self.assertEqual([], current["authority_effects"])
        self.assertEqual([], trajectory["authority_effects"])
        self.assertEqual([], intervention["authority_effects"])
        self.assertTrue(rich["nodes"]["Common#713"]["agent_health"]["advisory"])


if __name__ == "__main__":
    unittest.main()
