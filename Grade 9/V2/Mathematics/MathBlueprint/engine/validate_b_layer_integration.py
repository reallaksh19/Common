#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import digest, fail, load, validate_schema


def _status(doc: dict) -> str:
    c1b = doc["core1b_lane"]["status"]
    c2a = doc["core2a_lane"]["status"]
    c2b = doc["core2b_lane"]["status"]
    if c2b == "ACTIVE":
        return "CORE2B_ACTIVE"
    if c1b == "RELEASED" and c2a == "LEGAL_POOL_READY":
        return "CORE2B_READY"
    if c1b != "RELEASED":
        return "WAITING_FOR_CORE1B"
    return "WAITING_FOR_CORE2A"


def validate_b_layer_integration(doc: dict) -> None:
    validate_schema(doc, "math-b-layer-integration.schema.json")
    if doc["integration_digest"] != digest(doc, "integration_digest"):
        fail("MATH_B_LAYER_DIGEST_MISMATCH")

    realization = doc["core1a_realization"]
    if doc["execution_class"] == "PRODUCTION":
        if realization["manifest_origin"] != "RENDERER_EMITTED":
            fail("MATH_B_LAYER_TEST_FIXTURE_MANIFEST_USED_IN_PRODUCTION")
        if realization["semantic_binding"] != "SEMANTIC_COMPONENT_DIGESTS":
            fail("MATH_B_LAYER_PRODUCTION_SURFACE_SEMANTIC_BINDING_MISSING")

    c1b = doc["core1b_lane"]
    c2a = doc["core2a_lane"]
    c2b = doc["core2b_lane"]

    if c1b["status"] == "RELEASED" and not c1b["release_receipt_refs"]:
        fail("MATH_B_LAYER_CORE1B_RELEASE_RECEIPT_MISSING")
    if c1b["status"] in {"EXPOSURE_VERIFIED", "EVIDENCE_AVAILABLE", "RELEASED"} and not c1b["exposure_receipt_refs"]:
        fail("MATH_B_LAYER_CORE1B_EXPOSURE_RECEIPT_MISSING")
    if c1b["status"] in {"EVIDENCE_AVAILABLE", "RELEASED"} and not c1b["learner_evidence_refs"]:
        fail("MATH_B_LAYER_CORE1B_LEARNER_EVIDENCE_MISSING")

    pool_ready = c2a["status"] == "LEGAL_POOL_READY"
    if pool_ready and (not c2a["legal_pool_ref"] or not c2a["legal_pool_digest"]):
        fail("MATH_B_LAYER_CORE2A_POOL_BINDING_INCOMPLETE")
    if not pool_ready and (c2a["legal_pool_ref"] is not None or c2a["legal_pool_digest"] is not None):
        fail("MATH_B_LAYER_CORE2A_POOL_STATE_BINDING_CONFLICT")

    if c2b["status"] in {"READY", "ACTIVE"}:
        if c1b["status"] != "RELEASED":
            fail("MATH_B_LAYER_CORE2B_WITHOUT_CORE1B_RELEASE")
        if not pool_ready:
            fail("MATH_B_LAYER_CORE2B_WITHOUT_CORE2A_POOL")
        if not c2b["session_ref"]:
            fail("MATH_B_LAYER_CORE2B_SESSION_MISSING")

    expected = _status(doc)
    if doc["status"] != expected:
        fail("MATH_B_LAYER_STATUS_INCONSISTENT", f"expected={expected},actual={doc['status']}")


def seal_b_layer_integration(draft: dict) -> dict:
    out = copy.deepcopy(draft)
    out.setdefault("schema_version", "1.0.0")
    out.setdefault("subject", "MATHEMATICS")
    out.setdefault("invariants", {
        "planned_not_realized": True,
        "realized_not_evidenced": True,
        "core2a_legality_not_core2b_readiness": True,
        "core2b_requires_core1b_release": True,
        "core2b_requires_core2a_legal_pool": True,
        "core2b_items_must_resolve_in_bound_core2a_pool": True,
        "b_layer_may_not_rewrite_upstream_learner_state": True,
    })
    out["status"] = _status(out)
    identity = {k: v for k, v in out.items() if k not in {"integration_id", "integration_digest"}}
    out["integration_id"] = "MATH-BI-" + digest(identity)[:16]
    out["integration_digest"] = digest(out, "integration_digest")
    validate_b_layer_integration(out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Mathematics Core1B/Core2B blueprint integration boundary.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    draft = load(args.input)
    if draft.get("integration_id") and draft.get("integration_digest"):
        validate_b_layer_integration(draft)
        result = draft
    else:
        result = seal_b_layer_integration(draft)
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "integration_id": result["integration_id"], "runtime_status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
