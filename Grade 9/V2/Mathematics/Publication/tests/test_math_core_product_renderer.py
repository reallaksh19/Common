#!/usr/bin/env python3
"""Falsifier suite for the Mathematics Core1/Core2 renderer (#319).

Runs the real M-chain cold start, renders both products, and asserts that the
renderer is genuinely bound to M-chain output, genuinely realizes teaching
primitives as vector geometry, and never overstates its own review authority.
"""
import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
PUB = HERE.parents[1]
MATH = HERE.parents[2]
for path in (
    PUB / "engine",
    MATH / "ColdStart" / "engine",
    MATH / "Core1Authoring" / "engine",
    MATH.parent / "Shared" / "MasterTemplates",
):
    sys.path.insert(0, str(path))

import math_primitive_adapter as adapter  # noqa: E402
import realize_math_core_products as rr  # noqa: E402
from author_math_core1 import load_candidate_bundle  # noqa: E402
from math_cold_start_runner import REPO, load, run_cold_start  # noqa: E402


def expect(code, fn):
    try:
        fn()
    except ValueError as e:
        assert str(e).startswith(code), (code, str(e))
        return
    raise AssertionError(f"expected {code}")


FIX = MATH / "AssessmentIntake" / "fixtures"
QUESTIONS = load(FIX / "mixed-grade9-question-set.fixture.json")
TOPIC = load(FIX / "mixed-grade9-topic-scope.fixture.json")
REPORT, INTERNALS = run_cold_start(copy.deepcopy(QUESTIONS), copy.deepcopy(TOPIC), repo_root=REPO, run_id="MATH-M-K-RUN-A")
CORE1 = INTERNALS["core1_plan"]
CORE2 = INTERNALS["core2"]
CLOSURE = INTERNALS["closure"]
PRIMITIVES = load(MATH / "RepresentationSemantics" / "registry" / "math-teaching-primitive-registry.json")
_, ASSETS = load_candidate_bundle(MATH / "InstructionalKnowledge" / "registry" / "math-pck-candidates.json")

assert CORE1 is not None, "COLD_START_STILL_BLOCKED_AFTER_PCK_FIX"

# Every canonical teaching primitive has a real realization: none is label-only.
registry_names = {p["canonical_name"] for p in PRIMITIVES["primitives"]}
assert registry_names.issubset(set(adapter.SUPPORTED_KINDS)), sorted(registry_names - set(adapter.SUPPORTED_KINDS))
for name in registry_names:
    assert adapter.library_binding(name), name

work = Path(tempfile.mkdtemp(prefix="math-core-products-"))
try:
    RESULT, PER = rr.realize(CORE1, CORE2, CLOSURE, ASSETS, PRIMITIVES, work)
    SCHEMAS = {
        name: json.loads((PUB / "contracts" / name).read_text(encoding="utf-8"))
        for name in (
            "math-core-product-page-map.schema.json",
            "math-core-product-manifest.schema.json",
            "math-core-product-realization.schema.json",
        )
    }
    for schema in SCHEMAS.values():
        Draft202012Validator.check_schema(schema)
    Draft202012Validator(SCHEMAS["math-core-product-realization.schema.json"]).validate(RESULT)

    # Determinism: the same M-chain input renders byte-identical artifacts.
    work2 = Path(tempfile.mkdtemp(prefix="math-core-products-b-"))
    try:
        RESULT2, _ = rr.realize(CORE1, CORE2, CLOSURE, ASSETS, PRIMITIVES, work2)
        assert RESULT["artifact_set_digest"] == RESULT2["artifact_set_digest"], "renderer is not deterministic"
    finally:
        shutil.rmtree(work2, ignore_errors=True)

    core2_page_map = None
    for role in rr.PRODUCTS:
        pdf_path, structure, page_map, audit, manifest = PER[role]
        Draft202012Validator(SCHEMAS["math-core-product-page-map.schema.json"]).validate(page_map)
        Draft202012Validator(SCHEMAS["math-core-product-manifest.schema.json"]).validate(manifest)
        if role == "CORE2_TRANSFER_BOOK":
            core2_page_map = page_map

        # RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT: the manifest binds real M-chain digests.
        assert manifest["upstream"]["core1_plan_digest"] == CORE1["plan_digest"]
        assert manifest["upstream"]["core2_plan_digest"] == CORE2["plan_digest"]
        assert manifest["upstream"]["coverage_package_digest"] == CLOSURE["package_digest"]

        # ARTIFACT_HASH_NOT_BOUND: the manifest hash is the hash of the bytes on disk.
        import hashlib

        assert manifest["artifact_sha256"] == hashlib.sha256(Path(pdf_path).read_bytes()).hexdigest()
        assert page_map["artifact_sha256"] == manifest["artifact_sha256"]

        # TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED: real vector figures exist.
        assert page_map["figure_count"] >= 1 and page_map["vector_figure_count"] >= 1

        # PLACEMENT_OUT_OF_PAGE_BOUNDS
        for row in page_map["content_placements"]:
            assert 0 <= row["x0"] < row["x1"] <= rr.PAGE_W
            assert 0 <= row["y0"] < row["y1"] <= rr.PAGE_H

        # MATERIAL_CONTENT_NOT_PLACED: structure and page map agree exactly.
        structure_refs = [ref for intent in structure["page_intents"] for ref in intent["content_refs"]]
        assert sorted(structure_refs) == sorted(row["content_ref"] for row in page_map["content_placements"])
        assert len(structure_refs) == len(set(structure_refs))

        # PUBLICATION_ENGINEERING_CLAIMED_AS_SUBJECT_PASS
        assert manifest["quality_states"]["PUBLICATION_ENGINEERING"] == "PASS"
        for dimension in ("SUBJECT_CORRECTNESS", "PEDAGOGICAL_DESIGN", "ASSESSMENT_DESIGN", "VISUAL_USABILITY"):
            assert manifest["quality_states"][dimension] == "PENDING"

        # PROVISIONAL_PRODUCT_CLAIMED_RELEASE_LEGAL
        assert manifest["release_legal"] is False
        assert manifest["upstream"]["pck_expert_review_state"] == "PENDING"

    # The Core2 book must draw at least one numerically grounded figure from
    # declared item data: that is what separates a real diagram from a label.
    numeric = [r for r in core2_page_map["content_placements"] if r.get("data_grounding") == "DECLARED_NUMERIC"]
    assert numeric, "no figure was grounded in declared numeric item data"
    assert any(r["primitive"] == "COORDINATE_PLANE" for r in numeric)
    assert any(r["primitive"] == "SLOPE_TRIANGLE_VIEW" for r in numeric)

    # SOURCE_QUESTION_SHAPE_DRIFT: every original question reaches the book.
    structure = PER["CORE2_TRANSFER_BOOK"][1]
    titles = " ".join(i["title"] for i in structure["page_intents"])
    for page in CORE2["pages"]:
        assert page["question_ref"] + "." in titles, page["question_ref"]

    assert RESULT["release_legal"] is False
    assert RESULT["publication_engineering"] == "PASS"
