#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

D = Path(__file__).resolve().parents[1]


def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


copy_mod = mod("core1a_copy", D / "engine" / "physics_learner_copy.py")
build = mod("core1a_build", D / "engine" / "build_physics_core1a.py")
render = mod("core1a_render", D / "engine" / "render_physics_core1a.py")
POLICY = json.loads((D / "registry" / "physics-core1a-publication-policy.json").read_text())
COPY = json.loads((D / "registry" / "physics-learner-copy-titles.json").read_text())


def attempt(stage, prompt):
    return {
        "attempt_id": "A-" + stage,
        "support_stage": stage,
        "prompt": prompt,
        "representation_spec": ["SIGNED_AXIS"],
        "frame_sign_required": True,
        "model_validity_required": True,
        "verification_steps": ["CHECK_UNITS", "VERIFY_SIGN"],
    }


def lesson(mode="FULL_LEARNING", prompt="A cyclist moves east, brakes uniformly, and stops. Find the stopping time."):
    full = mode == "FULL_LEARNING"
    return {
        "lesson_id": "PHY-CORE1-LESSON-01",
        "capability_ref": "PHY-CAP-ACCELERATION-SIGN",
        "treatment": "ACTIVE_STUDY" if full else ("PROBE_FIRST" if mode == "PROBE" else "READY_VERIFY_ONLY"),
        "lesson_mode": mode,
        "priority": "HIGH",
        "primary_pck_family": "SYSTEM_FRAME_SIGN_SETUP",
        "family_selection_rule_ref": "R1",
        "pck_asset_refs": ["PCK1"],
        "content_roles": ["TEACH"],
        "scope_trace": {},
        "required_pck_jobs": ["SIGN_SETUP"],
        "frame_sign_required": True,
        "model_validity_required": True,
        "multiphase": False,
        "representation_requirements": ["SIGNED_AXIS"],
        "verification_steps": ["CHECK_UNITS", "VERIFY_SIGN"],
        "future_evidence_obligations": [],
        "release_authority_state": "PILOT_ONLY_HUMAN_EXPERT_RELEASE_NOT_GRANTED",
        "see_phenomenon_anchor": "A cyclist is moving to the right and applies the brakes.",
        "see_phase": "Watch the direction of motion and the direction of acceleration.",
        "see_system_frame_sign": "Choose right as positive before assigning signs.",
        "realize_phase": "Translate the story into a signed velocity and acceleration state.",
        "realize_representation_path": ["STORY", "SIGNED_AXIS"],
        "realize_reconstruction_steps": ["Draw the axis.", "Mark velocity.", "Mark acceleration."],
        "understand_phase": "Speed changes according to whether velocity and acceleration point together or oppositely.",
        "understand_relation_and_validity": "Use v = u + at only while acceleration is constant.",
        "model_validity_conditions": ["straight-line motion", "constant acceleration"],
        "ordinary_language_explanation": "Acceleration opposite to velocity reduces speed; acceleration in the same direction increases speed.",
        "activation": "Predict whether the cyclist speeds up or slows down.",
        "worked_example": {
            "instance_id": "W1", "source_class": "NEW_AUTHORED_CORE1", "problem_family_ref": "PF1",
            "primary_capability_ref": "PHY-CAP-ACCELERATION-SIGN", "physical_model_refs": ["M1"],
            "law_refs": ["L1"], "prompt": prompt, "representation_spec": ["SIGNED_AXIS"],
            "surface_variation": "cycling", "external_candidate_refs": [],
            "reasoning_steps": [
                {"role": "SET_FRAME", "text": "Take east as positive."},
                {"role": "SELECT_RELATION", "text": "Because acceleration is constant, use v = u + at."},
                {"role": "VERIFY_PHYSICAL_PLAUSIBILITY", "text": "The answer must be positive in time and the final speed must be zero."}
            ],
            "verification_steps": ["CHECK_UNITS", "VERIFY_SIGN"]
        } if full else None,
        "concept_helper": "same or opposite directions",
        "misconception_repair": {
            "wrong_model": "Negative acceleration always means slowing down.",
            "why_plausible": "Negative is often read as less.",
            "minimal_contrast": "An object moving left with leftward acceleration speeds up.",
            "repair_steps": ["Compare the directions of v and a.", "Decide whether their signs match."],
            "retry_prompt": "If v and a are both negative, what happens to speed?"
        } if full else None,
        "guided_attempt": attempt("GUIDED", "A car moves right while acceleration points left. Predict the speed change.") if full else None,
        "faded_attempt": attempt("FADED", "A trolley has v < 0 and a < 0. Is it speeding up or slowing down?") if full else None,
        "independent_attempt": attempt("INDEPENDENT", "A runner has v = -4 m/s and a = +1 m/s^2. Describe the speed change."),
        "probe_attempt": attempt("PROBE", "Without a formula, decide what v < 0 and a > 0 do to speed.") if mode == "PROBE" else None,
        "probe_requirements": ["direction reasoning"],
        "physical_verification": "Translate the signs back into arrow directions.",
        "transfer_bridge": "Use the same sign logic in vertical motion and braking problems."
    }


