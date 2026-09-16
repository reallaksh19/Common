#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def norm_tokens(value):
    if value is None:
        return []
    if isinstance(value, (int, float)):
        value = str(value)
    value = str(value).lower().replace("_", " ")
    return re.findall(r"[a-z0-9.+-]+", value)


def jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def five_shingles(text):
    toks = norm_tokens(text)
    if len(toks) < 5:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i:i + 5]) for i in range(len(toks) - 4)}


def lexical_similarity(a, b):
    return jaccard(five_shingles(a), five_shingles(b))


def field_similarity(a, b):
    if isinstance(a, list) or isinstance(b, list):
        aa = a if isinstance(a, list) else [a]
        bb = b if isinstance(b, list) else [b]
        return jaccard([" ".join(norm_tokens(x)) for x in aa], [" ".join(norm_tokens(x)) for x in bb])
    return jaccard(norm_tokens(a), norm_tokens(b))


def structural_similarity(fp_a, fp_b, weights):
    return sum(weight * field_similarity(fp_a.get(field), fp_b.get(field)) for field, weight in weights.items())


def fail(msg):
    raise AssertionError(msg)


def validate(doc):
    schema = load("contracts/content-custody-coverage-unit.schema.json")
    policy = load("policy/content-custody-coverage-unit.v2.json")
    badges = load("policy/question-badge-metadata.v1.json")
    calibration = load("calibration/physics-calibration-state.v1.json")
    jsonschema.validate(doc, schema)

    if calibration["duplication"]["maturity"] == "ENGINEERING":
        if policy["similarity"]["lexical_five_shingle_jaccard"]["engineering_threshold_action"] != "REVIEW_ONLY":
            fail("ENGINEERING lexical threshold may not auto-block")
        if policy["similarity"]["structural_fingerprint"]["engineering_threshold_action"] != "REVIEW_ONLY":
            fail("ENGINEERING structural threshold may not auto-block")

    assets = {a["asset_id"]: a for a in doc["canonical_assets"]}
    if len(assets) != len(doc["canonical_assets"]):
        fail("duplicate canonical asset_id")

    coverage = {}
    for row in doc["coverage_matrix"]:
        key = (row["asset_id"], row["core"])
        if key in coverage:
            fail(f"duplicate coverage row: {key}")
        if row["asset_id"] not in assets:
            fail(f"coverage references unknown asset: {row['asset_id']}")
        coverage[key] = row
        disp = row["disposition"]
        if disp == "REQUIRED" and not row.get("realization_ref"):
            fail(f"REQUIRED asset lacks realization_ref: {key}")
        if disp == "TRANSFORMED" and not (row.get("realization_ref") and row.get("parent_asset_id") and row.get("transformation_ref")):
            fail(f"TRANSFORMED asset lacks lineage: {key}")
        if disp == "HELD" and not row.get("blocking_reason"):
            fail(f"HELD asset lacks blocking_reason: {key}")
        if disp == "PROHIBITED" and row.get("realization_ref"):
            fail(f"PROHIBITED asset has realization_ref: {key}")

    for asset_id, asset in assets.items():
        for core in asset.get("applicable_cores", []):
            if (asset_id, core) not in coverage:
                fail(f"silent asset omission: {asset_id} missing disposition for {core}")

    qmap = {q["question_id"]: q for q in doc["question_records"]}
    if len(qmap) != len(doc["question_records"]):
        fail("duplicate question_id")

    required_badges = set(badges["student_facing_badges"]["required_for_every_released_question"])
    for q in doc["question_records"]:
        status, answer, source, source_class = q["legal_status"], q["answer"], q["source"], q["source_class"]
        if not required_badges.issubset(q["badges"]):
            fail(f"question missing required learner badges: {q['question_id']}")
        if not q.get("display_source_label"):
            fail(f"question missing visible source label: {q['question_id']}")
        if status in {"RELEASED", "DESIGN_PILOT_ONLY"}:
            if answer["status"] != "AVAILABLE" or answer["answer_type"] == "HELD":
                fail(f"learner-facing question lacks canonical resolution: {q['question_id']}")
            if not (answer.get("canonical_answer") or answer.get("solution_ref")):
                fail(f"learner-facing question has no answer content/ref: {q['question_id']}")
        if source_class == "FROZEN_SOURCE":
            original = source.get("source_question_no")
            if original and q["display_number"] != original:
                fail(f"frozen source number changed: {q['question_id']}")
            if status == "RELEASED" and (not source.get("source_digest") or source.get("source_digest") == "HELD"):
                fail(f"released frozen source lacks digest: {q['question_id']}")
        else:
            label = q["display_source_label"].upper()
            if source_class.startswith("AUTHOR_CREATED") and "AUTHOR" not in label:
                fail(f"author-created question source identity hidden: {q['question_id']}")
            if source_class == "GENERATED_LEGAL_SIBLING" and "GENERATED" not in label:
                fail(f"generated question source identity hidden: {q['question_id']}")
            if source_class == "OWNER_SUPPLIED" and "OWNER" not in label:
                fail(f"owner-supplied question source identity hidden: {q['question_id']}")

    sim = policy["similarity"]
    weights = sim["structural_fingerprint"]["weights"]
    structural_high = sim["structural_fingerprint"]["high_review_at_or_above"]
    structural_review = sim["structural_fingerprint"]["review_at_or_above"]
    lexical_high = sim["lexical_five_shingle_jaccard"]["high_review_at_or_above"]
    lexical_review = sim["lexical_five_shingle_jaccard"]["review_at_or_above"]
    lexical_candidate = sim["lexical_five_shingle_jaccard"]["candidate_at_or_above"]
    adjacent = {frozenset(("CORE1A", "CORE1B")), frozenset(("CORE2A", "CORE2B"))}
    results = []
    unresolved_review = False

    for pair in doc["similarity_pairs"]:
        left, right = qmap[pair["left_question_id"]], qmap[pair["right_question_id"]]
        relation = pair["relationship"]
        if relation in sim["release_blocked_classifications"]:
            fail(f"declared pedagogical duplication: {left['question_id']} vs {right['question_id']}")

        lex = lexical_similarity(pair.get("lexical_text_left", ""), pair.get("lexical_text_right", ""))
        fp_l, fp_r = left.get("example_fingerprint"), right.get("example_fingerprint")
        structural = structural_similarity(fp_l, fp_r, weights) if fp_l and fp_r else 0.0
        same_numeric = bool(fp_l and fp_r and fp_l.get("numeric_values") and fp_l.get("numeric_values") == fp_r.get("numeric_values"))
        exact_fp = bool(fp_l and fp_r and fp_l == fp_r)
        is_adjacent = frozenset((left["core"], right["core"])) in adjacent

        # Constitutional deterministic blocks do not depend on calibrated thresholds.
        if is_adjacent and same_numeric and relation != "FADING_ANCHOR":
            fail(f"exact numeric dataset reused across adjacent layers without FADING_ANCHOR: {left['question_id']} vs {right['question_id']}")
        if exact_fp and pair["usage_equivalent"] and relation != "FADING_ANCHOR":
            fail(f"exact fingerprint with equivalent pedagogy: {left['question_id']} vs {right['question_id']}")

        # FADING_ANCHOR is an explicit intentional-reuse lineage, not an unresolved heuristic duplicate.
        heuristic_review = relation != "FADING_ANCHOR" and (
            structural >= structural_review or lex >= lexical_review or relation == "NEAR_DUPLICATE"
        )
        risk = "LOW"
        if heuristic_review and (structural >= structural_high or lex >= lexical_high):
            risk = "HIGH_REVIEW"
        elif heuristic_review:
            risk = "REVIEW"
        elif lex >= lexical_candidate:
            risk = "CANDIDATE"

        disposition = pair.get("review_disposition", "PENDING" if heuristic_review else "NOT_REQUIRED")
        if heuristic_review:
            if disposition == "ADJUDICATED_BLOCK":
                fail(f"similarity review adjudicated block: {left['question_id']} vs {right['question_id']}")
            if disposition == "ADJUDICATED_ALLOW":
                if not pair.get("reviewer_ref") or not pair.get("review_reason"):
                    fail(f"adjudicated similarity allow lacks reviewer provenance: {left['question_id']} vs {right['question_id']}")
            else:
                unresolved_review = True

        results.append({
            "left": left["question_id"],
            "right": right["question_id"],
            "lexical": round(lex, 4),
            "structural": round(structural, 4),
            "risk": risk,
            "review_required": heuristic_review,
            "review_disposition": disposition,
            "relationship": relation
        })

    receipts = doc["receipts"]
    if receipts["coverage_receipt"] != "PASS":
        fail("CCU fixture must close canonical coverage")
    if receipts["question_custody_receipt"] != "PASS":
        fail("CCU fixture must close question custody")
    if receipts["duplication_receipt"] == "BLOCKED":
        fail("CCU duplication receipt is blocked")
    if unresolved_review and receipts["duplication_receipt"] != "REVIEW":
        fail("engineering similarity review unresolved but duplication receipt is not REVIEW")
    if not unresolved_review and receipts["duplication_receipt"] == "REVIEW":
        fail("duplication receipt REVIEW has no unresolved review signal")

    return results


def main():
    rel = sys.argv[1] if len(sys.argv) > 1 else "topics/m2d-sba23-ccu.v1.json"
    doc = load(rel)
    results = validate(doc)
    print(json.dumps({"status": "PASS", "bucket_id": doc["bucket_id"], "similarity": results}, indent=2))


if __name__ == "__main__":
    main()
