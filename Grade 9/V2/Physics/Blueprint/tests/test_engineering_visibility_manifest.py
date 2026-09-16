import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1] / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from compile_engineering_visibility_manifest import (  # noqa: E402
    compile_visibility_manifest,
    validate_visibility_manifest,
)
from compile_physics_engineering_workbench import (  # noqa: E402
    compile_binding,
    compile_closure,
    load,
    resolve_manifest,
)


REGISTRY = load("policies/physics-technical-engineering-gates.v1.json")


def request_for_gate(gate_id: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "request_id": "PHY-ENG-REQ-VISIBILITY_TEST",
        "scope_kind": "ENGINEERING_GATE",
        "scope_refs": [gate_id],
        "engineering_depth": "STANDARD",
        "learning_purpose": "FIRST_STUDY",
        "owner_decision_ref": None,
    }


class EngineeringVisibilityManifestTests(unittest.TestCase):
    def build_inputs(self, root: Path):
        gate_id = REGISTRY["subtopic_gates"][0]["subtopic_id"]
        request = request_for_gate(gate_id)
        manifest = resolve_manifest(request, copy.deepcopy(REGISTRY))
        receipt = compile_closure(request, manifest, copy.deepcopy(REGISTRY))
        binding = compile_binding(request, manifest, receipt, "CANONICAL_DOMAIN_REGISTRY")

        refs = {}
        for name, value in (("request", request), ("manifest", manifest), ("binding", binding)):
            path = root / f"{name}.json"
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            refs[name] = str(path.resolve())
        admission = {
            "schema_version": "2.0.0",
            "subject": "PHYSICS",
            "admission_id": "PHY-ENG-DOMAIN-ADMISSION-VISIBILITY_TEST",
            "domain_registry_ref": str((root / "domain_registry.json").resolve()),
            "authorizations": [{
                "authorization_id": "PHY-ENG-AUTH-VISIBILITY_TEST",
                "engineering_request_ref": refs["request"],
                "engineering_manifest_ref": refs["manifest"],
                "engineering_binding_ref": refs["binding"],
            }],
            "subtopic_gate_map": [{
                "subtopic_id": "TEST-SUBTOPIC",
                "gate_bindings": [{
                    "engineering_gate_id": gate_id,
                    "authorization_ref": "PHY-ENG-AUTH-VISIBILITY_TEST",
                }],
            }],
        }
        return admission, {"status": "PASS", "release_id": "VISIBILITY-TEST"}, gate_id, Path(refs["binding"])

    def test_visibility_is_derived_from_exact_bound_engineering(self):
        with tempfile.TemporaryDirectory() as td:
            admission, release_gate, gate_id, _ = self.build_inputs(Path(td))
            visibility = compile_visibility_manifest(admission, release_gate, registry=copy.deepcopy(REGISTRY))
            audit = validate_visibility_manifest(visibility)
            self.assertEqual(audit["status"], "PASS")
            self.assertEqual(visibility["publication_authorization"], "NOT_IMPLIED")
            self.assertEqual(visibility["authority"], "NON_AUTHORITATIVE_VIEW_OF_BOUND_ENGINEERING_AUTHORITY")
            self.assertIn(gate_id, {row["gate_id"] for row in visibility["gates"]})
            row = next(row for row in visibility["gates"] if row["gate_id"] == gate_id)
            self.assertEqual(row["technical_state"], "READY")
            self.assertTrue(row["release_checklist_pass"])
            self.assertEqual(row["structure_counts"]["representations"], len(row["representations"]))
            self.assertEqual(row["structure_counts"]["misconceptions"], len(row["misconceptions"]))
            self.assertEqual(row["structure_counts"]["verification_obligations"], len(row["verification_obligations"]))

    def test_stale_binding_cannot_render_visibility(self):
        with tempfile.TemporaryDirectory() as td:
            admission, release_gate, _, binding_path = self.build_inputs(Path(td))
            binding = json.loads(binding_path.read_text(encoding="utf-8"))
            binding["registry_digest"] = "sha256:" + "0" * 64
            binding_path.write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(Exception, "PHY_ENG_BIND_REGISTRY_DIGEST_MISMATCH"):
                compile_visibility_manifest(admission, release_gate, registry=copy.deepcopy(REGISTRY))

    def test_visibility_requires_released_product(self):
        with tempfile.TemporaryDirectory() as td:
            admission, _, _, _ = self.build_inputs(Path(td))
            with self.assertRaisesRegex(ValueError, "PHY_ENG_VISIBILITY_RELEASE_GATE_REQUIRED"):
                compile_visibility_manifest(admission, {"status": "BLOCKED"}, registry=copy.deepcopy(REGISTRY))

    def test_visibility_cannot_claim_publication_authority(self):
        with tempfile.TemporaryDirectory() as td:
            admission, release_gate, _, _ = self.build_inputs(Path(td))
            visibility = compile_visibility_manifest(admission, release_gate, registry=copy.deepcopy(REGISTRY))
            visibility["publication_authorization"] = "ALLOWED"
            with self.assertRaises(Exception):
                validate_visibility_manifest(visibility)


if __name__ == "__main__":
    unittest.main()
