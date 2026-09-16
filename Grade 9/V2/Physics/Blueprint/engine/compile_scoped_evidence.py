#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = ROOT.parents[3]
CURRICULUM_BINDING_REGISTRY_REF = "registry/physics-curriculum-scope-bindings.v1.json"


class ScopedEvidenceError(Exception):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def repo_path(rel: str) -> Path:
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_REF_OUTSIDE_REPOSITORY")
    path = REPO / p
    if not path.exists() or not path.is_file():
        raise ScopedEvidenceError("SCOPED_EVIDENCE_REF_MISSING:" + rel)
    return path


def load_repo_json(rel: str) -> dict[str, Any]:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))


def validate_schema(name: str, value: dict[str, Any]) -> None:
    Draft202012Validator(load_schema(name)).validate(value)


def _verify_assertions(envelope: dict[str, Any]) -> None:
    for row in envelope["repository_assertions"]:
        text = repo_path(row["path"]).read_text(encoding="utf-8")
        missing = [needle for needle in row["contains_all"] if needle not in text]
        if missing:
            raise ScopedEvidenceError("SCOPED_EVIDENCE_ASSERTION_FAILED:" + row["path"] + ":" + ",".join(missing))


def _metric(value: int, basis: str) -> dict[str, Any]:
    return {"value": int(value), "basis": basis}


def _load_curriculum_binding_registry() -> dict[str, Any]:
    registry = json.loads((ROOT / CURRICULUM_BINDING_REGISTRY_REF).read_text(encoding="utf-8"))
    validate_schema("physics-curriculum-scope-binding-registry.schema.json", registry)
    ids = [row["binding_id"] for row in registry["bindings"]]
    if len(ids) != len(set(ids)):
        raise ScopedEvidenceError("SCOPED_EVIDENCE_DUPLICATE_CURRICULUM_BINDING_ID")
    return registry


def _load_curriculum_authority_record(ref: str) -> dict[str, Any]:
    try:
        record = load_repo_json(ref)
        validate_schema("physics-curriculum-authority-record.schema.json", record)
    except (json.JSONDecodeError, ValidationError, KeyError, TypeError) as exc:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_CURRICULUM_AUTHORITY_RECORD_INVALID:" + ref) from exc
    return record


def _validate_authority_record_for_binding(record: dict[str, Any], binding: dict[str, Any], ref: str) -> None:
    if int(record["grade"]) != int(binding["grade"]) or record["curriculum"] != binding["curriculum"]:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_CURRICULUM_AUTHORITY_IDENTITY_MISMATCH:" + ref)

    source_roles = {row["source_role"] for row in record["evidence_sources"]}
    if "CONTENT_SYLLABUS" not in source_roles or not source_roles.intersection({"CURRICULUM_INDEX", "RELEASE_NOTICE"}):
        raise ScopedEvidenceError("SCOPED_EVIDENCE_CURRICULUM_AUTHORITY_SOURCE_ROLE_INCOMPLETE:" + ref)

    assertions = [
        row
        for row in record["scope_assertions"]
        if row["scope_kind"] == binding["scope_kind"]
        and row["scope_ref"] == binding["scope_ref"]
        and row["classification"] == binding["classification"]
        and set(row["supported_gate_ids"]) == set(binding["required_gate_ids"])
    ]
    if len(assertions) != 1:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_CURRICULUM_AUTHORITY_SCOPE_MISMATCH:" + ref)


