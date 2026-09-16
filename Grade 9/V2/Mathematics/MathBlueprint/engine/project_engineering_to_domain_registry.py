#!/usr/bin/env python3
"""Project validated Mathematics Engineering authority into Canonical Domain assets.

LEGACY_TRANSITIONAL:
Canonical production projection is project_engineering_to_domain_registry_v2.py
using math-engineering-domain-projection-v2.schema.json.
This V1 engine is preserved for backward compatibility.

The projector is exact-ID only. It consumes the canonical AssessmentScope->Engineering
resolution, walks prerequisite closure in the authoritative Engineering graph, and
adds rich typed assets to an already same-run Canonical Domain Registry. It never
matches by title, fuzzy text, or remembered aliases.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

from compile_mathematics_engineering_workbench import digest as engineering_digest
from validate_canonical_domain_registry import validate_registry

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
PROJECTION_SCHEMA = ROOT / "contracts" / "math-engineering-domain-projection.schema.json"


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _asset_id(kind: str, subtopic_id: str, gate_id: str, source_ref: str) -> str:
    material = [kind, subtopic_id, gate_id, source_ref]
    return f"REG-MATH-ENG-{kind}-{digest(material)[:16].upper()}"


def _gate_index(registry: dict) -> dict[str, dict]:
    return {row["subtopic_id"]: row for row in registry.get("subtopic_gates", [])}


def _closure(gates: dict[str, dict], gate_id: str, cache: dict[str, list[str]], visiting: set[str] | None = None) -> list[str]:
    if gate_id in cache:
        return cache[gate_id]
    visiting = set(visiting or set())
    if gate_id in visiting:
        fail("DOMAIN_PROJECTION_ENGINEERING_CYCLE", gate_id)
    gate = gates.get(gate_id)
    if gate is None:
        fail("DOMAIN_PROJECTION_ENGINEERING_GATE_UNKNOWN", gate_id)
    visiting.add(gate_id)
    out: list[str] = []
    for prereq in gate.get("prerequisite_ids", []):
        if not isinstance(prereq, str) or not prereq.startswith("MATH-"):
            continue
        for ref in _closure(gates, prereq, cache, visiting):
            if ref not in out:
                out.append(ref)
    if gate_id not in out:
        out.append(gate_id)
    cache[gate_id] = out
    return out


def _join_ref(base_registry: dict, subtopic_id: str) -> str:
    refs = {
        row["join_ref"] for row in base_registry.get("assets", [])
        if row.get("subtopic_id") == subtopic_id
    }
    if len(refs) != 1:
        fail("DOMAIN_PROJECTION_JOIN_BINDING_INVALID", f"{subtopic_id}:{sorted(refs)}")
    return next(iter(refs))


def _capability_asset_map(base_registry: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for asset in base_registry.get("assets", []):
        if asset.get("asset_type") != "CAPABILITY":
            continue
        for ref in asset.get("core1_refs", []):
            if ref in out and out[ref] != asset["asset_id"]:
                fail("DOMAIN_PROJECTION_CAPABILITY_ASSET_AMBIGUOUS", ref)
            out[ref] = asset["asset_id"]
    return out


def _representation_type(value: str) -> str:
    text = str(value or "").upper()
    if "NUMBER_LINE" in text:
        return "NUMBER_LINE"
    if "GRAPH" in text or "PLOT" in text or "CARTESIAN" in text or "ARGAND" in text:
        return "GRAPH"
    if "TABLE" in text or "CHART" in text:
        return "TABLE"
    if "CONSTRUCTION" in text or "GEOMET" in text or "TRIANGLE" in text or "CIRCLE" in text:
        return "GEOMETRIC_CONSTRUCTION"
    if "FLOW" in text or "DEPENDENCY" in text or "PROOF" in text:
        return "FLOW_DEPENDENCY"
    if "ALGEBRA" in text or "EQUATION" in text or "IDENTITY" in text:
        return "ALGEBRA_MAP"
    return "OTHER"


def _verification_type(text: str) -> str:
    value = text.lower()
    if "substitut" in value or "back-sub" in value:
        return "SUBSTITUTION_BACK"
    if "inverse" in value:
        return "INVERSE_RELATION"
    if "limit" in value or "boundary" in value or "special case" in value:
        return "LIMITING_CASE"
    if "unit" in value or "dimension" in value:
        return "UNITS"
    if "sign" in value:
        return "SIGN"
    if "graph" in value or "plot" in value:
        return "GRAPH_CONSISTENCY"
    if any(token in value for token in ("geometry", "geometric", "distance", "angle", "construction")):
        return "GEOMETRIC_CONSISTENCY"
    if any(token in value for token in ("identity", "expand", "factor", "square", "algebraic")):
        return "IDENTITY_CHECK"
    return "OTHER"


def _common(
    *,
    asset_id: str,
    asset_type: str,
    subtopic_id: str,
    title: str,
    caps: list[str],
    qrefs: list[str],
    join_ref: str,
    gate_id: str,
    source_kind: str,
    source_ref: str,
    gate_role: str,
    engineering_registry: dict,
    payload: dict,
    depends_on: list[str] | None = None,
    authority_class: str | None = None,
) -> tuple[dict, dict]:
    if not caps:
        fail("DOMAIN_PROJECTION_CAPABILITY_BINDING_EMPTY", f"{gate_id}:{source_kind}:{source_ref}")
    eng_digest = engineering_digest(engineering_registry)
    if authority_class is None:
        authority_class = "DUAL_VALIDATED" if qrefs else "CORE1_SEMANTIC"
    asset = {
        "asset_id": asset_id,
        "asset_type": asset_type,
        "subtopic_id": subtopic_id,
        "title": title,
        "authority_class": authority_class,
        "admission_status": "ADMITTED",
        "confidence": "HIGH",
        "ground_truth_refs": [
            f"ENGINEERING_GATE:{gate_id}",
            f"ENGINEERING_SOURCE:{source_kind}:{source_ref}",
        ],
        "core1_refs": sorted(set(caps)),
        "core2_refs": sorted(set(qrefs)),
        "validation_refs": [f"ENGINEERING_REGISTRY:{engineering_registry['registry_id']}:{eng_digest}"],
        "join_ref": join_ref,
        "depends_on": list(depends_on or []),
        "payload": payload,
        "provenance_note": (
            f"Deterministic {gate_role} projection from Mathematics Engineering Gate {gate_id}; "
            f"source={source_kind}:{source_ref}; exact-ID mapping only."
        ),
    }
    projection = {
        "asset_id": asset_id,
        "subtopic_id": subtopic_id,
        "engineering_gate_id": gate_id,
        "engineering_gate_role": gate_role,
        "engineering_source_kind": source_kind,
        "engineering_source_ref": source_ref,
        "capability_refs": sorted(set(caps)),
        "core2_refs": sorted(set(qrefs)),
        "asset_digest": digest(asset),
    }
    return asset, projection


def project_engineering_to_domain_registry(
    base_registry: dict,
    *,
    engineering_registry: dict,
    projection_coverage: dict,
    bucket_plan: dict,
    bucket_sid: dict[str, str],
    core2_pages: list[dict],
) -> tuple[dict, dict]:
    """Return (rich_registry, projection_receipt) without mutating inputs."""
    validate_registry(base_registry)
    gates = _gate_index(engineering_registry)
    cap_gate_map = projection_coverage.get("capability_gate_map") or {}
    bucket_rows = {row["bucket_id"]: row for row in projection_coverage.get("bucket_gate_map", [])}
    crosswalk_ref = projection_coverage.get("crosswalk_id")
    if not crosswalk_ref or not cap_gate_map or not bucket_rows:
        fail("DOMAIN_PROJECTION_COVERAGE_INCOMPLETE")

    cap_assets = _capability_asset_map(base_registry)
    pages = {row["question_ref"]: row for row in core2_pages}
    closure_cache: dict[str, list[str]] = {}
    new_assets: list[dict] = []
    provenance: list[dict] = []
    direct_all: set[str] = set()
    transitive_all: set[str] = set()

    def emit(**kwargs) -> str:
        asset, row = _common(engineering_registry=engineering_registry, **kwargs)
        new_assets.append(asset)
        provenance.append(row)
        return asset["asset_id"]

    for bucket in bucket_plan.get("buckets", []):
        bid = bucket["bucket_id"]
        sid = bucket_sid.get(bid)
        resolved = bucket_rows.get(bid)
        if sid is None or resolved is None:
            fail("DOMAIN_PROJECTION_BUCKET_BINDING_MISSING", bid)
        direct = list(resolved.get("engineering_gate_ids") or [])
        if not direct:
            fail("DOMAIN_PROJECTION_BUCKET_GATE_EMPTY", bid)
        direct_all.update(direct)
        bucket_closure: list[str] = []
        for gate_id in direct:
            for ref in _closure(gates, gate_id, closure_cache):
                if ref not in bucket_closure:
                    bucket_closure.append(ref)
        transitive_all.update(bucket_closure)
        join_ref = _join_ref(base_registry, sid)
        bucket_caps = list(bucket.get("member_capability_refs", []))

        for gate_id in bucket_closure:
            gate = gates.get(gate_id)
            if gate is None:
                fail("DOMAIN_PROJECTION_ENGINEERING_GATE_UNKNOWN", gate_id)
            gate_role = "DIRECT" if gate_id in direct else "PREREQUISITE_CLOSURE"
            caps = []
            for cap in bucket_caps:
                cap_direct = cap_gate_map.get(cap, [])
                if any(gate_id in _closure(gates, g, closure_cache) for g in cap_direct):
                    caps.append(cap)
            caps = sorted(set(caps))
            missing_cap_assets = sorted(set(caps) - set(cap_assets))
            if missing_cap_assets:
                fail("DOMAIN_PROJECTION_CAPABILITY_ASSET_MISSING", ",".join(missing_cap_assets))
            qrefs = sorted({
                qid for qid, page in pages.items()
                if set(page.get("capability_refs", [])) & set(caps)
            })

            concept_ids: list[str] = []
            for index, row in enumerate(gate.get("technical_core", []), 1):
                source_ref = str(row.get("concept_id") or f"TECHNICAL_CORE_{index}")
                aid = _asset_id("CON", sid, gate_id, source_ref)
                concept_ids.append(emit(
                    asset_id=aid, asset_type="CONCEPT", subtopic_id=sid,
                    title=str(row.get("concept_id") or gate["learner_title"]), caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="TECHNICAL_CORE",
                    source_ref=source_ref, gate_role=gate_role,
                    payload={
                        "statement": row["canonical_statement"],
                        "prerequisite_refs": [],
                        "implications": [row["why_required"]],
                        "boundary_notes": [row["failure_if_omitted"]],
                    },
                ))
            if not concept_ids:
                fail("DOMAIN_PROJECTION_GATE_CONCEPTS_EMPTY", gate_id)

            model_conditions = list(gate.get("model_conditions", []))
            if model_conditions:
                source_ref = "MODEL_CONDITIONS"
                emit(
                    asset_id=_asset_id("MODEL", sid, gate_id, source_ref), asset_type="MODEL", subtopic_id=sid,
                    title=f"Model conditions — {gate['learner_title']}", caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="MODEL_CONDITIONS",
                    source_ref=source_ref, gate_role=gate_role, depends_on=concept_ids,
                    payload={
                        "statement": "Model validity requires: " + " | ".join(str(x["condition"]) for x in model_conditions),
                        "prerequisite_refs": concept_ids,
                        "implications": [str(x["what_changes_if_violated"]) for x in model_conditions],
                        "boundary_notes": [str(x["why_needed"]) for x in model_conditions],
                    },
                )

            equation_ids: list[str] = []
            for index, row in enumerate(gate.get("mandatory_equations", []), 1):
                source_ref = str(row.get("equation_id") or f"MANDATORY_EQUATION_{index}")
                valid_when = [
                    str(x) for x in (row.get("conditions_of_validity"), row.get("reference_frame_or_sign"))
                    if isinstance(x, str) and x.strip()
                ]
                if not valid_when:
                    valid_when = [str(x["condition"]) for x in model_conditions if str(x.get("condition", "")).strip()]
                if not valid_when:
                    fail("DOMAIN_PROJECTION_EQUATION_VALIDITY_MISSING", f"{gate_id}:{source_ref}")
                term_meanings = []
                if str(row.get("meaning_of_symbols", "")).strip():
                    term_meanings.append(str(row["meaning_of_symbols"]))
                for symbol in row.get("symbols", []):
                    term_meanings.append(
                        f"{symbol.get('symbol')}: {symbol.get('name')}; domain={symbol.get('domain')}; role={symbol.get('geometric_or_algebraic_role')}"
                    )
                if not term_meanings:
                    fail("DOMAIN_PROJECTION_EQUATION_TERMS_MISSING", f"{gate_id}:{source_ref}")
                aid = _asset_id("EQ", sid, gate_id, source_ref)
                equation_ids.append(emit(
                    asset_id=aid, asset_type="EQUATION", subtopic_id=sid,
                    title=f"Engineering relation — {source_ref}", caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="MANDATORY_EQUATION",
                    source_ref=source_ref, gate_role=gate_role, depends_on=concept_ids,
                    payload={
                        "expression": row["formula"],
                        "mathematical_question": f"Which exact relation governs {gate['learner_title']} under its declared Engineering conditions?",
                        "parent_refs": concept_ids,
                        "valid_when": valid_when,
                        "term_meanings": term_meanings,
                        "inverse_uses": [],
                        "failure_cases": [str(x["what_changes_if_violated"]) for x in model_conditions],
                    },
                ))

            math_bindings = concept_ids + equation_ids
            for index, row in enumerate(gate.get("representations", []), 1):
                source_ref = str(row.get("representation_id") or f"REPRESENTATION_{index}")
                must_visible = [str(x) for x in row.get("mandatory_labels", []) if str(x).strip()]
                if str(row.get("math_encoded", "")).strip():
                    must_visible.append(str(row["math_encoded"]))
                must_not = []
                if str(row.get("common_incorrect_version", "")).strip():
                    must_not.append(str(row["common_incorrect_version"]))
                if str(row.get("what_cannot_be_omitted", "")).strip():
                    must_not.append("Must not omit: " + str(row["what_cannot_be_omitted"]))
                if not must_visible or not must_not:
                    fail("DOMAIN_PROJECTION_REPRESENTATION_SEMANTICS_MISSING", f"{gate_id}:{source_ref}")
                emit(
                    asset_id=_asset_id("REP", sid, gate_id, source_ref), asset_type="REPRESENTATION", subtopic_id=sid,
                    title=str(row.get("name") or source_ref), caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="REPRESENTATION",
                    source_ref=source_ref, gate_role=gate_role, depends_on=math_bindings,
                    payload={
                        "representation_type": _representation_type(str(row.get("representation_type", ""))),
                        "must_make_visible": must_visible,
                        "must_not_imply": must_not,
                        "math_bindings": math_bindings,
                    },
                )

            previous_atom: str | None = None
            for index, row in enumerate(gate.get("reasoning_sequence", []), 1):
                source_ref = f"REASONING_STEP_{row.get('step', index)}"
                prereqs = list(concept_ids)
                if previous_atom:
                    prereqs.append(previous_atom)
                previous_atom = emit(
                    asset_id=_asset_id("ATOM", sid, gate_id, source_ref), asset_type="LEARNING_ATOM", subtopic_id=sid,
                    title=f"Expert reasoning step {row.get('step', index)} — {gate['learner_title']}", caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="REASONING_STEP",
                    source_ref=source_ref, gate_role=gate_role, depends_on=prereqs,
                    payload={
                        "statement": str(row["expert_action"]),
                        "prerequisite_refs": prereqs,
                        "implications": ["Inferential jump: " + str(row["inferential_jump"])],
                        "boundary_notes": [],
                    },
                )

            for index, row in enumerate(gate.get("required_transformations", []), 1):
                source_ref = f"TRANSFORMATION_{index}"
                emit(
                    asset_id=_asset_id("ATOM", sid, gate_id, source_ref), asset_type="LEARNING_ATOM", subtopic_id=sid,
                    title=f"Required transformation {index} — {gate['learner_title']}", caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="REQUIRED_TRANSFORMATION",
                    source_ref=source_ref, gate_role=gate_role, depends_on=concept_ids,
                    payload={
                        "statement": str(row["description"]),
                        "prerequisite_refs": concept_ids,
                        "implications": [
                            f"{row['from_mode']} -> {row['to_mode']}",
                            "Target Core role: " + str(row["target_core_role"]),
                        ],
                        "boundary_notes": [],
                    },
                )

            for index, row in enumerate(gate.get("misconceptions", []), 1):
                source_ref = str(row.get("misconception_id") or f"MISCONCEPTION_{index}")
                triggers = [
                    str(x) for x in (row.get("why_plausible"), row.get("required_counterexample"))
                    if isinstance(x, str) and x.strip()
                ]
                if not triggers:
                    fail("DOMAIN_PROJECTION_MISCONCEPTION_TRIGGER_MISSING", f"{gate_id}:{source_ref}")
                emit(
                    asset_id=_asset_id("MISC", sid, gate_id, source_ref), asset_type="MISCONCEPTION", subtopic_id=sid,
                    title=f"Misconception — {source_ref}", caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="MISCONCEPTION",
                    source_ref=source_ref, gate_role=gate_role,
                    payload={
                        "incorrect_model": str(row["incorrect_belief"]),
                        "corrective_model": str(row["required_technical_repair"]),
                        "trigger_conditions": triggers,
                    },
                )

            for index, instruction in enumerate(gate.get("mandatory_verifications", []), 1):
                source_ref = f"VERIFICATION_{index}"
                emit(
                    asset_id=_asset_id("VER", sid, gate_id, source_ref), asset_type="VERIFICATION_RULE", subtopic_id=sid,
                    title=f"Independent verification {index} — {gate['learner_title']}", caps=caps, qrefs=qrefs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="MANDATORY_VERIFICATION",
                    source_ref=source_ref, gate_role=gate_role,
                    payload={
                        "verification_type": _verification_type(str(instruction)),
                        "instruction": str(instruction),
                        "uses_answer_key": False,
                    },
                )

            cap_asset_refs = [cap_assets[cap] for cap in caps]
            for index, row in enumerate(gate.get("problem_families", []), 1):
                source_ref = str(row.get("family_id") or f"PROBLEM_FAMILY_{index}")
                family_core2_refs = sorted(set([source_ref, *qrefs]))
                recognition = row.get("recognition_cues")
                recognition_cues = [str(recognition)] if isinstance(recognition, str) else [str(x) for x in (recognition or [])]
                if not recognition_cues:
                    fail("DOMAIN_PROJECTION_PROBLEM_FAMILY_RECOGNITION_MISSING", f"{gate_id}:{source_ref}")
                authority = "DUAL_VALIDATED" if qrefs else "CORE2_ASSESSMENT"
                emit(
                    asset_id=_asset_id("PF", sid, gate_id, source_ref), asset_type="PROBLEM_FAMILY", subtopic_id=sid,
                    title=str(row.get("name") or source_ref), caps=caps, qrefs=family_core2_refs,
                    join_ref=join_ref, gate_id=gate_id, source_kind="PROBLEM_FAMILY",
                    source_ref=source_ref, gate_role=gate_role, authority_class=authority,
                    payload={
                        "recognition_cues": recognition_cues,
                        "invariant_refs": concept_ids,
                        "required_capability_refs": cap_asset_refs,
                        "safe_variations": [],
                        "forbidden_variations": [],
                    },
                )

    result = copy.deepcopy(base_registry)
    existing = {row["asset_id"] for row in result["assets"]}
    duplicates = sorted(existing & {row["asset_id"] for row in new_assets})
    if duplicates:
        fail("DOMAIN_PROJECTION_ASSET_ID_COLLISION", ",".join(duplicates))
    result["assets"].extend(new_assets)
    validate_registry(result)

    receipt = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "projection_id": "",
        "domain_registry_ref": result["registry_id"],
        "engineering_registry_id": engineering_registry["registry_id"],
        "engineering_registry_digest": engineering_digest(engineering_registry),
        "crosswalk_ref": crosswalk_ref,
        "base_asset_count": len(base_registry["assets"]),
        "projected_asset_count": len(new_assets),
        "direct_gate_ids": sorted(direct_all),
        "transitive_gate_ids": sorted(transitive_all),
        "asset_projections": sorted(provenance, key=lambda x: x["asset_id"]),
        "projection_digest": "",
    }
    identity = {k: v for k, v in receipt.items() if k not in {"projection_id", "projection_digest"}}
    receipt["projection_id"] = "MATH-ENG-DOMAIN-PROJ-" + digest(identity)[:16].upper()
    receipt["projection_digest"] = digest({k: v for k, v in receipt.items() if k != "projection_digest"})
    jsonschema.validate(receipt, json.loads(PROJECTION_SCHEMA.read_text(encoding="utf-8")))
    return result, receipt
