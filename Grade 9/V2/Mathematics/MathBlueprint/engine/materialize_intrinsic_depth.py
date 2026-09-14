#!/usr/bin/env python3
"""Materialize Core1A/Core1B intrinsic-depth obligations without inventing math.

The input pages are already compiled from governed producer outputs. This module
may only re-express existing render nodes, representations, worked examples,
misconception contrasts, transfer practice and verification as additional
technical objects required by MEDIUM/HARD composition policy.
"""
from __future__ import annotations

import copy

import compile_bound_product_page_blueprint as bp
from blueprint_common import fail, load

POLICY_PATH = bp.POLICY_PATH


def _blocks(page: dict, kind: str) -> list[dict]:
    return [x for x in page.get("technical_blocks", []) if x.get("kind") == kind]


def _first(page: dict, kind: str) -> dict | None:
    rows = _blocks(page, kind)
    return rows[0] if rows else None


def _node_texts(block: dict, allowed: set[str] | None = None) -> list[dict]:
    nodes = copy.deepcopy(block.get("render_nodes") or [])
    if allowed is not None:
        nodes = [x for x in nodes if x.get("type") in allowed]
    return nodes


def _add_derivation(page: dict) -> str:
    existing = _first(page, "DERIVATION")
    if existing:
        return existing["block_id"]
    anchor = _first(page, "WORKED_EXAMPLE") or _first(page, "CASE_ANALYSIS")
    if not anchor:
        fail("MATH_DEPTH_DERIVATION_SOURCE_MISSING", page["page_id"])
    nodes = _node_texts(anchor, {"STEP", "MATH", "ANSWER"})
    if not nodes:
        nodes = _node_texts(anchor)
    bid = page["page_id"] + "-DERIVATION"
    page["technical_blocks"].append(bp.block(
        bid, "DERIVATION", "DERIVED_MATHEMATICS", list(anchor["math_refs"]), nodes,
        upstream=anchor["block_id"], transform="BUILD",
        authority_refs=list(anchor.get("authority_refs") or anchor["math_refs"]),
    ))
    return bid


def _add_representation(page: dict, suffix: str, kind: str, visible: list[str]) -> str:
    rid = page["page_id"] + "-REP-" + suffix
    if any(x["representation_id"] == rid for x in page.get("representations", [])):
        return rid
    refs = sorted({r for b in page.get("technical_blocks", []) for r in b.get("math_refs", [])})
    page["representations"].append(bp.representation(
        rid, refs, visible,
        ["The alternate representation must preserve the same governed mathematical conditions."],
        kind=kind,
    ))
    return rid


def _second_ttu(c1a_page: dict, c1b_page: dict | None = None) -> tuple[str, str | None]:
    worked = _blocks(c1a_page, "WORKED_EXAMPLE")
    if len(worked) < 2:
        fail("MATH_HARD_SECOND_RECONSTRUCTION_SOURCE_MISSING", c1a_page["page_id"])
    verify = _first(c1a_page, "VERIFICATION") or worked[-1]
    caps = list(worked[1]["math_refs"])
    c1a_tid = c1a_page["page_id"] + "-TTU-2"
    if not any(x["ttu_id"] == c1a_tid for x in c1a_page["reconstructable_ttus"]):
        prompt = next((x["text"] for x in worked[1]["render_nodes"] if x.get("type") == "QUESTION"), "Reconstruct the second governed route.")
        c1a_page["reconstructable_ttus"].append(bp.ttu(
            c1a_tid, caps, prompt, worked[1]["block_id"], verify["block_id"],
            source=None, transform="BUILD", fading="GUIDED",
        ))
    if c1b_page is None:
        return c1a_tid, None
    answer = _first(c1b_page, "ANSWER_DERIVATION")
    verify_b = _first(c1b_page, "VERIFICATION")
    if not answer or not verify_b:
        fail("MATH_HARD_CORE1B_SECOND_TTU_SOURCE_MISSING", c1b_page["page_id"])
    c1b_tid = c1b_page["page_id"] + "-TTU-2"
    if not any(x["ttu_id"] == c1b_tid for x in c1b_page["reconstructable_ttus"]):
        c1b_page["reconstructable_ttus"].append(bp.ttu(
            c1b_tid, caps, "Reconstruct the alternate governed route before checking the completion.",
            answer["block_id"], verify_b["block_id"], source=c1a_tid,
            transform="RECONSTRUCT", fading="FADED",
        ))
    return c1a_tid, c1b_tid


