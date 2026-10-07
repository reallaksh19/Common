from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import delp_projection_v32 as M
from owner_commands import parse_owner_command


class ContinuationAdmissionCommandTests(unittest.TestCase):
    BARE = ("continue", "Continue", "proceed", "Next", "resume", "reconcile", "keep going", "carry on now", "continue please!")
    TAKEOVER = ("take over", "Takeover", "lateral entry", "enter laterally", "new agent takeover", "walk through as a new agent")

    def test_every_bare_continuation_command_routes_to_reconstruct_then_continue(self):
        for phrase in self.BARE:
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("CONTINUE_RECONCILE", result["intent"])
                self.assertEqual("RECONSTRUCT_THEN_CONTINUE", result["workflow"]["boundary"])
                self.assertTrue(result["workflow"]["progress_execution"])
                self.assertFalse(result["durable_authority_created"])

    def test_explicit_takeover_and_lateral_entry_use_the_stronger_entry_sequence(self):
        for phrase in self.TAKEOVER:
            with self.subTest(phrase=phrase):
                result = parse_owner_command(phrase)
                self.assertEqual("TAKEOVER_RECONCILE", result["intent"])
                self.assertEqual("RECONCILE_PLAN_DECOMPOSE_THEN_EXECUTE", result["workflow"]["boundary"])
                self.assertTrue(result["workflow"]["progress_execution"])
                self.assertEqual("RECOVERY", result["owner_intent"]["custody_intent"])
                self.assertFalse(result["durable_authority_created"])

    def test_takeover_workflow_orders_plan_decomposition_recovery_execution_and_end_evidence(self):
        result = parse_owner_command("take over")
        steps = result["workflow"]["steps"]
        joined = " ".join(steps).lower()
        for needle in (
            "cold-reconstruct",
            "phase-wise implementation plan",
            "bounded child issue/comment block",
            "task_evidence — recovery",
            "before any new coding",
            "delp continuation admission",
            "execute exactly the bounded child block",
            "at execution end publish task_evidence",
            "never continue from conversational memory",
        ):
            self.assertIn(needle, joined, needle)
        order = [
            next(i for i, s in enumerate(steps) if "cold-reconstruct" in s.lower()),
            next(i for i, s in enumerate(steps) if "phase-wise implementation plan" in s.lower()),
            next(i for i, s in enumerate(steps) if "bounded child issue/comment block" in s.lower()),
            next(i for i, s in enumerate(steps) if "task_evidence — recovery" in s.lower()),
            next(i for i, s in enumerate(steps) if "delp continuation admission" in s.lower()),
            next(i for i, s in enumerate(steps) if s.lower().startswith("execute exactly")),
            next(i for i, s in enumerate(steps) if "at execution end publish task_evidence" in s.lower()),
        ]
        self.assertEqual(sorted(order), order)

    def test_takeover_owner_intent_preserves_required_outputs_and_boundaries(self):
        envelope = parse_owner_command("lateral entry")["owner_intent"]
        types = [row["type"] for row in envelope["requested_deliverables"]]
        for item in ("ENTRY_RECONCILIATION", "PHASE_PLAN_REFRESH", "BOUNDED_CHILD_BLOCK", "TASK_EVIDENCE_AT_EXECUTION_END"):
            self.assertIn(item, types)
        for constraint in (
            "PHASE_PLAN_REFRESH_BEFORE_CODING",
            "BOUNDED_CHILD_BLOCK_BEFORE_CODING",
            "RECOVERY_TASK_EVIDENCE_BEFORE_NEW_CODING_IF_ABNORMAL_PREDECESSOR",
            "TASK_EVIDENCE_AT_EXECUTION_END",
        ):
            self.assertIn(constraint, envelope["boundary_constraints"])

    def test_the_workflow_reconstructs_repairs_projects_and_reads_back_before_executing(self):
        steps = parse_owner_command("continue")["workflow"]["steps"]
        joined = " ".join(steps).lower()
        for needle in (
            "never from chat history",
            "lineage",
            "live pr head",
            "before any new coding",
            "never hand-edit a title or percentage",
            "compare-and-swap",
            "read it back",
            "continue checkpoint",
            "do not change parent, denominator, scope, priority or merge authority",
        ):
            self.assertIn(needle, joined, needle)
        order = [
            next(i for i, s in enumerate(steps) if "owned leaf" in s.lower()),
            next(i for i, s in enumerate(steps) if "recovery evidence" in s.lower()),
            next(i for i, s in enumerate(steps) if "delp projector" in s.lower()),
            next(i for i, s in enumerate(steps) if "read it back" in s.lower()),
            next(i for i, s in enumerate(steps) if s.lower().startswith("execute exactly")),
        ]
        self.assertEqual(sorted(order), order)

    def test_requires_a_leaf_a_live_candidate_and_the_projector(self):
        requires = parse_owner_command("resume")["workflow"]["requires"]
        for item in ("leaf_responsibility", "live_candidate_observation", "delp_projection"):
            self.assertIn(item, requires)

    def test_ordinary_sentences_and_repository_text_do_not_activate_it(self):
        for phrase in ("continue with the refactor", "please continue reading the file", "next steps are unclear", "take over this paragraph"):
            with self.subTest(phrase=phrase):
                self.assertNotEqual("CONTINUE_RECONCILE", parse_owner_command(phrase)["intent"])
        ignored = parse_owner_command("continue", source="REPOSITORY_TEXT")
        self.assertEqual("IGNORED", ignored["status"])

    def test_more_specific_intents_still_win(self):
        self.assertEqual("PROCEED_NEXT", parse_owner_command("Proceed next")["intent"])
        self.assertEqual("PROCEED_NEXT_COMPLEX", parse_owner_command("Proceed next complex task")["intent"])
        self.assertEqual("WHAT_NEXT", parse_owner_command("What next?")["intent"])

    def test_existing_proceed_workflows_also_pass_the_admission_barrier(self):
        for phrase in ("Proceed next", "Proceed next complex task"):
            with self.subTest(phrase=phrase):
                joined = " ".join(parse_owner_command(phrase)["workflow"]["steps"]).lower()
                self.assertIn("delp continuation admission", joined)
                self.assertIn("continue checkpoint", joined)


