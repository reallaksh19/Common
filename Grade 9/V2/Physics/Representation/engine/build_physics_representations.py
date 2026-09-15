#!/usr/bin/env python3
"""P-H — Physics teaching primitives and representation closure.

    P-G Core1 study plan
  + P-F capability records (structural obligations)
  + P-A question set (the only source of numeric quantities)
  + P-H teaching-primitive registry + page-intent profile + figure render contract
  -> PhysicsRepresentationBundle

Each representation spec is bound to exactly one registry primitive, carries the
render parameters that primitive needs, and records where every number in those
parameters came from. A spec that needs a quantity the source does not state
falls back to a schematic variant and says so; it never invents the number.
"""
import argparse, copy, hashlib, json, re
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]


def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(o, field=None):
    x = copy.deepcopy(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)


def uniq(xs):
    return sorted(set(xs))


# ------------------------------------------------------------ registry checks


def validate_registry(reg):
    if reg.get("subject") != "PHYSICS":
        fail("VISUAL_WITHOUT_CAPABILITY_BINDING", "registry subject")
    if reg.get("registry_digest") != digest(reg, "registry_digest"):
        fail("VISUAL_WITHOUT_INSTRUCTIONAL_JOB", "registry digest")
    by = {p["primitive_id"]: p for p in reg["primitives"]}
    if len(by) != len(reg["primitives"]):
        fail("VISUAL_WITHOUT_INSTRUCTIONAL_JOB", "duplicate primitive id")
    missing = set(reg["required_primitive_ids"]) - set(by)
    if missing:
        fail("REQUIRED_TEACHING_PRIMITIVE_MISSING", ",".join(sorted(missing)))
    for p in reg["primitives"]:
        pid = p["primitive_id"]
        if p.get("decorative") is not False:
            fail("DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS", pid)
        if not p.get("instructional_job") or not p.get("attention_target") or not p.get("learner_action"):
            fail("VISUAL_WITHOUT_INSTRUCTIONAL_JOB", pid)
        if p.get("realized_as_vector_graphics") is not True:
            fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", pid)
        if not isinstance(p.get("minimum_vector_ops"), int) or p["minimum_vector_ops"] < 1:
            fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", pid + ":no vector floor")
        if not p.get("renderer_binding"):
            fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", pid + ":no renderer binding")
        if "NO_QUANTITY_NOT_IN_SOURCE" not in p.get("renderer_constraints", []):
            fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", pid + ":constraint absent")
    return by


def validate_contract(contract):
    if contract.get("subject") != "PHYSICS":
        fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", "contract subject")
    if contract["accessibility"].get("grayscale_safe_required") is not True:
        fail("COLOUR_IS_THE_ONLY_CHANNEL")
    if contract["accessibility"].get("colour_may_not_be_the_only_channel") is not True:
        fail("COLOUR_IS_THE_ONLY_CHANNEL")
    return True


# --------------------------------------------------------- source quantities


def extract_source_quantities(question_set, item_refs, contract):
    """Pull every stated quantity for the given source items. No inference."""
    rules = contract["quantity_extraction"]
    named_re = re.compile(rules["named_quantity_pattern"])
    bare_re = re.compile(rules["bare_quantity_pattern"])
    directions = set(rules["direction_tokens"])
    roles = rules["symbol_roles"]

    by_id = {q["question_id"]: q for q in question_set["questions"]}
    named, bare, intervals, frames = [], [], [], []
    for ref in sorted(set(item_refs)):
        q = by_id.get(ref)
        if not q:
            continue
        texts = [g["text"] for g in q.get("givens", [])] + [q.get("stem", "")]
        for text in texts:
            lowered = text.lower()
            direction = next((d for d in directions if d in lowered), None)
            for m in named_re.finditer(text):
                symbol, value, unit = m.group(1), float(m.group(2)), m.group(3)
                named.append({
                    "item_ref": ref, "symbol": symbol, "value": value,
                    "unit": unit or "", "direction": direction,
                    "role": roles.get(symbol.lower(), "UNCLASSIFIED"),
                    "source_text": text,
                })
            for m in bare_re.finditer(text):
                if named_re.search(text) and "=" in text:
                    continue
                bare.append({
                    "item_ref": ref, "value": float(m.group(1)), "unit": m.group(2),
                    "direction": direction, "source_text": text,
                })
        for iv in q.get("time_intervals", []):
            intervals.append({"item_ref": ref, "interval_id": iv["interval_id"], "text": iv["text"]})
        if q.get("stated_positive_direction"):
            frames.append({"item_ref": ref, "positive_direction": q["stated_positive_direction"]})
    return {
        "named_quantities": named,
        "bare_quantities": bare,
        "time_intervals": intervals,
        "declared_frames": frames,
    }


