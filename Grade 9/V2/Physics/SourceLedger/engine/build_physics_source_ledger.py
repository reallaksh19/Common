#!/usr/bin/env python3
"""P-A0 — Physics source question reconciliation ledger.

    PhysicsSourceQuestionLedger    (frozen from the source documents, before authoring)
  + P-A question set               (what extraction actually produced)
  + P-B item validity registry     (what review deliberately excluded, and why)
  + optional P-J source coverage matrix
  -> PhysicsSourceReconciliationReport

Why this phase exists
---------------------

P-J's completeness proof is relative to whatever P-A's ``question_set`` already
contains. If extraction silently drops a source item, every downstream matrix still
reconciles perfectly against a denominator that is itself already short, and "concept
coverage looks complete" while direct source items have no home at all.

The ledger is the independent denominator. It is transcribed from the source documents
**before** authoring, it declares ``derived_from_question_set: false``, and it is
digest-frozen. Reconciliation then compares three things that can disagree:

1. what the source documents say exists          (the ledger),
2. what extraction produced                      (the question set),
3. what the product actually teaches or excludes (the coverage matrix).

The engine is generic. Every topic-specific fact lives in the ledger data; adding a
Physics topic means adding a ledger, not a code branch.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

D = Path(__file__).resolve().parents[1]

# A ledger is only an independent denominator if it predates the authoring it judges.
PHASE_ORDER = ["P-A", "P-B", "P-C", "P-D", "P-E", "P-F", "P-G"]
COVERED_DISPOSITIONS = {"COVERED_IN_CORE1_LESSON", "COVERED_IN_CORE1_PRACTICE"}
EXCUSED_DISPOSITIONS = {"EXCLUDED_BY_REVIEW"}


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


# --------------------------------------------------------------- ledger custody


def validate_ledger(ledger):
    """Structural and honesty checks on the frozen ledger itself."""
    if ledger.get("subject") != "PHYSICS":
        fail("SOURCE_LEDGER_DIGEST_MISMATCH", "ledger subject")
    if ledger.get("ledger_digest") != digest(ledger, "ledger_digest"):
        fail("SOURCE_LEDGER_DIGEST_MISMATCH", ledger.get("ledger_id", "ledger"))
    if ledger.get("derived_from_question_set") is not False:
        fail("SOURCE_LEDGER_DERIVED_FROM_QUESTION_SET", ledger.get("ledger_id", "ledger"))
    if ledger.get("frozen_before_phase") not in PHASE_ORDER:
        fail("SOURCE_LEDGER_NOT_FROZEN_BEFORE_AUTHORING", str(ledger.get("frozen_before_phase")))
    if ledger.get("ledger_class") == "SYNTHETIC_FIXTURE_LEDGER" and ledger.get("production_claim"):
        fail("SOURCE_LEDGER_IS_SYNTHETIC_CLAIMED_AS_PRODUCTION", ledger.get("ledger_id", "ledger"))

    seen = {}
    for doc in ledger["source_documents"]:
        if doc.get("document_digest") != digest(doc, "document_digest"):
            fail("SOURCE_LEDGER_DIGEST_MISMATCH", doc["document_id"])
        if len(doc["items"]) != doc["declared_item_count"]:
            fail("SOURCE_LEDGER_DIGEST_MISMATCH",
                 f"{doc['document_id']}: declared {doc['declared_item_count']} listed {len(doc['items'])}")
        for item in doc["items"]:
            if item["item_ref"] in seen:
                fail("SOURCE_LEDGER_DIGEST_MISMATCH", "duplicate item " + item["item_ref"])
            seen[item["item_ref"]] = item

    declared_direct = sorted(ledger["expected_direct_item_refs"])
    derived_direct = sorted(r for r, i in seen.items() if i["item_class"] == "DIRECT")
    if declared_direct != derived_direct:
        fail("SOURCE_LEDGER_DIGEST_MISMATCH",
             "expected_direct_item_refs does not match the listed DIRECT items")
    declared_support = sorted(ledger.get("expected_supporting_item_refs") or [])
    derived_support = sorted(r for r, i in seen.items() if i["item_class"] == "SUPPORTING")
    if declared_support != derived_support:
        fail("SOURCE_LEDGER_DIGEST_MISMATCH",
             "expected_supporting_item_refs does not match the listed SUPPORTING items")
    return seen


def ledger_is_usable_for(ledger, phase):
    """A ledger frozen at or before ``phase`` can independently judge that phase's output."""
    return PHASE_ORDER.index(ledger["frozen_before_phase"]) <= PHASE_ORDER.index(phase)


# ------------------------------------------------------------- reconciliation


def excluded_items(review_registry):
    out = {}
    for row in (review_registry or {}).get("items", []):
        ref = row.get("item_ref") or row.get("question_id")
        state = row.get("validity_state") or row.get("state")
        if ref and state and state not in {"VALID", "VALID_WITH_NOTE"}:
            out[ref] = row.get("reason") or state
    return out


