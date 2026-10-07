from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from typing import Any, Mapping

MODULE_DIR = Path(__file__).resolve().parent


def _load_sibling(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, MODULE_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"cannot load {filename}")
    spec.loader.exec_module(module)
    return module


DELP = _load_sibling("delp_projection_v35_for_assembler", "delp_projection_v35.py")
CLASSIFIER = _load_sibling("decomposition_classifier_v35_for_assembler", "decomposition_classifier_v35.py")
OBSERVER = _load_sibling("decomposition_observer_v35_for_assembler", "decomposition_observer_v35.py")

AUTHORITY = "DERIVED_TOPOLOGY_ADMISSION_ONLY"
RELEASE_FINDINGS_AUTHORITY = "DERIVED_TOPOLOGY_RELEASE_FINDINGS"
DECISION_BLOCKERS = {
    "SPLIT": "TOPOLOGY_SPLIT_REQUIRED",
    "MERGE": "TOPOLOGY_MERGE_REQUIRED",
    "DISCOVER_FIRST": "TOPOLOGY_DISCOVERY_REQUIRED",
    "REPLAN": "TOPOLOGY_REPLAN_REQUIRED",
}


class AssemblyError(ValueError):
    """Canonical topology basis and observations cannot be assembled safely."""


def _stable_id_to_ref(indexed: Mapping[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for ref in indexed["order"]:
        node = indexed["nodes"][ref]
        if node["kind"] != "LEAF":
            continue
        rid = node.get("responsibility_id")
        if rid:
            result[str(rid)] = ref
    return result


def assemble_topology_admission(
    graph: Mapping[str, Any],
    *,
    assessment_id: str,
    observations: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Assemble one current assessment and classify it without changing admission/progress."""
    if not isinstance(graph, Mapping):
        raise AssemblyError("graph must be a mapping")
    if observations is None:
        observations = {}
    if not isinstance(observations, Mapping):
        raise AssemblyError("observations must be a mapping keyed by leaf ref")

    try:
        indexed = DELP.validate_graph(graph)
    except Exception as exc:
        raise AssemblyError(f"invalid execution graph: {exc}") from exc

    basis = indexed["topology_assessments_by_id"].get(assessment_id)
    if basis is None:
        raise AssemblyError(f"unknown topology assessment {assessment_id!r}")

    id_to_ref = _stable_id_to_ref(indexed)
    currentness_rows: list[dict[str, Any]] = []
    current_cross_cutting = False

    for responsibility_id in basis["responsibility_ids"]:
        ref = id_to_ref.get(responsibility_id)
        if ref is None:  # validate_graph should already make this impossible.
            raise AssemblyError(f"missing current leaf for Responsibility {responsibility_id!r}")
        observation = observations.get(ref)
        try:
            current = OBSERVER.repository_observation_currentness(graph, ref, observation)
        except Exception as exc:
            raise AssemblyError(f"{responsibility_id}: invalid repository observation: {exc}") from exc

        if current["state"] == "CURRENT":
            impact = observation.get("change_impact") if isinstance(observation, Mapping) else None
            if impact not in OBSERVER.CHANGE_IMPACTS:
                raise AssemblyError(
                    f"{responsibility_id}: current observation change_impact must be one of "
                    f"{list(OBSERVER.CHANGE_IMPACTS)}"
                )
            if impact == "CROSS_CUTTING":
                current_cross_cutting = True

        currentness_rows.append(
            {
                "responsibility_id": responsibility_id,
                "ref": ref,
                **current,
            }
        )

    currentness_rows.sort(key=lambda row: row["responsibility_id"])
    states = {row["state"] for row in currentness_rows}
    basis_moved = "MOVED" in states

    claim_report = DELP.claim_topology_report(graph)
    claim_summary = claim_report["summary"]
    claim_blockers: list[str] = []
    if claim_summary["claims"] == 0:
        claim_blockers.append("CLAIMS_ABSENT")
    if claim_summary["uncovered_claims"]:
        claim_blockers.append("UNCOVERED_CLAIMS")
    if claim_summary["orphan_responsibilities"]:
        claim_blockers.append("ORPHAN_RESPONSIBILITIES")
    if claim_summary["duplicate_nonshared_ownership"]:
        claim_blockers.append("DUPLICATE_NONSHARED_OWNERSHIP")

    if "MISSING" in states:
        change_impact = "UNKNOWN"
    elif current_cross_cutting:
        change_impact = "CROSS_CUTTING"
    else:
        change_impact = basis["change_impact"]

    assessment = {
        "schema": CLASSIFIER.DECOMPOSITION_ASSESSMENT_SCHEMA,
        "subject": assessment_id,
        "proposal_kind": basis["proposal_kind"],
        "semantic_cohesion": basis["semantic_cohesion"],
        "dependency_closure": basis["dependency_closure"],
        "verification_closure": basis["verification_closure"],
        "uncertainty": "BLOCKING" if claim_blockers else basis["uncertainty"],
        "change_impact": change_impact,
        "execution_horizon": basis["execution_horizon"],
        "mutation_domains": list(basis["mutation_domains"]),
        "recovery_radius": basis["recovery_radius"],
        "handoff_cost": basis["handoff_cost"],
        "cross_child_cohesion": basis["cross_child_cohesion"],
        "stable_cut": copy.deepcopy(basis["stable_cut"]),
        "basis_moved": basis_moved,
    }
    errors = CLASSIFIER.validate_decomposition_assessment(assessment)
    if errors:
        raise AssemblyError("derived assessment is invalid: " + "; ".join(errors))
    decision = CLASSIFIER.classify_decomposition_assessment(assessment)

    return {
        "authority": AUTHORITY,
        "topology_assessment_id": assessment_id,
        "graph_digest": indexed["digest"],
        "responsibility_ids": list(basis["responsibility_ids"]),
        "source_refs": list(basis["source_refs"]),
        "claim_topology": {
            "summary": copy.deepcopy(claim_summary),
            "blockers": claim_blockers,
        },
        "repository_currentness": currentness_rows,
        "assessment": assessment,
        "decision": decision,
    }


def topology_release_findings(
    graph: Mapping[str, Any],
    *,
    observations: Mapping[str, Mapping[str, Any]] | None = None,
    closed: set[str] | frozenset[str] | None = None,
) -> dict[str, Any]:
    """Pure per-leaf release findings from canonical R2 topology admissions.

    This function does not alter DELP projection/admission. It only translates
    existing R2 decisions into deterministic blocker-shaped facts for R3.
    """
    if observations is None:
        observations = {}
    if not isinstance(observations, Mapping):
        raise AssemblyError("observations must be a mapping keyed by leaf ref")
    closed_refs = set(closed or ())
    try:
        indexed = DELP.validate_graph(graph)
    except Exception as exc:
        raise AssemblyError(f"invalid execution graph: {exc}") from exc

    claim_first_active = bool(
        indexed.get("acceptance_claims") or indexed.get("topology_assessments")
    )
    if not claim_first_active:
        return {
            "authority": RELEASE_FINDINGS_AUTHORITY,
            "active": False,
            "leaves": {},
            "summary": {
                "evaluated": 0,
                "blocked": 0,
                "missing_assessment": 0,
                "admissions": 0,
            },
        }

    id_to_ref = _stable_id_to_ref(indexed)
    active_refs = [
        ref
        for ref in indexed["order"]
        if indexed["nodes"][ref]["kind"] == "LEAF" and ref not in closed_refs
    ]
    rows: dict[str, dict[str, Any]] = {
        ref: {
            "responsibility_id": indexed["nodes"][ref].get("responsibility_id"),
            "admissions": [],
            "blockers": [],
        }
        for ref in active_refs
    }
    covered: set[str] = set()
    admission_count = 0

    for basis in indexed["topology_assessments"]:
        admission = assemble_topology_admission(
            graph,
            assessment_id=basis["id"],
            observations=observations,
        )
        decision = str(admission["decision"]["decision"])
        reasons = list(admission["decision"].get("reasons") or [])
        subjects = list(admission["responsibility_ids"])
        currentness = [
            {
                "responsibility_id": row["responsibility_id"],
                "state": row["state"],
            }
            for row in admission["repository_currentness"]
        ]
        meta = {
            "assessment_id": basis["id"],
            "authority": admission["authority"],
            "decision": decision,
            "reasons": reasons,
            "responsibility_ids": subjects,
            "repository_currentness": currentness,
        }
        admission_count += 1

        for responsibility_id in subjects:
            ref = id_to_ref.get(responsibility_id)
            if ref is None:
                raise AssemblyError(
                    f"{basis['id']}: missing current leaf for Responsibility {responsibility_id!r}"
                )
            if ref not in rows:
                continue
            covered.add(ref)
            rows[ref]["admissions"].append(copy.deepcopy(meta))
            blocker_code = DECISION_BLOCKERS.get(decision)
            if blocker_code:
                detail = (
                    f"{basis['id']} decided {decision} for {', '.join(subjects)}"
                    + (f" — reasons: {', '.join(reasons)}" if reasons else "")
                )
                rows[ref]["blockers"].append(
                    {
                        "code": blocker_code,
                        "detail": detail,
                        "assessment_id": basis["id"],
                        "decision": decision,
                    }
                )
            elif decision != "PASS":
                raise AssemblyError(f"{basis['id']}: unsupported topology decision {decision!r}")

    missing = 0
    for ref in active_refs:
        if ref not in covered:
            missing += 1
            rid = rows[ref]["responsibility_id"] or ref
            rows[ref]["blockers"].append(
                {
                    "code": "TOPOLOGY_ADMISSION_MISSING",
                    "detail": (
                        f"{rid} has no current topology assessment subject in a claim-first plan"
                    ),
                    "assessment_id": None,
                    "decision": "MISSING",
                }
            )
        rows[ref]["admissions"].sort(key=lambda row: row["assessment_id"])
        rows[ref]["blockers"].sort(
            key=lambda row: (
                row["code"],
                row["assessment_id"] or "",
                row["detail"],
            )
        )

    blocked = sum(1 for row in rows.values() if row["blockers"])
    return {
        "authority": RELEASE_FINDINGS_AUTHORITY,
        "active": True,
        "leaves": rows,
        "summary": {
            "evaluated": len(rows),
            "blocked": blocked,
            "missing_assessment": missing,
            "admissions": admission_count,
        },
    }
