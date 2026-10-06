import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from provider_state import (
    canonical_provider_key,
    derive_provider_action,
    validate_current_state,
    validate_provider_mutation,
)


DIGEST = "d" * 64
SHA = "a" * 40


def identity():
    value = {
        "programme_or_parent_id": "COMMON-PROD-CONTROL-V1",
        "prd_id": "PRD-527-P1-R3",
        "resource_kind": "ISSUE",
        "mutation_slot": "MATERIAL_RESPONSIBILITY",
        "canonical_key": "",
    }
    value["canonical_key"] = canonical_provider_key(value)
    return value


def mutation():
    ident = identity()
    value = {
        "schema_version": "PROVIDER_MUTATION_V1",
        "authority": "PROVIDER_MUTATION_TRANSACTION",
        "identity": ident,
        "mutation": {
            "class": "CREATE_ONCE",
            "operation": "CREATE_ISSUE",
            "payload_digest": DIGEST,
            "attempted": False,
            "attempt_id": None,
            "provider_id": None,
        },
        "lookup": {
            "performed": False,
            "matches": [],
        },
        "readback": {
            "performed": False,
            "provider_id": None,
            "canonical_key": None,
            "payload_digest": None,
        },
        "next_action": {
            "type": "LOOKUP",
            "reason_code": "LOOKUP_REQUIRED",
        },
    }
    return value


def set_derived(value):
    value["next_action"] = derive_provider_action(value)
    return value


def current_state():
    return {
        "schema_version": "CURRENT_STATE_V1",
        "authority": "CURRENT_STATE_PROJECTION",
        "parent": {
            "programme_or_parent_id": "COMMON-PROD-CONTROL-V1",
            "parent_ref": "issue://527",
            "parent_contract_version": "rev-1",
            "main_sha": SHA,
        },
        "active": {
            "phase": "PHASE-1-CANONICAL-RUNTIME",
            "prd_id": "PRD-527-P1-R3",
            "issue_ref": "issue://545",
            "role": "SOLO_CODER",
            "attempt": 1,
        },
        "candidate": {
            "state": "NONE",
            "pr": None,
            "branch": None,
            "base_sha": None,
            "head_sha": None,
            "changed_files": [],
        },
        "frontiers": {
            "material": "CHILD_MATERIALIZED",
            "semantic": "PROVIDER_TRANSACTION_CONTRACT_FROZEN",
            "evidence": "CHILD_CONTRACT",
        },
        "dependencies": [],
        "open_critical_findings": [],
        "open_critical_unknowns": [],
        "stale_evidence": [],
        "production": {
            "mode": "OFF",
            "authority_ref": None,
        },
        "merge_authority": {
            "state": "NOT_GRANTED",
            "authority_ref": None,
        },
        "next_single_action": "IMPLEMENT_PROVIDER_STATE_RUNTIME",
        "forbidden_next_actions": [
            "PRODUCTION_MODE_TRANSITION",
            "AUTO_MERGE",
        ],
        "source_refs": ["issue://527", "issue://545", f"commit://{SHA}"],
    }


