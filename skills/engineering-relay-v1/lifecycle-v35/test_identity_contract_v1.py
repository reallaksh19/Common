"""WP1/U1 source-identity contract tests, synthetic reference-only inputs."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("identity_contract_v1", HERE / "identity_contract_v1.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)
validate_identity = module.validate_identity
IdentityContractError = module.IdentityContractError

R = "reallaksh19/Common"
A, B, C = "a" * 40, "b" * 40, "c" * 40
H = "sha256:" + "d" * 64


def sample():
    return {
        "schema": "relay-lifecycle-source-identity-v1",
        "programme": {"id": "R14-WP1-READONLY", "repository": R, "root_issue": 787},
        "owner_source_grade": "GITHUB_VERBATIM_MIRROR",
        "graph_source": {"role": "PLAN_GRAPH_REVISION", "state": "REFERENCED", "repository": R,
                         "revision_sha": A, "path": "relay/graph.yaml", "content_sha256": H},
        "session_source": {"role": "SESSION_SOURCE_COMMIT", "state": "REFERENCED", "repository": R,
                           "commit_sha": B},
        "candidate_source": {"role": "CODE_CANDIDATE_HEAD", "state": "REFERENCED", "repository": R,
                             "pr_number": 884, "head_sha": C, "base_sha": A},
    }


class IdentityContractV1Tests(unittest.TestCase):
    def fail(self, value, substring):
        with self.assertRaises(IdentityContractError) as cm:
            validate_identity(value)
        self.assertIn(substring, str(cm.exception))

    def test_positive_three_typed_refs_no_authorization(self):
        got = validate_identity(sample())
        self.assertEqual("CALLER_REFERENCED_UNATTESTED", got["identity_grade"])
        self.assertTrue(got["identity_sha256"].startswith("sha256:"))
        self.assertEqual("sha256:3fc1962e7d8da436be7301f154a4b9614b5d5b0f5a5fc3b894e574fae6d5f828", got["identity_sha256"])
        self.assertEqual("NOT_GRANTED", got["writer_authorization"])
        self.assertEqual("NOT_EVALUATED", got["evidence_acceptance"])

    def test_distinct_roles_may_have_same_sha_without_collapsing_roles(self):
        val = sample()
        val["session_source"]["commit_sha"] = A
        val["candidate_source"]["head_sha"] = A
        self.assertEqual("CALLER_REFERENCED_UNATTESTED", validate_identity(val)["identity_grade"])

    def test_unknown_predecessor_and_candidate_are_not_zero_or_verified(self):
        val = sample()
        val["session_source"].update(state="UNKNOWN", commit_sha=None)
        val["candidate_source"].update(state="UNKNOWN", pr_number=None, head_sha=None, base_sha=None)
        val["owner_source_grade"] = "UNKNOWN"
        self.assertEqual("NOT_GRANTED", validate_identity(val)["owner_authorization"])

    def test_negative_swapped_role(self):
        val = sample(); val["graph_source"]["role"] = "CODE_CANDIDATE_HEAD"
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_forged_positive_source(self):
        val = sample(); val["owner_source_grade"] = "AUTHENTICATED_ORIGINAL_CHAT"
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_extra_writer_grant_field(self):
        val = sample(); val["writer_authorization"] = "GRANTED"
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_foreign_graph(self):
        val = sample(); val["graph_source"]["repository"] = "another/repo"
        self.fail(val, "CROSS_REPOSITORY_REFERENCE:graph_source")

    def test_negative_foreign_candidate(self):
        val = sample(); val["candidate_source"]["repository"] = "another/repo"
        self.fail(val, "CROSS_REPOSITORY_REFERENCE:candidate_source")

    def test_negative_candidate_head_not_hex(self):
        val = sample(); val["candidate_source"]["head_sha"] = "bad"
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_unknown_session_with_durable_commit_claim(self):
        val = sample(); val["session_source"]["state"] = "UNKNOWN"
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_partial_candidate_reference(self):
        val = sample(); val["candidate_source"]["base_sha"] = None
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_graph_content_sha_invalid(self):
        val = sample(); val["graph_source"]["content_sha256"] = "d" * 64
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_unsafe_graph_parent_path(self):
        val = sample(); val["graph_source"]["path"] = "relay/../graph.yaml"
        self.fail(val, "UNSAFE_GRAPH_PATH")

    def test_negative_unsafe_graph_windows_path(self):
        val = sample(); val["graph_source"]["path"] = "relay\\graph.yaml"
        self.fail(val, "SCHEMA_INVALID")

    def test_negative_unsafe_graph_double_slash(self):
        val = sample(); val["graph_source"]["path"] = "relay//graph.yaml"
        self.fail(val, "UNSAFE_GRAPH_PATH")

    def test_negative_unsafe_graph_control_char(self):
        val = sample(); val["graph_source"]["path"] = "relay/x\ngraph.yaml"
        self.fail(val, "UNSAFE_GRAPH_PATH")

    def test_mutated_candidate_or_graph_invalidates_identity_digest(self):
        base = sample()
        old = validate_identity(base)["identity_sha256"]
        moved = copy.deepcopy(base); moved["candidate_source"]["head_sha"] = "e" * 40
        self.assertNotEqual(old, validate_identity(moved)["identity_sha256"])
        moved = copy.deepcopy(base); moved["graph_source"]["revision_sha"] = "f" * 40
        self.assertNotEqual(old, validate_identity(moved)["identity_sha256"])

    def test_deterministic_key_order(self):
        base = sample()
        permuted = dict(reversed(list(base.items())))
        self.assertEqual(validate_identity(base)["identity_sha256"], validate_identity(permuted)["identity_sha256"])

    def test_fails_non_object(self):
        self.fail([], "IDENTITY_OBJECT_REQUIRED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
