#!/usr/bin/env python3
"""Realize the governed C-I source-transfer plan as Core (2A) source practice.

The source lane preserves every C-I question exactly, binds it to the already
closed Core1A bucket/hint evidence, adds learner-facing staged support, gives
an immediate answer check plus full working, and emits sanitized inline
provenance without leaking internal fixture/source identifiers onto learner
surfaces.

Both MCQ and constructed-response source questions are supported. Constructed
responses remain checkable when C-I supplies a canonical response; fake options
must never be invented merely to satisfy the learner-product layer.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(obj, field=None):
    value = copy.deepcopy(obj)
    if field:
        value.pop(field, None)
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def uniq(values):
    out = []
    for value in values:
        if value not in out:
            out.append(value)
    return out


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def safe_http_url(value):
    parsed = urlparse(value or "")
    return value if parsed.scheme in {"http", "https"} and parsed.netloc else None


def learner_question_locator(question_ref):
    """Convert internal source keys into a public locator without losing custody."""
    value = str(question_ref or "").strip()

    match = re.fullmatch(r"^EXT0*(\d+)$", value, flags=re.IGNORECASE)
    if match:
        return f"source item {int(match.group(1))}"

    match = re.fullmatch(r"^U0*(\d+)[-_]?Q0*(\d+)([A-Z])?$", value, flags=re.IGNORECASE)
    if match:
        part = f"({match.group(3).lower()})" if match.group(3) else ""
        return f"unit {int(match.group(1))}, question {int(match.group(2))}{part}"

    match = re.fullmatch(r"^SP0*(\d+)[-_]?Q0*(\d+)([A-Z])?$", value, flags=re.IGNORECASE)
    if match:
        part = f"({match.group(3).lower()})" if match.group(3) else ""
        return f"sample paper {int(match.group(1))}, question {int(match.group(2))}{part}"

    match = re.fullmatch(r"^(?:Q|QUESTION)[-_]?0*(\d+)$", value, flags=re.IGNORECASE)
    if match:
        return f"question {int(match.group(1))}"

    # Unknown machine identifiers stay in internal custody; they are never
    # prettified into learner text because that could silently expose schema ids.
    return "source question"


def response_mode(page):
    explicit = page.get("response_mode")
    if explicit in {"MCQ", "CONSTRUCTED_RESPONSE"}:
        return explicit
    return "MCQ" if page.get("source_options") else "CONSTRUCTED_RESPONSE"


def validate_response_shape(page):
    mode = response_mode(page)
    options = page.get("source_options") or []
    if mode == "MCQ" and len(options) < 2:
        fail("CORE2A_RESPONSE_MODE_INVALID", page["question_ref"] + ": MCQ requires source options")
    if mode == "CONSTRUCTED_RESPONSE" and options:
        fail("CORE2A_RESPONSE_MODE_INVALID", page["question_ref"] + ": constructed response cannot contain invented options")
    solution = page.get("solution_route") or {}
    if mode == "CONSTRUCTED_RESPONSE" and not str(solution.get("chemical_language_response") or "").strip():
        fail("CORE2A_RESPONSE_MODE_INVALID", page["question_ref"] + ": canonical response missing")
    return mode


def family_tables(registry):
    by_id = {row["family_id"]: row for row in registry["families"]}
    aliases = registry.get("question_family_aliases", {})
    return by_id, aliases


def canonical_family(ref, by_id, aliases):
    if ref in by_id:
        return ref
    mapped = aliases.get(ref)
    return mapped if mapped in by_id else None


def bucket_map(bucket_plan):
    question_to_bucket = {}
    for bucket in bucket_plan["buckets"]:
        binding_by_question = {row["question_ref"]: row for row in bucket["core2_hint_bindings"]}
        for question_ref in bucket["core2_primary_question_refs"]:
            if question_ref in question_to_bucket:
                fail("CORE2A_SOURCE_ITEM_DUPLICATED", question_ref + ": multiple Core1A buckets")
            if question_ref not in binding_by_question:
                fail("CORE2A_HINT_ATOM_NOT_PRETAUGHT", question_ref + ": missing Core1A hint binding")
            question_to_bucket[question_ref] = (bucket, binding_by_question[question_ref])
    return question_to_bucket


def validate_upstream(core2, bucket_plan):
    if bucket_plan.get("core2_plan_ref") != core2.get("plan_id"):
        fail("CORE2A_CORE1A_BUCKET_BINDING_MISSING", "Core2 plan ref")
    if bucket_plan.get("core2_plan_digest") != core2.get("plan_digest"):
        fail("CORE2A_CORE1A_BUCKET_BINDING_MISSING", "Core2 plan digest")
    required = [page["question_ref"] for page in core2["pages"]]
    mapped = [q for bucket in bucket_plan["buckets"] for q in bucket["core2_primary_question_refs"]]
    if Counter(required) != Counter(mapped):
        fail("CORE2A_CORE1A_BUCKET_BINDING_MISSING", "question denominator")


def family_watch_text(page, family_registry, policy):
    by_id, aliases = family_tables(family_registry)
    ref = canonical_family(page["problem_family_ref"], by_id, aliases)
    if not ref:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": problem family")
    family = by_id[ref]
    wrong = family.get("common_wrong_models", [])
    symbolic = family.get("common_symbolic_errors", [])
    source = wrong[0] if wrong else symbolic[0] if symbolic else None
    if not source:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": no misconception authority")
    return policy["watch_for_this"]["prefix"] + source, ref


def translated_verification(page, policy):
    table = policy["verification_language"]
    out = []
    for code in page["verification_route"]:
        if code not in table:
            fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": verification code " + code)
        out.append(table[code])
    return uniq(out)


def build_provenance(page, source_policy):
    badges = page["source_badges"]
    safe_url = safe_http_url(page["source_link"])
    label = str(badges.get("source") or "Chemistry source").replace("_", " ").strip().title()
    locator = str(page.get("source_locator") or "").strip()
    if not locator:
        parts = [str(badges.get(k) or "").strip() for k in ("year", "session")]
        shift = str(badges.get("shift") or "").strip()
        if shift:
            parts.append("shift " + shift)
        parts.append(learner_question_locator(page["question_ref"]))
        locator = " · ".join(x for x in parts if x)
    relation = page.get("source_text_relation") or "EXACT_SOURCE"
    official_ref = page.get("verified_official_source_ref")
    official_claim = bool(official_ref) or source_policy["provenance"]["official_past_question_claim_default"]
    return {
        "question_origin": "SOURCE_CORE2",
        "display_inline": True,
        "learner_label": "WHERE THIS QUESTION CAME FROM",
        "citations": [
            {
                "citation_kind": "CORE2_SOURCE",
                "label": label,
                "locator": locator,
                "url": safe_url,
                "use": "SOURCE_TEXT",
                "text_relation": relation,
            }
        ],
        "official_past_question_claim": official_claim,
        "verified_official_source_ref": official_ref,
    }


def build_answer_path(page, source_policy):
    mode = validate_response_shape(page)
    solution = page["solution_route"]
    translated = translated_verification(page, source_policy)
    condition_check = str(solution.get("condition_exception_check") or "").strip()
    verification_parts = translated + ([condition_check] if condition_check else [])
    if mode == "MCQ":
        answer_summary = str(solution["final_answer"]) + " — " + str(solution["chemical_language_response"])
        marking_points = []
    else:
        answer_summary = str(solution["chemical_language_response"]).strip()
        marking_points = list(page.get("quick_check_marking_points") or [])
        if not marking_points:
            marking_points = [answer_summary]
    return {
        "question_ref": page["question_ref"],
        "answer_path_kind": "OBJECTIVE_CHECKABLE",
        "learner_question_present": True,
        "answer_path_complete": True,
        "quick_check": {
            "learner_label": "QUICK CHECK",
            "answer_summary": answer_summary,
            "unit": None,
            "marking_points": marking_points,
        },
        "full_working": {
            "learner_label": "FULL WORKING",
            "steps": list(solution["reasoning_steps"]) + ["Final answer: " + answer_summary],
            "verification": " ".join(verification_parts),
        },
        "expected_response_rubric": None,
    }


def build_learner_support(page, bucket, hint_binding, family_registry, source_policy, language_policy):
    labels = language_policy["labels"]
    write_prefix = source_policy["write_this_first"]["prefix"]
    fields = page["workspace_spec"]["fields"]
    if not fields:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": empty working frame")
    watch, family_ref = family_watch_text(page, family_registry, source_policy)
    if family_ref != bucket["primary_problem_family_ref"] and family_ref not in {p["problem_family_ref"] for p in bucket["problem_families"]}:
        fail("CORE2A_CORE1A_BUCKET_BINDING_MISSING", page["question_ref"] + ": family not taught in bucket")
    source_visual_refs = [v["visual_id"] for v in page["visual_specs"]]
    if not source_visual_refs:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": no C-I visual")
    h2_refs = list(hint_binding["h2_evidence_refs"])
    bucket_rep_refs = {r["representation_ref"] for r in bucket["representation_obligations"]}
    if any(ref not in bucket_rep_refs for ref in h2_refs):
        fail("CORE2A_HINT_ATOM_NOT_PRETAUGHT", page["question_ref"] + ": H2")
    support = {
        "support_initially_hidden": True,
        "try_it_first": page["hint_ladder"]["h0_attempt_first"],
        "see_the_idea": {
            "learner_label": labels["REPRESENTATION"],
            "source_visual_refs": source_visual_refs,
            "pre_taught_representation_refs": h2_refs,
        },
        "write_this_first": write_prefix + fields[0],
        "small_clue": page["hint_ladder"]["h1_notice"],
        "bigger_clue": page["hint_ladder"]["h2_rule_model_representation"],
        "how_do_i_start": page["hint_ladder"]["h3_start"],
        "watch_for_this": watch,
        "think_it_through": [source_policy["think_it_through"]["opening"]] + [f"{i}. {field}" for i, field in enumerate(fields, 1)],
        "check_your_chemistry": translated_verification(page, source_policy),
    }
    forbidden = [term.lower() for term in language_policy["forbidden_learner_terms"]]
    learner_text = canonical(support).lower()
    leaked = [term for term in forbidden if term in learner_text]
    if leaked:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": learner jargon leak " + leaked[0])
    return support


def source_snapshot(page):
    return {
        "source_ref": page["source_ref"],
        "source_qc_status": page["source_qc_status"],
        "stem": page["source_stem"],
        "options": copy.deepcopy(page["source_options"]),
        "subparts": copy.deepcopy(page["source_subparts"]),
        "response_mode": response_mode(page),
        "source_locator": str(page.get("source_locator") or learner_question_locator(page["question_ref"])),
        "source_text_relation": page.get("source_text_relation") or "EXACT_SOURCE",
        "figure_required": page["source_figure_required"],
        "figure_semantic": copy.deepcopy(page["source_figure_semantic"]),
        "condition_text": page["source_condition_text"],
        "states": copy.deepcopy(page["source_states"]),
        "units": copy.deepcopy(page["source_units"]),
        "source_badges": copy.deepcopy(page["source_badges"]),
        "source_fidelity": copy.deepcopy(page["source_fidelity"]),
    }


def build_item(page, bucket, hint_binding, family_registry, source_policy, language_policy):
    validate_response_shape(page)
    atom_refs = {a["atom_id"] for a in bucket["learning_atoms"]}
    rep_refs = {r["representation_ref"] for r in bucket["representation_obligations"]}
    for key in ("h1_evidence_refs", "h2_evidence_refs", "h3_evidence_refs"):
        if not hint_binding[key] or any(ref not in atom_refs | rep_refs for ref in hint_binding[key]):
            fail("CORE2A_HINT_ATOM_NOT_PRETAUGHT", page["question_ref"] + ": " + key)
    item = {
        "item_id": "CHEM-C2A-SRC-" + page["question_ref"],
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "lane": "SOURCE_CORE2",
        "question_ref": page["question_ref"],
        "source_snapshot": source_snapshot(page),
        "core1a_binding": {
            "bucket_id": bucket["bucket_id"],
            "primary_problem_family_ref": page["problem_family_ref"],
            "primary_capability_ref": page["primary_capability_ref"],
            "supporting_capability_refs": copy.deepcopy(page["supporting_capability_refs"]),
            "h1_evidence_refs": copy.deepcopy(hint_binding["h1_evidence_refs"]),
            "h2_evidence_refs": copy.deepcopy(hint_binding["h2_evidence_refs"]),
            "h3_evidence_refs": copy.deepcopy(hint_binding["h3_evidence_refs"]),
        },
        "learner_support": build_learner_support(page, bucket, hint_binding, family_registry, source_policy, language_policy),
        "answer_path": build_answer_path(page, source_policy),
        "provenance": build_provenance(page, source_policy),
        "internal_source_custody": {
            "source_link_internal": page["source_link"],
            "display_url_allowed": safe_http_url(page["source_link"]) is not None,
            "core2_page_digest": page["page_digest"],
        },
        "item_digest": "",
    }
    item["item_digest"] = digest(item, "item_digest")
    return item


def validate_item(item, page, bucket, hint_binding, family_registry, source_policy, language_policy):
    validate_response_shape(page)
    if item["item_digest"] != digest(item, "item_digest"):
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", item["question_ref"] + ": item digest")
    if item["lane"] != "SOURCE_CORE2" or item["question_ref"] != page["question_ref"]:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": identity")
    if item["source_snapshot"] != source_snapshot(page):
        fail("CORE2A_SOURCE_INTEGRITY_DRIFT", page["question_ref"])
    if item["source_snapshot"]["source_qc_status"] != page["source_qc_status"]:
        fail("CORE2A_SOURCE_INTEGRITY_DRIFT", page["question_ref"] + ": QC")
    expected_support = build_learner_support(page, bucket, hint_binding, family_registry, source_policy, language_policy)
    if item["learner_support"] != expected_support:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": support drift")
    if item["answer_path"] != build_answer_path(page, source_policy):
        fail("CORE2A_ANSWER_PATH_MISSING", page["question_ref"])
    if item["provenance"] != build_provenance(page, source_policy):
        fail("CORE2A_QUESTION_CITATION_MISSING", page["question_ref"])
    raw = page["source_link"]
    if not safe_http_url(raw) and raw in canonical(item["provenance"]):
        fail("CORE2A_RAW_INTERNAL_SOURCE_LINK_LEAK", page["question_ref"])
    if item["internal_source_custody"]["source_link_internal"] != raw or item["internal_source_custody"]["core2_page_digest"] != page["page_digest"]:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", page["question_ref"] + ": custody")
    if item["core1a_binding"]["bucket_id"] != bucket["bucket_id"]:
        fail("CORE2A_CORE1A_BUCKET_BINDING_MISSING", page["question_ref"])
    for key in ("h1_evidence_refs", "h2_evidence_refs", "h3_evidence_refs"):
        if item["core1a_binding"][key] != hint_binding[key]:
            fail("CORE2A_HINT_ATOM_NOT_PRETAUGHT", page["question_ref"] + ": " + key)
    return True


def build_source_plan(core2, bucket_plan, family_registry, execution_policy, source_policy, language_policy, citation_policy, answer_policy, plan_id="CHEM-C2A-SOURCE-PLAN-PILOT-v1"):
    validate_upstream(core2, bucket_plan)
    expected_ids = {
        "execution": "CHEM-CORE2A-EXECUTION-v1",
        "source": "CHEM-CORE2A-SOURCE-REALIZATION-v1",
        "language": "CHEM-LEARNER-LANGUAGE-v1",
        "citation": "CHEM-QUESTION-CITATION-v1",
        "answer": "CHEM-ANSWER-PATH-v1",
    }
    actual_ids = {
        "execution": execution_policy.get("policy_id"),
        "source": source_policy.get("policy_id"),
        "language": language_policy.get("policy_id"),
        "citation": citation_policy.get("policy_id"),
        "answer": answer_policy.get("policy_id"),
    }
    if actual_ids != expected_ids:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", "policy binding")
    if not execution_policy["source_lane"]["preserve_all_core2_questions"] or not citation_policy["inline_provenance_required"]:
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", "source/citation policy")

    qmap = bucket_map(bucket_plan)
    items = []
    for page in core2["pages"]:
        if page["question_ref"] not in qmap:
            fail("CORE2A_SOURCE_ITEM_MISSING", page["question_ref"])
        bucket, hint_binding = qmap[page["question_ref"]]
        items.append(build_item(page, bucket, hint_binding, family_registry, source_policy, language_policy))

    required = [page["question_ref"] for page in core2["pages"]]
    realized = [item["question_ref"] for item in items]
    missing = [ref for ref in required if ref not in Counter(realized)]
    duplicates = sorted([ref for ref, count in Counter(realized).items() if count > 1])
    if missing:
        fail("CORE2A_SOURCE_ITEM_MISSING", str(missing))
    if duplicates:
        fail("CORE2A_SOURCE_ITEM_DUPLICATED", str(duplicates))
    count = len(required)
    out = {
        "plan_id": plan_id,
        "schema_version": "1.0.0",
        "subject": "CHEMISTRY",
        "lane": "SOURCE_CORE2",
        "core2_plan_ref": core2["plan_id"],
        "core2_plan_digest": core2["plan_digest"],
        "core1a_bucket_plan_ref": bucket_plan["plan_id"],
        "core1a_bucket_plan_digest": bucket_plan["plan_digest"],
        "execution_policy_ref": execution_policy["policy_id"],
        "source_realization_policy_ref": source_policy["policy_id"],
        "learner_language_policy_ref": language_policy["policy_id"],
        "citation_policy_ref": citation_policy["policy_id"],
        "answer_path_policy_ref": answer_policy["policy_id"],
        "items": items,
        "summary": {
            "source_questions_required": count,
            "source_questions_realized": len(items),
            "missing_source_question_refs": [],
            "duplicate_source_question_refs": [],
            "quick_checks_required": count,
            "quick_checks_realized": sum(item["answer_path"].get("quick_check") is not None for item in items),
            "full_workings_required": count,
            "full_workings_realized": sum(item["answer_path"].get("full_working") is not None for item in items),
            "hint_reveals_required": 3 * count,
            "hint_reveals_bound": 3 * len(items),
            "raw_internal_source_links_rendered": 0,
            "status": "PASS",
        },
        "plan_digest": "",
    }
    out["plan_digest"] = digest(out, "plan_digest")
    validate_source_plan(out, core2, bucket_plan, family_registry, execution_policy, source_policy, language_policy, citation_policy, answer_policy)
    return out


def validate_source_plan(plan, core2, bucket_plan, family_registry, execution_policy, source_policy, language_policy, citation_policy, answer_policy):
    validate_upstream(core2, bucket_plan)
    if plan["plan_digest"] != digest(plan, "plan_digest"):
        fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", "plan digest")
    expected = {
        "core2_plan_ref": core2["plan_id"],
        "core2_plan_digest": core2["plan_digest"],
        "core1a_bucket_plan_ref": bucket_plan["plan_id"],
        "core1a_bucket_plan_digest": bucket_plan["plan_digest"],
        "execution_policy_ref": execution_policy["policy_id"],
        "source_realization_policy_ref": source_policy["policy_id"],
        "learner_language_policy_ref": language_policy["policy_id"],
        "citation_policy_ref": citation_policy["policy_id"],
        "answer_path_policy_ref": answer_policy["policy_id"],
    }
    for key, value in expected.items():
        if plan.get(key) != value:
            fail("CORE2A_SOURCE_TEXT_UNTRACEABLE", key)
    pages = core2["pages"]
    if [item["question_ref"] for item in plan["items"]] != [page["question_ref"] for page in pages]:
        fail("CORE2A_SOURCE_ITEM_MISSING", "source order/denominator drift")
    qmap = bucket_map(bucket_plan)
    for item, page in zip(plan["items"], pages):
        bucket, hint_binding = qmap[page["question_ref"]]
        validate_item(item, page, bucket, hint_binding, family_registry, source_policy, language_policy)
    count = len(pages)
    summary = plan["summary"]
    expected_counts = {
        "source_questions_required": count,
        "source_questions_realized": count,
        "quick_checks_required": count,
        "quick_checks_realized": count,
        "full_workings_required": count,
        "full_workings_realized": count,
        "hint_reveals_required": 3 * count,
        "hint_reveals_bound": 3 * count,
        "raw_internal_source_links_rendered": 0,
        "status": "PASS",
    }
    for key, value in expected_counts.items():
        if summary.get(key) != value:
            fail("CORE2A_ANSWER_PATH_MISSING" if "check" in key or "working" in key else "CORE2A_SOURCE_ITEM_MISSING", key)
    if summary["missing_source_question_refs"] or summary["duplicate_source_question_refs"]:
        fail("CORE2A_SOURCE_ITEM_MISSING", "closure lists")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core2-plan", required=True)
    parser.add_argument("--core1a-bucket-plan", required=True)
    parser.add_argument("--problem-family-registry", required=True)
    parser.add_argument("--execution-policy", required=True)
    parser.add_argument("--source-realization-policy", required=True)
    parser.add_argument("--learner-language-policy", required=True)
    parser.add_argument("--citation-policy", required=True)
    parser.add_argument("--answer-path-policy", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--plan-id", default="CHEM-C2A-SOURCE-PLAN-PILOT-v1")
    args = parser.parse_args()
    plan = build_source_plan(
        load(args.core2_plan),
        load(args.core1a_bucket_plan),
        load(args.problem_family_registry),
        load(args.execution_policy),
        load(args.source_realization_policy),
        load(args.learner_language_policy),
        load(args.citation_policy),
        load(args.answer_path_policy),
        args.plan_id,
    )
    Path(args.out).write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
