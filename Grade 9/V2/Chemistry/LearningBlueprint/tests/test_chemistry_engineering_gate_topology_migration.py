import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
sys.path.insert(0, str(ENGINE))

from compile_chemistry_engineering_gate_topology import (  # noqa: E402
    ChemistryEngineeringTopologyError,
    compile_gate_topology,
    validate_gate_topology,
)

REGISTRY = json.loads((ROOT / "policies/chemistry-technical-engineering-gates.v1.json").read_text(encoding="utf-8"))
PRODUCTION_EXTENSION = json.loads((ROOT / "policies/chemistry-engineering-gate-topology-edges.v1.json").read_text(encoding="utf-8"))


def legacy_exact_edges():
    out = set()
    for gate in REGISTRY["subtopic_gates"]:
        source = gate["subtopic_id"]
        for target in gate.get("prerequisite_ids", []):
            relationship_type = "PREREQUISITE" if target.startswith("CHEM-") else "CROSS_DOMAIN_PREREQUISITE"
            out.add((source, target, relationship_type))
    return out


def explicit_exact_edges(extension):
    return {
        (row["source_gate_id"], row["target_id"], row["relationship_type"])
        for row in extension["edges"]
    }


def legacy_only_extension():
    return {
        "schema_version": "1.0.0",
        "extension_id": "CHEM-ENG-TOPOLOGY-EXT-legacy-only-test-v1",
        "subject": "CHEMISTRY",
        "registry_id": REGISTRY["registry_id"],
        "additive_only": True,
        "legacy_coverage": "ALLOW_PARTIAL",
        "edges": [],
    }


def semantic_edge_signature(topology):
    return [
        (
            row["source_gate_id"],
            row["target_id"],
            row["relationship_type"],
            row["target_domain"],
            row["closure_effect"],
            row["learner_scope_effect"],
            row["cycle_participates"],
            row["source_order"],
        )
        for row in topology["edges"]
    ]


class ChemistryEngineeringGateTopologyMigrationTests(unittest.TestCase):
    def test_production_sidecar_covers_every_legacy_relationship_exactly(self):
        expected = legacy_exact_edges()
        actual = explicit_exact_edges(PRODUCTION_EXTENSION)
        self.assertEqual(PRODUCTION_EXTENSION["legacy_coverage"], "REQUIRE_ALL_LEGACY_MIRRORS")
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 60)

        topology = compile_gate_topology(REGISTRY)
        self.assertEqual(validate_gate_topology(REGISTRY, topology)["status"], "PASS")
        self.assertEqual(topology["counts"]["legacy_edge_count"], len(expected))
        self.assertEqual(topology["counts"]["explicit_edge_count"], len(expected))
        self.assertTrue(all(row["origin"] == "LEGACY_AND_EXPLICIT" for row in topology["edges"]))

    def test_typed_migration_preserves_legacy_graph_semantics_and_order(self):
        legacy = compile_gate_topology(REGISTRY, topology_extension=legacy_only_extension())
        migrated = compile_gate_topology(REGISTRY)
        self.assertEqual(semantic_edge_signature(migrated), semantic_edge_signature(legacy))
        self.assertEqual(migrated["counts"]["relationship_type_counts"], legacy["counts"]["relationship_type_counts"])
        self.assertEqual(migrated["counts"]["closure_effect_counts"], legacy["counts"]["closure_effect_counts"])

    def test_full_coverage_mode_fails_closed_when_one_legacy_mirror_is_removed(self):
        missing = copy.deepcopy(PRODUCTION_EXTENSION)
        removed = missing["edges"].pop(0)
        with self.assertRaises(ChemistryEngineeringTopologyError) as ctx:
            compile_gate_topology(REGISTRY, topology_extension=missing)
        self.assertEqual(ctx.exception.code, "CHEM_ENG_TOPOLOGY_LEGACY_COVERAGE_MISSING")
        self.assertIn(removed["source_gate_id"], ctx.exception.message)
        self.assertIn(removed["target_id"], ctx.exception.message)

    def test_allow_partial_mode_remains_available_for_synthetic_extensions(self):
        partial = legacy_only_extension()
        topology = compile_gate_topology(REGISTRY, topology_extension=partial)
        self.assertEqual(topology["counts"]["explicit_edge_count"], 0)
        self.assertEqual(topology["counts"]["legacy_edge_count"], 60)


if __name__ == "__main__":
    unittest.main()
