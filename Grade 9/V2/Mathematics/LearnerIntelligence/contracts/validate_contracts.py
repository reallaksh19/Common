#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT.parent
sys.path.insert(0, str(ROOT / "engine"))
from derive_math_learner_state import derive


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


schemas = {p.name: load(p) for p in Path(__file__).parent.glob("*.schema.json")}
for name, schema in schemas.items():
    Draft202012Validator.check_schema(schema)

questions = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-question-set.fixture.json")
attempts = load(MATH / "AssessmentIntake/fixtures/mixed-grade9-attempt-set.fixture.json")
reviews = load(MATH / "AssessmentReview/registry/assessment-item-validity-registry.json")
authority = load(MATH / "AssessmentScope/authority/math-assessment-scope-authority.json")
item_semantics = load(MATH / "ProblemSemantics/registry/mixed-grade9-item-semantics.json")
registry = load(ROOT / "registry/math-observation-type-registry.json")
reviewed = load(ROOT / "fixtures/reviewed-observations.fixture.json")

result = derive(questions, reviews, authority, item_semantics, registry, attempts, reviewed)
Draft202012Validator(schemas["learner-evidence-ledger.schema.json"]).validate(result["evidence_ledger"])
obs_validator = Draft202012Validator(schemas["reasoning-observation.schema.json"])
for obs in result["observations"]:
    obs_validator.validate(obs)
case_validator = Draft202012Validator(schemas["diagnostic-case.schema.json"])
for case in result["learner_state_snapshot"]["diagnostic_cases"]:
    case_validator.validate(case)
snapshot_for_validation = dict(result["learner_state_snapshot"])
snapshot_for_validation["diagnostic_cases"] = []
Draft202012Validator(schemas["learner-state-snapshot.schema.json"]).validate(snapshot_for_validation)

absent = derive(questions, reviews, authority, item_semantics, registry)
Draft202012Validator(schemas["learner-evidence-ledger.schema.json"]).validate(absent["evidence_ledger"])
assert absent["learner_state_snapshot"]["scope_fingerprint"] == result["learner_state_snapshot"]["scope_fingerprint"]
print(f"MATH M-E contracts PASS ({len(schemas)} schemas; present+absent branches)")
