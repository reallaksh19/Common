#!/usr/bin/env python3
"""P-I falsifiers: graded hint ladder, Core1 linkage, source-body custody, scope eligibility."""
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
sys.path[:0] = [str(ROOT / "engine"), str(PHYS / "CoreAuthoring" / "tests")]

from upstream import core1_plan, load  # noqa: E402
from build_physics_core2_transfer import (  # noqa: E402
    build_plan, validate_plan, validate_corpus, hint_violations, digest, LEVELS,
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


def redigest(p):
    p["plan_digest"] = ""
    p["plan_digest"] = digest(p, "plan_digest")
    return p


corpus = load(ROOT / "fixtures" / "physics-external-transfer-source.fixture.json")
classification = load(ROOT / "registry" / "physics-external-corpus-classification.json")
profile = load(ROOT / "registry" / "physics-core2-authoring-profile.json")
badges = load(ROOT / "registry" / "physics-transfer-badge-policy.json")
segregation = load(ROOT / "registry" / "physics-concept-segregation.json")
scope, model, core1 = core1_plan(attempts=True)
scope_na, model_na, core1_na = core1_plan(attempts=False)


def build(cp=None, cl=None, c1=None, m=None, s=None, pr=None, bd=None, sg=None):
    return build_plan(
        copy.deepcopy(cp or corpus), copy.deepcopy(cl or classification),
        copy.deepcopy(c1 or core1), copy.deepcopy(m or model), copy.deepcopy(s or scope),
        copy.deepcopy(pr or profile), copy.deepcopy(bd or badges), copy.deepcopy(sg or segregation),
    )


plan = build()
PASSES.append("CORE2_PLAN_BUILDS_FROM_REAL_P_G_PLAN")
assert build()["plan_digest"] == plan["plan_digest"]
PASSES.append("CORE2_PLAN_DETERMINISTIC")

# ------------------------------------------------------------ eligibility ---
eligible = {c["candidate_id"] for c in classification["classifications"]
            if c["scope_status"] == "ELIGIBLE_IN_SCOPE"}
out_of_scope = {c["candidate_id"] for c in classification["classifications"]
                if c["scope_status"] != "ELIGIBLE_IN_SCOPE"}
assert out_of_scope, "fixture must include an out-of-scope candidate"
assert {p["candidate_ref"] for p in plan["transfer_pages"]} == eligible
PASSES.append("EVERY_ELIGIBLE_CANDIDATE_HAS_A_CORE2_PAGE")
assert not ({p["candidate_ref"] for p in plan["transfer_pages"]} & out_of_scope)
PASSES.append("OUT_OF_SCOPE_CANDIDATE_NOT_PUBLISHED")

dropped = copy.deepcopy(plan)
dropped["transfer_pages"] = dropped["transfer_pages"][:-1]
redigest(dropped)
expect("ELIGIBLE_ITEM_MISSING_CORE2",
       lambda: validate_plan(dropped, corpus, classification, core1, model, scope, profile, badges, segregation))

smuggled = copy.deepcopy(plan)
extra = copy.deepcopy(smuggled["transfer_pages"][0])
extra["candidate_ref"] = sorted(out_of_scope)[0]
extra["page_id"] = "PHY-CORE2-" + extra["candidate_ref"]
smuggled["transfer_pages"].append(extra)
redigest(smuggled)
expect("OUT_OF_SCOPE_ITEM_PUBLISHED_AS_CORE2",
       lambda: validate_plan(smuggled, corpus, classification, core1, model, scope, profile, badges, segregation))

unscoped = copy.deepcopy(classification)
row = next(c for c in unscoped["classifications"] if c["scope_status"] == "ELIGIBLE_IN_SCOPE")
row["primary_capability_ref"] = "PHY-CAP-NOT-IN-ASSESSMENT-SCOPE"
unscoped["registry_digest"] = ""
unscoped["registry_digest"] = digest(unscoped, "registry_digest")
expect("EXTERNAL_CANDIDATE_OUTSIDE_ASSESSMENT_SCOPE", lambda: build(cl=unscoped))

# --------------------------------------------------------- source custody ---
bodies = validate_corpus(corpus)
for p in plan["transfer_pages"]:
    body = bodies[p["candidate_ref"]]
    assert p["stem"] == body["stem"] and p["options"] == body["options"]
    assert p["source_link"] == body["source_link"]
PASSES.append("SOURCE_BODY_PRESERVED_EXACTLY")

rewritten = copy.deepcopy(plan)
rewritten["transfer_pages"][0]["stem"] = "A simplified restatement of the question."
redigest(rewritten)
expect("SOURCE_BODY_REWRITTEN",
       lambda: validate_plan(rewritten, corpus, classification, core1, model, scope, profile, badges, segregation))

lost_option = copy.deepcopy(plan)
lost_option["transfer_pages"][0]["options"] = lost_option["transfer_pages"][0]["options"][:-1]
redigest(lost_option)
expect("SOURCE_BODY_REWRITTEN",
       lambda: validate_plan(lost_option, corpus, classification, core1, model, scope, profile, badges, segregation))

thin_corpus = copy.deepcopy(corpus)
thin_corpus["records"][0]["options"] = thin_corpus["records"][0]["options"][:1]
thin_corpus["records"][0]["body_digest"] = ""
thin_corpus["records"][0]["body_digest"] = digest(thin_corpus["records"][0], "body_digest")
thin_corpus["candidates"][0]["source_digest"] = thin_corpus["records"][0]["body_digest"]
thin_corpus["corpus_digest"] = ""
thin_corpus["corpus_digest"] = digest(thin_corpus, "corpus_digest")
expect("MCQ_OPTION_LOST", lambda: validate_corpus(thin_corpus))

figless = copy.deepcopy(plan)
target = next(p for p in figless["transfer_pages"] if p["figure_required"])
target["figure_semantic"] = None
redigest(figless)
expect("SOURCE_FIGURE_LOST",
       lambda: validate_plan(figless, corpus, classification, core1, model, scope, profile, badges, segregation))

nolink = copy.deepcopy(plan)
nolink["transfer_pages"][0]["source_link"] = ""
redigest(nolink)
expect("SOURCE_LINK_MISSING_OR_WRONG",
       lambda: validate_plan(nolink, corpus, classification, core1, model, scope, profile, badges, segregation))

production_claim = copy.deepcopy(corpus)
production_claim["production_claim"] = True
production_claim["corpus_digest"] = ""
production_claim["corpus_digest"] = digest(production_claim, "corpus_digest")
expect("SYNTHETIC_CORPUS_CLAIMED_AS_PRODUCTION", lambda: validate_corpus(production_claim))

# ------------------------------------------------------------ hint ladder ---
for p in plan["transfer_pages"]:
    assert [h["level"] for h in p["hint_ladder"]] == list(LEVELS)
    assert p["hint_ladder"][0]["reveals_relation"] is False
    assert all(h["reveals_result"] is False for h in p["hint_ladder"])
PASSES.append("HINT_LADDER_IS_GRADED_H1_H2_H3")

# an H1 that names a relation is rejected
assert hint_violations("H1_NOTICE", "Use v = u + a t here.", ["A", "B"], profile) == ["RELATION"]
# an H2 that substitutes is rejected
assert "SUBSTITUTION" in hint_violations("H2_MODEL", "Substitute the values now.", ["A"], profile)
# any level naming an option label is rejected
assert "OPTION_LABEL" in hint_violations("H3_START", "Pick option B.", ["A", "B"], profile)
# any level stating a result is rejected
assert "RESULT" in hint_violations("H3_START", "Therefore the speed is 48 km/h.", ["A"], profile)
PASSES.append("HINT_CONTENT_RULES_ARE_ENFORCED_PER_LEVEL")

leaky = copy.deepcopy(plan)
leaky["transfer_pages"][0]["hint_ladder"][0]["text"] = "Notice that the answer is 48 km/h."
redigest(leaky)
expect("HINT_REVEALS_ANSWER",
       lambda: validate_plan(leaky, corpus, classification, core1, model, scope, profile, badges, segregation))

answer_text = copy.deepcopy(plan)
page = answer_text["transfer_pages"][0]
body = bodies[page["candidate_ref"]]
answer = next(o["text"] for o in body["options"] if o["label"] == body["answer_key"])
page["hint_ladder"][2]["text"] = "First move: consider " + answer + " carefully."
redigest(answer_text)
expect("HINT_REVEALS_ANSWER",
       lambda: validate_plan(answer_text, corpus, classification, core1, model, scope, profile, badges, segregation))

collapsed = copy.deepcopy(plan)
collapsed["transfer_pages"][0]["hint_ladder"] = collapsed["transfer_pages"][0]["hint_ladder"][1:]
redigest(collapsed)
expect("HINT_LADDER_COLLAPSES_TO_SOLUTION",
       lambda: validate_plan(collapsed, corpus, classification, core1, model, scope, profile, badges, segregation))

skipped = copy.deepcopy(plan)
ladder = skipped["transfer_pages"][0]["hint_ladder"]
ladder[0], ladder[1] = ladder[1], ladder[0]
redigest(skipped)
expect("HINT_LADDER_COLLAPSES_TO_SOLUTION",
       lambda: validate_plan(skipped, corpus, classification, core1, model, scope, profile, badges, segregation))

h1_relation = copy.deepcopy(plan)
h1_relation["transfer_pages"][0]["hint_ladder"][0]["reveals_relation"] = True
redigest(h1_relation)
expect("HINT_LADDER_COLLAPSES_TO_SOLUTION",
       lambda: validate_plan(h1_relation, corpus, classification, core1, model, scope, profile, badges, segregation))

# ---------------------------------------------------------- core1 linkage ---
lessons = {l["capability_ref"]: l["lesson_id"] for l in core1["lessons"]}
for p in plan["transfer_pages"]:
    link = p["core1_linkage"]
    assert link["primary_core1_lesson_ref"] == lessons[link["primary_capability_ref"]]
    assert link["primary_capability_ref"] not in [s["capability_ref"] for s in link["supporting_links"]]
PASSES.append("EVERY_TRANSFER_PAGE_LINKS_TO_ITS_CORE1_LESSON")

merged = copy.deepcopy(plan)
link = merged["transfer_pages"][0]["core1_linkage"]
link["supporting_links"].append({"capability_ref": link["primary_capability_ref"],
                                 "core1_lesson_ref": link["primary_core1_lesson_ref"],
                                 "link_class": "TAUGHT_IN_CORE1"})
redigest(merged)
expect("PRIMARY_SUPPORTS_NOT_DISTINGUISHED",
       lambda: validate_plan(merged, corpus, classification, core1, model, scope, profile, badges, segregation))

untaught = copy.deepcopy(plan)
untaught["transfer_pages"][0]["core1_linkage"]["supporting_links"].append(
    {"capability_ref": "PHY-CAP-NEVER-TAUGHT", "core1_lesson_ref": "none", "link_class": "TAUGHT_IN_CORE1"}
)
redigest(untaught)
expect("CORE2_REQUIRES_UNTAUGHT_CONCEPT",
       lambda: validate_plan(untaught, corpus, classification, core1, model, scope, profile, badges, segregation))

# a declared extension without a bridge is still rejected
bad_ext = copy.deepcopy(segregation)
bad_ext["core2_only_extensions"] = [{"capability_ref": "PHY-CAP-EXTENSION", "core1_bridge_lesson_ref": None}]
bad_class = copy.deepcopy(classification)
row = next(c for c in bad_class["classifications"] if c["scope_status"] == "ELIGIBLE_IN_SCOPE")
row["supporting_capability_refs"] = sorted(row["supporting_capability_refs"] + ["PHY-CAP-EXTENSION"])
bad_class["registry_digest"] = ""
bad_class["registry_digest"] = digest(bad_class, "registry_digest")
expect("EXTERNAL_CANDIDATE_OUTSIDE_ASSESSMENT_SCOPE", lambda: build(cl=bad_class, sg=bad_ext))

# -------------------------------------------------------------- solutions ---
for p in plan["transfer_pages"]:
    sections = [s["section"] for s in p["solution"]["sections"]]
    assert sections == profile["solution_required_sections"]
    assert p["solution"]["verification_steps"]
    assert p["solution"]["verification_is_independent_of_solving_route"] is True
PASSES.append("EVERY_SOLUTION_CARRIES_AN_INDEPENDENT_PHYSICAL_CHECK")

noverify = copy.deepcopy(plan)
noverify["transfer_pages"][0]["solution"]["verification_steps"] = []
redigest(noverify)
expect("SOLUTION_WITHOUT_PHYSICAL_VERIFICATION",
       lambda: validate_plan(noverify, corpus, classification, core1, model, scope, profile, badges, segregation))

missing_section = copy.deepcopy(plan)
missing_section["transfer_pages"][0]["solution"]["sections"] = \
    missing_section["transfer_pages"][0]["solution"]["sections"][:-1]
redigest(missing_section)
expect("SOLUTION_SECTION_MISSING",
       lambda: validate_plan(missing_section, corpus, classification, core1, model, scope, profile, badges, segregation))

# ------------------------------------------------- obligation carry-through ---
records = {r["capability_ref"]: r for r in model["capability_records"]}
for p in plan["transfer_pages"]:
    rec = records[p["core1_linkage"]["primary_capability_ref"]]
    assert set(p["representation_requirements"]) == set(rec["representation_requirements"])
PASSES.append("CORE2_CARRIES_THE_PRIMARY_CAPABILITY_OBLIGATIONS")

frame_dropped = copy.deepcopy(plan)
target = next(p for p in frame_dropped["transfer_pages"] if p["frame_sign_required"])
target["frame_sign_required"] = False
redigest(frame_dropped)
expect("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_CORE2",
       lambda: validate_plan(frame_dropped, corpus, classification, core1, model, scope, profile, badges, segregation))

rep_dropped = copy.deepcopy(plan)
rep_target = next(p for p in rep_dropped["transfer_pages"] if p["representation_requirements"])
rep_target["representation_requirements"] = []
redigest(rep_dropped)
expect("REPRESENTATION_REQUIREMENT_DROPPED_FROM_CORE2",
       lambda: validate_plan(rep_dropped, corpus, classification, core1, model, scope, profile, badges, segregation))

# ------------------------------------------------- first-step reference ------
families = {f["problem_family_ref"] for f in plan["first_step_reference"]}
assert families == {p["problem_family_ref"] for p in plan["transfer_pages"]}
assert all(f["first_move"] for f in plan["first_step_reference"])
PASSES.append("FIRST_STEP_REFERENCE_COVERS_EVERY_FAMILY")

nofirst = copy.deepcopy(plan)
nofirst["first_step_reference"] = nofirst["first_step_reference"][:-1]
redigest(nofirst)
expect("FIRST_STEP_REFERENCE_MISSING",
       lambda: validate_plan(nofirst, corpus, classification, core1, model, scope, profile, badges, segregation))

# ---------------------------------------------------------------- honesty ---
claimed = copy.deepcopy(plan)
claimed["human_expert_review_states"]["SUBJECT_EXPERT_PASS"] = "PASS"
redigest(claimed)
expect("FAKE_HUMAN_REVIEW_STATE",
       lambda: validate_plan(claimed, corpus, classification, core1, model, scope, profile, badges, segregation))

contaminated = copy.deepcopy(profile)
contaminated["reference_layout_source"] = "PR156 mature study guide"
expect("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON", lambda: build(pr=contaminated))

stale = copy.deepcopy(core1)
stale["study_model_digest"] = "0" * 64
expect("CORE2_AUTHORED_AGAINST_STALE_CORE1", lambda: build(c1=stale))

# ------------------------------------------------------- attempt invariance ---
plan_na = build(c1=core1_na, m=model_na, s=scope_na)
assert plan_na["eligible_candidate_refs"] == plan["eligible_candidate_refs"]
assert {p["candidate_ref"] for p in plan_na["transfer_pages"]} == \
       {p["candidate_ref"] for p in plan["transfer_pages"]}
assert {(p["candidate_ref"], p["problem_family_ref"]) for p in plan_na["transfer_pages"]} == \
       {(p["candidate_ref"], p["problem_family_ref"]) for p in plan["transfer_pages"]}
PASSES.append("ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY")

print(f"PHY P-I Core2 transfer falsifiers: {len(PASSES)} PASS")
for code in PASSES:
    print("  -", code)
