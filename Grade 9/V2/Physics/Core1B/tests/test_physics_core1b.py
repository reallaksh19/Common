from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "core1b_common.py"
SPEC = importlib.util.spec_from_file_location("core1b_common", ENGINE)
core1b = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(core1b)


class Core1BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "registry" / "projectile-vertical-event-atoms-v1.json").read_text())
        cls.unit = json.loads((ROOT / "golden" / "projectile-vertical-event" / "core1b-unit.json").read_text())

    def test_golden_registry_and_unit_pass(self):
        core1b.validate_atom_registry(self.registry)
        core1b.validate_unit(self.unit, self.registry)

    def test_prerequisite_cycle_fails(self):
        broken = json.loads(json.dumps(self.registry))
        broken["atoms"][0]["prerequisites"] = ["PHY-A-EQ-01"]
        with self.assertRaises(core1b.Core1BValidationError):
            core1b.validate_atom_registry(broken)

    def test_internal_labels_must_not_leak(self):
        broken = json.loads(json.dumps(self.unit))
        broken["learner_surface"]["teacher_moves"][0] = "Enter DIAGNOSTIC_BRANCH now."
        with self.assertRaises(core1b.Core1BValidationError):
            core1b.validate_unit(broken, self.registry)

    def test_release_requires_independent_readiness(self):
        broken = json.loads(json.dumps(self.unit))
        broken["readiness"]["first_move"] = False
        with self.assertRaises(core1b.Core1BValidationError):
            core1b.validate_unit(broken, self.registry)

    def test_receipt_has_no_unresolved_atoms(self):
        evidence = core1b.build_independent_evidence(self.unit, "PHY-LS-P20", "PF-PROJECTILE-VERTICAL-EVENT")
        receipt = core1b.build_release_receipt(
            self.unit,
            "E1B-PHY-GOLDEN",
            "T-PHY-M2D-EVENT-001",
            "PF-PROJECTILE-VERTICAL-EVENT",
        )
        self.assertEqual("INDEPENDENT", evidence["state"])
        self.assertEqual([], receipt["unresolved_required_atoms"])


if __name__ == "__main__":
    unittest.main()
