from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from v25_lease_view import CompatibilityError, build_view
from v3lib import validate_schema


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def fixture(root: Path, *, qualified: bool = False, tc_result: str = "PASS"):
    disc_path = "agents/relay/certifications/discovery/DISC-0001.yaml"
    tc_path = "agents/relay/certifications/takeover/TC-0001.yaml"
    qual_path = "agents/relay/certifications/qualification/QUAL-0001.yaml"
    admission = {
        "route_key": "SERIAL:EP-0001",
        "candidate": {"agent_instance_id": "legacy-agent"},
        "discovery_receipt": {"id": "DISC-0001", "path": disc_path},
        "certification": {"id": "TC-0001", "path": tc_path},
    }
    disc = {
        "id": "DISC-0001",
        "candidate": {"agent_instance_id": "legacy-agent"},
        "result": "PASS",
    }
    tc = {
        "id": "TC-0001",
        "candidate": {"agent_instance_id": "legacy-agent"},
        "route": {"route_key": "SERIAL:EP-0001", "ep_id": "EP-0001"},
        "basis": {
            "material_ref": "abc1234",
            "roadmap_revision": "RM-0001",
            "relay_protocol_basis_ref": "common-v2.5",
        },
        "discovery_receipt": {"id": "DISC-0001", "path": disc_path},
        "qualification": {
            "required": qualified,
            "status": "PASS" if qualified else "NOT_REQUIRED",
            "receipt_id": "QUAL-0001" if qualified else None,
            "receipt_path": qual_path if qualified else None,
            "receipt_digest": "sha256:legacy" if qualified else None,
        },
        "result": tc_result,
    }
    dump(root / disc_path, disc)
    dump(root / tc_path, tc)
    if qualified:
        dump(root / qual_path, {"id": "QUAL-0001", "result": "PASS"})
    return admission


class V25LeaseViewTests(unittest.TestCase):
    def test_pass_evidence_becomes_non_authoritative_compatibility_view(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            admission = fixture(root)
            view = build_view(
                root,
                admission,
                validation_status="PASS",
                validation_basis=["legacy validator PASS"],
            )
            self.assertEqual("DERIVED_COMPATIBILITY_VIEW", view["authority"])
            self.assertFalse(view["native_lease"])
            self.assertFalse(view["may_authorize_v3_actions"])
            self.assertEqual("2.5", view["source_protocol"])
            self.assertEqual("NOT_REQUIRED", view["qualification"]["status"])
            self.assertEqual([], validate_schema("v25-lease-view", view, "VIEW"))
            self.assertFalse((root / "relay/EVENTS.jsonl").exists())

    def test_qualified_legacy_evidence_is_preserved_as_reference(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            admission = fixture(root, qualified=True)
            view = build_view(
                root,
                admission,
                validation_status="PASS",
                validation_basis=["legacy validator PASS"],
            )
            self.assertTrue(view["qualification"]["required"])
            self.assertEqual("PASS", view["qualification"]["status"])
            self.assertEqual(
                "agents/relay/certifications/qualification/QUAL-0001.yaml",
                view["source_evidence"]["qualification"],
            )

    def test_failed_legacy_certification_cannot_look_passed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            admission = fixture(root, tc_result="FAIL")
            view = build_view(
                root,
                admission,
                validation_status="PASS",
                validation_basis=["synthetic upstream status"],
            )
            self.assertEqual("FAIL", view["validation"]["status"])
            self.assertFalse(view["may_authorize_v3_actions"])

    def test_pointer_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            admission = fixture(root)
            admission["certification"]["id"] = "TC-WRONG"
            with self.assertRaisesRegex(CompatibilityError, "pointer does not match"):
                build_view(
                    root,
                    admission,
                    validation_status="PASS",
                    validation_basis=["legacy validator PASS"],
                )


if __name__ == "__main__":
    unittest.main()
