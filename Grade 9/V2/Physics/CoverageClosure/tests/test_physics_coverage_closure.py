#!/usr/bin/env python3
"""P-J falsifiers: coverage closure, evidence feedback and longitudinal honesty."""
import copy, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
sys.path[:0] = [
    str(ROOT / "engine"), str(PHYS / "Representation" / "engine"),
    str(PHYS / "Core2Transfer" / "engine"), str(PHYS / "CoreAuthoring" / "tests"),
]

from upstream import core1_plan, core2_plan, representation_bundle, question_set, load  # noqa: E402
from realize_physics_representations import realize  # noqa: E402
from build_physics_coverage_closure import (  # noqa: E402
    build_closure, validate_closure, validate_ledger, dimension_state, digest,
)

PASSES = []


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        PASSES.append(code)
        return
    raise AssertionError("expected " + code)


def redigest(c):
    c["closure_digest"] = ""
    c["closure_digest"] = digest(c, "closure_digest")
    return c


scope, model, core1 = core1_plan(attempts=True)
bundle = representation_bundle(core1, model)
core2 = core2_plan(core1, model, scope)
rep = PHYS / "Representation"
registry = load(rep / "registry" / "physics-teaching-primitive-registry.json")
contract = load(rep / "registry" / "physics-figure-render-contract.json")
policy = load(ROOT / "registry" / "physics-transfer-evidence-policy.json")
ledger = load(ROOT / "fixtures" / "physics-transfer-evidence.fixture.json")
classification = load(PHYS / "Core2Transfer" / "registry" / "physics-external-corpus-classification.json")
review = load(PHYS / "AssessmentReview" / "registry" / "physics-item-validity-registry.json")
questions = question_set()

TMP = tempfile.TemporaryDirectory()
page_map, _ = realize(bundle, registry, contract, TMP.name)


def build(q=None, rv=None, c1=None, rb=None, c2=None, cl=None, sc=None, m=None,
          pol=None, led=..., pm=...):
    return build_closure(
        copy.deepcopy(q or questions), copy.deepcopy(rv or review), copy.deepcopy(c1 or core1),
        copy.deepcopy(rb or bundle), copy.deepcopy(c2 or core2), copy.deepcopy(cl or classification),
        copy.deepcopy(sc or scope), copy.deepcopy(m or model), copy.deepcopy(pol or policy),
        copy.deepcopy(ledger if led is ... else led),
        copy.deepcopy(page_map if pm is ... else pm),
    )


closure = build()
PASSES.append("CLOSURE_BUILDS_FROM_THE_REAL_P_G_P_H_P_I_CHAIN")
assert build()["closure_digest"] == closure["closure_digest"]
PASSES.append("CLOSURE_DETERMINISTIC")

assert closure["closure_state"] == "CLOSED" and not closure["gaps"]
assert closure["physically_realized"] is True
PASSES.append("CLOSURE_CLOSED_ONLY_WITH_ZERO_GAPS")

# ------------------------------------------------------------ source coverage
matrix = closure["source_coverage_matrix"]
assert matrix["denominator"] == len(questions["questions"])
assert not matrix["uncovered_item_refs"]
PASSES.append("EVERY_SOURCE_ITEM_ACCOUNTED_FOR")

thin_core1 = copy.deepcopy(core1)
victim = thin_core1["lessons"][0]["scope_trace"]["source_scope_trace_item_refs"]
orphan_item = victim[0]
for lesson in thin_core1["lessons"]:
    lesson["scope_trace"]["source_scope_trace_item_refs"] = [
        r for r in lesson["scope_trace"]["source_scope_trace_item_refs"] if r != orphan_item
    ]
