#!/usr/bin/env python3
"""Chemistry Engineering Discovery Compiler.

Implements non-authoritative candidate discovery across all registered
Chemistry technical engineering gates (Grades 9 to 11).
Computes deterministic relevance scores using token overlap, sequence matching,
and the chemistry engineering discovery vocabulary catalog.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_REL = "policies/chemistry-technical-engineering-gates.v1.json"
VOCABULARY_REL = "policies/chemistry-engineering-discovery-vocabulary.v1.json"
VOCABULARY_SCHEMA = "chemistry-engineering-discovery-vocabulary.schema.json"


class ChemistryEngineeringDiscoveryError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def canonical(val: Any) -> str:
    return json.dumps(val, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(val: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(val).encode("utf-8")).hexdigest()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_engineering(path_rel: str = REGISTRY_REL) -> dict:
    return _load_json(ROOT / path_rel)


def _schema_validate(doc: dict, schema_name: str, code: str) -> None:
    schema = _load_json(ROOT / "contracts" / schema_name)
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        e = errors[0]
        raise ChemistryEngineeringDiscoveryError(code, f"{e.message}; path={list(e.path)}")


def _normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def _tokens(value: str) -> set[str]:
    stop = {"a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with", "is", "are"}
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


def validate_discovery_vocabulary_catalog(catalog: dict, registry: dict) -> dict:
    _schema_validate(catalog, VOCABULARY_SCHEMA, "CHEM_ENG_DISCOVERY_VOCABULARY_SCHEMA")
    if catalog["registry_id"] != registry.get("registry_id"):
        raise ChemistryEngineeringDiscoveryError(
            "CHEM_ENG_DISCOVERY_VOCABULARY_REGISTRY_ID_MISMATCH",
            f"catalog={catalog['registry_id']} registry={registry.get('registry_id')}",
        )
    known = {gate["subtopic_id"] for gate in registry.get("subtopic_gates") or []}
    catalog_targets = set()
    term_count = 0
    for entry in catalog["entries"]:
        ref = entry["target_scope_ref"]
        if entry["target_scope_kind"] == "ENGINEERING_GATE" and ref not in known:
            raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_VOCABULARY_TARGET_UNKNOWN", ref)
        if ref in catalog_targets:
            raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_VOCABULARY_TARGET_DUPLICATE", ref)
        catalog_targets.add(ref)
        terms = entry["terms"]
        term_count += len(terms)
        phrases = [t["phrase"].strip().lower() for t in terms]
        if len(phrases) != len(set(phrases)):
            raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_VOCABULARY_PHRASE_DUPLICATE", ref)
    missing = sorted(known - catalog_targets)
    if missing:
        raise ChemistryEngineeringDiscoveryError(
            "CHEM_ENG_DISCOVERY_VOCABULARY_TARGET_MISSING",
            f"missing={missing[:5]} (total {len(missing)})",
        )
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
    vocab_path = ROOT / VOCABULARY_REL
    return _load_json(vocab_path)


def _vocabulary_by_target(catalog: dict) -> dict[str, list[dict]]:
    return {entry["target_scope_ref"]: list(entry["terms"]) for entry in catalog["entries"]}


def _build_discovery_index(registry: dict, catalog: dict) -> dict:
    vocabulary = _vocabulary_by_target(catalog)
    entries: list[dict] = []
    for gate in sorted(registry.get("subtopic_gates") or [], key=lambda x: x["subtopic_id"]):
        gid = gate["subtopic_id"]
        title = gate.get("learner_title") or gate.get("canonical_title") or gate["subtopic_title"]
        entries.append({
            "scope_kind": "ENGINEERING_GATE",
            "scope_ref": gid,
            "learner_label": title,
            "linked_gate_ids": [gid],
            "content_digest": digest(_flatten_strings(gate)),
            "vocabulary_terms": vocabulary.get(gid, []),
        })
    return {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
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
    linked_gate_text: bool = False,
) -> tuple[float, list[str], list[str]]:
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
            local += 1000.0
            _add_once(basis, "EXACT_IDENTITY")
        if term == label_norm:
            local += 800.0
            _add_once(basis, "EXACT_LABEL")
        elif term in label_norm:
            local += 300.0
            _add_once(basis, "LABEL_PHRASE")

        overlap = term_tokens & identity_tokens
        if overlap:
            local += 80.0 * len(overlap)
            _add_once(basis, "IDENTITY_TOKEN")

        overlap = term_tokens & label_tokens
        if overlap:
            local += 50.0 * len(overlap)
            _add_once(basis, "LABEL_TOKEN")

        overlap = term_tokens & content_tokens
        if overlap:
            local += 12.0 * len(overlap)
            _add_once(basis, "CONTENT_TOKEN")

        ratio = SequenceMatcher(None, term, label_norm).ratio()
        if ratio >= 0.72:
            local += 120.0 * ratio
            _add_once(basis, "APPROXIMATE_LABEL")

        for phrase, phrase_norm, phrase_tokens in vocabulary_rows:
            if term == phrase_norm:
                local += 450.0
                _add_once(basis, "VOCABULARY_EXACT")
                _add_once(matched, phrase)
            elif term in phrase_norm or phrase_norm in term:
                local += 180.0
                _add_once(basis, "VOCABULARY_PHRASE")
                _add_once(matched, phrase)
            v_overlap = term_tokens & phrase_tokens
            if v_overlap:
                local += 40.0 * len(v_overlap)
                _add_once(basis, "VOCABULARY_TOKEN")
                _add_once(matched, phrase)
            v_ratio = SequenceMatcher(None, term, phrase_norm).ratio()
            if v_ratio >= 0.80:
                local += 80.0 * v_ratio
                _add_once(basis, "APPROXIMATE_VOCABULARY")
                _add_once(matched, phrase)

        if index > 0 and local > 0.0:
            _add_once(basis, "HINT_MATCH")

        weight = 1.0 if index == 0 else 0.45
        total += local * weight

    if linked_gate_text and total > 0.0:
        _add_once(basis, "LINKED_GATE_TEXT")

    return round(total, 4), basis, matched


def _gate_candidate(gate: dict, query: str, hints: list[str], vocabulary_terms: list[dict]) -> dict | None:
    gid = gate["subtopic_id"]
    title = gate.get("learner_title") or gate.get("canonical_title") or gate["subtopic_title"]
    score, basis, matched = _score(query, hints, gid, title, _flatten_strings(gate), vocabulary_terms)
    if score <= 0:
        return None
    return {
        "scope_kind": "ENGINEERING_GATE",
        "scope_ref": gid,
        "learner_label": title,
        "score": score,
        "match_basis": basis,
        "matched_vocabulary_terms": matched,
        "declared_technical_readiness": gate.get("technical_readiness", "UNDECLARED"),
        "source_scope": gate.get("provenance", {}).get("source_scope", "UNDECLARED"),
    }


def _bucket_map(registry: dict) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {}
    for gate in registry.get("subtopic_gates") or []:
        for bucket in gate.get("linked_buckets") or []:
            buckets.setdefault(bucket, []).append(gate)
    return buckets


def _bucket_candidate(bucket_id: str, linked: list[dict], query: str, hints: list[str], vocabulary_terms: list[dict]) -> dict | None:
    gates = sorted(linked, key=lambda x: x["subtopic_id"])
    label = " / ".join(dict.fromkeys(g.get("learner_title") or g.get("canonical_title") or g["subtopic_title"] for g in gates))
    content = [text for g in gates for text in _flatten_strings(g)]
    score, basis, matched = _score(query, hints, bucket_id, label, content, vocabulary_terms, linked_gate_text=True)
    if score <= 0:
        return None
    readiness = {g.get("technical_readiness", "UNDECLARED") for g in gates}
    scopes = {g.get("provenance", {}).get("source_scope", "UNDECLARED") for g in gates}
    return {
        "scope_kind": "BUCKET",
        "scope_ref": bucket_id,
        "learner_label": label,
        "score": score,
        "match_basis": basis,
        "matched_vocabulary_terms": matched,
        "declared_technical_readiness": next(iter(readiness)) if len(readiness) == 1 else "MIXED",
        "source_scope": next(iter(scopes)) if len(scopes) == 1 else "MIXED",
    }


def discover_candidates(request: dict, registry: dict | None = None, vocabulary_catalog: dict | None = None) -> dict:
    _schema_validate(request, "chemistry-engineering-discovery-request.schema.json", "CHEM_ENG_DISCOVERY_REQUEST_SCHEMA")
    registry = registry or load_engineering(REGISTRY_REL)
    if registry.get("registry_id") != "CHEM-G9-11-TECHNICAL-ENGINEERING-GATES-v1":
        raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_REGISTRY_ID_MISMATCH", str(registry.get("registry_id")))
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
            candidate = _gate_candidate(gate, query, hints, vocabulary.get(gate["subtopic_id"], []))
            if candidate:
                rows.append(candidate)

    if "BUCKET" in kinds:
        for bucket_id, linked in _bucket_map(registry).items():
            candidate = _bucket_candidate(bucket_id, linked, query, hints, vocabulary.get(bucket_id, []))
            if candidate:
                rows.append(candidate)

    rows.sort(key=lambda row: (-row["score"], row["scope_kind"], row["scope_ref"]))
    rows = rows[: request.get("max_candidates", 6)]
    for rank, row in enumerate(rows, 1):
        row["rank"] = rank

    suffix = request["discovery_request_id"].removeprefix("CHEM-ENG-DISC-REQ-")
    receipt = {
        "schema_version": "1.1.0",
        "subject": "CHEMISTRY",
        "discovery_id": f"CHEM-ENG-DISC-{suffix}",
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
        "candidate_kinds": kinds,
        "candidate_count": len(rows),
        "candidates": rows,
    }
    _schema_validate(receipt, "chemistry-engineering-discovery-receipt.schema.json", "CHEM_ENG_DISCOVERY_RECEIPT_SCHEMA")
    return receipt


def _verify_receipt(request: dict, receipt: dict, registry: dict, vocabulary_catalog: dict) -> None:
    recomputed = discover_candidates(request, registry, vocabulary_catalog)
    if digest(recomputed) != digest(receipt):
        raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_RECEIPT_TAMPERED", "Receipt does not match request")


def promote_explicit_selection(
    selection: dict,
    request: dict,
    receipt: dict,
    registry: dict | None = None,
    vocabulary_catalog: dict | None = None,
) -> dict:
    _schema_validate(selection, "chemistry-engineering-discovery-selection.schema.json", "CHEM_ENG_DISCOVERY_SELECTION_SCHEMA")
    _schema_validate(request, "chemistry-engineering-discovery-request.schema.json", "CHEM_ENG_DISCOVERY_REQUEST_SCHEMA")
    _schema_validate(receipt, "chemistry-engineering-discovery-receipt.schema.json", "CHEM_ENG_DISCOVERY_RECEIPT_SCHEMA")

    registry = registry or load_engineering(REGISTRY_REL)
    vocabulary_catalog = vocabulary_catalog or _load_vocabulary_catalog()
    _verify_receipt(request, receipt, registry, vocabulary_catalog)

    if selection["discovery_id"] != receipt["discovery_id"]:
        raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_SELECTION_MISMATCH", "discovery_id mismatch")
    if selection["discovery_receipt_digest"] != digest(receipt):
        raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_SELECTION_DIGEST_MISMATCH", "receipt digest mismatch")

    candidates_by_ref = {c["scope_ref"]: c for c in receipt["candidates"] if c["scope_kind"] == selection["selected_scope_kind"]}
    for ref in selection["selected_scope_refs"]:
        if ref not in candidates_by_ref:
            raise ChemistryEngineeringDiscoveryError("CHEM_ENG_DISCOVERY_SELECTION_NOT_IN_RECEIPT", ref)

    return {
        "status": "PASS",
        "subject": "CHEMISTRY",
        "selection_id": selection["selection_id"],
        "discovery_id": selection["discovery_id"],
        "selected_scope_kind": selection["selected_scope_kind"],
        "selected_scope_refs": selection["selected_scope_refs"],
        "engineering_depth": selection["engineering_depth"],
        "learning_purpose": selection["learning_purpose"],
        "technical_authorization": "ALLOWED_FOR_DOWNSTREAM_MANIFEST",
        "publication_authorization": "NOT_IMPLIED",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Chemistry Engineering Discovery Compiler")
    ap.add_argument("--query", required=True)
    ap.add_argument("--hint", action="append", default=[])
    ap.add_argument("--out", help="Write receipt to JSON file")
    args = ap.parse_args()

    req = {
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "discovery_request_id": f"CHEM-ENG-DISC-REQ-{hashlib.sha256(args.query.encode()).hexdigest()[:8].upper()}",
        "query": args.query,
        "hints": args.hint,
        "candidate_kinds": ["ENGINEERING_GATE", "BUCKET"],
        "max_candidates": 6,
    }
    receipt = discover_candidates(req)
    out_str = json.dumps(receipt, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(out_str + "\n", encoding="utf-8")
        print(f"Receipt written to {args.out}")
    else:
        print(out_str)


if __name__ == "__main__":
    main()
