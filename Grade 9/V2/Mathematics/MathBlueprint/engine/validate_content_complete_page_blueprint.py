#!/usr/bin/env python3
"""Fail-closed gate for publication-ready Mathematics LearnerPageBlueprints.

The structural page-blueprint contract proves technical composition. This gate adds
one publication invariant: every learner-visible content block must carry its exact
render payload inside the Blueprint. A renderer may format these nodes; it may not
invent explanatory text, mathematics, hints, questions, answers or checks.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import fail, load
from validate_learner_page_blueprint import validate_page_blueprint

ALLOWED_NODE_TYPES = {
    "HEADING", "PARAGRAPH", "BULLET", "MATH", "QUESTION", "STEP",
    "HINT", "ANSWER", "CHECK", "SOURCE", "LABEL",
}


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _content_blocks(page: dict):
    yield from page.get("technical_blocks", [])
    yield from page.get("prose_blocks", [])


def _validate_node(node: dict, block_id: str) -> None:
    if not isinstance(node, dict):
        fail("MATH_BLUEPRINT_RENDER_NODE_INVALID", block_id)
    ntype = node.get("type")
    if ntype not in ALLOWED_NODE_TYPES:
        fail("MATH_BLUEPRINT_RENDER_NODE_TYPE_INVALID", f"{block_id}:{ntype}")
    text = node.get("text")
    if not isinstance(text, str) or not text.strip():
        fail("MATH_BLUEPRINT_RENDER_NODE_TEXT_REQUIRED", f"{block_id}:{ntype}")


def validate_content_complete_blueprint(doc: dict) -> dict:
    validate_page_blueprint(doc)
    block_count = 0
    rendered_ids = set()

    for page in doc["pages"]:
        for block in _content_blocks(page):
            block_id = block["block_id"]
            block_count += 1
            nodes = block.get("render_nodes")
            authority_refs = block.get("authority_refs")
            render_digest = block.get("render_digest")
            if not isinstance(nodes, list) or not nodes:
                fail("MATH_BLUEPRINT_RENDER_PAYLOAD_MISSING", block_id)
            for node in nodes:
                _validate_node(node, block_id)
            if not isinstance(authority_refs, list) or not authority_refs or any(not str(x).strip() for x in authority_refs):
                fail("MATH_BLUEPRINT_RENDER_AUTHORITY_MISSING", block_id)
            actual = digest(nodes)
            if render_digest != actual:
                fail("MATH_BLUEPRINT_RENDER_DIGEST_MISMATCH", f"{block_id}:{render_digest}!={actual}")
            if block_id in rendered_ids:
                fail("MATH_BLUEPRINT_RENDER_ID_DUPLICATE", block_id)
            rendered_ids.add(block_id)

        for rep in page.get("representations", []):
            rid = rep["representation_id"]
            if rid in rendered_ids:
                fail("MATH_BLUEPRINT_RENDER_ID_DUPLICATE", rid)
            # Representation semantics are themselves the exact render payload:
            # kind + semantic geometry + must-make-visible + must-not-imply.
            if not rep.get("math_refs") or not rep.get("semantic_geometry_refs"):
                fail("MATH_BLUEPRINT_REPRESENTATION_RENDER_PAYLOAD_INCOMPLETE", rid)
            rendered_ids.add(rid)

        for ttu in page.get("reconstructable_ttus", []):
            tid = ttu["ttu_id"]
            if tid in rendered_ids:
                fail("MATH_BLUEPRINT_RENDER_ID_DUPLICATE", tid)
            # TTU schema already contains prompt, given/missing parts, completion
            # key and verification refs; no renderer-authored completion is legal.
            if not ttu.get("reconstruction_prompt") or not ttu.get("completion_key"):
                fail("MATH_BLUEPRINT_TTU_RENDER_PAYLOAD_INCOMPLETE", tid)
            rendered_ids.add(tid)

        for workspace in page.get("workspace_blocks", []):
            wid = workspace["workspace_id"]
            if wid in rendered_ids:
                fail("MATH_BLUEPRINT_RENDER_ID_DUPLICATE", wid)
            rendered_ids.add(wid)

    if block_count == 0:
        fail("MATH_BLUEPRINT_NO_RENDERABLE_CONTENT")

    return {
        "status": "PASS",
        "blueprint_id": doc["blueprint_id"],
        "page_count": len(doc["pages"]),
        "content_block_count": block_count,
        "render_object_count": len(rendered_ids),
        "render_object_ids": sorted(rendered_ids),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--audit-out")
    args = ap.parse_args()
    doc = load(args.input)
    result = validate_content_complete_blueprint(doc)
    result["blueprint_sha256"] = digest(doc)
    if args.audit_out:
        Path(args.audit_out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
