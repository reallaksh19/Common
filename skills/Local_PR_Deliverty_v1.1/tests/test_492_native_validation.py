import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(TESTS))

from acceptance_basis import canonical_digest
from test_protocol import example_bundle, readdress_review_lease

SPEC = importlib.util.spec_from_file_location("validate_native", ROOT / "scripts" / "validate_native.py")
native = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(native)


PRD = "PRD-492-NATIVE"
EPOCH = "AE-492-2"
PROFILE = "APR-PRD-492-NATIVE-AE2"
DIGEST64 = "d" * 64


def _replace_task_id(bundle, old, new):
    for stage in bundle["stages"]:
        if stage["task_id"] == old:
            stage["task_id"] = new
    for result in bundle["results"]:
        if result["task_id"] == old:
            result["task_id"] = new
    for collection in ["review_leases", "context_snapshots", "waivers", "observed_states"]:
        for record in bundle["support"][collection]:
            if record.get("task_id") == old:
                record["task_id"] = new
    if old in bundle["observed"].get("spec_digests", {}):
        bundle["observed"]["spec_digests"][new] = bundle["observed"]["spec_digests"].pop(old)
    if old in bundle["observed"].get("target_heads", {}):
        bundle["observed"]["target_heads"][new] = bundle["observed"]["target_heads"].pop(old)
    if old in bundle["observed"].get("dependency_heads", {}):
        bundle["observed"]["dependency_heads"][new] = bundle["observed"]["dependency_heads"].pop(old)


def _role_bindings(protocol, criterion_id, role):
    criterion = next(
        criterion
        for acceptance_set in protocol["acceptance_sets"]
        for criterion in acceptance_set["criteria"]
        if criterion["id"] == criterion_id
    )
    methods = {method["id"]: method for method in protocol["verification_methods"]}
    rows = []
    for method_id in criterion["verification_method_ids"]:
        method = methods[method_id]
        if role not in method["applies_to_roles"]:
            continue
        rows.append({
            "criterion_id": criterion_id,
            "verification_method_id": method_id,
            "harness_id": method["harness_id"],
            "external_gate_id": method["external_gate_id"],
            "required_evidence_classes": list(method["required_evidence_classes"]),
        })
    return rows


