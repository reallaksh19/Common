#!/usr/bin/env python3
import copy, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

SCOPE = Path(__file__).resolve().parents[1]
MATH = SCOPE.parent
sys.path.insert(0, str(SCOPE / "engine"))
from reconcile_math_assessment_scope import reconcile, digest_without_field  # noqa: E402

Q = MATH / "AssessmentIntake" / "fixtures" / "mixed-grade9-question-set.fixture.json"
T = MATH / "AssessmentIntake" / "fixtures" / "mixed-grade9-topic-scope.fixture.json"
R = MATH / "AssessmentReview" / "registry" / "assessment-item-validity-registry.json"
P = MATH / "AssessmentReview" / "policies" / "diagnostic-use-policy.json"
A = SCOPE / "authority" / "math-assessment-scope-authority.json"
B = SCOPE / "registry" / "mixed-grade9-question-scope-bindings.json"

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

BASE = tuple(load(p) for p in [Q,T,R,P,A,B])

def run(values=None):
    return reconcile(*(copy.deepcopy(x) for x in (values or BASE)))

def reseal_bindings(b):
    b["binding_registry_digest"] = digest_without_field(b, "binding_registry_digest")

def expect_code(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        return
    raise AssertionError(f"expected {code}")

scope_model, coverage, report, prereq = run()
assert coverage["coverage_complete"] is True
assert len(coverage["rows"]) == 17
assert report["summary"]["item_count"] == 17
assert report["summary"]["mapping_state_counts"] == {"MAPPED": 15,"OUTSIDE_DECLARED_SCOPE": 1,"PARTIAL_SCOPE_MATCH": 1}
codes = [f["code"] for f in report["findings"]]
assert "QUESTION_OUTSIDE_DECLARED_SCOPE" in codes
assert "PARTIAL_SCOPE_MATCH" in codes
assert "QUESTION_MAPS_TO_UNDECLARED_PREREQUISITE" in codes
assert "DECLARED_TOPIC_NOT_ASSESSED" in codes

by_item = {r["item_ref"]: r for r in coverage["rows"]}
assert by_item["Q6"]["mapping_state"] == "OUTSIDE_DECLARED_SCOPE"
assert by_item["Q6"]["canonical_capability_refs"] == ["MATH-UNORDERED-PAIR-COUNT"]
assert by_item["Q9"]["validity_state"] == "UNDERDETERMINED"
assert by_item["Q9"]["diagnostic_use"] == "POSITIVE_EVIDENCE_ONLY"
assert by_item["Q9"]["mapping_state"] == "PARTIAL_SCOPE_MATCH"
assert by_item["Q12"]["validity_state"] == "VALID_MULTIPLE_SOLUTIONS"
assert "MATH-GEOMETRIC-MODELLING" in by_item["Q12"]["prerequisite_capability_refs"]
assert scope_model["attempt_data_consumed"] is False
assert report["attempt_data_consumed"] is False

q12_findings = [f for f in report["findings"] if f["item_ref"] == "Q12"]
assert any(f["code"] == "QUESTION_MAPS_TO_UNDECLARED_PREREQUISITE" and f["capability_ref"] == "MATH-GEOMETRIC-MODELLING" for f in q12_findings)
assert any(f["code"] == "DECLARED_TOPIC_NOT_ASSESSED" and f["declared_topic_ref"] == "MATH-ALGEBRA-VERIFY" for f in report["findings"])

contracts = SCOPE / "contracts"
for schema_name, instance in [
    ("math-assessment-scope-model.schema.json", scope_model),
    ("math-assessment-coverage-matrix.schema.json", coverage),
    ("scope-reconciliation.schema.json", report),
    ("math-prerequisite-closure.schema.json", prereq),
]:
    Draft202012Validator(load(contracts / schema_name)).validate(instance)

assert run() == run()

vals=list(copy.deepcopy(BASE)); b=vals[5]
b["bindings"] = [x for x in b["bindings"] if x["item_ref"] != "Q7"]
reseal_bindings(b)
expect_code("QUESTION_DROPPED_DURING_SCOPE_DERIVATION", lambda: run(tuple(vals)))

vals=list(copy.deepcopy(BASE)); b=vals[5]
next(x for x in b["bindings"] if x["item_ref"]=="Q7")["mapping_state"]="MAGIC"
reseal_bindings(b)
expect_code("QUESTION_WITHOUT_EXPLICIT_MAPPING_STATE", lambda: run(tuple(vals)))

vals=list(copy.deepcopy(BASE)); b=vals[5]
row=next(x for x in b["bindings"] if x["item_ref"]=="Q10")
row["prerequisite_capability_refs"] = row["prerequisite_capability_refs"][1:]
reseal_bindings(b)
expect_code("PREREQUISITE_INFERRED_BUT_NOT_RECORDED", lambda: run(tuple(vals)))

vals=list(copy.deepcopy(BASE)); b=vals[5]
row=next(x for x in b["bindings"] if x["item_ref"]=="Q6")
row["mapping_state"]="MAPPED"; row["declared_topic_refs"]=["MATH-COORD-DISTANCE"]
reseal_bindings(b)
expect_code("TOPIC_LIST_SILENTLY_OVERRIDES_QUESTION_EVIDENCE", lambda: run(tuple(vals)))

vals=list(copy.deepcopy(BASE)); b=vals[5]
row=next(x for x in b["bindings"] if x["item_ref"]=="Q6")
row["declared_topic_refs"]=["MATH-COORD-DISTANCE"]
reseal_bindings(b)
expect_code("QUESTION_EVIDENCE_SILENTLY_OVERRIDES_DECLARED_BOUNDARY", lambda: run(tuple(vals)))

vals=list(copy.deepcopy(BASE)); b=vals[5]
row=next(x for x in b["bindings"] if x["item_ref"]=="Q7")
row["mapping_state"]="UNMAPPED"
for k in ["declared_topic_refs","canonical_concept_refs","canonical_capability_refs","prerequisite_capability_refs","problem_family_refs","representation_demands","verification_obligations","reasoning_role_expectations"]:
    row[k]=[]
reseal_bindings(b)
_, cov, rep, _ = run(tuple(vals))
r7=next(x for x in cov["rows"] if x["item_ref"]=="Q7")
assert r7["mapping_state"]=="UNMAPPED"
assert any(f["code"]=="UNMAPPED_QUESTION" and f["item_ref"]=="Q7" for f in rep["findings"])

vals=list(copy.deepcopy(BASE)); b=vals[5]
b["attempt_set"]={"forbidden":True}
reseal_bindings(b)
expect_code("SCOPE_RESOLUTION_CONSUMES_LEARNER_DATA", lambda: run(tuple(vals)))

print("MATH M-C scope-reconciliation falsifiers PASS")
