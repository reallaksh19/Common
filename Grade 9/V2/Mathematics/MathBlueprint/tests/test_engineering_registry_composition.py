from __future__ import annotations

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
    load_canonical_engineering_registry,
)
from validate_assessment_engineering_crosswalk import (  # noqa: E402
    DEFAULT_CROSSWALK,
    MathematicsAssessmentEngineeringCrosswalkError,
    load as load_crosswalk,
)


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
            prefix="math-eng-composition-",
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
        for path in (ROOT / "tests").glob("math-eng-composition-*.json"):
            path.unlink(missing_ok=True)

    def canonical_extension(self) -> tuple[str, dict]:
        self.assertTrue(CANONICAL_EXTENSION_RELS)
        ref = CANONICAL_EXTENSION_RELS[0]
        return ref, raw(ref)

    def test_canonical_composition_has_unique_catalogued_gates(self):
        base = raw(BASE_REGISTRY_REL)
        registry = load_canonical_engineering_registry()
        ids = [row["subtopic_id"] for row in registry["subtopic_gates"]]
        expected = len(base["subtopic_gates"])
        catalogued_ids = []
        for rel in CANONICAL_EXTENSION_RELS:
            extension = raw(rel)
            expected += len(extension["subtopic_gates"])
            catalogued_ids.extend(row["subtopic_id"] for row in extension["subtopic_gates"])
        self.assertEqual(len(ids), expected)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(catalogued_ids).issubset(ids))

    def test_extension_stale_base_blob_fails_closed(self):
        _, extension = self.canonical_extension()
        extension["base_registry_git_blob_sha"] = "0" * 40
        path = self.temp_json(extension)
        with self.assertRaises(EngineeringRegistryCompositionError) as ctx:
            load_canonical_engineering_registry(extension_rels=[str(path)])
        self.assertEqual(ctx.exception.code, "MATH_ENG_EXTENSION_BASE_BLOB_STALE")

    def test_extension_wrong_base_gate_count_fails_closed(self):
        _, extension = self.canonical_extension()
        extension["expected_base_gate_count"] -= 1
        path = self.temp_json(extension)
        with self.assertRaises(EngineeringRegistryCompositionError) as ctx:
            load_canonical_engineering_registry(extension_rels=[str(path)])
        self.assertEqual(ctx.exception.code, "MATH_ENG_EXTENSION_BASE_GATE_COUNT_DRIFT")

    def test_extension_duplicate_gate_id_fails_closed(self):
        _, extension = self.canonical_extension()
        base = raw(BASE_REGISTRY_REL)
        extension["subtopic_gates"][0]["subtopic_id"] = base["subtopic_gates"][0]["subtopic_id"]
        path = self.temp_json(extension)
        with self.assertRaises(EngineeringRegistryCompositionError) as ctx:
            load_canonical_engineering_registry(extension_rels=[str(path)])
        self.assertEqual(ctx.exception.code, "MATH_ENG_EXTENSION_DUPLICATE_GATE_ID")

    def test_v2_crosswalk_patch_stale_extension_blob_fails_closed(self):
        patch = raw(DEFAULT_CROSSWALK)
        patch["engineering_extension_git_blob_sha"] = "0" * 40
        path = self.temp_json(patch)
        with self.assertRaises(MathematicsAssessmentEngineeringCrosswalkError) as ctx:
            load_crosswalk(path)
        self.assertEqual(ctx.exception.code, "MATH_ENG_CROSSWALK_PATCH_EXTENSION_STALE")

    def test_v2_crosswalk_patch_stale_base_crosswalk_blob_fails_closed(self):
        patch = raw(DEFAULT_CROSSWALK)
        patch["base_crosswalk_git_blob_sha"] = "0" * 40
        path = self.temp_json(patch)
        with self.assertRaises(MathematicsAssessmentEngineeringCrosswalkError) as ctx:
            load_crosswalk(path)
        self.assertEqual(ctx.exception.code, "MATH_ENG_CROSSWALK_PATCH_BASE_STALE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
