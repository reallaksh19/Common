#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from core2a_common import (
    PURPOSES,
    canonical,
    check_purpose_coverage,
    choose_source_items,
    digest,
    ensure_no_hint_leak,
    near_copy_report,
    release_evidence,
    teaching_index,
    validate_physics_case,
    bind_answer_equivalence,
)


def realize_source(row, purpose):
    rep = row["core2_representation"]
    hints = {h["level"]: h["text"] for h in rep["hints"]}
    required = {"H1_NOTICE", "H2_MODEL", "H3_START"}
    if set(hints) != required:
        raise ValueError("CORE2A_SOURCE_BINDING_INVALID:HINT_LADDER:" + row["question_ref"])
    return {
        "item_id": "PHY-C2A-SRC-" + digest({"q": row["question_ref"], "purpose": purpose}),
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "lane": "SOURCE_CORE2",
        "purpose": purpose,
        "question_ref": row["question_ref"],
        "bucket_id": row["bucket_id"],
        "problem_family_ref": row["problem_family_ref"],
        "source_snapshot": {
            "source_body": rep["source_body"],
            "figure_semantics": rep.get("figure_semantics", []),
            "source_contract_ref": rep["source_contract_ref"],
            "answer_contract_ref": rep["answer_contract_ref"],
        },
        "teaching_release": {
            "status": "RELEASED",
            "required_capability_refs": row["required_capability_refs"],
            "receipt_refs": row["receipt_refs"],
        },
        "learner_support": {
            "try_it_first": True,
            "small_clue": hints["H1_NOTICE"],
            "bigger_clue": hints["H2_MODEL"],
            "how_do_i_start": hints["H3_START"],
            "think_it_through": [rep["first_step_reference"]],
            "quick_check": rep["verification"],
        },
        "answer_path": {
            "full_working": rep["solution"],
            "verification": rep["verification"],
        },
        "provenance": {
            "origin": "SOURCE_CORE2",
            "learner_label": "WHERE THIS QUESTION CAME FROM",
            "source_locator": row["source_provenance"],
        },
    }


def realize_challenge(candidate, purpose, source_rows, source_by_ref, teaching_by_cap):
    anchor = source_by_ref.get(candidate["anchor_question_ref"])
    if anchor is None:
        raise ValueError("CORE2A_SOURCE_BINDING_INVALID:" + candidate["challenge_id"])
    if anchor["problem_family_ref"] != candidate["problem_family_ref"]:
        raise ValueError("CORE2A_SOURCE_BINDING_INVALID:FAMILY_DRIFT:" + candidate["challenge_id"])
    if anchor["bucket_id"] != candidate["bucket_id"]:
        raise ValueError("CORE2A_SOURCE_BINDING_INVALID:BUCKET_DRIFT:" + candidate["challenge_id"])
    if anchor.get("release_status") != "RELEASED":
        raise ValueError("CORE2A_SOURCE_BINDING_INVALID:ANCHOR_HELD:" + candidate["challenge_id"])

    missing, receipt_refs = release_evidence(
        candidate["required_capability_refs"], teaching_by_cap
    )
    if missing:
        raise ValueError(
            "CORE2A_UNTAUGHT_PHYSICS_REQUIRED:"
            + candidate["challenge_id"]
            + ":"
            + ",".join(missing)
        )

    if candidate.get("official_past_question_claim"):
        raise ValueError("CORE2A_FALSE_OFFICIAL_ATTRIBUTION:" + candidate["challenge_id"])

    ensure_no_hint_leak(candidate)
    validation = validate_physics_case(candidate["physics_validation_case"])
    validation = bind_answer_equivalence(candidate, validation)
    near_copy = near_copy_report(candidate["prompt"], source_rows)

    return {
        "item_id": "PHY-C2A-CH-" + digest(
            {"id": candidate["challenge_id"], "purpose": purpose, "prompt": candidate["prompt"]}
        ),
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "lane": "GENERATED_ORIGINAL",
        "purpose": purpose,
        "challenge_id": candidate["challenge_id"],
        "anchor_question_ref": candidate["anchor_question_ref"],
        "bucket_id": candidate["bucket_id"],
        "problem_family_ref": candidate["problem_family_ref"],
        "archetype": candidate["archetype"],
        "prompt": candidate["prompt"],
        "required_capability_refs": candidate["required_capability_refs"],
        "receipt_refs": receipt_refs,
        "learner_support": {
            "try_it_first": True,
            "small_clue": candidate["staged_help"]["small_clue"],
            "bigger_clue": candidate["staged_help"]["bigger_clue"],
            "how_do_i_start": candidate["staged_help"]["how_do_i_start"],
        },
        "answer_path": {
            "canonical_answer": candidate["canonical_answer"],
            "full_working": candidate["full_working"],
            "quick_check": candidate["quick_check"],
        },
        "physics_validation": validation,
        "near_copy_check": near_copy,
        "provenance": {
            "origin": "GENERATED_ORIGINAL",
            "learner_label": "WHERE THIS QUESTION CAME FROM",
            "fresh_original": True,
            "official_past_question_claim": False,
            "construction_refs": candidate["construction_refs"],
        },
    }


