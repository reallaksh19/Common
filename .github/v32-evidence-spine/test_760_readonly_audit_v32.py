"""Independent frozen-oracle tests for default-off S5-D1 provider audit."""
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
import audit_live_scoreboard_v32 as mod

ORACLE=json.loads((HERE/"760-readonly-audit-oracles-v1.json").read_text())
WORKFLOW=(ROOT/".github/workflows/v32-718-trusted-live-scoreboard.yml").read_text()
SOURCE=(HERE/"audit_live_scoreboard_v32.py").read_text()

def observed(match=False):
    state="MATCH" if match else "MISSING"
    return {
        "authority":"READ_ONLY_SELF_REPLAY_NO_ACCEPTANCE",
        "pr_binding":"BOUND",
        "full_ESC_6_gate":"FAIL_CLOSED_UNRELEASED_CONSUMERS",
        "authority_effects":[],
        "candidate_sha":"d511fc0210ee823272f41c43621bc90bc290e739",
        "source_input_digest":"sha256:"+"a"*64,
        "delp_input_digest":"sha256:"+"b"*64,
        "semantic_progress":{"P":0,"E":0,"D":0,"DE":0},
        "read_views":{ref:{"title":"MATCH","managed_block":state}
                      for ref in ("Common#718","Common#733","Common#740")},
        "reconciliation":"MATCH" if match else "DRIFT_OR_UNPUBLISHED",
    }

def check(view,flag="",writer="skipped"):
    return mod.summary(view,checkout_sha="c"*40,event_name="issue_comment",
                       enabled_flag=flag,writer_job_result=writer)


