#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
sys.path.insert(0, str(ROOT / "engine"))

from compile_domain_prerequisite_closure import compile_domain_prerequisite_closure  # noqa: E402
from compile_engineering_closure import compile_closure, load  # noqa: E402


class EngineeringReadinessError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def _research_state(request: dict, engineering_receipt: dict) -> str:
    if request["engineering_depth"] != "RESEARCH":
        return "NOT_REQUIRED"
    research_codes = {
        "E_ENG_RESEARCH_DOSSIER_REQUIRED",
        "E_ENG_RESEARCH_DOSSIER_INVALID",
        "E_ENG_CLAIM_LEDGER_REQUIRED",
        "E_ENG_CLAIM_LEDGER_INVALID",
    }
    return "BLOCKED" if any(row["code"] in research_codes for row in engineering_receipt["blockers"]) else "READY"


def _source_state(source_item_status: str) -> str:
    return {
        "SOURCE_READY": "READY",
        "SOURCE_HELD": "HELD",
        "INDEPENDENT_OF_TECHNICAL_GATE": "NOT_APPLICABLE",
    }[source_item_status]


def build_envelope(request: dict, engineering_receipt: dict, domain_receipt: dict) -> dict:
    if request["request_id"] != engineering_receipt["request_id"]:
        raise EngineeringReadinessError("E_ENG_READY_REQUEST_MISMATCH", "engineering receipt belongs to another request")
    if domain_receipt["engineering_receipt_ref"] != engineering_receipt["receipt_id"]:
        raise EngineeringReadinessError("E_ENG_READY_DOMAIN_MISMATCH", "domain closure is not bound to the engineering receipt")

    blockers: list[dict] = []
    research_codes = {
        "E_ENG_RESEARCH_DOSSIER_REQUIRED",
        "E_ENG_RESEARCH_DOSSIER_INVALID",
        "E_ENG_CLAIM_LEDGER_REQUIRED",
        "E_ENG_CLAIM_LEDGER_INVALID",
    }
    for row in engineering_receipt["blockers"]:
        blockers.append({
            "code": row["code"],
            "dimension": "RESEARCH_PROVENANCE" if row["code"] in research_codes else "PHYSICS_TECHNICAL",
            "ref": row.get("gate_id"),
            "message": row["message"],
        })
    for row in domain_receipt["prerequisites"]:
        if row["status"] != "READY_FROM_AUTHORITATIVE_DOMAIN":
            blockers.append({
                "code": "E_ENG_EXTERNAL_PREREQUISITE_HELD",
                "dimension": "EXTERNAL_PREREQUISITES",
                "ref": row["prerequisite_id"],
                "message": f"{row['prerequisite_id']} has no provider-owned authoritative-domain receipt",
            })

    technical_ready = engineering_receipt["closure_status"] == "READY"
    external_ready = domain_receipt["closure_status"] == "READY"
    consumable = technical_ready and external_ready
    reason_codes = sorted({row["code"] for row in blockers})

    permissions = {}
    for consumer in ["CCU", "CORE1A", "CORE1B", "CORE2A", "CORE2B"]:
        permissions[consumer] = {
            "status": "ALLOWED" if consumable else "BLOCKED",
            "reason_codes": [] if consumable else reason_codes,
        }
    permissions["PUBLICATION"] = {
        "status": "NOT_AUTHORIZED",
        "reason_codes": ["ENGINEERING_DOES_NOT_AUTHORIZE_PUBLICATION"],
    }

    if consumable:
        next_action = "Technical consumers may proceed; pedagogy, learner evidence, transfer legality and publication remain independently governed."
    elif blockers:
        next_action = blockers[0]["message"]
    else:
        next_action = "Resolve engineering readiness blockers and recompile the envelope."

    envelope = {
        "schema_version": "1.0.0",
        "envelope_id": engineering_receipt["receipt_id"].replace("ENG-CLOSURE-", "ENG-READY-", 1),
        "request_id": request["request_id"],
        "manifest_id": engineering_receipt["manifest_id"],
        "engineering_receipt": {
            "receipt_id": engineering_receipt["receipt_id"],
            "closure_digest": engineering_receipt["closure_digest"],
            "closure_status": engineering_receipt["closure_status"],
            "source_item_status": engineering_receipt["source_item_status"],
        },
        "domain_receipt": {
            "receipt_id": domain_receipt["receipt_id"],
            "closure_digest": domain_receipt["closure_digest"],
            "closure_status": domain_receipt["closure_status"],
            "prerequisite_count": len(domain_receipt["prerequisites"]),
            "held_count": sum(1 for row in domain_receipt["prerequisites"] if row["status"] != "READY_FROM_AUTHORITATIVE_DOMAIN"),
        },
        "dimensions": {
            "physics_technical": "READY" if technical_ready else "BLOCKED",
            "research_provenance": _research_state(request, engineering_receipt),
            "external_prerequisites": "READY" if external_ready else "HELD",
            "source_authority": _source_state(engineering_receipt["source_item_status"]),
        },
        "consumer_permissions": permissions,
        "overall_state": "READY_FOR_TECHNICAL_CONSUMPTION" if consumable else "BLOCKED",
        "publication_authorization": "NOT_IMPLIED",
        "blockers": blockers,
        "next_action": next_action,
        "envelope_digest": "",
    }
    envelope["envelope_digest"] = digest({k: v for k, v in envelope.items() if k != "envelope_digest"})
    jsonschema.validate(envelope, load("contracts/engineering-readiness-envelope.schema.json"))
    return envelope