def resolve_curriculum_binding(envelope: dict[str, Any], registry: dict[str, Any] | None = None) -> dict[str, Any]:
    requested = envelope["requested_curriculum"]
    if requested == "REPOSITORY_GOVERNED_PHYSICS":
        return {
            "state": "REPOSITORY_INTERNAL_SCOPE",
            "binding_id": None,
            "binding_digest": None,
            "classification": None,
            "authority_refs": [],
            "registry_ref": CURRICULUM_BINDING_REGISTRY_REF,
            "registry_digest": None,
        }

    registry = copy.deepcopy(registry) if registry is not None else _load_curriculum_binding_registry()
    validate_schema("physics-curriculum-scope-binding-registry.schema.json", registry)
    matches = [
        row
        for row in registry["bindings"]
        if int(row["grade"]) == int(envelope["grade"])
        and row["curriculum"] == requested
        and row["scope_kind"] == envelope["scope_kind"]
        and row["scope_ref"] == envelope["scope_ref"]
        and set(row["required_gate_ids"]) == set(envelope["required_gate_ids"])
        and row["state"] == "CONFIRMED"
    ]
    if len(matches) > 1:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_AMBIGUOUS_CURRICULUM_BINDING")
    registry_digest = digest(registry)
    if not matches:
        return {
            "state": "UNBOUND",
            "binding_id": None,
            "binding_digest": None,
            "classification": None,
            "authority_refs": [],
            "registry_ref": CURRICULUM_BINDING_REGISTRY_REF,
            "registry_digest": registry_digest,
        }

    binding = matches[0]
    binding_refs = list(binding["authority_refs"])
    if set(binding_refs) != set(envelope["curriculum_authority_refs"]):
        raise ScopedEvidenceError("SCOPED_EVIDENCE_CURRICULUM_BINDING_REF_MISMATCH")
    for ref in binding_refs:
        record = _load_curriculum_authority_record(ref)
        _validate_authority_record_for_binding(record, binding, ref)
    return {
        "state": "BOUND_CONFIRMED",
        "binding_id": binding["binding_id"],
        "binding_digest": digest(binding),
        "classification": binding["classification"],
        "authority_refs": binding_refs,
        "registry_ref": CURRICULUM_BINDING_REGISTRY_REF,
        "registry_digest": registry_digest,
    }


