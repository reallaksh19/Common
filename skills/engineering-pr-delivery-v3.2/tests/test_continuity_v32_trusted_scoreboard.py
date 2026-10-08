"""#744 event-to-publisher gate: frozen event expected values before runner code.

Source-level negative control: no untrusted PR checkout, no event-authorized
semantic progress, no auth from a supplied title or stale SHA.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve()
V32 = HERE.parents[1]
ROOT = HERE.parents[3]
sys.path.insert(0, str(V32 / "scripts"))
import trusted_scoreboard_v32 as trusted  # noqa: E402

ORACLES = ROOT / ".github/v32-evidence-spine/744-event-oracles-v1.json"
GRAPH = ROOT / ".github/v32-evidence-spine/718-proposal-v2.json"
MANIFEST = ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"
WORKFLOW = ROOT / ".github/workflows/v32-718-trusted-live-scoreboard.yml"


class TrustedEventScoreboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.oracle = json.loads(ORACLES.read_text())
        cls.graph = json.loads(GRAPH.read_text())
        cls.manifest = json.loads(MANIFEST.read_text())
        assert len(cls.oracle["cases"]) == 10
        assert cls.oracle["baseline_main"] == "fa832b7530fceb14605baf22058ad56d14e6cf01"

    def provider(self, head="a"*40):
        return {
            "number": 740, "state": "open", "draft": True,
            "head": {"sha": head, "repo": {"full_name": "reallaksh19/Common"}},
            "base": {"ref": "main", "repo": {"full_name": "reallaksh19/Common"}},
        }

    def test_01_all_ten_precommitted_event_auth_oracles(self):
        for case in self.oracle["cases"]:
            with self.subTest(id=case["id"]):
                result = trusted.gate(
                    case["event_name"], case["event"], self.graph,
                    self.provider(case["provider_sha"]), enabled=case["enabled"])
                self.assertEqual(case["expected"], result["decision"])
                self.assertEqual(0, result["writes"])
                self.assertEqual("NEVER_ASSIGNED", result["semantic_progress"])

    def test_02_missing_provider_origin_never_authorized(self):
        case = self.oracle["cases"][0]
        provider = self.provider()
        del provider["head"]["repo"]
        got = trusted.gate(case["event_name"], case["event"], self.graph,
                           provider, enabled=True)
        self.assertEqual("DENY_PROVIDER_HEAD_REPOSITORY", got["decision"])

    def test_03_provider_PR_number_is_independently_verified(self):
        case = self.oracle["cases"][0]
        provider = self.provider()
        provider["number"] = 999
        got = trusted.gate(case["event_name"], case["event"], self.graph, provider, enabled=True)
        self.assertEqual("DENY_PROVIDER_PR_IDENTITY", got["decision"])

    def test_04_provider_base_must_match_main(self):
        case = self.oracle["cases"][0]
        provider = self.provider()
        provider["base"]["ref"] = "dev"
        got = trusted.gate(case["event_name"], case["event"], self.graph, provider, enabled=True)
        self.assertEqual("DENY_PROVIDER_BASE", got["decision"])

    def test_05_unapproved_graph_never_selects_some_other_PR(self):
        altered = copy.deepcopy(self.graph)
        leaf = next(n for n in altered["nodes"] if n.get("responsibility_id") == "R-PROJECTION")
        leaf["primary_pr"] = "Common#741"
        with self.assertRaisesRegex(ValueError, "UNRELEASED_GENERIC_LIVE_ADAPTER"):
            trusted._identity(altered)

    def test_06_trusted_workflow_uses_only_default_branch_and_safe_event(self):
        text = WORKFLOW.read_text()
        self.assertIn("pull_request_target:", text)
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", text)
        self.assertIn("persist-credentials: false", text)
        self.assertIn("vars.V32_718_LIVE_SCOREBOARD_ENABLED == 'true'", text)
        self.assertIn("contents: read", text)
        self.assertIn("issues: write", text)
        self.assertIn("pull-requests: write", text)
        self.assertIn("cancel-in-progress: false", text)
        self.assertNotIn("github.event.pull_request.head.sha }}", text)
        self.assertNotIn("ref: ${{ github.head_ref }}", text)
        self.assertNotIn("actions/checkout@v4\n        with:\n          ref: ${{ github.event.pull_request.head.sha }}",text)

    def test_07_denied_event_never_invokes_publisher_or_other_provider_calls(self):
        case=self.oracle["cases"][1]
        class Provider:
            def __init__(self,pr):
                self.calls=[]
                self.pr=pr
            def get_pull(self,n):
                self.calls.append(("get_pull",n))
                return copy.deepcopy(self.pr)
            def __getattr__(self,name):
                raise AssertionError("DISALLOWED_PROVIDER_ACCESS:"+name)
        provider=Provider(self.provider())
        result=trusted.run(case["event_name"],case["event"],enabled=True,apply=True,
                           transport=provider,graph=self.graph,manifest=self.manifest)
        self.assertEqual("SKIPPED_WITHOUT_MUTATION",result["status"])
        self.assertEqual("DENY_UNBOUND_PR",result["decision"])
        self.assertEqual([("get_pull",740)],provider.calls)

    def test_08_disabled_flag_zero_mutations_despite_valid_event(self):
        case=self.oracle["cases"][0]
        class Provider:
            def get_pull(self,n):
                return {"number":740,"head":{"sha":"a"*40,
                    "repo":{"full_name":"reallaksh19/Common"}},
                    "base":{"ref":"main"}}
            def __getattr__(self,n):
                raise AssertionError("NOT_ALLOWED_WHILE_DISABLED")
        r=trusted.run(case["event_name"],case["event"],enabled=False,apply=True,
                      transport=Provider(),graph=self.graph,manifest=self.manifest)
        self.assertEqual("DISABLED_BY_OWNER_FLAG",r["decision"])
        self.assertEqual(0,r["writes"])

    def test_09_valid_event_uses_actual_DELP_live_readback_in_dry_run(self):
        case=self.oracle["cases"][0]
        class Provider:
            def __init__(self): self.calls=[]
            def get_commit_sha(self,ref): return "e"*40
            def get_issue(self,n):
                return {"number":n,"title":(
                    "🟡 [718] NEXT #733/C4 · RESERVE35 · FACTS UNREPORTED — V3.2 Evidence Spine"
                    if n==718 else
                    "🟡 [718›733] R-PROJECTION · C4 · PR#740 · UNMATERIALIZED — Issue/PR Views"),
                    "body":"## Human Owner specification preserved\n"}
            def get_pull(self,n):
                if n==740:
                    return {"number":740,"head":{"sha":"a"*40,
                        "repo":{"full_name":"reallaksh19/Common"}},
                        "state":"open","draft":True,"merged":False,
                        "base":{"ref":"main"},
                        "title":"🟡 [718›733] DRAFT · VIEW-PR · HEAD:aaaaaaa · Q:UNPROVEN — Cross-Surface Views",
                        "body":"## Human PR rationale preserved\n"}
                if n in (722,728):
                    sha=("b3dfba3becf829d3a4e21d6eaa54983f05317b65" if n==722
                         else "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414")
                    return {"number":n,"head":{"sha":sha},"state":"closed",
                            "draft":False,"merged":True}
                raise AssertionError("unrecognized PR")
            def list_comments(self,n):return []
            def __getattr__(self,name):
                raise AssertionError("DRY_RUN_CANNOT_WRITE:"+name)
        result=trusted.run(case["event_name"],case["event"],enabled=True,apply=False,
                           transport=Provider(),graph=self.graph,manifest=self.manifest)
        self.assertEqual("ALLOW",result["decision"])
        self.assertEqual("AUTHORIZED_DRY_RUN_NO_WRITE",result["status"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED",result["reconciliation"])
        self.assertEqual(0,result["writes"])
        self.assertTrue(result["input_digest"].startswith("sha256:"))


    def test_10_malformed_PR_event_cannot_borrow_dispatch_inputs(self):
        case = self.oracle["cases"][0]
        payload = copy.deepcopy(case["event"])
        del payload["pull_request"]
        payload["inputs"] = {"pr_number": "740", "expected_head": "a"*40}
        result = trusted.gate("pull_request_target", payload, self.graph,
                              self.provider(), enabled=True)
        self.assertEqual("DENY_MISSING_PR_EVENT", result["decision"])
        self.assertEqual(0, result["writes"])

    def test_11_dispatch_requires_its_own_shape_no_PR_fallback(self):
        payload = copy.deepcopy(self.oracle["cases"][0]["event"])
        result = trusted.gate("workflow_dispatch", payload, self.graph,
                              self.provider(), enabled=True)
        self.assertEqual("DENY_MISSING_DISPATCH_INPUTS", result["decision"])
        self.assertEqual(0, result["writes"])

    def test_12_abandoned_closed_PR_cannot_trigger_live_sync(self):
        case = self.oracle["cases"][0]
        pr = self.provider()
        pr["state"] = "closed"
        pr["merged"] = False
        self.assertEqual("DENY_CLOSED_UNMERGED_PR",
            trusted.gate(case["event_name"], case["event"], self.graph, pr,
                         enabled=True)["decision"])
        pr["merged"] = True
        self.assertEqual("ALLOW", trusted.gate("workflow_dispatch",
            self.oracle["cases"][8]["event"], self.graph, pr,
            enabled=True)["decision"])

if __name__ == "__main__":
    unittest.main()