def reconcile(ledger, question_set, review_registry=None, source_coverage_matrix=None,
              report_id="PHY-P-A0-SOURCE-RECONCILIATION-v1"):
    items = validate_ledger(ledger)
    present = {q["question_id"] for q in question_set.get("questions", [])}
    excluded = excluded_items(review_registry)
    coverage = {}
    if source_coverage_matrix:
        for row in source_coverage_matrix.get("rows", []):
            coverage[row["item_ref"]] = row

    rows, findings = [], []

    def note(code, ref, detail):
        findings.append({"code": code, "ref": ref, "detail": detail})

    for ref in sorted(items):
        item = items[ref]
        row = {
            "item_ref": ref,
            "item_class": item["item_class"],
            "source_order": item.get("source_order"),
            "declared_subtopic_ref": item.get("declared_subtopic_ref"),
            "coverage_disposition": None,
            "coverage_home_refs": [],
            "exclusion_reason": excluded.get(ref),
        }
        if ref in present:
            row["disposition"] = "PRESENT_IN_QUESTION_SET"
        elif ref in excluded:
            row["disposition"] = "EXCLUDED_BY_REVIEW"
        else:
            row["disposition"] = "ABSENT_FROM_QUESTION_SET"
            if item["item_class"] != "NON_ASSESSED":
                note("SOURCE_ITEM_MISSING_FROM_QUESTION_SET", ref,
                     "The source documents list this item, extraction did not produce it, and review "
                     "did not exclude it. Every downstream coverage proof is therefore short by one "
                     "item it cannot see.")

        cov = coverage.get(ref)
        if cov is not None:
            row["coverage_disposition"] = cov.get("disposition")
            row["coverage_home_refs"] = sorted(
                list(cov.get("core1_lesson_refs") or []) + list(cov.get("core1_practice_item_refs") or []))
        if item["item_class"] == "DIRECT" and source_coverage_matrix is not None:
            # A review exclusion is a home: the item is accounted for, with a stated reason.
            home_ok = ref in excluded or (cov is not None and cov.get("disposition") in (
                COVERED_DISPOSITIONS | EXCUSED_DISPOSITIONS))
            if not home_ok:
                note("DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME", ref,
                     "A direct source item has no lesson, no practice item and no review exclusion. "
                     "Concept coverage can still look complete while this item has nowhere to live.")
        rows.append(row)

    for ref in sorted(present - set(items)):
        rows.append({
            "item_ref": ref, "item_class": "UNDECLARED",
            "disposition": "UNDECLARED_BY_SOURCE_LEDGER",
            "source_order": None, "declared_subtopic_ref": None,
            "coverage_disposition": (coverage.get(ref) or {}).get("disposition"),
            "coverage_home_refs": [], "exclusion_reason": None,
        })
        note("QUESTION_SET_ITEM_NOT_IN_SOURCE_LEDGER", ref,
             "The question set contains an item the frozen source ledger does not list. Either the "
             "ledger is stale or the item did not come from the declared source.")

    if source_coverage_matrix is None:
        note("COVERAGE_PROVEN_ONLY_AGAINST_ITSELF", ledger["ledger_id"],
             "No coverage matrix was supplied, so this run proves only that extraction matches the "
             "source listing, not that every direct source item has a home in the product.")

    direct = [r for r in rows if r["item_class"] == "DIRECT"]
    report = {
        "report_id": report_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "ledger_ref": ledger["ledger_id"],
        "ledger_digest": ledger["ledger_digest"],
        "ledger_class": ledger["ledger_class"],
        "question_set_ref": question_set["question_set_id"],
        "question_set_digest": question_set.get("question_set_digest") or digest(question_set),
        "coverage_matrix_ref": (source_coverage_matrix or {}).get("matrix_id"),
        "ledger_denominator": len(items),
        "question_set_denominator": len(present),
        "rows": rows,
        "findings": sorted(findings, key=lambda f: (f["code"], f["ref"])),
        "reconciliation_state": "RECONCILED" if not findings else "OPEN",
        "summary": {
            "direct_expected": len(direct),
            "direct_present": sum(1 for r in direct if r["disposition"] == "PRESENT_IN_QUESTION_SET"),
            "direct_absent": sum(1 for r in direct if r["disposition"] == "ABSENT_FROM_QUESTION_SET"),
            "direct_without_coverage_home": sum(
                1 for f in findings if f["code"] == "DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME"),
            "undeclared_question_set_items": sum(
                1 for r in rows if r["disposition"] == "UNDECLARED_BY_SOURCE_LEDGER"),
        },
        "report_digest": "",
    }
    report["report_digest"] = digest(report, "report_digest")
    return report


def assert_reconciled(report):
    """Fail-closed form: raise on the first finding, naming its own falsifier."""
    if report["findings"]:
        first = report["findings"][0]
        fail(first["code"], f"{first['ref']}: {first['detail']}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Reconcile a Physics question set against its frozen source ledger")
    ap.add_argument("--ledger", default=str(D / "registry" / "physics-source-question-ledger.json"))
    ap.add_argument("--question-set", required=True)
    ap.add_argument("--review-registry")
    ap.add_argument("--source-coverage-matrix")
    ap.add_argument("--out")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on any finding")
    a = ap.parse_args()

    report = reconcile(
        load(a.ledger), load(a.question_set),
        load(a.review_registry) if a.review_registry else None,
        load(a.source_coverage_matrix) if a.source_coverage_matrix else None,
    )
    if a.out:
        Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
    print(f"PHY P-A0 source reconciliation: {report['reconciliation_state']} "
          f"(ledger {report['ledger_denominator']} items, question set "
          f"{report['question_set_denominator']} items)")
    for f in report["findings"]:
        print(f"  - {f['code']}: {f['ref']}")
    return 1 if (a.strict and report["findings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