def compile_scoped_evidence(envelope: dict[str, Any]) -> dict[str, Any]:
    validate_schema("scoped-execution-envelope.schema.json", envelope)
    _verify_assertions(envelope)
    topic = load_repo_json(envelope["topic_blueprint_ref"])
    if topic.get("topic_id") != envelope["topic_id"]:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_TOPIC_MISMATCH")
    if int(topic.get("grade")) != int(envelope["grade"]):
        raise ScopedEvidenceError("SCOPED_EVIDENCE_GRADE_MISMATCH")
    for ref in envelope["semantic_evidence_refs"] + envelope["curriculum_authority_refs"] + envelope["assessment_coverage"]["evidence_refs"]:
        repo_path(ref)

    curriculum_binding = resolve_curriculum_binding(envelope)
    corpus_path = repo_path(envelope["assessment_corpus_ref"])
    coverage = envelope["assessment_coverage"]
    state = coverage["state"]
    matched = int(coverage["matched_target_item_count"])
    issues = list(coverage.get("unresolved_issues") or [])
    if state == "VERIFIED_NO_TARGET_DEMAND" and matched != 0:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_ZERO_DEMAND_COUNT_MISMATCH")
    if state == "DEMANDS_PRESENT" and matched < 1:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_PRESENT_DEMAND_COUNT_REQUIRED")
    if state == "COVERAGE_UNKNOWN" and not issues:
        raise ScopedEvidenceError("SCOPED_EVIDENCE_UNKNOWN_REQUIRES_ISSUE")

    parent = copy.deepcopy(topic["evidence"])
    evidence = copy.deepcopy(parent)
    evidence["ground_truth_refs"] = list(
        dict.fromkeys(
            [envelope["topic_blueprint_ref"], envelope["assessment_corpus_ref"]]
            + envelope["semantic_evidence_refs"]
            + coverage["evidence_refs"]
            + curriculum_binding["authority_refs"]
        )
    )
    pm = parent["metrics"]
    ps = parent["sources"]
    has_semantic = bool(envelope["semantic_evidence_refs"])
    if has_semantic:
        evidence["sources"]["semantic_source"] = copy.deepcopy(ps["semantic_source"])
        evidence["sources"]["semantic_source"]["notes"] = list(evidence["sources"]["semantic_source"].get("notes") or []) + [
            "Scoped semantic evidence is bound to exact repository refs for this execution envelope."
        ]
        ss = int(pm["SS"]["value"])
    else:
        evidence["sources"]["semantic_source"] = {
            "availability": "ABSENT",
            "authority_strength": 0,
            "granularity": "NONE",
            "integrity_state": "NOT_APPLICABLE",
            "notes": ["No target-scoped semantic evidence refs were supplied."],
        }
        ss = 0

    if state == "VERIFIED_NO_TARGET_DEMAND":
        evidence["sources"]["question_corpus"] = {
            "availability": "ABSENT",
            "authority_strength": 0,
            "granularity": "DETAILED",
            "count": 0,
            "integrity_state": "NOT_APPLICABLE",
            "notes": ["Target-scoped corpus audit verified zero matching demand items; topic-wide question richness is not inherited."],
        }
        evidence["sources"]["answer_key"] = {
            "availability": "ABSENT",
            "authority_strength": 0,
            "granularity": "NONE",
            "count": 0,
            "integrity_state": "NOT_APPLICABLE",
            "notes": ["No target demand item exists, so no target answer-key demand is projected."],
        }
        qe = qr = 0
        ua = int(pm["UA"]["value"])
    elif state == "DEMANDS_PRESENT":
        evidence["sources"]["question_corpus"] = copy.deepcopy(ps["question_corpus"])
        evidence["sources"]["question_corpus"]["count"] = matched
        evidence["sources"]["answer_key"] = copy.deepcopy(ps["answer_key"])
        qe = int(pm["QE"]["value"])
        qr = int(pm["QR"]["value"])
        ua = int(pm["UA"]["value"])
    else:
        evidence["sources"]["question_corpus"] = {
            "availability": "PARTIAL",
            "authority_strength": 0,
            "granularity": "NONE",
            "count": matched,
            "integrity_state": "AMBIGUOUS",
            "notes": issues,
        }
        evidence["sources"]["answer_key"] = {
            "availability": "PARTIAL",
            "authority_strength": 0,
            "granularity": "NONE",
            "integrity_state": "AMBIGUOUS",
            "notes": issues,
        }
        qe = qr = 0
        ua = max(3, int(pm["UA"]["value"]))

    evidence["metrics"] = {
        "SA": _metric(int(pm["SA"]["value"]), "Scope authority cannot be strengthened by narrowing; inherited as the parent-topic ceiling."),
        "SS": _metric(ss, "Semantic strength is inherited only when exact target-scoped semantic evidence refs exist."),
        "QE": _metric(qe, "Question evidence is target-scoped; verified zero target demand forces QE=0."),
        "QR": _metric(qr, "Demand resolution is target-scoped; verified zero target demand forces QR=0."),
        "UA": _metric(ua, "Unknown target coverage raises uncertainty; otherwise parent uncertainty is retained."),
        "CI": _metric(int(pm["CI"]["value"]), "Conflict severity is not reduced by scope projection without a separate adjudication."),
    }
    validate_schema("evidence-state.schema.json", evidence)

    scope_descriptor = {
        "subject": envelope["subject"],
        "grade": envelope["grade"],
        "scope_kind": envelope["scope_kind"],
        "topic_id": envelope["topic_id"],
        "scope_ref": envelope["scope_ref"],
        "requested_curriculum": envelope["requested_curriculum"],
        "required_gate_ids": envelope["required_gate_ids"],
    }
    scope_digest = digest(scope_descriptor)
    assessment_coverage = {
        "state": state,
        "matched_target_item_count": matched,
        "scope_digest": scope_digest,
        "corpus_digest": file_digest(corpus_path),
        "evidence_refs": list(coverage["evidence_refs"]),
        "unresolved_issues": issues,
    }
    curriculum_status = (
        "SUPPORTED_BY_REPOSITORY_AUTHORITY"
        if curriculum_binding["state"] in {"BOUND_CONFIRMED", "REPOSITORY_INTERNAL_SCOPE"}
        else "HELD_INSUFFICIENT_AUTHORITY"
    )
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": envelope["envelope_id"].replace("SCOPE-PHY-", "SCOPED-EVIDENCE-PHY-", 1),
        "derivation": "SCOPED_EVIDENCE_COMPILER_V1",
        "scope_kind": envelope["scope_kind"],
        "scope_ref": envelope["scope_ref"],
        "topic_id": envelope["topic_id"],
        "grade": envelope["grade"],
        "requested_curriculum": envelope["requested_curriculum"],
        "curriculum_status": curriculum_status,
        "curriculum_binding": curriculum_binding,
        "required_gate_ids": list(envelope["required_gate_ids"]),
        "parent_topic_blueprint_ref": envelope["topic_blueprint_ref"],
        "parent_topic_blueprint_digest": str(topic["topic_blueprint_digest"]),
        "scope_digest": scope_digest,
        "assessment_coverage": assessment_coverage,
        "evidence": evidence,
        "evidence_digest": digest(evidence),
        "repository_assertion_count": len(envelope["repository_assertions"]),
        "receipt_digest": "",
    }
    receipt["receipt_digest"] = digest({k: v for k, v in receipt.items() if k != "receipt_digest"})
    validate_schema("scoped-evidence-receipt.schema.json", receipt)
    return receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("envelope", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    result = compile_scoped_evidence(json.loads(a.envelope.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    a.out.write_text(text, encoding="utf-8") if a.out else print(text, end="")


if __name__ == "__main__":
    main()
