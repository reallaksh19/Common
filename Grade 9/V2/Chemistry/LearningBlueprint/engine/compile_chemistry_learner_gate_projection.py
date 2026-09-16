#!/usr/bin/env python3
"""Project governed Chemistry semantic atoms into learner-facing jobs.

This boundary is topic-neutral and non-pedagogical. It does not author explanations,
examples, prompts, hints, or solutions. It classifies already-governed semantic atoms
into: (1) direct learner jobs, (2) prerequisite/context semantics, or (3) metadata-only
semantics. Source semantic role, polarity, lineage, and mode authority are preserved.
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

from compile_chemistry_semantic_projection import (
    compile_semantic_projection,
    validate_semantic_projection,
)

ROOT = Path(__file__).resolve().parents[1]
POLICY_REL = "policies/chemistry-learner-gate-projection.v1.json"
SCHEMA_REL = "contracts/chemistry-learner-gate-projection.schema.json"
SEMANTIC_POLICY_REL = "policies/chemistry-semantic-projection.v1.json"


class ChemistryLearnerGateProjectionError(ValueError):
    def __init__(self, code: str, message: str = ""):
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code
        self.message = message


def fail(code: str, message: str = "") -> None:
    raise ChemistryLearnerGateProjectionError(code, message)


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


def learner_gate_id(semantic_id: str, learner_job: str, polarity: str) -> str:
    seed = f"{semantic_id}|{learner_job}|{polarity}".encode("utf-8")
    return "CHEM-LG-" + hashlib.sha256(seed).hexdigest()[:24].upper()


def _validate_policy(policy: dict[str, Any]) -> None:
    if policy.get("policy_id") != "CHEM-BLUEPRINT-LEARNER-GATE-PROJECTION-v1":
        fail("CHEM_LEARNER_GATE_POLICY_INVALID", "policy_id")
    if policy.get("subject") != "CHEMISTRY" or policy.get("status") != "ACTIVE":
        fail("CHEM_LEARNER_GATE_POLICY_INVALID", "subject/status")
    rules = policy.get("role_rules")
    if not isinstance(rules, dict) or not rules:
        fail("CHEM_LEARNER_GATE_POLICY_INVALID", "role_rules")

    semantic_policy = load(SEMANTIC_POLICY_REL)
    semantic_roles = set(semantic_policy.get("semantic_roles") or [])
    if set(rules) != semantic_roles:
        missing = sorted(semantic_roles - set(rules))
        extra = sorted(set(rules) - semantic_roles)
        fail("CHEM_LEARNER_GATE_POLICY_ROLE_COVERAGE", f"missing={missing}:extra={extra}")

    allowed_polarities = {"POSITIVE", "NEGATIVE", "CONTEXT"}
    allowed_visibility = {"LEARNER_GATE", "METADATA_ONLY"}
    for role, rule in rules.items():
        if not isinstance(rule, dict):
            fail("CHEM_LEARNER_GATE_POLICY_INVALID", role)
        job = rule.get("learner_job")
        polarity = rule.get("polarity")
        visibility = rule.get("visibility")
        if not isinstance(job, str) or not job:
            fail("CHEM_LEARNER_GATE_POLICY_INVALID", f"{role}:learner_job")
        if polarity not in allowed_polarities or visibility not in allowed_visibility:
            fail("CHEM_LEARNER_GATE_POLICY_INVALID", f"{role}:polarity/visibility")
        if visibility == "METADATA_ONLY" and job != "NONE":
            fail("CHEM_LEARNER_GATE_POLICY_METADATA_JOB_INVALID", role)
        if visibility == "LEARNER_GATE" and job == "NONE":
            fail("CHEM_LEARNER_GATE_POLICY_LEARNER_JOB_MISSING", role)

    if rules["ERROR_TO_AVOID"]["polarity"] != "NEGATIVE":
        fail("CHEM_LEARNER_GATE_POLICY_ERROR_POLARITY_INVALID")
    if rules["MISCONCEPTION"]["polarity"] != "NEGATIVE":
        fail("CHEM_LEARNER_GATE_POLICY_MISCONCEPTION_POLARITY_INVALID")
    if rules["METHOD_STEP"]["polarity"] != "POSITIVE":
        fail("CHEM_LEARNER_GATE_POLICY_METHOD_POLARITY_INVALID")
    if rules["DIFFICULTY_EVIDENCE"]["visibility"] != "METADATA_ONLY":
        fail("CHEM_LEARNER_GATE_POLICY_DIFFICULTY_VISIBILITY_INVALID")


def _gate_from_atom(atom: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    return {
        "learner_gate_id": learner_gate_id(
            atom["semantic_id"], rule["learner_job"], rule["polarity"]
        ),
        "source_semantic_id": atom["semantic_id"],
        "source_gate_id": atom["source_gate_id"],
        "source_obligation_id": atom["source_obligation_id"],
        "source_asset_ref": atom["source_asset_ref"],
        "semantic_role": atom["semantic_role"],
        "learner_job": rule["learner_job"],
        "polarity": rule["polarity"],
        "content": atom["content"],
        "authorized_modes": list(atom["authorized_modes"]),
        "required_realization_modes": list(atom["required_realization_modes"]),
        "source_authority_tier": atom["source_authority_tier"],
        "source_payload_digest": atom["source_payload_digest"],
    }


def compile_learner_gate_projection(
    obligation_packet: dict[str, Any],
    *,
    semantic_projection: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    projection_id: str | None = None,
) -> dict[str, Any]:
    governed_semantics = (
        copy.deepcopy(semantic_projection)
        if semantic_projection is not None
        else compile_semantic_projection(obligation_packet)
    )
    try:
        validate_semantic_projection(obligation_packet, governed_semantics)
    except Exception as exc:
        fail("CHEM_LEARNER_GATE_SEMANTIC_PROJECTION_INVALID", str(exc))

    policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    _validate_policy(policy)
    rules = policy["role_rules"]

    learner_gates: list[dict[str, Any]] = []
    context_semantic_ids: list[str] = []
    metadata_semantic_ids: list[str] = []
    classified_ids: list[str] = []

    for atom in governed_semantics["semantic_atoms"]:
        role = atom["semantic_role"]
        rule = rules.get(role)
        if rule is None:
            fail("CHEM_LEARNER_GATE_SEMANTIC_ROLE_UNMAPPED", role)
        semantic_id = atom["semantic_id"]
        if rule["visibility"] == "METADATA_ONLY":
            metadata_semantic_ids.append(semantic_id)
        elif atom["direct"] is True:
            learner_gates.append(_gate_from_atom(atom, rule))
        else:
            context_semantic_ids.append(semantic_id)
        classified_ids.append(semantic_id)

    source_ids = [row["semantic_id"] for row in governed_semantics["semantic_atoms"]]
    if sorted(classified_ids) != sorted(source_ids) or len(classified_ids) != len(set(classified_ids)):
        fail("CHEM_LEARNER_GATE_SEMANTIC_CLASSIFICATION_DRIFT")
    if not learner_gates:
        fail("CHEM_LEARNER_GATE_EMPTY")

    gate_ids = [row["learner_gate_id"] for row in learner_gates]
    if len(gate_ids) != len(set(gate_ids)):
        fail("CHEM_LEARNER_GATE_ID_COLLISION")
    source_gate_semantic_ids = [row["source_semantic_id"] for row in learner_gates]
    if len(source_gate_semantic_ids) != len(set(source_gate_semantic_ids)):
        fail("CHEM_LEARNER_GATE_SOURCE_SEMANTIC_DUPLICATE")

    resolved_projection_id = projection_id or governed_semantics["projection_id"].replace(
        "CHEM-BP-SEM-", "CHEM-BP-LG-", 1
    )
    learner_job_counts = dict(sorted(Counter(row["learner_job"] for row in learner_gates).items()))
    polarity_counts = dict(sorted(Counter(row["polarity"] for row in learner_gates).items()))
    output = {
        "schema_version": "1.0.0",
        "projection_id": resolved_projection_id,
        "subject": "CHEMISTRY",
        "semantic_projection_id": governed_semantics["projection_id"],
        "semantic_projection_digest": governed_semantics["projection_digest"],
        "policy_ref": POLICY_REL,
        "policy_digest": digest(policy),
        "learner_gates": learner_gates,
        "context_semantic_ids": sorted(context_semantic_ids),
        "metadata_semantic_ids": sorted(metadata_semantic_ids),
        "counts": {
            "source_semantic_atom_count": len(source_ids),
            "learner_gate_count": len(learner_gates),
            "context_semantic_count": len(context_semantic_ids),
            "metadata_semantic_count": len(metadata_semantic_ids),
            "learner_job_counts": learner_job_counts,
            "polarity_counts": polarity_counts,
        },
        "status": "LEARNER_GATE_PROJECTION_READY",
        "projection_digest": "",
    }
    output["projection_digest"] = digest_without(output, "projection_digest")
    try:
        jsonschema.validate(output, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_LEARNER_GATE_SCHEMA", exc.message)
    return output


def validate_learner_gate_projection(
    obligation_packet: dict[str, Any],
    projection: dict[str, Any],
    *,
    semantic_projection: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = copy.deepcopy(policy) if policy is not None else load(POLICY_REL)
    _validate_policy(policy)
    try:
        jsonschema.validate(projection, load(SCHEMA_REL))
    except jsonschema.ValidationError as exc:
        fail("CHEM_LEARNER_GATE_SCHEMA", exc.message)
    if projection.get("projection_digest") != digest_without(projection, "projection_digest"):
        fail("CHEM_LEARNER_GATE_DIGEST_MISMATCH")
    if projection.get("policy_digest") != digest(policy):
        fail("CHEM_LEARNER_GATE_POLICY_DRIFT")

    expected = compile_learner_gate_projection(
        obligation_packet,
        semantic_projection=semantic_projection,
        policy=policy,
        projection_id=projection["projection_id"],
    )
    if canonical(expected) != canonical(projection):
        fail("CHEM_LEARNER_GATE_PROJECTION_DRIFT")
    return {
        "status": "PASS",
        "projection_id": projection["projection_id"],
        "learner_gate_count": projection["counts"]["learner_gate_count"],
        "context_semantic_count": projection["counts"]["context_semantic_count"],
        "metadata_semantic_count": projection["counts"]["metadata_semantic_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("obligation_packet")
    parser.add_argument("--out")
    args = parser.parse_args()
    packet = json.loads(Path(args.obligation_packet).read_text(encoding="utf-8"))
    projection = compile_learner_gate_projection(packet)
    text = json.dumps(projection, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
