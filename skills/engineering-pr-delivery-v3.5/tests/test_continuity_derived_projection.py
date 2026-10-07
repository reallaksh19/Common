"""DERIVED_FROM_FACTS continuity snapshots: agents publish facts, never the E flag or the title."""

import importlib.util
import json
import pathlib
import tempfile
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "continuity_projection.py"
spec = importlib.util.spec_from_file_location("continuity_projection_derived", MODULE_PATH)
cp = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(cp)

SHA_A = "a" * 40
SHA_B = "b" * 40
REF = "Common#592#issuecomment-12"


def derived(units=None, material=SHA_A, semantic=SHA_A, delta=0, **kwargs):
    return cp.new_snapshot(
        "owner/repo#592",
        units or [{"id": "U01", "weight": 20}, {"id": "U02", "weight": 30}, {"id": "U03", "weight": 50}],
        "issuecomment-plan",
        material,
        semantic,
        delta,
        projection_mode=cp.PROJECTION_DERIVED,
        **kwargs,
    )


class DerivedFromFactsTests(unittest.TestCase):
    def test_agent_cannot_assert_evidenced_when_declaring_units(self):
        with self.assertRaises(cp.ContinuityError):
            derived([{"id": "U01", "complete": True, "evidenced": True}])

    def test_unit_update_rejects_the_evidenced_flag(self):
        with self.assertRaises(cp.ContinuityError):
            cp.event(derived(), "unit-update", unit_id="U01", complete=True, evidenced=True)

    def test_evidence_needs_refs_and_a_candidate_equal_to_the_observed_head(self):
        s = cp.event(derived(), "unit-update", unit_id="U01", complete=True)
        self.assertEqual((20, 0), (s["progress"]["progress_percent"], s["progress"]["evidence_percent"]))
        s = cp.event(s, "unit-update", unit_id="U01", evidence_refs=[REF])
        self.assertEqual(0, s["progress"]["evidence_percent"])  # refs but no candidate
        s = cp.event(s, "unit-update", unit_id="U01", evidence_candidate=SHA_B)
        self.assertEqual(0, s["progress"]["evidence_percent"])  # candidate is not the observed head
        s = cp.event(s, "unit-update", unit_id="U01", evidence_candidate=SHA_A)
        self.assertEqual((20, 20), (s["progress"]["progress_percent"], s["progress"]["evidence_percent"]))
        self.assertTrue(s["units"][0]["evidenced"])

    def test_evidence_cannot_lead_completion(self):
        s = cp.event(derived(), "unit-update", unit_id="U01", evidence_refs=[REF], evidence_candidate=SHA_A)
        self.assertFalse(s["units"][0]["evidenced"])
        self.assertEqual(0, s["progress"]["evidence_percent"])

    def test_candidate_must_be_a_full_commit(self):
        with self.assertRaises(cp.ContinuityError):
            cp.event(derived(), "unit-update", unit_id="U01", evidence_candidate="abc123")

    def test_a_moved_head_drops_E_but_keeps_P_until_evidence_is_republished(self):
        s = cp.event(derived(), "unit-update", unit_id="U01", complete=True, evidence_refs=[REF], evidence_candidate=SHA_A)
        self.assertEqual(20, s["progress"]["evidence_percent"])
        s["frontier"] = cp.frontier(SHA_B, SHA_A, 3)
        s = cp.reproject(s)
        self.assertEqual((20, 0), (s["progress"]["progress_percent"], s["progress"]["evidence_percent"]))
        s = cp.event(s, "unit-update", unit_id="U01", evidence_candidate=SHA_B)
        self.assertEqual(20, s["progress"]["evidence_percent"])

    def test_reopening_a_unit_clears_its_evidence(self):
        s = cp.event(derived(), "unit-update", unit_id="U01", complete=True, evidence_refs=[REF], evidence_candidate=SHA_A)
        s = cp.event(s, "unit-update", unit_id="U01", complete=False)
        self.assertEqual([], s["units"][0]["evidence_refs"])
        self.assertEqual(0, s["progress"]["progress_percent"])

    def test_weights_are_honoured_and_percent_is_half_up_never_falsely_full(self):
        s = derived([{"id": "A", "weight": 1}, {"id": "B", "weight": 7}])
        s = cp.event(s, "unit-update", unit_id="A", complete=True)
        self.assertEqual(13, s["progress"]["progress_percent"])  # 12.5 -> half-up
        s = derived([{"id": "A", "weight": 1}, {"id": "B", "weight": 250}])
        s = cp.event(s, "unit-update", unit_id="B", complete=True)
        self.assertEqual(99, s["progress"]["progress_percent"])  # 250/251 must not display as 100

    def test_legacy_snapshots_stay_readable_and_unchanged(self):
        legacy = cp.new_snapshot("r", [{"id": "A", "complete": True, "evidenced": True}, {"id": "B"}], "p", "b", "a", 1)
        self.assertEqual(cp.PROJECTION_LEGACY, legacy["projection_mode"])
        self.assertEqual((50, 50), (legacy["progress"]["progress_percent"], legacy["progress"]["evidence_percent"]))
        self.assertIn("LEGACY_AGENT_ASSERTED", cp.markdown(legacy))

    def test_markdown_states_who_may_write_what(self):
        text = cp.markdown(derived())
        self.assertIn("PROJECTION_MODE: DERIVED_FROM_FACTS", text)
        self.assertIn("titles are written only by the DELP runner", text)

    def test_cli_init_defaults_to_derived_and_rejects_the_evidenced_flag(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "units.json").write_text(json.dumps([{"id": "U01"}, {"id": "U02"}]), encoding="utf-8")
            out = root / "snapshot.json"
            self.assertEqual(0, cp.main(["init", "--responsibility", "r", "--units", str(root / "units.json"), "--output", str(out)]))
            snapshot = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(cp.PROJECTION_DERIVED, snapshot["projection_mode"])
            with self.assertRaises(cp.ContinuityError):
                cp.main(["unit-update", "--snapshot", str(out), "--unit-id", "U01", "--evidenced", "YES", "--output", str(out)])

    def test_derived_sync_never_patches_the_issue_title(self):
        s = cp.new_snapshot(
            "owner/repo#10", [{"id": "A"}], "plan", SHA_A, SHA_A, 0, "owner/repo", 10, projection_mode=cp.PROJECTION_DERIVED
        )
        s = cp.event(s, "implementation-start")
        store = {"issue": {"title": "Hand written title", "number": 10}, "comments": []}
        calls = []
        old = (cp.gh_json, cp.gh_patch, cp.gh_post, cp.gh_comments)

        def fake_json(*args):
            endpoint = args[-1]
            calls.append(("GET", endpoint))
            if endpoint == "repos/owner/repo/issues/10":
                return dict(store["issue"])
            cid = int(endpoint.rsplit("/", 1)[1])
            return next(row for row in store["comments"] if row["id"] == cid)

        def fake_post(endpoint, payload):
            calls.append(("POST", endpoint))
            row = {"id": 100 + len(store["comments"]), "body": payload["body"]}
            store["comments"].append(row)
            return dict(row)

        def fake_patch(endpoint, payload):
            calls.append(("PATCH", endpoint))
            if endpoint == "repos/owner/repo/issues/10":
                store["issue"]["title"] = payload["title"]
            return {}

        cp.gh_json, cp.gh_post, cp.gh_patch = fake_json, fake_post, fake_patch
        cp.gh_comments = lambda repo, issue: [dict(row) for row in store["comments"]]
        try:
            synced = cp.sync_github(s)
        finally:
            cp.gh_json, cp.gh_patch, cp.gh_post, cp.gh_comments = old
        self.assertNotIn(("PATCH", "repos/owner/repo/issues/10"), calls)
        self.assertEqual("Hand written title", store["issue"]["title"])
        self.assertEqual("DELP_RUNNER", synced["observability"]["title_authority"])
        self.assertEqual("SYNCED", synced["observability"]["provider_sync"]["status"])


if __name__ == "__main__":
    unittest.main()
