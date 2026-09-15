#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

from compile_mathematics_engineering_workbench import (  # noqa: E402
    REGISTRY_REL,
    digest,
    load as load_engineering,
)


class MathematicsEngineeringDiscoveryError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_validate(doc: dict, schema_name: str, code: str) -> None:
    schema = _load_json(ROOT / "contracts" / schema_name)
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        error = errors[0]
        raise MathematicsEngineeringDiscoveryError(code, f"{error.message}; path={list(error.path)}")


def _normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def _tokens(value: str) -> set[str]:
    stop = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with"}
    return {token for token in _normalize(value).split() if len(token) >= 2 and token not in stop}


def _flatten_strings(value: Any) -> list[str]:
    rows: list[str] = []
    if isinstance(value, str):
        rows.append(value)
    elif isinstance(value, list):
        for item in value:
            rows.extend(_flatten_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            rows.extend(_flatten_strings(item))
    return rows


def _add_basis(basis: list[str], value: str) -> None:
    if value not in basis:
        basis.append(value)


def _score(
    query: str,
    hints: list[str],
    identity: str,
    label: str,
    content_strings: list[str],
    *,
    linked_gate_text: bool = False,
) -> tuple[float, list[str]]:
    identity_norm = _normalize(identity)
    label_norm = _normalize(label)
    identity_tokens = _tokens(identity)
    label_tokens = _tokens(label)
    content_tokens: set[str] = set()
    for text in content_strings:
        content_tokens.update(_tokens(text))

    total = 0.0
    basis: list[str] = []
    for index, raw_term in enumerate([query, *hints]):
        term = _normalize(raw_term)
        if not term:
            continue
        term_tokens = _tokens(raw_term)
        local = 0.0

        if term == identity_norm:
            local += 1000.0
            _add_basis(basis, "EXACT_IDENTITY")
        if term == label_norm:
            local += 800.0
            _add_basis(basis, "EXACT_LABEL")
        elif term in label_norm:
            local += 300.0
            _add_basis(basis, "LABEL_PHRASE")

        identity_overlap = term_tokens & identity_tokens
        if identity_overlap:
            local += 80.0 * len(identity_overlap)
            _add_basis(basis, "IDENTITY_TOKEN")

        label_overlap = term_tokens & label_tokens
        if label_overlap:
            local += 50.0 * len(label_overlap)
            _add_basis(basis, "LABEL_TOKEN")

        content_overlap = term_tokens & content_tokens
        if content_overlap:
            local += 12.0 * len(content_overlap)
            _add_basis(basis, "CONTENT_TOKEN")

        if term and label_norm:
            ratio = SequenceMatcher(None, term, label_norm).ratio()
            if ratio >= 0.55:
                local += round(ratio * 100.0, 3)
                _add_basis(basis, "APPROXIMATE_LABEL")

        if index > 0 and local > 0:
            _add_basis(basis, "HINT_MATCH")
        total += local

    if linked_gate_text and total > 0 and "EXACT_IDENTITY" not in basis:
        _add_basis(basis, "LINKED_GATE_TEXT")
    return round(total, 3), basis


def _gate_candidate(gate: dict, query: str, hints: list[str]) -> dict | None:
    identity = gate["subtopic_id"]
    label = gate["learner_title"]
    score, basis = _score(query, hints, identity, label, _flatten_strings(gate))
    if score <= 0:
        return None
    return {
        "scope_kind": "ENGINEERING_GATE",
        "scope_ref": identity,
        "learner_label": label,
        "score": score,
        "match_basis": basis,
        "declared_technical_readiness": gate.get("technical_readiness", "UNDECLARED"),
        "source_scope": gate.get("provenance", {}).get("source_scope", "UNDECLARED"),
    }


def _bucket_candidate(bucket_id: str, linked_gates: list[dict], query: str, hints: list[str]) -> dict | None:
    titles = list(dict.fromkeys(gate["learner_title"] for gate in linked_gates))
    label = " / ".join(titles)
    content: list[str] = []
    for gate in linked_gates:
        content.extend(_flatten_strings(gate))
    score, basis = _score(query, hints, bucket_id, label, content, linked_gate_text=True)
    if score <= 0:
        return None

    readiness = {gate.get("technical_readiness", "UNDECLARED") for gate in linked_gates}
    scopes = {gate.get("provenance", {}).get("source_scope", "UNDECLARED") for gate in linked_gates}
    return {
        "scope_kind": "BUCKET",
        "scope_ref": bucket_id,
        "learner_label": label,
        "score": score,
        "match_basis": basis,
        "declared_technical_readiness": next(iter(readiness)) if len(readiness) == 1 else "MIXED",
        "source_scope": next(iter(scopes)) if len(scopes) == 1 else "MIXED",
    }


def discover_candidates(request: dict, registry: dict | None = None) -> dict:
    """Return ranked, non-authoritative Engineering candidates.

    This function is deliberately permissive. It performs approximate lexical
    discovery over current registry data and optional user hints. It does not
    validate Engineering readiness, compute prerequisite closure, or authorize
    any candidate.
    """
    _schema_validate(
        request,
        "mathematics-engineering-discovery-request.schema.json",
        "MATH_ENG_DISCOVERY_REQUEST_SCHEMA",
    )
    registry = registry or load_engineering(REGISTRY_REL)
    if registry.get("registry_id") != "REG-MATH-TECH-GATE-V1":
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_REGISTRY_ID_MISMATCH",
            str(registry.get("registry_id")),
        )

    query = request["query"]
    hints = list(request.get("hints") or [])
    candidate_kinds = list(request.get("candidate_kinds") or ["ENGINEERING_GATE", "BUCKET"])
    max_candidates = request.get("max_candidates", 6)
    rows: list[dict] = []

    gates = registry.get("subtopic_gates") or []
    if "ENGINEERING_GATE" in candidate_kinds:
        for gate in gates:
            candidate = _gate_candidate(gate, query, hints)
            if candidate is not None:
                rows.append(candidate)

    if "BUCKET" in candidate_kinds:
        bucket_map: dict[str, list[dict]] = {}
        for gate in gates:
            for bucket_id in gate.get("linked_buckets") or []:
                bucket_map.setdefault(bucket_id, []).append(gate)
        for bucket_id, linked_gates in bucket_map.items():
            candidate = _bucket_candidate(bucket_id, linked_gates, query, hints)
            if candidate is not None:
                rows.append(candidate)

    rows.sort(key=lambda row: (-row["score"], row["scope_kind"], row["scope_ref"]))
    rows = rows[:max_candidates]
    for index, row in enumerate(rows, start=1):
        row["rank"] = index

    suffix = request["discovery_request_id"].removeprefix("MATH-ENG-DISC-REQ-")
    receipt = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "discovery_id": f"MATH-ENG-DISC-{suffix}",
        "discovery_request_id": request["discovery_request_id"],
        "discovery_request_digest": digest(request),
        "view_class": "NON_AUTHORITATIVE_ENGINEERING_DISCOVERY",
        "authority": "CANDIDATE_DISCOVERY_ONLY",
        "technical_authorization": "NOT_EVALUATED",
        "publication_authorization": "NOT_IMPLIED",
        "automatic_selection": False,
        "requires_explicit_exact_selection": True,
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "query": query,
        "hints": hints,
        "candidate_kinds": candidate_kinds,
        "candidate_count": len(rows),
        "candidates": rows,
    }
    _schema_validate(
        receipt,
        "mathematics-engineering-discovery-receipt.schema.json",
        "MATH_ENG_DISCOVERY_RECEIPT_SCHEMA",
    )
    return receipt


