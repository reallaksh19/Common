#!/usr/bin/env python3
"""P-H falsifiers: primitives must be REALIZED as vector graphics, bound to capabilities,
grounded in source quantities, and reconciled to physical page custody."""
import copy, json, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT.parent
sys.path[:0] = [str(ROOT / "engine"), str(PHYS / "CoreAuthoring" / "tests")]

from upstream import core1_plan, load  # noqa: E402
from build_physics_representations import (  # noqa: E402
    build_bundle, validate_bundle, validate_registry, extract_source_quantities, digest,
)
from physics_primitive_renderer import render_primitive, supported_kinds, UnknownPrimitive  # noqa: E402
from physics_page_custody import reconciliation_errors, realization_errors  # noqa: E402
from realize_physics_representations import realize, audit  # noqa: E402
from reportlab.pdfgen import canvas as rl_canvas  # noqa: E402

PASSES = []


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        PASSES.append(code)
        return
    raise AssertionError("expected " + code)


def redigest(b):
    b["bundle_digest"] = ""
    b["bundle_digest"] = digest(b, "bundle_digest")
    return b


registry = load(ROOT / "registry" / "physics-teaching-primitive-registry.json")
profile = load(ROOT / "registry" / "physics-page-intent-profile.json")
contract = load(ROOT / "registry" / "physics-figure-render-contract.json")
questions = load(PHYS / "AssessmentIntake" / "fixtures" / "motion-question-set.fixture.json")
scope, model, plan = core1_plan(attempts=True)
scope_na, model_na, plan_na = core1_plan(attempts=False)


def build(p=None, m=None, q=None, reg=None, prof=None, con=None):
    return build_bundle(
        copy.deepcopy(p or plan), copy.deepcopy(m or model), copy.deepcopy(q or questions),
        copy.deepcopy(reg or registry), copy.deepcopy(prof or profile), copy.deepcopy(con or contract),
    )


bundle = build()
PASSES.append("REPRESENTATION_BUNDLE_BUILDS_FROM_REAL_P_G_PLAN")
assert build()["bundle_digest"] == bundle["bundle_digest"]
PASSES.append("REPRESENTATION_BUNDLE_DETERMINISTIC")

# ---------------------------------------------------------------- registry ---
# Every primitive named in #256 / #234 Phase 7 exists.
required = set(registry["required_primitive_ids"])
declared = {p["primitive_id"] for p in registry["primitives"]}
assert required <= declared, sorted(required - declared)
assert {"PHENOMENON_SCENE", "MOTION_STRIP", "VECTOR_STATE_VIEW", "PHASE_BOUNDARY_VIEW",
        "TRAJECTORY_VIEW", "POSITION_TIME_GRAPH", "VELOCITY_TIME_GRAPH", "FORCE_DIAGRAM",
        "SIGN_FRAME_OVERLAY", "DIAGRAM_EQUATION_BRIDGE"} <= declared
PASSES.append("REQUIRED_TEACHING_PRIMITIVE_PRESENT")

# Every declared primitive has a real renderer.
assert declared <= set(supported_kinds()), sorted(declared - set(supported_kinds()))
PASSES.append("EVERY_PRIMITIVE_HAS_A_RENDERER")

missing_required = copy.deepcopy(registry)
missing_required["primitives"] = [p for p in missing_required["primitives"]
                                  if p["primitive_id"] != "FORCE_DIAGRAM"]
missing_required["registry_digest"] = ""
missing_required["registry_digest"] = digest(missing_required, "registry_digest")
expect("REQUIRED_TEACHING_PRIMITIVE_MISSING", lambda: validate_registry(missing_required))

decorative = copy.deepcopy(registry)
decorative["primitives"][0]["decorative"] = True
decorative["registry_digest"] = ""
decorative["registry_digest"] = digest(decorative, "registry_digest")
expect("DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS", lambda: validate_registry(decorative))

label_only = copy.deepcopy(registry)
label_only["primitives"][0]["realized_as_vector_graphics"] = False
label_only["registry_digest"] = ""
label_only["registry_digest"] = digest(label_only, "registry_digest")
expect("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", lambda: validate_registry(label_only))

