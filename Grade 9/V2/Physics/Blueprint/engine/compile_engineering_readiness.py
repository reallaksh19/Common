#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
SHARED_ENGINEERING_GATE = REPO / "Grade 9" / "V2" / "Shared" / "EngineeringGate" / "engine"
sys.path.insert(0, str(ROOT / "engine"))
sys.path.insert(0, str(SHARED_ENGINEERING_GATE))

from compile_domain_prerequisite_closure import compile_domain_prerequisite_closure  # noqa: E402
from compile_engineering_closure import compile_closure, load  # noqa: E402
from evaluate_readiness import (  # noqa: E402
    EngineeringGateError,
    build_envelope as build_global_envelope,
    render_markdown,
    require_consumer,
)

EngineeringReadinessError = EngineeringGateError


def build_envelope(request: dict, manifest: dict, engineering_receipt: dict, domain_receipt: dict) -> dict:
    """Compatibility adapter. Readiness authority lives in Shared/EngineeringGate."""
    return build_global_envelope(request, manifest, engineering_receipt, domain_receipt)


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
    return engineering, domain, build_global_envelope(request, manifest, engineering, domain)


def _authority_inputs(raw_refs: list[str]) -> tuple[list[dict], list[str]]:
    receipts: list[dict] = []
    refs: list[str] = []
    for raw in raw_refs:
        path = Path(raw).resolve()
        try:
            ref = path.relative_to(REPO).as_posix()
        except ValueError as exc:
            raise EngineeringGateError("E_ENG_GATE_AUTHORITY_OUTSIDE_REPO", raw) from exc
        refs.append(ref)
        receipts.append(json.loads(path.read_text(encoding="utf-8")))
    return receipts, refs


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile receipts, then consume the global Engineering Gate readiness authority")
    ap.add_argument("request")
    ap.add_argument("manifest")
    ap.add_argument("--authority", action="append", default=[])
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--require-consumer")
    args = ap.parse_args()

    request = load(args.request)
    manifest = load(args.manifest)
    receipts, refs = _authority_inputs(args.authority)
    engineering, domain, envelope = compile_readiness(
        request, manifest, authority_receipts=receipts, authority_refs=refs
    )
    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "engineering-closure.json").write_text(json.dumps(engineering, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "domain-prerequisite-closure.json").write_text(json.dumps(domain, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "engineering-readiness-envelope.json").write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "engineering-readiness.md").write_text(render_markdown(envelope), encoding="utf-8")
    else:
        print(json.dumps(envelope, indent=2))

    if args.require_consumer:
        require_consumer(envelope, args.require_consumer)


if __name__ == "__main__":
    main()
