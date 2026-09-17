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


def _bound(ref, digest_value, delivery) -> bool:
    return bool(ref and digest_value and delivery == "STATIC")


def _status(doc: dict) -> str:
    c1b_compiled = doc["core1b_lane"]["status"] == "COMPILED"
    c2b_compiled = doc["core2b_lane"]["status"] == "COMPILED"
    c2a_ready = doc["core2a_lane"]["status"] == "LEGAL_POOL_READY"
    ceiling_ready = doc["core2b_compile_ceiling"]["max_demand_level"] is not None

    if c1b_compiled and c2b_compiled:
        return "COMPILED"
    if c1b_compiled or c2b_compiled:
        return "PARTIALLY_COMPILED"
    if c2a_ready and ceiling_ready:
        return "READY_TO_COMPILE"
    return "WAITING_UPSTREAM"


def validate_b_layer_integration(doc: dict) -> None:
    validate_schema(doc, "math-b-layer-integration.schema.json")
    if doc["integration_digest"] != digest(doc, "integration_digest"):
        fail("MATH_B_LAYER_DIGEST_MISMATCH")

    c1a = doc["core1a_authority"]
    if not c1a["authority_ref"] or not c1a["authority_digest"] or not c1a["approved_capability_refs"]:
        fail("MATH_B_LAYER_CORE1A_AUTHORITY_MISSING")

    c1b = doc["core1b_lane"]
    if c1b["status"] == "COMPILED":
        if not _bound(c1b["compiled_plan_ref"], c1b["compiled_plan_digest"], c1b["delivery_mode"]):
            if c1b["delivery_mode"] != "STATIC":
                fail("MATH_B_LAYER_CORE1B_NONSTATIC_DELIVERY")
            fail("MATH_B_LAYER_CORE1B_PRODUCT_BINDING_INCOMPLETE")
    else:
        if any(x is not None for x in [c1b["compiled_plan_ref"], c1b["compiled_plan_digest"], c1b["delivery_mode"]]):
            fail("MATH_B_LAYER_CORE1B_STATE_BINDING_CONFLICT")

    c2a = doc["core2a_lane"]
    pool_ready = c2a["status"] == "LEGAL_POOL_READY"
    if pool_ready:
        if not c2a["legal_pool_ref"] or not c2a["legal_pool_digest"] or not c2a["purpose"]:
            fail("MATH_B_LAYER_CORE2A_POOL_BINDING_INCOMPLETE")
    else:
        if any(x is not None for x in [c2a["legal_pool_ref"], c2a["legal_pool_digest"], c2a["purpose"]]):
            fail("MATH_B_LAYER_CORE2A_POOL_STATE_BINDING_CONFLICT")

    ceiling = doc["core2b_compile_ceiling"]
    ceiling_ready = ceiling["max_demand_level"] is not None
    if ceiling_ready:
        if not ceiling["source_ref"] or not ceiling["source_class"]:
            fail("MATH_B_LAYER_CORE2B_COMPILE_CEILING_MISSING")
    else:
        if ceiling["source_ref"] is not None or ceiling["source_class"] is not None:
            fail("MATH_B_LAYER_CORE2B_CEILING_STATE_BINDING_CONFLICT")

    c2b = doc["core2b_lane"]
    if c2b["status"] == "COMPILED":
        if not pool_ready:
            fail("MATH_B_LAYER_CORE2B_WITHOUT_CORE2A_POOL")
        if not ceiling_ready:
            fail("MATH_B_LAYER_CORE2B_COMPILE_CEILING_MISSING")
        if not _bound(c2b["compiled_plan_ref"], c2b["compiled_plan_digest"], c2b["delivery_mode"]):
            if c2b["delivery_mode"] != "STATIC":
                fail("MATH_B_LAYER_CORE2B_NONSTATIC_DELIVERY")
            fail("MATH_B_LAYER_CORE2B_PRODUCT_BINDING_INCOMPLETE")
    else:
        if any(x is not None for x in [c2b["compiled_plan_ref"], c2b["compiled_plan_digest"], c2b["delivery_mode"]]):
            fail("MATH_B_LAYER_CORE2B_STATE_BINDING_CONFLICT")

    expected = _status(doc)
    if doc["status"] != expected:
        fail("MATH_B_LAYER_STATUS_INCONSISTENT", f"expected={expected},actual={doc['status']}")


def seal_b_layer_integration(draft: dict) -> dict:
    out = copy.deepcopy(draft)
    out.setdefault("schema_version", "2.0.0")
    out.setdefault("subject", "MATHEMATICS")
    out.setdefault("invariants", {
        "a_layers_govern_validity": True,
        "b_layers_are_static_compilers": True,
        "compiled_product_not_learner_evidence": True,
        "core1b_cannot_add_math": True,
        "core2b_requires_core2a_legal_pool": True,
        "core2b_ceiling_is_upstream_compile_input": True,
        "core2b_does_not_require_core1b_product": True,
        "b_layers_do_not_ingest_learner_responses": True,
        "b_layers_do_not_emit_learner_state_transitions": True,
        "b_layers_may_not_rewrite_upstream_learner_state": True,
    })
    out["status"] = _status(out)
    identity = {k: v for k, v in out.items() if k not in {"integration_id", "integration_digest"}}
    out["integration_id"] = "MATH-BI-" + digest(identity)[:16]
    out["integration_digest"] = digest(out, "integration_digest")
    validate_b_layer_integration(out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Mathematics static Core1B/Core2B compiler integration.")
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
    print(json.dumps({"status": "PASS", "integration_id": result["integration_id"], "compiler_status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
