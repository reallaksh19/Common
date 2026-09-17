from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from blueprint_common import digest, seal_learning_run
from compile_assimilation_plan import apply_assimilation_plan, compile_assimilation_plan


class AssimilationCompilerTests(unittest.TestCase):
    BUNDLE = "MATH-HB-0000000000000001"

    OBL_SEM = "MATH-OBL-0000000000000001"
    OBL_INF = "MATH-OBL-0000000000000002"
    OBL_EQ = "MATH-OBL-0000000000000003"
    OBL_REP = "MATH-OBL-0000000000000004"
    OBL_MC = "MATH-OBL-0000000000000005"
    OBL_TR = "MATH-OBL-0000000000000006"

    def make_run(self, purpose="FIRST_STUDY"):
        return seal_learning_run({
            "run_id": "",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "ground_truth_ref": "MATH-GT-1111111111111111",
            "ground_truth_digest": "1" * 64,
            "control_plane": {
                "learner_prior_percent": 50,
                "learning_purpose": purpose,
                "product_mode": "PRACTICE",
                "owner_override_refs": [],
            },
            "current_state": "JOIN_READY",
            "state_history": [
                {"sequence": 0, "state": "GT_READY", "reason_code": "TEST_GT"},
                {"sequence": 1, "state": "ROUTED", "reason_code": "TEST_ROUTE"},
                {"sequence": 2, "state": "FIRST_CORE_COMPLETE", "reason_code": "TEST_FIRST"},
                {"sequence": 3, "state": "SECOND_CORE_COMPLETE", "reason_code": "TEST_SECOND"},
                {"sequence": 4, "state": "CROSS_VALIDATED", "reason_code": "TEST_XV"},
                {"sequence": 5, "state": "JOIN_READY", "reason_code": "TEST_JOIN"},
            ],
            "routing_ref": "MATH-RP-TEST",
            "bundles": [{
                "bundle_id": self.BUNDLE,
                "subtopic_refs": ["ALG-ROOT-RELATIONS"],
                "first_role": "CORE1",
                "core1_execution_ref": "MATH-SP-1111111111111111",
                "core2_execution_ref": "MATH-SP-2222222222222222",
                "cross_validation_ref": "MATH-XV-3333333333333333",
                "join_ref": None,
                "assimilation_plan_ref": None,
                "core1a_ref": None,
                "exposure_receipt_refs": [],
                "core2a_eligibility_ref": None,
                "core2a_ref": None,
            }],
            "publication_ref": None,
            "audit_ref": None,
            "run_digest": "",
        })

    def obligation(self, oid, otype, cap, *, required=True):
        return {
            "obligation_id": oid,
            "obligation_type": otype,
            "statement": f"Teach {otype.lower()} with explicit structure.",
            "origin_claim_refs": ["MATH-CL-1111111111111111"],
            "origin_evidence_refs": ["GT-SYLLABUS-1111111111111111"],
            "capability_refs": [cap],
            "learner_gap_states": ["NO_IDENTIFIED_GAP"],
            "required_before_core2a": required,
            "notes": None,
        }

    def make_demand(self, run, *, include_transfer=True, owner_constraints=None):
        obligations = [
            self.obligation(self.OBL_SEM, "SEMANTIC_UNDERSTANDING", "CAP-SEM"),
            self.obligation(self.OBL_INF, "INFERENCE_BRIDGE", "CAP-INF"),
            self.obligation(self.OBL_EQ, "EQUATION_ASSIMILATION", "CAP-EQ"),
            self.obligation(self.OBL_REP, "REPRESENTATION", "CAP-REP"),
            self.obligation(self.OBL_MC, "MISCONCEPTION_CONTRAST", "CAP-MC"),
        ]
        if include_transfer:
            obligations.append(self.obligation(self.OBL_TR, "TRANSFER", "CAP-TR"))

        gaps = []
        for obl in obligations:
            cap = obl["capability_refs"][0]
            developing = cap == "CAP-SEM"
            gaps.append({
                "capability_ref": cap,
                "readiness": "DEVELOPING" if developing else "READY",
                "gap_state": "BRIDGE_OR_PRACTICE_REQUIRED" if developing else "NO_IDENTIFIED_GAP",
                "basis": "LEARNER_EVIDENCE",
                "evidence_refs": ["LEARNER-EVIDENCE-1"],
                "owner_control_ref": None,
            })
            obl["learner_gap_states"] = [gaps[-1]["gap_state"]]

        demand = {
            "assimilation_demand_id": "",
            "schema_version": "1.0.0",
            "subject": "MATHEMATICS",
            "run_ref": run["run_id"],
            "bundle_ref": self.BUNDLE,
            "core1_package_ref": "MATH-SP-1111111111111111",
            "core1_package_digest": "2" * 64,
            "core2_package_ref": "MATH-SP-2222222222222222",
            "core2_package_digest": "3" * 64,
            "cross_validation_ref": "MATH-XV-3333333333333333",
            "cross_validation_digest": "4" * 64,
            "learner_capability_state_ref": "MATH-LCS-4444444444444444",
            "learner_capability_state_digest": "5" * 64,
            "learning_purpose": run["control_plane"]["learning_purpose"],
            "semantic_requirements": [{
                "claim_ref": "MATH-CL-1111111111111111",
                "claim_type": "CONCEPT",
                "statement": "Roots and coefficients are structurally related.",
                "resolution": "CONFIRMED",
                "evidence_refs": ["GT-SYLLABUS-1111111111111111"],
            }],
            "assessment_requirements": [{
                "claim_ref": "MATH-CL-2222222222222222",
                "claim_type": "QUESTION_DEMAND",
                "statement": "Recognize the useful symmetric relation before calculation.",
                "resolution": "INDEPENDENT_GROUNDED",
                "evidence_refs": ["GT-QUESTION_CORPUS-2222222222222222"],
            }],
            "learner_gaps": gaps,
            "purpose_requirements": ["TEST_PURPOSE_REQUIREMENT"],
            "owner_constraints": copy.deepcopy(owner_constraints or []),
            "unknowns": [],
            "conflicts": [],
            "assimilation_obligations": obligations,
            "unresolved_issue_refs": [],
            "status": "JOIN_READY",
            "demand_digest": "",
        }
        identity = {k: v for k, v in demand.items() if k not in {"assimilation_demand_id", "demand_digest"}}
        demand["assimilation_demand_id"] = "MATH-AD-" + digest(identity)[:16]
        demand["demand_digest"] = digest(demand, "demand_digest")

        out = copy.deepcopy(run)
        out["bundles"][0]["join_ref"] = demand["assimilation_demand_id"]
        run = seal_learning_run(out)
        return run, demand

    def make_spec(self, run, demand, *, include_transfer=True):
        obligations = {x["obligation_id"]: x for x in demand["assimilation_obligations"]}

        transformations = []
        atoms = []
        for idx, oid in enumerate(obligations, start=1):
            key = f"a{idx}"
            transformations.append({
                "local_key": f"t{idx}",
                "obligation_refs": [oid],
                "from_state": "fragmented recognition",
                "to_state": "connected usable structure",
                "transformation_type": "MODEL_BUILD",
                "rationale": "Convert a source-backed obligation into an explicit learner mental model.",
            })
            atoms.append({
                "local_key": key,
                "atom_type": "CONCEPT",
                "statement": f"Learning atom for {oid}.",
                "obligation_refs": [oid],
                "capability_refs": obligations[oid]["capability_refs"],
                "prerequisite_atom_keys": [] if idx == 1 else ["a1"],
            })

        inf_key = next(k for k, a in [(x["local_key"], x) for x in atoms] if self.OBL_INF in a["obligation_refs"])
        atoms.append({
            "local_key": "a_inf_target",
            "atom_type": "RELATION",
            "statement": "Target relation follows from the recognized invariant.",
            "obligation_refs": [self.OBL_INF],
            "capability_refs": ["CAP-INF"],
            "prerequisite_atom_keys": [inf_key],
        })

        by_obl = {}
        for atom in atoms:
            by_obl.setdefault(atom["obligation_refs"][0], []).append(atom["local_key"])

        spec = {
            "run_ref": run["run_id"],
            "bundle_ref": self.BUNDLE,
            "assimilation_demand_ref": demand["assimilation_demand_id"],
            "cognitive_transformations": transformations,
            "learning_atoms": atoms,
            "inference_chains": [{
                "local_key": "ic1",
                "obligation_refs": [self.OBL_INF],
                "atom_keys": [by_obl[self.OBL_INF][0], "a_inf_target"],
                "steps": [{
                    "from_atom_key": by_obl[self.OBL_INF][0],
                    "to_atom_key": "a_inf_target",
                    "inference": "Use the invariant to derive the target relation.",
                }],
            }],
            "equation_assimilations": [{
                "local_key": "eq1",
                "obligation_refs": [self.OBL_EQ],
                "atom_keys": [by_obl[self.OBL_EQ][0]],
                "equation_text": "alpha + beta + gamma = -a",
                "meaning": "The sum of the roots equals the negative cubic coefficient in monic form.",
                "symbol_bridge_keys": ["sb1"],
                "validity_conditions": ["Polynomial is monic and coefficients follow x^3 + ax^2 + bx + c."],
            }],
            "representation_requirements": [{
                "local_key": "rr1",
                "obligation_refs": [self.OBL_REP],
                "atom_keys": [by_obl[self.OBL_REP][0]],
                "purpose": "MAKE_RELATION_VISIBLE",
                "must_externalize": True,
            }],
            "representation_candidates": [{
                "local_key": "rc1",
                "requirement_key": "rr1",
                "representation_type": "ROOT_FACTOR_MAP",
                "description": "Map roots to factors and then to coefficient relations.",
                "affordances": ["Shows the structural bridge from roots to coefficients."],
                "limitations": ["Less compact than a formula-only view."],
                "admissible": True,
            }, {
                "local_key": "rc2",
                "requirement_key": "rr1",
                "representation_type": "ALGEBRAIC_TABLE",
                "description": "Table of elementary symmetric sums and coefficients.",
                "affordances": ["Supports quick comparison of coefficient roles."],
                "limitations": ["Can hide why the relations are true."],
                "admissible": True,
            }],
            "representation_decisions": [{
                "requirement_key": "rr1",
                "selected_candidate_key": "rc1",
                "rationale": "The root-factor map exposes causality before compression into a table.",
                "rejected_candidate_keys": ["rc2"],
            }],
            "misconception_contrasts": [{
                "local_key": "mc1",
                "obligation_refs": [self.OBL_MC],
                "atom_keys": [by_obl[self.OBL_MC][0]],
                "misconception": "The sign of the root sum matches the x^2 coefficient.",
                "contrast": "For a monic cubic the root sum is the negative of that coefficient.",
                "diagnostic_cue": "Learner writes alpha+beta+gamma=a instead of -a.",
            }],
            "symbol_bridges": [{
                "local_key": "sb1",
                "obligation_refs": [self.OBL_EQ],
                "atom_keys": [by_obl[self.OBL_EQ][0]],
                "symbol": "a",
                "meaning": "coefficient of x^2 in the monic cubic",
                "bridge_statement": "Read a as a coefficient role, not as a free root.",
            }],
            "fading_plans": [{
                "local_key": "fp1",
                "obligation_refs": [self.OBL_SEM],
                "atom_keys": [by_obl[self.OBL_SEM][0]],
                "stages": ["MODELLED", "GUIDED", "FADED", "INDEPENDENT"],
                "support_notes": [
                    "Teacher exposes the root-factor-coefficient bridge.",
                    "Learner completes one missing relation with prompts.",
                    "Learner receives only a structural cue.",
                    "Learner reconstructs the relation unaided.",
                ],
            }],
            "transfer_bridges": [],
            "owner_constraint_compliance": [{
                "constraint_id": x["constraint_id"],
                "disposition": "SATISFIED",
                "rationale": "Compiler spec explicitly satisfies this owner control.",
            } for x in demand["owner_constraints"]],
            "unresolved_issue_refs": [],
        }
        if include_transfer and self.OBL_TR in obligations:
            spec["transfer_bridges"].append({
                "local_key": "tb1",
                "obligation_refs": [self.OBL_TR],
                "atom_keys": [by_obl[self.OBL_TR][0]],
                "source_structure": "Direct coefficient-to-root-sum relation.",
                "changed_surface": "Target is hidden inside a symmetric expression.",
                "invariant_to_preserve": "The same elementary symmetric relation controls the expression.",
                "target_demand": "Recognize the invariant before calculating.",
            })
        return spec

    def prepared(self, purpose="FIRST_STUDY", *, include_transfer=True, owner_constraints=None):
        run = self.make_run(purpose)
        run, demand = self.make_demand(
            run, include_transfer=include_transfer, owner_constraints=owner_constraints
        )
        spec = self.make_spec(run, demand, include_transfer=include_transfer)
        return run, demand, spec

    def test_compile_and_apply_reaches_assimilation_compiled(self):
        run, demand, spec = self.prepared()
        plan = compile_assimilation_plan(run, demand, spec)
        self.assertEqual(plan["status"], "ASSIMILATION_READY")
        self.assertEqual(
            {x["obligation_ref"] for x in plan["obligation_coverage"]},
            {x["obligation_id"] for x in demand["assimilation_obligations"]},
        )
        self.assertEqual(len(plan["representation_decisions"]), 1)
        updated = apply_assimilation_plan(run, plan)
        self.assertEqual(updated["current_state"], "ASSIMILATION_COMPILED")
        self.assertEqual(updated["bundles"][0]["assimilation_plan_ref"], plan["assimilation_plan_id"])

    def test_compilation_is_deterministic(self):
        run, demand, spec = self.prepared()
        self.assertEqual(
            compile_assimilation_plan(run, demand, spec),
            compile_assimilation_plan(run, demand, copy.deepcopy(spec)),
        )

    def test_inference_obligation_requires_inference_chain(self):
        run, demand, spec = self.prepared()
        spec["inference_chains"] = []
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_OBLIGATION_COMPONENT_MISSING"):
            compile_assimilation_plan(run, demand, spec)

    def test_representation_requires_two_candidates(self):
        run, demand, spec = self.prepared()
        spec["representation_candidates"] = spec["representation_candidates"][:1]
        spec["representation_decisions"][0]["rejected_candidate_keys"] = []
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_REPRESENTATION_CANDIDATES_INSUFFICIENT"):
            compile_assimilation_plan(run, demand, spec)

    def test_inadmissible_representation_cannot_be_selected(self):
        run, demand, spec = self.prepared()
        spec["representation_candidates"][0]["admissible"] = False
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_REPRESENTATION_SELECTED_INADMISSIBLE"):
            compile_assimilation_plan(run, demand, spec)

    def test_prerequisite_graph_must_be_acyclic(self):
        run, demand, spec = self.prepared()
        spec["learning_atoms"][0]["prerequisite_atom_keys"] = ["a2"]
        spec["learning_atoms"][1]["prerequisite_atom_keys"] = ["a1"]
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_PREREQUISITE_CYCLE"):
            compile_assimilation_plan(run, demand, spec)

    def test_developing_or_unknown_gap_requires_fading(self):
        run, demand, spec = self.prepared()
        spec["fading_plans"] = []
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_FADING_REQUIRED"):
            compile_assimilation_plan(run, demand, spec)

    def test_competitive_purpose_requires_transfer_even_without_transfer_obligation(self):
        run, demand, spec = self.prepared("COMPETITIVE_EXAM", include_transfer=False)
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_COMPETITION_TRANSFER_REQUIRED"):
            compile_assimilation_plan(run, demand, spec)

    def test_hard_owner_constraint_cannot_be_deferred(self):
        constraint = {
            "constraint_id": "OWNER-1",
            "mode": "HARD",
            "target": "REPRESENTATION",
            "instruction": "Use an explicit structural representation.",
            "authority_class": "OWNER_CONTROL",
        }
        run, demand, spec = self.prepared(owner_constraints=[constraint])
        spec["owner_constraint_compliance"][0]["disposition"] = "DEFERRED"
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_HARD_OWNER_CONSTRAINT_UNSATISFIED"):
            compile_assimilation_plan(run, demand, spec)

    def test_demand_must_match_run_purpose(self):
        run, demand, spec = self.prepared()
        demand = copy.deepcopy(demand)
        demand["learning_purpose"] = "REVISION"
        demand["demand_digest"] = digest(demand, "demand_digest")
        with self.assertRaisesRegex(ValueError, "ASSIMILATION_COMPILER_PURPOSE_MISMATCH"):
            compile_assimilation_plan(run, demand, spec)


if __name__ == "__main__":
    unittest.main()
