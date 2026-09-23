from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
for entry in (SCRIPTS, TESTS):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

from relay_can import evaluate
from validate_foundation import validate
from v3lib import validate_schema
from test_v3_foundation import DIGEST, dump, materialize


WRITE_PATH = "skills/engineering-pr-delivery-v3.1/scripts/new_feature.py"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def prepare_git(root: Path) -> tuple[str, str]:
    materialize(root)
    (root / "skills/engineering-pr-delivery-v3.1/scripts").mkdir(parents=True, exist_ok=True)
    (root / "skills/engineering-pr-delivery-v3.1/scripts/base.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "deps").mkdir(parents=True, exist_ok=True)
    (root / "deps/compiler.py").write_text("VERSION = 1\n", encoding="utf-8")
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs/unrelated.md").write_text("base\n", encoding="utf-8")

    subprocess.check_call(["git", "-C", str(root), "init", "-b", "exec"], stdout=subprocess.DEVNULL)
    git(root, "config", "user.email", "relay@example.test")
    git(root, "config", "user.name", "Relay Test")
    git(root, "add", ".")
    git(root, "commit", "-m", "material base")
    base_sha = git(root, "rev-parse", "HEAD")
    git(root, "branch", "base")

    ep_path = root / "relay/WORK/EP-TA-011.yaml"
    ep = yaml.safe_load(ep_path.read_text(encoding="utf-8"))
    ep["basis"]["material_base"] = base_sha
    ep["basis"]["semantic_dependencies"] = [
        {"path": "deps/compiler.py", "reason": "Compiler semantics affect the EP."}
    ]
    dump(ep_path, ep)

    lease_path = root / "relay/LEASES/LEASE-TA-011-01.yaml"
    lease = yaml.safe_load(lease_path.read_text(encoding="utf-8"))
    lease["basis"]["material_base"] = base_sha
    dump(lease_path, lease)

    git(root, "add", "relay/WORK/EP-TA-011.yaml", "relay/LEASES/LEASE-TA-011-01.yaml")
    git(root, "commit", "-m", "coordination config")
    return base_sha, "base"


def add_control(root: Path, control: dict) -> None:
    path = root / "relay/CONTROLS/controls.yaml"
    controls = yaml.safe_load(path.read_text(encoding="utf-8"))
    controls["controls"].append(control)
    dump(path, controls)


def owner_authority(action: str) -> dict:
    return {
        "id": f"CTRL-OWNER-{action}",
        "kind": "OWNER",
        "state": "OPEN",
        "source": {"type": "OWNER", "ref": f"direct-owner:{action.lower()}"},
        "condition": f"Owner explicitly authorizes {action}.",
        "blocks": [],
        "permits": [action],
        "resolution": {"condition": "Action completed or authority revoked.", "evidence": []},
    }


def advance_base(root: Path, path: str, content: str) -> str:
    git(root, "checkout", "base")
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    git(root, "add", path)
    git(root, "commit", "-m", f"base changes {path}")
    sha = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "exec")
    return sha