finally:
    shutil.rmtree(work, ignore_errors=True)


# --- adapter-level falsifiers ------------------------------------------------
class _NullCanvas:
    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return 0

        return _noop


# UNKNOWN_TEACHING_PRIMITIVE_KIND
expect(
    "UNKNOWN_TEACHING_PRIMITIVE_KIND",
    lambda: adapter.render_primitive("NOT_A_PRIMITIVE", {"payload": {"a": 1}}, _NullCanvas(), (0, 0, 10, 10)),
)
# MATH_VISUAL_EMPTY_PARAMS
expect(
    "MATH_VISUAL_EMPTY_PARAMS",
    lambda: adapter.render_primitive("COORDINATE_PLANE", {"payload": {}}, _NullCanvas(), (0, 0, 10, 10)),
)
# MATH_VISUAL_OUT_OF_BOUNDS
expect(
    "MATH_VISUAL_OUT_OF_BOUNDS",
    lambda: adapter.render_primitive("COORDINATE_PLANE", {"payload": {"points": []}}, _NullCanvas(), (0, 0, 0, 10)),
)
# MATH_VISUAL_UNGROUNDED_VALUE: a number the item never declared cannot be drawn.
expect(
    "MATH_VISUAL_UNGROUNDED_VALUE",
    lambda: adapter.assert_grounded({"declared_text": ["A=(1,2)"], "declared_claims": []}, ["99"]),
)
adapter.assert_grounded({"declared_text": ["A=(1,2)"], "declared_claims": []}, ["1", "2"])

# Declared-point extraction reads only what the item declares.
points = adapter.declared_points(
    {"source_stem": "check A(-2,-2), B(8,2) and C(3,0)", "source_givens": [], "source_options": [],
     "source_units": [], "source_subparts": [], "solution_route": {"steps": [], "final_answer": {}}}
)
assert [(p["label"], p["x"], p["y"]) for p in points] == [("A", -2.0, -2.0), ("B", 8.0, 2.0), ("C", 3.0, 0.0)]

# RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT: a tampered plan is refused.
bad_core1 = copy.deepcopy(CORE1)
bad_core1["lessons"] = []
expect(
    "RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT",
    lambda: rr.realize(bad_core1, CORE2, CLOSURE, ASSETS, PRIMITIVES, tempfile.mkdtemp(prefix="math-bad-")),
)
drifted = copy.deepcopy(CORE2)
drifted["pages"][0]["source_stem"] = "tampered"
expect(
    "RENDERER_DISCONNECTED_FROM_M_CHAIN_OUTPUT",
    lambda: rr.realize(CORE1, drifted, CLOSURE, ASSETS, PRIMITIVES, tempfile.mkdtemp(prefix="math-bad2-")),
)
# TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED: an unrealized registry entry blocks the render.
label_only = copy.deepcopy(PRIMITIVES)
label_only["primitives"].append(dict(label_only["primitives"][0], canonical_name="UNREALIZED_LABEL_PRIMITIVE"))
expect(
    "TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
    lambda: rr.realize(CORE1, CORE2, CLOSURE, ASSETS, label_only, tempfile.mkdtemp(prefix="math-bad3-")),
)

print("MATH renderer: two products realized from real M-chain JSON, vector primitives PASS")
print("MATH renderer: publication engineering PASS; subject/pedagogy/assessment/visual review PENDING")
