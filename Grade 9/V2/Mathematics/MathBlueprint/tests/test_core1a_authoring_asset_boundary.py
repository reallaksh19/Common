from __future__ import annotations

import ast
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
CORE1A = MATH / "Core1A"
CORE1A_ENGINE = CORE1A / "engine"
if str(CORE1A_ENGINE) not in sys.path:
    sys.path.insert(0, str(CORE1A_ENGINE))

import build_math_core1a_textbook as base
import core1a_capability_authoring as authoring
import core1a_family_authoring as family_authoring


def assignment_value(tree: ast.Module, name: str):
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node.value
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            return node.value
    return None


class Core1AAuthoringAssetBoundaryTests(unittest.TestCase):
    def test_projection_is_typed_non_authoritative_and_custodied(self):
        projection = authoring.load_authoring_assets()
        self.assertEqual(projection["subject"], "MATHEMATICS")
        self.assertEqual(projection["content_role"], "CORE1A_AUTHORING_CANDIDATE")
        self.assertFalse(projection["curriculum_authority"])
        self.assertTrue(projection["asset_set_id"].startswith("MATH-CORE1A-AUTHORING-ASSETS-"))
        self.assertEqual(len(projection["asset_set_digest"]), 64)
        refs = [row["capability_ref"] for row in projection["capabilities"]]
        self.assertEqual(len(refs), len(set(refs)))
        custom = [row for row in projection["capabilities"] if row["bank_source"] == "CUSTOM_MIGRATED"]
        self.assertTrue(custom)
        for row in custom:
            self.assertGreaterEqual(len(row["examples"]), 6)
            self.assertEqual(len({x["example_id"] for x in row["examples"]}), len(row["examples"]))
            self.assertTrue(all(x["source_class"] == "AUTHORING_CANDIDATE" for x in row["examples"]))

    def test_family_projection_is_typed_non_authoritative_and_custodied(self):
        projection = family_authoring.load_family_authoring_assets()
        self.assertEqual(projection["subject"], "MATHEMATICS")
        self.assertEqual(projection["content_role"], "CORE1A_FAMILY_AUTHORING_CANDIDATE")
        self.assertFalse(projection["curriculum_authority"])
        self.assertTrue(projection["asset_set_id"].startswith("MATH-CORE1A-FAMILY-AUTHORING-ASSETS-"))
        self.assertEqual(len(projection["asset_set_digest"]), 64)
        refs = [row["family_ref"] for row in projection["families"]]
        self.assertEqual(len(refs), len(set(refs)))
        for row in projection["families"]:
            self.assertGreaterEqual(len(row["examples"]), 6)
            self.assertEqual(len({x["example_id"] for x in row["examples"]}), len(row["examples"]))
            self.assertTrue(all(x["source_class"] == "AUTHORING_CANDIDATE" for x in row["examples"]))

    def test_executable_module_no_longer_defines_legacy_math_banks(self):
        executable = (CORE1A_ENGINE / "core1a_capability_authoring.py").read_text(encoding="utf-8")
        tree = ast.parse(executable)
        executable_functions = {x.name for x in tree.body if isinstance(x, ast.FunctionDef)}
        legacy = (CORE1A / "policies" / "core1a-capability-authoring.legacy.pydata").read_text(encoding="utf-8")
        legacy_tree = ast.parse(legacy)
        custom_node = authoring._assignment(legacy_tree, "CUSTOM_BANKS")
        legacy_bank_functions = {value.id for value in custom_node.values if isinstance(value, ast.Name)}
        self.assertFalse(executable_functions & legacy_bank_functions)
        self.assertNotIsInstance(assignment_value(tree, "CAPABILITY_TITLES"), ast.Dict)
        self.assertNotIsInstance(assignment_value(tree, "CUSTOM_BANKS"), ast.Dict)
        self.assertNotIn("def angle_sum_bank", executable)
        self.assertNotIn("def geometric_modelling_bank", executable)

    def test_base_builder_no_longer_defines_family_math_banks(self):
        executable = (CORE1A_ENGINE / "build_math_core1a_textbook.py").read_text(encoding="utf-8")
        tree = ast.parse(executable)
        executable_functions = {x.name for x in tree.body if isinstance(x, ast.FunctionDef)}
        legacy = (CORE1A / "policies" / "core1a-family-authoring.legacy.pydata").read_text(encoding="utf-8")
        legacy_tree = ast.parse(legacy)
        family_node = family_authoring._assignment(legacy_tree, "FAMILY_BANKS")
        legacy_bank_functions = {value.id for value in family_node.values if isinstance(value, ast.Name)}
        self.assertFalse(executable_functions & legacy_bank_functions)
        self.assertNotIsInstance(assignment_value(tree, "FAMILY_BANKS"), ast.Dict)
        self.assertNotIsInstance(assignment_value(tree, "DISPLAY_TITLES"), ast.Dict)
        self.assertIsNone(assignment_value(tree, "EXTRA_INSTANCES"))
        self.assertNotIn("def distance_instances", executable)
        self.assertNotIn("def river_instances", executable)

    def test_source_custody_tamper_fails_closed(self):
        manifest = json.loads(authoring.MANIFEST_PATH.read_text(encoding="utf-8"))
        data = (CORE1A / manifest["legacy_source_ref"]).read_bytes()
        tampered = copy.deepcopy(manifest)
        tampered["legacy_source_git_blob_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "CORE1A_AUTHORING_SOURCE_CUSTODY_MISMATCH"):
            authoring._verify_source_custody(data, tampered)

    def test_family_source_custody_tamper_fails_closed(self):
        manifest = json.loads(family_authoring.MANIFEST_PATH.read_text(encoding="utf-8"))
        data = (CORE1A / manifest["legacy_source_ref"]).read_bytes()
        tampered = copy.deepcopy(manifest)
        tampered["legacy_source_git_blob_sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "CORE1A_FAMILY_AUTHORING_SOURCE_CUSTODY_MISMATCH"):
            family_authoring._verify_source_custody(data, tampered)

    def test_custom_bank_materialization_preserves_typed_projection(self):
        projection = authoring.load_authoring_assets()
        for row in projection["capabilities"]:
            if row["bank_source"] != "CUSTOM_MIGRATED":
                continue
            materialized = authoring.capability_bank(row["capability_ref"], "unused")
            self.assertEqual(len(materialized), len(row["examples"]))
            for inst, source in zip(materialized, row["examples"]):
                self.assertEqual(inst.prompt, source["prompt"])
                self.assertEqual(list(inst.steps), source["steps"])
                self.assertEqual(inst.answer, source["answer"])
                self.assertEqual(list(inst.hints), source["hints"])

    def test_family_bank_materialization_preserves_typed_projection(self):
        projection = family_authoring.load_family_authoring_assets()
        for row in projection["families"]:
            materialized = base.family_bank(row["family_ref"])
            self.assertEqual(len(materialized), len(row["examples"]))
            for inst, source in zip(materialized, row["examples"]):
                self.assertEqual(inst.prompt, source["prompt"])
                self.assertEqual(list(inst.steps), source["steps"])
                self.assertEqual(inst.answer, source["answer"])
                self.assertEqual(list(inst.hints), source["hints"])


if __name__ == "__main__":
    unittest.main()