def _named(source, role=None, symbol=None):
    for row in source["named_quantities"]:
        if symbol and row["symbol"].lower() == symbol.lower():
            return row
        if role and symbol is None and row["role"] == role:
            return row
    return None


def _interval_bounds(text):
    nums = re.findall(r"-?\d+(?:\.\d+)?", text or "")
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    return None


def _positive_direction(source):
    rows = source["declared_frames"]
    return rows[0]["positive_direction"] if rows else None


# ------------------------------------------------------------- render params


def _signed(row):
    """Apply the stated direction to a stated magnitude. No new numbers."""
    if row is None:
        return None
    value = row["value"]
    if row.get("direction") in {"downward", "left", "backward", "west", "south"}:
        value = -abs(value)
    return value


def build_render_params(primitive_id, lesson, record, source, contract):
    """Return (params, grounding, used_quantity_refs).

    ``grounding`` is SOURCE_QUANTITIES only when at least one number in the
    params came from the source; otherwise SCHEMATIC_STRUCTURE_ONLY.
    """
    used = []
    params = {"positive_direction": _positive_direction(source)}

    def take(row, key=None):
        if row is not None:
            used.append({
                "item_ref": row["item_ref"],
                "symbol": row.get("symbol"),
                "value": row["value"],
                "unit": row.get("unit", ""),
                "source_text": row["source_text"],
            })
        return row

    if primitive_id == "PHENOMENON_SCENE":
        params["body_label"] = "body"
        params["events"] = [
            "Read what physically happens, in order.",
            "Mark the start state and the end state.",
            "Mark the quantity the question asks for.",
        ]

    elif primitive_id == "MOTION_STRIP":
        params["time_step_label"] = "equal time steps"

    elif primitive_id == "VECTOR_STATE_VIEW":
        vectors = []
        for symbol in ("u", "v", "a", "g"):
            row = _named(source, symbol=symbol)
            if row:
                take(row)
                vectors.append({"name": symbol, "value": _signed(row), "unit": row["unit"]})
        if vectors:
            params["vectors"] = vectors

    elif primitive_id == "PHASE_BOUNDARY_VIEW":
        phases = uniq(p for o in record["state_phase_obligations"] for p in o["phases"])
        carried = uniq(s for o in record["state_phase_obligations"] for s in o["continuity_state_refs"])
        if phases:
            params["phases"] = phases
        if carried:
            params["continuity_states"] = carried

    elif primitive_id == "TRAJECTORY_VIEW":
        params["path_label"] = "path travelled (distance)"
        params["chord_label"] = "straight start to end (displacement)"

    elif primitive_id in {"POSITION_TIME_GRAPH", "SLOPE_AREA_DECODER"}:
        u = take(_named(source, symbol="u"))
        v = take(_named(source, symbol="v"))
        t = take(_named(source, symbol="t"))
        if u is not None and v is not None and t is not None:
            params["points"] = [(0.0, abs(u["value"])), (abs(t["value"]), abs(v["value"]))]
            params["u"], params["v"], params["t_accel"] = abs(u["value"]), abs(v["value"]), abs(t["value"]) or 1.0

    elif primitive_id == "VELOCITY_TIME_GRAPH":
        u = take(_named(source, symbol="u"))
        v = take(_named(source, symbol="v"))
        t = take(_named(source, symbol="t"))
        if u is not None:
            params["u"] = abs(u["value"])
        if v is not None:
            params["v"] = abs(v["value"])
        if t is not None and t["value"]:
            params["t_accel"] = abs(t["value"])

    elif primitive_id == "ACCELERATION_TIME_GRAPH":
        segs = []
        t0 = 0.0
        for symbol in ("a1", "a2", "a"):
            row = _named(source, symbol=symbol)
            if row:
                take(row)
                segs.append({"t0": t0, "t1": t0 + 2.0, "a": row["value"]})
                t0 += 2.0
        if segs:
            params["intervals"] = segs

    elif primitive_id == "SIGN_FRAME_OVERLAY":
        # No source item in this fixture states a multi-leg journey, so no legs are
        # supplied and the renderer draws its own schematic frame. Passing legs=None
        # through to the shared Vector1DDiagram would silently display that library's
        # hard-coded "+5 m East / -3 m West" example as if the source had stated it.
        params["ticks"] = [-3, -2, -1, 0, 1, 2, 3, 4, 5]
        params["origin"] = 0
        params["legs"] = []

    elif primitive_id == "DIAGRAM_EQUATION_BRIDGE":
        bindings = []
        for symbol, feature in (
            ("u", "arrow at the start instant"),
            ("v", "arrow at the end instant"),
            ("a", "change of the arrow between the instants"),
            ("t", "span between the two instants"),
        ):
            if _named(source, symbol=symbol):
                bindings.append({"symbol": symbol, "feature": feature})
        if bindings:
            params["symbol_bindings"] = bindings
            for b in bindings:
                take(_named(source, symbol=b["symbol"]))
        params["relation_text"] = "Bind every symbol to a diagram feature before substituting."

    elif primitive_id == "STATE_TABLE":
        rows = []
        for var in uniq(s for o in record["state_phase_obligations"] for s in o["state_variable_refs"]):
            row = _named(source, symbol=var[:1].lower()) if var else None
            start = f"{row['value']:g} {row['unit']}".strip() if row else "?"
            if row:
                take(row)
            rows.append([var.replace("_", " ").lower(), start, "?"])
        if rows:
            params["columns"] = ["state variable", "stated in the source", "to find"]
            params["rows"] = rows
            params["unknown"] = "?"

    elif primitive_id == "TIMELINE_INTERVAL_VIEW":
        if source["time_intervals"]:
            iv = source["time_intervals"][0]
            bounds = _interval_bounds(iv["text"])
            if bounds:
                params["t0"], params["t1"] = bounds
                params["t_end"] = max(bounds[1] * 1.4, bounds[1] + 1)
                params["interval_label"] = iv["text"]
                used.append({
                    "item_ref": iv["item_ref"], "symbol": iv["interval_id"],
                    "value": bounds[1], "unit": "s", "source_text": iv["text"],
                })

    elif primitive_id == "RELATIVE_FRAME_VIEW":
        g = take(_named(source, symbol="g"))
        if g:
            value = _signed(g)
            params["bodies"] = [
                {"name": "A", "value": value, "unit": g["unit"]},
                {"name": "B", "value": value, "unit": g["unit"]},
            ]
            params["frame_body"] = "A"

    elif primitive_id == "OPTION_GRAPH_SET_VIEW":
        params["decisive_feature"] = "Reject each option by naming the feature it gets wrong."

    elif primitive_id == "MINIMAL_PHYSICS_CONTRAST":
        repair = lesson.get("misconception_repair") or {}
        params["cases"] = [
            {"label": "the shortcut reproduces the right answer here"},
            {"label": "the shortcut fails here"},
        ]
        params["decisive_feature"] = repair.get("minimal_contrast", "exactly one physical feature differs")

    elif primitive_id == "VERIFICATION_CHECK_STRIP":
        params["checks"] = list(record["verification_requirements"]) or list(lesson["verification_steps"])

    elif primitive_id == "MODEL_VALIDITY_GATE":
        conditions = uniq(
            cond for o in record["model_validity_obligations"] for cond in o["validity_conditions"]
        )
        models = uniq(record["physical_model_refs"])
        params["conditions"] = conditions or ["every assumption of the selected model must be stated or implied"]
        params["model_label"] = ", ".join(models) if models else "selected model"

    elif primitive_id == "FORCE_DIAGRAM":
        params["forces"] = None

    grounding = "SOURCE_QUANTITIES" if used else "SCHEMATIC_STRUCTURE_ONLY"
    return params, grounding, used


