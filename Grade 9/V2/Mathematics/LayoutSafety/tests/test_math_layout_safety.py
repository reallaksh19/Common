#!/usr/bin/env python3
"""Falsifier suite for typography and layout safety (M-UPGRADE-2 item 7).

Every mutation is a defect the seven-topic stress test actually produced: type below the
readable minimum for its role, microtype beside unused space, two siblings overlapping,
measured content larger than its allocated rectangle, a workspace that ignores the response
the question demands, and fixed-density solution packing.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

PHASE = Path(__file__).resolve().parents[1]
MATH = PHASE.parent
sys.path[:0] = [str(PHASE / "engine"), str(PHASE / "fixtures"),
                str(MATH / "SourceLedger" / "engine")]

from validate_layout_safety import (  # noqa: E402
    FALSIFIERS,
    assert_layout_safe,
    audit_layout,
    load,
    measure_then_pack,
)

PROBE = load(PHASE / "fixtures" / "math-layout-probe.fixture.json")
REGISTRY = load(PHASE / "registry" / "math-typography-role-registry.json")
POLICY = load(PHASE / "policies" / "math-layout-safety-policy.json")
AUDIT_SCHEMA = json.loads((PHASE / "contracts" / "math-layout-audit.schema.json")
                          .read_text(encoding="utf-8"))
MAP_SCHEMA = json.loads((MATH / "SourceLedger" / "contracts"
                         / "math-rendered-object-map.schema.json")
                        .read_text(encoding="utf-8"))
PRINTABLE_H = PROBE["page_height_pt"] - 2 * PROBE["printable_margin_pt"]


def probe() -> dict:
    return copy.deepcopy(PROBE)


def find(object_map: dict, object_id: str) -> dict:
    return next(o for o in object_map["objects"] if o["object_id"] == object_id)


class LayoutPositive(unittest.TestCase):
    def test_probe_validates_against_the_shared_object_map_contract(self):
        Draft202012Validator(MAP_SCHEMA).validate(PROBE)

    def test_audit_passes_and_validates(self):
        audit = assert_layout_safe(probe())
        self.assertEqual(audit["status"], "PASS")
        Draft202012Validator(AUDIT_SCHEMA).validate(audit)

    def test_minimum_size_is_per_role_not_a_global_floor(self):
        """A 9.0pt diagram label is fine; a 9.0pt question body is not."""
        self.assertLess(REGISTRY["roles"]["DIAGRAM_LABEL"]["min_pt"],
                        REGISTRY["roles"]["QUESTION_BODY"]["min_pt"])
        label = find(probe(), "Q2/figure/label-A")
        self.assertEqual(label["font_size_pt"], 9.0)
        ok = probe()
        assert_layout_safe(ok)          # 9.0pt is legal for DIAGRAM_LABEL
        bad = probe()
        find(bad, "Q2/stem")["font_size_pt"] = 9.0
        with self.assertRaises(ValueError):
            assert_layout_safe(bad)     # the same 9.0pt is illegal for QUESTION_BODY

    def test_containment_is_not_a_collision(self):
        """A subpart inside its question panel overlaps it completely and is legal."""
        panel = find(probe(), "Q2/panel")
        child = find(probe(), "Q2/proof-1")
        self.assertEqual(child["container_id"], panel["object_id"])
        self.assertGreaterEqual(child["box"]["x"], panel["box"]["x"])
        self.assertEqual(audit_layout(probe())["collisions"]["intersections"], [])

    def test_solution_packing_is_measured_then_packed(self):
        gap = REGISTRY["solution_packing_policy"]["inter_block_gap_pt"]
        blocks = [{"block_id": "a", "height_pt": 322.0},
                  {"block_id": "b", "height_pt": 358.0}]
        self.assertEqual(measure_then_pack(blocks, PRINTABLE_H, gap), [["a", "b"]])
        # one tall solution legitimately takes a whole page
        tall = [{"block_id": "a", "height_pt": 600.0},
                {"block_id": "b", "height_pt": 400.0}]
        self.assertEqual(measure_then_pack(tall, PRINTABLE_H, gap), [["a"], ["b"]])

    def test_workspace_follows_response_mode(self):
        workspaces = {o["object_id"]: o for o in PROBE["objects"]
                      if o["kind"] == "WORKSPACE"}
        self.assertEqual(workspaces["Q2/workspace"]["response_mode"], "PROOF")
        self.assertEqual(workspaces["Q3/workspace"]["response_mode"], "MULTIPART")
        requirements = REGISTRY["workspace_requirements"]
        self.assertGreater(requirements["PROOF"]["min_height_pt"],
                           requirements["MCQ_SELECTION"]["min_height_pt"])

    def test_whitespace_alone_is_not_a_failure(self):
        """Unused space is only a finding when readable size was sacrificed for it."""
        audit = audit_layout(probe())
        page_one = next(p for p in audit["whitespace"]["unused_area_ratio_by_page"]
                        if p["page"] == 1)
        self.assertGreater(page_one["unused_ratio"],
                           REGISTRY["whitespace_policy"]["unused_page_area_ratio_threshold"])
        self.assertEqual(audit["whitespace"]["microtype_with_space_available"], [])

    def test_audit_is_deterministic(self):
        self.assertEqual(audit_layout(probe())["audit_digest"],
                         audit_layout(probe())["audit_digest"])

    def test_policy_declares_every_falsifier_the_engine_can_raise(self):
        self.assertEqual(sorted(POLICY["falsifiers"]), sorted(FALSIFIERS))

    def test_the_layout_phase_shares_the_source_ledger_object_model(self):
        """One object map, audited by both phases: completeness and layout."""
        from build_math_source_ledger import rendered_coverage_witness

        manifest = load(MATH / "SourceLedger" / "fixtures"
                        / "math-source-corpus.fixture.json")
        # the probe carries Q2 and Q3 atomic asks, so the witness can read it directly
        witness = rendered_coverage_witness(manifest, probe())
        self.assertTrue(witness["evaluated"])
        for ref in ("Q2#PROOF-1", "Q2#PROOF-2", "Q3#SUB-a", "Q3#SUB-b", "Q3#COND"):
            self.assertNotIn(ref, witness["occluded"])
            self.assertNotIn(ref, witness["clipped"])


class LayoutFalsifiers(unittest.TestCase):
    def expect(self, code: str, object_map: dict):
        with self.assertRaises(ValueError) as ctx:
            assert_layout_safe(object_map)
        self.assertIn(code, str(ctx.exception), f"expected {code}, got {ctx.exception}")

    # 1
    def test_LEARNER_TEXT_BELOW_MIN_READABLE_SIZE(self):
        bad = probe()
        find(bad, "Q3/sub-a")["font_size_pt"] = 8.4
        self.expect("LEARNER_TEXT_BELOW_MIN_READABLE_SIZE", bad)

    # 2
    def test_LEARNER_TEXT_BELOW_MIN_READABLE_SIZE_for_solution_body(self):
        bad = probe()
        find(bad, "Q2/solution")["font_size_pt"] = 8.5
        self.expect("LEARNER_TEXT_BELOW_MIN_READABLE_SIZE", bad)

    # 3
    def test_DIAGRAM_LABEL_BELOW_MIN_READABLE_SIZE(self):
        bad = probe()
        find(bad, "Q2/figure/label-B")["font_size_pt"] = 6.0
        self.expect("DIAGRAM_LABEL_BELOW_MIN_READABLE_SIZE", bad)

    # 4
    def test_LEARNER_TEXT_BELOW_MIN_READABLE_SIZE_on_unknown_role(self):
        bad = probe()
        find(bad, "Q2/stem")["typography_role"] = "SOME_RENDERER_LOCAL_STYLE"
        self.expect("LEARNER_TEXT_BELOW_MIN_READABLE_SIZE", bad)

    # 5 — the Euclid finding: microtype and unused space on the same page
    def test_MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS(self):
        bad = probe()
        find(bad, "Q2/proof-1")["font_size_pt"] = 10.0     # legal, but below preferred
        self.expect("MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS", bad)

    # 6 — the Euclid two-up collision
    def test_LAYOUT_COMPONENT_INTERSECTION_between_siblings(self):
        bad = probe()
        find(bad, "Q3/solution")["box"]["y"] += 120.0
        self.expect("LAYOUT_COMPONENT_INTERSECTION", bad)

    # 7
    def test_LAYOUT_COMPONENT_INTERSECTION_between_panel_children(self):
        bad = probe()
        find(bad, "Q3/sub-b")["box"]["y"] += 20.0
        self.expect("LAYOUT_COMPONENT_INTERSECTION", bad)

    # 8 — a page-bounds check cannot see this, which is the point
    def test_collision_is_invisible_to_a_page_bounds_check(self):
        bad = probe()
        moved = find(bad, "Q3/solution")
        moved["box"]["y"] += 120.0
        margin = bad["printable_margin_pt"]
        self.assertGreaterEqual(moved["box"]["y"], margin - 0.5)
        self.assertLessEqual(moved["box"]["y"] + moved["box"]["h"],
                             bad["page_height_pt"] - margin + 0.5)
        self.expect("LAYOUT_COMPONENT_INTERSECTION", bad)

    # 9 — the Polynomials multipart overflow
    def test_CONTENT_OVERFLOW(self):
        bad = probe()
        find(bad, "Q3/workspace")["content_height_pt"] = 420.0
        self.expect("CONTENT_OVERFLOW", bad)

    # 10
    def test_NEGATIVE_REMAINING_HEIGHT(self):
        bad = probe()
        find(bad, "Q2/panel")["box"]["h"] = 60.0
        self.expect("NEGATIVE_REMAINING_HEIGHT", bad)

    # 11 — a generic box under a proof prompt
    def test_WORKSPACE_RESPONSE_MODE_MISMATCH_too_small_for_a_proof(self):
        bad = probe()
        workspace = find(bad, "Q2/workspace")
        workspace["box"]["h"] = 60.0
        workspace["content_height_pt"] = 60.0
        self.expect("WORKSPACE_RESPONSE_MODE_MISMATCH", bad)

    # 12
    def test_WORKSPACE_RESPONSE_MODE_MISMATCH_when_no_mode_is_declared(self):
        bad = probe()
        find(bad, "Q3/workspace")["response_mode"] = None
        self.expect("WORKSPACE_RESPONSE_MODE_MISMATCH", bad)

    # 13
    def test_WORKSPACE_RESPONSE_MODE_MISMATCH_on_unknown_mode(self):
        bad = probe()
        find(bad, "Q3/workspace")["response_mode"] = "FREEFORM"
        self.expect("WORKSPACE_RESPONSE_MODE_MISMATCH", bad)

    # 14 — fixed-density two-up instead of measure-then-pack
    def test_SOLUTION_BLOCK_PACKING_OVERFLOW(self):
        bad = probe()
        find(bad, "Q3/solution")["content_height_pt"] = 520.0
        self.expect("SOLUTION_BLOCK_PACKING_OVERFLOW", bad)

    # 15
    def test_SOLUTION_BLOCK_PACKING_OVERFLOW_when_a_third_block_is_forced_on(self):
        bad = probe()
        extra = copy.deepcopy(find(bad, "Q2/solution"))
        extra["object_id"] = "Q4/solution"
        extra["question_ref"] = "Q4"
        extra["paint_order"] = 9
        extra["box"] = {"x": 42.0, "y": 42.0, "w": 511.28, "h": 300.0}
        extra["content_height_pt"] = 300.0
        bad["objects"].append(extra)
        self.expect("SOLUTION_BLOCK_PACKING_OVERFLOW", bad)

    # 16
    def test_audit_reports_BLOCKED_without_raising(self):
        bad = probe()
        find(bad, "Q3/sub-a")["font_size_pt"] = 8.0
        audit = audit_layout(bad)
        self.assertEqual(audit["status"], "BLOCKED")
        Draft202012Validator(AUDIT_SCHEMA).validate(audit)

    # 17
    def test_object_map_contract_rejects_a_zero_height_box(self):
        bad = probe()
        find(bad, "Q2/stem")["box"]["h"] = 0
        with self.assertRaises(Exception):
            Draft202012Validator(MAP_SCHEMA).validate(bad)

    # 18
    def test_registry_covers_every_role_the_probe_uses(self):
        used = {o["typography_role"] for o in PROBE["objects"]}
        for role in used:
            self.assertIn(role, REGISTRY["roles"], role)


if __name__ == "__main__":
    unittest.main(verbosity=2)
