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
VOCABULARY_REL = "policies/mathematics-engineering-discovery-vocabulary.v1.json"
VOCABULARY_SCHEMA = "mathematics-engineering-discovery-vocabulary.schema.json"

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


def _add_match(matches: list[str], value: str) -> None:
    if value not in matches:
        matches.append(value)


def _known_targets(registry: dict) -> tuple[set[str], set[str]]:
    gate_ids = {gate["subtopic_id"] for gate in registry.get("subtopic_gates") or []}
    bucket_ids = {
        bucket_id
        for gate in registry.get("subtopic_gates") or []
        for bucket_id in gate.get("linked_buckets") or []
    }
    return gate_ids, bucket_ids


def validate_discovery_vocabulary_catalog(catalog: dict, registry: dict) -> dict:
    _schema_validate(catalog, VOCABULARY_SCHEMA, "MATH_ENG_DISCOVERY_VOCABULARY_SCHEMA")
    if catalog["registry_id"] != registry.get("registry_id"):
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_VOCABULARY_REGISTRY_ID_MISMATCH",
            f"catalog={catalog['registry_id']} registry={registry.get('registry_id')}",
        )
    current_registry_digest = digest(registry)
    if catalog["registry_digest"] != current_registry_digest:
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_VOCABULARY_REGISTRY_DIGEST_MISMATCH",
            f"catalog={catalog['registry_digest']} registry={current_registry_digest}",
        )

    gate_ids, bucket_ids = _known_targets(registry)
    seen_targets: set[tuple[str, str]] = set()
    term_count = 0
    for entry in catalog["entries"]:
        target = (entry["target_scope_kind"], entry["target_scope_ref"])
        if target in seen_targets:
            raise MathematicsEngineeringDiscoveryError(
                "MATH_ENG_DISCOVERY_VOCABULARY_DUPLICATE_TARGET",
                f"duplicate vocabulary target {target}",
            )
        seen_targets.add(target)

        valid_refs = gate_ids if target[0] == "ENGINEERING_GATE" else bucket_ids
        if target[1] not in valid_refs:
            raise MathematicsEngineeringDiscoveryError(
                "MATH_ENG_DISCOVERY_VOCABULARY_UNKNOWN_TARGET",
                f"unknown vocabulary target {target}",
            )

        seen_terms: set[str] = set()
        for term in entry["terms"]:
            normalized = _normalize(term["phrase"])
            if not normalized:
                raise MathematicsEngineeringDiscoveryError(
                    "MATH_ENG_DISCOVERY_VOCABULARY_EMPTY_TERM",
                    f"empty normalized term for {target}",
                )
            if normalized in seen_terms:
                raise MathematicsEngineeringDiscoveryError(
                    "MATH_ENG_DISCOVERY_VOCABULARY_DUPLICATE_TERM",
                    f"duplicate normalized term {normalized!r} for {target}",
                )
            seen_terms.add(normalized)
            term_count += 1

    return {
        "status": "PASS",
        "catalog_id": catalog["catalog_id"],
        "catalog_digest": digest(catalog),
        "registry_id": registry["registry_id"],
        "registry_digest": current_registry_digest,
        "entry_count": len(catalog["entries"]),
        "term_count": term_count,
    }


def _load_vocabulary_catalog() -> dict:
    return _load_json(ROOT / VOCABULARY_REL)


def _vocabulary_by_target(catalog: dict) -> dict[tuple[str, str], list[dict]]:
    return {
        (entry["target_scope_kind"], entry["target_scope_ref"]): list(entry["terms"])
        for entry in catalog["entries"]
    }


def _bucket_map(registry: dict) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {}
    for gate in registry.get("subtopic_gates") or []:
        for bucket_id in gate.get("linked_buckets") or []:
            rows.setdefault(bucket_id, []).append(gate)
    return rows


def _build_discovery_index(registry: dict, catalog: dict) -> dict:
    vocabulary = _vocabulary_by_target(catalog)
    entries: list[dict] = []
    for gate in sorted(registry.get("subtopic_gates") or [], key=lambda row: row["subtopic_id"]):
        target = ("ENGINEERING_GATE", gate["subtopic_id"])
        entries.append(
            {
                "scope_kind": target[0],
                "scope_ref": target[1],
                "learner_label": gate["learner_title"],
                "linked_gate_ids": [gate["subtopic_id"]],
                "content_digest": digest(_flatten_strings(gate)),
                "vocabulary_terms": vocabulary.get(target, []),
            }
        )

    for bucket_id, linked_gates in sorted(_bucket_map(registry).items()):
        target = ("BUCKET", bucket_id)
        sorted_gates = sorted(linked_gates, key=lambda row: row["subtopic_id"])
        entries.append(
            {
                "scope_kind": target[0],
                "scope_ref": target[1],
                "learner_label": " / ".join(dict.fromkeys(gate["learner_title"] for gate in sorted_gates)),
                "linked_gate_ids": [gate["subtopic_id"] for gate in sorted_gates],
                "content_digest": digest([text for gate in sorted_gates for text in _flatten_strings(gate)]),
                "vocabulary_terms": vocabulary.get(target, []),
            }
        )

    return {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "index_class": "NON_AUTHORITATIVE_GENERATED_DISCOVERY_INDEX",
        "authority": "CANDIDATE_DISCOVERY_ONLY",
        "technical_authorization": "NOT_EVALUATED",
        "publication_authorization": "NOT_IMPLIED",
        "registry_id": registry["registry_id"],
        "registry_digest": digest(registry),
        "vocabulary_catalog_id": catalog["catalog_id"],
        "vocabulary_catalog_digest": digest(catalog),
        "entries": entries,
    }


