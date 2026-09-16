#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
REPO = ROOT.parents[3]
SHARED_CROSS = REPO / "Grade 9" / "V2" / "Shared" / "CrossDomain"
SHARED_GATE = REPO / "Grade 9" / "V2" / "Shared" / "EngineeringGate"
sys.path.insert(0, str(ROOT / "engine"))

from build_physics_engineering_gate_registry_v3 import build_registry  # noqa: E402


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def shared_cross_schema(name: str) -> dict[str, Any]:
    return json.loads((SHARED_CROSS / "contracts" / name).read_text(encoding="utf-8"))


def shared_gate_schema(name: str) -> dict[str, Any]:
    return json.loads((SHARED_GATE / "contracts" / name).read_text(encoding="utf-8"))


def load_policy() -> dict[str, Any]:
    return json.loads((SHARED_CROSS / "registry" / "domain-provider-registry.v1.json").read_text(encoding="utf-8"))


def repo_path(ref: str) -> Path:
    rel = Path(ref)
    if rel.is_absolute() or ".." in rel.parts:
        raise AssertionError("DOMAIN_PREREQUISITE_REF_OUTSIDE_REPOSITORY:" + ref)
    path = REPO / rel
    if not path.exists() or not path.is_file():
        raise AssertionError("DOMAIN_PREREQUISITE_REF_MISSING:" + ref)
    return path


def provider_for(prerequisite_id: str) -> dict[str, Any] | None:
    matches = [row for row in load_policy()["providers"] if prerequisite_id.startswith(row["prerequisite_prefix"])]
    if len(matches) > 1:
        raise AssertionError("DOMAIN_PREREQUISITE_PROVIDER_AMBIGUOUS:" + prerequisite_id)
    return matches[0] if matches else None


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9-]+", "-", value).strip("-")


def _registry_context() -> tuple[dict[str, Any], str, tuple[str, ...], str]:
    registry = build_registry()
    registry_id = registry.get("registry_id", "")
    if not registry_id:
        raise AssertionError("ENGINEERING_GATE_REGISTRY_ID_REQUIRED")
    requester_subject = registry_id.split("-", 1)[0]
    gate_prefixes = sorted({gate["subtopic_id"].split("-", 1)[0] for gate in registry["gates"]})
    if not gate_prefixes:
        raise AssertionError("ENGINEERING_GATE_INTERNAL_PREFIX_REQUIRED")
    internal_prefixes = tuple(prefix + "-" for prefix in gate_prefixes)
    receipt_namespace = "-".join(gate_prefixes)
    return registry, requester_subject, internal_prefixes, receipt_namespace


def _closure_validator() -> Draft202012Validator:
    demand = shared_cross_schema("domain-prerequisite-demand.schema.json")
    registry = Registry().with_resource(demand["$id"], Resource.from_contents(demand))
    return Draft202012Validator(shared_gate_schema("domain-prerequisite-closure.schema.json"), registry=registry)


def _verify_authorities(
    authority_receipts: list[dict[str, Any]],
    authority_refs: list[str],
) -> dict[str, dict[str, Any]]:
    if len(authority_receipts) != len(authority_refs):
        raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_SOURCE_REF_REQUIRED")

    validator = Draft202012Validator(shared_cross_schema("domain-prerequisite-authority.schema.json"))
    authorities: dict[str, dict[str, Any]] = {}

    for row, source_ref in zip(authority_receipts, authority_refs, strict=True):
        validator.validate(row)
        pid = row["prerequisite_id"]
        if pid in authorities:
            raise AssertionError("DOMAIN_PREREQUISITE_DUPLICATE_AUTHORITY:" + pid)

        provider = provider_for(pid)
        if provider is None:
            raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_PROVIDER_UNROUTABLE:" + pid)
        if row["provider_subject"] != provider["provider_subject"]:
            raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_PROVIDER_MISMATCH:" + pid)

        provider_root = provider["provider_root"].rstrip("/") + "/"
        if not source_ref.startswith(provider_root):
            raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_NOT_PROVIDER_OWNED:" + pid)

        source_path = repo_path(source_ref)
        source_obj = json.loads(source_path.read_text(encoding="utf-8"))
        if source_obj != row:
            raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_SOURCE_DRIFT:" + pid)

        expected_digest = digest({k: v for k, v in row.items() if k != "receipt_digest"})
        if row["receipt_digest"] != expected_digest:
            raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_DIGEST_MISMATCH:" + pid)

        for evidence_ref in row["evidence_refs"]:
            repo_path(evidence_ref)

        authorities[pid] = {"receipt": row, "source_ref": source_ref}

    return authorities


