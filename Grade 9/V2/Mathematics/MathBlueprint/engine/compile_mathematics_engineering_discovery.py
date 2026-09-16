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

from compile_mathematics_engineering_workbench import REGISTRY_REL, digest, load as load_engineering  # noqa: E402


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
        e = errors[0]
        raise MathematicsEngineeringDiscoveryError(code, f"{e.message}; path={list(e.path)}")


def _normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def _tokens(value: str) -> set[str]:
    stop = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with"}
    return {x for x in _normalize(value).split() if len(x) >= 2 and x not in stop}


def _flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in _flatten_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _flatten_strings(item)]
    return []


def _add_once(rows: list[str], value: str) -> None:
    if value not in rows:
        rows.append(value)


def _bucket_map(registry: dict) -> dict[str, list[dict]]:
    rows: dict[str, list[dict]] = {}
    for gate in registry.get("subtopic_gates") or []:
        for bucket_id in gate.get("linked_buckets") or []:
            rows.setdefault(bucket_id, []).append(gate)
    return rows


def validate_discovery_vocabulary_catalog(catalog: dict, registry: dict) -> dict:
    _schema_validate(catalog, VOCABULARY_SCHEMA, "MATH_ENG_DISCOVERY_VOCABULARY_SCHEMA")
    if catalog["registry_id"] != registry.get("registry_id"):
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_VOCABULARY_REGISTRY_ID_MISMATCH",
            f"catalog={catalog['registry_id']} registry={registry.get('registry_id')}",
        )

    gate_ids = {gate["subtopic_id"] for gate in registry.get("subtopic_gates") or []}
    bucket_ids = set(_bucket_map(registry))
    seen_targets: set[tuple[str, str]] = set()
    term_count = 0
    for entry in catalog["entries"]:
        target = (entry["target_scope_kind"], entry["target_scope_ref"])
        if target in seen_targets:
            raise MathematicsEngineeringDiscoveryError(
                "MATH_ENG_DISCOVERY_VOCABULARY_DUPLICATE_TARGET", f"duplicate vocabulary target {target}"
            )
        seen_targets.add(target)
        valid_refs = gate_ids if target[0] == "ENGINEERING_GATE" else bucket_ids
        if target[1] not in valid_refs:
            raise MathematicsEngineeringDiscoveryError(
                "MATH_ENG_DISCOVERY_VOCABULARY_UNKNOWN_TARGET", f"unknown vocabulary target {target}"
            )
        seen_terms: set[str] = set()
        for term in entry["terms"]:
            normalized = _normalize(term["phrase"])
            if not normalized:
                raise MathematicsEngineeringDiscoveryError(
                    "MATH_ENG_DISCOVERY_VOCABULARY_EMPTY_TERM", f"empty normalized term for {target}"
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
        "registry_digest": digest(registry),
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


def _build_discovery_index(registry: dict, catalog: dict) -> dict:
    vocabulary = _vocabulary_by_target(catalog)
    entries: list[dict] = []
    for gate in sorted(registry.get("subtopic_gates") or [], key=lambda x: x["subtopic_id"]):
        target = ("ENGINEERING_GATE", gate["subtopic_id"])
        entries.append({
            "scope_kind": target[0],
            "scope_ref": target[1],
            "learner_label": gate["learner_title"],
            "linked_gate_ids": [gate["subtopic_id"]],
            "content_digest": digest(_flatten_strings(gate)),
            "vocabulary_terms": vocabulary.get(target, []),
        })
    for bucket_id, linked in sorted(_bucket_map(registry).items()):
        target = ("BUCKET", bucket_id)
        gates = sorted(linked, key=lambda x: x["subtopic_id"])
        entries.append({
            "scope_kind": target[0],
            "scope_ref": target[1],
            "learner_label": " / ".join(dict.fromkeys(g["learner_title"] for g in gates)),
            "linked_gate_ids": [g["subtopic_id"] for g in gates],
            "content_digest": digest([text for g in gates for text in _flatten_strings(g)]),
            "vocabulary_terms": vocabulary.get(target, []),
        })
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


def _score(query: str, hints: list[str], identity: str, label: str, content_strings: list[str], vocabulary_terms: list[dict], *, linked_gate_text: bool = False) -> tuple[float, list[str], list[str]]:
    identity_norm, label_norm = _normalize(identity), _normalize(label)
    identity_tokens, label_tokens = _tokens(identity), _tokens(label)
    content_tokens: set[str] = set()
    for text in content_strings:
        content_tokens.update(_tokens(text))
    vocabulary_rows = [(t["phrase"], _normalize(t["phrase"]), _tokens(t["phrase"])) for t in vocabulary_terms]

    total = 0.0
    basis: list[str] = []
    matched: list[str] = []
    for index, raw in enumerate([query, *hints]):
        term = _normalize(raw)
        if not term:
            continue
        term_tokens = _tokens(raw)
        local = 0.0
        if term == identity_norm:
            local += 1000.0; _add_once(basis, "EXACT_IDENTITY")
        if term == label_norm:
            local += 800.0; _add_once(basis, "EXACT_LABEL")
        elif term in label_norm:
            local += 300.0; _add_once(basis, "LABEL_PHRASE")
        overlap = term_tokens & identity_tokens
        if overlap:
            local += 80.0 * len(overlap); _add_once(basis, "IDENTITY_TOKEN")
        overlap = term_tokens & label_tokens
        if overlap:
            local += 50.0 * len(overlap); _add_once(basis, "LABEL_TOKEN")
        overlap = term_tokens & content_tokens
        if overlap:
            local += 12.0 * len(overlap); _add_once(basis, "CONTENT_TOKEN")
        ratio = SequenceMatcher(None, term, label_norm).ratio() if term and label_norm else 0.0
        if ratio >= 0.55:
            local += round(ratio * 100.0, 3); _add_once(basis, "APPROXIMATE_LABEL")

        exact = [p for p, n, _ in vocabulary_rows if term == n]
        if exact:
            local += 700.0; _add_once(basis, "VOCABULARY_EXACT")
            for phrase in exact: _add_once(matched, phrase)
        phrases = [p for p, n, _ in vocabulary_rows if term != n and n and (n in term or term in n)]
        if phrases:
            local += 280.0; _add_once(basis, "VOCABULARY_PHRASE")
            for phrase in phrases: _add_once(matched, phrase)
        best_overlap = max((len(term_tokens & toks) for _, _, toks in vocabulary_rows), default=0)
        if best_overlap:
            local += 65.0 * best_overlap; _add_once(basis, "VOCABULARY_TOKEN")
            for phrase, _, toks in vocabulary_rows:
                if len(term_tokens & toks) == best_overlap: _add_once(matched, phrase)
        ratios = [(SequenceMatcher(None, term, n).ratio(), p) for p, n, _ in vocabulary_rows if n]
        best_ratio = max((r for r, _ in ratios), default=0.0)
        if best_ratio >= 0.62 and not exact:
            local += round(best_ratio * 90.0, 3); _add_once(basis, "APPROXIMATE_VOCABULARY")
            for r, phrase in ratios:
                if r == best_ratio: _add_once(matched, phrase)
        if index > 0 and local > 0:
            _add_once(basis, "HINT_MATCH")
        total += local
    if linked_gate_text and total > 0 and "EXACT_IDENTITY" not in basis:
        _add_once(basis, "LINKED_GATE_TEXT")
    return round(total, 3), basis, matched


def _gate_candidate(gate: dict, query: str, hints: list[str], vocabulary_terms: list[dict]) -> dict | None:
    score, basis, matched = _score(query, hints, gate["subtopic_id"], gate["learner_title"], _flatten_strings(gate), vocabulary_terms)
    if score <= 0:
        return None
    return {
        "scope_kind": "ENGINEERING_GATE", "scope_ref": gate["subtopic_id"], "learner_label": gate["learner_title"],
        "score": score, "match_basis": basis, "matched_vocabulary_terms": matched,
        "declared_technical_readiness": gate.get("technical_readiness", "UNDECLARED"),
        "source_scope": gate.get("provenance", {}).get("source_scope", "UNDECLARED"),
    }


def _bucket_candidate(bucket_id: str, linked: list[dict], query: str, hints: list[str], vocabulary_terms: list[dict]) -> dict | None:
    gates = sorted(linked, key=lambda x: x["subtopic_id"])
    label = " / ".join(dict.fromkeys(g["learner_title"] for g in gates))
    content = [text for g in gates for text in _flatten_strings(g)]
    score, basis, matched = _score(query, hints, bucket_id, label, content, vocabulary_terms, linked_gate_text=True)
    if score <= 0:
        return None
    readiness = {g.get("technical_readiness", "UNDECLARED") for g in gates}
    scopes = {g.get("provenance", {}).get("source_scope", "UNDECLARED") for g in gates}
    return {
        "scope_kind": "BUCKET", "scope_ref": bucket_id, "learner_label": label,
        "score": score, "match_basis": basis, "matched_vocabulary_terms": matched,
        "declared_technical_readiness": next(iter(readiness)) if len(readiness) == 1 else "MIXED",
        "source_scope": next(iter(scopes)) if len(scopes) == 1 else "MIXED",
    }


def discover_candidates(request: dict, registry: dict | None = None, vocabulary_catalog: dict | None = None) -> dict:
    _schema_validate(request, "mathematics-engineering-discovery-request.schema.json", "MATH_ENG_DISCOVERY_REQUEST_SCHEMA")
    registry = registry or load_engineering(REGISTRY_REL)
    if registry.get("registry_id") != "REG-MATH-TECH-GATE-V1":
        raise MathematicsEngineeringDiscoveryError("MATH_ENG_DISCOVERY_REGISTRY_ID_MISMATCH", str(registry.get("registry_id")))
    vocabulary_catalog = vocabulary_catalog or _load_vocabulary_catalog()
    validate_discovery_vocabulary_catalog(vocabulary_catalog, registry)
    vocabulary = _vocabulary_by_target(vocabulary_catalog)
    discovery_index = _build_discovery_index(registry, vocabulary_catalog)

    query = request["query"]
    hints = list(request.get("hints") or [])
    kinds = list(request.get("candidate_kinds") or ["ENGINEERING_GATE", "BUCKET"])
    rows: list[dict] = []
    if "ENGINEERING_GATE" in kinds:
        for gate in registry.get("subtopic_gates") or []:
            candidate = _gate_candidate(gate, query, hints, vocabulary.get(("ENGINEERING_GATE", gate["subtopic_id"]), []))
            if candidate: rows.append(candidate)
    if "BUCKET" in kinds:
        for bucket_id, linked in _bucket_map(registry).items():
            candidate = _bucket_candidate(bucket_id, linked, query, hints, vocabulary.get(("BUCKET", bucket_id), []))
            if candidate: rows.append(candidate)
    rows.sort(key=lambda row: (-row["score"], row["scope_kind"], row["scope_ref"]))
    rows = rows[: request.get("max_candidates", 6)]
    for rank, row in enumerate(rows, 1): row["rank"] = rank

    suffix = request["discovery_request_id"].removeprefix("MATH-ENG-DISC-REQ-")
    receipt = {
        "schema_version": "1.1.0", "subject": "MATHEMATICS", "discovery_id": f"MATH-ENG-DISC-{suffix}",
        "discovery_request_id": request["discovery_request_id"], "discovery_request_digest": digest(request),
        "view_class": "NON_AUTHORITATIVE_ENGINEERING_DISCOVERY", "authority": "CANDIDATE_DISCOVERY_ONLY",
        "technical_authorization": "NOT_EVALUATED", "publication_authorization": "NOT_IMPLIED",
        "automatic_selection": False, "requires_explicit_exact_selection": True,
        "registry_id": registry["registry_id"], "registry_digest": digest(registry),
        "vocabulary_catalog_id": vocabulary_catalog["catalog_id"], "vocabulary_catalog_digest": digest(vocabulary_catalog),
        "discovery_index_digest": digest(discovery_index), "discovery_index_entry_count": len(discovery_index["entries"]),
        "query": query, "hints": hints, "candidate_kinds": kinds, "candidate_count": len(rows), "candidates": rows,
    }
    _schema_validate(receipt, "mathematics-engineering-discovery-receipt.schema.json", "MATH_ENG_DISCOVERY_RECEIPT_SCHEMA")
    return receipt


def _verify_receipt(request: dict, receipt: dict, registry: dict, vocabulary_catalog: dict) -> None:
    _schema_validate(receipt, "mathematics-engineering-discovery-receipt.schema.json", "MATH_ENG_DISCOVERY_RECEIPT_SCHEMA")
    if receipt != discover_candidates(request, registry, vocabulary_catalog):
        raise MathematicsEngineeringDiscoveryError(
            "MATH_ENG_DISCOVERY_RECEIPT_STALE_OR_FORGED",
            "discovery receipt does not match current request, registry, vocabulary catalog and generated index",
        )


def promote_explicit_selection(discovery_request: dict, discovery_receipt: dict, selection: dict, registry: dict | None = None, vocabulary_catalog: dict | None = None) -> dict:
    _schema_validate(selection, "mathematics-engineering-discovery-selection.schema.json", "MATH_ENG_DISCOVERY_SELECTION_SCHEMA")
    registry = registry or load_engineering(REGISTRY_REL)
    vocabulary_catalog = vocabulary_catalog or _load_vocabulary_catalog()
    _verify_receipt(discovery_request, discovery_receipt, registry, vocabulary_catalog)
    if selection["discovery_id"] != discovery_receipt["discovery_id"]:
        raise MathematicsEngineeringDiscoveryError("MATH_ENG_DISCOVERY_SELECTION_WRONG_RECEIPT", selection["discovery_id"])
    if selection["discovery_receipt_digest"] != digest(discovery_receipt):
        raise MathematicsEngineeringDiscoveryError("MATH_ENG_DISCOVERY_SELECTION_DIGEST_MISMATCH", "selection is not bound to this exact discovery receipt")
    exact = {(row["scope_kind"], row["scope_ref"]) for row in discovery_receipt["candidates"]}
    missing = [ref for ref in selection["selected_scope_refs"] if (selection["selected_scope_kind"], ref) not in exact]
    if missing:
        raise MathematicsEngineeringDiscoveryError("MATH_ENG_DISCOVERY_SELECTION_NOT_CANDIDATE", f"selected exact identities were not in the bound candidate set: {missing}")
    suffix = selection["selection_id"].removeprefix("MATH-ENG-DISC-SEL-")
    request = {
        "schema_version": "1.0.0", "subject": "MATHEMATICS", "request_id": f"MATH-ENG-REQ-DISC_{suffix}",
        "scope_kind": selection["selected_scope_kind"], "scope_refs": list(selection["selected_scope_refs"]),
        "engineering_depth": selection["engineering_depth"], "learning_purpose": selection["learning_purpose"],
        "owner_decision_ref": selection["selection_id"],
    }
    _schema_validate(request, "mathematics-engineering-request.schema.json", "MATH_ENG_DISCOVERY_PROMOTED_REQUEST_SCHEMA")
    return request


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
