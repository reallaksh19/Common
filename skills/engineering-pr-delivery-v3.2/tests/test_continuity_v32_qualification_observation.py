"""Independent R-PROOF acceptance cases — execute via hosted test_continuity_v32*.py.

This is deliberately red-first against the declared non-functional module stub.
All positive evidence is supplied by a fake *read-only provider transport*; no
caller-supplied progress, check conclusion or prose TASK_EVIDENCE grants proof.
"""
from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "qualification_observation_v32.py"
SPEC = importlib.util.spec_from_file_location("qualification_observation_v32", SCRIPT)
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

HEAD = "a" * 40
BLOB = "b" * 40
OLD = "c" * 40
REPO = "reallaksh19/Common"
TEST_ID = "test_continuity_v32_replay.RetainedReplay.test_source_bound_behavior"
TEST_LINE = f"test_source_bound_behavior ({TEST_ID}) ... ok"
ARTIFACT = "skills/engineering-pr-delivery-v3.2/scripts/delp_projection_v32.py"


def contract():
    return {
        "schema": M.INPUT_SCHEMA,
        "repository": REPO,
        "responsibility": "Common#724",
        "pull_number": 715,
        "candidate_sha": HEAD,
        "requirements": [
            {"id": "T-RUN", "kind": "UNITTEST", "case_id": TEST_ID,
             "job_name": "validate-v3-2-candidate", "step_name": "Run V3.2 continuity regressions"},
            {"id": "B-SHIP", "kind": "BLOB", "path": ARTIFACT, "expected_blob_sha": BLOB},
        ],
    }


class Provider:
    """Data returned by external authenticated provider endpoints, never from the contract."""
    def __init__(self):
        self.pull = {"number": 715, "head": {"sha": HEAD}, "state": "open"}
        self.runs = [{"id": 9001, "head_sha": HEAD, "status": "completed", "conclusion": "success"}]
        self.jobs = {9001: [{"id": 9002, "name": "validate-v3-2-candidate", "status": "completed",
                             "conclusion": "success", "steps": [
                                 {"name": "Run V3.2 continuity regressions",
                                  "status": "completed", "conclusion": "success"}]}]}
        self.logs = {9002: "2026-10-08T00:00:00Z " + TEST_LINE + "\nRan 1 test in 0.01s\nOK\n"}
        self.tree = {"truncated": False, "tree": [{"path": ARTIFACT, "type": "blob", "sha": BLOB}]}
        self.calls = []

    def get_pull(self, repo, number):
        self.calls.append(("get_pull", repo, number))
        return copy.deepcopy(self.pull)

    def list_runs(self, repo, sha):
        self.calls.append(("list_runs", repo, sha))
        return copy.deepcopy(self.runs)

    def list_jobs(self, repo, run_id):
        self.calls.append(("list_jobs", repo, run_id))
        return copy.deepcopy(self.jobs.get(run_id, []))

    def get_job_log(self, repo, job_id):
        self.calls.append(("get_job_log", repo, job_id))
        return self.logs.get(job_id)

    def get_tree(self, repo, sha):
        self.calls.append(("get_tree", repo, sha))
        return copy.deepcopy(self.tree)