def compile_readiness(
    request: dict,
    manifest: dict,
    *,
    authority_receipts: list[dict] | None = None,
    authority_refs: list[str] | None = None,
) -> tuple[dict, dict, dict]:
    engineering = compile_closure(request, manifest)
    domain = compile_domain_prerequisite_closure(
        engineering,
        authority_receipts=authority_receipts or [],
        authority_refs=authority_refs or [],
    )
    return engineering, domain, build_envelope(request, engineering, domain)


def render_markdown(envelope: dict) -> str:
    lines = [
        "# Physics Engineering Readiness",
        "",
        f"- **Overall:** {envelope['overall_state']}",
        f"- **Physics technical:** {envelope['dimensions']['physics_technical']}",
        f"- **Research provenance:** {envelope['dimensions']['research_provenance']}",
        f"- **External prerequisites:** {envelope['dimensions']['external_prerequisites']}",
        f"- **Source authority:** {envelope['dimensions']['source_authority']}",
        f"- **Publication authorization:** {envelope['publication_authorization']}",
        "",
        "## Consumer permissions",
        "",
    ]
    for consumer, row in envelope["consumer_permissions"].items():
        reasons = ", ".join(row["reason_codes"]) if row["reason_codes"] else "none"
        lines.append(f"- **{consumer}:** {row['status']} — {reasons}")
    lines.extend(["", "## Blockers", ""])
    if envelope["blockers"]:
        for row in envelope["blockers"]:
            ref = f" `{row['ref']}`" if row.get("ref") else ""
            lines.append(f"- **{row['dimension']} / {row['code']}**{ref}: {row['message']}")
    else:
        lines.append("- None.")
    lines.extend(["", "## Next action", "", envelope["next_action"], ""])
    return "\n".join(lines)


def _authority_inputs(raw_refs: list[str]) -> tuple[list[dict], list[str]]:
    receipts: list[dict] = []
    refs: list[str] = []
    for raw in raw_refs:
        path = Path(raw).resolve()
        try:
            ref = path.relative_to(REPO).as_posix()
        except ValueError as exc:
            raise EngineeringReadinessError("E_ENG_READY_AUTHORITY_OUTSIDE_REPO", raw) from exc
        refs.append(ref)
        receipts.append(json.loads(path.read_text(encoding="utf-8")))
    return receipts, refs


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile the aggregate Physics Engineering Readiness Envelope")
    ap.add_argument("request")
    ap.add_argument("manifest")
    ap.add_argument("--authority", action="append", default=[])
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--require-consumer", choices=["CCU", "CORE1A", "CORE1B", "CORE2A", "CORE2B"])
    args = ap.parse_args()

    receipts, refs = _authority_inputs(args.authority)
    engineering, domain, envelope = compile_readiness(
        load(args.request), load(args.manifest), authority_receipts=receipts, authority_refs=refs
    )
    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "engineering-closure.json").write_text(json.dumps(engineering, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "domain-prerequisite-closure.json").write_text(json.dumps(domain, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "engineering-readiness-envelope.json").write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "engineering-readiness.md").write_text(render_markdown(envelope), encoding="utf-8")
    else:
        print(json.dumps(envelope, indent=2))

    if args.require_consumer and envelope["consumer_permissions"][args.require_consumer]["status"] != "ALLOWED":
        raise EngineeringReadinessError(
            "E_ENG_READY_CONSUMER_BLOCKED",
            f"{args.require_consumer} blocked by {envelope['consumer_permissions'][args.require_consumer]['reason_codes']}",
        )


if __name__ == "__main__":
    main()