def core1(mode="FULL_LEARNING", worked_prompt=None):
    l = lesson(mode, worked_prompt) if worked_prompt else lesson(mode)
    obj = {
        "plan_id": "PHY-P-G-TEST",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "pedagogy_model": "SEE_REALIZE_UNDERSTAND",
        "lessons": [l],
        "appendices": {
            "appendix_a": {"present": True, "title": "Appendix A — Core Practice", "items": [
                {"item_id": "A1", "support_stage": "INDEPENDENT", "prompt": "Decide whether v<0,a<0 speeds up or slows down."}
            ]},
            "appendix_b": {"present": True, "title": "Appendix B — Core Solutions", "solutions": [
                {"item_ref": "A1", "reasoning_steps": [{"role": "COMPARE_SIGNS", "text": "The signs match."}],
                 "final_response": "The object speeds up in the negative direction.",
                 "model_validity_note": "The sign conclusion is instantaneous."}
            ]},
            "appendix_c": {"present": True, "title": "Appendix C — Printable Handout", "reference_entries": [
                {"capability_ref": "PHY-CAP-ACCELERATION-SIGN", "first_move": "Compare v and a directions.",
                 "frame_sign_cue": "Declare positive direction.", "relation_or_decision_cue": "Same sign means speed increases.",
                 "verification_cue": "VERIFY_SIGN"}
            ]}
        },
        "plan_digest": ""
    }
    obj["plan_digest"] = build.digest(obj, "plan_digest")
    return obj


class Core1ATests(unittest.TestCase):
    def test_full_learning_has_mature_cycle(self):
        plan = build.build_publication_plan(core1(), POLICY)
        kinds = [m["kind"] for m in plan["lessons"][0]["modules"]]
        for required in POLICY["full_learning_required_modules"]:
            self.assertIn(required, kinds)
        self.assertEqual(plan["product_id"], "CORE_STUDY_GUIDE")
        self.assertTrue(plan["two_product_topology_preserved"])

    def test_template_only_content_is_reported_not_rewritten(self):
        c = core1(worked_prompt="Work a newly authored instance of this family; set up the system and frame.")
        plan = build.build_publication_plan(c, POLICY)
        self.assertIn("CORE1A_TEMPLATE_ONLY_CONTENT", plan["lessons"][0]["content_maturity_findings"])
        self.assertEqual(plan["quality_summary"]["template_only_content_count"], 1)

    def test_probe_stays_pre_explanatory(self):
        plan = build.build_publication_plan(core1("PROBE"), POLICY)
        kinds = [m["kind"] for m in plan["lessons"][0]["modules"]]
        self.assertEqual(kinds[1], "PROBE")
        self.assertNotIn("WORKED_EXAMPLE", kinds)
        self.assertNotIn("COMMON_TRAP", kinds)

    def test_verify_only_does_not_expand_to_reteach(self):
        plan = build.build_publication_plan(core1("CONCISE_VERIFY_ONLY"), POLICY)
        kinds = [m["kind"] for m in plan["lessons"][0]["modules"]]
        self.assertNotIn("WORKED_EXAMPLE", kinds)
        self.assertNotIn("REAL_WORLD_ANCHOR", kinds)

    def test_renderer_binds_exact_upstream_digest(self):
        c = core1()
        plan = build.build_publication_plan(c, POLICY)
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "physics-core-study-guide.pdf"
            report = render.render_core1a(c, plan, pdf, POLICY)
            self.assertTrue(pdf.exists())
            self.assertGreater(pdf.stat().st_size, 1000)
            self.assertEqual(report["upstream_core1_digest"], c["plan_digest"])
            self.assertEqual(report["publication_plan_digest"], plan["plan_digest"])
            self.assertGreaterEqual(report["minimum_body_font_pt"], POLICY["page"]["body_font_minimum_pt"])