no_floor = copy.deepcopy(registry)
no_floor["primitives"][0]["minimum_vector_ops"] = 0
no_floor["registry_digest"] = ""
no_floor["registry_digest"] = digest(no_floor, "registry_digest")
expect("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", lambda: validate_registry(no_floor))

# ------------------------------------------------- realization is measured ---
# THE central falsifier: every primitive must draw real vector graphics, measured
# at draw time, above its declared floor. A text-only figure cannot pass.
with tempfile.TemporaryDirectory() as td:
    c = rl_canvas.Canvas(str(Path(td) / "probe.pdf"), pagesize=(595.2756, 841.8898))
    floors = {p["primitive_id"]: p["minimum_vector_ops"] for p in registry["primitives"]}
    for kind in supported_kinds():
        ev = render_primitive(kind, {}, c, (40, 400, 515, 150))
        assert ev["realized"] is True, kind
        assert ev["vector_ops"] >= floors[kind], (kind, ev["vector_ops"], floors[kind])
        assert ev["ink_bbox"] is not None, kind
    c.save()
PASSES.append("EVERY_PRIMITIVE_REALIZED_ABOVE_ITS_VECTOR_FLOOR")

try:
    render_primitive("NOT_A_PRIMITIVE", {}, None, (0, 0, 10, 10))
    raise AssertionError("unknown primitive accepted")
except UnknownPrimitive:
    PASSES.append("UNKNOWN_TEACHING_PRIMITIVE_REJECTED")

# a placement that drew only text is rejected by the custody layer
fake = {"content_placements": [
    {"content_ref": "REP-X", "primitive": "PHENOMENON_SCENE", "vector_ops": 0, "text_ops": 12},
]}
errs = realization_errors(fake, {"PHENOMENON_SCENE": 8})
assert any("label-only" in e for e in errs), errs
PASSES.append("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED")

# ------------------------------------------------------- capability binding ---
caps = {r["capability_ref"] for r in model["capability_records"]}
assert {s["capability_ref"] for s in bundle["representations"]} == caps
PASSES.append("EVERY_CAPABILITY_HAS_A_REPRESENTATION")

orphan = copy.deepcopy(bundle)
orphan["representations"][0]["capability_ref"] = "PHY-CAP-NOT-IN-SCOPE"
redigest(orphan)
expect("VISUAL_WITHOUT_CAPABILITY_BINDING",
       lambda: validate_bundle(orphan, plan, model, questions, registry, profile, contract))

nojob = copy.deepcopy(bundle)
nojob["representations"][0]["instructional_job"] = "looks nice"
redigest(nojob)
expect("VISUAL_WITHOUT_INSTRUCTIONAL_JOB",
       lambda: validate_bundle(nojob, plan, model, questions, registry, profile, contract))

decor = copy.deepcopy(bundle)
decor["representations"][0]["decorative"] = True
redigest(decor)
expect("DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS",
       lambda: validate_bundle(decor, plan, model, questions, registry, profile, contract))

# ------------------------------------------ representation obligation custody ---
mapping = profile["primitive_by_representation_requirement"]
for r in model["capability_records"]:
    pids = {s["primitive_id"] for s in bundle["representations"] if s["capability_ref"] == r["capability_ref"]}
    for req in r["representation_requirements"]:
        assert mapping[req] in pids, (r["capability_ref"], req)
PASSES.append("EVERY_REPRESENTATION_OBLIGATION_HAS_A_PRIMITIVE")

dropped = copy.deepcopy(bundle)
victim = next(s for s in dropped["representations"] if s["primitive_id"] == "STATE_TABLE")
dropped["representations"] = [s for s in dropped["representations"]
                              if not (s["capability_ref"] == victim["capability_ref"]
                                      and s["primitive_id"] == "STATE_TABLE")]
redigest(dropped)
expect("REPRESENTATION_REQUIREMENT_DROPPED_FROM_REPRESENTATION",
       lambda: validate_bundle(dropped, plan, model, questions, registry, profile, contract))

trimming = copy.deepcopy(profile)
trimming["representation_obligations_never_trimmed"] = False
expect("REPRESENTATION_REQUIREMENT_DROPPED_FROM_REPRESENTATION", lambda: build(prof=trimming))

