#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path

D = Path(__file__).resolve().parents[1]
CHEM = D.parent
sys.path.insert(0, str(D / "engine"))
sys.path.insert(0, str(CHEM / "AssessmentReview" / "engine"))

from build_chemistry_scope import build_scope, digest_without_field  # noqa: E402
from review_chemistry_assessment import build_review, load_registry as load_review_registry  # noqa: E402

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def expect_error(code, fn):
    try:
        fn()
    except ValueError as exc:
        assert str(exc).startswith(code), (code, str(exc))
        return
    raise AssertionError(f"expected {code}")

A = CHEM / "AssessmentIntake" / "fixtures"
R = CHEM / "AssessmentReview"
S = D / "registry"

sources = load(A / "mixed-chemistry-source.fixture.json")
questions = load(A / "mixed-chemistry-question-set.fixture.json")
corpus = load(A / "mixed-chemistry-external-corpus.fixture.json")
scope = load(A / "mixed-chemistry-topic-scope.fixture.json")
review_registry, manifest_digest = load_review_registry(R / "registry" / "chemistry-item-validity-registry.json")
review_bundle = build_review(
    copy.deepcopy(sources), copy.deepcopy(questions), review_registry,
    load(R / "policies" / "chemistry-diagnostic-use-policy.json"),
    load(R / "registry" / "chemistry-qc-events.json"),
    registry_manifest_digest=manifest_digest
)
source_ledger = load(S / "chemistry-source-obligation-ledger.json")
question_bindings = load(S / "chemistry-question-capability-bindings.json")
external = load(S / "chemistry-external-corpus-classification.json")
authority = load(D / "authority" / "chemistry-canonical-authority.json")

def run(sl=None, qb=None, ex=None, au=None, rb=None):
    return build_scope(
        copy.deepcopy(sources), copy.deepcopy(questions), copy.deepcopy(corpus), copy.deepcopy(scope),
        copy.deepcopy(rb if rb is not None else review_bundle),
        copy.deepcopy(sl if sl is not None else source_ledger),
        copy.deepcopy(qb if qb is not None else question_bindings),
        copy.deepcopy(ex if ex is not None else external),
        copy.deepcopy(au if au is not None else authority),
    )

bundle = run()
assert bundle["bundle_digest"] == digest_without_field(bundle, "bundle_digest")
assert bundle["summary"]["source_obligation_total"] == 12
assert bundle["summary"]["question_item_total"] == 17
assert bundle["summary"]["external_candidate_total"] == 6
assert bundle["summary"]["external_eligible_total"] == 5
assert bundle["summary"]["external_source_unresolved_total"] == 1
assert bundle["summary"]["finding_count"] == 6
assert bundle["summary"]["counters_derived_from_records"] is True
assert bundle["assessment_coverage_matrix"]["summary"]["source_scope_status_counts"] == {"ELIGIBLE_IN_SCOPE":10,"OUT_OF_SCOPE":2}
assert bundle["assessment_coverage_matrix"]["summary"]["question_scope_status_counts"] == {"ELIGIBLE_IN_SCOPE":14,"OUT_OF_SCOPE":2,"SOURCE_UNRESOLVED":1}
assert bundle["assessment_coverage_matrix"]["summary"]["external_eligible_total"] == 5
assert bundle["assessment_scope_model"]["eligible_primary_units"]["FORMULA"]
assert bundle["assessment_scope_model"]["eligible_primary_units"]["REACTION"]
assert bundle["assessment_scope_model"]["eligible_primary_units"]["PRACTICAL"]
assert bundle["prerequisite_closure"]["status"] == "CLOSED"

# 1 SOURCE_OBLIGATION_DROPPED_DURING_SCOPE_DERIVATION
bad = copy.deepcopy(source_ledger)
bad["obligations"] = bad["obligations"][:-1]
expect_error("SOURCE_OBLIGATION_DROPPED_DURING_SCOPE_DERIVATION", lambda: run(sl=bad))

# 2 EXAMSIDE_TOPIC_LABEL_TREATED_AS_ELIGIBILITY
bad = copy.deepcopy(external)
bad["classifications"][0]["eligibility_basis"] = "TOPIC_LABEL"
expect_error("EXAMSIDE_TOPIC_LABEL_TREATED_AS_ELIGIBILITY", lambda: run(ex=bad))

# 3 DECLARED_SCOPE_SILENTLY_OVERRIDES_SOURCE
bad = copy.deepcopy(review_bundle)
next(x for x in bad["source_reviews"] if x["source_unit_ref"] == "CS01")["source_integrity_state"] = "REVIEW_REQUIRED"
expect_error("DECLARED_SCOPE_SILENTLY_OVERRIDES_SOURCE", lambda: run(rb=bad))

