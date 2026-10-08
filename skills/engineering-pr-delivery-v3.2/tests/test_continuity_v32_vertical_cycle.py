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
        self.assertEqual(frozen["programme"]["decomposition_proposal"],
                         live["programme"]["decomposition_proposal"])
        self.assertEqual(frozen["programme"]["acceptance_claims"],
                         live["programme"]["acceptance_claims"])
        self.assertEqual(frozen["nodes"][0]["reserve_weight"], live["nodes"][0]["reserve_weight"])
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
            "Common#733": "Issue/PR Views"})
        self.assertEqual(
            "🟡 [718] NEXT #733/C4 · RESERVE35 · FACTS UNREPORTED — V3.2 Evidence Spine",
            result["issue_titles"]["Common#718"])
        self.assertEqual(
            "🟡 [718›733] R-PROJECTION · C4 · PR#740 · UNMATERIALIZED — Issue/PR Views",
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


    def _provider(self, *, child_title=None, pr_title=None, moved=False):
        """Deterministic GitHub GET-only fake, with exact PR identity/readback."""
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
                "🟡 [718] NEXT #733/C4 · RESERVE35 · FACTS UNREPORTED — V3.2 Evidence Spine"
                if number == 718 else
                child_title or "🟡 [718›733] R-PROJECTION · C4 · PR#740 · UNMATERIALIZED — Issue/PR Views"
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

if __name__ == "__main__":
    unittest.main()
