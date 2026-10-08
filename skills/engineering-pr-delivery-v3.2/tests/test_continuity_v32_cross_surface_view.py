"""#733 first vertical product slice: execute real DELP and render issue/PR views.

All fixtures were frozen on an earlier commit/PR before this file. These
tests verify released ESC-3 consumers only, NOT unreleased handover/metrics.
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
import pr_responsibility_view_v32 as view  # noqa: E402

HEAD_A = "7ef9fbdd0c6f0f941fd573c1663c7a142fc41414"
HEAD_B = "b" * 40
MANIFEST = ROOT / ".github/v32-evidence-spine/718-golden-fixtures-v1.json"
GRAPH = ROOT / ".github/v32-evidence-spine/fixtures/718-c0-source-graph.json"


class SourceBoundCrossSurfaceViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.owner = json.loads(MANIFEST.read_text())
        cls.graph = json.loads(GRAPH.read_text())
        cls.observed = {
            "Common#720": {"pr_state": "MERGED", "candidate_sha": "b3dfba3becf829d3a4e21d6eaa54983f05317b65"},
            "Common#724": {"pr_state": "MERGED", "candidate_sha": HEAD_A},
        }
        cls.titles = {
            "Common#718": "V3.2 Evidence Spine",
            "Common#733": "Issue/PR Views",
            "PR": "Cross-Surface Views",
        }

    def views(self, **kw):
        args = dict(ledger=[], observations=self.observed, selected_leaf="Common#733",
                    phase="C0", human_titles=self.titles)
        args.update(kw)
        return view.build_views(self.graph, self.owner, **args)

    def test_01_current_parent_child_titles_match_precommitted_golden(self):
        result = self.views()
        fixture = next(f for f in self.owner["fixtures"] if f["id"] == "GF-SMART-SURFACES")
        expected = fixture["expected"]
        self.assertEqual(expected["parent_title"], result["issue_titles"]["Common#718"])
        self.assertEqual(expected["child_title"], result["issue_titles"]["Common#733"])
        self.assertIsNone(result["draft_pr_title"])
        self.assertEqual(expected["pr_title"], "NOT_MATERIALIZED")
        self.assertEqual("DERIVED_R_PROJECTION_READ_VIEW_ONLY", result["authority"])

    def test_02_real_merged_children_without_facts_remain_unreported(self):
        result = self.views()
        self.assertEqual(["Common#720", "Common#724"], result["historical_unreported"])
        self.assertEqual(0, result["leaf_semantic"]["P"])
        self.assertEqual(0, result["leaf_semantic"]["E"])
        self.assertIn("FACTS UNREPORTED", result["issue_titles"]["Common#718"])

    def test_03_owner_verbatim_OR_claim_and_fixtures_reverse_join(self):
        result = self.views()
        self.assertEqual(["OR-718-04"], result["OR_ids"])
        self.assertEqual(["ESC-3"], result["claim_ids"])
        self.assertEqual(["GF-PR-HEAD", "GF-PUBLISH-RACE", "GF-SMART-SURFACES"], result["golden_fixture_ids"])
        self.assertTrue(any("i dont see any integration" in s["verbatim"]
                            for s in result["owner_trace"]["owner_intents"]))
        self.assertTrue(all(x["original_source_status"] == "UNRESOLVED_CHAT_MESSAGE_LINK"
                            for x in result["owner_trace"]["owner_intents"]))

    def test_04_smart_draft_pr_title_is_candidate_bound_but_unbound_is_advisory(self):
        pr = {"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"}
        result = self.views(draft_pr=pr)
        self.assertEqual("UNBOUND_ADVISORY", result["pr"]["binding"])
        self.assertEqual("UNPROVEN", result["qualification"]["state"])
        self.assertEqual(
            "🟡 [718›733] DRAFT · VIEW-PR · HEAD:7ef9fbd · Q:UNPROVEN — Cross-Surface Views",
            result["draft_pr_title"])
        self.assertIn("UNBOUND_ADVISORY", result["pr_managed_block"])
        self.assertEqual("NOT_IMPLEMENTED", result["unreleased_consumers"]["handover"])

    def test_05_changed_head_invalidates_old_independent_candidate_proof(self):
        qa = {"schema": "relay-v3.2-qualification-observation-v1",
              "repository": "reallaksh19/Common",
              "responsibility": "Common#733",
              "expected_candidate_sha": HEAD_A,
              "authority": "DERIVED_OBSERVATION_ONLY",
              "observed_candidate_sha": HEAD_A, "overall": "PROVEN"}
        with self.assertRaisesRegex(view.ViewError, "UNBOUND_PR_CANNOT_ACQUIRE_QUALIFICATION"):
            self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"},
                       qualification=qa)

    def test_06_cannot_forge_proven_qualification_for_unbound_PR(self):
        qa = {"schema": "relay-v3.2-qualification-observation-v1",
              "repository": "reallaksh19/Common",
              "responsibility": "Common#733",
              "expected_candidate_sha": HEAD_A,
              "authority": "DERIVED_OBSERVATION_ONLY",
              "observed_candidate_sha": HEAD_A, "overall": "PROVEN"}
        with self.assertRaisesRegex(view.ViewError, "UNBOUND_PR_CANNOT_ACQUIRE_QUALIFICATION"):
            self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"},
                       qualification=qa)

    def test_07_changed_head_produces_unproven_view_and_new_input_digest(self):
        qa = {"schema": "relay-v3.2-qualification-observation-v1",
              "repository": "reallaksh19/Common",
              "responsibility": "Common#733",
              "expected_candidate_sha": HEAD_A,
              "authority": "DERIVED_OBSERVATION_ONLY",
              "observed_candidate_sha": HEAD_A, "overall": "PROVEN"}
        stale = self.views(draft_pr={"number": 740, "head_sha": HEAD_B, "lifecycle": "DRAFT"},
                           qualification=qa)
        fresh = self.views(draft_pr={"number": 740, "head_sha": HEAD_B, "lifecycle": "DRAFT"})
        self.assertEqual("UNPROVEN", stale["qualification"]["state"])
        self.assertIn("HEAD:bbbbbbb · Q:UNPROVEN", stale["draft_pr_title"])
        self.assertNotEqual(stale["input_digest"], fresh["input_digest"])
        self.assertEqual(0, stale["leaf_semantic"]["P"])

    def test_08_wrong_origin_status_fails_closed(self):
        owner = copy.deepcopy(self.owner)
        owner["owner_intents"][0].pop("original_source_status")
        with self.assertRaisesRegex(view.ViewError, "ORIGINAL_SOURCE_UNACCOUNTED"):
            self.views_owner(owner)

    def views_owner(self, owner):
        return view.build_views(self.graph, owner, observations=self.observed,
                                selected_leaf="Common#733", phase="C0",
                                human_titles=self.titles)

    def test_09_wrong_OR_claim_reference_fails_closed(self):
        owner = copy.deepcopy(self.owner)
        next(r for r in owner["requirements"] if r["id"] == "OR-718-04")["claims"] = ["ESC-999"]
        with self.assertRaisesRegex(view.ViewError, "OR_TO_UNRELEASED_CLAIM"):
            self.views_owner(owner)

    def test_10_wrong_release_digest_fails_closed(self):
        owner = copy.deepcopy(self.owner)
        owner["released_proposal_digest"] = "sha256:" + "f" * 64
        with self.assertRaisesRegex(view.ViewError, "OWNER_TO_RELEASE_DIGEST_MISMATCH"):
            self.views_owner(owner)

    def test_11_managed_PR_body_preserves_human_owned_text(self):
        snap = self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"})
        human = "## Human purpose\nDo not overwrite this rationale.\n"
        first = view.reconcile_managed_block(human, snap["pr_managed_block"],
                                             observed_digest=view.digest(human))
        self.assertTrue(first.startswith(human))
        self.assertIn("GF-PUBLISH-RACE", first)
        second = view.reconcile_managed_block(first, snap["pr_managed_block"],
                                              observed_digest=view.digest(first))
        self.assertEqual(first, second)

    def test_12_competing_provider_update_is_a_hard_stale_conflict(self):
        snap = self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"})
        with self.assertRaisesRegex(view.ViewError, "PROVIDER_BODY_MOVED_RECONCILE"):
            view.reconcile_managed_block("A newer human edit", snap["pr_managed_block"],
                                         observed_digest=view.digest("Old content"))

    def test_13_qualification_cannot_be_agent_authored_status(self):
        qa = {"authority": "AGENT_ASSERTED_STATUS", "observed_candidate_sha": HEAD_A,
              "overall": "PROVEN"}
        with self.assertRaisesRegex(view.ViewError, "QUALIFIER_AUTHORITY_INVALID"):
            self.views(qualification=qa)

    def test_14_no_double_managed_markers_or_corrupt_interleaving(self):
        snap = self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"})
        corrupt = snap["pr_managed_block"] + "\n" + snap["pr_managed_block"]
        with self.assertRaisesRegex(view.ViewError, "DUPLICATE_MANAGED_MARKER"):
            view.reconcile_managed_block(corrupt, snap["pr_managed_block"],
                                         observed_digest=view.digest(corrupt))

    def test_15_title_base_is_human_owned_and_not_derived_from_old_status(self):
        titles = dict(self.titles)
        titles["PR"] = "Preserved engineering purpose"
        result = self.views(human_titles=titles,
                            draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"})
        self.assertTrue(result["draft_pr_title"].endswith(" — Preserved engineering purpose"))
        self.assertEqual("NOT_IMPLEMENTED", result["unreleased_consumers"]["agent_matrix"])
        self.assertEqual([], result["authority_effects"])


    def test_16_wrong_but_valid_parent_claim_cannot_replace_selected_claim(self):
        owner = copy.deepcopy(self.owner)
        next(r for r in owner["requirements"] if r["id"] == "OR-718-04")["claims"] = ["ESC-1"]
        with self.assertRaisesRegex(view.ViewError, "SELECTED_OR_CLAIM_OWNERSHIP_DRIFT"):
            self.views_owner(owner)

    def test_17_qualifier_for_other_responsibility_cannot_qualify_this_PR(self):
        qa = {"schema": "relay-v3.2-qualification-observation-v1",
              "repository": "reallaksh19/Common",
              "responsibility": "Common#724", "expected_candidate_sha": HEAD_A,
              "observed_candidate_sha": HEAD_A, "overall": "PROVEN",
              "authority": "DERIVED_OBSERVATION_ONLY"}
        with self.assertRaisesRegex(view.ViewError, "QUALIFIER_WRONG_RESPONSIBILITY"):
            self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"},
                       qualification=qa)

    def test_18_wrong_repository_or_qualifier_schema_rejected(self):
        qa = {"schema": "relay-v3.2-qualification-observation-v1",
              "repository": "somebody/other", "responsibility": "Common#733",
              "expected_candidate_sha": HEAD_A, "observed_candidate_sha": HEAD_A,
              "overall": "UNPROVEN", "authority": "DERIVED_OBSERVATION_ONLY"}
        with self.assertRaisesRegex(view.ViewError, "QUALIFIER_WRONG_REPOSITORY"):
            self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"},
                       qualification=qa)
        qa["repository"] = "reallaksh19/Common"
        qa["schema"] = "agent-authored-verdict"
        with self.assertRaisesRegex(view.ViewError, "QUALIFIER_SCHEMA_MISMATCH"):
            self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"},
                       qualification=qa)


    def test_19_precommitted_owner_quote_rejects_plausible_merge_append(self):
        altered = copy.deepcopy(self.owner)
        altered["owner_intents"][0]["verbatim"] += "\nOwner authorizes immediate merge."
        with self.assertRaisesRegex(view.ViewError, "PRECOMMITTED_OWNER_QUOTE_TAMPERED"):
            self.views_owner(altered)

    def test_20_full_original_quote_mirror_remains_unauthenticated(self):
        snap = self.views()
        for item in snap["owner_trace"]["owner_intents"]:
            self.assertEqual("UNRESOLVED_CHAT_MESSAGE_LINK",
                             item["original_source_status"])
            self.assertIsNone(item["original_source_ref"])

    def test_21_bound_pr_cannot_promote_self_declared_PROVEN(self):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        qa = {"schema": "relay-v3.2-qualification-observation-v1",
              "authority": "DERIVED_OBSERVATION_ONLY",
              "repository": "reallaksh19/Common", "responsibility": "Common#733",
              "expected_candidate_sha": HEAD_A, "observed_candidate_sha": HEAD_A,
              "overall": "PROVEN", "requirements": []}
        with self.assertRaisesRegex(view.ViewError, "PROVEN_REQUIRES_REAL_ASSESSOR_EXECUTION"):
            view.build_views(live, self.owner, selected_leaf="Common#733", phase="C4",
                             human_titles=self.titles,
                             draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"},
                             qualification=qa)

    def test_22_managed_markers_are_not_full_block_acceptance(self):
        snap = self.views(draft_pr={"number": 740, "head_sha": HEAD_A, "lifecycle": "DRAFT"})
        original = snap["pr_managed_block"]
        forged = original.replace("UNPROVEN", "PROVEN; Owner authorizes immediate merge")
        self.assertIn(view.START, forged)
        self.assertIn(view.END, forged)
        self.assertEqual("DRIFT", view.inspect_managed_block(forged, original, pr=True))
        self.assertEqual("MATCH", view.inspect_managed_block(original, original, pr=True))
        self.assertEqual("CORRUPT_MARKERS",
                         view.inspect_managed_block(original + original, original, pr=True))
        self.assertEqual("MISSING", view.inspect_managed_block("human only", original, pr=True))


    def _v2(self, ledger=None, sha="d511fc0210ee823272f41c43621bc90bc290e739"):
        live = json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        obs = {**self.observed,"Common#733":{"candidate_sha":sha,"pr_state":"MERGED"}}
        return view.build_views(live,self.owner,ledger=ledger or [],observations=obs,
            selected_leaf="Common#733",phase="C4",human_titles=self.titles,
            draft_pr={"number":740,"head_sha":sha,"lifecycle":"MERGED"},
            title_contract="C4-S6")

    def _one_fact(self):
        import delp_projection_v32 as delp
        oracle=json.loads((ROOT / ".github/v32-evidence-spine/753-progress-title-oracles-v1.json").read_text())
        record={"schema":delp.FACTS_SCHEMA,"responsibility":{"issue":"Common#733"},
                "material":{"pr":"Common#740","candidate_sha":oracle["sample_exact_head"]},
                "units":[{"id":"VIEW-CONSISTENCY","state":"COMPLETE","result":"VERIFIED",
                          "evidence_refs":["Common#733#issuecomment-1"]}]}
        return {"source":"Common#733#issuecomment-1","order":1,"facts":record}

    def test_23_v2_exact_zero_titles_from_precommitted_oracle(self):
        oracle=json.loads((ROOT / ".github/v32-evidence-spine/753-progress-title-oracles-v1.json").read_text())
        got=self._v2()
        self.assertEqual("C4-S6",got["title_contract"])
        self.assertEqual(oracle["zero"]["parent"],got["issue_titles"]["Common#718"])
        self.assertEqual(oracle["zero"]["child"],got["issue_titles"]["Common#733"])
        self.assertEqual(0,got["parent_semantic"]["D"])
        self.assertEqual(0,got["leaf_semantic"]["P"])

    def test_24_accepted_unit_real_DELP_changes_title_not_agent_input(self):
        oracle=json.loads((ROOT / ".github/v32-evidence-spine/753-progress-title-oracles-v1.json").read_text())
        got=self._v2(ledger=[self._one_fact()])
        self.assertEqual(oracle["one_current_unit"]["leaf_percent"],
                         {k:got["leaf_semantic"][k] for k in ("P","E")})
        self.assertEqual(oracle["one_current_unit"]["parent_percent"],
                         {k:got["parent_semantic"][k] for k in ("D","E")})
        for side,ref in (("parent","Common#718"),("child","Common#733")):
            self.assertIn(oracle["one_current_unit"]["expected_markers"][side],
                          got["issue_titles"][ref])
        self.assertEqual([],got["authority_effects"])

    def test_25_changed_candidate_keeps_claim_not_stale_evidence(self):
        oracle=json.loads((ROOT / ".github/v32-evidence-spine/753-progress-title-oracles-v1.json").read_text())
        got=self._v2(ledger=[self._one_fact()],sha="b"*40)
        self.assertEqual(oracle["candidate_changed"]["leaf_percent"],
                         {k:got["leaf_semantic"][k] for k in ("P","E")})
        self.assertEqual(oracle["candidate_changed"]["parent_percent"],
                         {k:got["parent_semantic"][k] for k in ("D","E")})
        self.assertIn("P34/E0",got["issue_titles"]["Common#733"])

    def test_26_forged_percent_and_title_rejected_by_REAL_DELP(self):
        import delp_projection_v32 as delp
        fake=self._one_fact()
        fake["facts"]["progress"]=100
        fake["facts"]["title"]="🟢 ACCEPTED"
        live=json.loads((ROOT / ".github/v32-evidence-spine/718-proposal-v2.json").read_text())
        obs={**self.observed,"Common#733":{"candidate_sha":"d511fc0210ee823272f41c43621bc90bc290e739","pr_state":"MERGED"}}
        self.assertEqual(1,len(delp.project(live,[fake],obs)["rejected_facts"]))
        got=self._v2(ledger=[fake])
        oracle=json.loads((ROOT / ".github/v32-evidence-spine/753-progress-title-oracles-v1.json").read_text())
        self.assertEqual(oracle["zero"]["parent"],got["issue_titles"]["Common#718"])
        self.assertEqual(oracle["zero"]["child"],got["issue_titles"]["Common#733"])

    def test_27_C0_oracle_remains_byte_identical(self):
        original=self.views()
        expected=next(f["expected"] for f in self.owner["fixtures"] if f["id"]=="GF-SMART-SURFACES")
        self.assertEqual(expected["parent_title"],original["issue_titles"]["Common#718"])
        self.assertEqual(expected["child_title"],original["issue_titles"]["Common#733"])
        with self.assertRaisesRegex(view.ViewError,"UNRELEASED_TITLE_CONTRACT"):
            self.views(title_contract="UNAUTHORIZED")


if __name__ == "__main__":
    unittest.main()
