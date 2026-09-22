#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from v3lib import load_yaml, validate_schema


class CompatibilityError(RuntimeError):
    pass


def _text(value: Any) -> str:
    return str(value or "").strip()


def find_admission(state: dict[str, Any], route_key: str, candidate_id: str) -> dict[str, Any]:
    matches = [
        item
        for item in state.get("takeover_admissions") or []
        if isinstance(item, dict)
        and _text(item.get("route_key")) == route_key
        and _text((item.get("candidate") or {}).get("agent_instance_id")) == candidate_id
    ]
    if len(matches) != 1:
        raise CompatibilityError(
            f"expected one V2.5 takeover admission for {candidate_id} on {route_key}; found {len(matches)}"
        )
    return matches[0]


def build_view(
    root: Path,
    admission: dict[str, Any],
    *,
    validation_status: str,
    validation_basis: list[str],
) -> dict[str, Any]:
    if validation_status not in {"PASS", "FAIL"}:
        raise CompatibilityError("validation_status must be PASS or FAIL")
    certification = admission.get("certification") or {}
    discovery = admission.get("discovery_receipt") or {}
    tc_path = _text(certification.get("path"))
    disc_path = _text(discovery.get("path"))
    if not tc_path or not disc_path:
        raise CompatibilityError("V2.5 admission must point to DISC and TC evidence")
    tc = load_yaml(root / tc_path)
    disc = load_yaml(root / disc_path)
    if _text(tc.get("id")) != _text(certification.get("id")):
        raise CompatibilityError("V2.5 TC pointer does not match certification file")
    if _text(disc.get("id")) != _text(discovery.get("id")):
        raise CompatibilityError("V2.5 DISC pointer does not match discovery file")

    candidate = _text((admission.get("candidate") or {}).get("agent_instance_id"))
    if _text((tc.get("candidate") or {}).get("agent_instance_id")) != candidate:
        raise CompatibilityError("V2.5 TC candidate disagrees with takeover admission")
    if _text((disc.get("candidate") or {}).get("agent_instance_id")) != candidate:
        raise CompatibilityError("V2.5 DISC candidate disagrees with takeover admission")

    qual = tc.get("qualification") or {}
    qualification_required = qual.get("required") is True
    qpath = _text(qual.get("receipt_path")) if qualification_required else ""
    qstatus = "NOT_REQUIRED"
    if qualification_required:
        if not qpath:
            raise CompatibilityError("V2.5 TC requires qualification but has no receipt path")
        qreceipt = load_yaml(root / qpath)
        if qreceipt.get("result") == "PASS" and qual.get("status") == "PASS":
            qstatus = "PASS"
        else:
            validation_status = "FAIL"

    if tc.get("result") != "PASS" or disc.get("result") != "PASS":
        validation_status = "FAIL"

    basis = tc.get("basis") or {}
    route = tc.get("route") or {}
    view = {
        "schema_version": "relay-v3-v25-lease-view",
        "authority": "DERIVED_COMPATIBILITY_VIEW",
        "source_protocol": "2.5",
        "native_lease": False,
        "may_authorize_v3_actions": False,
        "route": _text(admission.get("route_key")),
        "executor": candidate,
        "basis": {
            "ep_id": _text(route.get("ep_id")),
            "material_ref": _text(basis.get("material_ref")),
            "roadmap_revision": _text(basis.get("roadmap_revision")),
            "protocol_basis": _text(basis.get("relay_protocol_basis_ref")),
        },
        "qualification": {
            "required": qualification_required,
            "status": qstatus,
            "receipt": qpath or None,
        },
        "source_evidence": {
            "discovery": disc_path,
            "qualification": qpath or None,
            "certification": tc_path,
        },
        "validation": {
            "status": validation_status,
            "basis": list(validation_basis),
        },
    }
    errors = validate_schema("v25-lease-view", view, "V25_LEASE_VIEW")
    if errors:
        raise CompatibilityError("; ".join(errors))
    return view


def validate_live_v25(root: Path) -> tuple[str, list[str]]:
    validator = root / "skills/engineering-pr-delivery-v2.5/scripts/validate_takeover_certification.py"
    if not validator.exists():
        return "FAIL", ["V2.5 takeover validator is unavailable"]
    proc = subprocess.run(
        [sys.executable, str(validator), str(root)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    basis = [f"validate_takeover_certification.py exit={proc.returncode}"]
    basis.extend(output[-10:] or ["validator produced no output"])
    return ("PASS" if proc.returncode == 0 else "FAIL"), basis


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read validated V2.5 takeover evidence as a non-authoritative V3 compatibility lease view."
    )
    parser.add_argument("repo_root", nargs="?", default=".")
    parser.add_argument("--route-key", required=True)
    parser.add_argument("--candidate-id", required=True)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    state = load_yaml(root / "agents/relay/REPO_STATE.yaml")
    admission = find_admission(state, args.route_key, args.candidate_id)
    status, basis = validate_live_v25(root)
    view = build_view(root, admission, validation_status=status, validation_basis=basis)
    print(yaml.safe_dump(view, sort_keys=False), end="")
    raise SystemExit(0 if view["validation"]["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