class ContractObservationTests(unittest.TestCase):
    def check(self, plan=None, reader=None):
        return M.assess(plan or contract(), reader or Provider())

    def requirement(self, output, rid):
        return next(x for x in output["requirements"] if x["id"] == rid)

    def test_full_source_bound_clean_control_is_proven_advisory_only(self):
        provider = Provider()
        output = self.check(reader=provider)
        self.assertEqual("PROVEN", output["overall"], output)
        self.assertEqual(M.AUTHORITY, output["authority"])
        self.assertEqual(HEAD, output["observed_candidate_sha"])
        self.assertEqual({"PROVEN"}, {x["status"] for x in output["requirements"]})
        self.assertTrue(self.requirement(output, "T-RUN")["evidence_refs"])
        self.assertTrue(self.requirement(output, "B-SHIP")["evidence_refs"])
        self.assertIn(("get_pull", REPO, 715), provider.calls)
        self.assertIn(("get_tree", REPO, HEAD), provider.calls)
        self.assertNotIn("progress", output)
        self.assertNotIn("merge_authority", output)

    def test_moved_pr_head_invalidates_all_old_proof(self):
        provider = Provider()
        provider.pull["head"]["sha"] = OLD
        output = self.check(reader=provider)
        self.assertEqual("UNPROVEN", output["overall"], output)
        self.assertEqual(OLD, output["observed_candidate_sha"])
        self.assertTrue(all(x["status"] != "PROVEN" for x in output["requirements"]))
        self.assertNotIn(("get_tree", REPO, HEAD), provider.calls)

    def test_named_test_missing_from_green_job_is_not_executed(self):
        provider = Provider()
        provider.logs[9002] = "2026-10-08T00:00:00Z test_unrelated (other.Tests.test_unrelated) ... ok\nOK"
        output = self.check(reader=provider)
        self.assertEqual("UNPROVEN", self.requirement(output, "T-RUN")["status"])
        self.assertNotEqual("PROVEN", output["overall"])

    def test_green_job_step_without_named_test_is_not_proof(self):
        provider = Provider()
        provider.logs[9002] = "2026-10-08T00:00:00Z Run V3.2 continuity regressions\nRan 0 tests in 0.000s\nOK\n"
        self.assertEqual("UNPROVEN", self.requirement(self.check(reader=provider), "T-RUN")["status"])

    def test_unrelated_green_job_cannot_certify_expected_method(self):
        provider = Provider()
        provider.jobs[9001][0]["name"] = "validate-other"
        self.assertNotEqual("PROVEN", self.requirement(self.check(reader=provider), "T-RUN")["status"])

    def test_unavailable_raw_job_log_is_unknown_not_pass(self):
        provider = Provider()
        provider.logs[9002] = None
        output = self.check(reader=provider)
        self.assertEqual("UNKNOWN", self.requirement(output, "T-RUN")["status"])
        self.assertEqual("UNKNOWN", output["overall"])

    def test_failed_job_does_not_count_even_if_text_mentions_case(self):
        provider = Provider()
        provider.jobs[9001][0]["conclusion"] = "failure"
        self.assertEqual("UNPROVEN", self.requirement(self.check(reader=provider), "T-RUN")["status"])

    def test_echoed_source_command_is_not_execution_result(self):
        provider = Provider()
        provider.logs[9002] = "2026-10-08T00:00:00Z echo '" + TEST_LINE + "'\n"
        self.assertEqual("UNPROVEN", self.requirement(self.check(reader=provider), "T-RUN")["status"])

    def test_job_run_on_different_head_does_not_qualify_candidate(self):
        provider = Provider()
        provider.runs[0]["head_sha"] = OLD
        self.assertNotEqual("PROVEN", self.requirement(self.check(reader=provider), "T-RUN")["status"])

    def test_same_named_file_with_old_blob_does_not_count_as_shipped(self):
        provider = Provider()
        provider.tree["tree"][0]["sha"] = OLD
        output = self.check(reader=provider)
        self.assertEqual("UNPROVEN", self.requirement(output, "B-SHIP")["status"])
        self.assertEqual("UNPROVEN", output["overall"])

    def test_missing_expected_surface_is_unproven(self):
        provider = Provider()
        provider.tree["tree"] = []
        self.assertEqual("UNPROVEN", self.requirement(self.check(reader=provider), "B-SHIP")["status"])

    def test_truncated_git_tree_preserves_unknown(self):
        provider = Provider()
        provider.tree["truncated"] = True
        output = self.check(reader=provider)
        self.assertEqual("UNKNOWN", self.requirement(output, "B-SHIP")["status"])
        self.assertEqual("UNKNOWN", output["overall"])

    def test_provider_failure_preserves_unknown_not_false_pass(self):
        provider = Provider()
        provider.pull = None
        output = self.check(reader=provider)
        self.assertEqual("UNKNOWN", output["overall"])
        self.assertFalse(any(x["status"] == "PROVEN" for x in output["requirements"]))

    def test_wrong_contract_candidate_sha_is_rejected(self):
        plan = contract()
        plan["candidate_sha"] = "not-an-exact-commit"
        with self.assertRaises(ValueError):
            self.check(plan=plan)

    def test_agent_authored_status_and_progress_are_rejected(self):
        plan = contract()
        plan["progress"] = {"P": 100, "E": 100}
        plan["overall"] = "PROVEN"
        with self.assertRaises(ValueError):
            self.check(plan=plan)


if __name__ == "__main__":
    unittest.main()
