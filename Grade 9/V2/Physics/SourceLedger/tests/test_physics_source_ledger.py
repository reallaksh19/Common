#!/usr/bin/env python3
"""P-A0 falsifiers: the source ledger is an independent denominator, not a second opinion.

The defect this phase exists to catch is the one the owner's own review of PR #332 found:
concept coverage read as complete while three direct source items had no home, because the
completeness proof was relative to the question set rather than to the source documents.
"""
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
sys.path[:0] = [str(ROOT / "engine")]

from build_physics_source_ledger import (  # noqa: E402
    reconcile, validate_ledger, assert_reconciled, digest, ledger_is_usable_for,
)

PASSES = []


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        PASSES.append(code)
        return
    raise AssertionError("expected " + code)


def refrozen(ledger):
    ledger["ledger_digest"] = ""
    ledger["ledger_digest"] = digest(ledger, "ledger_digest")
    return ledger


LEDGER = load(ROOT / "registry" / "physics-source-question-ledger.json")
QUESTIONS = load(PHYS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
REVIEW = load(PHYS / "AssessmentReview" / "registry" / "physics-item-validity-registry.json")


def covered_matrix(refs, disposition="COVERED_IN_CORE1_LESSON"):
    return {
        "matrix_id": "TEST-MATRIX",
        "rows": [{"item_ref": r, "disposition": disposition,
                  "core1_lesson_refs": ["L-" + r], "core1_practice_item_refs": []}
                 for r in refs],
    }


# ---------------------------------------------------------------- happy path
full = covered_matrix([q["question_id"] for q in QUESTIONS["questions"]])
report = reconcile(LEDGER, QUESTIONS, REVIEW, full)
assert report["reconciliation_state"] == "RECONCILED", report["findings"]
assert report["ledger_denominator"] == 14
assert report["summary"]["direct_expected"] == 14
assert report["summary"]["direct_present"] == 14
assert_reconciled(report)
PASSES.append("LEDGER_RECONCILES_A_COMPLETE_EXTRACTION")

# the ledger must be usable as an authority for the phases it judges
assert ledger_is_usable_for(LEDGER, "P-G")
assert LEDGER["derived_from_question_set"] is False
PASSES.append("LEDGER_IS_AN_INDEPENDENT_DENOMINATOR")


# ------------------------------------------- the blind spot this phase closes
# A source item that extraction never produced is invisible to a proof that uses the
# question set as its own denominator. Against the ledger it is a named finding.
short = copy.deepcopy(QUESTIONS)
short["questions"] = [q for q in short["questions"] if q["question_id"] not in {"Q5", "Q9", "Q11"}]
short_matrix = covered_matrix([q["question_id"] for q in short["questions"]])
missing = reconcile(LEDGER, short, REVIEW, short_matrix)
codes = {f["code"] for f in missing["findings"]}
assert "SOURCE_ITEM_MISSING_FROM_QUESTION_SET" in codes
assert {f["ref"] for f in missing["findings"]
        if f["code"] == "SOURCE_ITEM_MISSING_FROM_QUESTION_SET"} == {"Q5", "Q9", "Q11"}
assert missing["reconciliation_state"] == "OPEN"
assert missing["summary"]["direct_absent"] == 3
try:
    assert_reconciled(missing)
    raise AssertionError("expected a fail-closed reconciliation error")
except ValueError as e:
    assert str(e).split(":")[0] in codes, str(e)
PASSES.append("SOURCE_ITEM_MISSING_FROM_QUESTION_SET")

# and the same three items are reported as having no coverage home at all
assert "DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME" in codes
PASSES.append("MISSING_SOURCE_ITEM_IS_VISIBLE_AGAINST_THE_LEDGER")

# a direct item that IS extracted but has no lesson, practice item or exclusion
homeless = covered_matrix([q["question_id"] for q in QUESTIONS["questions"]])
homeless["rows"] = [r for r in homeless["rows"] if r["item_ref"] != "Q9"]
homeless["rows"].append({"item_ref": "Q9", "disposition": "UNCOVERED",
                         "core1_lesson_refs": [], "core1_practice_item_refs": []})
report = reconcile(LEDGER, QUESTIONS, REVIEW, homeless)
assert [f["ref"] for f in report["findings"]
        if f["code"] == "DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME"] == ["Q9"]
expect("DIRECT_SOURCE_ITEM_WITHOUT_COVERAGE_HOME", lambda: assert_reconciled(report))

# an item in the question set that the frozen ledger never listed
extra = copy.deepcopy(QUESTIONS)
extra["questions"].append(dict(extra["questions"][0], question_id="Q99"))
report = reconcile(LEDGER, extra, REVIEW, covered_matrix(
    [q["question_id"] for q in extra["questions"]]))
assert [f["ref"] for f in report["findings"]
        if f["code"] == "QUESTION_SET_ITEM_NOT_IN_SOURCE_LEDGER"] == ["Q99"]
expect("QUESTION_SET_ITEM_NOT_IN_SOURCE_LEDGER", lambda: assert_reconciled(report))

# no coverage matrix at all: the engine says so instead of implying completeness
report = reconcile(LEDGER, QUESTIONS, REVIEW)
assert any(f["code"] == "COVERAGE_PROVEN_ONLY_AGAINST_ITSELF" for f in report["findings"])
expect("COVERAGE_PROVEN_ONLY_AGAINST_ITSELF", lambda: assert_reconciled(report))


# ------------------------------------------------------------ ledger custody
circular = refrozen(dict(copy.deepcopy(LEDGER), derived_from_question_set=True))
expect("SOURCE_LEDGER_DERIVED_FROM_QUESTION_SET", lambda: validate_ledger(circular))

tampered = copy.deepcopy(LEDGER)
tampered["expected_direct_item_refs"] = tampered["expected_direct_item_refs"][:-1]
expect("SOURCE_LEDGER_DIGEST_MISMATCH", lambda: validate_ledger(tampered))

dropped = copy.deepcopy(LEDGER)
dropped["source_documents"][0]["items"] = dropped["source_documents"][0]["items"][:-1]
refrozen(dropped)
expect("SOURCE_LEDGER_DIGEST_MISMATCH", lambda: validate_ledger(dropped))

late = refrozen(dict(copy.deepcopy(LEDGER), frozen_before_phase="P-K"))
expect("SOURCE_LEDGER_NOT_FROZEN_BEFORE_AUTHORING", lambda: validate_ledger(late))

faked = refrozen(dict(copy.deepcopy(LEDGER), production_claim=True))
expect("SOURCE_LEDGER_IS_SYNTHETIC_CLAIMED_AS_PRODUCTION", lambda: validate_ledger(faked))


# ------------------------------------------------------- review exclusion path
# An item review deliberately excluded is reconciled, not reported as a gap.
excluded_review = {"items": [{"item_ref": "Q13", "validity_state": "EXCLUDED",
                              "reason": "the figure the item depends on is missing"}]}
without_q13 = copy.deepcopy(QUESTIONS)
without_q13["questions"] = [q for q in without_q13["questions"] if q["question_id"] != "Q13"]
report = reconcile(LEDGER, without_q13, excluded_review,
                   covered_matrix([q["question_id"] for q in without_q13["questions"]]))
row = next(r for r in report["rows"] if r["item_ref"] == "Q13")
assert row["disposition"] == "EXCLUDED_BY_REVIEW"
assert report["reconciliation_state"] == "RECONCILED", report["findings"]
PASSES.append("REVIEW_EXCLUSION_IS_A_HOME_NOT_A_GAP")

print("PHY P-A0 source ledger falsifiers: PASS")
for code in PASSES:
    print("  - " + code)