def _score(
    query: str,
    hints: list[str],
    identity: str,
    label: str,
    content_strings: list[str],
    vocabulary_terms: list[dict],
    *,
    linked_gate_text: bool = False,
) -> tuple[float, list[str], list[str]]:
    identity_norm = _normalize(identity)
    label_norm = _normalize(label)
    identity_tokens = _tokens(identity)
    label_tokens = _tokens(label)
    content_tokens: set[str] = set()
    for text in content_strings:
        content_tokens.update(_tokens(text))

    vocabulary_rows = [
        (term["phrase"], _normalize(term["phrase"]), _tokens(term["phrase"]))
        for term in vocabulary_terms
    ]

    total = 0.0
    basis: list[str] = []
    matched_vocabulary_terms: list[str] = []
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

        exact_vocab = [phrase for phrase, normalized, _ in vocabulary_rows if term == normalized]
        if exact_vocab:
            local += 700.0
            _add_basis(basis, "VOCABULARY_EXACT")
            for phrase in exact_vocab:
                _add_match(matched_vocabulary_terms, phrase)

        phrase_vocab = [
            phrase
            for phrase, normalized, _ in vocabulary_rows
            if term != normalized and normalized and (normalized in term or term in normalized)
        ]
        if phrase_vocab:
            local += 280.0
            _add_basis(basis, "VOCABULARY_PHRASE")
            for phrase in phrase_vocab:
                _add_match(matched_vocabulary_terms, phrase)

        best_overlap = 0
        overlap_phrases: list[str] = []
        for phrase, _, vocabulary_tokens in vocabulary_rows:
            overlap = len(term_tokens & vocabulary_tokens)
            if overlap > best_overlap:
                best_overlap = overlap
                overlap_phrases = [phrase]
            elif overlap > 0 and overlap == best_overlap:
                overlap_phrases.append(phrase)
        if best_overlap:
            local += 65.0 * best_overlap
            _add_basis(basis, "VOCABULARY_TOKEN")
            for phrase in overlap_phrases:
                _add_match(matched_vocabulary_terms, phrase)

        best_ratio = 0.0
        approximate_phrases: list[str] = []
        for phrase, normalized, _ in vocabulary_rows:
            if not normalized:
                continue
            ratio = SequenceMatcher(None, term, normalized).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                approximate_phrases = [phrase]
            elif ratio == best_ratio:
                approximate_phrases.append(phrase)
        if best_ratio >= 0.62 and not exact_vocab:
            local += round(best_ratio * 90.0, 3)
            _add_basis(basis, "APPROXIMATE_VOCABULARY")
            for phrase in approximate_phrases:
                _add_match(matched_vocabulary_terms, phrase)

        if index > 0 and local > 0:
            _add_basis(basis, "HINT_MATCH")
        total += local

    if linked_gate_text and total > 0 and "EXACT_IDENTITY" not in basis:
        _add_basis(basis, "LINKED_GATE_TEXT")
    return round(total, 3), basis, matched_vocabulary_terms


def _gate_candidate(gate: dict, query: str, hints: list[str], vocabulary_terms: list[dict]) -> dict | None:
    identity = gate["subtopic_id"]
    label = gate["learner_title"]
    score, basis, matched_terms = _score(
        query,
        hints,
        identity,
        label,
        _flatten_strings(gate),
        vocabulary_terms,
    )
    if score <= 0:
        return None
    return {
        "scope_kind": "ENGINEERING_GATE",
        "scope_ref": identity,
        "learner_label": label,
        "score": score,
        "match_basis": basis,
        "matched_vocabulary_terms": matched_terms,
        "declared_technical_readiness": gate.get("technical_readiness", "UNDECLARED"),
        "source_scope": gate.get("provenance", {}).get("source_scope", "UNDECLARED"),
    }