no_gate = copy.deepcopy(bundle)
target_cap = next(l["capability_ref"] for l in plan["lessons"]
                  if l["model_validity_required"] and l["lesson_mode"] == "FULL_LEARNING")
no_gate["representations"] = [s for s in no_gate["representations"]
                              if not (s["capability_ref"] == target_cap
                                      and s["primitive_id"] == "MODEL_VALIDITY_GATE")]
redigest(no_gate)
expect("MODEL_VALIDITY_REQUIRED_BUT_NOT_VISIBLE",
       lambda: validate_bundle(no_gate, plan, model, questions, registry, profile, contract))

no_check = copy.deepcopy(bundle)
vcap = next(l["capability_ref"] for l in plan["lessons"] if l["verification_steps"])
no_check["representations"] = [s for s in no_check["representations"]
                               if not (s["capability_ref"] == vcap
                                       and s["primitive_id"] == "VERIFICATION_CHECK_STRIP")]
redigest(no_check)
expect("VERIFICATION_REQUIRED_BUT_NOT_VISIBLE",
       lambda: validate_bundle(no_check, plan, model, questions, registry, profile, contract))

# ---------------------------------------------------- quantitative grounding ---
grounded = [s for s in bundle["representations"] if s["quantitative_grounding"] == "SOURCE_QUANTITIES"]
assert grounded, "fixture must ground at least one figure in source quantities"
by_q = {q["question_id"]: q for q in questions["questions"]}
for s in grounded:
    for q in s["source_quantities"]:
        item = by_q[q["item_ref"]]
        blob = " ".join([g["text"] for g in item["givens"]] + [item["stem"]]
                        + [iv["text"] for iv in item.get("time_intervals", [])])
        assert q["source_text"] in blob
PASSES.append("EVERY_FIGURE_QUANTITY_TRACES_TO_A_SOURCE_ITEM")

invented = copy.deepcopy(bundle)
target = next(s for s in invented["representations"] if s["source_quantities"])
target["source_quantities"][0]["source_text"] = "u=999 m/s"
redigest(invented)
expect("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE",
       lambda: validate_bundle(invented, plan, model, questions, registry, profile, contract))

foreign = copy.deepcopy(bundle)
target = next(s for s in foreign["representations"] if s["source_quantities"])
target["source_quantities"][0]["item_ref"] = "Q99"
redigest(foreign)
expect("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE",
       lambda: validate_bundle(foreign, plan, model, questions, registry, profile, contract))

overclaim = copy.deepcopy(bundle)
target = next(s for s in overclaim["representations"]
              if s["quantitative_grounding"] == "SCHEMATIC_STRUCTURE_ONLY")
target["quantitative_grounding"] = "SOURCE_QUANTITIES"
redigest(overclaim)
expect("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE",
       lambda: validate_bundle(overclaim, plan, model, questions, registry, profile, contract))

# A schematic frame strip must not display the shared library's own hard-coded
# example journey as if the Physics source had stated it.
frame_specs = [s for s in bundle["representations"] if s["primitive_id"] == "SIGN_FRAME_OVERLAY"]
assert frame_specs
for s in frame_specs:
    assert s["render_params"].get("legs") == [], s["representation_id"]
PASSES.append("SHARED_LIBRARY_DEFAULT_JOURNEY_NOT_PRESENTED_AS_SOURCE")

# --------------------------------------------------------------- extraction ---
src = extract_source_quantities(questions, ["Q5"], contract)
symbols = {r["symbol"]: r["value"] for r in src["named_quantities"]}
assert symbols.get("u") == 0.0 and symbols.get("a") == 2.0 and symbols.get("v") == 10.0, symbols
src6 = extract_source_quantities(questions, ["Q6"], contract)
g = next(r for r in src6["named_quantities"] if r["symbol"] == "g")
assert g["direction"] == "downward" and g["value"] == 10.0
assert src6["declared_frames"][0]["positive_direction"] == "upward"
PASSES.append("SOURCE_QUANTITY_EXTRACTION_IS_FAITHFUL")

