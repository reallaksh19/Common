from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from engineering_registry_composition import (  # noqa: E402
    BASE_REGISTRY_REL,
    CANONICAL_EXTENSION_RELS,
    EngineeringRegistryCompositionError,
    git_blob_sha,
    load_canonical_engineering_registry,
)
from validate_engineering_gates import validate as validate_engineering_registry  # noqa: E402


def raw(path: str | Path) -> dict:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


class EngineeringRegistryCompositionTests(unittest.TestCase):
    def temp_json(self, value: dict) -> Path:
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            prefix="phy-eng-composition-",
            dir=ROOT / "tests",
            delete=False,
            encoding="utf-8",
        )
        try:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            return Path(handle.name)
        finally:
            handle.close()

    def tearDown(self) -> None:
        for path in (ROOT / "tests").glob("phy-eng-composition-*.json"):
            path.unlink(missing_ok=True)

    def synthetic_extension(self) -> dict:
        base = raw(BASE_REGISTRY_REL)
        template_gate = copy.deepcopy(base["subtopic_gates"][0])
        suffix = "-EXTENSIBILITY"

        template_gate["subtopic_id"] = "PHY-TST-CATALOG-EXTENSIBILITY"
        template_gate["learner_title"] = "Synthetic catalog extensibility gate"
        template_gate["linked_buckets"] = [value + suffix for value in template_gate.get("linked_buckets", ["B-SYNTHETIC"])]
        template_gate["canonical_concept_ids"] = [value + suffix for value in template_gate.get("canonical_concept_ids", ["C-SYNTHETIC"])]
        for row in template_gate.get("technical_core", []):
            row["concept_id"] += suffix
        for row in template_gate.get("mandatory_equations", []):
            row["equation_id"] += suffix
        for row in template_gate.get("representations", []):
            row["representation_id"] += suffix
        for row in template_gate.get("misconceptions", []):
            row["misconception_id"] += suffix
        family_map = {}
        for row in template_gate.get("problem_families", []):
            old = row["family_id"]
            row["family_id"] = old + suffix
            family_map[old] = row["family_id"]
        template_gate["linked_problem_family_ids"] = [family_map.get(value, value + suffix) for value in template_gate.get("linked_problem_family_ids", [])]
        for row in template_gate.get("falsification_cases", []):
            if "test_id" in row:
                row["test_id"] += suffix
        template_gate["prerequisite_ids"] = []

        current = raw(BASE_REGISTRY_REL)
        return {
            "schema_version": "1.0.0",
            "subject": "PHYSICS",
            "extension_id": "REG-PHY-TECH-GATE-V1-EXTENSIBILITY-TEST",
            "base_registry_id": current["registry_id"],
            "base_registry_git_blob_sha": git_blob_sha(BASE_REGISTRY_REL),
            "expected_base_gate_count": len(current["subtopic_gates"]),
            "expected_composed_gate_count": len(current["subtopic_gates"]) + 1,
            "subtopic_gates": [template_gate],
        }

    def test_canonical_composition_has_all_base_gates(self):
        base = raw(BASE_REGISTRY_REL)
        registry = load_canonical_engineering_registry()
        ids = [row["subtopic_id"] for row in registry["subtopic_gates"]]
        self.assertEqual(len(ids), len(base["subtopic_gates"]))
        self.assertEqual(len(ids), 43)
        self.assertEqual(len(ids), len(set(ids)))

    def test_new_gate_can_be_added_and_validated_without_production_python_change(self):
        extension = self.synthetic_extension()
        template_gate = extension["subtopic_gates"][0]
        path = self.temp_json(extension)
        composed = load_canonical_engineering_registry(
            extension_rels=[*CANONICAL_EXTENSION_RELS, str(path)]
        )
        validated = validate_engineering_registry(composed)
        self.assertIn(template_gate["subtopic_id"], validated)
        self.assertEqual(len(composed["subtopic_gates"]), 44)

    def test_extension_stale_base_blob_fails_closed(self):
        extension = self.synthetic_extension()
        extension["base_registry_git_blob_sha"] = "0" * 40
        path = self.temp_json(extension)
        with self.assertRaises(EngineeringRegistryCompositionError) as ctx:
            load_canonical_engineering_registry(extension_rels=[str(path)])
        self.assertEqual(ctx.exception.code, "PHY_ENG_EXTENSION_BASE_BLOB_STALE")

    def test_extension_wrong_base_gate_count_fails_closed(self):
        extension = self.synthetic_extension()
        extension["expected_base_gate_count"] -= 1
        path = self.temp_json(extension)
        with self.assertRaises(EngineeringRegistryCompositionError) as ctx:
            load_canonical_engineering_registry(extension_rels=[str(path)])
        self.assertEqual(ctx.exception.code, "PHY_ENG_EXTENSION_BASE_GATE_COUNT_DRIFT")

    def test_extension_duplicate_gate_id_fails_closed(self):
        extension = self.synthetic_extension()
        base = raw(BASE_REGISTRY_REL)
        extension["subtopic_gates"][0]["subtopic_id"] = base["subtopic_gates"][0]["subtopic_id"]
        path = self.temp_json(extension)
        with self.assertRaises(EngineeringRegistryCompositionError) as ctx:
            load_canonical_engineering_registry(extension_rels=[str(path)])
        self.assertEqual(ctx.exception.code, "PHY_ENG_EXTENSION_DUPLICATE_GATE_ID")


if __name__ == "__main__":
    unittest.main(verbosity=2)
