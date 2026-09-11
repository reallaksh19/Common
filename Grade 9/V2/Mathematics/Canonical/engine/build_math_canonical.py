#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "canonical"

def canonical_bytes(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load(name: str):
    return json.loads((CANON / name).read_text(encoding="utf-8"))

def build() -> dict:
    files = [
        "capabilities.v1.json",
        "error_signatures.v1.json",
        "diagnostic_probes.v1.json",
        "reasoning_contracts.v1.json",
    ]
    loaded = {name: load(name) for name in files}
    caps = loaded["capabilities.v1.json"]
    errs = loaded["error_signatures.v1.json"]
    probes = loaded["diagnostic_probes.v1.json"]
    rcs = loaded["reasoning_contracts.v1.json"]

    payload = {
        "package_id": "MATH-V2-CANONICAL-FOUNDATIONS-001",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "registry_version": "MATH-V2-FOUNDATIONS-1.0.0",
        "source_artifacts": [
            {"path": f"canonical/{name}", "sha256": sha256_bytes((CANON / name).read_bytes())}
            for name in files
        ],
        "capability_ids": sorted(row["capability_id"] for row in caps),
        "error_signature_ids": sorted(row["error_signature_id"] for row in errs),
        "diagnostic_probe_ids": sorted(row["probe_id"] for row in probes),
        "reasoning_contract_ids": sorted(row["reasoning_contract_id"] for row in rcs),
        "reasoning_family_refs": sorted({fam for row in caps for fam in row.get("reasoning_family_refs", [])}),
        "benchmark_inputs": [],
    }
    payload["package_digest"] = sha256_bytes(canonical_bytes(payload))
    return payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical_bytes(build()) + b"\n")

if __name__ == "__main__":
    main()