thin_core1["plan_digest"] = ""
thin_core1["plan_digest"] = digest(thin_core1, "plan_digest")
thin_bundle = copy.deepcopy(bundle)
thin_bundle["core1_plan_digest"] = thin_core1["plan_digest"]
thin_bundle["bundle_digest"] = ""
thin_bundle["bundle_digest"] = digest(thin_bundle, "bundle_digest")
thin_core2 = copy.deepcopy(core2)
thin_core2["core1_plan_digest"] = thin_core1["plan_digest"]
thin_core2["plan_digest"] = ""
thin_core2["plan_digest"] = digest(thin_core2, "plan_digest")
open_closure = build(c1=thin_core1, rb=thin_bundle, c2=thin_core2, pm=None)
assert open_closure["closure_state"] == "OPEN"
assert any(g["gap_class"] == "SOURCE_ITEM_UNCOVERED" for g in open_closure["gaps"])
PASSES.append("UNCOVERED_SOURCE_ITEM_OPENS_CLOSURE")

lying = copy.deepcopy(open_closure)
lying["closure_state"] = "CLOSED"
redigest(lying)
expect("SOURCE_ITEM_UNCOVERED_BUT_CLOSURE_CLAIMED",
       lambda: validate_closure(lying, scope, model, policy))

# --------------------------------------------------------- external coverage
ext = closure["external_corpus_coverage_matrix"]
assert ext["denominator"] == len(classification["classifications"])
assert not ext["uncovered_candidate_refs"]
assert any(r["disposition"] == "EXCLUDED_BY_REVIEW" for r in ext["rows"])
PASSES.append("EVERY_EXTERNAL_CANDIDATE_ACCOUNTED_FOR")

missing_page = copy.deepcopy(core2)
missing_page["transfer_pages"] = missing_page["transfer_pages"][:-1]
missing_page["plan_digest"] = ""
missing_page["plan_digest"] = digest(missing_page, "plan_digest")
gapped = build(c2=missing_page)
assert gapped["closure_state"] == "OPEN"
assert any(g["gap_class"] == "EXTERNAL_CANDIDATE_UNCOVERED" for g in gapped["gaps"])
PASSES.append("UNCOVERED_EXTERNAL_CANDIDATE_OPENS_CLOSURE")

lying_ext = copy.deepcopy(gapped)
lying_ext["closure_state"] = "CLOSED"
lying_ext["gaps"] = []
redigest(lying_ext)
expect("EXTERNAL_CANDIDATE_UNCOVERED_BUT_CLOSURE_CLAIMED",
       lambda: validate_closure(lying_ext, scope, model, policy))

# ---------------------------------------------------- representation coverage
thin_reps = copy.deepcopy(bundle)
dropped_cap = thin_reps["representations"][0]["capability_ref"]
thin_reps["representations"] = [s for s in thin_reps["representations"]
                                if s["capability_ref"] != dropped_cap]
thin_reps["bundle_digest"] = ""
thin_reps["bundle_digest"] = digest(thin_reps, "bundle_digest")
no_rep = build(rb=thin_reps, pm=None)
assert any(g["gap_class"] == "CAPABILITY_WITHOUT_REPRESENTATION_COVERAGE" for g in no_rep["gaps"])
PASSES.append("CAPABILITY_WITHOUT_REPRESENTATION_COVERAGE")

# ------------------------------------------------------- physical realization
unrealized = build(pm=None)
assert unrealized["closure_state"] == "OPEN"
assert unrealized["physically_realized"] is False
assert any(g["gap_class"] == "PHYSICAL_REALIZATION_ABSENT" for g in unrealized["gaps"])
PASSES.append("CLOSURE_REQUIRES_PHYSICAL_REALIZATION")

fake_realized = copy.deepcopy(unrealized)
fake_realized["closure_state"] = "CLOSED"
fake_realized["gaps"] = []
redigest(fake_realized)
expect("CLOSURE_CLAIMED_WITHOUT_PHYSICAL_REALIZATION",
       lambda: validate_closure(fake_realized, scope, model, policy))

