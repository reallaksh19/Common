#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
SCRIPTS = HERE.parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import delp_projection_v35 as DELP  # noqa: E402
import actual_next_v35 as NEXT  # noqa: E402


def condition(kind: str, status: str = "TRUE") -> dict:
    return {
        "type": kind,
        "status": status,
        "reason": f"{kind.upper()}_{status}",
        "message": f"{kind} is {status}.",
        "observed_generation": 3,
        "candidate_sha": "a" * 40,
        "source_refs": [f"fixture:{kind}"],
    }


def canonical_conditions(**overrides: str) -> list[dict]:
    statuses = {
        "PlanReady": "TRUE",
        "SpecCurrent": "TRUE",
        "MaterialObserved": "TRUE",
        "EvidenceCurrent": "TRUE",
        "DependenciesReady": "NOT_APPLICABLE",
        "CustodySafe": "NOT_APPLICABLE",
        "AssuranceSatisfied": "NOT_APPLICABLE",
        "ProviderVisible": "TRUE",
    }
    statuses.update(overrides)
    return [condition(kind, statuses[kind]) for kind in DELP.CONDITION_ORDER]


def base_leaf(**extra) -> dict:
    row = {
        "lifecycle": "ACTIVE",
        "conditions": canonical_conditions(),
        "activity_epoch": 1,
        "units": [{"id": "U1", "complete": False}],
        "gates": [],
        "dependencies": {"declared": [], "ready": True, "blocking": []},
        "active_unit": "U1",
        "next": {"unit": "U1", "action": "executor detail"},
        "owner_action": "NONE",
        "successor_policy": None,
    }
    row.update(extra)
    return row


