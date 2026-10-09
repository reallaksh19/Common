"""#718/#733 source-level integrated fixture replay — separately frozen oracle.

The full programme gate intentionally remains red: ESC-4/5 consumers
are separately unreleased. This suite certifies only the bounded ESC-3
pure cross-surface product slice, including real DELP and R-PROOF join.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess

HERE = Path(__file__).resolve()
V32 = HERE.parents[1]
ROOT = HERE.parents[3]
sys.path.insert(0, str(V32 / "scripts"))
import vertical_cycle_v32 as replay  # noqa: E402
import pr_responsibility_view_v32 as view  # noqa: E402


class VerticalResponsibilityCycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json").read_text())
        cls.graph = json.loads((ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json").read_text())

    def test_01_release_claim_and_owner_source_bound_real_chain(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual("PASS_PURE_READ_VIEWS", r["R_PROJECTION_phase_gate"])
        self.assertEqual("UNREPORTED", r["material_vs_facts"]["checkpoint_facts"])
        self.assertEqual(["UNRESOLVED_CHAT_MESSAGE_LINK"], r["owner_origin_status"])
        self.assertEqual([], r["authority_effects"])

    def test_02_parent_title_oracle_independent_of_renderer(self):
        r = replay.replay(self.manifest, self.graph)
        golden = replay._fixture(self.manifest, "GF-SMART-SURFACES")["expected"]
        self.assertEqual(golden["parent_title"], r["parent_actual_title"])

    def test_03_child_title_oracle_independent_of_renderer(self):
        r = replay.replay(self.manifest, self.graph)
        golden = replay._fixture(self.manifest, "GF-SMART-SURFACES")["expected"]
        self.assertEqual(golden["child_title"], r["child_actual_title"])

    def test_04_changed_candidate_draft_smart_title_never_keeps_old_head(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertIn("HEAD:bbbbbbb · Q:UNPROVEN", r["draft_changed_head_title"])
        self.assertNotEqual(r["source_input_digest"], r["changed_head_input_digest"])

    def test_05_PR_managed_block_preserves_exact_OI_OR_and_evidence_basis(self):
        r = replay.replay(self.manifest, self.graph)
        body = r["draft_pr_managed_description"]
        self.assertIn("OR-718-04", body)
        self.assertIn("GF-PR-HEAD", body)
        self.assertIn(r["changed_head_input_digest"], body)
        self.assertIn("UNBOUND_ADVISORY", body)

    def test_06_full_chain_fails_closed_on_unreleased_handover_and_metric(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", r["full_ESC_6_gate"])
        self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED", r["stage_results"]["HANDOVER_PROMPT"])
        self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED", r["stage_results"]["AGENT_MATRIX"])

    def test_07_mutated_parent_title_oracle_is_rejected(self):
        m = copy.deepcopy(self.manifest)
        replay._fixture(m, "GF-SMART-SURFACES")["expected"]["parent_title"] = "🟢 [718] COMPLETE"
        with self.assertRaisesRegex(replay.ReplayError, "GOLDEN_PARENT_TITLE_MISMATCH"):
            replay.replay(m, self.graph)

    def test_08_mutated_child_title_oracle_is_rejected(self):
        m = copy.deepcopy(self.manifest)
        replay._fixture(m, "GF-SMART-SURFACES")["expected"]["child_title"] = "🟢 [733] CODE COMPLETE"
        with self.assertRaisesRegex(replay.ReplayError, "GOLDEN_CHILD_TITLE_MISMATCH"):
            replay.replay(m, self.graph)

    def test_09_changed_graph_release_digest_rejected(self):
        g = copy.deepcopy(self.graph)
        g["programme"]["decomposition_proposal"]["released_proposal_digest"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(replay.ReplayError, "FROZEN_PLAN_DIGEST_DRIFT"):
            replay.replay(self.manifest, g)

    def test_10_wrong_original_chat_source_status_rejected(self):
        m = copy.deepcopy(self.manifest)
        m["owner_intents"][0]["original_source_status"] = "KNOWN"
        with self.assertRaisesRegex(view.ViewError, "ORIGINAL_SOURCE_UNACCOUNTED"):
            replay.replay(m, self.graph)

    def test_11_exact_candidate_move_does_not_claim_semantic_progress(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual("PASS_REAL_V32_DELP_AND_STALE_QUALIFIER", r["stage_results"]["SOURCE_OBSERVATION"])
        self.assertEqual("UNREPORTED", r["material_vs_facts"]["checkpoint_facts"])
        self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", r["full_ESC_6_gate"])

    def test_12_report_is_deterministic_and_no_authority_leaks(self):
        a = replay.replay(self.manifest, self.graph)
        b = replay.replay(self.manifest, self.graph)
        self.assertEqual(a, b)
        self.assertNotIn("OWNER_AUTHORIZED_MERGE", json.dumps(a))
        self.assertNotIn("FULL_PASS", json.dumps(a))

    def test_13_output_stage_contract_has_every_consumer(self):
        r = replay.replay(self.manifest, self.graph)
        self.assertEqual(set(self.manifest["required_stage_outputs"]), set(r["stage_results"]))

    def test_14_real_source_runner_generates_replay_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "report.json"
            report = replay.replay(self.manifest, self.graph)
            path.write_text(json.dumps(report, sort_keys=True), encoding="utf-8")
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("PASS_PURE_READ_VIEWS", loaded["R_PROJECTION_phase_gate"])
            self.assertTrue(loaded["fixture_manifest_digest"].startswith("sha256:"))


    def test_15_executable_source_module_phase_gate_and_report(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "phase-report.json"
            command = [sys.executable, str(V32 / "scripts" / "vertical_cycle_v32.py"),
                       "--manifest", str(ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"),
                       "--graph", str(ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json"),
                       "--report", str(report)]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(0, run.returncode, run.stderr)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("PASS_PURE_READ_VIEWS", result["R_PROJECTION_phase_gate"])
            self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", result["full_ESC_6_gate"])
            self.assertEqual(0, result["exit_code"])
            print("V32_733_REAL_CLI_PHASE=PASS")
            print("V32_733_CLI_FIXTURE_DIGEST=" + result["fixture_manifest_digest"])

    def test_16_executable_source_module_full_gate_must_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "full-expected-red.json"
            command = [sys.executable, str(V32 / "scripts" / "vertical_cycle_v32.py"),
                       "--assert-all-consumers", "--report", str(report)]
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(2, run.returncode, run.stderr)
            result = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("FAIL_CLOSED_UNRELEASED_CONSUMERS", result["full_ESC_6_gate"])
            self.assertEqual(2, result["exit_code"])
            self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED",
                             result["stage_results"]["HANDOVER_PROMPT"])
            self.assertEqual("NOT_IMPLEMENTED_NOT_RELEASED",
                             result["stage_results"]["AGENT_MATRIX"])
            print("V32_733_REAL_CLI_FULL=EXPECTED_RED_UNRELEASED")


    def test_17_frozen_c0_and_live_graph_are_distinct_but_same_release(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        frozen = self.graph
        old_plan = frozen["programme"]["decomposition_proposal"]
        new_plan = live["programme"]["decomposition_proposal"]
        # A claim-first released plan can materialize a new responsibility
        # binding without changing the frozen original C0 release digest.
        oracle = json.loads((ROOT / ".github/v32-evidence-spine/793-binding-oracles-v1.json").read_text())
        self.assertEqual(old_plan["released_proposal_digest"], new_plan["released_proposal_digest"])
        self.assertEqual(old_plan["responsibilities"], new_plan["responsibilities"])
        self.assertEqual({x["responsibility_id"]: x["ref"] for x in new_plan["bindings"]},
                         {x["responsibility_id"]: x["ref"] for x in oracle["expected_bindings"]})
        self.assertTrue({x["responsibility_id"] for x in old_plan["bindings"]}
                        < {x["responsibility_id"] for x in new_plan["bindings"]})
        self.assertEqual(frozen["programme"]["acceptance_claims"], live["programme"]["acceptance_claims"])
        self.assertEqual(oracle["old_reserve_weight"], frozen["nodes"][0]["reserve_weight"])
        self.assertEqual(oracle["expected_reserve_weight"], live["nodes"][0]["reserve_weight"])
        old_child = next(n for n in frozen["nodes"] if n.get("responsibility_id") == "R-PROJECTION")
        new_child = next(n for n in live["nodes"] if n.get("responsibility_id") == "R-PROJECTION")
        self.assertNotIn("primary_pr", old_child)
        self.assertEqual("Common#740", new_child["primary_pr"])
        new_child = dict(new_child)
        new_child.pop("primary_pr")
        self.assertEqual(old_child, new_child)

    def test_18_historical_oracle_source_graph_blob_is_precommit_exact(self):
        source = ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json"
        result = subprocess.run(["git", "hash-object", str(source)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        self.assertEqual("f4055eb0e8d47e87c59cbd0ccf0b4ce56654a5d3",
                         result.stdout.strip())
        self.assertEqual("Common#718", self.graph["programme"]["root"])

    def test_19_live_bound_draft_PR_does_not_award_factless_work(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        fake_current = "c" * 40
        observations = {
            "Common#720": {"pr_state": "MERGED", "candidate_sha": "b3dfba3becf829d3a4e21d6eaa54983f05317b65"},
            "Common#724": {"pr_state": "MERGED", "candidate_sha": "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414"},
            "Common#733": {"pr_state": "OPEN", "candidate_sha": fake_current},
        }
        rendered = view.build_views(
            live, self.manifest, observations=observations, ledger=[],
            selected_leaf="Common#733", phase="C4",
            human_titles={"Common#718": "V3.2 Evidence Spine",
                          "Common#733": "Issue/PR Views",
                          "PR": "Cross-Surface Views"},
            draft_pr={"number": 740, "head_sha": fake_current, "lifecycle": "DRAFT"})
        self.assertEqual("BOUND", rendered["pr"]["binding"])
        self.assertEqual(0, rendered["leaf_semantic"]["P"])
        self.assertEqual(0, rendered["leaf_semantic"]["E"])
        self.assertEqual(["Common#720", "Common#724"], rendered["historical_unreported"])
        self.assertIn("PR#740", rendered["issue_titles"]["Common#733"])
        self.assertIn("HEAD:ccccccc · Q:UNPROVEN", rendered["draft_pr_title"])
        self.assertEqual("MATERIALIZE_FACTS_OR_CONTRACT", rendered["actual_next"])
        self.assertEqual([], rendered["authority_effects"])

    def test_20_live_parent_smart_title_recomputed_from_current_graph(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        observations = {
            "Common#720": {"pr_state": "MERGED", "candidate_sha": "b3dfba3becf829d3a4e21d6eaa54983f05317b65"},
            "Common#724": {"pr_state": "MERGED", "candidate_sha": "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414"},
            "Common#733": {"pr_state": "OPEN", "candidate_sha": "c" * 40},
        }
        result = view.build_views(
            live, self.manifest, observations=observations, selected_leaf="Common#733",
            phase="C4", human_titles={"Common#718": "V3.2 Evidence Spine",
            "Common#733": "Issue/PR Views"}, title_contract="C4-S6")
        self.assertEqual(
            f"🟡 [718] NEXT #733/C4 · D0/E0 · RESERVE{next(n['reserve_weight'] for n in live['nodes'] if n['kind'] == 'ROOT')} · FACTS UNREPORTED — V3.2 Evidence Spine",
            result["issue_titles"]["Common#718"])
        self.assertEqual(
            "🟡 [718›733] R-PROJECTION · C4 · P0/E0 · PR#740 · UNMATERIALIZED — Issue/PR Views",
            result["issue_titles"]["Common#733"])

    def test_21_current_draft_candidate_head_changes_only_derived_inputs(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        common = dict(selected_leaf="Common#733", phase="C4",
                      human_titles={"Common#718": "V3.2 Evidence Spine",
                                    "Common#733": "Issue/PR Views",
                                    "PR": "Cross-Surface Views"})
        a = view.build_views(live, self.manifest, draft_pr={
            "number": 740, "head_sha": "c" * 40, "lifecycle": "DRAFT"}, **common)
        b = view.build_views(live, self.manifest, draft_pr={
            "number": 740, "head_sha": "d" * 40, "lifecycle": "DRAFT"}, **common)
        self.assertEqual(a["leaf_semantic"], b["leaf_semantic"])
        self.assertNotEqual(a["input_digest"], b["input_digest"])
        self.assertNotEqual(a["draft_pr_title"], b["draft_pr_title"])
        self.assertEqual("NOT_IMPLEMENTED", b["unreleased_consumers"]["agent_matrix"])

    def test_22_live_projection_never_modifies_c0_golden_oracle(self):
        before = json.loads((ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json").read_text())
        result = replay.replay(self.manifest, self.graph)
        after = json.loads((ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json").read_text())
        self.assertEqual(before, after)
        self.assertEqual(
            replay._fixture(self.manifest, "GF-SMART-SURFACES")["expected"]["parent_title"],
            result["parent_actual_title"])


    def _provider(self, *, child_title=None, pr_title=None, moved=False, graph=None):
        """Graph-declared GitHub GET fake; independent C0/C4 selected PR oracles stay frozen.

        A new released leaf may introduce a new primary_pr; the fake must not
        reject a valid DELP observation merely because this test's old hardcoded
        allowlist predates the released graph. Undeclared PRs still fail closed.
        """
        released = graph if graph is not None else json.loads(
            (ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text()
        )
        declared_prs = {
            int(node["primary_pr"].rsplit("#", 1)[1])
            for node in released["nodes"]
            if node["kind"] == "LEAF" and node.get("primary_pr")
        }
        class Provider:
            pass
        p = Provider()
        p.repository = "reallaksh19/Common"
        p.head = "c" * 40
        p.count = 0
        p.get_commit_sha = lambda name: "e" * 40
        p.get_issue = lambda number: {
            "number": number,
            "title": (
                f"🟡 [718] NEXT #733/C4 · D0/E0 · RESERVE{next(n['reserve_weight'] for n in released['nodes'] if n['kind'] == 'ROOT')} · FACTS UNREPORTED — V3.2 Evidence Spine"
                if number == 718 else
                child_title or (
                    "🟡 [718›733] R-PROJECTION · C4 · P0/E0 · PR#740 · UNMATERIALIZED — Issue/PR Views"
                    if number == 733 else
                    f"🟡 [718›{number}] LEAF · C4 · P0/E0 — Child Issue {number}"
                )
            ),
            "body": "## Human Owner specification preserved\n"
        }
        p.list_comments = lambda number: []
        def get_pull(number):
            if number == 740:
                p.count += 1
                head = ("d" * 40 if moved and p.count >= 3 else p.head)
                return {
                    "number": 740, "head": {"sha": head},
                    "state": "open", "draft": True, "merged": False,
                    "title": pr_title or
                        "🟡 [718›733] DRAFT · VIEW-PR · HEAD:ccccccc · Q:UNPROVEN — Cross-Surface Views",
                    "body": "## Human PR rationale preserved\n",
                }
            if number in (722, 728):
                sha = ("b3dfba3becf829d3a4e21d6eaa54983f05317b65" if number == 722 else
                       "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414")
                return {"number": number, "head": {"sha": sha},
                        "state": "closed", "draft": False, "merged": True}
            if number in declared_prs:
                # Additional, graph-declared leaf: legitimate source material,
                # NOT completed work, qualification, or an Owner-approved review.
                return {
                    "number": number, "head": {"sha": "e" * 40},
                    "state": "open", "draft": True, "merged": False,
                    "title": pr_title or f"🟡 PR#{number} — Graph Leaf PR",
                    "body": "## Human PR rationale preserved\n",
                }
            raise AssertionError(f"unapproved fake PR #{number}")
        p.get_pull = get_pull
        return p

    def test_23_live_provider_readback_uses_actual_v32_module_and_no_mutations(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._provider()
        report = replay.live_readback(self.manifest, live, provider)
        self.assertEqual("BOUND", report["pr_binding"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED", report["reconciliation"])
        self.assertEqual("MATCH", report["read_views"]["Common#718"]["title"])
        self.assertEqual("MATCH", report["read_views"]["Common#733"]["title"])
        self.assertEqual("MATCH", report["read_views"]["Common#740"]["title"])
        self.assertEqual("MISSING", report["read_views"]["Common#740"]["managed_block"])
        self.assertEqual(["Common#720", "Common#724"], report["historical_unreported"])
        self.assertEqual(0, report["semantic_progress"]["P"])
        self.assertEqual(0, report["semantic_progress"]["E"])
        self.assertEqual([], report["authority_effects"])
        self.assertEqual(3, provider.count)

    def test_24_live_child_title_drift_detected_even_if_parent_matches(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        report = replay.live_readback(self.manifest, live, self._provider(
            child_title="🟢 [718›733] COMPLETE — Issue/PR Views"))
        self.assertEqual("MATCH", report["read_views"]["Common#718"]["title"])
        self.assertEqual("DRIFT", report["read_views"]["Common#733"]["title"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED", report["reconciliation"])

    def test_25_live_provider_changed_head_midflight_refuses_stale_render(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        with self.assertRaisesRegex(replay.ReplayError, "PROVIDER_MOVED_DURING_RECONCILIATION"):
            replay.live_readback(self.manifest, live, self._provider(moved=True))

    def test_26_live_PR_title_head_drift_detected_without_fabricating_facts(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        r = replay.live_readback(self.manifest, live, self._provider(
            pr_title="🟡 [718›733] DRAFT · HEAD:OLD · Q:PROVEN — Cross-Surface Views"))
        self.assertEqual("DRIFT", r["read_views"]["Common#740"]["title"])
        self.assertEqual("UNPROVEN", r["qualifier"]["state"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED", r["reconciliation"])


    def test_27_issue_body_changes_during_readback_fail_closed(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        transport = self._provider()
        original = transport.get_issue
        reads = [0]
        def moving_issue(number):
            response = original(number)
            if number == 733:
                reads[0] += 1
                if reads[0] == 2:
                    response["body"] = "Some new Owner edit requiring a new read"
            return response
        transport.get_issue = moving_issue
        with self.assertRaisesRegex(replay.ReplayError,
                                    "PROVIDER_ISSUE_MOVED_DURING_RECONCILIATION"):
            replay.live_readback(self.manifest, live, transport)

    def test_28_PR_human_description_changes_during_readback_fail_closed(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        transport = self._provider()
        original = transport.get_pull
        reads = [0]
        def moving_pr(number):
            response = original(number)
            if number == 740:
                reads[0] += 1
                if reads[0] == 3:
                    response["body"] = "New human purpose discovered during readback"
            return response
        transport.get_pull = moving_pr
        with self.assertRaisesRegex(replay.ReplayError,
                                    "PROVIDER_PR_METADATA_MOVED_DURING_RECONCILIATION"):
            replay.live_readback(self.manifest, live, transport)


    def test_29_actual_guarded_publisher_blocks_wrong_provider_identity(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._provider()
        provider.repository = "another/repository"
        with self.assertRaisesRegex(replay.ReplayError, "MUTATION_REPOSITORY_NOT_ALLOWED"):
            replay.guarded_publish(self.manifest, live, provider,
                expected_head="c" * 40,
                expected_input_digest="sha256:" + "a" * 64, apply=True)

    def test_30_actual_guarded_publisher_dry_run_no_mutations(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        first = replay.live_readback(self.manifest, live, self._provider())
        adapter = self._provider()
        report = replay.guarded_publish(self.manifest, live, adapter,
                    expected_head="c" * 40,
                    expected_input_digest=first["source_input_digest"], apply=False)
        self.assertEqual("DRY_RUN", report["requested_mode"])
        self.assertEqual("PLANNED", report["status"])
        self.assertEqual(["Common#718", "Common#733", "Common#740"],
                         report["changed_surfaces"])
        self.assertEqual([], report["applied_surfaces"])
        self.assertEqual([], report["authority_effects"])

    def test_31_real_live_readback_rejects_valid_markers_forged_content(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        first = replay.live_readback(self.manifest, live, self._provider())
        refs = first["expected_managed_blocks"]
        provider = self._provider()
        get_issue, get_pull = provider.get_issue, provider.get_pull
        def issue_with_managed(number):
            raw = get_issue(number)
            body = refs[f"Common#{number}"]
            if number == 733:
                body = body.replace("UNPROVEN", "PROVEN OWNER MERGE APPROVED")
            raw["body"] = raw["body"] + "\\n" + body
            return raw
        def pr_with_managed(number):
            raw = get_pull(number)
            if number == 740:
                raw["body"] += "\\n" + refs["Common#740"]
            return raw
        provider.get_issue, provider.get_pull = issue_with_managed, pr_with_managed
        second = replay.live_readback(self.manifest, live, provider)
        self.assertEqual("MATCH", second["read_views"]["Common#718"]["managed_block"])
        self.assertEqual("DRIFT", second["read_views"]["Common#733"]["managed_block"])
        self.assertEqual("MATCH", second["read_views"]["Common#740"]["managed_block"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED", second["reconciliation"])

    def test_32_complete_exact_managed_readback_can_match_without_writer(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        first = replay.live_readback(self.manifest, live, self._provider())
        refs = first["expected_managed_blocks"]
        provider = self._provider()
        get_issue, get_pull = provider.get_issue, provider.get_pull
        def issue_with_managed(number):
            raw = get_issue(number)
            raw["body"] += "\\n" + refs[f"Common#{number}"]
            return raw
        def pr_with_managed(number):
            raw = get_pull(number)
            if number == 740:
                raw["body"] += "\\n" + refs["Common#740"]
            return raw
        provider.get_issue, provider.get_pull = issue_with_managed, pr_with_managed
        result = replay.live_readback(self.manifest, live, provider)
        self.assertEqual("MATCH", result["reconciliation"])
        self.assertTrue(all(v["title"] == "MATCH" and
                            v["managed_block"] == "MATCH"
                            for v in result["read_views"].values()))
        self.assertEqual([], result["authority_effects"])


    def test_33_legacy_DELP_issue_title_writer_rejected_for_bound_718(self):
        import delp_projection_v32 as delp
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        store = delp.InMemoryStore()
        with self.assertRaisesRegex(delp.DelpError, "SOURCE_SMART_TITLE_POLICY_REQUIRED"):
            delp.sync_projection(store, live, lambda: [], lambda: {}, {})
        self.assertEqual([], store.writes)

    def test_34_single_DELP_issue_writer_publishes_source_smart_titles(self):
        import delp_projection_v32 as delp
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        observation = {
            "Common#720": {"candidate_sha": "b3dfba3becf829d3a4e21d6eaa54983f05317b65", "pr_state": "MERGED"},
            "Common#724": {"candidate_sha": "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414", "pr_state": "MERGED"},
            "Common#733": {"candidate_sha": "c"*40, "pr_state": "OPEN"},
        }
        snapshot = replay.view.build_views(live, self.manifest, ledger=[],
            observations=observation, selected_leaf="Common#733", phase="C4",
            human_titles={"Common#718":"V3.2 Evidence Spine",
                          "Common#733":"Issue/PR Views", "PR":"Cross-Surface Views"},
            draft_pr={"number":740,"head_sha":"c"*40,"lifecycle":"DRAFT"})
        projection = delp.project(live, [], observation)
        store = delp.InMemoryStore()
        results = delp.sync_projection(store, live, lambda: [], lambda: observation,
            {"Common#718":"V3.2 Evidence Spine", "Common#733":"Issue/PR Views"},
            title_overrides=snapshot["issue_titles"],
            selected_refs=("Common#718","Common#733"),
            expected_input_digest=projection["input_digest"])
        self.assertEqual(["Common#733","Common#718"], list(results))
        self.assertEqual(snapshot["issue_titles"]["Common#718"], store.titles["Common#718"])
        self.assertEqual(snapshot["issue_titles"]["Common#733"], store.titles["Common#733"])
        self.assertEqual(2, len(store.writes))
        self.assertEqual(projection["input_digest"], store.status["Common#733"]["digest"])
        self.assertEqual(0, store.status["Common#733"]["document"]["node"]["progress"]["P"])
        self.assertEqual(0, store.status["Common#733"]["document"]["node"]["progress"]["E"])

    def test_35_single_DELP_writer_rejects_stale_input_before_any_write(self):
        import delp_projection_v32 as delp
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        store = delp.InMemoryStore()
        with self.assertRaisesRegex(delp.DelpError, "ISSUE_PUBLISHER_INPUT_MOVED"):
            delp.sync_projection(store, live, lambda: [], lambda: {},
                {"Common#718":"V3.2 Evidence Spine", "Common#733":"Issue/PR Views"},
                title_overrides={"Common#718":"safe parent", "Common#733":"safe child"},
                selected_refs=("Common#718","Common#733"),
                expected_input_digest="sha256:"+"0"*64)
        self.assertEqual([], store.writes)

    def test_36_single_DELP_writer_rejects_partial_title_ownership_or_scope(self):
        import delp_projection_v32 as delp
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        kwargs = dict(title_overrides={"Common#718":"root", "Common#733":"child"},
                      selected_refs=("Common#718","Common#733"),
                      expected_input_digest="sha256:"+"a"*64)
        for key,value,error in (
            ("title_overrides",{"Common#718":"root"},"SOURCE_SMART_TITLE_POLICY_REQUIRED"),
            ("selected_refs",("Common#718","Common#720","Common#733"),
             "SOURCE_SMART_TITLE_SCOPE_MISMATCH"),
            ("title_overrides",{"Common#718":"root","Common#733":"child","Common#0":"x"},
             "ISSUE_PUBLISHER_INVALID_TITLE_OVERRIDE"),
        ):
            store = delp.InMemoryStore()
            args=dict(kwargs)
            args[key]=value
            with self.subTest(key=key):
                with self.assertRaisesRegex(delp.DelpError, error):
                    delp.sync_projection(store, live, lambda: [], lambda: {}, {}, **args)
                self.assertEqual([], store.writes)

    def _writing_provider(self):
        """Mutable stateful GitHub fake: ACTUAL DELP comment, issue and PR writers."""
        provider = self._provider()
        get_issue, get_pull = provider.get_issue, provider.get_pull
        provider.issues = {n: get_issue(n) for n in (718,733)}
        provider.issues[733]["title"] = (
            "🟡 [718›733] R-PROJECTION · C4 · OLD — Issue/PR Views")
        provider.pull = get_pull(740)
        provider.comments = {718:[],733:[]}
        provider.writes = []
        provider.get_issue = lambda n: copy.deepcopy(provider.issues[n])
        def pull(number):
            if number == 740:
                return copy.deepcopy(provider.pull)
            return get_pull(number)
        provider.get_pull = pull
        provider.list_comments = lambda n: copy.deepcopy(provider.comments.get(n,[]))
        def post_comment(number, body):
            row = {"id": 120000+sum(map(len, provider.comments.values())), "body":body}
            provider.comments[number].append(row)
            provider.writes.append(("DELP_STATUS_COMMENT",number))
            return copy.deepcopy(row)
        provider.post_comment = post_comment
        def patch_comment(number, body):
            for n, comments in provider.comments.items():
                for x in comments:
                    if x["id"] == number:
                        x["body"] = body
                        provider.writes.append(("DELP_STATUS_COMMENT",n))
                        return copy.deepcopy(x)
            raise AssertionError("managed comment not present")
        provider.patch_comment = patch_comment
        def patch_title(number, title):
            provider.issues[number]["title"] = title
            provider.writes.append(("DELP_ISSUE_TITLE",number))
            return copy.deepcopy(provider.issues[number])
        provider.patch_title = patch_title
        def patch_issue_body(number, body):
            provider.issues[number]["body"] = body
            provider.writes.append(("ISSUE_BODY_ONLY",number))
            return copy.deepcopy(provider.issues[number])
        provider.patch_issue_body = patch_issue_body
        def patch_pull_title_body(number, title, body):
            assert number == 740
            provider.pull["title"], provider.pull["body"] = title,body
            provider.writes.append(("PR_TITLE_BODY_ONLY",number))
            return copy.deepcopy(provider.pull)
        provider.patch_pull_title_body = patch_pull_title_body
        return provider

    def test_37_actual_single_writer_end_to_end_hosted_fake(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._writing_provider()
        before = replay.live_readback(self.manifest,live,provider)
        result = replay.guarded_publish(self.manifest,live,provider,
            expected_head=before["candidate_sha"],
            expected_input_digest=before["source_input_digest"],apply=True)
        self.assertEqual("VERIFIED_ALL_SURFACES",result["status"])
        self.assertEqual("MATCH",result["verified_readback"])
        self.assertEqual(["Common#733","Common#718","Common#740"],result["applied_surfaces"])
        self.assertEqual("WRITTEN",result["delp_issue_status"]["Common#733"]["status"])
        self.assertEqual("WRITTEN",result["delp_issue_status"]["Common#718"]["status"])
        self.assertEqual([("DELP_STATUS_COMMENT",733),("DELP_ISSUE_TITLE",733),
            ("DELP_STATUS_COMMENT",718),("ISSUE_BODY_ONLY",733),
            ("ISSUE_BODY_ONLY",718),("PR_TITLE_BODY_ONLY",740)], provider.writes)
        for n in (718,733):
            self.assertIn("Human Owner specification preserved",provider.issues[n]["body"])
            self.assertIn("relay-v32:issue-read-view:start",provider.issues[n]["body"])
            self.assertEqual(1,len(provider.comments[n]))
        self.assertIn("Human PR rationale preserved",provider.pull["body"])
        self.assertIn("HEAD:ccccccc",provider.pull["title"])
        self.assertEqual([],result["authority_effects"])

    def test_38_concurrent_human_edit_after_DELP_title_fails_without_overwrite(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._writing_provider()
        initial = replay.live_readback(self.manifest,live,provider)
        prior_patch = provider.patch_title
        def human_races_title(number,title):
            row = prior_patch(number,title)
            provider.issues[number]["body"] += "\nHUMAN EDIT AFTER TITLE"
            return row
        provider.patch_title = human_races_title
        with self.assertRaises(replay.PublicationIncomplete) as error:
            replay.guarded_publish(self.manifest,live,provider,
                expected_head=initial["candidate_sha"],
                expected_input_digest=initial["source_input_digest"],apply=True)
        self.assertEqual("INCOMPLETE_SYNC",error.exception.report["status"])
        self.assertIn("PROVIDER_MOVED_AFTER_DELP_BEFORE_BODY",str(error.exception))
        self.assertIn("HUMAN EDIT AFTER TITLE",provider.issues[733]["body"])
        self.assertNotIn("relay-v32:pr-read-view:start",provider.pull["body"])
        self.assertFalse(any(x[0]=="PR_TITLE_BODY_ONLY" for x in provider.writes))

    def test_39_changed_PR_head_midflight_is_partial_not_false_green(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._writing_provider()
        initial = replay.live_readback(self.manifest,live,provider)
        prior_patch = provider.patch_issue_body
        def moved_head(number,body):
            row = prior_patch(number,body)
            provider.pull["head"]["sha"] = "d"*40
            return row
        provider.patch_issue_body = moved_head
        with self.assertRaises(replay.PublicationIncomplete) as error:
            replay.guarded_publish(self.manifest,live,provider,
                expected_head=initial["candidate_sha"],
                expected_input_digest=initial["source_input_digest"],apply=True)
        self.assertEqual("INCOMPLETE_SYNC",error.exception.report["status"])
        self.assertIn("PROVIDER_MOVED_BEFORE_PR_WRITE",str(error.exception))
        self.assertFalse(any(x[0]=="PR_TITLE_BODY_ONLY" for x in provider.writes))
        self.assertEqual("d"*40,provider.pull["head"]["sha"])

    def test_40_single_writer_second_run_idempotent_without_false_progress(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._writing_provider()
        first = replay.live_readback(self.manifest,live,provider)
        replay.guarded_publish(self.manifest,live,provider,
            expected_head=first["candidate_sha"],
            expected_input_digest=first["source_input_digest"],apply=True)
        original = list(provider.writes)
        second = replay.live_readback(self.manifest,live,provider)
        again = replay.guarded_publish(self.manifest,live,provider,
            expected_head=second["candidate_sha"],
            expected_input_digest=second["source_input_digest"],apply=True)
        self.assertEqual("VERIFIED_ALL_SURFACES",again["status"])
        self.assertEqual([],again["applied_surfaces"])
        self.assertEqual(original,provider.writes)
        self.assertEqual("UNCHANGED",again["delp_issue_status"]["Common#733"]["status"])
        self.assertEqual(0,second["semantic_progress"]["P"])
        self.assertEqual(0,second["semantic_progress"]["E"])

    def test_41_tampered_PR_write_readback_never_claims_complete(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._writing_provider()
        initial = replay.live_readback(self.manifest,live,provider)
        orig = provider.patch_pull_title_body
        def corrupt(number,title,body):
            return orig(number,title,body+"\nBROKEN")
        provider.patch_pull_title_body = corrupt
        with self.assertRaises(replay.PublicationIncomplete) as error:
            replay.guarded_publish(self.manifest,live,provider,
                expected_head=initial["candidate_sha"],
                expected_input_digest=initial["source_input_digest"],apply=True)
        self.assertIn("PROVIDER_FAILED_PR_READBACK",str(error.exception))
        self.assertEqual("INCOMPLETE_SYNC",error.exception.report["status"])


    def test_42_smart_title_owner_derived_from_graph_not_literal_issue_PR(self):
        import delp_projection_v32 as delp
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        self.assertEqual(("Common#718","Common#733"),
                         delp._source_view_title_contract(live))
        moved = copy.deepcopy(live)
        moved["programme"]["id"] = "ANOTHER-REPO-RELEASE"
        moved["programme"]["root"] = "Another#10"
        leaf = next(n for n in moved["nodes"] if n.get("responsibility_id")=="R-PROJECTION")
        leaf["ref"] = "Another#20"
        leaf["primary_pr"] = "Another#30"
        binding = next(b for b in moved["programme"]["decomposition_proposal"]["bindings"]
                       if b["responsibility_id"]=="R-PROJECTION")
        binding["ref"] = "Another#20"
        self.assertEqual(("Another#10","Another#20"),
                         delp._source_view_title_contract(moved))
        del leaf["primary_pr"]
        self.assertIsNone(delp._source_view_title_contract(moved))

    def test_43_frozen_unbound_graph_does_not_require_smart_title_policy(self):
        import delp_projection_v32 as delp
        self.assertIsNone(delp._source_view_title_contract(self.graph))
        store=delp.InMemoryStore()
        report=delp.sync_projection(store,self.graph,lambda:[],lambda:{},{})
        self.assertEqual(set(report),set(n["ref"] for n in self.graph["nodes"]))
        self.assertTrue(all(v["status"]=="WRITTEN" for v in report.values()))


    def test_44_live_readback_uses_source_bound_C4_S6_progress_title(self):
        live=json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        report=replay.live_readback(self.manifest,live,self._provider())
        self.assertEqual("MATCH",report["read_views"]["Common#718"]["title"])
        self.assertEqual("MATCH",report["read_views"]["Common#733"]["title"])
        self.assertIn("D0/E0",report["read_views"]["Common#718"]["expected"])
        self.assertIn("P0/E0",report["read_views"]["Common#733"]["expected"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED",report["reconciliation"])
        self.assertEqual([],report["authority_effects"])


    def test_46_live_fixture_title_tracks_released_reserve_without_rewriting_golden(self):
        current = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        alternate = copy.deepcopy(current)
        root = next(n for n in alternate["nodes"] if n["kind"] == "ROOT")
        root["reserve_weight"] = 7
        observed = self._provider(graph=alternate).get_issue(718)["title"]
        self.assertIn("RESERVE7", observed)
        self.assertNotIn("RESERVE7", self._provider(graph=current).get_issue(718)["title"])
        frozen = replay.replay(self.manifest, self.graph)
        self.assertIn("RESERVE35", frozen["parent_actual_title"])

    def test_45_future_released_leaf_is_provider_bound_without_test_allowlist_edit(self):
        """The fake observes governed material, but refuses undeclared PR identities."""
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        declared = {
            int(n["primary_pr"].rsplit("#", 1)[1])
            for n in live["nodes"]
            if n["kind"] == "LEAF" and n.get("primary_pr")
        }
        provider = self._provider(graph=live)
        self.assertTrue(declared)
        for number in declared:
            self.assertEqual(number, provider.get_pull(number)["number"])
        import delp_projection_v32 as delp
        observed = delp.observe_github(provider, live)
        new_leaf = next(n["ref"] for n in live["nodes"]
                        if n.get("responsibility_id") == "R-RECONSTRUCTION")
        self.assertEqual("e" * 40, observed[new_leaf]["candidate_sha"])
        with self.assertRaisesRegex(AssertionError, "unapproved fake PR"):
            provider.get_pull(98764)

        # Challenge graph-selected binding rather than specifically whitelisting
        # newly released C4 PR #800 in the provider fixture.
        modified = copy.deepcopy(live)
        leaf = next(n for n in modified["nodes"] if n.get("responsibility_id") == "R-RECONSTRUCTION")
        previous = int(leaf["primary_pr"].rsplit("#", 1)[1])
        leaf["primary_pr"] = "Common#98765"
        future = self._provider(graph=modified)
        self.assertEqual(98765, future.get_pull(98765)["number"])
        with self.assertRaisesRegex(AssertionError, "unapproved fake PR"):
            future.get_pull(previous)

    def test_47_live_readback_leaf_793_graph_derived(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._provider(graph=live)
        # 793 has bound primary PR Common#800
        report = replay.live_readback(self.manifest, live, provider, selected_leaf="Common#793")
        self.assertEqual("Common#793", report["selected_leaf"])
        self.assertEqual("BOUND", report["pr_binding"])
        self.assertIn("Common#793", report["read_views"])
        self.assertIn("Common#800", report["read_views"])
        self.assertEqual([], report["authority_effects"])

    def test_48_title_without_dash_delimiter_parses_safely(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        provider = self._provider(graph=live, child_title="Plain Human Title Without Dash")
        report = replay.live_readback(self.manifest, live, provider)
        self.assertEqual("DRIFT", report["read_views"]["Common#733"]["title"])
        self.assertEqual("DRIFT_OR_UNPUBLISHED", report["reconciliation"])


    def test_49_plain_owner_title_with_em_dash_keeps_entire_human_text(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        whole = "Scope A — Engineering constraints"
        report = replay.live_readback(
            self.manifest, live, self._provider(graph=live, child_title=whole)
        )
        self.assertTrue(
            report["read_views"]["Common#733"]["expected"].endswith(" — " + whole),
            report["read_views"]["Common#733"]["expected"],
        )

    def test_50_undeclared_leaf_fails_before_any_provider_access(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        class Trap:
            def __getattr__(self, key):
                raise AssertionError("PROVIDER_MUST_NOT_BE_CONTACTED:" + key)
        with self.assertRaisesRegex(replay.ReplayError, "SELECTED_RESPONSIBILITY_NOT_BOUND"):
            replay.live_readback(self.manifest, live, Trap(), selected_leaf="Common#99999")


    def test_51_new_leaf_cannot_bypass_unreleased_writer_scope(self):
        """Graph-selected READ does not grant #793 LIVE_STATUS/title write authority."""
        import delp_projection_v32 as delp
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        observations = {
            "Common#793": {"candidate_sha": "e" * 40, "pr_state": "OPEN"},
        }
        snap = replay.view.build_views(
            live, self.manifest, selected_leaf="Common#793", phase="C4",
            human_titles={"Common#718": "Evidence Spine", "Common#793": "Handover", "PR": "Source View"},
            draft_pr={"number": 800, "head_sha": "e" * 40, "lifecycle": "OPEN"},
            observations=observations, title_contract="C4-S6",
        )
        store = delp.InMemoryStore()
        with self.assertRaisesRegex(delp.DelpError, "SOURCE_SMART_TITLE_POLICY_REQUIRED"):
            delp.sync_projection(
                store, live, lambda: [], lambda: observations,
                {"Common#718": "Evidence Spine", "Common#793": "Handover"},
                title_overrides=snap["issue_titles"],
                selected_refs=("Common#718", "Common#793"),
                expected_input_digest=snap["delp_input_digest"],
            )
        self.assertEqual([], store.writes)


if __name__ == "__main__":
    unittest.main()

