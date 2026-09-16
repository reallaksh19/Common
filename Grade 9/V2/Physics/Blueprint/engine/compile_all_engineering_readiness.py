#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from compile_engineering_readiness import compile_readiness, render_markdown  # noqa: E402


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def discover_pairs() -> list[tuple[Path, Path]]:
    """Discover canonical subject manifests from repository data, never from case IDs."""
    workbench = ROOT / "fixtures" / "engineering-workbench"
    requests: dict[str, Path] = {}
    manifests: list[tuple[dict, Path]] = []
    for path in sorted(workbench.glob("*.json")):
        try:
            obj = load(path)
        except (OSError, json.JSONDecodeError):
            continue
        if obj.get("schema_version") != "1.0.0":
            continue
        if obj.get("request_id", "").startswith("ENG-REQ-") and obj.get("requested_action") == "AUTO_DISCOVER":
            requests[obj["request_id"]] = path
        # Canonical batch membership is declared by the subject's generated registry.
        # No topic, bucket, subtopic, prerequisite, or downstream consumer is named here.
        if obj.get("manifest_id", "").startswith("ENG-MAN-") and obj.get("registry_ref") == "GENERATED:physics-technical-engineering-gates.v3":
            manifests.append((obj, path))

    pairs: list[tuple[Path, Path]] = []
    for manifest, manifest_path in manifests:
        request_path = requests.get(manifest["request_id"])
        if request_path is None:
            raise AssertionError(f"ENGINEERING_REQUEST_NOT_FOUND:{manifest['request_id']}:{manifest_path.name}")
        pairs.append((request_path, manifest_path))
    if not pairs:
        raise AssertionError("NO_CANONICAL_ENGINEERING_MANIFESTS_DISCOVERED")
    return pairs


def main() -> None:
    ap = argparse.ArgumentParser(description="Compile every canonical subject request/manifest through the global Engineering Gate readiness pipeline")
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for request_path, manifest_path in discover_pairs():
        request, manifest = load(request_path), load(manifest_path)
        engineering, domain, envelope = compile_readiness(request, manifest)
        slug = manifest["manifest_id"].lower()
        out = args.out_dir / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "engineering-closure.json").write_text(json.dumps(engineering, indent=2) + "\n", encoding="utf-8")
        (out / "domain-prerequisite-closure.json").write_text(json.dumps(domain, indent=2) + "\n", encoding="utf-8")
        (out / "engineering-readiness-envelope.json").write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
        (out / "engineering-readiness.md").write_text(render_markdown(envelope), encoding="utf-8")

        # Batch aggregation mirrors the global envelope. Consumer names and statuses
        # are copied from manifest-driven policy output rather than inferred here.
        rows.append({
            "request_id": request["request_id"],
            "manifest_id": manifest["manifest_id"],
            "scope_kind": manifest["scope_kind"],
            "scope_ref": manifest["scope_ref"],
            "engineering_depth": request["engineering_depth"],
            "technical": envelope["dimensions"]["technical"],
            "research_provenance": envelope["dimensions"]["research_provenance"],
            "external_prerequisites": envelope["dimensions"]["external_prerequisites"],
            "source_authority": envelope["dimensions"]["source_authority"],
            "consumer_permissions": envelope["consumer_permissions"],
            "overall_state": envelope["overall_state"],
            "blocker_count": len(envelope["blockers"]),
            "envelope_digest": envelope["envelope_digest"],
        })

    summary = {
        "schema_version": "1.0.0",
        "compiled_count": len(rows),
        "ready_for_technical_consumption": sum(1 for row in rows if row["overall_state"] == "READY_FOR_TECHNICAL_CONSUMPTION"),
        "blocked_count": sum(1 for row in rows if row["overall_state"] == "BLOCKED"),
        "rows": rows,
    }
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    md = ["# Engineering Gate Readiness — canonical subject manifests", ""]
    for row in rows:
        permissions = ", ".join(
            f"{consumer}={permission['status']}"
            for consumer, permission in row["consumer_permissions"].items()
        ) or "none declared"
        md.append(
            f"- `{row['manifest_id']}` / `{row['scope_ref']}` — "
            f"technical={row['technical']}, research={row['research_provenance']}, "
            f"external={row['external_prerequisites']}, source={row['source_authority']}, "
            f"overall={row['overall_state']}, consumers=[{permissions}], blockers={row['blocker_count']}"
        )
    md.append("")
    (args.out_dir / "summary.md").write_text("\n".join(md), encoding="utf-8")
    print(f"Engineering readiness batch: PASS ({len(rows)} canonical manifests compiled; held states remain visible, not hidden)")


if __name__ == "__main__":
    main()