class ActualNextContractV35Tests(unittest.TestCase):
    def test_exact_canonical_condition_set_is_required(self):
        missing = base_leaf()
        missing["conditions"] = missing["conditions"][:-1]
        with self.assertRaises(DELP.DelpError):
            NEXT.derive_actual_next(missing)

        duplicate = base_leaf()
        duplicate["conditions"].append(copy.deepcopy(duplicate["conditions"][0]))
        with self.assertRaises(DELP.DelpError):
            NEXT.derive_actual_next(duplicate)

    def test_output_is_one_pure_decision_record(self):
        result = NEXT.derive_actual_next(base_leaf())
        self.assertEqual(
            {"authority", "action", "reason", "source_basis", "detail"},
            set(result),
        )
        self.assertEqual(NEXT.AUTHORITY, result["authority"])
        self.assertIn(result["action"], NEXT.ACTIONS)
        self.assertIsInstance(result["source_basis"], list)

    def test_terminal_lifecycle_returns_none_before_nonterminal_conditions(self):
        row = base_leaf(
            lifecycle="COMPLETE",
            conditions=canonical_conditions(
                PlanReady="FALSE",
                SpecCurrent="FALSE",
                EvidenceCurrent="FALSE",
            ),
        )
        result = NEXT.derive_actual_next(row)
        self.assertEqual(("NONE", "TERMINAL_LIFECYCLE"), (result["action"], result["reason"]))

    def test_same_input_is_canonically_deterministic(self):
        row = base_leaf()
        first = NEXT.derive_actual_next(copy.deepcopy(row))
        second = NEXT.derive_actual_next(copy.deepcopy(row))
        self.assertEqual(
            json.dumps(first, sort_keys=True, separators=(",", ":")),
            json.dumps(second, sort_keys=True, separators=(",", ":")),
        )

    def test_derivation_does_not_mutate_leaf_input(self):
        row = base_leaf()
        before = copy.deepcopy(row)
        NEXT.derive_actual_next(row)
        self.assertEqual(before, row)


    def test_plan_ready_false_outranks_all_downstream_recovery(self):
        row = base_leaf(
            conditions=canonical_conditions(
                PlanReady="FALSE",
                SpecCurrent="FALSE",
                CustodySafe="FALSE",
                EvidenceCurrent="FALSE",
                DependenciesReady="FALSE",
            ),
            materialization={"status": "UNMATERIALIZED", "provider_signal": "PR_OPEN"},
            dependencies={"declared": ["Common#9"], "ready": False, "blocking": []},
        )
        self.assertEqual("FIX_PLAN", NEXT.derive_actual_next(row)["action"])

    def test_spec_false_outranks_custody_material_and_evidence(self):
        row = base_leaf(
            conditions=canonical_conditions(
                SpecCurrent="FALSE",
                CustodySafe="FALSE",
                EvidenceCurrent="FALSE",
            ),
            materialization={"status": "UNMATERIALIZED", "provider_signal": "PR_OPEN"},
        )
        self.assertEqual("RECONCILE_SPEC", NEXT.derive_actual_next(row)["action"])

    def test_custody_false_outranks_materialization_and_evidence(self):
        row = base_leaf(
            conditions=canonical_conditions(
                CustodySafe="FALSE",
                EvidenceCurrent="FALSE",
            ),
            materialization={"status": "UNMATERIALIZED", "provider_signal": "PR_OPEN"},
        )
        self.assertEqual("RECOVER_CUSTODY", NEXT.derive_actual_next(row)["action"])

    def test_provider_visible_work_without_facts_materializes_before_evidence_recovery(self):
        row = base_leaf(
            activity_epoch=0,
            conditions=canonical_conditions(EvidenceCurrent="FALSE"),
            materialization={"status": "UNMATERIALIZED", "provider_signal": "PR_OPEN"},
        )
        self.assertEqual("MATERIALIZE_FACTS", NEXT.derive_actual_next(row)["action"])

    def test_provider_unavailable_waits_when_existing_facts_need_material_or_evidence_truth(self):
        row = base_leaf(
            activity_epoch=2,
            conditions=canonical_conditions(
                ProviderVisible="UNKNOWN",
                MaterialObserved="UNKNOWN",
                EvidenceCurrent="UNKNOWN",
            ),
        )
        self.assertEqual("WAIT_PROVIDER", NEXT.derive_actual_next(row)["action"])

    def test_evidence_false_recovers_when_higher_precedence_conditions_are_clear(self):
        row = base_leaf(conditions=canonical_conditions(EvidenceCurrent="FALSE"))
        self.assertEqual("RECOVER_EVIDENCE", NEXT.derive_actual_next(row)["action"])


    def test_independent_reconstruction_handoff_precedes_dependency_wait(self):
        row = base_leaf(
            conditions=canonical_conditions(DependenciesReady="FALSE"),
            dependencies={"declared": ["Common#9"], "ready": False, "blocking": []},
            successor_policy={
                "mode": "INDEPENDENT_RECONSTRUCTION",
                "decision_at_risk": "root classification",
            },
            handover={"status": "RECONSTRUCTING"},
        )
        self.assertEqual("RECONCILE_HANDOFF", NEXT.derive_actual_next(row)["action"])

    def test_declared_dependency_false_or_unknown_waits(self):
        for status in ("FALSE", "UNKNOWN"):
            with self.subTest(status=status):
                row = base_leaf(
                    conditions=canonical_conditions(DependenciesReady=status),
                    dependencies={"declared": ["Common#9"], "ready": False, "blocking": []},
                )
                self.assertEqual("WAIT_DEPENDENCY", NEXT.derive_actual_next(row)["action"])

    def test_assurance_false_remediates_after_dependencies_are_clear(self):
        row = base_leaf(conditions=canonical_conditions(AssuranceSatisfied="FALSE"))
        self.assertEqual("REMEDIATE_FINDING", NEXT.derive_actual_next(row)["action"])

    def test_complete_units_with_open_delivery_gate_reviews_candidate_before_owner_wait(self):
        row = base_leaf(
            units=[{"id": "U1", "complete": True}],
            gates=[{"id": "REVIEW", "passed": False, "evidence_current": False}],
            active_unit=None,
            owner_action="REQUIRED — merge decision",
        )
        self.assertEqual("REVIEW_CANDIDATE", NEXT.derive_actual_next(row)["action"])

    def test_explicit_owner_action_precedes_continue_unit(self):
        row = base_leaf(owner_action="REQUIRED — approve external dependency")
        self.assertEqual("WAIT_OWNER", NEXT.derive_actual_next(row)["action"])

    def test_active_unit_continues_and_executor_next_is_detail_only(self):
        row = base_leaf(next={"unit": "U1", "action": "run bounded implementation"})
        result = NEXT.derive_actual_next(row)
        self.assertEqual("CONTINUE_UNIT", result["action"])
        self.assertEqual("ACTIVE_UNIT_AVAILABLE", result["reason"])
        self.assertEqual("U1 — run bounded implementation", result["detail"])

    def test_complete_clean_units_publish_result(self):
        row = base_leaf(
            units=[{"id": "U1", "complete": True}],
            gates=[],
            active_unit=None,
            next={"unit": None, "action": "executor says continue anyway"},
        )
        self.assertEqual("PUBLISH_RESULT", NEXT.derive_actual_next(row)["action"])


    def test_provider_unknown_fresh_leaf_does_not_invent_wait_provider_or_spec_reconcile(self):
        row = base_leaf(
            activity_epoch=0,
            conditions=canonical_conditions(
                SpecCurrent="UNKNOWN",
                ProviderVisible="UNKNOWN",
                MaterialObserved="UNKNOWN",
                EvidenceCurrent="UNKNOWN",
            ),
        )
        self.assertEqual("CONTINUE_UNIT", NEXT.derive_actual_next(row)["action"])

    def test_not_applicable_custody_and_assurance_never_fabricate_actions(self):
        row = base_leaf(
            conditions=canonical_conditions(
                CustodySafe="NOT_APPLICABLE",
                AssuranceSatisfied="NOT_APPLICABLE",
            ),
        )
        self.assertEqual("CONTINUE_UNIT", NEXT.derive_actual_next(row)["action"])

    def test_dependency_unknown_without_declared_dependencies_does_not_block(self):
        row = base_leaf(conditions=canonical_conditions(DependenciesReady="UNKNOWN"))
        self.assertEqual("CONTINUE_UNIT", NEXT.derive_actual_next(row)["action"])

    def test_declared_dependency_not_applicable_is_a_fail_closed_contradiction(self):
        row = base_leaf(
            conditions=canonical_conditions(DependenciesReady="NOT_APPLICABLE"),
            dependencies={"declared": ["Common#9"], "ready": False, "blocking": []},
        )
        with self.assertRaises(DELP.DelpError):
            NEXT.derive_actual_next(row)

    def test_executor_proposed_next_cannot_override_higher_actual_next(self):
        row = base_leaf(
            conditions=canonical_conditions(PlanReady="FALSE"),
            next={"unit": "U1", "action": "merge immediately"},
        )
        result = NEXT.derive_actual_next(row)
        self.assertEqual("FIX_PLAN", result["action"])
        self.assertNotIn("merge immediately", json.dumps(result, sort_keys=True))

    def test_decision_record_contains_no_progress_or_provider_authority_fields(self):
        result = NEXT.derive_actual_next(base_leaf())
        forbidden = {
            "progress",
            "percentage",
            "P",
            "E",
            "D",
            "DE",
            "title",
            "frontier",
            "provider",
            "merge_authorized",
        }
        self.assertTrue(forbidden.isdisjoint(result))

    def test_incomplete_leaf_without_active_unit_or_recovery_signal_fails_closed(self):
        row = base_leaf(active_unit=None, next={"unit": None, "action": "guess"})
        with self.assertRaises(DELP.DelpError):
            NEXT.derive_actual_next(row)


    def test_passed_but_stale_delivery_gate_still_reviews_candidate(self):
        row = base_leaf(
            units=[{"id": "U1", "complete": True}],
            gates=[{"id": "REVIEW", "passed": True, "evidence_current": False}],
            active_unit=None,
        )
        self.assertEqual("REVIEW_CANDIDATE", NEXT.derive_actual_next(row)["action"])


    def test_provider_unknown_without_accepted_facts_does_not_invent_wait_provider(self):
        row = base_leaf(
            activity_epoch=0,
            conditions=canonical_conditions(
                ProviderVisible="UNKNOWN",
                MaterialObserved="UNKNOWN",
                EvidenceCurrent="UNKNOWN",
            ),
        )
        result = NEXT.derive_actual_next(row)
        self.assertEqual("CONTINUE_UNIT", result["action"])

    def test_spec_unknown_without_accepted_facts_does_not_force_reconcile(self):
        row = base_leaf(
            activity_epoch=0,
            conditions=canonical_conditions(SpecCurrent="UNKNOWN"),
        )
        self.assertEqual("CONTINUE_UNIT", NEXT.derive_actual_next(row)["action"])

    def test_not_applicable_custody_and_assurance_do_not_trigger_future_phase_actions(self):
        row = base_leaf(
            conditions=canonical_conditions(
                CustodySafe="NOT_APPLICABLE",
                AssuranceSatisfied="NOT_APPLICABLE",
            )
        )
        action = NEXT.derive_actual_next(row)["action"]
        self.assertEqual("CONTINUE_UNIT", action)
        self.assertNotIn(action, {"RECOVER_CUSTODY", "REMEDIATE_FINDING"})

    def test_dependency_unknown_without_declared_dependencies_does_not_block(self):
        row = base_leaf(
            conditions=canonical_conditions(DependenciesReady="UNKNOWN"),
            dependencies={"declared": [], "ready": False, "blocking": []},
        )
        self.assertEqual("CONTINUE_UNIT", NEXT.derive_actual_next(row)["action"])

    def test_declared_dependencies_cannot_be_not_applicable(self):
        row = base_leaf(
            conditions=canonical_conditions(DependenciesReady="NOT_APPLICABLE"),
            dependencies={"declared": ["Common#9"], "ready": False, "blocking": []},
        )
        with self.assertRaises(DELP.DelpError):
            NEXT.derive_actual_next(row)

    def test_executor_next_cannot_override_higher_actual_next(self):
        row = base_leaf(
            conditions=canonical_conditions(PlanReady="FALSE"),
            next={"unit": "U1", "action": "PUBLISH_RESULT and merge"},
        )
        result = NEXT.derive_actual_next(row)
        self.assertEqual("FIX_PLAN", result["action"])
        self.assertNotIn("PUBLISH_RESULT", result["detail"] or "")

    def test_executor_next_unit_cannot_select_a_different_active_unit(self):
        row = base_leaf(
            active_unit="U1",
            next={"unit": "U99", "action": "work on a different unit"},
        )
        result = NEXT.derive_actual_next(row)
        self.assertEqual("CONTINUE_UNIT", result["action"])
        self.assertTrue((result["detail"] or "").startswith("U1"))
        self.assertNotIn("U99", result["detail"] or "")

    def test_optional_check_telemetry_is_ignored_by_actual_next(self):
        row = base_leaf(check={"state": "FAILED", "name": "optional-ci"})
        baseline = NEXT.derive_actual_next(base_leaf())
        observed = NEXT.derive_actual_next(row)
        self.assertEqual(baseline, observed)

    def test_decision_never_authors_progress_or_projection_fields(self):
        result = NEXT.derive_actual_next(base_leaf())
        forbidden = {
            "progress", "percent", "percentage", "p", "e", "d", "frontier",
            "title", "live_status", "currentness", "graph_generation",
            "contract_current", "provider_observation",
        }
        self.assertTrue(forbidden.isdisjoint({key.lower() for key in result}))


if __name__ == "__main__":
    unittest.main()