def compile_core2a(run):
    purpose = run.get("purpose")
    if purpose not in PURPOSES:
        raise ValueError("CORE2A_PURPOSE_REQUIRED")

    teaching_by_cap, _ = teaching_index(
        run.get("taught_receipts", []),
        run["learner_profile_ref"],
        purpose,
    )

    source_rows = []
    source_by_ref = {}
    held = []
    for row in run.get("source_items", []):
        q = row["question_ref"]
        if q in source_by_ref:
            raise ValueError("CORE2A_SOURCE_BINDING_INVALID:DUPLICATE:" + q)
        missing, receipt_refs = release_evidence(
            row["required_capability_refs"], teaching_by_cap
        )
        enriched = dict(row)
        enriched["receipt_refs"] = receipt_refs
        enriched["release_status"] = "RELEASED" if not missing else "HELD_UNTIL_TEACHING_COMPLETE"
        enriched["missing_capability_refs"] = missing
        source_rows.append(enriched)
        source_by_ref[q] = enriched
        if missing:
            held.append(
                {
                    "question_ref": q,
                    "bucket_id": row["bucket_id"],
                    "status": "HELD_UNTIL_TEACHING_COMPLETE",
                    "missing_capability_refs": missing,
                }
            )

    selected_rows = choose_source_items(purpose, source_rows)
    source_products = [realize_source(row, purpose) for row in selected_rows]

    accepted = []
    for candidate in run.get("challenge_candidates", []):
        if purpose not in candidate.get("eligible_purposes", []):
            continue
        accepted.append(
            realize_challenge(candidate, purpose, source_rows, source_by_ref, teaching_by_cap)
        )

    check_purpose_coverage(purpose, selected_rows, accepted)

    blueprint = {
        "schema_version": "1.0.0",
        "product_id": "PHY-C2A-PRODUCT-" + digest(
            {
                "run": run["run_id"],
                "purpose": purpose,
                "sources": [x["question_ref"] for x in source_products],
                "challenges": [x["challenge_id"] for x in accepted],
            }
        ),
        "run_ref": run["run_id"],
        "purpose": purpose,
        "source_corpus_count": len(source_rows),
        "source_selected_count": len(source_products),
        "source_held_count": len(held),
        "source_items": source_products,
        "generated_items": accepted,
        "held_source_items": held,
        "authority_statement": {
            "core2_source_corpus_immutable": True,
            "core2a_product_selection_is_derived": True,
            "requires_teaching_complete_receipts": True,
            "learner_mastery_not_inferred_from_publication": True,
        },
    }
    audit = {
        "status": "PASS",
        "run_ref": run["run_id"],
        "purpose": purpose,
        "source_corpus_count": len(source_rows),
        "source_selected_count": len(source_products),
        "source_held_count": len(held),
        "generated_count": len(accepted),
        "product_ref": blueprint["product_id"],
        "checks": [
            "PURPOSE_EXPLICIT",
            "SOURCE_CORPUS_CUSTODY",
            "TEACHING_RECEIPT_GATE",
            "SOURCE_FIDELITY",
            "PHYSICS_INDEPENDENT_RECOMPUTE",
            "TAUGHT_SCOPE_ONLY",
            "NEAR_COPY_PASS",
            "INLINE_PROVENANCE",
            "ANSWER_CLOSURE",
        ],
    }
    return blueprint, audit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    run = json.loads(Path(args.run).read_text(encoding="utf-8"))
    blueprint, audit = compile_core2a(run)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "physics_core2a_product.json").write_text(
        json.dumps(blueprint, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "physics_core2a_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
