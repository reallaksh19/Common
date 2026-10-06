import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from review_basis import review_basis_errors


CANDIDATE = "c" * 40
BASE = "a" * 40
DIGEST = "d" * 64


def criterion(result="PASS"):
    item = {"applicability": "REQUIRED", "result": result}
    if result == "PASS":
        item["evidence_refs"] = ["evidence://review"]
    return item


def profile(role="SELF_REVIEW", independence="NONE", author="agent://1", reviewer="agent://1"):
    return {
        "review_profile": {
            "common_protocol": {
                "ref": "repo://common-reviewer@exact",
                "version": "1.0",
                "digest": DIGEST,
            },
            "project_protocol": {
                "ref": "issue://project-review",
                "digest": DIGEST,
            },
            "role": role,
            "author_principal": author,
            "review_principal": reviewer,
            "principal_independence": independence,
            "context_reset": "FRESH_REVIEW_ATTEMPT",
            "common_criteria": {
                f"CR-{index:02d}": criterion()
                for index in range(1, 11)
            },
            "project_method_ids": ["PROJECT-METHOD-1"],
            "unresolved_required_findings": 0,
            "final_candidate": CANDIDATE,
            "result": "COMPLETE",
        }
    }


def self_context():
    return {
        "schema_version": "SELF_CHECK_CONTEXT_V1",
        "authority": "SOLO_SELF_CHECK_CONTEXT",
        "candidate_sha": CANDIDATE,
        "manifest_ref": "manifest://1",
        "manifest_digest": DIGEST,
        "principal": {
            "kind": "SOLO_PRINCIPAL",
            "identity": "agent://1",
            "principal_independence": "NONE",
            "fresh_reconstruction": True,
            "blindness_claim": "NONE",
        },
        "reconstruction_policy": {
            "original_task_ref": "issue://537",
            "base_sha": BASE,
            "candidate_sha": CANDIDATE,
            "repository_context_refs": ["repo://base", "repo://candidate"],
            "expectation_manifest_frozen": True,
            "author_reasoning_used_as_evidence": False,
            "coder_confidence_used_as_evidence": False,
            "prior_self_check_used_as_evidence": False,
            "outcome_falsification_required": True,
        },
        "tool_access": ["repository", "tests"],
    }


def review_context(kind="SAME_PRINCIPAL_FRESH_CONTEXT", independence="DEGRADED", identity="agent://1"):
    return {
        "schema_version": "REVIEW_CONTEXT_V1",
        "authority": "FRESH_REVIEW_CONTEXT",
        "candidate_sha": CANDIDATE,
        "manifest_ref": "manifest://1",
        "manifest_digest": DIGEST,
        "reviewer": {
            "kind": kind,
            "identity": identity,
            "principal_independence": independence,
            "fresh_context": True,
        },
        "context_policy": {
            "original_task_ref": "issue://537",
            "base_sha": BASE,
            "candidate_sha": CANDIDATE,
            "repository_context_refs": ["repo://base", "repo://candidate"],
            "candidate_visible_in_phase_a": False,
            "generated_tests_visible_in_phase_a": False,
            "coder_reasoning_included": False,
            "coder_confidence_included": False,
            "prior_self_review_included": False,
            "implementation_rationale_included": False,
            "candidate_visible_in_phase_b": True,
        },
        "tool_access": ["repository", "tests"],
    }


class ReviewBasisTests(unittest.TestCase):
    def test_solo_self_review_basis_is_valid(self):
        self.assertEqual(review_basis_errors(profile(), self_context()), [])

    def test_self_review_requires_self_check_context(self):
        errors = review_basis_errors(profile(), review_context())
        self.assertTrue(any("SELF_CHECK_CONTEXT_V1" in error for error in errors), errors)

    def test_self_review_cannot_claim_degraded_independence(self):
        value = profile(independence="DEGRADED")
        errors = review_basis_errors(value, self_context())
        self.assertTrue(errors)

    def test_self_check_rejects_author_reasoning_as_evidence(self):
        ctx = self_context()
        ctx["reconstruction_policy"]["author_reasoning_used_as_evidence"] = True
        errors = review_basis_errors(profile(), ctx)
        self.assertTrue(
            any(
                "author_reasoning_used_as_evidence" in error
                or "author reasoning" in error
                for error in errors
            ),
            errors,
        )

    def test_same_principal_reviewer_must_be_degraded(self):
        value = profile(role="REVIEWER", independence="DEGRADED")
        self.assertEqual(review_basis_errors(value, review_context()), [])

    def test_distinct_reviewer_requires_distinct_identity(self):
        value = profile(
            role="REVIEWER",
            independence="DISTINCT_PRINCIPAL",
            reviewer="agent://2",
        )
        ctx = review_context(
            kind="DISTINCT_PRINCIPAL",
            independence="DISTINCT",
            identity="agent://2",
        )
        self.assertEqual(review_basis_errors(value, ctx), [])

    def test_distinct_claim_with_same_identity_is_rejected(self):
        value = profile(role="REVIEWER", independence="DISTINCT_PRINCIPAL")
        errors = review_basis_errors(value, review_context(
            kind="DISTINCT_PRINCIPAL",
            independence="DISTINCT",
        ))
        self.assertTrue(any("distinct principal identities" in error for error in errors), errors)

    def test_required_pass_needs_evidence(self):
        value = profile()
        value["review_profile"]["common_criteria"]["CR-05"].pop("evidence_refs")
        errors = review_basis_errors(value, self_context())
        self.assertTrue(any("CR-05: PASS requires" in error for error in errors), errors)

    def test_not_applicable_needs_basis(self):
        value = profile()
        value["review_profile"]["common_criteria"]["CR-07"] = {
            "applicability": "NOT_APPLICABLE",
            "result": "NOT_APPLICABLE",
        }
        errors = review_basis_errors(value, self_context())
        self.assertTrue(any("applicability_basis" in error for error in errors), errors)

    def test_complete_cannot_hide_not_run_required_criterion(self):
        value = profile()
        value["review_profile"]["common_criteria"]["CR-08"] = criterion("NOT_RUN")
        errors = review_basis_errors(value, self_context())
        self.assertTrue(any("COMPLETE review requires PASS" in error for error in errors), errors)

    def test_candidate_mismatch_is_rejected(self):
        ctx = self_context()
        ctx["candidate_sha"] = "e" * 40
        ctx["reconstruction_policy"]["candidate_sha"] = "e" * 40
        errors = review_basis_errors(profile(), ctx)
        self.assertTrue(any("profile final_candidate" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