def _add_transfer_bridge(page: dict, bucket: dict) -> str:
    existing = [x for x in page["technical_blocks"] if x["block_id"].endswith("-TRANSFER-BRIDGE")]
    if existing:
        return existing[0]["block_id"]
    candidate = None
    authority = []
    refs = []
    for unit in bucket.get("capability_units", []):
        item = (unit.get("practice") or {}).get("TRANSFER")
        if item:
            candidate = item
            refs = [unit["capability_ref"]]
            authority = [item.get("governed_example_asset_ref") or unit["lesson_id"], unit["capability_ref"]]
            break
    if not candidate:
        fail("MATH_HARD_TRANSFER_BRIDGE_SOURCE_MISSING", page["page_id"])
    nodes = [bp.node("QUESTION", candidate["prompt"])]
    nodes.extend(bp.node("HINT", x) for x in candidate.get("hints", []))
    nodes.append(bp.node("ANSWER", candidate["answer"]))
    bid = page["page_id"] + "-TRANSFER-BRIDGE"
    page["technical_blocks"].append(bp.block(
        bid, "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", refs, nodes,
        upstream=None, transform="TRANSFER", authority_refs=[x for x in authority if x],
    ))
    return bid


def materialize_uniform_depth(pages: list[dict], badge: str, book: dict) -> list[dict]:
    if badge not in {"EASY", "MEDIUM", "HARD"}:
        fail("MATH_INTRINSIC_DEPTH_BADGE_INVALID", badge)
    out = copy.deepcopy(pages)
    if badge == "EASY":
        return out

    c1a = [x for x in out if x["stage"] == "CORE1A"]
    c1b = [x for x in out if x["stage"] == "CORE1B"]
    if len(c1a) != len(book.get("buckets", [])) or len(c1a) != len(c1b):
        fail("MATH_INTRINSIC_DEPTH_BUCKET_PAGE_ALIGNMENT_DRIFT")

    for a, b, bucket in zip(c1a, c1b, book["buckets"]):
        _add_derivation(a)
        model = _first(a, "CASE_ANALYSIS") or a["technical_blocks"][0]
        counter = _first(a, "COUNTEREXAMPLE")
        verify = _first(a, "VERIFICATION")
        if counter is None or verify is None:
            fail("MATH_INTRINSIC_DEPTH_MISCONCEPTION_OR_VERIFY_MISSING", a["page_id"])
        visible = [x["text"] for x in model.get("render_nodes", []) if x.get("type") in {"PARAGRAPH", "STEP", "MATH"}]
        _add_representation(a, "SYMBOL-BRIDGE", "SYMBOL_MAP", visible[:4] or [a["page_purpose"]])

        if not _first(b, "COUNTEREXAMPLE"):
            fail("MATH_INTRINSIC_DEPTH_CORE1B_CONTRAST_MISSING", b["page_id"])

        if badge == "HARD":
            _add_representation(a, "FLOW", "FLOW", visible[:5] or [a["page_purpose"]])
            _add_representation(b, "FLOW", "FLOW", [b["page_purpose"]])
            _second_ttu(a, b)
            _add_transfer_bridge(a, bucket)

    return out