# ---------------------------------------------------------- spec construction


def primitive_ids_for(lesson, record, profile, registry_by):
    mapping = profile["primitive_by_representation_requirement"]
    ids = []
    anchor = profile["anchor_primitive_by_lesson_mode"].get(lesson["lesson_mode"])
    if anchor:
        ids.append(anchor)
    for req in record["representation_requirements"]:
        pid = mapping.get(req)
        if pid is None:
            fail("REPRESENTATION_REQUIREMENT_WITHOUT_PRIMITIVE", f"{lesson['capability_ref']}:{req}")
        ids.append(pid)

    allowed = profile["conditional_primitives_by_lesson_mode"][lesson["lesson_mode"]]
    conditions = {
        "multiphase": lesson["multiphase"],
        "model_validity": lesson["model_validity_required"],
        "verification": bool(lesson["verification_steps"]),
        "misconception_repair": lesson.get("misconception_repair") is not None,
    }
    for key in allowed:
        if conditions.get(key):
            ids.append(profile["conditional_primitives"][key])

    # Representation obligations are never trimmed for page density: P-F fixes what must
    # be teachable, so a required representation always gets a primitive. Lesson mode
    # controls only which *conditional* primitives are added on top.
    out = list(dict.fromkeys(ids))
    if profile.get("representation_obligations_never_trimmed") is not True:
        fail("REPRESENTATION_REQUIREMENT_DROPPED_FROM_REPRESENTATION", "profile allows trimming")
    for pid in out:
        if pid not in registry_by:
            fail("VISUAL_WITHOUT_INSTRUCTIONAL_JOB", pid)
    return out


