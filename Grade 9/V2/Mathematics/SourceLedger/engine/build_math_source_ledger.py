#!/usr/bin/env python3
"""Two-dimensional source completeness plus a post-layout rendered witness.

Three independent failures from the seven-topic stress test:

* Number Systems — completeness measured against the *supplied* question set is
  self-relative; an upstream omission cannot be detected by it.
* Polynomials — 72/72 top-level questions did not imply 151/151 atomic asks. A compound
  question can lose a subpart, a proof obligation or a parameter condition while its
  top-level count stays unchanged.
* Linear Equations — all four options were present in the JSON while C and D were covered
  by the next panel on the rendered page.

So this module freezes ``required_question_refs[]`` *and* ``required_atomic_ask_refs[]``
before authoring, reconciles the authored plan against both, and then verifies the
learner-visible objects actually survived layout — present, unclipped and unoccluded.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

PHASE = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = PHASE / "policies" / "math-source-completeness-policy.json"
DEFAULT_KIND_REGISTRY = PHASE / "registry" / "math-atomic-ask-kind-registry.json"

SHAPE_KEYS = ("subpart_count", "option_count", "proof_obligation_count",
              "parameter_condition_count")
KIND_TO_SHAPE_KEY = {
    "SUBPART": "subpart_count",
    "OPTION": "option_count",
    "PROOF_OBLIGATION": "proof_obligation_count",
    "PARAMETER_CONDITION": "parameter_condition_count",
}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict):
        item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()


def load(path: Path | str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


# --------------------------------------------------------------------------
# freezing the corpus
# --------------------------------------------------------------------------
def freeze_manifest(manifest: dict) -> dict:
    """Derive the two required-ref lists from the corpus and seal the manifest.

    Derivation is deliberate: the required lists are computed from the corpus rows rather
    than trusted as input, so a manifest cannot claim completeness it does not describe.
    """
    out = copy.deepcopy(manifest)
    out["required_question_refs"] = [q["question_ref"] for q in out["questions"]]
    out["required_atomic_ask_refs"] = [
        ask["atomic_ask_ref"] for q in out["questions"] for ask in q["atomic_asks"]
    ]
    out.pop("manifest_id", None)
    out.pop("manifest_digest", None)
    out["manifest_id"] = "MATH-SCM-" + digest(out)[:16]
    out["manifest_digest"] = digest(out, "manifest_digest")
    return out


def validate_manifest(manifest: dict, *, kinds: dict | None = None) -> list[str]:
    kinds = kinds if kinds is not None else load(DEFAULT_KIND_REGISTRY)
    failures: list[str] = []
    if manifest.get("frozen_at_stage") != "BEFORE_AUTHORING":
        failures.append("SOURCE_CORPUS_NOT_FROZEN_BEFORE_AUTHORING:"
                        f"{manifest.get('frozen_at_stage')}")
    if manifest["manifest_digest"] != digest(manifest, "manifest_digest"):
        failures.append(f"SOURCE_CORPUS_MANIFEST_DIGEST_DRIFT:{manifest['manifest_id']}")

    derived_questions = [q["question_ref"] for q in manifest["questions"]]
    if manifest["required_question_refs"] != derived_questions:
        failures.append("CORE2_SOURCE_CORPUS_COVERAGE_GAP:manifest_required_refs_drift")
    derived_asks = [a["atomic_ask_ref"] for q in manifest["questions"] for a in q["atomic_asks"]]
    if manifest["required_atomic_ask_refs"] != derived_asks:
        failures.append("CORE2_ATOMIC_ASK_COVERAGE_GAP:manifest_required_refs_drift")

    for question in manifest["questions"]:
        observed = shape_of(question["atomic_asks"])
        declared = {k: question["subpart_shape"][k] for k in SHAPE_KEYS}
        if observed != declared:
            failures.append(f"CORE2_SUBPART_SHAPE_DRIFT:{question['question_ref']}:manifest")
        for ask in question["atomic_asks"]:
            if ask["kind"] not in kinds["kinds"]:
                failures.append(f"CORE2_ATOMIC_ASK_COVERAGE_GAP:"
                                f"{ask['atomic_ask_ref']}:unknown_kind")
        if question["response_mode"] not in kinds["response_modes"]:
            failures.append(f"CORE2_SUBPART_SHAPE_DRIFT:{question['question_ref']}:"
                            "unknown_response_mode")
    return sorted(set(failures))


def shape_of(atomic_asks: Iterable[dict]) -> dict[str, int]:
    shape = {k: 0 for k in SHAPE_KEYS}
    for ask in atomic_asks:
        key = KIND_TO_SHAPE_KEY.get(ask["kind"])
        if key:
            shape[key] += 1
    return shape


# --------------------------------------------------------------------------
# reconciliation against the authored plan
# --------------------------------------------------------------------------
def _dimension(required: list[str], included: list[str]) -> dict:
    required_set, included_set = set(required), set(included)
    return {
        "required": len(required_set),
        "included": len(included_set & required_set),
        "missing": sorted(required_set - included_set),
        "extra": sorted(included_set - required_set),
    }


def reconcile(manifest: dict, authored: dict, *,
              object_map: dict | None = None, rendered_page_text: list[str] | None = None,
              policy: dict | None = None) -> dict:
    """Build the reconciliation ledger. Never raises; ``status`` carries the verdict.

    ``authored`` is the plan under audit:
        {"topic_ref", "pages": [{"question_ref", "atomic_ask_refs": [...],
          "subpart_shape": {...}, "concept_linked": bool, "core1_evidence_linked": bool,
          "solution_complete": bool, "verification_complete": bool}]}
    """
    policy = policy if policy is not None else load(DEFAULT_POLICY)

    authored_questions = [p["question_ref"] for p in authored["pages"]]
    authored_asks = [ref for p in authored["pages"] for ref in p["atomic_ask_refs"]]

    question_dimension = _dimension(manifest["required_question_refs"], authored_questions)
    ask_dimension = _dimension(manifest["required_atomic_ask_refs"], authored_asks)

    by_ref = {q["question_ref"]: q for q in manifest["questions"]}
    shape_dimension = []
    for page in authored["pages"]:
        expected_question = by_ref.get(page["question_ref"])
        if expected_question is None:
            continue
        expected = {k: expected_question["subpart_shape"][k] for k in SHAPE_KEYS}
        observed = {k: page["subpart_shape"][k] for k in SHAPE_KEYS}
        drift = [f"{k}:{expected[k]}->{observed[k]}" for k in SHAPE_KEYS
                 if expected[k] != observed[k]]
        shape_dimension.append({
            "question_ref": page["question_ref"],
            "expected": expected,
            "observed": observed,
            "drift": drift,
        })

    rendered = {"evaluated": False, "checked": 0, "visible": 0,
                "missing": [], "occluded": [], "clipped": []}
    if object_map is not None:
        rendered = rendered_coverage_witness(
            manifest, object_map, rendered_page_text=rendered_page_text, policy=policy)

    unresolved: list[str] = []
    unresolved += [f"MISSING_SOURCE_ROW:{r}" for r in question_dimension["missing"]]
    unresolved += [f"MISSING_ATOMIC_ASK:{r}" for r in ask_dimension["missing"]]
    unresolved += [f"SHAPE_DRIFT:{s['question_ref']}:{d}"
                   for s in shape_dimension for d in s["drift"]]
    unresolved += [f"NOT_RENDERED:{r}" for r in rendered["missing"]]
    unresolved += [f"OCCLUDED:{r}" for r in rendered["occluded"]]
    unresolved += [f"CLIPPED:{r}" for r in rendered["clipped"]]

    ledger = {
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "topic_ref": manifest["topic_ref"],
        "manifest_ref": manifest["manifest_id"],
        "manifest_digest": manifest["manifest_digest"],
        "question_dimension": question_dimension,
        "atomic_ask_dimension": ask_dimension,
        "shape_dimension": shape_dimension,
        "rendered_dimension": rendered,
        "reconciliation": {
            "required_source_rows": question_dimension["required"],
            "included_source_rows": question_dimension["included"],
            "required_atomic_asks": ask_dimension["required"],
            "included_atomic_asks": ask_dimension["included"],
            "concept_linked": sum(1 for p in authored["pages"] if p.get("concept_linked")),
            "core1_evidence_linked": sum(1 for p in authored["pages"]
                                         if p.get("core1_evidence_linked")),
            "solution_complete": sum(1 for p in authored["pages"]
                                     if p.get("solution_complete")),
            "verification_complete": sum(1 for p in authored["pages"]
                                         if p.get("verification_complete")),
            "render_visible": rendered["visible"],
            "unresolved": sorted(set(unresolved)),
        },
        "status": "PASS" if not unresolved else "BLOCKED",
        "release_meaning": "PUBLICATION_ENGINEERING only; subject/pedagogy/assessment/"
                           "visual/expert review PENDING",
    }
    ledger["ledger_id"] = "MATH-SRL-" + digest(ledger)[:16]
    ledger["ledger_digest"] = digest(ledger, "ledger_digest")
    return ledger


# --------------------------------------------------------------------------
# the post-layout witness
# --------------------------------------------------------------------------
def _overlap_area(a: dict, b: dict) -> float:
    dx = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
    dy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
    return dx * dy if dx > 0 and dy > 0 else 0.0


def rendered_coverage_witness(manifest: dict, object_map: dict, *,
                              rendered_page_text: list[str] | None = None,
                              policy: dict | None = None) -> dict:
    """Verify the learner-visible source objects survived layout.

    A pre-render JSON equality check cannot see occlusion or clipping, so this walks the
    object map in paint order and, when the actual page text is supplied, also confirms
    the object's text is extractable from the rendered page.
    """
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    threshold = float(policy["occlusion_policy"]["overlap_area_ratio_threshold"])
    tolerance = float(policy["clipping_policy"]["tolerance_pt"])
    margin = float(object_map["printable_margin_pt"])
    page_w = float(object_map["page_width_pt"])
    page_h = float(object_map["page_height_pt"])

    required_visible = {
        ask["atomic_ask_ref"]
        for question in manifest["questions"]
        for ask in question["atomic_asks"]
        if ask["learner_visible"]
    }
    ask_text = {
        ask["atomic_ask_ref"]: ask["text"]
        for question in manifest["questions"]
        for ask in question["atomic_asks"]
    }

    placed: dict[str, list[dict]] = {}
    for obj in object_map["objects"]:
        ref = obj.get("atomic_ask_ref")
        if ref:
            placed.setdefault(ref, []).append(obj)

    missing = sorted(required_visible - set(placed))
    occluded: set[str] = set()
    clipped: set[str] = set()

    by_page: dict[int, list[dict]] = {}
    for obj in object_map["objects"]:
        by_page.setdefault(obj["page"], []).append(obj)

    for page_objects in by_page.values():
        ordered = sorted(page_objects, key=lambda o: o["paint_order"])
        for index, obj in enumerate(ordered):
            box = obj["box"]
            ref = obj.get("atomic_ask_ref")
            if box["x"] < margin - tolerance or box["y"] < margin - tolerance or \
                    box["x"] + box["w"] > page_w - margin + tolerance or \
                    box["y"] + box["h"] > page_h - margin + tolerance:
                clipped.add(ref or obj["object_id"])
            if ref is None:
                continue
            area = box["w"] * box["h"]
            for later in ordered[index + 1:]:
                if not later["opaque"]:
                    continue
                if _overlap_area(box, later["box"]) / area > threshold:
                    occluded.add(ref)
                    break

    # the strongest layer: the text a learner must read has to be on the page
    text_missing: set[str] = set()
    if rendered_page_text is not None:
        # whitespace is normalised on both sides: a wrapped line break in the rendered page
        # is a layout detail, not a missing atomic ask
        blob = " ".join(" ".join(rendered_page_text).split())
        for ref in sorted(required_visible & set(placed)):
            expected = " ".join(str(ask_text.get(ref, "")).split())
            if expected and expected not in blob:
                text_missing.add(ref)

    missing = sorted(set(missing) | text_missing)
    visible = len(required_visible) - len(set(missing) | occluded | clipped)
    return {
        "evaluated": True,
        "checked": len(required_visible),
        "visible": max(visible, 0),
        "missing": missing,
        "occluded": sorted(occluded),
        "clipped": sorted(clipped),
    }


# --------------------------------------------------------------------------
# the fail-closed gate
# --------------------------------------------------------------------------
def audit_source_completeness(manifest: dict, authored: dict, *,
                              object_map: dict | None = None,
                              rendered_page_text: list[str] | None = None,
                              policy: dict | None = None,
                              kinds: dict | None = None) -> dict:
    policy = policy if policy is not None else load(DEFAULT_POLICY)
    failures = validate_manifest(manifest, kinds=kinds)

    ledger = reconcile(manifest, authored, object_map=object_map,
                       rendered_page_text=rendered_page_text, policy=policy)

    for ref in ledger["question_dimension"]["missing"]:
        failures.append(f"CORE2_SOURCE_CORPUS_COVERAGE_GAP:{ref}")
    for ref in ledger["atomic_ask_dimension"]["missing"]:
        failures.append(f"CORE2_ATOMIC_ASK_COVERAGE_GAP:{ref}")
    for entry in ledger["shape_dimension"]:
        for drift in entry["drift"]:
            failures.append(f"CORE2_SUBPART_SHAPE_DRIFT:{entry['question_ref']}:{drift}")
    rendered = ledger["rendered_dimension"]
    for ref in rendered["missing"]:
        failures.append(f"RENDERED_SOURCE_OPTION_COVERAGE_GAP:{ref}")
    for ref in rendered["occluded"]:
        failures.append(f"ASSESSMENT_OBJECT_OCCLUSION:{ref}")
    for ref in rendered["clipped"]:
        failures.append(f"ASSESSMENT_OBJECT_CLIPPED:{ref}")

    if failures:
        fail("SOURCE_LEDGER_GATE_FAILED", "|".join(sorted(set(failures))))
    return ledger