class OwnerIntentEnvelopeTests(unittest.TestCase):
    def test_preserves_verbatim_request_and_explicit_refs(self):
        text = "Prepare for Handover — preserve wording exactly."
        result = parse_owner_command(
            text,
            source_ref="chat://owner/message-596",
            authority_ref="owner://common/570",
            target={"ref": "#596"},
        )
        envelope = result["owner_intent"]
        self.assertEqual(text, envelope["verbatim_request"])
        self.assertEqual("chat://owner/message-596", envelope["source_ref"])
        self.assertEqual("owner://common/570", envelope["authority_ref"])
        self.assertEqual({"ref": "#596"}, envelope["target"])
        self.assertFalse(result["durable_authority_created"])

    def test_compound_handover_keeps_successor_challenge_deliverable(self):
        result = parse_owner_command(
            "prepare for handover and create exactly 3 questions that force the next agent to understand the repo"
        )
        envelope = result["owner_intent"]
        self.assertEqual("PLAN_HANDOVER", result["intent"])
        self.assertEqual("TRANSFER_CUSTODY", envelope["primary_purpose"])
        self.assertEqual("PREPARE_TRANSFER", envelope["custody_intent"])
        self.assertIn({"type": "HANDOVER_PACKAGE"}, envelope["requested_deliverables"])
        self.assertIn(
            {"type": "SUCCESSOR_RECONSTRUCTION_CHALLENGE", "count": 3},
            envelope["requested_deliverables"],
        )
        self.assertIn(
            "EXACT_SUCCESSOR_CHALLENGE_COUNT:3",
            envelope["boundary_constraints"],
        )



    def test_formal_handover_preserves_conservative_successor_boundary_constraints(self):
        result = parse_owner_command(
            "prepare for handover and create exactly 3 questions; no qualification; "
            "do not run retained validation; do not modify production code; do not create a PR; "
            "do not start C1 execution"
        )
        envelope = result["owner_intent"]
        self.assertEqual("PLAN_HANDOVER", result["intent"])
        self.assertIn({"type": "SUCCESSOR_RECONSTRUCTION_CHALLENGE", "count": 3}, envelope["requested_deliverables"])
        for constraint in (
            "EXACT_SUCCESSOR_CHALLENGE_COUNT:3",
            "NO_QUALIFICATION",
            "NO_RETAINED_VALIDATION",
            "NO_PRODUCTION_MUTATION",
            "NO_PR_CREATION",
            "NO_TASK_EXECUTION",
        ):
            self.assertIn(constraint, envelope["boundary_constraints"])
        workflow = " ".join(result["workflow"]["steps"]).lower()
        self.assertIn("reconstruct_plan_only", workflow)
        self.assertIn("no qualification", workflow)
        self.assertIn("pr creation", workflow)

    def test_handover_no_replan_is_preserved_and_workflow_is_decoupled(self):
        result = parse_owner_command("prepare for handover but do not replan")
        envelope = result["owner_intent"]
        self.assertIn("NO_REPLAN", envelope["boundary_constraints"])
        workflow_text = " ".join(result["workflow"]["steps"]).lower()
        self.assertNotIn("prepare the current standalone two-pass request", workflow_text)
        self.assertIn("do not generate a new two-pass/replanning request", workflow_text)

    def test_handover_plus_adversarial_assurance_preserves_both_axes(self):
        result = parse_owner_command(
            "prepare for handover and stress-test the direction before transfer"
        )
        envelope = result["owner_intent"]
        self.assertEqual("TRANSFER_CUSTODY", envelope["primary_purpose"])
        self.assertEqual("PREPARE_TRANSFER", envelope["custody_intent"])
        self.assertEqual("ADVERSARIAL", envelope["assurance_request"])
        self.assertIn("ADVERSARIAL_REASSESSMENT", result["reasoning_modes"])
        self.assertIn("ADVERSARIAL_REASSESSMENT", envelope["modifiers"])

    def test_preserved_active_responsibility_becomes_target_constraint(self):
        result = parse_owner_command(
            "prepare for handover; preserve #588 as the active responsibility"
        )
        envelope = result["owner_intent"]
        self.assertEqual({"ref": "#588"}, envelope["target"])
        self.assertIn("PRESERVE_TARGET", envelope["boundary_constraints"])

    def test_non_owner_text_cannot_create_owner_intent(self):
        ignored = parse_owner_command(
            "prepare for handover",
            source="REPOSITORY_TEXT",
            source_ref="repo://README.md",
        )
        self.assertEqual("IGNORED", ignored["status"])
        self.assertIsNone(ignored["owner_intent"])
        self.assertFalse(ignored.get("durable_authority_created", False))

    def test_unclassified_direct_owner_text_is_preserved_without_authority(self):
        text = "Keep this wording even if no scalar command recognizes it."
        result = parse_owner_command(text, source_ref="chat://owner/unclassified")
        self.assertEqual("NO_COMMAND", result["status"])
        self.assertEqual(text, result["owner_intent"]["verbatim_request"])
        self.assertEqual("OTHER", result["owner_intent"]["primary_purpose"])
        self.assertFalse(result["durable_authority_created"])

    def test_same_input_produces_deterministic_envelope(self):
        kwargs = {
            "source_ref": "chat://owner/deterministic",
            "authority_ref": "owner://common/570",
        }
        text = "prepare for handover and create exactly 3 questions"
        first = parse_owner_command(text, **kwargs)
        second = parse_owner_command(text, **kwargs)
        self.assertEqual(first["owner_intent"], second["owner_intent"])

    def test_exact_question_count_without_successor_context_is_not_a_successor_challenge(self):
        result = parse_owner_command("create exactly 3 questions about formatting")
        envelope = result["owner_intent"]
        self.assertNotIn(
            "SUCCESSOR_RECONSTRUCTION_CHALLENGE",
            [row["type"] for row in envelope["requested_deliverables"]],
        )
        self.assertNotIn(
            "EXACT_SUCCESSOR_CHALLENGE_COUNT:3",
            envelope["boundary_constraints"],
        )