class ProviderMutationTests(unittest.TestCase):
    def test_canonical_key_is_stable_and_not_title_based(self):
        first = identity()
        second = copy.deepcopy(first)
        self.assertEqual(canonical_provider_key(first), canonical_provider_key(second))
        self.assertNotIn("title", first)

    def test_stored_canonical_key_must_match_machine_identity(self):
        value = mutation()
        value["identity"]["canonical_key"] = "pm:v1:" + "0" * 64
        errors = validate_provider_mutation(value)
        self.assertTrue(any("machine-derived provider key" in error for error in errors), errors)

    def test_first_action_is_lookup(self):
        value = mutation()
        self.assertEqual(derive_provider_action(value)["type"], "LOOKUP")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_zero_matches_create_once(self):
        value = mutation()
        value["lookup"]["performed"] = True
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "CREATE_ONCE")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_retry_after_attempt_never_creates_again(self):
        value = mutation()
        value["lookup"]["performed"] = True
        value["mutation"].update({
            "attempted": True,
            "attempt_id": "provider-request://1",
            "provider_id": None,
        })
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "READBACK_AFTER_MUTATION")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_one_existing_match_reuses_and_reads_back(self):
        value = mutation()
        value["lookup"] = {
            "performed": True,
            "matches": [{
                "provider_id": "issue://545",
                "canonical_key": value["identity"]["canonical_key"],
            }],
        }
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "READBACK_EXISTING")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_multiple_matches_fail_closed(self):
        value = mutation()
        key = value["identity"]["canonical_key"]
        value["lookup"] = {
            "performed": True,
            "matches": [
                {"provider_id": "issue://1", "canonical_key": key},
                {"provider_id": "issue://2", "canonical_key": key},
            ],
        }
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "RECONCILE_DUPLICATES")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_mutate_existing_requires_target(self):
        value = mutation()
        value["mutation"]["class"] = "MUTATE_EXISTING_ONCE"
        value["mutation"]["operation"] = "UPDATE_ISSUE"
        value["lookup"]["performed"] = True
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "RECONCILE_MISSING_TARGET")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_mutate_existing_one_match_allows_one_mutation(self):
        value = mutation()
        value["mutation"]["class"] = "MUTATE_EXISTING_ONCE"
        value["mutation"]["operation"] = "UPDATE_ISSUE"
        value["lookup"] = {
            "performed": True,
            "matches": [{
                "provider_id": "issue://545",
                "canonical_key": value["identity"]["canonical_key"],
            }],
        }
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "MUTATE_ONCE")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_matching_readback_completes(self):
        value = mutation()
        key = value["identity"]["canonical_key"]
        value["lookup"] = {
            "performed": True,
            "matches": [{"provider_id": "issue://545", "canonical_key": key}],
        }
        value["readback"] = {
            "performed": True,
            "provider_id": "issue://545",
            "canonical_key": key,
            "payload_digest": DIGEST,
        }
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "COMPLETE")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_mismatched_readback_reconciles(self):
        value = mutation()
        key = value["identity"]["canonical_key"]
        value["lookup"] = {
            "performed": True,
            "matches": [{"provider_id": "issue://545", "canonical_key": key}],
        }
        value["readback"] = {
            "performed": True,
            "provider_id": "issue://545",
            "canonical_key": key,
            "payload_digest": "e" * 64,
        }
        set_derived(value)
        self.assertEqual(value["next_action"]["type"], "RECONCILE_MISMATCH")
        self.assertEqual(validate_provider_mutation(value), [])

    def test_attempt_before_lookup_is_invalid(self):
        value = mutation()
        value["mutation"].update({
            "attempted": True,
            "attempt_id": "provider-request://1",
        })
        set_derived(value)
        errors = validate_provider_mutation(value)
        self.assertTrue(any("before lookup" in error for error in errors), errors)

    def test_title_cannot_be_added_as_identity(self):
        value = mutation()
        value["title"] = "looks like the same responsibility"
        errors = validate_provider_mutation(value)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors), errors)


class CurrentStateTests(unittest.TestCase):
    def test_minimal_projection_is_valid(self):
        self.assertEqual(validate_current_state(current_state()), [])

    def test_no_candidate_cannot_claim_candidate_fields(self):
        value = current_state()
        value["candidate"]["head_sha"] = SHA
        errors = validate_current_state(value)
        self.assertTrue(any("candidate NONE" in error for error in errors), errors)

    def test_active_candidate_requires_exact_branch_base_and_head(self):
        value = current_state()
        value["candidate"]["state"] = "ACTIVE"
        value["candidate"]["branch"] = "prod/example"
        value["candidate"]["base_sha"] = SHA
        value["candidate"]["head_sha"] = "b" * 40
        value["candidate"]["pr"] = 999
        self.assertEqual(validate_current_state(value), [])

    def test_off_mode_cannot_carry_active_authority_ref(self):
        value = current_state()
        value["production"]["authority_ref"] = "owner://old-cutover"
        errors = validate_current_state(value)
        self.assertTrue(any("OFF cannot carry" in error for error in errors), errors)

    def test_non_off_mode_requires_authority_ref(self):
        value = current_state()
        value["production"]["mode"] = "SHADOW_ONLY"
        errors = validate_current_state(value)
        self.assertTrue(any("requires authority_ref" in error for error in errors), errors)

    def test_merge_grant_requires_authority_ref(self):
        value = current_state()
        value["merge_authority"]["state"] = "OWNER_GRANTED"
        errors = validate_current_state(value)
        self.assertTrue(any("OWNER_GRANTED" in error for error in errors), errors)

    def test_verified_dependency_requires_exact_evidence(self):
        value = current_state()
        value["dependencies"] = [{
            "producer": "PRD-UPSTREAM",
            "required_state": "COMPLETE",
            "observed_state": "VERIFIED",
            "evidence_ref": None,
            "exact_result_ref": None,
        }]
        errors = validate_current_state(value)
        self.assertTrue(any("requires evidence_ref" in error for error in errors), errors)

    def test_next_action_cannot_also_be_forbidden(self):
        value = current_state()
        value["forbidden_next_actions"].append(value["next_single_action"])
        errors = validate_current_state(value)
        self.assertTrue(any("cannot also be forbidden" in error for error in errors), errors)

    def test_projection_cannot_claim_extra_authority_field(self):
        value = current_state()
        value["merge_now"] = True
        errors = validate_current_state(value)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