def _verify_receipt(request: dict, receipt: dict, registry: dict) -> None:
    _schema_validate(
        receipt,
        "mathematics-engineering-discovery-receipt.schema.json",
        "MATH_ENG_DISCOVERY_RECEIPT_SCHEMA",
    )
    expected = discover_candidates(request, registry)
    if receipt != expected:
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED",
            "discovery receipt does not match current request and registry",
        )


def promote_explicit_selection(
    discovery_request: dict,
    discovery_receipt: dict,
    selection: dict,
    registry: dict | None = None,
) -> dict:
    """Convert an explicit exact candidate selection into a standard request.

    Promotion here means only promotion from discovery UI state into the existing
    authoritative request format. It does not perform Engineering authorization;
    the returned request must still pass the unchanged exact resolver and closure.
    """
    _schema_validate(
        selection,
        "mathematics-engineering-discovery-selection.schema.json",
        "MATH_ENG_DISCOVERY_SELECTION_SCHEMA",
    )
    registry = registry or load_engineering(REGISTRY_REL)
    _verify_receipt(discovery_request, discovery_receipt, registry)

    if selection["discovery_id"] != discovery_receipt["discovery_id"]:
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_SELECTION_WRONG_RECEIPT",
            selection["discovery_id"],
        )
    if selection["discovery_receipt_digest"] != digest(discovery_receipt):
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_SELECTION_DIGEST_MISMATCH",
            "selection is not bound to this exact discovery receipt",
        )

    exact_candidates = {
        (row["scope_kind"], row["scope_ref"])
        for row in discovery_receipt["candidates"]
    }
    missing = [
        ref
        for ref in selection["selected_scope_refs"]
        if (selection["selected_scope_kind"], ref) not in exact_candidates
    ]
    if missing:
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_SELECTION_NOT_CANDIDATE",
            f"selected exact identities were not in the bound candidate set: {missing}",
        )

    suffix = selection["selection_id"].removeprefix("MATH-ENG-DISC-SEL-")
    engineering_request = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "request_id": f"MATH-ENG-REQ-DISC_{suffix}",
        "scope_kind": selection["selected_scope_kind"],
        "scope_refs": list(selection["selected_scope_refs"]),
        "engineering_depth": selection["engineering_depth"],
        "learning_purpose": selection["learning_purpose"],
        "owner_decision_ref": selection["selection_id"],
    }
    _schema_validate(
        engineering_request,
        "mathematics-engineering-request.schema.json",
        "MATH_ENG_DISCOVERY_PROMOTED_REQUEST_SCHEMA",
    )
    return engineering_request


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile non-authoritative Mathematics Engineering discovery candidates")
    parser.add_argument("--request", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    request = _load_json(Path(args.request))
    receipt = discover_candidates(request)
    Path(args.out).write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