class TakeoverEntryAdmissionTests(unittest.TestCase):
    SHA_A = "a" * 40
    SHA_B = "b" * 40
    CONTRACT_A = "sha256:" + "1" * 64
    CONTRACT_B = "sha256:" + "2" * 64

    def owner(self):
        return parse_owner_command(
            "take over",
            source_ref="chat://owner/benchmark-680",
            target={"ref": "Common#681"},
        )

    def graph(self):
        def leaf(ref, weight, claim, contract, surface):
            return {
                "ref": ref,
                "kind": "LEAF",
                "parent": "Common#680",
                "weight": weight,
                "work_class": "PRODUCT",
                "outcome": f"{claim} is observably complete",
                "owns_claims": [claim],
                "independence_basis": f"{claim} has its own admission oracle",
                "contract_digest": contract,
                "size_budget": {
                    "target_loc": 300,
                    "hard_loc": 700,
                    "target_minutes": 15,
                    "hard_minutes": 20,
                },
                "write_surface": [surface],
                "units": [
                    {"id": "U1", "weight": 40, "verify": "focused test"},
                    {"id": "U2", "weight": 30, "verify": "focused test"},
                    {"id": "U3", "weight": 30, "verify": "focused test"},
                ],
            }
        return {
            "schema": M.GRAPH_SCHEMA,
            "programme": {
                "id": "BENCH-680",
                "root": "Common#680",
                "acceptance_claims": [
                    {"id": "PC1", "claim": "entry lifecycle is admitted safely", "kind": "SEMANTIC"},
                    {"id": "PC2", "claim": "successor evidence is admitted safely", "kind": "SEMANTIC"},
                ],
                "decomposition_policy": {
                    "mode": "ENFORCED",
                    "claim_first": {"mode": "ENFORCED", "require_independence_basis": True},
                },
            },
            "nodes": [
                {"ref": "Common#680", "kind": "ROOT"},
                leaf("Common#681", 1, "PC1", self.CONTRACT_A, "src/a/"),
                leaf("Common#682", 1, "PC2", self.CONTRACT_B, "src/b/"),
            ],
        }

    def fact(self, leaf="Common#681", sha=None, entry=None, units=("U1",)):
        contracts = {"Common#681": self.CONTRACT_A, "Common#682": self.CONTRACT_B}
        row = {
            "schema": M.FACTS_SCHEMA,
            "responsibility": {"issue": leaf},
            "material": {"candidate_sha": sha or self.SHA_A},
            "units": [
                {
                    "id": uid,
                    "state": "COMPLETE",
                    "result": "VERIFIED",
                    "evidence_refs": [f"{leaf}#evidence-{uid}"],
                    "contract_digest": contracts[leaf],
                }
                for uid in units
            ],
        }
        if entry is not None:
            row["entry"] = entry
        return row

    def receipt(self, graph, leaf="Common#681", sequence=1, event="PREPARED", **extra):
        contracts = {"Common#681": self.CONTRACT_A, "Common#682": self.CONTRACT_B}
        row = {
            "event": event,
            "mode": "TAKEOVER_RECONCILE",
            "session_digest": M.entry_session_digest(self.owner()),
            "plan_digest": M.validate_graph(graph)["digest"],
            "child_ref": leaf,
            "child_contract_digest": contracts[leaf],
            "sequence": sequence,
            "evidence_refs": [f"{leaf}#entry-evidence"],
        }
        if event == "PREPARED":
            row.update({
                "phase_plan_ref": "Common#680#phase-plan",
                "reconciliation_ref": "Common#680#reconcile",
            })
        row.update(extra)
        return row

    def project(self, graph, ledger, moved=False):
        observations = {
            "Common#681": {"candidate_sha": self.SHA_B if moved else self.SHA_A},
            "Common#682": {"candidate_sha": self.SHA_A},
        }
        wrapped = [{"source": source, "order": i, "facts": fact} for i, (source, fact) in enumerate(ledger, 1)]
        return M.project(graph, wrapped, observations)

    def test_takeover_blocks_without_current_prepared_entry_evidence(self):
        g = self.graph()
        p = self.project(g, [("facts", self.fact())])
        report = M.admit(p, "Common#681", "take over", self.owner())
        self.assertEqual("RECONCILE_ENTRY", report["action"])
        self.assertEqual("ENTRY_PREPARED_EVIDENCE_MISSING", report["entry_admission"]["blocker"]["code"])

    def test_current_prepared_receipt_admits_only_the_bounded_child(self):
        g = self.graph()
        p = self.project(g, [("prep", self.fact(entry=self.receipt(g)))])
        report = M.admit(p, "Common#681", "take over", self.owner())
        self.assertEqual(("CONTINUE_UNIT", "U2"), (report["action"], report["child"]["unit"]))
        self.assertTrue(report["entry_admission"]["ready"])

    def test_recovery_precedes_entry_admission_when_material_moved(self):
        g = self.graph()
        p = self.project(g, [("facts", self.fact())], moved=True)
        report = M.admit(p, "Common#681", "take over", self.owner())
        self.assertEqual("RECOVER_EVIDENCE", report["action"])

    def test_stale_plan_or_wrong_child_contract_fails_closed(self):
        g = self.graph()
        cases = (
            ({"plan_digest": "sha256:" + "f" * 64}, "ENTRY_PLAN_STALE"),
            ({"child_contract_digest": "sha256:" + "e" * 64}, "ENTRY_CHILD_CONTRACT_MISMATCH"),
            ({"child_ref": "Common#682"}, "ENTRY_CHILD_MISMATCH"),
        )
        for overrides, expected in cases:
            with self.subTest(expected=expected):
                receipt = self.receipt(g, **overrides)
                p = self.project(g, [("prep", self.fact(entry=receipt))])
                report = M.admit(p, "Common#681", "take over", self.owner())
                self.assertEqual(expected, report["entry_admission"]["blocker"]["code"])

    def test_second_child_requires_exact_previous_execution_end(self):
        g = self.graph()
        prep1 = self.fact(entry=self.receipt(g))
        prep2 = self.fact(
            leaf="Common#682",
            entry=self.receipt(
                g,
                leaf="Common#682",
                sequence=2,
                previous_leaf_ref="Common#681",
                previous_evidence_ref="end-681",
            ),
        )
        blocked = self.project(g, [("prep-681", prep1), ("prep-682", prep2)])
        report = M.admit(blocked, "Common#682", "take over", self.owner())
        self.assertEqual("ENTRY_PREVIOUS_END_MISSING", report["entry_admission"]["blocker"]["code"])

        end1 = self.fact(entry=self.receipt(g, event="EXECUTION_END"))
        allowed = self.project(g, [("prep-681", prep1), ("end-681", end1), ("prep-682", prep2)])
        report = M.admit(allowed, "Common#682", "take over", self.owner())
        self.assertEqual(("CONTINUE_UNIT", "U2"), (report["action"], report["child"]["unit"]))

    def test_entry_receipt_is_strict_and_never_moves_progress(self):
        g = self.graph()
        good = self.receipt(g)
        self.assertEqual([], M.validate_facts(self.fact(entry=good)))
        baseline = self.project(g, [("facts", self.fact())])["nodes"]["Common#681"]["progress"]
        with_entry = self.project(g, [("prep", self.fact(entry=good))])["nodes"]["Common#681"]["progress"]
        self.assertEqual(baseline, with_entry)

        for key, value in (
            ("sequence", 0),
            ("plan_digest", "bad"),
            ("event", "STARTED"),
            ("evidence_refs", []),
        ):
            bad = copy.deepcopy(good)
            bad[key] = value
            with self.subTest(key=key):
                self.assertTrue(M.validate_facts(self.fact(entry=bad)))


if __name__ == "__main__":
    unittest.main()
