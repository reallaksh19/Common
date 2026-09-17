#!/usr/bin/env python3
"""Compile legacy and typed Engineering gate relationships into one governed topology.

Legacy ``prerequisite_ids`` remain authoritative during migration. They are normalized
into typed edges so generic closure code consumes one graph model. Explicit relationships
live in an additive governed sidecar. An exact typed mirror of a legacy prerequisite is
allowed; conflicting or duplicate relationship declarations fail closed.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
POLICY_REL = "policies/chemistry-engineering-gate-topology.v1.json"
EXTENSION_REL = "policies/chemistry-engineering-gate-topology-edges.v1.json"
EXTENSION_SCHEMA_REL = "contracts/chemistry-engineering-gate-topology-extension.schema.json"
SCHEMA_REL = "contracts/chemistry-engineering-gate-topology.schema.json"


class ChemistryEngineeringTopologyError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryEngineeringTopologyError(code, message)


def load(rel: str) -> dict[str, Any]:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def digest_without(obj: dict[str, Any], field: str) -> str:
    value = copy.deepcopy(obj)
    value.pop(field, None)
    return digest(value)


def edge_id(source_gate_id: str, target_id: str, relationship_type: str) -> str:
    seed = f"{source_gate_id}|{relationship_type}|{target_id}".encode("utf-8")
    return "CHEM-EDGE-" + hashlib.sha256(seed).hexdigest()[:24].upper()


def _validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("policy_id") != "CHEM-ENGINEERING-GATE-TOPOLOGY-v1":
        fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", "policy_id")
    if policy.get("subject") != "CHEMISTRY" or policy.get("status") != "ACTIVE":
        fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", "subject/status")
    relationships = policy.get("relationship_types")
    if not isinstance(relationships, dict) or not relationships:
        fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", "relationship_types")
    required_types = {
        "PREREQUISITE",
        "EXTENDS",
        "DECOMPOSES",
        "USES_MODEL_FROM",
        "OPTIONAL_RESEARCH_EXTENSION",
        "CROSS_DOMAIN_PREREQUISITE",
    }
    if set(relationships) != required_types:
        fail(
            "CHEM_ENG_TOPOLOGY_POLICY_RELATIONSHIP_COVERAGE",
            f"missing={sorted(required_types - set(relationships))}:extra={sorted(set(relationships) - required_types)}",
        )
    valid_domains = {"CHEMISTRY_GATE", "EXTERNAL_DEPENDENCY"}
    valid_closure = {"REQUIRED_GATE", "NON_REQUIRED_REFERENCE", "REQUIRED_EXTERNAL_RESOLUTION"}
    valid_learner = {"CONTEXT_ONLY", "NOT_PROMOTED"}
    for relationship_type, rule in relationships.items():
        if rule.get("target_domain") not in valid_domains:
            fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", f"{relationship_type}:target_domain")
        if rule.get("closure_effect") not in valid_closure:
            fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", f"{relationship_type}:closure_effect")
        if rule.get("learner_scope_effect") not in valid_learner:
            fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", f"{relationship_type}:learner_scope_effect")
        if not isinstance(rule.get("cycle_participates"), bool):
            fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", f"{relationship_type}:cycle_participates")
    legacy = policy.get("legacy_prerequisite_mapping") or {}
    if legacy.get("chemistry_gate") != "PREREQUISITE":
        fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", "legacy chemistry mapping")
    if legacy.get("external_dependency") != "CROSS_DOMAIN_PREREQUISITE":
        fail("CHEM_ENG_TOPOLOGY_POLICY_INVALID", "legacy external mapping")


def _validate_extension(extension: dict[str, Any], registry: dict[str, Any]) -> None:
    try:
        jsonschema.validate(extension, load(EXTENSION_SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_ENG_TOPOLOGY_EXTENSION_SCHEMA", exc.message)
    if extension.get("registry_id") != registry.get("registry_id"):
        fail(
            "CHEM_ENG_TOPOLOGY_EXTENSION_REGISTRY_MISMATCH",
            f"extension={extension.get('registry_id')}:registry={registry.get('registry_id')}",
        )


def _edge_row(
    source_gate_id: str,
    target_id: str,
    relationship_type: str,
    origin: str,
    source_order: int,
    policy: dict[str, Any],
    *,
    authority_note: str | None = None,
) -> dict[str, Any]:
    rule = policy["relationship_types"][relationship_type]
    row = {
        "edge_id": edge_id(source_gate_id, target_id, relationship_type),
        "source_gate_id": source_gate_id,
        "target_id": target_id,
        "relationship_type": relationship_type,
        "target_domain": rule["target_domain"],
        "closure_effect": rule["closure_effect"],
        "learner_scope_effect": rule["learner_scope_effect"],
        "cycle_participates": rule["cycle_participates"],
        "origin": origin,
        "source_order": source_order,
    }
    if authority_note:
        row["authority_note"] = authority_note
    return row


def _validate_target(row: dict[str, Any], gate_map: dict[str, dict[str, Any]]) -> None:
    source = row["source_gate_id"]
    target = row["target_id"]
    if row["target_domain"] == "CHEMISTRY_GATE":
        if not target.startswith("CHEM-") or target not in gate_map:
            fail("CHEM_ENG_TOPOLOGY_GATE_TARGET_MISSING", f"{source}->{target}")
        if source == target:
            fail("CHEM_ENG_TOPOLOGY_SELF_EDGE", source)
    else:
        if target.startswith("CHEM-") or target in gate_map:
            fail("CHEM_ENG_TOPOLOGY_EXTERNAL_TARGET_INVALID", f"{source}->{target}")


def _validate_required_cycle(edges: list[dict[str, Any]], gate_ids: list[str]) -> None:
    adjacency: dict[str, list[str]] = {gid: [] for gid in gate_ids}
    for row in edges:
        if row["target_domain"] == "CHEMISTRY_GATE" and row["cycle_participates"]:
            adjacency[row["source_gate_id"]].append(row["target_id"])
    visiting: list[str] = []
    done: set[str] = set()

    def walk(gid: str) -> None:
        if gid in done:
            return
        if gid in visiting:
            index = visiting.index(gid)
            fail("CHEM_ENG_TOPOLOGY_REQUIRED_CYCLE", " -> ".join(visiting[index:] + [gid]))
        visiting.append(gid)
        for target in adjacency[gid]:
            walk(target)
        visiting.pop()
        done.add(gid)

    for gid in gate_ids:
        walk(gid)


def compile_gate_topology(
    registry: dict[str, Any],
    *,
    topology_extension: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    topology_id: str | None = None,
) -> dict[str, Any]:
    policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    extension = copy.deepcopy(topology_extension) if topology_extension is not None else load(EXTENSION_REL)
    _validate_policy(policy)
    _validate_extension(extension, registry)

    gates = registry.get("subtopic_gates")
    if not isinstance(gates, list) or not gates:
        fail("CHEM_ENG_TOPOLOGY_REGISTRY_INVALID", "subtopic_gates")
    gate_ids = [row.get("subtopic_id") for row in gates]
    if any(not isinstance(gid, str) or not gid for gid in gate_ids):
        fail("CHEM_ENG_TOPOLOGY_REGISTRY_INVALID", "subtopic_id")
    if len(gate_ids) != len(set(gate_ids)):
        fail("CHEM_ENG_TOPOLOGY_GATE_DUPLICATE")
    gate_map = {row["subtopic_id"]: row for row in gates}
    gate_order = {gid: index for index, gid in enumerate(gate_ids)}

    merged: dict[tuple[str, str], dict[str, Any]] = {}
    legacy_keys: set[tuple[str, str]] = set()
    explicit_keys: set[tuple[str, str]] = set()
    explicit_exact: set[tuple[str, str, str]] = set()

    legacy_mapping = policy["legacy_prerequisite_mapping"]
    for gate in gates:
        source = gate["subtopic_id"]
        prereqs = list(gate.get("prerequisite_ids") or [])
        if len(prereqs) != len(set(prereqs)):
            fail("CHEM_ENG_TOPOLOGY_LEGACY_DUPLICATE", source)
        for index, target in enumerate(prereqs):
            relationship_type = (
                legacy_mapping["chemistry_gate"]
                if str(target).startswith("CHEM-")
                else legacy_mapping["external_dependency"]
            )
            key = (source, str(target))
            row = _edge_row(source, str(target), relationship_type, "LEGACY_PREREQUISITE", index, policy)
            _validate_target(row, gate_map)
            merged[key] = row
            legacy_keys.add(key)

    explicit_by_source: Counter[str] = Counter()
    for edge in extension["edges"]:
        source = edge["source_gate_id"]
        target = edge["target_id"]
        relationship_type = edge["relationship_type"]
        if source not in gate_map:
            fail("CHEM_ENG_TOPOLOGY_SOURCE_GATE_MISSING", source)
        if relationship_type not in policy["relationship_types"]:
            fail("CHEM_ENG_TOPOLOGY_RELATIONSHIP_UNKNOWN", relationship_type)
        exact = (source, target, relationship_type)
        if exact in explicit_exact:
            fail("CHEM_ENG_TOPOLOGY_DUPLICATE_EXPLICIT_EDGE", "|".join(exact))
        explicit_exact.add(exact)
        key = (source, target)
        current = merged.get(key)
        if current is not None and current["relationship_type"] != relationship_type:
            fail(
                "CHEM_ENG_TOPOLOGY_RELATIONSHIP_CONFLICT",
                f"{source}->{target}:{current['relationship_type']}!={relationship_type}",
            )
        source_order = len(gate_map[source].get("prerequisite_ids") or []) + explicit_by_source[source]
        explicit_by_source[source] += 1
        candidate = _edge_row(
            source,
            target,
            relationship_type,
            "EXPLICIT_TYPED_EDGE",
            source_order,
            policy,
            authority_note=edge["authority_note"],
        )
        _validate_target(candidate, gate_map)
        if current is not None:
            current["origin"] = "LEGACY_AND_EXPLICIT"
            current["authority_note"] = edge["authority_note"]
        else:
            merged[key] = candidate
        explicit_keys.add(key)

    edges = sorted(
        merged.values(),
        key=lambda row: (
            gate_order[row["source_gate_id"]],
            row["source_order"],
            row["target_id"],
            row["relationship_type"],
        ),
    )
    ids = [row["edge_id"] for row in edges]
    if len(ids) != len(set(ids)):
        fail("CHEM_ENG_TOPOLOGY_EDGE_ID_COLLISION")
    _validate_required_cycle(edges, gate_ids)

    resolved_id = topology_id or "CHEM-ENG-TOPOLOGY-" + hashlib.sha256(
        str(registry.get("registry_id", "REGISTRY")).encode("utf-8")
    ).hexdigest()[:16].upper()
    output = {
        "schema_version": "1.0.0",
        "topology_id": resolved_id,
        "subject": "CHEMISTRY",
        "registry_id": str(registry.get("registry_id", "")),
        "registry_digest": digest(registry),
        "policy_ref": POLICY_REL,
        "policy_digest": digest(policy),
        "extension_ref": EXTENSION_REL,
        "extension_id": extension["extension_id"],
        "extension_digest": digest(extension),
        "edges": edges,
        "counts": {
            "edge_count": len(edges),
            "legacy_edge_count": len(legacy_keys),
            "explicit_edge_count": len(explicit_keys),
            "relationship_type_counts": dict(sorted(Counter(row["relationship_type"] for row in edges).items())),
            "closure_effect_counts": dict(sorted(Counter(row["closure_effect"] for row in edges).items())),
        },
        "status": "ENGINEERING_GATE_TOPOLOGY_READY",
        "topology_digest": "",
    }
    output["topology_digest"] = digest_without(output, "topology_digest")
    try:
        jsonschema.validate(output, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_ENG_TOPOLOGY_SCHEMA", exc.message)
    return output


def validate_gate_topology(
    registry: dict[str, Any],
    topology: dict[str, Any],
    *,
    topology_extension: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    extension = copy.deepcopy(topology_extension) if topology_extension is not None else load(EXTENSION_REL)
    _validate_policy(policy)
    _validate_extension(extension, registry)
    try:
        jsonschema.validate(topology, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_ENG_TOPOLOGY_SCHEMA", exc.message)
    if topology.get("topology_digest") != digest_without(topology, "topology_digest"):
        fail("CHEM_ENG_TOPOLOGY_DIGEST_MISMATCH")
    if topology.get("registry_digest") != digest(registry):
        fail("CHEM_ENG_TOPOLOGY_REGISTRY_DRIFT")
    if topology.get("policy_digest") != digest(policy):
        fail("CHEM_ENG_TOPOLOGY_POLICY_DRIFT")
    if topology.get("extension_digest") != digest(extension):
        fail("CHEM_ENG_TOPOLOGY_EXTENSION_DRIFT")
    expected = compile_gate_topology(
        registry,
        topology_extension=extension,
        policy=policy,
        topology_id=topology["topology_id"],
    )
    if canonical(expected) != canonical(topology):
        fail("CHEM_ENG_TOPOLOGY_DRIFT")
    return {
        "status": "PASS",
        "topology_id": topology["topology_id"],
        "edge_count": topology["counts"]["edge_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry")
    parser.add_argument("--extension")
    parser.add_argument("--out")
    args = parser.parse_args()
    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    extension = json.loads(Path(args.extension).read_text(encoding="utf-8")) if args.extension else None
    topology = compile_gate_topology(registry, topology_extension=extension)
    text = json.dumps(topology, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