# 4 QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE
bad = copy.deepcopy(question_bindings)
r = next(x for x in bad["bindings"] if x["item_ref"] == "CQ08")
r["scope_status"] = "ELIGIBLE_IN_SCOPE"
r["declared_topic_refs"] = ["PRACTICAL"]
r["primary_learner_unit"] = "PRACTICAL"
expect_error("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE", lambda: run(qb=bad))

# 5 CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC
bad = copy.deepcopy(authority)
bad["declared_topic_bindings"]["FORMULA"]["allowed_concept_refs"].append("CHEM-CONCEPT-NOT-REGISTERED")
expect_error("CANONICAL_CHEMISTRY_SILENTLY_ADDS_UNDECLARED_TOPIC", lambda: run(au=bad))

# 6 QUESTION_WITHOUT_EXPLICIT_SCOPE_STATE
bad = copy.deepcopy(question_bindings)
next(x for x in bad["bindings"] if x["item_ref"] == "CQ04")["scope_status"] = ""
expect_error("QUESTION_WITHOUT_EXPLICIT_SCOPE_STATE", lambda: run(qb=bad))

# 7 PREREQUISITE_INFERRED_BUT_NOT_RECORDED
bad = copy.deepcopy(question_bindings)
next(x for x in bad["bindings"] if x["item_ref"] == "CQ03")["prerequisite_capability_refs"] = []
expect_error("PREREQUISITE_INFERRED_BUT_NOT_RECORDED", lambda: run(qb=bad))

# 8 CONDITION_EXCEPTION_INFERRED_BUT_NOT_RECORDED
bad = copy.deepcopy(question_bindings)
next(x for x in bad["bindings"] if x["item_ref"] == "CQ07")["conditions_exceptions"] = []
expect_error("CONDITION_EXCEPTION_INFERRED_BUT_NOT_RECORDED", lambda: run(qb=bad))

# 9 REPRESENTATION_DEPENDENCY_DROPPED
bad = copy.deepcopy(question_bindings)
next(x for x in bad["bindings"] if x["item_ref"] == "CQ10")["representation_demands"] = []
expect_error("REPRESENTATION_DEPENDENCY_DROPPED", lambda: run(qb=bad))

# 10 ELIGIBLE_ITEM_WITHOUT_UNIQUE_PRIMARY_HOME
bad = copy.deepcopy(external)
next(x for x in bad["classifications"] if x["candidate_id"] == "EXT01")["primary_learner_unit"] = None
expect_error("ELIGIBLE_ITEM_WITHOUT_UNIQUE_PRIMARY_HOME", lambda: run(ex=bad))

# 11 COUNTERS_ACCEPTED_WITHOUT_RECORD_DERIVATION
bad = copy.deepcopy(external)
bad["summary"] = {"eligible_total":999}
expect_error("COUNTERS_ACCEPTED_WITHOUT_RECORD_DERIVATION", lambda: run(ex=bad))

# Low-confidence external source cannot be promoted to eligible just because a title looks relevant.
bad = copy.deepcopy(external)
r = next(x for x in bad["classifications"] if x["candidate_id"] == "EXT06")
r.update({
    "scope_status":"ELIGIBLE_IN_SCOPE","declared_topic_refs":["PRACTICAL"],
    "canonical_concept_refs":["CHEM-CONCEPT-APPARATUS-METHOD"],
    "canonical_capability_refs":["CAP-READ-APPARATUS-METHOD"],
    "problem_family_refs":["QF-APPARATUS-METHOD"],"representation_demands":["FIGURE"],
    "primary_learner_unit":"PRACTICAL","eligibility_basis":"MINIMUM_SOLUTION_PATH_FROM_SYNTHETIC_FIXTURE"
})
expect_error("QUESTION_EVIDENCE_SILENTLY_EXPANDS_SCOPE", lambda: run(ex=bad))

again = run()
assert json.dumps(bundle, sort_keys=True, separators=(",", ":"), ensure_ascii=False) == json.dumps(again, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

print("CHEMISTRY C-C required falsifiers = 11 PASS")
print("CHEMISTRY C-C low-confidence external fail-closed = PASS")
print("CHEMISTRY C-C baseline = 12 source obligations / 17 question items / 6 external candidates")
print("CHEMISTRY C-C external classification = 5 eligible / 1 source unresolved")
print("CHEMISTRY C-C deterministic replay = PASS")
