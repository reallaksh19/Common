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



    def test_pull_moves_during_observation_is_not_certified(self):
        class RacingProvider(Provider):
            reads = 0
            def get_pull(self, repo, number):
                self.reads += 1
                value = super().get_pull(repo, number)
                if self.reads >= 2:
                    value["head"]["sha"] = OLD
                return value
        output = self.check(reader=RacingProvider())
        self.assertNotEqual("PROVEN", output["overall"], output)
        self.assertTrue(all(r["status"] != "PROVEN" for r in output["requirements"]))

    def test_an_earlier_missing_case_does_not_mask_later_proven_run(self):
        provider = Provider()
        provider.runs.insert(0, {"id": 8999, "head_sha": HEAD, "status": "completed", "conclusion": "success"})
        provider.jobs[8999] = copy.deepcopy(provider.jobs[9001])
        provider.jobs[8999][0]["id"] = 8998
        provider.logs[8998] = "2026-10-08T00:00:00Z test_other (other.Tests.test_other) ... ok\nOK"
        outcome = self.check(reader=provider)
        self.assertEqual("PROVEN", self.requirement(outcome, "T-RUN")["status"], outcome)



class SchemaBoundaryTests(unittest.TestCase):
    def test_source_bound_result_conforms_to_schema(self):
        import jsonschema
        import yaml
        document = yaml.safe_load(
            (Path(__file__).resolve().parents[1] / "schemas" /
             "qualification-observation-v32.schema.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(M.RESULT_SCHEMA, document["$id"])
        jsonschema.validate(M.assess(contract(), Provider()), document)

    def test_schema_disallows_progress_or_task_result_fields(self):
        import jsonschema
        import yaml
        document = yaml.safe_load(
            (Path(__file__).resolve().parents[1] / "schemas" /
             "qualification-observation-v32.schema.yaml").read_text(encoding="utf-8")
        )
        fake = M.assess(contract(), Provider())
        fake["progress"] = {"P": 100}
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(fake, document)




class AuthenticatedProviderTests(unittest.TestCase):
    def test_provider_requires_authentication_without_exposing_secret(self):
        from unittest import mock
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError):
                M.GhReadOnlyProvider()

    def test_authenticated_reads_use_get_only_and_exact_commit_tree(self):
        import json
        import subprocess
        from unittest import mock
        commit = "d" * 40
        tree_hash = "e" * 40
        responses = {
            "/repos/reallaksh19/Common/pulls/715": {"head": {"sha": HEAD}},
            f"/repos/reallaksh19/Common/actions/runs?head_sha={HEAD}&per_page=100":
                {"total_count": 1, "workflow_runs": [{"id": 9001, "head_sha": HEAD}]},
            "/repos/reallaksh19/Common/actions/runs/9001/jobs?per_page=100":
                {"total_count": 1, "jobs": [{"id": 9002}]},
            f"/repos/reallaksh19/Common/git/commits/{HEAD}": {"tree": {"sha": tree_hash}},
            f"/repos/reallaksh19/Common/git/trees/{tree_hash}?recursive=1":
                {"tree": [{"path": ARTIFACT, "sha": BLOB, "type": "blob"}], "truncated": False},
        }
        calls = []
        def fake_run(argv, **kw):
            calls.append((argv, kw))
            uri = argv[-1]
            raw = TEST_LINE if uri.endswith("/actions/jobs/9002/logs") else json.dumps(responses[uri])
            return subprocess.CompletedProcess(argv, 0, stdout=raw.encode(), stderr=b"")
        with mock.patch.dict("os.environ", {"GH_TOKEN": "canary-never-printed"}, clear=True):
            with mock.patch.object(M.subprocess, "run", side_effect=fake_run):
                provider = M.GhReadOnlyProvider()
                self.assertEqual(HEAD, provider.get_pull(REPO, 715)["head"]["sha"])
                self.assertEqual(1, len(provider.list_runs(REPO, HEAD)))
                self.assertEqual(1, len(provider.list_jobs(REPO, 9001)))
                self.assertIn(TEST_LINE, provider.get_job_log(REPO, 9002))
                self.assertEqual(BLOB, provider.get_tree(REPO, HEAD)["tree"][0]["sha"])
        self.assertEqual(6, len(calls))
        for argv, kw in calls:
            self.assertEqual(["gh", "api", "--method", "GET"], argv[:4])
            self.assertFalse(kw.get("shell", False))
            self.assertNotIn("canary-never-printed", " ".join(argv))

    def test_incomplete_runs_page_returns_unknown(self):
        import json
        import subprocess
        from unittest import mock
        def fake_run(argv, **kw):
            return subprocess.CompletedProcess(argv, 0,
                stdout=json.dumps({"total_count": 101, "workflow_runs": [{"id": 1}]}).encode(), stderr=b"")
        with mock.patch.dict("os.environ", {"GH_TOKEN": "canary"}, clear=True):
            with mock.patch.object(M.subprocess, "run", side_effect=fake_run):
                self.assertIsNone(M.GhReadOnlyProvider().list_runs(REPO, HEAD))

    def test_provider_api_failure_fails_closed_as_unknown(self):
        import subprocess
        from unittest import mock
        def failed(argv, **kw):
            return subprocess.CompletedProcess(argv, 1, stdout=b"", stderr=b"private-error-with-token")
        with mock.patch.dict("os.environ", {"GH_TOKEN": "canary"}, clear=True):
            with mock.patch.object(M.subprocess, "run", side_effect=failed):
                output = M.assess(contract(), M.GhReadOnlyProvider())
        self.assertEqual("UNKNOWN", output["overall"])
        self.assertFalse(any(q["status"] == "PROVEN" for q in output["requirements"]))


if __name__ == "__main__":
    unittest.main()
