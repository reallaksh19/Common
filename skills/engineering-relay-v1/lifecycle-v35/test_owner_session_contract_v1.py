"""U2 source-event/custody provenance falsifiers; synthetic, no GitHub writes."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owner_session_contract_v1", HERE / "owner_session_contract_v1.py")
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
validate = module.validate_owner_session
ContractError = module.OwnerSessionError
R = "reallaksh19/Common"
A, B, C = "a" * 40, "b" * 40, "c" * 40
D = "sha256:" + "d" * 64


def sample():
    return {
        "schema": "relay-lifecycle-owner-session-v1", "mode": "RESEARCH_ONLY",
        "identity": {
            "schema": "relay-lifecycle-source-identity-v1",
            "programme": {"id": "R14-WP1-RESEARCH", "repository": R, "root_issue": 787},
            "owner_source_grade": "GITHUB_VERBATIM_MIRROR",
            "graph_source": {"role": "PLAN_GRAPH_REVISION", "state": "REFERENCED", "repository": R,
                             "revision_sha": A, "path": "relay/graph.yaml", "content_sha256": D},
            "session_source": {"role": "SESSION_SOURCE_COMMIT", "state": "REFERENCED", "repository": R, "commit_sha": B},
            "candidate_source": {"role": "CODE_CANDIDATE_HEAD", "state": "REFERENCED", "repository": R,
                                 "pr_number": 891, "head_sha": C, "base_sha": A},
        },
        "owner_events": [
            {"id": "O001", "kind": "REQUIREMENT_MIRROR", "source_grade": "GITHUB_VERBATIM_MIRROR",
             "source_url": "https://github.com/reallaksh19/Common/issues/787#issuecomment-100",
             "content_sha256": D, "predecessor_id": None},
            {"id": "O002", "kind": "AMENDMENT_MIRROR", "source_grade": "GITHUB_VERBATIM_MIRROR",
             "source_url": "https://github.com/reallaksh19/Common/issues/878#issuecomment-200",
             "content_sha256": D, "predecessor_id": "O001"},
        ],
        "session_events": [
            {"id": "S001", "session_id": "AGENT_A_SESSION", "actor_label": "Agent A (unverified)",
             "kind": "START_CLAIMED", "owner_event_id": "O001", "source_commit": A,
             "predecessor_id": None},
            {"id": "S002", "session_id": "AGENT_A_SESSION", "actor_label": "Agent A (unverified)",
             "kind": "HANDOVER_OFFERED", "owner_event_id": "O002", "source_commit": B,
             "predecessor_id": "S001"},
        ],
    }


class OwnerSessionContractTests(unittest.TestCase):
    def error(self, payload, part):
        with self.assertRaises(ContractError) as ctx:
            validate(payload)
        self.assertIn(part, str(ctx.exception))

    def test_positive_ordered_mirror_and_source_fingerprint(self):
        out = validate(sample())
        self.assertEqual("NOT_PROVEN", out["exclusive_execution_lease"])
        self.assertEqual("NOT_GRANTED", out["writer_authorization"])
        self.assertEqual("NOT_CALCULATED", out["programme_projection"])
        self.assertEqual(2, out["owner_event_count"])
        self.assertEqual(2, out["session_event_count"])
        self.assertEqual(1, out["claimed_active_session_count"])
        self.assertTrue(out["history_sha256"].startswith("sha256:"))

    def test_unknown_owner_and_session_does_not_imply_origin_or_lease(self):
        x = sample()
        x["identity"]["owner_source_grade"] = "UNKNOWN"
        x["identity"]["session_source"].update(state="UNKNOWN", commit_sha=None)
        for e in x["owner_events"]:
            e.update(source_grade="UNKNOWN", source_url=None, content_sha256=None)
        x["session_events"][-1]["source_commit"] = None
        out = validate(x)
        self.assertEqual("NOT_AUTHENTICATED", out["owner_authenticity"])
        self.assertEqual("NOT_PROVEN", out["exclusive_execution_lease"])

    def test_digest_order_insensitive_but_event_order_sensitive(self):
        x = sample(); h = validate(x)["history_sha256"]
        self.assertEqual(h, validate(dict(reversed(list(x.items()))))["history_sha256"])
        x["owner_events"][1]["content_sha256"] = "sha256:" + "e"*64
        self.assertNotEqual(h, validate(x)["history_sha256"])

    def test_new_owner_amendment_invalidates_digest(self):
        x = sample(); h = validate(x)["history_sha256"]
        x["owner_events"].append({"id":"O003","kind":"DECISION_CLAIM","source_grade":"UNKNOWN",
                                  "source_url":None,"content_sha256":None,"predecessor_id":"O002"})
        self.assertNotEqual(h, validate(x)["history_sha256"])

    def test_derived_custody_claims_never_grant_lease_even_after_stop(self):
        x = sample(); x["session_events"].append({"id":"S003","session_id":"AGENT_A_SESSION",
          "actor_label":"Agent A (unverified)","kind":"STOP_CLAIMED","owner_event_id":"O002",
          "source_commit":B,"predecessor_id":"S002"})
        out=validate(x)
        self.assertEqual(0,out["claimed_active_session_count"])
        self.assertEqual("NOT_PROVEN",out["exclusive_execution_lease"])
        self.assertEqual("HOLD_NOT_PROVEN",out["handover_admission"])

    def test_concurrent_active_claims_are_exposed_not_promoted(self):
        x=sample(); x["session_events"].append({"id":"S003","session_id":"AGENT_B_SESSION",
          "actor_label":"Agent B (unverified)","kind":"START_CLAIMED","owner_event_id":"O002",
          "source_commit":B,"predecessor_id":"S002"})
        out=validate(x)
        self.assertEqual("MULTIPLE_ACTIVE_CLAIMS",out["custody_conflict"])
        self.assertEqual("NOT_PROVEN",out["exclusive_execution_lease"])

    def test_runner_prepared_not_a_new_active_writer(self):
        x=sample(); x["session_events"].append({"id":"S003","session_id":"RUNNER_B_SESSION",
          "actor_label":"Runner B","kind":"RUNNER_PREPARED","owner_event_id":"O002",
          "source_commit":B,"predecessor_id":"S002"})
        self.assertEqual(1,validate(x)["claimed_active_session_count"])

    def test_no_fake_writer_field(self):
        x=sample(); x["authorization_granted"]=True
        self.error(x,"SCHEMA_INVALID")

    def test_no_false_original_chat_grade(self):
        x=sample(); x["owner_events"][0]["source_grade"]="AUTHENTICATED_ORIGINAL"
        self.error(x,"SCHEMA_INVALID")

    def test_no_cross_repository_owner_url(self):
        x=sample(); x["owner_events"][0]["source_url"]="https://github.com/other/Repo/issues/787#issuecomment-1"
        self.error(x,"GITHUB_MIRROR_LOCATOR_UNTRUSTED")

    def test_no_untrusted_github_domain(self):
        x=sample(); x["owner_events"][0]["source_url"]="https://github.com.evil.example/reallaksh19/Common/issues/787#issuecomment-1"
        self.error(x,"GITHUB_MIRROR_LOCATOR_UNTRUSTED")

    def test_no_fake_commentless_source(self):
        x=sample(); x["owner_events"][0]["source_url"]="https://github.com/reallaksh19/Common/issues/787"
        self.error(x,"GITHUB_MIRROR_LOCATOR_UNTRUSTED")

    def test_no_percent_encoded_alias(self):
        x=sample(); x["owner_events"][0]["source_url"]="https://github.com/reallaksh19/Common/%69ssues/787#issuecomment-1"
        self.error(x,"GITHUB_MIRROR_LOCATOR_UNTRUSTED")

    def test_no_unknown_grade_with_mirrored_sha(self):
        x=sample(); x["owner_events"][1]["source_grade"]="UNKNOWN"
        self.error(x,"UNKNOWN_OWNER_SOURCE_HAS_MATERIAL")

    def test_no_grade_escalation(self):
        x=sample(); x["identity"]["owner_source_grade"]="UNKNOWN"
        self.error(x,"OWNER_GRADE_ESCALATION")

    def test_no_synthetic_mixing_into_real_mirror(self):
        x=sample(); x["owner_events"][1].update(source_grade="SYNTHETIC_LAB_ONLY",source_url=None)
        self.error(x,"MIXED_OWNER_SOURCE_CONTEXT")

    def test_no_duplicate_owner_id(self):
        x=sample(); x["owner_events"][1]["id"]="O001"
        self.error(x,"DUPLICATE_OWNER_EVENT_ID")

    def test_no_disconnected_owner_chain(self):
        x=sample(); x["owner_events"][1]["predecessor_id"]=None
        self.error(x,"BROKEN_OWNER_HISTORY")

    def test_no_second_initial_requirement(self):
        x=sample(); x["owner_events"][1]["kind"]="REQUIREMENT_MIRROR"
        self.error(x,"OWNER_REQUEST_ORDER_INVALID")

    def test_no_session_referencing_unknown_owner(self):
        x=sample(); x["session_events"][1]["owner_event_id"]="O999"
        self.error(x,"SESSION_UNKNOWN_OWNER_EVENT")

    def test_no_session_stop_without_start(self):
        x=sample(); x["session_events"][1].update(kind="STOP_CLAIMED",session_id="OTHER_SESSION")
        self.error(x,"SESSION_NO_LIVE_START")

    def test_no_duplicate_session_start(self):
        x=sample(); x["session_events"][1]["kind"]="START_CLAIMED"
        self.error(x,"SESSION_RESTART_AMBIGUOUS")

    def test_no_session_actor_alias_change(self):
        x=sample(); x["session_events"][1]["actor_label"]="Another actor"
        self.error(x,"SESSION_ACTOR_IDENTITY_CHANGED")

    def test_changed_session_event_commit_invalidates_history_digest(self):
        x=sample(); first=validate(x)["history_sha256"]
        x["session_events"][0]["source_commit"]="e"*40
        self.assertNotEqual(first,validate(x)["history_sha256"])

    def test_no_session_commit_mismatch(self):
        x=sample(); x["session_events"][-1]["source_commit"]="f"*40
        self.error(x,"SESSION_COMMIT_IDENTITY_MISMATCH")

    def test_no_graph_reference_grade_bypass(self):
        x=sample(); x["identity"]["graph_source"]["repository"]="some/other"
        self.error(x,"U1_IDENTITY_INVALID")

    def test_no_session_event_forged_grant(self):
        x=sample(); x["session_events"][0]["writer_lease"]=True
        self.error(x,"SCHEMA_INVALID")

    def test_no_history_duplicate_session_event(self):
        x=sample(); x["session_events"][1]["id"]="S001"
        self.error(x,"DUPLICATE_SESSION_EVENT_ID")

    def test_not_an_authentication_service(self):
        x=sample(); out=validate(x)
        self.assertEqual("NOT_EVALUATED",out["source_receipt_authenticity"])
        self.assertEqual("UNVERIFIED_ACTOR_ASSERTIONS",out["session_claims"])

if __name__=="__main__": unittest.main(verbosity=2)