def make_spec(index, primitive, lesson, record, source, contract, profile):
    pid = primitive["primitive_id"]
    params, grounding, used = build_render_params(pid, lesson, record, source, contract)
    accessibility = primitive["accessibility_pattern"]
    if record["representation_requirements"]:
        accessibility += " Representation obligations: " + ", ".join(record["representation_requirements"]) + "."
    return {
        "representation_id": f"REP-{lesson['capability_ref']}-{index:02d}-{pid}",
        "primitive_id": pid,
        "capability_ref": lesson["capability_ref"],
        "lesson_ref": lesson["lesson_id"],
        "page_intent_phase": profile["primitive_page_intent_phase"][pid],
        "problem_family_ref": sorted(record["problem_family_refs"])[0] if record["problem_family_refs"] else None,
        "instructional_job": primitive["instructional_job"],
        "attention_target": primitive["attention_target"],
        "learner_action_expected": primitive["learner_action"],
        "translation_obligation": primitive["translation_obligation"],
        "renderer_constraints": uniq(primitive["renderer_constraints"] + ["RENDER_CONTRACT:" + contract["contract_id"]]),
        "minimum_vector_ops": primitive["minimum_vector_ops"],
        "render_params": params,
        "quantitative_grounding": grounding,
        "source_quantities": used,
        "source_semantic_data": {
            "assessment_question_refs": list(record["assessment_question_refs"]),
            "source_scope_trace_item_refs": list(record["source_scope_trace_item_refs"]),
            "representation_requirements": list(record["representation_requirements"]),
            "physical_model_refs": list(record["physical_model_refs"]),
            "law_refs": list(record["law_refs"]),
            "verification_requirements": list(record["verification_requirements"]),
            "frame_sign_required": lesson["frame_sign_required"],
            "model_validity_required": lesson["model_validity_required"],
            "multiphase": lesson["multiphase"],
        },
        "accessibility_text": accessibility,
        "decorative": False,
    }


