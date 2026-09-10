#!/usr/bin/env python3
"""Bind a Core (2) publication request to a frozen Core (1) research package.

This utility performs no subject research. It materializes the v1 PublicationTarget
identity fields from ResearchBundleManifest + LearnerProfile and leaves all
purpose/product choices to the supplied request.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--learner", type=Path, required=True)
    ap.add_argument("--request", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    manifest = load(args.manifest)
    learner = load(args.learner)
    request = load(args.request)

    target = {
        "publication_target_id": request["publication_target_id"],
        "schema_version": "1.0.0",
        "research_bundle_id": manifest["research_bundle_id"],
        "research_package_digest": manifest["package_digest"],
        "learner_profile_id": learner["learner_profile_id"],
        "purpose": request["purpose"],
        "requested_products": request["requested_products"],
    }
    if "publication_profile" in request:
        target["publication_profile"] = request["publication_profile"]

    write(args.out, target)
    print(f"PUBLICATION_TARGET_BOUND = PASS")
    print(f"RESEARCH_BUNDLE_ID = {target['research_bundle_id']}")
    print(f"RESEARCH_PACKAGE_DIGEST = {target['research_package_digest']}")
    print(f"LEARNER_PROFILE_ID = {target['learner_profile_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
