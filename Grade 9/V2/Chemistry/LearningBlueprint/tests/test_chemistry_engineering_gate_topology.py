import copy
import inspect
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_blueprint_obligations import compile_blueprint_obligations  # noqa: E402
from compile_chemistry_engineering_authorization_binding import compile_binding  # noqa: E402
from compile_chemistry_engineering_closure import (  # noqa: E402
    ChemistryEngineeringClosureError,
    compile_closure,
)
from compile_chemistry_engineering_gate_topology import (  # noqa: E402
    ChemistryEngineeringTopologyError,
    compile_gate_topology,
    validate_gate_topology,
)
from compile_chemistry_learner_gate_projection import compile_learner_gate_projection  # noqa: E402
from compile_chemistry_semantic_projection import compile_semantic_projection  # noqa: E402

REGISTRY = json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))
BINDING_SCHEMA = json.loads((ROOT / "contracts/chemistry-engineering-authorization-binding.schema.json").read_text(encoding="utf-8"))
PACKET_SCHEMA = json.loads((ROOT / "contracts/chemistry-engineering-blueprint-obligations.schema.json").read_text(encoding="utf-8"))
TOPOLOGY_FIELDS = (
    "topology_id",
    "topology_digest",
    "topology_extension_id",
    "topology_extension_digest",
)


def extension(registry, edges, extension_id="CHEM-ENG-TOPOLOGY-EXT-synthetic-v1"):
    return {
        "schema_version": "1.0.0",
        "extension_id": extension_id,
        "subject": "CHEMISTRY",
        "registry_id": registry["registry_id"],
        "additive_only": True,
        "edges": copy.deepcopy(edges),
    }


def edge(source, target, relationship_type):
    return {
        "source_gate_id": source,
        "target_id": target,
        "relationship_type": relationship_type,
        "authority_note": "Synthetic topology falsifier; no topic-specific authority.",
    }


def stripped_registry():
    registry = copy.deepcopy(REGISTRY)
    for gate in registry["subtopic_gates"]:
        gate["prerequisite_ids"] = []
    return registry


def ready_pair(registry):
    ready = [
        gate["subtopic_id"]
        for gate in registry["subtopic_gates"]
        if gate["technical_readiness"] == "ENGINEERING_GATE_READY"
    ]
    if len(ready) < 2:
        raise AssertionError("topology falsifier requires at least two ready gates")
    return ready[0], ready[1]


def legacy_internal_pair():
    gate_ids = {gate["subtopic_id"] for gate in REGISTRY["subtopic_gates"]}
    for gate in REGISTRY["subtopic_gates"]:
        for target in gate.get("prerequisite_ids", []):
            if target.startswith("CHEM-") and target in gate_ids:
                return gate["subtopic_id"], target
    raise AssertionError("registry must contain at least one internal legacy prerequisite")


def request():
    return {
        "schema_version": "2.0.0",
        "request_id": "CHEM-ENG-REQ-TOPOLOGY-TEST",
        "subject": "CHEMISTRY",
        "requested_topic": "Synthetic topology contract test",
        "requested_scope": "Generic typed relationship semantics only",
        "engineering_depth": "STANDARD",
        "requested_action": "DECLARE_DIRECT_GATES",
        "requested_for": ["CORE1A"],
    }


def manifest(required, *, optional=None, out_of_scope=None, resolutions=None):
    return {
        "schema_version": "2.0.0",
        "manifest_id": "CHEM-ENG-MAN-TOPOLOGY-TEST",
        "request_id": "CHEM-ENG-REQ-TOPOLOGY-TEST",
        "scope_kind": "TOPIC",
        "scope_ref": "TOPOLOGY-TEST",
        "topic_id": "CHEM-TOPOLOGY-TEST",
        "title": "Synthetic topology contract test",
        "registry_ref": "policies/chemistry-technical-engineering-gates.v1.json",
        "required_gate_ids": list(required),
        "optional_gate_ids": list(optional or []),
        "out_of_scope_gate_ids": list(out_of_scope or []),
        "source_audits": [],
        "external_prerequisite_resolutions": list(resolutions or []),
        "source_item_status": "INDEPENDENT_OF_TECHNICAL_GATE",
        "downstream_consumers": ["PAL"],
    }