class Core1AProductCustodyTests(unittest.TestCase):
    """P-UPGRADE-2 item 1: Core (1A) is the P-K CORE_STUDY_GUIDE, so it owns page custody."""

    def test_report_carries_a_physical_page_map_and_required_sections(self):
        c = core1()
        plan = build.build_publication_plan(c, POLICY)
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "physics-core-study-guide.pdf"
            report = render.render_core1a(c, plan, pdf, POLICY)
            pm = report["physical_page_map"]
            self.assertTrue(pm["actual_placement_evidence"])
            self.assertEqual(pm["artifact_sha256"], report["artifact_sha256"])
            self.assertEqual(pm["physical_page_count"], report["page_count"])
            self.assertEqual([m["page"] for m in pm["page_metrics"]],
                             list(range(1, pm["physical_page_count"] + 1)))
            for section in ("MAIN_TEACHING", "APPENDIX_A_CORE_PRACTICE",
                            "APPENDIX_B_CORE_SOLUTIONS", "APPENDIX_C_PRINTABLE_HANDOUT"):
                self.assertIn(section, report["required_sections"])

    def test_every_supplied_representation_is_physically_placed(self):
        """Core (1A) may choose the spread, but it may not silently drop a P-H figure."""
        c = core1()
        plan = build.build_publication_plan(c, POLICY)
        specs = []
        for i, phase in enumerate(("SEE", "REALIZE", "UNDERSTAND", "UNDERSTAND", "SEE"), 1):
            specs.append({
                "representation_id": f"REP-{i}",
                "capability_ref": "PHY-CAP-ACCELERATION-SIGN",
                "primitive_id": "STATE_TABLE",
                "page_intent_phase": phase,
                "minimum_vector_ops": 1,
                "quantitative_grounding": "SCHEMATIC_STRUCTURE_ONLY",
                "render_params": {},
                "accessibility_text": "A start and end state table.",
            })
        bundle = {"representations": specs}
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "physics-core-study-guide.pdf"
            report = render.render_core1a(c, plan, pdf, POLICY, bundle)
            placed = {p["content_ref"] for p in report["physical_page_map"]["content_placements"]}
            self.assertEqual(placed, {s["representation_id"] for s in specs})
            self.assertEqual(report["figure_count"], len(specs))
            self.assertGreater(report["total_vector_ops"], 0)
            self.assertEqual(
                report["physical_page_map"]["realization_summary"]["label_only_figure_count"], 0)


class LearnerCopyTests(unittest.TestCase):
    """P-UPGRADE-2 item 7: internal identifiers stay internal, learner pages stay plain."""

    def test_internal_identifiers_are_unchanged_and_mapped(self):
        for role in ("MISCONCEPTION_REPAIR", "WORKED", "GUIDED", "FADED", "INDEPENDENT",
                     "TRANSFER", "VERIFY", "RECONSTRUCT", "ANCHOR", "MODEL", "EXECUTE",
                     "INTERPRET", "READINESS_PROBE", "MODEL_CHECK", "PHYSICAL_CHECK"):
            self.assertIn(role, COPY["titles"], role)
            title = copy_mod.learner_title(role)
            self.assertNotEqual(title, role)
            self.assertEqual(copy_mod.learner_copy_violations(title), [])

    def test_falsifier_fires_on_a_raw_internal_role_label(self):
        self.assertIn("MISCONCEPTION_REPAIR",
                      copy_mod.learner_copy_violations("Section: MISCONCEPTION_REPAIR"))
        self.assertIn("misconception repair",
                      copy_mod.learner_copy_violations("Misconception Repair"))
        self.assertIn("readiness gate", copy_mod.learner_copy_violations("Readiness Gate"))
        with self.assertRaises(ValueError) as ctx:
            copy_mod.assert_learner_copy("Worked Example", where="page 3")
        self.assertIn("INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE", str(ctx.exception))

    def test_rendered_core1a_page_text_carries_no_internal_role_label(self):
        c = core1()
        plan = build.build_publication_plan(c, POLICY)
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "physics-core-study-guide.pdf"
            report = render.render_core1a(c, plan, pdf, POLICY)
            self.assertEqual(report["learner_copy_violations"], [])
            self.assertNotIn("INTERNAL_ROLE_LABEL_ON_LEARNER_SURFACE", report["machine_findings"])

    def test_module_titles_come_from_the_governed_registry(self):
        plan = build.build_publication_plan(core1(), POLICY)
        for m in plan["lessons"][0]["modules"]:
            self.assertEqual(copy_mod.learner_copy_violations(m["title"]), [], m["kind"])
            if copy_mod.is_mapped(m["kind"]):
                self.assertEqual(m["title"], copy_mod.learner_title(m["kind"]))


if __name__ == "__main__":
    unittest.main()