def _bucket_candidate(
    bucket_id: str,
    linked_gates: list[dict],
    query: str,
    hints: list[str],
    vocabulary_terms: list[dict],
) -> dict | None:
    sorted_gates = sorted(linked_gates, key=lambda row: row["subtopic_id"])
    titles = list(dict.fromkeys(gate["learner_title"] for gate in sorted_gates))
    label = " / ".join(titles)
    content: list[str] = []
    for gate in sorted_gates:
        content.extend(_flatten_strings(gate))
    score, basis, matched_terms = _score(
        query,
        hints,
        bucket_id,
        label,
        content,
        vocabulary_terms,
        linked_gate_text=True,
    )
    if score <= 0:
        return None

    readiness = {gate.get("technical_readiness", "UNDECLARED") for gate in sorted_gates}
    scopes = {gate.get("provenance", {}).get("source_scope", "UNDECLARED") for gate in sorted_gates}
    return {
        "scope_kind": "BUCKET",
        "scope_ref": bucket_id,
        "learner_label": label,
        "score": score,
        "match_basis": basis,
        "matched_vocabulary_terms": matched_terms,
        "declared_technical_readiness": next(iter(readiness)) if len(readiness) == 1 else "MIXED",
        "source_scope": next(iter(scopes)) if len(scopes) == 1 else "MIXED",
    }


def discover_candidates(
    request: dict,
    registry: dict | None = None,
    vocabulary_catalog: dict | None = None,
) -> dict:
    """Return ranked, non-authoritative Engineering candidates.

    Discovery is deliberately permissive. Registry text and governed discovery
    vocabulary can improve candidate finding, but neither validates readiness,
    computes prerequisite closure, nor authorizes any candidate.
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

    vocabulary_catalog = vocabulary_catalog or _load_vocabulary_catalog()
    validate_discovery_vocabulary_catalog(vocabulary_catalog, registry)
    vocabulary = _vocabulary_by_target(vocabulary_catalog)
    discovery_index = _build_discovery_index(registry, vocabulary_catalog)

    query = request["query"]
    hints = list(request.get("hints") or [])
    candidate_kinds = list(request.get("candidate_kinds") or ["ENGINEERING_GATE", "BUCKET"])
    max_candidates = request.get("max_candidates", 6)
    rows: list[dict] = []

    gates = registry.get("subtopic_gates") or []
    if "ENGINEERING_GATE" in candidate_kinds:
        for gate in gates:
            target = ("ENGINEERING_GATE", gate["subtopic_id"])
            candidate = _gate_candidate(gate, query, hints, vocabulary.get(target, []))
            if candidate is not None:
                rows.append(candidate)

    if "BUCKET" in candidate_kinds:
        for bucket_id, linked_gates in _bucket_map(registry).items():
            target = ("BUCKET", bucket_id)
            candidate = _bucket_candidate(
                bucket_id,
                linked_gates,
                query,
                hints,
                vocabulary.get(target, []),
            )
            if candidate is not None:
                rows.append(candidate)

    rows.sort(key=lambda row: (-row["score"], row["scope_kind"], row["scope_ref"]))
    rows = rows[:max_candidates]
    for index, row in enumerate(rows, start=1):
        row["rank"] = index

    suffix = request["discovery_request_id"].removeprefix("MATH-ENG-DISC-REQ-")
    receipt = {
        "schema_version": "1.1.0",
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
        "vocabulary_catalog_id": vocabulary_catalog["catalog_id"],
        "vocabulary_catalog_digest": digest(vocabulary_catalog),
        "discovery_index_digest": digest(discovery_index),
        "discovery_index_entry_count": len(discovery_index["entries"]),
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


def _verify_receipt(request: dict, receipt: dict, registry: dict, vocabulary_catalog: dict) -> None:
    _schema_validate(
        receipt,
        "mathematics-engineering-discovery-receipt.schema.json",
        "MATH_ENG_DISCOVERY_RECEIPT_SCHEMA",
    )
    expected = discover_candidates(request, registry, vocabulary_catalog)
    if receipt != expected:
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED",
            "discovery receipt does not match current request, registry, vocabulary catalog and generated index",
        )


def promote_explicit_selection(
    discovery_request: dict,
    discovery_receipt: dict,
    selection: dict,
    registry: dict | None = None,
    vocabulary_catalog: dict | None = None,
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
    vocabulary_catalog = vocabulary_catalog or _load_vocabulary_catalog()
    _verify_receipt(discovery_request, discovery_receipt, registry, vocabulary_catalog)

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
    parser.add_argument("--vocabulary")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    request = _load_json(Path(args.request))
    vocabulary = _load_json(Path(args.vocabulary)) if args.vocabulary else None
    receipt = discover_candidates(request, vocabulary_catalog=vocabulary)
    Path(args.out).write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