class ChemistryEngineeringGateTopologyTests(unittest.TestCase):
    def test_legacy_prerequisites_normalize_without_changing_closure_contract(self):
        topology = compile_gate_topology(REGISTRY)
        self.assertEqual(topology["counts"]["explicit_edge_count"], 0)
        self.assertEqual(validate_gate_topology(REGISTRY, topology)["status"], "PASS")
        by_pair = {(row["source_gate_id"], row["target_id"]): row for row in topology["edges"]}
        expected_count = 0
        for gate in REGISTRY["subtopic_gates"]:
            for target in gate.get("prerequisite_ids", []):
                expected_count += 1
                row = by_pair[(gate["subtopic_id"], target)]
                expected_type = "PREREQUISITE" if target.startswith("CHEM-") else "CROSS_DOMAIN_PREREQUISITE"
                self.assertEqual(row["relationship_type"], expected_type)
                self.assertEqual(row["origin"], "LEGACY_PREREQUISITE")
        self.assertEqual(topology["counts"]["edge_count"], expected_count)

        source, _ = ready_pair(stripped_registry())
        legacy = compile_closure(request(), manifest([source]), registry=stripped_registry(), topology_extension=extension(stripped_registry(), []))
        implicit = compile_closure(request(), manifest([source]), registry=stripped_registry(), topology_extension=None)
        self.assertEqual(legacy, implicit)
        self.assertFalse(any(field in legacy for field in TOPOLOGY_FIELDS))

    def test_exact_legacy_mirror_is_allowed_but_relationship_reclassification_fails(self):
        source, target = legacy_internal_pair()
        mirrored = compile_gate_topology(
            REGISTRY,
            topology_extension=extension(REGISTRY, [edge(source, target, "PREREQUISITE")]),
        )
        row = next(row for row in mirrored["edges"] if row["source_gate_id"] == source and row["target_id"] == target)
        self.assertEqual(row["origin"], "LEGACY_AND_EXPLICIT")
        self.assertEqual(row["relationship_type"], "PREREQUISITE")

        with self.assertRaises(ChemistryEngineeringTopologyError) as ctx:
            compile_gate_topology(
                REGISTRY,
                topology_extension=extension(REGISTRY, [edge(source, target, "EXTENDS")]),
            )
        self.assertEqual(ctx.exception.code, "CHEM_ENG_TOPOLOGY_RELATIONSHIP_CONFLICT")

    def test_duplicate_explicit_edge_and_required_cycle_fail_closed(self):
        registry = stripped_registry()
        source, target = ready_pair(registry)
        duplicate = [edge(source, target, "EXTENDS"), edge(source, target, "EXTENDS")]
        with self.assertRaises(ChemistryEngineeringTopologyError) as ctx:
            compile_gate_topology(registry, topology_extension=extension(registry, duplicate))
        self.assertEqual(ctx.exception.code, "CHEM_ENG_TOPOLOGY_DUPLICATE_EXPLICIT_EDGE")

        cycle = [edge(source, target, "EXTENDS"), edge(target, source, "USES_MODEL_FROM")]
        with self.assertRaises(ChemistryEngineeringTopologyError) as ctx:
            compile_gate_topology(registry, topology_extension=extension(registry, cycle))
        self.assertEqual(ctx.exception.code, "CHEM_ENG_TOPOLOGY_REQUIRED_CYCLE")

        non_cycle = [edge(source, target, "EXTENDS"), edge(target, source, "OPTIONAL_RESEARCH_EXTENSION")]
        topology = compile_gate_topology(registry, topology_extension=extension(registry, non_cycle))
        self.assertEqual(topology["status"], "ENGINEERING_GATE_TOPOLOGY_READY")

    def test_all_required_internal_relationship_types_enter_closure_as_context(self):
        for relationship_type in ("PREREQUISITE", "EXTENDS", "DECOMPOSES", "USES_MODEL_FROM"):
            with self.subTest(relationship_type=relationship_type):
                registry = stripped_registry()
                source, target = ready_pair(registry)
                relationship_slug = relationship_type.replace("_", "-")
                ext = extension(registry, [edge(source, target, relationship_type)], extension_id=f"CHEM-ENG-TOPOLOGY-EXT-{relationship_slug}-v1")
                receipt = compile_closure(request(), manifest([source]), registry=registry, topology_extension=ext)
                self.assertEqual(receipt["closure_status"], "READY")
                self.assertIn(target, receipt["closure_gate_ids"])
                for field in TOPOLOGY_FIELDS:
                    self.assertIn(field, receipt)

                binding = compile_binding(request(), manifest([source]), registry=registry, topology_extension=ext)
                packet = compile_blueprint_obligations(request(), manifest([source]), registry=registry, topology_extension=ext)
                for field in TOPOLOGY_FIELDS:
                    self.assertEqual(binding[field], receipt[field])
                    self.assertEqual(packet[field], receipt[field])

                target_obligations = [row for row in packet["obligations"] if row["gate_id"] == target]
                self.assertTrue(target_obligations)
                self.assertTrue(all(row["direct"] is False for row in target_obligations))
                self.assertTrue(all(row["required_realization_modes"] == [] for row in target_obligations))

                semantic = compile_semantic_projection(packet)
                learner = compile_learner_gate_projection(packet, semantic_projection=semantic)
                target_atoms = [row for row in semantic["semantic_atoms"] if row["source_gate_id"] == target]
                self.assertTrue(target_atoms)
                self.assertFalse(any(row["source_gate_id"] == target for row in learner["learner_gates"]))
                classified = set(learner["context_semantic_ids"]) | set(learner["metadata_semantic_ids"])
                self.assertTrue({row["semantic_id"] for row in target_atoms}.issubset(classified))

                broken_binding = copy.deepcopy(binding)
                broken_binding.pop("topology_digest")
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(broken_binding, BINDING_SCHEMA)
                broken_packet = copy.deepcopy(packet)
                broken_packet.pop("topology_extension_digest")
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(broken_packet, PACKET_SCHEMA)

    def test_optional_research_extension_never_enters_required_closure(self):
        registry = stripped_registry()
        source, target = ready_pair(registry)
        ext = extension(registry, [edge(source, target, "OPTIONAL_RESEARCH_EXTENSION")])
        receipt = compile_closure(request(), manifest([source]), registry=registry, topology_extension=ext)
        self.assertEqual(receipt["closure_status"], "READY")
        self.assertNotIn(target, receipt["closure_gate_ids"])
        self.assertIn("topology_id", receipt)
        packet = compile_blueprint_obligations(request(), manifest([source]), registry=registry, topology_extension=ext)
        self.assertFalse(any(row["gate_id"] == target for row in packet["obligations"]))

    def test_cross_domain_prerequisite_requires_explicit_resolution(self):
        registry = stripped_registry()
        source, _ = ready_pair(registry)
        dependency = "PHYS-SYNTHETIC-MODEL"
        ext = extension(registry, [edge(source, dependency, "CROSS_DOMAIN_PREREQUISITE")])
        blocked = compile_closure(request(), manifest([source]), registry=registry, topology_extension=ext)
        self.assertEqual(blocked["closure_status"], "BLOCKED")
        self.assertIn("CHEM_ENG_EXTERNAL_PREREQ_UNRESOLVED", {row["code"] for row in blocked["blockers"]})

        resolved = compile_closure(
            request(),
            manifest(
                [source],
                resolutions=[{
                    "dependency_id": dependency,
                    "status": "RESOLVED_BY_AUTHORITY",
                    "evidence_ref": "SYNTHETIC_TEST_ONLY",
                }],
            ),
            registry=registry,
            topology_extension=ext,
        )
        self.assertEqual(resolved["closure_status"], "READY")
        state = next(row for row in resolved["external_dependency_states"] if row["dependency_id"] == dependency)
        self.assertEqual(state["status"], "RESOLVED_BY_AUTHORITY")

    def test_required_typed_edge_cannot_smuggle_optional_or_out_of_scope_gate_into_closure(self):
        registry = stripped_registry()
        source, target = ready_pair(registry)
        ext = extension(registry, [edge(source, target, "EXTENDS")])
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(request(), manifest([source], optional=[target]), registry=registry, topology_extension=ext)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_OPTIONAL_GATE_REQUIRED_BY_CLOSURE")
        with self.assertRaises(ChemistryEngineeringClosureError) as ctx:
            compile_closure(request(), manifest([source], out_of_scope=[target]), registry=registry, topology_extension=ext)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_REQUIRED_DEPENDENCY_OUT_OF_SCOPE")

    def test_generic_topology_compiler_contains_no_topic_control_flow(self):
        source = inspect.getsource(__import__("compile_chemistry_engineering_gate_topology")).lower()
        for forbidden in ("re" + "dox", "thermo" + "dynamics", "perman" + "ganate", "mn" + "o4"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
