from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location(
    "compile_sdu_lau_generation_spec",
    ROOT / "engine" / "compile_sdu_lau_generation_spec.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def profile(value: int) -> dict:
    return {
        "prerequisite_depth": value,
        "element_interactivity": value,
        "inferential_jump_severity": value,
        "representation_translation": value,
        "model_discrimination": value,
        "sign_or_frame_sensitivity": value,
        "multi_step_dependency": value,
        "abstraction": value,
        "misconception_density": value,
        "synthesis": value,
        "provisional_difficulty": "EASY" if value <= 1 else "MEDIUM" if value == 2 else "HARD",
        "difficulty_basis": "Synthetic structural fixture",
        "maturity": "ENGINEERING",
    }


def registry() -> dict:
    return {
        "subtopic_gates": [
            {"subtopic_id": "G-EASY", "difficulty_profile": profile(1)},
            {"subtopic_id": "G-MEDIUM", "difficulty_profile": profile(2)},
            {"subtopic_id": "G-HARD", "difficulty_profile": profile(3)},
        ]
    }


def bucket_plan() -> dict:
    return {
        "buckets": [
            {"bucket_id": "B-EASY", "title": "Easy", "member_capability_refs": ["CAP-E"]},
            {"bucket_id": "B-MEDIUM", "title": "Medium", "member_capability_refs": ["CAP-M"]},
            {"bucket_id": "B-HARD", "title": "Hard", "member_capability_refs": ["CAP-H"]},
        ]
    }


def coverage() -> dict:
    return {
        "bucket_gate_map": [
            {"bucket_id": "B-EASY", "engineering_gate_ids": ["G-EASY"]},
            {"bucket_id": "B-MEDIUM", "engineering_gate_ids": ["G-MEDIUM"]},
            {"bucket_id": "B-HARD", "engineering_gate_ids": ["G-HARD"]},
        ]
    }


def study(observed: bool = False) -> dict:
    rows = []
    for cap in ("CAP-E", "CAP-M", "CAP-H"):
        rows.append({
            "capability_ref": cap,
            "learner_state_readiness": "PARTIAL" if observed else "UNKNOWN",
            "learner_state_confidence": 0.7 if observed else 0.0,
            "learner_state_observation_refs": ["OBS:" + cap] if observed else [],
        })
    return {"study_model_id": "SM-1", "study_model_digest": "d" * 64, "capability_plans": rows}


def waiver(release_class: str = "TEST_ONLY") -> dict:
    row = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "waiver_id": "MATH-CORE2-WAIVER-UNIT",
        "release_class": release_class,
        "owner_ref": "OWNER:UNIT",
        "reason": "Unit fixture has no authorized learner percentage evidence.",
        "selected_core2a_support_profile": "STANDARD_GUIDED",
        "selected_core2a_max_demand_level": "M3_INVERSE_TARGET",
        "selected_core2b_max_demand_level": "M4_HIDDEN_STRUCTURE",
        "waiver_digest": "",
    }
    row["waiver_digest"] = mod.digest(row, "waiver_digest")
    return row


def evidence(study_model: dict, *, bad_observation: bool = False) -> dict:
    rows = []
    for idx, cap in enumerate(("CAP-E", "CAP-M", "CAP-H")):
        obs = "OBS:WRONG" if bad_observation and idx == 0 else "OBS:" + cap
        rows.append({"capability_ref": cap, "percent": 55 + idx * 5, "observation_refs": [obs]})
    row = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "evidence_id": "MATH-CORE2-KNOWLEDGE-UNIT",
        "release_class": "PRODUCTION",
        "source_ref": "ASSESSMENT:UNIT-DIAGNOSTIC",
        "calibration_policy_ref": "OWNER_POLICY:UNIT-v1",
        "learner_knowledge_percent": 60,
        "capability_knowledge": rows,
        "resolved_core2a_support_profile": "STANDARD_GUIDED",
        "resolved_core2a_max_demand_level": "M3_INVERSE_TARGET",
        "resolved_core2b_max_demand_level": "M4_HIDDEN_STRUCTURE",
        "evidence_digest": "",
    }
    row["evidence_digest"] = mod.digest(row, "evidence_digest")
    return row


