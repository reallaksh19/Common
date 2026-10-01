import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


cp = load("continuity_projection", ROOT / "scripts" / "continuity_projection.py")
compat = load("compatibility_v32", ROOT / "scripts" / "compatibility_v32.py")


class AuditedRealityReplayTests(unittest.TestCase):
    def test_reality_c_375_six_commit_semantic_gap_is_immediately_visible(self):
        snapshot = cp.new_snapshot(
            "Grade9V3#379",
            [{"id": f"STEP-{i:02d}"} for i in range(1, 11)],
            "issuecomment-5927240816",
            "a57f8991c086dd1cde49e1b3a43c2f864e7d38ae",
            "e71d66133a9c6be14702c74141c18d8131f9e882",
            6,
        )
        self.assertEqual(snapshot["frontier"]["relation"], "MATERIAL_AHEAD")
        self.assertEqual(snapshot["frontier"]["delta_commits"], 6)
        self.assertEqual(snapshot["progress"]["progress_percent"], 0)
        recovered = cp.event(snapshot, "stream-loss")
        self.assertTrue(recovered["recovery"]["recovery_evidence_required"])

    def test_reality_a_376_24_commit_distance_is_visibility_not_progress(self):
        snapshot = cp.new_snapshot(
            "Grade9V3#376",
            [{"id": "AUDIT"}],
            "historical-audit-basis",
            "7fbf2178f93578fae110924ada04418d5fd568cd",
            "896bf786c9615d45b3b6639d44e52dc252b96a08",
            24,
        )
        self.assertEqual(snapshot["frontier"]["relation"], "MATERIAL_AHEAD")
        self.assertEqual(snapshot["frontier"]["delta_commits"], 24)
        self.assertEqual(snapshot["progress"]["progress_percent"], 0)
        self.assertEqual(snapshot["progress"]["evidence_percent"], 0)

    def test_reality_b_377_legacy_result_never_guesses_responsibility_complete(self):
        legacy = compat.normalize_task_result({"outcome": "ACHIEVED"})
        self.assertEqual(legacy["result_scope"], "UNKNOWN")
        self.assertEqual(legacy["coverage"], "UNKNOWN")
        self.assertIsNone(legacy["responsibility_complete"])
        self.assertTrue(legacy["compatibility_inferred"])

        explicit = compat.normalize_task_result(
            {
                "RESULT_SCOPE": "RESPONSIBILITY",
                "COVERAGE": "10/10",
                "RESPONSIBILITY_COMPLETE": "YES",
            }
        )
        self.assertTrue(explicit["responsibility_complete"])
        self.assertEqual(explicit["result_scope"], "RESPONSIBILITY")

    def test_clean_path_adds_start_observability_but_no_progress_or_heartbeat(self):
        snapshot = cp.new_snapshot(
            "clean#1",
            [{"id": "UNIT-01"}, {"id": "UNIT-02"}],
            "plan-ref",
            "head-a",
            "head-a",
            0,
        )
        started = cp.event(snapshot, "implementation-start")
        self.assertEqual(started["state"], "IMPLEMENTING")
        self.assertEqual(started["progress"]["progress_percent"], 0)
        self.assertEqual(started["progress"]["evidence_percent"], 0)
        self.assertTrue(started["observability"]["provider_sync_required"])
        with self.assertRaises(cp.ContinuityError):
            cp.event(started, "timer")

    def test_fast_recovery_first_line_is_six_steps_with_explicit_deep_fallback(self):
        self.assertEqual(len(compat.FAST_RECOVERY_STEPS), 6)
        self.assertEqual(compat.FAST_RECOVERY_STEPS[4], "TASK_EVIDENCE_RECOVERY")
        self.assertGreaterEqual(len(compat.DEEP_RECOVERY_TRIGGERS), 1)


if __name__ == "__main__":
    unittest.main()
