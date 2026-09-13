#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import digest, fail, file_digest, load, seal_ground_truth, validate_schema


def build_manifest(spec: dict, *, base_dir: Path) -> dict:
    validate_schema(spec, "math-ground-truth-build-spec.schema.json")
    items = []
    for row in spec["items"]:
        availability = row["availability"]
        source_path = row.get("source_path")
        ref = row.get("ref")
        declared = row.get("declared_digest")

        if availability == "ABSENT":
            if source_path is not None or ref is not None or declared is not None:
                fail("ABSENT_EVIDENCE_HAS_SOURCE_BINDING", row["evidence_type"])
            evidence_ref = None
            evidence_digest = None
        elif source_path:
            path = Path(source_path)
            if not path.is_absolute():
                path = base_dir / path
            if not path.exists() or not path.is_file():
                fail("GROUND_TRUTH_SOURCE_FILE_MISSING", str(path))
            evidence_ref = ref or source_path
            evidence_digest = file_digest(path)
            if declared is not None and declared != evidence_digest:
                fail("GROUND_TRUTH_DECLARED_DIGEST_MISMATCH", row["evidence_type"])
        else:
            if not ref or not declared:
                fail("GROUND_TRUTH_NONLOCAL_BINDING_INCOMPLETE", row["evidence_type"])
            evidence_ref = ref
            evidence_digest = declared

        identity_payload = {
            "evidence_type": row["evidence_type"],
            "authority_class": row["authority_class"],
            "availability": availability,
            "ref": evidence_ref,
            "digest": evidence_digest,
            "source_locator": row.get("source_locator"),
            "scope_refs": sorted(row.get("scope_refs") or []),
        }
        item = {
            "evidence_id": f"GT-{row['evidence_type']}-" + digest(identity_payload)[:16],
            "evidence_type": row["evidence_type"],
            "authority_class": row["authority_class"],
            "availability": availability,
            "ref": evidence_ref,
            "digest": evidence_digest,
            "source_locator": row.get("source_locator"),
            "scope_refs": sorted(set(row.get("scope_refs") or [])),
            "notes": row.get("notes"),
            "conflict_refs": sorted(set(row.get("conflict_refs") or [])),
        }
        items.append(item)

    # Stable ordering keeps manifest identity independent of input-spec row order.
    items.sort(key=lambda x: (x["evidence_type"], x["evidence_id"]))
    manifest = {
        "manifest_id": "",
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "evidence_items": items,
        "manifest_digest": "",
    }
    return seal_ground_truth(manifest)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    spec_path = Path(args.spec)
    manifest = build_manifest(load(spec_path), base_dir=spec_path.resolve().parent)
    Path(args.out).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "manifest_id": manifest["manifest_id"],
        "evidence_count": len(manifest["evidence_items"]),
        "manifest_digest": manifest["manifest_digest"],
    }, indent=2))


if __name__ == "__main__":
    main()