def make_native_bundle(*, collapse=False, complete=True):
    bundle = example_bundle()
    if not complete:
        bundle["stages"] = bundle["stages"][:3]
        bundle["results"] = []
        bundle["observed"]["main_sha"] = "b" * 40
        bundle["observed"]["merged"] = {}
        bundle["observed"]["pr_states"]["101"] = "DRAFT"
        bundle["observed"]["issue_states"] = {"85": "OPEN", "86": "OPEN"}

    parent, child = bundle["tasks"]
    old_task_id = child["task_id"]
    protocol = bundle["support"]["project_protocols"][0]
    original_acceptance = copy.deepcopy(child["acceptance"])
    criterion_ids = [row["id"] for row in original_acceptance]

    _replace_task_id(bundle, old_task_id, PRD)
    child["task_id"] = PRD
    child["kind"] = "RESPONSIBILITY"
    child["representation"] = {
        "kind": "SINGLE_ISSUE",
        "primary_issue": child["issue"],
        "member_issues": [child["issue"]],
        "predecessor_attempt_refs": [],
        "delivery_pr_history": [child["pr"]],
    }
    child["acceptance_epoch_id"] = EPOCH
    child["acceptance_profile_ref"] = PROFILE
    child["acceptance"] = []

    protected_surface_digest = canonical_digest(protocol["protected_surface"])
    epoch = {
        "record": "ACCEPTANCE_EPOCH",
        "version": "1",
        "epoch_id": EPOCH,
        "parent_task_id": parent["task_id"],
        "previous_epoch_id": None,
        "project_protocol_ref": protocol["source_ref"],
        "project_protocol_digest": protocol["digest"],
        "protected_surface_digest": protected_surface_digest,
        "adopted_by": "owner",
        "adoption_ref": "https://example.invalid/issues/85#epoch-adoption",
        "adopted_at": "2026-10-03T23:30:00Z",
        "change_proposal_ref": "ACP-492-2",
        "change_kind": "DEFECT_REPAIR",
        "risk_effect": "STRENGTHENING",
        "digest": "0" * 64,
    }
    epoch["digest"] = canonical_digest(epoch)

    profile = {
        "record": "ACCEPTANCE_PROFILE",
        "version": "1",
        "profile_id": PROFILE,
        "task_id": PRD,
        "acceptance_epoch_id": EPOCH,
        "project_protocol_ref": protocol["source_ref"],
        "project_protocol_digest": protocol["digest"],
        "acceptance_set_refs": [protocol["acceptance_sets"][0]["id"]],
        "criterion_refs": criterion_ids,
        "excluded_criteria": [],
        "parameters": {},
        "role_bindings": {
            "REVIEWER": sum((_role_bindings(protocol, cid, "REVIEWER") for cid in criterion_ids), []),
            "COORDINATOR": sum((_role_bindings(protocol, cid, "COORDINATOR") for cid in criterion_ids), []),
        },
        "external_gate_ids": [gate["id"] for gate in protocol["external_gates"] if gate["applies_to"] in ["CHILD", "ALL"]],
        "dependency_requirements": [],
        "digest": "0" * 64,
    }
    profile["digest"] = canonical_digest(profile)
    child["acceptance_profile_digest"] = profile["digest"]

    parent["control_plane"] = {
        "bootstrap_state": "ESTABLISHED",
        "current_acceptance_epoch_id": EPOCH,
        "acceptance_basis_registry": [{
            "epoch_id": EPOCH,
            "epoch_ref": "native://acceptance-epoch/" + EPOCH,
            "epoch_digest": epoch["digest"],
        }],
        "responsibility_registry": [{
            "task_id": PRD,
            "release_state": "READY",
            "acceptance_profile_ref": PROFILE,
            "acceptance_profile_digest": profile["digest"],
        }],
        "authority_grant_refs": [],
    }

    # Native permission targets PRD identity, not provider issue number.
    permission = parent["start_permissions"][0]
    permission["child_issue"] = None
    permission["responsibility_task_id"] = PRD

    # Native review leases bind the adopted basis in addition to exact candidate/context.
    for lease in list(bundle["support"]["review_leases"]):
        if lease["task_id"] == PRD:
            lease["acceptance_epoch_id"] = EPOCH
            lease["acceptance_profile_digest"] = profile["digest"]
            readdress_review_lease(bundle, lease)

    grants = []
    transitions = []
    if collapse:
        # Reviewer and Coordinator are intentionally the same authenticated principal.
        shared = "reviewer"
        parent["parent_owner"] = shared
        child["parent_owner"] = shared
        parent["role_principals"] = {
            "CODER": ["coder", "new-coder", "other-coder"],
            "REVIEWER": [shared],
            "COORDINATOR": [shared],
        }
        child["role_principals"] = copy.deepcopy(parent["role_principals"])
        permission["coordinator"] = shared

        coordinator = next(stage for stage in bundle["stages"] if stage["task_id"] == PRD and stage["stage"] == "COORDINATOR")
        coordinator["executor"] = shared
        coordinator["role_integrity"]["principal"] = shared
        for evidence in bundle["support"]["evidence_records"]:
            if evidence["collected_by_role"] == "COORDINATOR" and evidence["collected_by_principal"] == "coordinator":
                evidence["collected_by_principal"] = shared
                if evidence["origin_kind"] == "STAGE_EXECUTOR":
                    evidence["origin_principal"] = shared
        for lease in list(bundle["support"]["review_leases"]):
            if lease["task_id"] == PRD and lease["certifier_role"] == "COORDINATOR":
                lease["certifier_principal"] = shared
                readdress_review_lease(bundle, lease)

        parent_check = next(stage for stage in bundle["stages"] if stage["stage"] == "PARENT_CHECK") if complete else None
        if parent_check:
            parent_check["executor"] = shared
            parent_check["role_integrity"]["principal"] = shared
            for evidence in bundle["support"]["evidence_records"]:
                if evidence["collected_by_role"] == "PARENT_CHECK" and evidence["collected_by_principal"] == "coordinator":
                    evidence["collected_by_principal"] = shared
                    if evidence["origin_kind"] == "STAGE_EXECUTOR":
                        evidence["origin_principal"] = shared
            for lease in list(bundle["support"]["review_leases"]):
                if lease["task_id"] == parent["task_id"] and lease["certifier_role"] == "PARENT_CHECK":
                    lease["certifier_principal"] = shared
                    readdress_review_lease(bundle, lease)

        grant = {
            "record": "AUTHORITY_GRANT",
            "version": "1",
            "grant_id": "AUTH-ROLE-COLLAPSE-1",
            "principal": shared,
            "capability": "ROLE_EXECUTION",
            "scope": {
                "parent_task_id": parent["task_id"],
                "responsibility_task_id": PRD,
                "acceptance_epoch_id": EPOCH,
            },
            "issued_by": "owner",
            "instruction_ref": "https://example.invalid/issues/85#owner-role-collapse",
            "issued_at": "2026-10-04T00:00:45Z",
            "expires_at": None,
            "revoked_at": None,
            "source_kind": "DIRECT_OWNER_SESSION",
            "source_digest": "a" * 64,
            "authentication_status": "AUTHENTICATED",
        }
        grants.append(grant)
        parent["control_plane"]["authority_grant_refs"] = [grant["grant_id"]]

        reviewer = next(stage for stage in bundle["stages"] if stage["task_id"] == PRD and stage["stage"] == "REVIEWER")
        replay_refs = list(coordinator["acceptance_results"][0]["evidence_ids"])
        transitions.append({
            "record": "ROLE_TRANSITION",
            "version": "1",
            "transition_id": "RT-REVIEWER-COORDINATOR-1",
            "task_id": PRD,
            "previous_record_id": reviewer["record_id"],
            "next_record_id": coordinator["record_id"],
            "transition_at": "2026-10-04T00:01:45Z",
            "role_execution_grant_ref": grant["grant_id"],
            "previous_end_ref": reviewer["publications"]["end"]["comment_ref"],
            "previous_timer_stop_ref": "timer://reviewer/stop/S2",
            "next_start_ref": coordinator["publications"]["start"]["comment_ref"],
            "next_timer_arm_ref": "timer://coordinator/arm/S3",
            "next_context_start_ref": coordinator["context_start_ref"],
            "fresh_replay_evidence_refs": replay_refs,
        })

    bundle["native_support"] = {
        "acceptance_epochs": [epoch],
        "acceptance_profiles": [profile],
        "authority_grants": grants,
        "role_transitions": transitions,
    }
    return bundle