class ReadonlyScoreboardAuditTests(unittest.TestCase):
    def test_01_precommitted_independent_audit_contract(self):
        self.assertEqual("relay-v32-760-readonly-activation-audit-oracle-v1",ORACLE["schema"])
        self.assertEqual(10,len(ORACLE["cases"]))
        self.assertEqual("Common#760",ORACLE["child"])
        self.assertIn("NO_--apply",ORACLE["required"]["audit_no_mutation"])

    def test_02_ungated_read_job_still_separate_from_optin_writer(self):
        self.assertIn("audit-readback:",WORKFLOW)
        writer,audit=WORKFLOW.split("\n  audit-readback:",1)
        self.assertIn("vars.V32_718_LIVE_SCOREBOARD_ENABLED == 'true'",writer)
        self.assertIn("--apply",writer)
        self.assertIn("needs: trusted-reconcile",audit)
        self.assertIn("always()",audit)
        self.assertNotIn("--apply",audit)
        self.assertNotIn("vars.V32_718_LIVE_SCOREBOARD_ENABLED == 'true'",audit)

    def test_03_audit_job_scope_and_actual_read_only_permissions(self):
        audit=WORKFLOW.split("\n  audit-readback:",1)[1]
        self.assertIn("github.event.issue.number == 733",audit)
        self.assertIn("github.event.pull_request.number == 740",audit)
        self.assertIn("github.event_name == 'workflow_dispatch'",audit)
        self.assertIn("!startsWith(github.event.comment.body, '<!-- relay-delp:live-status:start -->')",audit)
        self.assertIn("permissions:\n      contents: read\n      issues: read\n      pull-requests: read",audit)
        self.assertNotIn("issues: write",audit)
        self.assertNotIn("pull-requests: write",audit)

    def test_04_only_trusted_checkout_and_no_cli_write_invocation(self):
        audit=WORKFLOW.split("\n  audit-readback:",1)[1]
        self.assertIn("ref: ${{ github.event.repository.default_branch }}",audit)
        self.assertIn("persist-credentials: false",audit)
        self.assertIn("audit_live_scoreboard_v32.py",audit)
        self.assertNotIn("github.event.pull_request.head.sha }}",audit)
        self.assertIn('"--live-readback"',SOURCE)
        self.assertNotIn('"--apply",',SOURCE)
        self.assertNotIn(".patch_title(",SOURCE)
        self.assertNotIn(".patch_issue_body(",SOURCE)
        self.assertNotIn(".patch_pull_title_body(",SOURCE)

    def test_05_unsupported_true_flag_never_promotes_audit_to_mutation(self):
        out=check(observed(False),flag="true")
        self.assertEqual("ENABLED",out["repository_flag_state"])
        self.assertEqual(0,out["write_count"])
        self.assertEqual([] ,out["authority_effects"])
        self.assertEqual("OBSERVED_DRIFT_OR_UNPUBLISHED",out["status"])

    def test_06_unset_false_flag_still_audits_source(self):
        self.assertEqual("NOT_OBSERVED_ENABLED",check(observed(False))["repository_flag_state"])
        self.assertEqual("DISABLED",check(observed(False),flag="false")["repository_flag_state"])
        self.assertEqual("OBSERVED_DRIFT_OR_UNPUBLISHED",check(observed(False))["status"])

    def test_07_full_match_still_no_owner_acceptance(self):
        out=check(observed(True))
        self.assertEqual("OBSERVED_MATCH_NO_ACCEPTANCE",out["status"])
        self.assertEqual("MATCH",out["observed_reconciliation"])
        self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS",out["full_ESC_6_gate"])
        self.assertEqual(0,out["write_count"])

    def test_08_false_green_reconciliation_and_missing_surface_refused(self):
        x=observed(False)
        x["reconciliation"]="MATCH"
        with self.assertRaisesRegex(mod.AuditError,"READBACK_FALSE_SUCCESS"):
            check(x)
        x=observed(True)
        del x["read_views"]["Common#740"]
        with self.assertRaisesRegex(mod.AuditError,"THREE_SURFACE_READBACK_MISSING"):
            check(x)

    def test_09_writer_failure_does_not_show_verified_status(self):
        out=check(observed(True),flag="true",writer="failure")
        self.assertEqual("FAILED_WRITER_REVIEW_PROVIDER_STATE",out["status"])
        self.assertEqual("MATCH",out["observed_reconciliation"])
        self.assertEqual(0,out["write_count"])

    def test_10_provider_error_persists_failure_artifact(self):
        with TemporaryDirectory() as td:
            report=Path(td)/"audit.json"
            argv=["audit_live_scoreboard_v32.py","--output",str(report),
                  "--event-name","issue_comment","--writer-job-result","skipped"]
            responses=[subprocess.CompletedProcess([],0,stdout="c"*40+"\n"),
                       subprocess.CompletedProcess([],4,stdout="",stderr="GET failed")]
            with patch.object(sys,"argv",argv),patch.object(mod.subprocess,"run",side_effect=responses):
                self.assertEqual(3,mod.main())
            saved=json.loads(report.read_text())
            self.assertEqual("FAILED_UNVERIFIED",saved["status"])
            self.assertEqual(0,saved["write_count"])
            self.assertIn("READ_ONLY_PROVIDER_REPLAY_FAILED_EXIT_4",saved["error"])


    def test_11_five_PRECOMMITTED_failure_codes_are_exact_and_never_leak(self):
        fixture=json.loads((HERE/"767-readback-error-oracles-v1.json").read_text())
        self.assertEqual("relay-v32-767-safe-failure-oracle-v1", fixture["schema"])
        self.assertEqual(5,len(fixture["cases"]))
        for row in fixture["cases"]:
            with self.subTest(oracle_id=row["id"]):
                got=mod.classify_provider_failure(row["exit"],row["stderr"])
                self.assertEqual((row["category"],row["exception"],row["code"]),
                    (got["category"],got["exception_class"],got["reason_code"]))
                self.assertEqual(row["exit"],got["exit_code"])
                self.assertEqual(0, got["stderr_bytes"] if not row["stderr"] else
                                    got["stderr_bytes"]-len(row["stderr"].encode("utf-8")))
                self.assertTrue(got["stderr_sha256"].startswith("sha256:"))
                self.assertFalse(got["raw_stderr_exposed"])
                self.assertNotIn("TOKEN_PRIVATE_SAMPLE",json.dumps(got))
                self.assertNotIn("ghp_FAKE_PRIVATE_BEARER_SHOULD_NOT_LEAK",json.dumps(got))

    def test_12_real_wrapper_failure_retains_safe_diagnostic_artifact(self):
        with TemporaryDirectory() as td:
            report=Path(td)/"audit.json"
            argv=["audit_live_scoreboard_v32.py","--output",str(report),
                  "--event-name","issue_comment","--writer-job-result","skipped"]
            stderr="Traceback...\\nDelpError: gh: HTTP 403: TOKEN_PRIVATE_SAMPLE"
            responses=[subprocess.CompletedProcess([],0,stdout="c"*40+"\\n"),
                       subprocess.CompletedProcess([],1,stdout="",stderr=stderr)]
            with patch.object(sys,"argv",argv),patch.object(mod.subprocess,"run",side_effect=responses):
                self.assertEqual(3,mod.main())
            saved=json.loads(report.read_text())
            self.assertEqual("FAILED_UNVERIFIED",saved["status"])
            self.assertEqual(0,saved["write_count"])
            self.assertEqual("GH_HTTP",saved["provider_failure"]["category"])
            self.assertEqual("HTTP_403",saved["provider_failure"]["reason_code"])
            self.assertEqual(1,saved["provider_failure"]["exit_code"])
            self.assertNotIn("TOKEN_PRIVATE_SAMPLE",report.read_text())


    def test_13_precommitted_three_observer_candidate_guard_cases(self):
        fixture=json.loads((HERE/"773-three-observer-oracles-v1.json").read_text())
        self.assertEqual("INDEPENDENT_EXPECTATIONS_COMMITTED_BEFORE_PROBE",fixture["authority"])
        self.assertEqual(5,len(fixture["cases"]))
        for row in fixture["cases"]:
            with self.subTest(case=row["id"]):
                got=mod.three_head_verdict(row["direct_initial"],
                                           row["delp_observed"],row["direct_final"])
                self.assertEqual(row["expected"],got["verdict"])
                self.assertEqual(row["direct_initial"],got["direct_initial_sha"])
                self.assertEqual(row["delp_observed"],got["delp_observed_sha"])
                self.assertEqual(row["direct_final"],got["direct_final_sha"])
                self.assertEqual(0,got["write_count"])
                self.assertEqual([],got["authority_effects"])

    def test_14_probe_is_READ_ONLY_and_only_guarded_source_failure(self):
        import inspect
        source=inspect.getsource(mod.live_three_head_probe)
        self.assertIn("provider.get_pull(740)",source)
        self.assertIn("delp.observe_github(provider, graph)",source)
        self.assertNotIn("patch_",source)
        self.assertNotIn("post_comment",source)
        self.assertNotIn("--apply",source)
        main=inspect.getsource(mod.main)
        self.assertIn("CANDIDATE_CHANGED_DURING_OBSERVATION",main)
        self.assertIn("run_guarded_trace()",main)
        self.assertIn("NEW_GUARDED_REPLAY_AFTER_ORIGINAL_FAILURE",main)

    def test_15_source_failure_probe_stays_FAILED_UNVERIFIED(self):
        with TemporaryDirectory() as td:
            path=Path(td)/"report.json"
            argv=["audit_live_scoreboard_v32.py","--output",str(path),
                  "--event-name","issue_comment","--writer-job-result","skipped"]
            err="V32-718-REPLAY-FAILED: ReplayError: CANDIDATE_CHANGED_DURING_OBSERVATION"
            responses=[subprocess.CompletedProcess([],0,stdout="c"*40+"\\n"),
                       subprocess.CompletedProcess([],1,stdout="",stderr=err)]
            import same_guarded_readback_trace_v32 as tracing
            trace={"source_outcome":"SOURCE_REPLAY_FAILED_UNVERIFIED",
                   "invocation_scope":"NEW_GUARDED_REPLAY_AFTER_ORIGINAL_FAILURE",
                   "verdict":"DELP_OBSERVER_MISMATCH","write_count":0,"authority_effects":[]}
            with patch.object(sys,"argv",argv),patch.object(mod.subprocess,"run",side_effect=responses),patch.object(tracing,"run_guarded_trace",return_value=trace):
                self.assertEqual(3,mod.main())
            audit=json.loads(path.read_text())
            self.assertEqual("FAILED_UNVERIFIED",audit["status"])
            self.assertEqual("DELP_OBSERVER_MISMATCH",audit["same_guarded_replay_trace"]["verdict"])
            self.assertEqual("NEW_GUARDED_REPLAY_AFTER_ORIGINAL_FAILURE",
                             audit["same_guarded_replay_trace"]["invocation_scope"])
            self.assertEqual(0,audit["write_count"])
            self.assertEqual([],audit["authority_effects"])


    def test_16_precommitted_writer_only_concurrency_scope(self):
        fixture=json.loads((HERE/"776-writer-lock-oracles-v1.json").read_text())
        self.assertEqual("relay-v32-776-job-scoped-writer-concurrency-oracle-v1",fixture["schema"])
        self.assertEqual(5,len(fixture["cases"]))
        self.assertFalse(fixture["requirements"]["root_workflow_lock"])
        self.assertTrue(fixture["requirements"]["audit_no_concurrency"])
        # Root-level YAML must not serialize unrelated read-only events.
        pre_jobs, jobs=WORKFLOW.split("\njobs:\n",1)
        self.assertNotIn("\nconcurrency:",pre_jobs)
        writer, audit=jobs.split("\n  audit-readback:",1)
        self.assertIn("  trusted-reconcile:\n",writer)
        self.assertIn("    concurrency:\n      group: v32-718-single-issue-scoreboard-publisher\n      cancel-in-progress: false",writer)
        self.assertEqual(1,WORKFLOW.count("group: v32-718-single-issue-scoreboard-publisher"))
        self.assertIn("vars.V32_718_LIVE_SCOREBOARD_ENABLED == 'true'",writer)
        self.assertIn("needs: trusted-reconcile",audit)
        self.assertIn("always()",audit)
        self.assertNotIn("concurrency:",audit)
        self.assertNotIn("--apply",audit)
        self.assertIn("contents: read\n      issues: read\n      pull-requests: read",audit)
        self.assertIn("github.event.issue.number == 733",audit)
        self.assertIn("github.event.pull_request.number == 740",audit)
        self.assertIn("relay-delp:live-status:start",audit)


    def test_17_precommitted_same_invocation_oracle(self):
        import same_guarded_readback_trace_v32 as trace
        fixture=json.loads((HERE/"780-same-call-trace-oracles-v1.json").read_text())
        self.assertEqual("relay-v32-780-same-guarded-readback-observer-trace-oracle-v1",fixture["schema"])
        self.assertEqual(5,len(fixture["cases"]))
        for case in fixture["cases"]:
            with self.subTest(id=case["id"]):
                observations=[{"sha":p["sha"]} for p in case["get_pulls"]]
                report=trace.classify_calls(observations)
                self.assertEqual(case["verdict"],report["verdict"])
                self.assertEqual(case["expected"],
                    [x["phase"] for x in report["ordered_bound_pull_reads"]])
                self.assertEqual(len(case["get_pulls"]),report["read_count"])

    def test_18_tracing_transport_is_GET_ONLY_and_source_guard_unchanged(self):
        import inspect
        import same_guarded_readback_trace_v32 as trace
        self.assertEqual({"get_pull","get_issue","get_commit_sha","compare","list_comments"},
            {name for name in vars(trace.ReadOnlyTraceTransport)
             if not name.startswith("_")})
        src=inspect.getsource(trace.run_guarded_trace)
        self.assertIn("cycle.live_readback(",src)
        self.assertIn("ReadOnlyTraceTransport(",src)
        self.assertNotIn("patch_",src)
        self.assertNotIn("post_comment",src)
        self.assertNotIn("--apply",src)

    def test_19_original_failing_guard_is_captured_in_one_new_invocation(self):
        import same_guarded_readback_trace_v32 as trace
        fake_graph={"programme":{"repository":"reallaksh19/Common"},
                    "nodes":[{"ref":"Common#733","primary_pr":"Common#740"}]}
        class FakeGetOnlyProvider:
            def __init__(self):
                self.idx=0
            def get_pull(self,n):
                self.idx+=1
                return {"number":n,"head":{"sha":"d"*40 if self.idx==1 else "b"*40}}
        provider=FakeGetOnlyProvider()
        def fake_readback(manifest,graph,transport):
            self.assertEqual("d"*40,transport.get_pull(740)["head"]["sha"])
            self.assertEqual("b"*40,transport.get_pull(740)["head"]["sha"])
            raise trace.cycle.ReplayError("CANDIDATE_CHANGED_DURING_OBSERVATION")
        with patch.object(trace.cycle,"live_readback",side_effect=fake_readback) as source:
            got=trace.run_guarded_trace(provider=provider,graph=fake_graph,manifest={})
        self.assertEqual(1,source.call_count)
        self.assertEqual(2,got["read_count"])
        self.assertEqual("DELP_OBSERVER_MISMATCH",got["verdict"])
        self.assertEqual("CANDIDATE_CHANGED_DURING_OBSERVATION",got["source_error_code"])
        self.assertEqual("SOURCE_REPLAY_FAILED_UNVERIFIED",got["source_outcome"])
        self.assertEqual("NEW_GUARDED_REPLAY_AFTER_ORIGINAL_FAILURE",got["invocation_scope"])
        self.assertEqual(0,got["write_count"])
        self.assertEqual([],got["authority_effects"])


if __name__=="__main__":
    unittest.main()
