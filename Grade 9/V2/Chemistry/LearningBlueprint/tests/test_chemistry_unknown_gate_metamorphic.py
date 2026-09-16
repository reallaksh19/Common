import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_engineering_closure import compile_closure  # noqa: E402
from compile_chemistry_semantic_projection import compile_semantic_projection  # noqa: E402

PRODUCTION_REGISTRY = json.loads(
    (ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8")
)
TEMPLATE = PRODUCTION_REGISTRY["subtopic_gates"][0]


def synthetic_gate(gate_id: str, suffix: str, prerequisites: list[str]) -> dict:
    gate = copy.deepcopy(TEMPLATE)
    gate["subtopic_id"] = gate_id
    gate["learner_title"] = f"Synthetic governed Chemistry gate {suffix}"
    gate["chapter"] = "Synthetic compiler falsifier"
    gate["prerequisite_ids"] = list(prerequisites)
    gate["provenance"] = {
        "authority_class": "SOURCE-DEFINED",
        "source_curriculum": "Synthetic compiler falsifier only",
        "source_scope": "IN_SCOPE",
        "source_reference": f"SYNTHETIC-SOURCE-{suffix}",
        "claim_status": "VERIFIED_CANONICAL",
    }

    concept_map = {}
    for index, row in enumerate(gate["technical_core"], 1):
        old = row["concept_id"]
        new = f"CON-CHEM-SYNTH-{suffix}-{index:02d}"
        concept_map[old] = new
        row["concept_id"] = new
        row["canonical_statement"] = f"Synthetic canonical Chemistry statement {suffix}-{index}."
        row["why_required"] = "Proves a newly declared gate can flow through generic authority."
        row["failure_if_omitted"] = "The synthetic gate would lose required technical structure."
    gate["canonical_concept_ids"] = [concept_map[value] for value in gate["canonical_concept_ids"]]

    for index, row in enumerate(gate["mandatory_equations"], 1):
        row["equation_id"] = f"EQ-CHEM-SYNTH-{suffix}-{index:02d}"
        row["formula"] = f"X{index} = Y{index}"
        row["meaning_of_symbols"] = "Synthetic symbolic relationship used only for compiler falsification."
        row["conditions_of_validity"] = "Synthetic declared condition only."

    for index, row in enumerate(gate["representations"], 1):
        row["representation_id"] = f"REP-CHEM-SYNTH-{suffix}-{index:02d}"
        row["name"] = f"Synthetic representation {suffix}-{index}"
        row["chemistry_encoded"] = "Synthetic governed relationship, not a topic-specific representation."
        row["mandatory_labels"] = ["Synthetic input", "Synthetic output"]
        row["what_cannot_be_omitted"] = "The governed relationship."
        row["common_incorrect_version"] = "An ungoverned relationship."
        row["verification_method"] = "Verify the represented relationship against the synthetic authority."

    for index, row in enumerate(gate["misconceptions"], 1):
        row["misconception_id"] = f"MISC-CHEM-SYNTH-{suffix}-{index:02d}"
        row["incorrect_belief"] = "A synthetic governed relationship may be reversed without evidence."
        row["why_plausible"] = "The learner may ignore directionality."
        row["required_counterexample"] = "A synthetic case where reversal contradicts the stated evidence."
        row["required_technical_repair"] = "Preserve the relationship direction established by evidence."

    family_map = {}
    for index, row in enumerate(gate["problem_families"], 1):
        old = row["family_id"]
        new = f"PF-CHEM-SYNTH-{suffix}-{index:02d}"
        family_map[old] = new
        row["family_id"] = new
        row["name"] = f"Synthetic governed problem family {suffix}-{index}"
        row["recognition_cues"] = "A governed synthetic relationship must be identified before solving."
        row["first_technical_move"] = "Write the governed synthetic relationship explicitly."
        row["common_fatal_error"] = "Reverse the governed relationship before checking evidence."
        row["typical_unknown"] = "The chemically consistent synthetic conclusion."
    gate["linked_problem_family_ids"] = [family_map[value] for value in gate["linked_problem_family_ids"]]

    gate["mandatory_verifications"] = [
        "Verify the synthetic conclusion independently against the declared relationship."
    ]
    gate["difficulty_profile"]["difficulty_basis"] = (
        "Synthetic difficulty evidence used only to prove topic-neutral compiler behavior."
    )
    gate["release_checklist"] = {key: True for key in gate["release_checklist"]}
    gate["falsification_cases"] = [
        {
            "test_id": f"CHEM-FAIL-SYNTH-{suffix}",
            "authoring_defect": "Drop a governed synthetic relationship.",
            "expected_failure_reason": "Required engineering structure would be missing.",
        }
    ]
    return gate


def registry(*gates: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "registry_id": "CHEM-G9-11-TECHNICAL-ENGINEERING-GATES-v1",
        "authority": "CANONICAL_DOMAIN_REGISTRY",
        "governing_standard": "FAIL_CLOSED_ENGINEERING_GATES",
        "maturity": "ENGINEERING",
        "subtopic_gates": list(gates),
    }


def request(request_id: str, depth: str = "STANDARD") -> dict:
    return {
        "schema_version": "2.0.0",
        "request_id": request_id,
        "subject": "CHEMISTRY",
        "requested_topic": "Synthetic unknown-gate compiler proof",
        "requested_scope": "Synthetic authority supplied only to generic compilers",
        "engineering_depth": depth,
        "requested_action": "DECLARE_DIRECT_GATES",
        "requested_for": ["CORE1A", "CORE1B", "CORE2A", "CORE2B", "PAL"],
    }


def manifest(request_id: str, manifest_id: str, direct_gate: str, *, research=False) -> dict:
    out = {
        "schema_version": "2.0.0",
        "manifest_id": manifest_id,
        "request_id": request_id,
        "scope_kind": "SUBTOPIC",
        "scope_ref": "SYNTHETIC_UNKNOWN_GATE",
        "topic_id": "CHEM-SYNTHETIC-UNKNOWN-GATE",
        "title": "Synthetic unknown-gate compiler proof",
        "registry_ref": "policies/chemistry-technical-engineering-gates.v1.json",
        "required_gate_ids": [direct_gate],
        "optional_gate_ids": [],
        "out_of_scope_gate_ids": [],
        "source_audits": [],
        "external_prerequisite_resolutions": [
            {
                "dependency_id": "MATH-BASIC-ARITHMETIC",
                "status": "RESOLVED_BY_AUTHORITY",
                "evidence_ref": "SYNTHETIC_TEST_AUTHORITY",
            }
        ],
        "source_item_status": "INDEPENDENT_OF_TECHNICAL_GATE",
        "downstream_consumers": ["CDAU", "SDU", "LAU", "TTU", "PAL"],
    }
    if research:
        out["research_dossier_ref"] = "tests/in-memory-synthetic-research-dossier.json"
        out["claim_ledger_ref"] = "tests/in-memory-synthetic-claim-ledger.json"
    return out


def research_dossier(request_id: str) -> dict:
    return {
        "schema_version": "2.0.0",
        "dossier_id": "CHEM-ENG-DOSSIER-SYNTHETIC-UNKNOWN-GATE",
        "request_id": request_id,
        "engineering_depth": "RESEARCH",
        "scope_definition": "Synthetic research-depth Chemistry scope used only for generic compiler falsification.",
        "authoritative_source_set": [
            {
                "source_ref": "SYNTHETIC-RESEARCH-SOURCE",
                "authority_class": "SOURCE_DEFINED",
                "scope": "Synthetic test scope",
            }
        ],
        "curriculum_boundaries": ["Synthetic boundary: no production learner content."],
        "representation_evidence": ["Synthetic representation evidence."],
        "misconception_evidence": ["Synthetic misconception evidence."],
        "selected_design_decisions": ["Use only declared synthetic authority."],
        "rejected_alternatives": ["Infer undeclared Chemistry from a topic name."],
        "status": "RESEARCH_DOSSIER_READY",
    }


def claim_ledger(request_id: str) -> dict:
    return {
        "schema_version": "2.0.0",
        "ledger_id": "CHEM-ENG-CLAIMS-SYNTHETIC-UNKNOWN-GATE",
        "request_id": request_id,
        "claims": [
            {
                "claim_id": "SYNTHETIC-CLAIM-01",
                "statement": "Synthetic research claim remains explicitly source-bound.",
                "authority_class": "SOURCE_DEFINED",
                "evidence_ref": "SYNTHETIC-RESEARCH-SOURCE",
                "scope_status": "IN_SCOPE",
            }
        ],
        "status": "CLAIM_LEDGER_READY",
    }


def structural_signature(packet: dict) -> list[tuple]:
    return [
        (
            row["kind"],
            row["direct"],
            tuple(row["authorized_modes"]),
            tuple(row["required_realization_modes"]),
            tuple(sorted(row["payload"].keys())),
        )
        for row in packet["obligations"]
    ]


class ChemistryUnknownGateMetamorphicTests(unittest.TestCase):
    def test_unknown_gate_id_renaming_does_not_change_compiler_behavior(self):
        alpha_gate = synthetic_gate("CHEM-SYNTH-ALPHA", "ALPHA", ["MATH-BASIC-ARITHMETIC"])
        beta_gate = synthetic_gate("CHEM-SYNTH-BETA", "BETA", ["MATH-BASIC-ARITHMETIC"])

        alpha_request = request("CHEM-ENG-REQ-SYNTH-ALPHA")
        alpha_manifest = manifest(
            alpha_request["request_id"],
            "CHEM-ENG-MAN-SYNTH-ALPHA",
            alpha_gate["subtopic_id"],
        )
        beta_request = request("CHEM-ENG-REQ-SYNTH-BETA")
        beta_manifest = manifest(
            beta_request["request_id"],
            "CHEM-ENG-MAN-SYNTH-BETA",
            beta_gate["subtopic_id"],
        )

        alpha_packet = compile_blueprint_obligations(
            alpha_request,
            alpha_manifest,
            registry=registry(alpha_gate),
        )
        beta_packet = compile_blueprint_obligations(
            beta_request,
            beta_manifest,
            registry=registry(beta_gate),
        )

        self.assertEqual(structural_signature(alpha_packet), structural_signature(beta_packet))
        alpha_semantics = compile_semantic_projection(alpha_packet)
        beta_semantics = compile_semantic_projection(beta_packet)
        self.assertEqual(
            [(row["source_kind"], row["source_field"], row["semantic_role"]) for row in alpha_semantics["semantic_atoms"]],
            [(row["source_kind"], row["source_field"], row["semantic_role"]) for row in beta_semantics["semantic_atoms"]],
        )

    def test_three_gate_chain_closes_prerequisites_but_only_c_is_direct(self):
        gate_a = synthetic_gate("CHEM-SYNTH-A", "A", ["MATH-BASIC-ARITHMETIC"])
        gate_b = synthetic_gate("CHEM-SYNTH-B", "B", [gate_a["subtopic_id"]])
        gate_c = synthetic_gate("CHEM-SYNTH-C", "C", [gate_b["subtopic_id"]])
        reg = registry(gate_a, gate_b, gate_c)
        req = request("CHEM-ENG-REQ-SYNTH-CHAIN")
        man = manifest(req["request_id"], "CHEM-ENG-MAN-SYNTH-CHAIN", gate_c["subtopic_id"])

        receipt = compile_closure(req, man, registry=reg)
        self.assertEqual(receipt["closure_status"], "READY")
        self.assertEqual(receipt["closure_gate_ids"], ["CHEM-SYNTH-A", "CHEM-SYNTH-B", "CHEM-SYNTH-C"])
        self.assertEqual(receipt["direct_gate_ids"], ["CHEM-SYNTH-C"])
        self.assertEqual(
            [row["gate_id"] for row in receipt["gate_states"] if row["direct"]],
            ["CHEM-SYNTH-C"],
        )

        packet = compile_blueprint_obligations(req, man, registry=reg)
        self.assertTrue(any(row["gate_id"] == "CHEM-SYNTH-C" and row["direct"] for row in packet["obligations"]))
        self.assertFalse(any(row["gate_id"] in {"CHEM-SYNTH-A", "CHEM-SYNTH-B"} and row["direct"] for row in packet["obligations"]))
        self.assertFalse(any(
            row["gate_id"] in {"CHEM-SYNTH-A", "CHEM-SYNTH-B"} and row["required_realization_modes"]
            for row in packet["obligations"]
        ))

    def test_research_depth_fails_without_evidence_and_passes_with_governed_artifacts(self):
        gate = synthetic_gate("CHEM-SYNTH-RESEARCH", "RESEARCH", ["MATH-BASIC-ARITHMETIC"])
        reg = registry(gate)
        req = request("CHEM-ENG-REQ-SYNTH-RESEARCH", depth="RESEARCH")

        missing_manifest = manifest(
            req["request_id"],
            "CHEM-ENG-MAN-SYNTH-RESEARCH-MISSING",
            gate["subtopic_id"],
            research=False,
        )
        blocked = compile_closure(req, missing_manifest, registry=reg)
        self.assertEqual(blocked["closure_status"], "BLOCKED")
        self.assertEqual(
            {row["code"] for row in blocked["blockers"]},
            {"CHEM_ENG_RESEARCH_DOSSIER_REQUIRED", "CHEM_ENG_CLAIM_LEDGER_REQUIRED"},
        )

        governed_manifest = manifest(
            req["request_id"],
            "CHEM-ENG-MAN-SYNTH-RESEARCH-GOVERNED",
            gate["subtopic_id"],
            research=True,
        )
        dossier = research_dossier(req["request_id"])
        ledger = claim_ledger(req["request_id"])
        ready = compile_closure(
            req,
            governed_manifest,
            registry=reg,
            research_dossier=dossier,
            claim_ledger=ledger,
        )
        self.assertEqual(ready["closure_status"], "READY")

        packet = compile_blueprint_obligations(
            req,
            governed_manifest,
            registry=reg,
            research_dossier=dossier,
            claim_ledger=ledger,
        )
        self.assertEqual(packet["status"], "BLUEPRINT_OBLIGATIONS_READY")
        self.assertEqual(packet["direct_gate_ids"], ["CHEM-SYNTH-RESEARCH"])


if __name__ == "__main__":
    unittest.main()