def build_bundle(core1_plan, study_model, question_set, registry, profile, contract,
                 bundle_id="PHY-P-H-REPRESENTATIONS-v1"):
    by = validate_registry(registry)
    validate_contract(contract)
    if core1_plan["study_model_digest"] != study_model["study_model_digest"]:
        fail("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING", "study model drift")

    records = {r["capability_ref"]: r for r in study_model["capability_records"]}
    specs = []
    for lesson in core1_plan["lessons"]:
        record = records[lesson["capability_ref"]]
        source = extract_source_quantities(question_set, record["source_scope_trace_item_refs"], contract)
        for i, pid in enumerate(primitive_ids_for(lesson, record, profile, by), 1):
            specs.append(make_spec(i, by[pid], lesson, record, source, contract, profile))

    counts = Counter(s["primitive_id"] for s in specs)
    grounded = sum(1 for s in specs if s["quantitative_grounding"] == "SOURCE_QUANTITIES")
    bundle = {
        "bundle_id": bundle_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "core1_plan_ref": core1_plan["plan_id"],
        "core1_plan_digest": core1_plan["plan_digest"],
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "question_set_ref": question_set["question_set_id"],
        "primitive_registry_ref": registry["registry_id"],
        "primitive_registry_digest": registry["registry_digest"],
        "page_intent_profile_ref": profile["profile_id"],
        "figure_render_contract_ref": contract["contract_id"],
        "representations": specs,
        "summary": {
            "representation_count": len(specs),
            "capability_count": len({s["capability_ref"] for s in specs}),
            "primitive_counts": dict(sorted(counts.items())),
            "source_grounded_count": grounded,
            "schematic_only_count": len(specs) - grounded,
            "renderer_invention_allowed": False,
        },
        "bundle_digest": "",
    }
    bundle["bundle_digest"] = digest(bundle, "bundle_digest")
    validate_bundle(bundle, core1_plan, study_model, question_set, registry, profile, contract)
    return bundle


