import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
TESTS = ROOT / "tests"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(TESTS))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_core_authority import compile_core_authority  # noqa: E402
from compile_chemistry_core_product_custody import compile_core_product_custody  # noqa: E402
from test_chemistry_four_core_compilation import (  # noqa: E402
    make_manifest,
    make_production_audit,
    make_request,
    payloads,
    scope_for,
)

REGISTRY = json.loads((ROOT / "policies" / "chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))
MODES = ("CORE1A", "CORE1B", "CORE2A", "CORE2B")


def first_ready_gate_for_grade(grade: int):
    rows = [
        gate for gate in REGISTRY["subtopic_gates"]
        if gate.get("technical_readiness") == "ENGINEERING_GATE_READY"
        and (gate.get("cbse_ref") or {}).get("grade") == grade
    ]
    if not rows:
        raise AssertionError(f"No engineering-ready Chemistry gate found for grade {grade}")
    return rows[0]


class ChemistryFourCoreCrossGradeTests(unittest.TestCase):
    def test_same_four_core_compiler_closes_grade9_and_grade11_gates(self):
        selected = [first_ready_gate_for_grade(9), first_ready_gate_for_grade(11)]
        self.assertNotEqual(selected[0]["subtopic_id"], selected[1]["subtopic_id"])

        for gate in selected:
            with self.subTest(grade=gate["cbse_ref"]["grade"], gate=gate["subtopic_id"]):
                audit_ref = f"tests/in-memory-cross-grade-{gate['cbse_ref']['grade']}-audit.json"
                audit = make_production_audit(gate)
                request = make_request()
                manifest = make_manifest(gate, audit_ref)
                audit_payloads = {audit_ref: audit}
                packet = compile_blueprint_obligations(
                    request,
                    manifest,
                    registry=REGISTRY,
                    source_audit_payloads=audit_payloads,
                )
                self.assertEqual(packet["status"], "BLUEPRINT_OBLIGATIONS_READY")
                self.assertEqual(packet["direct_gate_ids"], [gate["subtopic_id"]])

                for mode in MODES:
                    realized = [
                        row["obligation_id"]
                        for row in packet["obligations"]
                        if mode in row["authorized_modes"]
                    ]
                    authority = compile_core_authority(
                        mode,
                        "TEST_ONLY",
                        payloads(gate)[mode],
                        packet,
                        realized,
                        authority_id=f"CHEM-CORE-AUTH-CROSS-GRADE-{gate['cbse_ref']['grade']}-{mode}",
                        payload_ref=f"tests/cross-grade-{mode.lower()}.json",
                    )
                    self.assertEqual(authority["representation_closure"]["status"], "PASS")
                    scope = scope_for(authority, audit, audit_ref)
                    custody = compile_core_product_custody(
                        request,
                        manifest,
                        packet,
                        scope,
                        authority,
                        registry=REGISTRY,
                        source_audit_payloads=audit_payloads,
                    )
                    self.assertEqual(custody["status"], "CORE_PRODUCT_CUSTODY_READY")
                    self.assertEqual(custody["product_mode"], mode)
                    self.assertEqual(custody["subtopic_id"], "TEST_ONLY")

    def test_cross_grade_acceptance_selects_by_registry_metadata_not_topic_name(self):
        engine_names = (
            "compile_chemistry_blueprint_obligations.py",
            "compile_chemistry_core_authority.py",
            "compile_chemistry_core_product_custody.py",
            "validate_chemistry_core_source_scope.py",
        )
        generic_source = "\n".join((ENGINE / name).read_text(encoding="utf-8").lower() for name in engine_names)
        forbidden = ("re" + "dox", "mn" + "o4", "perman" + "ganate")
        for token in forbidden:
            self.assertNotIn(token, generic_source)
        harness_source = Path(__file__).read_text(encoding="utf-8").lower()
        self.assertIn("cbse_ref", harness_source)
        self.assertIn("technical_readiness", harness_source)


if __name__ == "__main__":
    unittest.main()