class NativeValidation492Tests(unittest.TestCase):
    def test_native_responsibility_delegates_to_established_validator(self):
        bundle = make_native_bundle()
        result = native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")
        self.assertEqual(result["record_consistency"], "PASS")
        self.assertEqual(result["native_projection"], "PASS")
        self.assertEqual(result["native_responsibility_ids"], [PRD])
        self.assertFalse(result["projection_mutated_source"])

    def test_native_validation_does_not_mutate_source_records(self):
        bundle = make_native_bundle()
        before = json.dumps(bundle, sort_keys=True)
        native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")
        self.assertEqual(json.dumps(bundle, sort_keys=True), before)
        child = next(task for task in bundle["tasks"] if task["task_id"] == PRD)
        self.assertEqual(child["kind"], "RESPONSIBILITY")
        self.assertEqual(child["acceptance"], [])

    def test_profile_digest_drift_is_rejected_before_legacy_projection(self):
        bundle = make_native_bundle()
        bundle["tasks"][1]["acceptance_profile_digest"] = "f" * 64
        with self.assertRaisesRegex(native.NativeValidationError, "Profile digest mismatch"):
            native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")

    def test_review_lease_must_bind_epoch_and_profile(self):
        bundle = make_native_bundle()
        lease = next(lease for lease in bundle["support"]["review_leases"] if lease["task_id"] == PRD)
        lease["acceptance_epoch_id"] = "AE-OLD"
        readdress_review_lease(bundle, lease)
        with self.assertRaisesRegex(native.NativeValidationError, "review lease acceptance epoch is stale"):
            native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")

    def test_owner_authorized_same_principal_reviewer_coordinator_validates(self):
        bundle = make_native_bundle(collapse=True)
        result = native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")
        self.assertEqual(result["record_consistency"], "PASS")
        self.assertEqual(result["role_transition_summary"]["same_principal_collapses"], 1)
        self.assertEqual(result["role_transition_summary"]["transition_records_used"], ["RT-REVIEWER-COORDINATOR-1"])

    def test_same_principal_without_role_transition_is_rejected(self):
        bundle = make_native_bundle(collapse=True)
        bundle["native_support"]["role_transitions"] = []
        with self.assertRaisesRegex(native.NativeValidationError, "lacks durable ROLE_TRANSITION"):
            native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")

    def test_same_principal_without_role_execution_grant_is_rejected(self):
        bundle = make_native_bundle(collapse=True)
        bundle["native_support"]["authority_grants"] = []
        bundle["tasks"][0]["control_plane"]["authority_grant_refs"] = []
        with self.assertRaisesRegex(native.NativeValidationError, "ROLE_EXECUTION"):
            native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")

    def test_same_principal_fresh_replay_must_come_from_new_stage(self):
        bundle = make_native_bundle(collapse=True)
        transition = bundle["native_support"]["role_transitions"][0]
        reviewer = next(stage for stage in bundle["stages"] if stage["task_id"] == PRD and stage["stage"] == "REVIEWER")
        transition["fresh_replay_evidence_refs"] = [reviewer["evidence_refs"][0]]
        with self.assertRaisesRegex(native.NativeValidationError, "not from the new role attempt"):
            native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")

    def test_release_blocked_native_responsibility_cannot_validate_as_ready(self):
        bundle = make_native_bundle()
        bundle["tasks"][0]["control_plane"]["responsibility_registry"][0]["release_state"] = "BLOCKED_DEPENDENCY"
        with self.assertRaisesRegex(native.NativeValidationError, "not released"):
            native.validate_native_bundle(bundle, "2026-10-04T00:08:00Z")


if __name__ == "__main__":
    unittest.main()