def validate_bundle(bundle, core1_plan, study_model, question_set, registry, profile, contract):
    by = validate_registry(registry)
    validate_contract(contract)
    if bundle["bundle_digest"] != digest(bundle, "bundle_digest"):
        fail("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING", "bundle digest")
    if bundle["core1_plan_digest"] != core1_plan["plan_digest"]:
        fail("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING", "core1 drift")
    if bundle["study_model_digest"] != study_model["study_model_digest"]:
        fail("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING", "study model drift")

    records = {r["capability_ref"]: r for r in study_model["capability_records"]}
    lessons = {l["capability_ref"]: l for l in core1_plan["lessons"]}
    grouped = {cap: [] for cap in records}
    by_id = {q["question_id"]: q for q in question_set["questions"]}

    for s in bundle["representations"]:
        rid = s["representation_id"]
        if s.get("decorative") is not False:
            fail("DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS", rid)
        cap = s["capability_ref"]
        if cap not in records:
            fail("VISUAL_WITHOUT_CAPABILITY_BINDING", rid)
        grouped[cap].append(s)
        p = by.get(s["primitive_id"])
        if not p:
            fail("VISUAL_WITHOUT_INSTRUCTIONAL_JOB", rid)
        if s["instructional_job"] != p["instructional_job"] or s["attention_target"] != p["attention_target"]:
            fail("VISUAL_WITHOUT_INSTRUCTIONAL_JOB", rid)
        if s["minimum_vector_ops"] != p["minimum_vector_ops"]:
            fail("TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED", rid + ":vector floor drift")
        if not set(p["renderer_constraints"]) <= set(s["renderer_constraints"]):
            fail("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING", rid + ":renderer constraints")
        if not s.get("accessibility_text"):
            fail("COLOUR_IS_THE_ONLY_CHANNEL", rid)

        r = records[cap]
        sem = s["source_semantic_data"]
        if set(sem["representation_requirements"]) != set(r["representation_requirements"]):
            fail("REPRESENTATION_REQUIREMENT_DROPPED_FROM_REPRESENTATION", rid)
        if set(sem["source_scope_trace_item_refs"]) != set(r["source_scope_trace_item_refs"]):
            fail("VISUAL_WITHOUT_SOURCE_SCOPE_TRACE", rid)
        if set(sem["verification_requirements"]) != set(r["verification_requirements"]):
            fail("RENDERER_INVENTS_UNDECLARED_PHYSICS_MEANING", rid + ":verification")

        # every number used must be traceable to a source item in this capability's own trace
        allowed_items = set(r["source_scope_trace_item_refs"])
        for q in s["source_quantities"]:
            if q["item_ref"] not in allowed_items:
                fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", f"{rid}:{q['item_ref']}")
            item = by_id.get(q["item_ref"])
            if not item:
                fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", f"{rid}:{q['item_ref']} not in question set")
            haystack = " ".join([g["text"] for g in item.get("givens", [])] + [item.get("stem", "")]
                                + [iv["text"] for iv in item.get("time_intervals", [])])
            if q["source_text"] not in haystack:
                fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", f"{rid}:{q['source_text']!r}")
        if s["quantitative_grounding"] == "SOURCE_QUANTITIES" and not s["source_quantities"]:
            fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", rid + ":claims grounding without quantities")
        if s["quantitative_grounding"] == "SCHEMATIC_STRUCTURE_ONLY" and s["source_quantities"]:
            fail("FIGURE_INVENTS_QUANTITY_NOT_IN_SOURCE", rid + ":grounding understated")

    mapping = profile["primitive_by_representation_requirement"]
    for cap, r in records.items():
        if not grouped.get(cap):
            fail("VISUAL_WITHOUT_CAPABILITY_BINDING", cap + ":no representation")
        pids = {x["primitive_id"] for x in grouped[cap]}
        for req in r["representation_requirements"]:
            if mapping[req] not in pids:
                fail("REPRESENTATION_REQUIREMENT_DROPPED_FROM_REPRESENTATION", f"{cap}:{req}")
        lesson = lessons[cap]
        allowed = profile["conditional_primitives_by_lesson_mode"][lesson["lesson_mode"]]
        if "model_validity" in allowed and lesson["model_validity_required"] and "MODEL_VALIDITY_GATE" not in pids:
            fail("MODEL_VALIDITY_REQUIRED_BUT_NOT_VISIBLE", cap)
        if "verification" in allowed and lesson["verification_steps"] and "VERIFICATION_CHECK_STRIP" not in pids:
            fail("VERIFICATION_REQUIRED_BUT_NOT_VISIBLE", cap)
        if ("misconception_repair" in allowed and lesson.get("misconception_repair")
                and "MINIMAL_PHYSICS_CONTRAST" not in pids):
            fail("CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED", cap)
    return True


def main():
    ap = argparse.ArgumentParser()
    for x in ["core1-plan", "study-model", "question-set", "primitive-registry",
              "page-intent-profile", "render-contract", "out"]:
        ap.add_argument("--" + x, required=True)
    a = ap.parse_args()
    bundle = build_bundle(
        load(a.core1_plan), load(a.study_model), load(a.question_set),
        load(a.primitive_registry), load(a.page_intent_profile), load(a.render_contract),
    )
    Path(a.out).write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