label_only = copy.deepcopy(page_map)
label_only["realization_summary"]["label_only_figure_count"] = 1
starved = build(pm=label_only)
assert any(g["gap_class"] == "TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED" for g in starved["gaps"])
PASSES.append("LABEL_ONLY_FIGURE_OPENS_CLOSURE")

drifted_map = copy.deepcopy(page_map)
drifted_map["bundle_digest"] = "0" * 64
expect("CLOSURE_CLAIMED_WITHOUT_PHYSICAL_REALIZATION", lambda: build(pm=drifted_map))

# -------------------------------------------------- longitudinal honesty -----
# THE carried-forward invariant: one current success may not close a future obligation.
for u in closure["longitudinal_update"]["capability_updates"]:
    assert u["dimensions_after"]["delayed_retention"] != "CLOSED", u["capability_ref"]
PASSES.append("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL")

xt = next(u for u in closure["longitudinal_update"]["capability_updates"]
          if u["capability_ref"] == "PHY-CAP-XT-SLOPE-VELOCITY")
assert xt["dimensions_after"]["near_transfer"] == "OPEN_WITH_PARTIAL_EVIDENCE"
assert xt["evidence_detail"]["near_transfer"]["blocked_reason"] == \
       "SINGLE_CURRENT_SUCCESS_MAY_NOT_CLOSE_THIS_DIMENSION"
PASSES.append("SINGLE_NEW_INSTANCE_DOES_NOT_CLOSE_NEAR_TRANSFER")

# two distinct successes still may not close far transfer before the declared delay
state, detail = dimension_state(
    "far_transfer",
    [
        {"event_class": "CORE2_NEW_CONTEXT", "outcome": "CORRECT", "instance_ref": "I1", "days_since_core1": 1},
        {"event_class": "CORE2_NEW_CONTEXT", "outcome": "CORRECT", "instance_ref": "I2", "days_since_core1": 2},
    ],
    policy, "OPEN",
)
assert state == "OPEN_WITH_PARTIAL_EVIDENCE" and detail["blocked_reason"] == "BELOW_MINIMUM_DELAY"
PASSES.append("FAR_TRANSFER_REQUIRES_THE_DECLARED_DELAY")

# and delayed retention requires both the count and the delay
state, detail = dimension_state(
    "delayed_retention",
    [
        {"event_class": "DELAYED_RETRIEVAL", "outcome": "CORRECT", "instance_ref": "I1", "days_since_core1": 30},
        {"event_class": "DELAYED_RETRIEVAL", "outcome": "CORRECT", "instance_ref": "I2", "days_since_core1": 40},
    ],
    policy, "OPEN",
)
assert state == "CLOSED", detail
PASSES.append("DELAYED_RETENTION_CLOSES_ONLY_ON_DELAYED_REPEATED_EVIDENCE")

forged = copy.deepcopy(closure)
u = forged["longitudinal_update"]["capability_updates"][0]
u["dimensions_after"]["delayed_retention"] = "CLOSED"
redigest(forged)
expect("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL",
       lambda: validate_closure(forged, scope, model, policy))

forged_far = copy.deepcopy(closure)
u = forged_far["longitudinal_update"]["capability_updates"][0]
u["dimensions_after"]["far_transfer"] = "CLOSED"
redigest(forged_far)
expect("ONE_CURRENT_SUCCESS_CLOSES_FUTURE_EVIDENCE",
       lambda: validate_closure(forged_far, scope, model, policy))

dropped_dim = copy.deepcopy(closure)
dropped_dim["longitudinal_update"]["capability_updates"][0]["dimensions_after"].pop("fluency")
redigest(dropped_dim)
expect("LONGITUDINAL_DIMENSION_DROPPED",
       lambda: validate_closure(dropped_dim, scope, model, policy))

# --------------------------------------------------------- evidence custody --
for e in ledger["events"]:
    assert e["source_trace_refs"] and e["instance_ref"]