# ------------------------------------------------------- physical custody ---
with tempfile.TemporaryDirectory() as td:
    page_map, pdf_path = realize(bundle, registry, contract, td)
    pdf_bytes = Path(pdf_path).read_bytes()
    assert audit(page_map, pdf_bytes, registry, contract)
    PASSES.append("PHYSICAL_PAGE_CUSTODY_RECONCILES")

    assert page_map["realization_summary"]["label_only_figure_count"] == 0
    assert page_map["realization_summary"]["figure_count"] == len(bundle["representations"])
    PASSES.append("EVERY_REPRESENTATION_PHYSICALLY_PLACED")

    with tempfile.TemporaryDirectory() as td2:
        page_map2, pdf2 = realize(bundle, registry, contract, td2)
        assert Path(pdf2).read_bytes() == pdf_bytes
        assert page_map2["page_map_digest"] == page_map["page_map_digest"]
        PASSES.append("REALIZATION_IS_BYTE_DETERMINISTIC")

    expect("EXACT_ARTIFACT_HASH_MISMATCH",
           lambda: audit(page_map, pdf_bytes + b"\n", registry, contract))

    lost = copy.deepcopy(page_map)
    lost["content_placements"] = lost["content_placements"][:-1]
    expect("PHYSICAL_PAGE_CUSTODY_FAILURE", lambda: audit(lost, pdf_bytes, registry, contract))

    planned = copy.deepcopy(page_map)
    planned["actual_placement_evidence"] = False
    expect("PHYSICAL_PAGE_CUSTODY_FAILURE", lambda: audit(planned, pdf_bytes, registry, contract))

    escaped = copy.deepcopy(page_map)
    escaped["content_placements"][0]["ink_bbox"]["x1"] = page_map["page_width_pt"] + 60
    expect("PHYSICAL_PAGE_CUSTODY_FAILURE", lambda: audit(escaped, pdf_bytes, registry, contract))

    off_intent = copy.deepcopy(page_map)
    off_intent["content_placements"][0]["page"] = 999
    expect("PHYSICAL_PAGE_CUSTODY_FAILURE", lambda: audit(off_intent, pdf_bytes, registry, contract))

    starved = copy.deepcopy(page_map)
    starved["content_placements"][0]["vector_ops"] = 1
    expect("PHYSICAL_PAGE_CUSTODY_FAILURE", lambda: audit(starved, pdf_bytes, registry, contract))

    # a bundle whose spec floor exceeds what the primitive draws fails at render time
    starved_bundle = copy.deepcopy(bundle)
    starved_bundle["representations"][0]["minimum_vector_ops"] = 10_000
    redigest(starved_bundle)
    with tempfile.TemporaryDirectory() as td3:
        expect("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
               lambda: realize(starved_bundle, registry, contract, td3))

# ------------------------------------------------------------ scope stability ---
bundle_na = build(p=plan_na, m=model_na)
obligation_primitives = set(mapping.values())


def obligation_set(b):
    return {
        (s["capability_ref"], s["primitive_id"])
        for s in b["representations"]
        if s["primitive_id"] in obligation_primitives
    }


# The assessment-derived representation obligations are identical with and without
# attempts. Learner evidence may add or remove *conditional* teaching support
# (anchor scene, motion strip, misconception contrast); it may never remove an
# obligation the assessment created.
assert obligation_set(bundle_na) == obligation_set(bundle)
assert {s["capability_ref"] for s in bundle_na["representations"]} == \
       {s["capability_ref"] for s in bundle["representations"]}
PASSES.append("ATTEMPT_MODE_DOES_NOT_CHANGE_REPRESENTATION_OBLIGATIONS")

# and the difference is only conditional support, never fewer obligations
assert len(bundle_na["representations"]) >= len(bundle["representations"])
PASSES.append("LEARNER_EVIDENCE_ONLY_REMOVES_CONDITIONAL_SUPPORT")

# ---------------------------------------------------------------- authority ---
drift = copy.deepcopy(bundle)
drift["study_model_digest"] = "0" * 64
redigest(drift)
expect("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING",
       lambda: validate_bundle(drift, plan, model, questions, registry, profile, contract))

nocolour = copy.deepcopy(contract)
nocolour["accessibility"]["grayscale_safe_required"] = False
expect("COLOUR_IS_THE_ONLY_CHANNEL", lambda: build(con=nocolour))

print(f"PHY P-H representation and realization falsifiers: {len(PASSES)} PASS")
for code in PASSES:
    print("  -", code)
