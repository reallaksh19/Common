#!/usr/bin/env python3
"""P-A0 contract validation: the frozen source question ledger and its reconciliation report."""
import json, sys, warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
C = ROOT / "contracts"
sys.path[:0] = [str(ROOT / "engine")]

from build_physics_source_ledger import reconcile, validate_ledger  # noqa: E402


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


ledger = load(ROOT / "registry" / "physics-source-question-ledger.json")
questions = load(PHYS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
review = load(PHYS / "AssessmentReview" / "registry" / "physics-item-validity-registry.json")

Draft202012Validator(load(C / "physics-source-question-ledger.schema.json")).validate(ledger)
validate_ledger(ledger)

report = reconcile(ledger, questions, review)
Draft202012Validator(load(C / "physics-source-reconciliation-report.schema.json")).validate(report)

# Without a coverage matrix the engine must say so rather than claim completeness.
assert any(f["code"] == "COVERAGE_PROVEN_ONLY_AGAINST_ITSELF" for f in report["findings"])
assert ledger["derived_from_question_set"] is False
assert ledger["production_claim"] is False, "the synthetic Motion ledger may not claim production"

print(
    "PHY P-A0 contract validation: PASS "
    f"(ledger {report['ledger_denominator']} source items / "
    f"{report['summary']['direct_expected']} direct, question set "
    f"{report['question_set_denominator']} items, "
    f"state={report['reconciliation_state']} without a coverage matrix)"
)