class RelayCanTests(unittest.TestCase):
    def test_material_write_allows_disjoint_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            advance_base(root, "docs/unrelated.md", "unrelated base change\n")
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertTrue(result["allowed"], result)
            self.assertEqual(["ALLOW"], result["reason_codes"])
            self.assertTrue(any(item == "drift:DISJOINT" for item in result["basis"]), result)

    def test_stale_generated_snapshot_does_not_block_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            snapshot_path = root / "relay/GENERATED/CURRENT_SNAPSHOT.yaml"
            snapshot = yaml.safe_load(snapshot_path.read_text(encoding="utf-8"))
            snapshot["execution"]["ep"] = "EP-STALE"
            dump(snapshot_path, snapshot)
            self.assertTrue(validate(root))
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertTrue(result["allowed"], result)

    def test_delivery_only_control_does_not_block_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            add_control(root, {
                "id": "CTRL-PROJECTION",
                "kind": "DELIVERY",
                "state": "OPEN",
                "source": {"type": "PROVIDER", "ref": "github:stale-projection"},
                "condition": "External projection is stale.",
                "blocks": ["HANDOVER", "PR_READY"],
                "permits": ["MATERIAL_WRITE", "TEST"],
                "resolution": {"condition": "Projection converges.", "evidence": []},
            })
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertTrue(result["allowed"], result)

    def test_write_collision_blocks_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            add_control(root, {
                "id": "CTRL-COLLISION",
                "kind": "COLLISION",
                "state": "OPEN",
                "source": {"type": "VALIDATOR", "ref": "exclusive-lease-check"},
                "condition": "Competing writer overlaps this serial route.",
                "blocks": ["MATERIAL_WRITE"],
                "permits": ["READ", "ANALYZE"],
                "resolution": {"condition": "Exclusive ownership restored.", "evidence": []},
            })
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertFalse(result["allowed"], result)
            self.assertIn("CONTROL_BLOCKS_ACTION", result["reason_codes"])
            self.assertEqual(["CTRL-COLLISION"], result["blocking_controls"])

    def test_relevant_dependency_drift_blocks_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            advance_base(root, "deps/compiler.py", "VERSION = 2\n")
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertFalse(result["allowed"], result)
            self.assertIn("DRIFT_RELEVANT", result["reason_codes"])
            self.assertTrue(any(item == "drift:RELEVANT" for item in result["basis"]), result)

    def test_unknown_drift_blocks_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="does-not-exist")
            self.assertFalse(result["allowed"], result)
            self.assertIn("DRIFT_UNKNOWN", result["reason_codes"])

    def test_missing_base_ref_blocks_material_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH)
            self.assertFalse(result["allowed"], result)
            self.assertIn("BASE_REF_REQUIRED", result["reason_codes"])

    def test_protected_or_out_of_scope_path_is_denied(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = evaluate(
                root,
                "MATERIAL_WRITE",
                path="skills/three-pass-prompt-generator/schema.md",
                base_ref="base",
            )
            self.assertFalse(result["allowed"], result)
            self.assertIn("PATH_OUTSIDE_EP_WRITE_SCOPE", result["reason_codes"])
            self.assertIn("PATH_PROTECTED", result["reason_codes"])

    def test_owner_override_allows_bounded_write_but_not_merge(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            lease_path = root / "relay/LEASES/LEASE-TA-011-01.yaml"
            lease = yaml.safe_load(lease_path.read_text(encoding="utf-8"))
            lease["admission"] = {
                "method": "OWNER_OVERRIDE",
                "result": "PASS",
                "repository_only": False,
                "qualification": {"required": False, "qset": None, "evaluator": None, "result": None, "evidence": []},
                "owner_basis": {
                    "direct_utterance_digest": DIGEST,
                    "session_timestamp": "2026-09-22T03:29:06Z",
                },
            }
            lease["scope"] = {
                "ep_or_task": "EP-TA-011",
                "branch": "v3/issue-418-foundation",
                "allowed_writes": ["skills/engineering-pr-delivery-v3.1/**"],
                "prohibited": ["MERGE", "RELEASE"],
            }
            dump(lease_path, lease)

            write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertTrue(write["allowed"], write)

            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["delivery"] = {
                "required": True,
                "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
            }
            dump(state_path, state)
            add_control(root, owner_authority("MERGE"))
            merge = evaluate(root, "MERGE")
            self.assertFalse(merge["allowed"], merge)
            self.assertIn("OWNER_OVERRIDE_DELIVERY_FORBIDDEN", merge["reason_codes"])

    def test_checkpoint_requires_live_base_ref(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            denied = evaluate(root, "CHECKPOINT")
            self.assertFalse(denied["allowed"], denied)
            self.assertIn("BASE_REF_REQUIRED", denied["reason_codes"])

            allowed = evaluate(root, "CHECKPOINT", base_ref="base")
            self.assertTrue(allowed["allowed"], allowed)

    def test_handover_and_pr_ready_do_not_require_active_execution_lease(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["execution"] = {"lifecycle": "IDLE", "ep": None, "lease": None, "route": None}
            state["delivery"] = {
                "required": True,
                "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
            }
            dump(state_path, state)

            lease_path = root / "relay/LEASES/LEASE-TA-011-01.yaml"
            lease = yaml.safe_load(lease_path.read_text(encoding="utf-8"))
            lease["state"] = "RELEASED"
            dump(lease_path, lease)

            handover = evaluate(root, "HANDOVER")
            self.assertTrue(handover["allowed"], handover)
            local_export = evaluate(root, "LOCAL_EXECUTION_EXPORT")
            self.assertTrue(local_export["allowed"], local_export)
            draft_update = evaluate(root, "DRAFT_PR_UPDATE")
            self.assertTrue(draft_update["allowed"], draft_update)
            pr_ready = evaluate(root, "PR_READY")
            self.assertTrue(pr_ready["allowed"], pr_ready)

    def test_pr_ready_requires_pull_request_delivery_vehicle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            result = evaluate(root, "PR_READY")
            self.assertFalse(result["allowed"], result)
            self.assertIn("DELIVERY_VEHICLE_REQUIRED", result["reason_codes"])

    def test_prepared_selector_cannot_authorize_live_v3_execution(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            dump(root / "relay/PROTOCOL_SELECTION.yaml", {
                "schema_version": "relay-v3.1-protocol-selection",
                "selected_protocol": "V2_5",
                "status": "PREPARED",
                "legacy": {"root": "agents/relay", "tree_digest": "sha256:" + ("a" * 64), "policy": "LIVE_COMPATIBILITY"},
                "v3": {"state_path": "relay/STATE.yaml", "validation": "PENDING"},
                "cutover": {"owner_authorized": False, "owner_basis": None, "readiness_digest": None, "activated_at": None},
            })
            (root / "agents/relay").mkdir(parents=True, exist_ok=True)
            (root / "agents/relay/REPO_STATE.yaml").write_text("schema_version: relay-v2.5\n", encoding="utf-8")

            write = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertFalse(write["allowed"], write)
            self.assertIn("PROTOCOL_NOT_ACTIVE", write["reason_codes"])

            handover = evaluate(root, "HANDOVER")
            self.assertTrue(handover["allowed"], handover)

    def test_merge_requires_explicit_owner_delivery_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["delivery"] = {
                "required": True,
                "primary_vehicle": {"provider": "GITHUB", "kind": "PULL_REQUEST", "number": 419},
            }
            dump(state_path, state)

            denied = evaluate(root, "MERGE")
            self.assertFalse(denied["allowed"], denied)
            self.assertEqual(["OWNER_DELIVERY_AUTHORITY_REQUIRED"], denied["reason_codes"])

            add_control(root, owner_authority("MERGE"))
            allowed = evaluate(root, "MERGE")
            self.assertTrue(allowed["allowed"], allowed)
            self.assertEqual(["ALLOW"], allowed["reason_codes"])

    def test_merge_requires_delivery_vehicle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)
            add_control(root, owner_authority("MERGE"))
            result = evaluate(root, "MERGE")
            self.assertFalse(result["allowed"], result)
            self.assertIn("DELIVERY_VEHICLE_REQUIRED", result["reason_codes"])


    def test_parallel_lifecycle_is_rejected_as_execution_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prepare_git(root)

            state_path = root / "relay/STATE.yaml"
            state = yaml.safe_load(state_path.read_text(encoding="utf-8"))
            state["execution"]["lifecycle"] = "PARALLEL"

            schema_errors = validate_schema("state", state, "STATE")
            self.assertTrue(schema_errors)
            self.assertTrue(
                any("PARALLEL" in item or "lifecycle" in item for item in schema_errors),
                schema_errors,
            )

            dump(state_path, state)
            result = evaluate(root, "MATERIAL_WRITE", path=WRITE_PATH, base_ref="base")
            self.assertFalse(result["allowed"], result)
            self.assertIn("INVALID_FOUNDATION", result["reason_codes"])


if __name__ == "__main__":
    unittest.main()