def compile_domain_prerequisite_closure(
    engineering_receipt: dict[str, Any],
    authority_receipts: list[dict[str, Any]] | None = None,
    authority_refs: list[str] | None = None,
) -> dict[str, Any]:
    authority_receipts = authority_receipts or []
    authority_refs = authority_refs or []
    authorities = _verify_authorities(authority_receipts, authority_refs)
    policy = load_policy()
    registry, requester_subject, internal_prefixes, receipt_namespace = _registry_context()

    gate_map = {gate["subtopic_id"]: gate for gate in registry["gates"]}
    required_by: dict[str, set[str]] = {}
    for gate_id in engineering_receipt["transitive_gate_ids"]:
        gate = gate_map.get(gate_id)
        if not gate:
            continue
        for prerequisite_id in gate["prerequisites"]:
            if prerequisite_id.startswith(internal_prefixes):
                continue
            required_by.setdefault(prerequisite_id, set()).add(gate_id)

    rows: list[dict[str, Any]] = []
    demands: list[dict[str, Any]] = []
    demand_validator = Draft202012Validator(shared_cross_schema("domain-prerequisite-demand.schema.json"))

    for prerequisite_id in sorted(required_by):
        authority = authorities.get(prerequisite_id)
        if authority:
            rows.append({
                "prerequisite_id": prerequisite_id,
                "status": "READY_FROM_AUTHORITATIVE_DOMAIN",
                "authority_ref": authority["source_ref"],
                "demand_id": None,
            })
            continue

        provider = provider_for(prerequisite_id)
        request_suffix = engineering_receipt["request_id"].replace("ENG-REQ-", "", 1)
        demand_id = f"DOMAIN-DEMAND-{receipt_namespace}-" + _slug(request_suffix + "-" + prerequisite_id)
        demand = {
            "schema_version": "1.0.0",
            "demand_id": demand_id,
            "requester_subject": requester_subject,
            "provider_subject": provider["provider_subject"] if provider else None,
            "provider_entrypoint_ref": provider["authority_entrypoint_ref"] if provider else None,
            "prerequisite_id": prerequisite_id,
            "required_by_gate_ids": sorted(required_by[prerequisite_id]),
            "engineering_receipt_ref": engineering_receipt["receipt_id"],
            "engineering_closure_digest": engineering_receipt["closure_digest"],
            "authority_contract_ref": policy["authority_contract_ref"],
            "status": "OPEN_HELD" if provider else "OPEN_UNROUTABLE",
            "demand_digest": "",
        }
        demand["demand_digest"] = digest({k: v for k, v in demand.items() if k != "demand_digest"})
        demand_validator.validate(demand)
        demands.append(demand)
        rows.append({
            "prerequisite_id": prerequisite_id,
            "status": "HELD_NO_DOMAIN_RECEIPT",
            "authority_ref": None,
            "demand_id": demand_id,
        })

    closure_status = "HELD" if demands else "READY"
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": f"DOMAIN-CLOSURE-{receipt_namespace}-" + engineering_receipt["request_id"].replace("ENG-REQ-", "", 1),
        "engineering_receipt_ref": engineering_receipt["receipt_id"],
        "prerequisites": rows,
        "demands": demands,
        "closure_status": closure_status,
        "closure_digest": "",
    }
    receipt["closure_digest"] = digest({k: v for k, v in receipt.items() if k != "closure_digest"})
    _closure_validator().validate(receipt)
    return receipt


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile external-domain prerequisite closure from the active Engineering Gate registry")
    ap.add_argument("engineering_receipt", type=Path)
    ap.add_argument("--authority", action="append", default=[])
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    engineering = json.loads(args.engineering_receipt.read_text(encoding="utf-8"))
    authority_receipts: list[dict[str, Any]] = []
    authority_refs: list[str] = []
    for raw in args.authority:
        path = Path(raw).resolve()
        try:
            ref = path.relative_to(REPO).as_posix()
        except ValueError as exc:
            raise AssertionError("DOMAIN_PREREQUISITE_AUTHORITY_NOT_IN_REPOSITORY:" + raw) from exc
        authority_refs.append(ref)
        authority_receipts.append(json.loads(path.read_text(encoding="utf-8")))

    result = compile_domain_prerequisite_closure(engineering, authority_receipts, authority_refs)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