PASSES.append("EVERY_EVIDENCE_EVENT_CARRIES_A_SOURCE_TRACE")

untraced = copy.deepcopy(ledger)
untraced["events"][0]["source_trace_refs"] = []
untraced["events"][0]["event_digest"] = ""
untraced["events"][0]["event_digest"] = digest(untraced["events"][0], "event_digest")
untraced["ledger_digest"] = ""
untraced["ledger_digest"] = digest(untraced, "ledger_digest")
expect("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", lambda: validate_ledger(untraced, scope, policy))

tampered = copy.deepcopy(ledger)
tampered["events"][0]["outcome"] = "CORRECT" if tampered["events"][0]["outcome"] != "CORRECT" else "INCORRECT"
tampered["ledger_digest"] = ""
tampered["ledger_digest"] = digest(tampered, "ledger_digest")
expect("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", lambda: validate_ledger(tampered, scope, policy))

production = copy.deepcopy(ledger)
production["production_claim"] = True
production["ledger_digest"] = ""
production["ledger_digest"] = digest(production, "ledger_digest")
expect("SYNTHETIC_EVIDENCE_CLAIMED_AS_PRODUCTION", lambda: validate_ledger(production, scope, policy))

offscope = copy.deepcopy(ledger)
offscope["events"][0]["capability_ref"] = "PHY-CAP-NOT-IN-SCOPE"
offscope["events"][0]["event_digest"] = ""
offscope["events"][0]["event_digest"] = digest(offscope["events"][0], "event_digest")
offscope["ledger_digest"] = ""
offscope["ledger_digest"] = digest(offscope, "ledger_digest")
expect("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", lambda: validate_ledger(offscope, scope, policy))

# ------------------------------------------------ scope is never shrunk ------
scope_caps = {r["capability_ref"] for r in scope["capability_scope_records"]}
assert {r["capability_ref"] for r in closure["learner_state_update"]["capability_updates"]} == scope_caps
assert all(r["remains_in_assessment_scope"] for r in closure["learner_state_update"]["capability_updates"])
PASSES.append("TRANSFER_EVIDENCE_DOES_NOT_SHRINK_ASSESSMENT_SCOPE")

shrunk = copy.deepcopy(closure)
shrunk["learner_state_update"]["capability_updates"] = \
    shrunk["learner_state_update"]["capability_updates"][:-1]
redigest(shrunk)
expect("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE",
       lambda: validate_closure(shrunk, scope, model, policy))

# a capability with an incorrect transfer attempt stays in scope, marked as difficulty
mp = next(r for r in closure["learner_state_update"]["capability_updates"]
          if r["capability_ref"] == "PHY-CAP-MULTIPHASE-KINEMATICS")
assert mp["updated_state"] == "EVIDENCE_OF_DIFFICULTY" and mp["remains_in_assessment_scope"] is True
PASSES.append("DIFFICULTY_EVIDENCE_DOES_NOT_REMOVE_A_CAPABILITY")

# ------------------------------------------------------------------ honesty --
claimed = copy.deepcopy(closure)
claimed["human_expert_review_states"]["PEDAGOGY_EXPERT_PASS"] = "PASS"
redigest(claimed)
expect("FAKE_HUMAN_REVIEW_STATE", lambda: validate_closure(claimed, scope, model, policy))

# a run with no evidence at all leaves every dimension untouched and still closes coverage
no_evidence = build(led=None)
assert no_evidence["summary"]["evidence_event_count"] == 0
assert no_evidence["closure_state"] == "CLOSED"
for u in no_evidence["longitudinal_update"]["capability_updates"]:
    assert all(v != "CLOSED" for v in u["dimensions_after"].values())
PASSES.append("NO_EVIDENCE_RUN_CLOSES_NO_LONGITUDINAL_DIMENSION")

TMP.cleanup()
print(f"PHY P-J coverage closure falsifiers: {len(PASSES)} PASS")
for code in PASSES:
    print("  -", code)
