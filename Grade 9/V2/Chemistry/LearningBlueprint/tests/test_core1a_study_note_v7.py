from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "policies" / "v7-core1a-study-note-sufficiency-policy.json").read_text(encoding="utf-8"))
AUTHORITY = json.loads((ROOT / "golden" / "v7" / "core1a-study-note-redox-authority.json").read_text(encoding="utf-8"))
CCBOM = json.loads((ROOT / "golden" / "v7" / "ccbom-redox.json").read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location("studyv7", ROOT / "engine" / "validate_core1a_study_note_v7.py")
studyv7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(studyv7)


class Core1AStudyNoteV7Tests(unittest.TestCase):
    def test_redox_content_bearing_authority_passes(self):
        out = studyv7.validate(copy.deepcopy(AUTHORITY), copy.deepcopy(CCBOM), POLICY)
        self.assertEqual(out["status"], "PASS")
        self.assertGreaterEqual(out["content_object_count"], 30)
        self.assertEqual(out["learner_surface_internal_jargon_leaks"], 0)
        self.assertEqual(out["pagination_mode"], "CONTENT_FIRST")

    def test_label_only_object_cannot_pass_as_study_content(self):
        p = copy.deepcopy(AUTHORITY)
        p["content_objects"][0]["learner_payload"] = ""
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "OBJECT_PAYLOAD_EMPTY"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_unresolved_source_ref_fails(self):
        p = copy.deepcopy(AUTHORITY)
        p["content_objects"][0]["source_ref"] = "UNDECLARED-SOURCE"
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "OBJECT_SOURCE_UNRESOLVED"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_object_missing_from_ccbom_fails(self):
        p = copy.deepcopy(CCBOM)
        missing_id = AUTHORITY["content_objects"][0]["ccbom_asset_id"]
        p["assets"] = [x for x in p["assets"] if x["asset_id"] != missing_id]
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "OBJECT_CCBOM_UNRESOLVED"):
            studyv7.validate(copy.deepcopy(AUTHORITY), p, POLICY)

    def test_internal_architecture_jargon_cannot_reach_learner_payload(self):
        p = copy.deepcopy(AUTHORITY)
        p["content_objects"][0]["learner_payload"] = "Use the PAL support_band before deciding the chemistry."
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "INTERNAL_JARGON_LEAK"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_ascii_chemistry_leak_fails(self):
        p = copy.deepcopy(AUTHORITY)
        eq = next(x for x in p["content_objects"] if x["object_id"] == "OBJ-ZN-HALF")
        eq["learner_payload"] = "Zn -> Zn2+ + 2e-"
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "ASCII_CHEMISTRY_LEAK"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_every_learning_atom_requires_all_study_jobs(self):
        p = copy.deepcopy(AUTHORITY)
        p["learning_atoms"][0]["required_job_object_ids"].pop("WORKED_OR_MODELED_EXAMPLE")
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "ATOM_JOB_SET_INCOMPLETE"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_hard_note_requires_multiple_representation_types(self):
        p = copy.deepcopy(AUTHORITY)
        for obj in p["content_objects"]:
            if "representation_type" in obj:
                obj["representation_type"] = "ONE_GENERIC_VIEW"
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "HARD_REPRESENTATION_DEPTH_LOW"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_hard_note_requires_guided_and_independent_practice(self):
        p = copy.deepcopy(AUTHORITY)
        for obj in p["content_objects"]:
            if obj.get("practice_level") == "INDEPENDENT":
                obj["practice_level"] = "GUIDED"
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "HARD_PRACTICE_LEVELS_INCOMPLETE"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_page_count_targeting_fails(self):
        p = copy.deepcopy(AUTHORITY)
        p["pagination_policy"]["page_count_is_target"] = True
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "PAGINATION_POLICY_INVALID"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)

    def test_completeness_summary_is_recomputed_not_trusted(self):
        p = copy.deepcopy(AUTHORITY)
        p["completeness_summary"]["content_object_count"] += 1
        with self.assertRaisesRegex(studyv7.Core1AStudyNoteError, "SUMMARY_DRIFT"):
            studyv7.validate(p, copy.deepcopy(CCBOM), POLICY)


if __name__ == "__main__":
    unittest.main()