def depth_obligations(badge: str, pages: list[dict]) -> list[dict]:
    policy = load(POLICY_PATH)
    by_stage = {s: [p for p in pages if p["stage"] == s] for s in ("CORE1A", "CORE1B")}
    if not by_stage["CORE1A"] or not by_stage["CORE1B"]:
        fail("MATH_DEPTH_STAGE_PAGES_MISSING")

    def first_id(stage: str, kind: str) -> str | None:
        for p in by_stage[stage]:
            for b in p.get("technical_blocks", []):
                if b.get("kind") == kind:
                    return b["block_id"]
        return None

    def rep(stage: str, contains: str | None = None, index: int = 0) -> str | None:
        rows = [r for p in by_stage[stage] for r in p.get("representations", []) if contains is None or contains in r["representation_id"]]
        return rows[index]["representation_id"] if len(rows) > index else None

    def ttu_ids(stage: str) -> list[str]:
        return [t["ttu_id"] for p in by_stage[stage] for t in p.get("reconstructable_ttus", [])]

    evidence: dict[str, dict[str, list[str]]] = {"CORE1A": {}, "CORE1B": {}}
    a_ttu = ttu_ids("CORE1A"); b_ttu = ttu_ids("CORE1B")
    evidence["CORE1A"].update({
        "OBJECT_MODEL": [first_id("CORE1A", "CASE_ANALYSIS")],
        "PRIMARY_RELATION": [first_id("CORE1A", "CASE_ANALYSIS")],
        "RELATION_DERIVATION": [first_id("CORE1A", "DERIVATION")],
        "PRIMARY_REPRESENTATION": [rep("CORE1A")],
        "REPRESENTATION_SYMBOL_BRIDGE": [rep("CORE1A", "SYMBOL-BRIDGE")],
        "MULTI_REPRESENTATION_TRANSLATION": [x for x in [rep("CORE1A"), rep("CORE1A", "FLOW")] if x],
        "WORKED_ANCHOR": [first_id("CORE1A", "WORKED_EXAMPLE")],
        "RECONSTRUCTABLE_TTU": a_ttu[:1],
        "MULTIPLE_RECONSTRUCTABLE_TTUS": a_ttu[:2],
        "CASE_ANALYSIS": [first_id("CORE1A", "CASE_ANALYSIS")],
        "VALIDITY_OR_SPECIAL_CASE": [first_id("CORE1A", "COUNTEREXAMPLE")],
        "MISCONCEPTION_COUNTEREXAMPLE": [first_id("CORE1A", "COUNTEREXAMPLE")],
        "FAILURE_MODE": [first_id("CORE1A", "COUNTEREXAMPLE")],
        "TRANSFER_BRIDGE": [next((b["block_id"] for p in by_stage["CORE1A"] for b in p["technical_blocks"] if b["block_id"].endswith("-TRANSFER-BRIDGE")), None)],
        "VERIFICATION": [first_id("CORE1A", "VERIFICATION")],
        "INDEPENDENT_CHECK": [first_id("CORE1A", "VERIFICATION")],
    })
    evidence["CORE1B"].update({
        "OPEN_RECONSTRUCTION": [first_id("CORE1B", "OPEN_TASK")],
        "REPRESENTATION_REBUILD": [rep("CORE1B")],
        "MULTI_REPRESENTATION_REBUILD": [x for x in [rep("CORE1B"), rep("CORE1B", "FLOW")] if x],
        "RECONSTRUCTABLE_TTU": b_ttu[:1],
        "MULTIPLE_RECONSTRUCTABLE_TTUS": b_ttu[:2],
        "METHOD_OR_ERROR_CONTRAST": [first_id("CORE1B", "COUNTEREXAMPLE")],
        "CASE_DISCRIMINATION": [first_id("CORE1B", "COUNTEREXAMPLE")],
        "FADED_RECONSTRUCTION": b_ttu[:1],
        "FAILURE_DIAGNOSIS": [first_id("CORE1B", "COUNTEREXAMPLE")],
        "INDEPENDENT_USE": [first_id("CORE1B", "OPEN_TASK")],
        "TRANSFER_RECONSTRUCTION": b_ttu[1:2] or b_ttu[:1],
        "ANSWER_VERIFICATION": [first_id("CORE1B", "VERIFICATION")],
    })

    rows = []
    for stage in ("CORE1A", "CORE1B"):
        for obligation in policy["depth_obligations"][stage][badge]:
            oid = obligation["id"]
            refs = [x for x in evidence[stage].get(oid, []) if x]
            if obligation["required"] and not refs:
                fail("MATH_BLUEPRINT_REQUIRED_DEPTH_EVIDENCE_UNAVAILABLE", f"{stage}:{badge}:{oid}")
            rows.append({
                "stage": stage,
                "badge": badge,
                "obligation_id": oid,
                "disposition": "SATISFIED" if refs else "NOT_APPLICABLE",
                "evidence_refs": refs,
                "not_applicable_reason": None if refs else "Optional obligation has no governed source in this product.",
            })
    return rows