class SduLauGenerationCompilerTests(unittest.TestCase):
    def setUp(self):
        self.sid = {"B-EASY": "SUB-E", "B-MEDIUM": "SUB-M", "B-HARD": "SUB-H"}

    def test_engineering_profiles_derive_easy_medium_hard_without_learner_state(self):
        rows = mod.compile_sdu_rows(bucket_plan(), self.sid, registry(), coverage())
        self.assertEqual([x["difficulty_badge"] for x in rows], ["EASY", "MEDIUM", "HARD"])
        self.assertTrue(all(x["difficulty_badge_basis"] == "CORE1_SEMANTIC_COMPLEXITY" for x in rows))
        self.assertTrue(all(x["difficulty_validation_refs"] for x in rows))

    def test_unknown_learner_state_uses_explicit_waiver_without_percent(self):
        spec, manifest, audit = mod.compile_generation_spec(
            bucket_plan=bucket_plan(),
            study_model=study(False),
            bucket_sid=self.sid,
            engineering_registry=registry(),
            projection_coverage=coverage(),
            purpose="REVISION",
            release_class="TEST_ONLY",
            owner_waiver=waiver(),
            allow_test_research_fixture=True,
        )
        cal = spec["core2_calibration"]
        self.assertIsNone(cal["learner_knowledge_percent"])
        self.assertEqual(cal["capability_knowledge"], [])
        self.assertIn("MATH-CORE2-WAIVER-UNIT@sha256:", cal["owner_waiver"]["owner_ref"])
        self.assertEqual(audit["lau_mode"], "OWNER_WAIVER")
        self.assertFalse(audit["lau_fabricated_percent"])
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest["release_class"], "TEST_ONLY")

    def test_missing_evidence_and_waiver_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "MATH_LAU_EXACTLY_ONE_EVIDENCE_OR_WAIVER_REQUIRED"):
            mod.compile_lau_calibration(study(False), purpose="REVISION", release_class="TEST_ONLY")

    def test_test_only_waiver_cannot_authorize_production(self):
        with self.assertRaisesRegex(ValueError, "MATH_LAU_TEST_WAIVER_FOR_PRODUCTION"):
            mod.compile_lau_calibration(
                study(False), purpose="REVISION", release_class="PRODUCTION", owner_waiver=waiver("TEST_ONLY")
            )

    def test_evidence_must_be_present_in_current_study_model(self):
        sm = study(True)
        with self.assertRaisesRegex(ValueError, "MATH_LAU_CAPABILITY_EVIDENCE_NOT_IN_STUDY_MODEL"):
            mod.compile_lau_calibration(
                sm,
                purpose="REVISION",
                release_class="PRODUCTION",
                learner_knowledge_evidence=evidence(sm, bad_observation=True),
            )

    def test_observed_evidence_can_drive_lau_without_waiver(self):
        sm = study(True)
        cal = mod.compile_lau_calibration(
            sm,
            purpose="REVISION",
            release_class="PRODUCTION",
            learner_knowledge_evidence=evidence(sm),
        )
        self.assertEqual(cal["learner_knowledge_percent"], 60)
        self.assertIsNone(cal["owner_waiver"])
        self.assertTrue(cal["knowledge_percent_source_ref"].startswith("MATH-CORE2-KNOWLEDGE-UNIT@sha256:"))

    def test_production_medium_hard_requires_research_manifest(self):
        with self.assertRaisesRegex(ValueError, "MATH_SDU_RESEARCH_BINDING_REQUIRED"):
            mod.compile_generation_spec(
                bucket_plan=bucket_plan(),
                study_model=study(False),
                bucket_sid=self.sid,
                engineering_registry=registry(),
                projection_coverage=coverage(),
                purpose="REVISION",
                release_class="PRODUCTION",
                owner_waiver=waiver("OWNER_DECLARED"),
            )

    def test_test_research_fixture_cannot_be_requested_for_production(self):
        with self.assertRaisesRegex(ValueError, "MATH_SDU_TEST_RESEARCH_FIXTURE_FOR_PRODUCTION"):
            mod.compile_generation_spec(
                bucket_plan=bucket_plan(),
                study_model=study(False),
                bucket_sid=self.sid,
                engineering_registry=registry(),
                projection_coverage=coverage(),
                purpose="REVISION",
                release_class="PRODUCTION",
                owner_waiver=waiver("OWNER_DECLARED"),
                allow_test_research_fixture=True,
            )

    def test_unknown_engineering_gate_fails_closed(self):
        bad = coverage()
        bad["bucket_gate_map"][0]["engineering_gate_ids"] = ["G-NOT-THERE"]
        with self.assertRaisesRegex(ValueError, "MATH_SDU_ENGINEERING_GATE_UNKNOWN"):
            mod.compile_sdu_rows(bucket_plan(), self.sid, registry(), bad)

    def test_incomplete_engineering_profile_fails_closed(self):
        bad = registry()
        del bad["subtopic_gates"][0]["difficulty_profile"]["synthesis"]
        with self.assertRaisesRegex(ValueError, "MATH_SDU_ENGINEERING_DIFFICULTY_PROFILE_INCOMPLETE"):
            mod.compile_sdu_rows(bucket_plan(), self.sid, bad, coverage())

    def test_profile_mutation_changes_derived_badge(self):
        reg = registry()
        reg["subtopic_gates"][0]["difficulty_profile"] = profile(3)
        rows = mod.compile_sdu_rows(bucket_plan(), self.sid, reg, coverage())
        self.assertEqual(rows[0]["difficulty_badge"], "HARD")


if __name__ == "__main__":
    unittest.main(verbosity=2)
