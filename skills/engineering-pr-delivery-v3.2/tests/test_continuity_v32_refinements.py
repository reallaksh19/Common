import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "continuity_projection.py"
spec = importlib.util.spec_from_file_location("continuity_projection_refinements", MODULE_PATH)
cp = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(cp)


PROTOCOL_REF = (
    "reallaksh19/Common@c48bf987a2ea4523ed556ebdbcc627b1aafea1c0:"
    "skills/engineering-pr-delivery-v3.2"
)


def snapshot(material="b", semantic="a", delta=1):
    return cp.new_snapshot(
        "owner/repo#10",
        [{"id": "UNIT-01", "complete": False, "evidenced": False}],
        "issuecomment-plan",
        material,
        semantic,
        delta,
        protocol_ref=PROTOCOL_REF,
    )


class PostMockContinuityRefinementTests(unittest.TestCase):
    def test_protocol_ref_is_stored_and_rendered_for_successor(self):
        current = snapshot(material="a", semantic="a", delta=0)
        self.assertEqual(current["protocol_ref"], PROTOCOL_REF)
        rendered = cp.markdown(current)
        self.assertIn(f"PROTOCOL_REF: {PROTOCOL_REF}", rendered)

    def test_material_ahead_is_passive_reconciliation_need_not_active_recovery(self):
        current = snapshot()
        self.assertTrue(current["frontier"]["recovery_reconciliation_needed"])
        self.assertEqual(current["recovery"]["mode"], "NONE")
        self.assertFalse(current["recovery"]["recovery_evidence_required"])
        rendered = cp.markdown(current)
        self.assertIn("reconciliation_needed=true", rendered)
        self.assertIn("mode=NONE", rendered)
        self.assertIn("evidence_required=false", rendered)

    def test_successor_recovery_start_turns_gap_into_active_evidence_obligation(self):
        recovering = cp.event(
            snapshot(),
            "recovery-start",
            mode="FRONTIER_RECONCILIATION",
        )
        self.assertEqual(recovering["state"], "RECOVERING")
        self.assertEqual(
            recovering["recovery"]["mode"],
            "FRONTIER_RECONCILIATION",
        )
        self.assertTrue(recovering["recovery"]["recovery_evidence_required"])
        self.assertEqual(
            recovering["observability"]["update_reason"],
            "RECOVERY_START",
        )

    def test_frontier_recovery_start_rejects_aligned_frontier(self):
        with self.assertRaisesRegex(
            cp.ContinuityError,
            "requires unresolved frontier",
        ):
            cp.event(
                snapshot(material="a", semantic="a", delta=0),
                "recovery-start",
                mode="FRONTIER_RECONCILIATION",
            )

    def test_stream_loss_uses_interrupted_executor_mode(self):
        recovering = cp.event(snapshot(), "stream-loss")
        self.assertEqual(
            recovering["recovery"]["mode"],
            "INTERRUPTED_EXECUTOR",
        )
        self.assertTrue(recovering["recovery"]["recovery_evidence_required"])

    def test_readback_clears_recovery_mode_and_reconciliation_need(self):
        recovering = cp.event(
            snapshot(),
            "recovery-start",
            mode="FRONTIER_RECONCILIATION",
        )
        pending = cp.event(recovering, "recovery-evidence", claim="Recovered B.")
        final = cp.finalize_recovery_evidence(pending, 123)
        self.assertEqual(final["recovery"]["mode"], "NONE")
        self.assertFalse(final["recovery"]["recovery_evidence_required"])
        self.assertFalse(final["frontier"]["recovery_reconciliation_needed"])
        self.assertEqual(final["frontier"]["relation"], "ALIGNED")
        self.assertEqual(
            final["recovery"]["recovery_evidence"]["provider_comment_id"],
            123,
        )


if __name__ == "__main__":
    unittest.main()
