#!/usr/bin/env python3
"""Compile a content-complete Blueprint from governed producer outputs.

Unlike the first EASY-only publication slice, this compiler supports a uniform
EASY, MEDIUM or HARD run. It never authors new mathematical content: additional
depth objects are materialized only from already-governed producer content.
Core1A worked examples must bind to the governed-example admission catalog.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import compile_bound_product_page_blueprint as legacy
from blueprint_common import fail, load
from materialize_intrinsic_depth import materialize_uniform_depth, depth_obligations
from validate_content_complete_page_blueprint import validate_content_complete_blueprint
from validate_self_teaching_generation_spec import validate_generation_spec


def _governed_example_index(catalog: dict) -> dict[str, list[dict]]:
    if catalog.get("subject") != "MATHEMATICS" or catalog.get("catalog_role") != "GOVERNED_CORE1A_EXAMPLE_ADMISSION":
        fail("MATH_BLUEPRINT_GOVERNED_EXAMPLE_CATALOG_INVALID")
    expected = catalog.get("catalog_digest")
    material = copy.deepcopy(catalog)
    material.pop("catalog_digest", None)
    if not expected or legacy.digest(material) != expected:
        fail("MATH_BLUEPRINT_GOVERNED_EXAMPLE_CATALOG_DIGEST_INVALID")
    out: dict[str, list[dict]] = {}
    for row in catalog.get("examples", []):
        if row.get("admission_status") != "ADMITTED" or not row.get("example_asset_id", "").startswith("GEX-MATH-"):
            fail("MATH_BLUEPRINT_UNADMITTED_EXAMPLE", str(row.get("example_asset_id")))
        out.setdefault(row["prompt"], []).append(row)
    if not out:
        fail("MATH_BLUEPRINT_GOVERNED_EXAMPLE_CATALOG_EMPTY")
    return out


def bind_governed_example_authority(pages: list[dict], book: dict, catalog: dict) -> None:
    index = _governed_example_index(catalog)
    known = {row["example_asset_id"]: row for rows in index.values() for row in rows}

    for bucket in book.get("buckets", []):
        for unit in bucket.get("capability_units", []):
            cap = unit["capability_ref"]
            for ex in unit.get("worked_examples", []):
                ref = ex.get("governed_example_asset_ref")
                if not ref or ref not in known:
                    fail("MATH_BLUEPRINT_WORKED_EXAMPLE_NOT_GOVERNED", f"{cap}:{ref}")
                if known[ref]["content_digest"] != ex.get("content_digest"):
                    fail("MATH_BLUEPRINT_WORKED_EXAMPLE_DIGEST_DRIFT", ref)
            for role, item in (unit.get("practice") or {}).items():
                ref = item.get("governed_example_asset_ref")
                if not ref or ref not in known:
                    fail("MATH_BLUEPRINT_PRACTICE_EXAMPLE_NOT_GOVERNED", f"{cap}:{role}:{ref}")
                if known[ref]["content_digest"] != item.get("content_digest"):
                    fail("MATH_BLUEPRINT_PRACTICE_EXAMPLE_DIGEST_DRIFT", ref)

    for page in pages:
        if page["stage"] != "CORE1A":
            continue
        for block in page.get("technical_blocks", []):
            if block.get("kind") != "WORKED_EXAMPLE":
                continue
            prompt = next((x["text"] for x in block.get("render_nodes", []) if x.get("type") == "QUESTION"), None)
            if not prompt:
                fail("MATH_BLUEPRINT_WORKED_EXAMPLE_PROMPT_MISSING", block["block_id"])
            candidates = [x for x in index.get(prompt, []) if x["capability_ref"] in block.get("math_refs", [])]
            if len(candidates) != 1:
                fail("MATH_BLUEPRINT_WORKED_EXAMPLE_AUTHORITY_AMBIGUOUS", block["block_id"])
            gex = candidates[0]
            block["authority_refs"] = [x for x in block.get("authority_refs", []) if not str(x).startswith("CORE1A_AUTHORED_INSTANCE:")]
            block["authority_refs"] = list(dict.fromkeys([*block["authority_refs"], gex["example_asset_id"], *gex.get("capability_registry_refs", [])]))
            if any(str(x).startswith("CORE1A_AUTHORED_INSTANCE:") for x in block["authority_refs"]):
                fail("MATH_BLUEPRINT_RAW_AUTHORED_INSTANCE_AUTHORITY_FORBIDDEN", block["block_id"])


def compile_document(bucket_plan: dict, book: dict, core1b_dir: Path, c2a: dict, c2b: dict, gen: dict, catalog: dict) -> dict:
    validate_generation_spec(gen)
    badges = {row["difficulty_badge"] for row in gen["core1_buckets"]}
    if len(badges) != 1:
        fail("MATH_BLUEPRINT_MIXED_DIFFICULTY_PUBLICATION_REQUIRES_BUNDLE", ",".join(sorted(badges)))
    badge = next(iter(badges))

    c1a_pages, c1a_ttu, unit_by_cap = legacy.compile_core1a_pages(book)
    plans = legacy.load_core1b_plans(core1b_dir, [b["title"] for b in bucket_plan["buckets"]])
    c1b_pages, _ = legacy.compile_core1b_pages(bucket_plan, plans, c1a_ttu)
    c2a_pages, c2a_ttu, _ = legacy.compile_core2a_pages(c2a, unit_by_cap)
    c2b_pages = legacy.compile_core2b_pages(c2b, c2a_ttu)
    pages = [*c1a_pages, *c1b_pages, *c2a_pages, *c2b_pages]

    bind_governed_example_authority(pages, book, catalog)
    pages = materialize_uniform_depth(pages, badge, book)

    raw = json.dumps(pages, ensure_ascii=False)
    if "CORE1A_AUTHORED_INSTANCE:" in raw:
        fail("MATH_BLUEPRINT_RAW_AUTHORED_INSTANCE_AUTHORITY_FORBIDDEN")

    doc = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "blueprint_id": "",
        "difficulty_badge": badge,
        "pages": pages,
        "depth_obligations": depth_obligations(badge, pages),
    }
    doc["blueprint_id"] = "MATH-PAGE-BP-GOV-" + legacy.digest(doc)[:16]
    validate_content_complete_blueprint(doc)
    return doc


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket-plan", required=True)
    ap.add_argument("--core1a-manuscript", required=True)
    ap.add_argument("--core1a-example-catalog", required=True)
    ap.add_argument("--core1b-dir", required=True)
    ap.add_argument("--core2a-blueprint", required=True)
    ap.add_argument("--core2b-plan", required=True)
    ap.add_argument("--generation-spec", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    doc = compile_document(
        load(args.bucket_plan), load(args.core1a_manuscript), Path(args.core1b_dir),
        load(args.core2a_blueprint), load(args.core2b_plan), load(args.generation_spec),
        load(args.core1a_example_catalog),
    )
    Path(args.out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    audit = validate_content_complete_blueprint(doc)
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
