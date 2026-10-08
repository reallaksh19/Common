"""C2 pre-product ESC-4 golden acceptance gate.

Executes real V3.2 DELP and legacy successor source. Product integration is
deliberately RED; these tests MUST NOT certify a handover consumer or Owner.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPTS = ROOT / "skills/engineering-pr-delivery-v3.2/scripts"
sys.path.insert(0, str(SCRIPTS))
import delp_projection_v32 as delp  # noqa: E402
import handover_context as legacy  # noqa: E402
import qualification_observation_v32 as qualifier  # noqa: E402
import pr_responsibility_view_v32 as read_view  # noqa: E402

GOLDEN = HERE / "793-handover-golden-v1.json"
GRAPH = HERE / "718-proposal-v2.json"
C0 = HERE / "718-golden-fixtures-v1.json"


class HandoverPrecommit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oracle = json.loads(GOLDEN.read_text(encoding="utf-8"))
        cls.graph = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.legacy_oracle = json.loads(C0.read_text(encoding="utf-8"))
        cls.cases = {row["id"]: row for row in cls.oracle["precommitted_cases"]}

    def test_01_source_identity_and_claim_are_released(self):
        self.assertEqual([f"H{i:02d}" for i in range(1, 11)], list(self.cases))
        self.assertEqual("ESC-4", self.oracle["claim"])
        g = self.graph
        self.assertEqual("RELEASEABLE", delp.decomposition_report(g)["release_state"])
        self.assertEqual(self.oracle["baseline"]["released_proposal_digest"], g["programme"]["decomposition_proposal"]["released_proposal_digest"])
        self.assertEqual(self.oracle["baseline"]["undecomposed_reserve_after_C1"], g["nodes"][0]["reserve_weight"])
        leaf = next(n for n in g["nodes"] if n.get("responsibility_id") == "R-RECONSTRUCTION")
        self.assertEqual(self.oracle["child"], leaf["ref"])
        self.assertEqual(["ESC-4"], leaf["owns_claims"])
        self.assertEqual("MATCH", self.cases["H01"]["expected"]["proposal_binding"])
        self.assertEqual("NOT_IMPLEMENTED", self.cases["H01"]["expected"]["handover_completeness"])

    def test_02_moved_candidate_invalidates_source_basis(self):
        original = delp.project(self.graph, [], {})
        changed = delp.project(self.graph, [], {self.oracle["child"]: {
            "pr_state": "OPEN", "candidate_sha": "a"*40
        }})
        self.assertNotEqual(original["input_digest"], changed["input_digest"])
        self.assertEqual("RECONCILE", self.cases["H02"]["expected"]["currentness"])

    def test_03_plan_mutation_invalidates_release(self):
        changed = copy.deepcopy(self.graph)
        leaf = next(n for n in changed["nodes"] if n.get("responsibility_id") == "R-RECONSTRUCTION")
        leaf["owns_claims"] = ["ESC-5"]
        report = delp.decomposition_report(changed)
        self.assertEqual("NOT_RELEASEABLE", report["release_state"])
        self.assertEqual("RECONCILE", self.cases["H03"]["expected"]["currentness"])

    def test_04_original_owner_chat_not_authenticated_by_archive(self):
        rows = self.legacy_oracle["owner_intents"]
        self.assertTrue(rows)
        self.assertTrue(all(x["original_source_ref"] is None and
                            x["original_source_status"] == "UNRESOLVED_CHAT_MESSAGE_LINK" for x in rows))
        self.assertEqual("UNKNOWN", self.cases["H04"]["expected"]["owner_source"])

    def test_05_merged_material_without_facts_has_zero_progress(self):
        g = self.graph
        observations = {
            "Common#720": {"pr_state": "MERGED", "candidate_sha": "b3dfba3becf829d3a4e21d6eaa54983f05317b65"},
            "Common#724": {"pr_state": "MERGED", "candidate_sha": "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414"},
        }
        view = delp.project(g, [], observations)
        for ref in observations:
            self.assertEqual(0, view["nodes"][ref]["progress"]["P"])
            self.assertEqual(0, view["nodes"][ref]["progress"]["E"])
            self.assertNotEqual("COMPLETE", view["nodes"][ref]["state"])
        self.assertEqual("UNREPORTED", self.cases["H05"]["expected"]["evidence"])

    def test_06_provider_merged_overrides_stale_draft_description(self):
        expected = self.cases["H06"]["expected"]
        # The real issue/PR renderer detects managed-content drift; the real
        # legacy successor only uses the explicitly supplied provider state,
        # not the outdated human-controlled DRAFT string.
        source = read_view.START + "\\n- Candidate: MERGED\\n" + read_view.END
        observed = read_view.START + "\\n- Candidate: DRAFT\\n" + read_view.END
        self.assertEqual(expected["title_integrity"],
                         read_view.inspect_managed_block(observed, source, pr=True))
        ctx = {"target": {"state": "MERGED", "provider_ref": "Common#740"},
               "reality_context": {"material": {}, "execution": {}},
               "accumulated_learning": {"what_remains_uncertain": ["stale draft title"]}}
        successor = legacy._successor_entry(ctx, 1)
        self.assertEqual("TERMINAL_TARGET_REQUIRES_RECONCILIATION",
                         successor["challenge_basis"]["freshness"])
        self.assertEqual(expected["provider_lifecycle"], successor["challenge_basis"]["target_state"])
        self.assertIn("PRODUCTION_MUTATION", successor["forbidden_actions"])
        self.assertEqual(expected["handover_state"], "RECONCILE")

    def test_07_forged_green_run_without_required_case_remains_unproven(self):
        sha = "b" * 40
        case = "tests.case.TestBounded.test_required"
        contract = {
            "schema": qualifier.INPUT_SCHEMA, "repository": "reallaksh19/Common",
            "responsibility": "Common#793", "pull_number": 798,
            "candidate_sha": sha, "requirements": [{
                "id": "H07-REQUIRED", "kind": "UNITTEST", "case_id": case,
                "job_name": "required source", "step_name": "Execute required case"
            }]
        }
        class GreenButWrongCase:
            def get_pull(self, repo, number):
                return {"head": {"sha": sha}}
            def list_runs(self, repo, head):
                return [{"head_sha": sha, "status": "completed", "conclusion": "success", "id": 17}]
            def list_jobs(self, repo, run_id):
                return [{"name": "required source", "status": "completed",
                         "conclusion": "success", "id": 19, "steps": [
                             {"name": "Execute required case", "status": "completed",
                              "conclusion": "success"}]}]
            def get_job_log(self, repo, job_id):
                return "test_wrong_case (tests.case.TestBounded.test_wrong_case) ... ok"
        actual = qualifier.assess(contract, GreenButWrongCase())
        self.assertEqual(self.cases["H07"]["expected"]["qualification"], actual["overall"])
        self.assertEqual("UNPROVEN", actual["requirements"][0]["status"])
        self.assertFalse(self.cases["H07"]["expected"]["admit_execution"])

    def test_08_legacy_successor_source_does_not_bind_delp_digest(self):
        ctx = {
            "target": {"state": "DRAFT", "provider_ref": "Common#794"},
            "reality_context": {"material": {"head": "6f2d9f4dca3655605542a4e4326f2d533b3b8e3c"},
                                "execution": {"branch": "v32/793-r-reconstruction-source-bind"}},
            "accumulated_learning": {"reconstruction_context": {
                "original_intent": {"source_ref": None}, "primary_conversation_refs": []},
                "what_remains_uncertain": ["no accepted facts"],
                "attempted_and_rejected": ["assume draft title is live state"]},
        }
        handover = legacy._successor_entry(ctx, 0)
        # Source reality check: the inherited custody entry has no accepted
        # DELP plan/input digest comparison. Product C4 MUST add it.
        self.assertEqual("RECONSTRUCT_PLAN_ONLY", handover["mode"])
        self.assertNotIn("delp_input_digest", handover)
        self.assertEqual("FAIL_CLOSED_UNIMPLEMENTED", self.cases["H08"]["expected"]["integration_gate"])

    def test_09_real_source_projection_and_successor_do_not_grant_authority(self):
        e = self.cases["H09"]["expected"]
        original = copy.deepcopy(self.graph)
        projected = delp.project(self.graph, [], {})
        admission = delp.admit(projected, self.oracle["child"], command="continue")
        handover_input = {
            "target": {"state": "DRAFT", "provider_ref": "Common#794"},
            "reality_context": {"material": {}, "execution": {}},
            "accumulated_learning": {"first_successor_action": "Review source"}
        }
        snapshot = copy.deepcopy(handover_input)
        successor = legacy._successor_entry(handover_input, 1)
        self.assertEqual(original, self.graph, "pure DELP mutated graph")
        self.assertEqual(snapshot, handover_input, "successor source mutated context")
        self.assertEqual([], admission["authority_effects"])
        self.assertEqual("OWNER_EXPLICIT_EXECUTION_ADMISSION", successor["execution_admission"])
        for forbidden in ("PR_CREATION", "PRODUCTION_MUTATION", "TASK_EXECUTION"):
            self.assertIn(forbidden, successor["forbidden_actions"])
        self.assertEqual(0, e["github_writes"])
        self.assertEqual("NOT_GRANTED", e["owner_merge_authority"])
        self.assertEqual("NOT_TRANSFERRED", e["handover_custody"])

    def test_10_real_parent_child_pr_entry_stays_reconstruction_only(self):
        e = self.cases["H10"]["expected"]
        expected = [("PARENT", "Common#718"), ("CHILD", "Common#793"), ("PR", "Common#798")]
        self.assertEqual(e["entry_views"], [k for k, _ in expected])
        for kind, ref in expected:
            ctx = {
                "target": {"state": "DRAFT" if kind == "PR" else "OPEN", "provider_ref": ref},
                "reality_context": {"material": {}, "execution": {}},
                "accumulated_learning": {"what_remains_uncertain": ["provider check not performed"]},
            }
            entry = legacy._successor_entry(ctx, 1)
            self.assertEqual("RECONSTRUCT_PLAN_ONLY", entry["mode"])
            self.assertEqual("OWNER_EXPLICIT_EXECUTION_ADMISSION", entry["execution_admission"])
            self.assertNotIn("delp_input_digest", entry)
            self.assertTrue(entry["successor_reconstruction_challenge"])
            self.assertIn("TASK_EXECUTION", entry["forbidden_actions"])
        self.assertTrue(e["same_source_digest_required"])
        self.assertTrue(e["current_provider_recheck_required"])
        self.assertEqual("NOT_YET_TESTED", e["acceptance"])


if __name__ == "__main__":
    unittest.main()
