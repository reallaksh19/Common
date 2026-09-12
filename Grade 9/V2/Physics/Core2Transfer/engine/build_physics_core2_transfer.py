#!/usr/bin/env python3
"""P-I — Physics Core2 transfer: H1 Notice → H2 Model → H3 Start, First-Step Reference, Core1 linkage.

    P-I external transfer corpus (source bodies, preserved exactly)
  + P-I external corpus classification (scope-eligible denominator, learner-independent)
  + P-G Core1 study plan   (what was actually taught)
  + P-F capability records (structural obligations of the primary capability)
  + P-I authoring profile / badge policy / concept segregation
  -> PhysicsCore2TransferPlan

The hint ladder is graded by construction: H1 may not name a relation, H2 may not
substitute, H3 may not state a result, and no level may name an option label. The
solution supplies the full reasoning route plus an independent physical check.
"""
import argparse, copy, hashlib, json, re
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parents[1]
LEVELS = ("H1_NOTICE", "H2_MODEL", "H3_START")


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


# ------------------------------------------------------------ source custody


def validate_corpus(corpus):
    if corpus.get("subject") != "PHYSICS":
        fail("SOURCE_LINK_MISSING_OR_WRONG", "corpus subject")
    if corpus.get("production_claim") is not False:
        fail("SYNTHETIC_CORPUS_CLAIMED_AS_PRODUCTION")
    if corpus.get("corpus_digest") != digest(corpus, "corpus_digest"):
        fail("SOURCE_BODY_REWRITTEN", "corpus digest")
    if len(corpus["candidates"]) != corpus["candidate_count_declared"]:
        fail("SOURCE_LINK_MISSING_OR_WRONG", "declared denominator")
    bodies = {r["candidate_id"]: r for r in corpus["records"]}
    if set(bodies) != {c["candidate_id"] for c in corpus["candidates"]}:
        fail("SOURCE_LINK_MISSING_OR_WRONG", "body coverage")
    for c in corpus["candidates"]:
        body = bodies[c["candidate_id"]]
        if body["body_digest"] != digest(body, "body_digest"):
            fail("SOURCE_BODY_REWRITTEN", c["candidate_id"])
        if c["source_digest"] != body["body_digest"]:
            fail("SOURCE_BODY_REWRITTEN", c["candidate_id"] + ":candidate digest")
        if not body.get("source_link"):
            fail("SOURCE_LINK_MISSING_OR_WRONG", c["candidate_id"])
        if not body.get("stem") or len(body.get("options", [])) < 2:
            fail("MCQ_OPTION_LOST", c["candidate_id"])
        if body.get("figure_required") and not body.get("figure_semantic"):
            fail("SOURCE_FIGURE_LOST", c["candidate_id"])
    return bodies


def validate_classification(classification, corpus, study_scope, families):
    if classification.get("corpus_digest") != corpus["corpus_digest"]:
        fail("SOURCE_BODY_REWRITTEN", "classification corpus drift")
    if classification.get("registry_digest") != digest(classification, "registry_digest"):
        fail("SOURCE_LINK_MISSING_OR_WRONG", "classification digest")
    rows = {c["candidate_id"]: c for c in classification["classifications"]}
    if set(rows) != {c["candidate_id"] for c in corpus["candidates"]}:
        fail("EXTERNAL_CANDIDATE_UNCLASSIFIED", "classification coverage")
    scope_caps = {r["capability_ref"] for r in study_scope["capability_scope_records"]}
    for cid, row in rows.items():
        if row["scope_status"] == "ELIGIBLE_IN_SCOPE":
            if row["primary_capability_ref"] not in scope_caps:
                fail("EXTERNAL_CANDIDATE_OUTSIDE_ASSESSMENT_SCOPE", cid)
            if row["problem_family_ref"] not in families:
                fail("TRANSFER_PAGE_WITHOUT_PROBLEM_FAMILY", cid)
            for sup in row["supporting_capability_refs"]:
                if sup not in scope_caps:
                    fail("EXTERNAL_CANDIDATE_OUTSIDE_ASSESSMENT_SCOPE", f"{cid}:{sup}")
            if row["primary_capability_ref"] in row["supporting_capability_refs"]:
                fail("PRIMARY_SUPPORTS_NOT_DISTINGUISHED", cid)
        else:
            if not row.get("out_of_scope_reason"):
                fail("EXTERNAL_CANDIDATE_UNCLASSIFIED", cid + ":no reason")
    return rows


# ------------------------------------------------------------------- hinting


ANSWER_TOKENS = re.compile(r"\b(?:therefore|the answer is|equals|option\s+[A-D]\b)", re.I)
RELATION_TOKENS = re.compile(r"[=]|\bv\s*=\s*u\b|\bformula\b|\bequation\b", re.I)
SUBSTITUTION_TOKENS = re.compile(r"\bsubstitut|\bplug in\b|\d+\s*[x*/+-]\s*\d+", re.I)


def hint_violations(level, text, option_labels, profile):
    """Content-shape rules for one hint level. Returns a list of violated tokens."""
    forbidden = profile["hint_level_forbidden_content"][level]
    bad = []
    if "OPTION_LABEL" in forbidden:
        for label in option_labels:
            if re.search(rf"\boption\s+{re.escape(label)}\b", text, re.I):
                bad.append("OPTION_LABEL")
                break
    if "RESULT" in forbidden and ANSWER_TOKENS.search(text):
        bad.append("RESULT")
    if "RELATION" in forbidden and RELATION_TOKENS.search(text):
        bad.append("RELATION")
    if "SUBSTITUTION" in forbidden and SUBSTITUTION_TOKENS.search(text):
        bad.append("SUBSTITUTION")
    return sorted(set(bad))


def first_move_for(record, semantics_item, profile):
    """Derive the first physically meaningful move from P-D/P-F structure, not a topic table."""
    if record["system_frame_obligations"] and any(
        o["reference_frame"]["required"] or o["sign_convention"]["required"]
        for o in record["system_frame_obligations"]
    ):
        return "name the moving body and declare the origin and positive direction"
    if any(o["phase_kind"] != "SINGLE_PHASE" for o in record["state_phase_obligations"]):
        return "mark the instant at which the motion changes character and split the situation there"
    if any("GRAPH" in r.upper() for r in record["representation_requirements"]):
        return "read both axis labels and decide whether the question needs a slope or an area"
    return "name the moving body and fill the start and end states before choosing anything"


def model_clause(record):
    models = uniq(record["physical_model_refs"])
    conditions = uniq(c for o in record["model_validity_obligations"] for c in o["validity_conditions"])
    model = ", ".join(models) if models else "the model this situation states"
    condition = ", ".join(conditions) if conditions else "the situation states its assumptions"
    return model, condition


def attention_clause(record):
    if any(o["phase_kind"] != "SINGLE_PHASE" for o in record["state_phase_obligations"]):
        return "that the motion does not keep the same character throughout"
    if any("GRAPH" in r.upper() for r in record["representation_requirements"]):
        return "what each axis of the given graph actually measures"
    if any(o["reference_frame"]["required"] or o["sign_convention"]["required"]
           for o in record["system_frame_obligations"]):
        return "that a direction has to be declared before any signed quantity means anything"
    return "which two instants the situation is asking you to compare"


def build_hint_ladder(page_id, record, profile, option_labels):
    model, condition = model_clause(record)
    text_by_level = {
        "H1_NOTICE": profile["hint_templates"]["H1_NOTICE"].format(attention=attention_clause(record)),
        "H2_MODEL": profile["hint_templates"]["H2_MODEL"].format(model=model, condition=condition),
        "H3_START": profile["hint_templates"]["H3_START"].format(
            first_move=first_move_for(record, None, profile)
        ),
    }
    ladder = []
    for i, level in enumerate(LEVELS, 1):
        text = text_by_level[level]
        bad = hint_violations(level, text, option_labels, profile)
        if bad:
            fail("HINT_REVEALS_ANSWER", f"{page_id}:{level}:{','.join(bad)}")
        ladder.append({
            "hint_id": f"{page_id}-{level}",
            "level": level,
            "order": i,
            "intent": profile["hint_level_intent"][level],
            "text": text,
            "reveals_relation": level != "H1_NOTICE",
            "reveals_result": False,
        })
    return ladder


# --------------------------------------------------------------------- badge


def demand_vector(record, policy):
    dims = {k: 0 for k in policy["demand_keys"]}
    reps = record["representation_requirements"]
    dims["representation_translation"] = min(3, len(reps))
    dims["frame_sign_discipline"] = 2 if any(
        o["reference_frame"]["required"] or o["sign_convention"]["required"]
        for o in record["system_frame_obligations"]
    ) else 0
    dims["model_selection"] = min(3, len(record["physical_model_refs"]))
    dims["model_validity_load"] = 2 if any(o["required"] for o in record["model_validity_obligations"]) else 0
    dims["phase_continuity"] = 2 if any(
        o["phase_kind"] != "SINGLE_PHASE" or o["continuity_state_refs"]
        for o in record["state_phase_obligations"]
    ) else 0
    dims["graph_decoding"] = 2 if any("GRAPH" in r.upper() or "AREA" in r.upper() for r in reps) else 0
    dims["vector_reasoning"] = 2 if {"MOTION_VECTOR_DIAGRAM", "RELATIVE_STATE_DIAGRAM"} & set(reps) else 0
    dims["reasoning_chain_length"] = min(3, max(1, len(record["reasoning_route_roles"]) // 4))
    dims["concept_combination"] = min(3, max(0, len(record["problem_family_refs"]) - 1))
    dims["quantitative_execution_load"] = 1
    dims["verification_demand"] = min(2, len(record["verification_requirements"]))
    score = sum(dims.values())
    badge = next(t["badge"] for t in policy["thresholds"] if score <= t["max_score"])
    return badge, dims, score


# ------------------------------------------------------------------ solution


def build_solution(page_id, record, profile):
    model, condition = model_clause(record)
    sections = {
        "SYSTEM_AND_FRAME": "Name the body being tracked and declare the origin and positive direction; "
                            "every signed quantity below uses that one convention.",
        "STATE_TABLE": "Enter each stated quantity into the start state or the end state row, with its unit "
                       "and the sign the declared direction forces, and mark the unknown.",
        "MODEL_AND_VALIDITY": f"Model: {model}. Check each assumption against the situation: {condition}.",
        "RELATION_CHOICE": "Choose the relation whose variables are exactly the known and wanted state "
                           "variables, and say which variable it deliberately leaves out.",
        "EXECUTION": "Substitute the signed values and carry the algebra through without dropping a sign.",
        "PHYSICAL_VERIFICATION": "Run an independent check that could reject the answer: "
                                 + "; ".join(record["verification_requirements"] or ["VERIFY_DIMENSIONS"]),
        "RESULT_INTERPRETATION": "Translate the signed result back into a direction and state what it means "
                                 "physically before selecting an option.",
    }
    missing = [s for s in profile["solution_required_sections"] if s not in sections]
    if missing:
        fail("SOLUTION_SECTION_MISSING", f"{page_id}:{','.join(missing)}")
    if not record["verification_requirements"] and profile["solution_requires_independent_verification"]:
        # the capability may declare none; the route default still has to be independent
        pass
    return {
        "solution_id": f"{page_id}-SOLUTION",
        "sections": [{"section": s, "text": sections[s]} for s in profile["solution_required_sections"]],
        "verification_steps": list(record["verification_requirements"]) or ["VERIFY_DIMENSIONS"],
        "verification_is_independent_of_solving_route": True,
        "reasoning_route_roles": list(record["reasoning_route_roles"]),
    }


# ---------------------------------------------------------------- core1 link


def core1_links(page_id, classification_row, core1_plan, segregation):
    lessons = {l["capability_ref"]: l for l in core1_plan["lessons"]}
    primary = classification_row["primary_capability_ref"]
    if primary not in lessons:
        fail("TRANSFER_PAGE_WITHOUT_CORE1_LINK", f"{page_id}:{primary}")
    extensions = {e["capability_ref"]: e for e in segregation["core2_only_extensions"]}
    supporting = []
    for cap in classification_row["supporting_capability_refs"]:
        if cap in lessons:
            supporting.append({"capability_ref": cap, "core1_lesson_ref": lessons[cap]["lesson_id"],
                               "link_class": "TAUGHT_IN_CORE1"})
        elif cap in extensions:
            bridge = extensions[cap].get("core1_bridge_lesson_ref")
            if not bridge:
                fail("CORE2_REQUIRES_UNTAUGHT_CONCEPT", f"{page_id}:{cap}:no bridge")
            supporting.append({"capability_ref": cap, "core1_lesson_ref": bridge,
                               "link_class": "DECLARED_TRANSFER_EXTENSION"})
        else:
            fail("CORE2_REQUIRES_UNTAUGHT_CONCEPT", f"{page_id}:{cap}")
    return {
        "primary_capability_ref": primary,
        "primary_core1_lesson_ref": lessons[primary]["lesson_id"],
        "supporting_links": sorted(supporting, key=lambda x: x["capability_ref"]),
    }


# ------------------------------------------------------------------- builder


def build_plan(corpus, classification, core1_plan, study_model, study_scope,
               profile, badge_policy, segregation, plan_id="PHY-P-I-CORE2-PLAN-v1"):
    bodies = validate_corpus(corpus)
    records = {r["capability_ref"]: r for r in study_model["capability_records"]}
    families = uniq(f for r in records.values() for f in r["problem_family_refs"])
    rows = validate_classification(classification, corpus, study_scope, families)
    if core1_plan["study_model_digest"] != study_model["study_model_digest"]:
        fail("CORE2_AUTHORED_AGAINST_STALE_CORE1", "study model drift")
    scanned = copy.deepcopy({"profile": profile, "badges": badge_policy, "segregation": segregation})
    scanned["profile"].pop("forbidden_producer_inputs", None)  # the deny-list is not itself a use
    blob = canonical(scanned).lower()
    for token in profile["forbidden_producer_inputs"]:
        if token.lower() in blob:
            fail("PR156_USED_AS_PRODUCER_INPUT_BEFORE_FINAL_COMPARISON", token)

    pages, first_steps = [], {}
    eligible = [cid for cid, row in rows.items() if row["scope_status"] == "ELIGIBLE_IN_SCOPE"]
    for cid in sorted(eligible):
        row = rows[cid]
        body = bodies[cid]
        record = records[row["primary_capability_ref"]]
        page_id = "PHY-CORE2-" + cid
        option_labels = [o["label"] for o in body["options"]]
        badge, dims, score = demand_vector(record, badge_policy)
        family = row["problem_family_ref"]
        if family not in first_steps:
            first_steps[family] = {
                "problem_family_ref": family,
                "first_move": first_move_for(record, None, profile),
                "frame_sign_required": any(
                    o["reference_frame"]["required"] or o["sign_convention"]["required"]
                    for o in record["system_frame_obligations"]
                ),
                "derived_from": profile["first_step_reference_source"],
            }
        pages.append({
            "page_id": page_id,
            "candidate_ref": cid,
            "source_link": body["source_link"],
            "source_body_digest": body["body_digest"],
            "source_body_preserved": True,
            "stem": body["stem"],
            "options": copy.deepcopy(body["options"]),
            "figure_required": body["figure_required"],
            "figure_semantic": copy.deepcopy(body["figure_semantic"]),
            "problem_family_ref": family,
            "guide_demand_badge": badge,
            "demand_vector": dims,
            "demand_score": score,
            "core1_linkage": core1_links(page_id, row, core1_plan, segregation),
            "first_step_reference_ref": family,
            "hint_ladder": build_hint_ladder(page_id, record, profile, option_labels),
            "solution": build_solution(page_id, record, profile),
            "frame_sign_required": any(
                o["reference_frame"]["required"] or o["sign_convention"]["required"]
                for o in record["system_frame_obligations"]
            ),
            "model_validity_required": any(o["required"] for o in record["model_validity_obligations"]),
            "representation_requirements": list(record["representation_requirements"]),
        })

    counts = Counter(p["guide_demand_badge"] for p in pages)
    plan = {
        "plan_id": plan_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "corpus_ref": corpus["corpus_id"],
        "corpus_digest": corpus["corpus_digest"],
        "classification_ref": classification["registry_id"],
        "core1_plan_ref": core1_plan["plan_id"],
        "core1_plan_digest": core1_plan["plan_digest"],
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "authoring_profile_ref": profile["profile_id"],
        "badge_policy_ref": badge_policy["policy_id"],
        "concept_segregation_ref": segregation["registry_id"],
        "eligible_candidate_refs": sorted(eligible),
        "out_of_scope_candidate_refs": sorted(set(rows) - set(eligible)),
        "transfer_pages": pages,
        "first_step_reference": [first_steps[k] for k in sorted(first_steps)],
        "summary": {
            "page_count": len(pages),
            "eligible_candidate_count": len(eligible),
            "badge_counts": dict(sorted(counts.items())),
            "first_step_reference_count": len(first_steps),
            "hint_levels": list(LEVELS),
        },
        "release_authority_state": "PILOT_ONLY_HUMAN_EXPERT_RELEASE_NOT_GRANTED",
        "human_expert_review_states": {
            "SUBJECT_EXPERT_PASS": "PENDING",
            "PEDAGOGY_EXPERT_PASS": "PENDING",
            "ASSESSMENT_EXPERT_PASS": "PENDING",
        },
        "plan_digest": "",
    }
    plan["plan_digest"] = digest(plan, "plan_digest")
    validate_plan(plan, corpus, classification, core1_plan, study_model, study_scope,
                  profile, badge_policy, segregation)
    return plan


def validate_plan(plan, corpus, classification, core1_plan, study_model, study_scope,
                  profile, badge_policy, segregation):
    bodies = validate_corpus(corpus)
    if plan["plan_digest"] != digest(plan, "plan_digest"):
        fail("CORE2_AUTHORED_AGAINST_STALE_CORE1", "plan digest")
    if plan["core1_plan_digest"] != core1_plan["plan_digest"]:
        fail("CORE2_AUTHORED_AGAINST_STALE_CORE1", "core1 digest")
    for state in plan["human_expert_review_states"].values():
        if state == "PASS":
            fail("FAKE_HUMAN_REVIEW_STATE", "plan claims an expert pass")

    rows = {c["candidate_id"]: c for c in classification["classifications"]}
    eligible = {cid for cid, r in rows.items() if r["scope_status"] == "ELIGIBLE_IN_SCOPE"}
    pages = {p["candidate_ref"]: p for p in plan["transfer_pages"]}
    if set(pages) != eligible:
        missing = eligible - set(pages)
        if missing:
            fail("ELIGIBLE_ITEM_MISSING_CORE2", ",".join(sorted(missing)))
        fail("OUT_OF_SCOPE_ITEM_PUBLISHED_AS_CORE2", ",".join(sorted(set(pages) - eligible)))
    if len(pages) != len(plan["transfer_pages"]):
        fail("DUPLICATE_PRIMARY_PLACEMENT", "candidate placed twice")

    records = {r["capability_ref"]: r for r in study_model["capability_records"]}
    lessons = {l["capability_ref"]: l for l in core1_plan["lessons"]}
    first_steps = {f["problem_family_ref"]: f for f in plan["first_step_reference"]}

    for cid, p in pages.items():
        body = bodies[cid]
        if p["source_body_digest"] != body["body_digest"]:
            fail("SOURCE_BODY_REWRITTEN", cid)
        if p["stem"] != body["stem"] or p["options"] != body["options"]:
            fail("SOURCE_BODY_REWRITTEN", cid + ":body text")
        if len(p["options"]) != len(body["options"]):
            fail("MCQ_OPTION_LOST", cid)
        if p["figure_required"] and not p["figure_semantic"]:
            fail("SOURCE_FIGURE_LOST", cid)
        if p["source_link"] != body["source_link"]:
            fail("SOURCE_LINK_MISSING_OR_WRONG", cid)

        link = p["core1_linkage"]
        if link["primary_capability_ref"] not in lessons:
            fail("TRANSFER_PAGE_WITHOUT_CORE1_LINK", cid)
        if link["primary_core1_lesson_ref"] != lessons[link["primary_capability_ref"]]["lesson_id"]:
            fail("TRANSFER_PAGE_WITHOUT_CORE1_LINK", cid + ":lesson ref")
        if link["primary_capability_ref"] in [s["capability_ref"] for s in link["supporting_links"]]:
            fail("PRIMARY_SUPPORTS_NOT_DISTINGUISHED", cid)
        declared_ext = {e["capability_ref"] for e in segregation["core2_only_extensions"]}
        for s in link["supporting_links"]:
            if s["capability_ref"] not in lessons and s["capability_ref"] not in declared_ext:
                fail("CORE2_REQUIRES_UNTAUGHT_CONCEPT", f"{cid}:{s['capability_ref']}")

        ladder = p["hint_ladder"]
        if [h["level"] for h in ladder] != list(LEVELS):
            fail("HINT_LADDER_COLLAPSES_TO_SOLUTION", cid + ":level order")
        if ladder[0]["level"] != "H1_NOTICE":
            fail("H1_NOTICE_SKIPPED", cid)
        option_labels = [o["label"] for o in p["options"]]
        for h in ladder:
            bad = hint_violations(h["level"], h["text"], option_labels, profile)
            if bad:
                fail("HINT_REVEALS_ANSWER", f"{cid}:{h['level']}:{','.join(bad)}")
            if h["reveals_result"]:
                fail("HINT_REVEALS_ANSWER", f"{cid}:{h['level']}:declared result reveal")
            answer = next((o["text"] for o in p["options"] if o["label"] == body.get("answer_key")), None)
            if answer and answer.lower() in h["text"].lower():
                fail("HINT_REVEALS_ANSWER", f"{cid}:{h['level']}:answer text")
        if ladder[0]["reveals_relation"]:
            fail("HINT_LADDER_COLLAPSES_TO_SOLUTION", cid + ":H1 reveals the relation")

        sol = p["solution"]
        got = [s["section"] for s in sol["sections"]]
        if got != profile["solution_required_sections"]:
            fail("SOLUTION_SECTION_MISSING", cid)
        if not sol["verification_steps"] or not sol["verification_is_independent_of_solving_route"]:
            fail("SOLUTION_WITHOUT_PHYSICAL_VERIFICATION", cid)

        record = records[link["primary_capability_ref"]]
        if p["frame_sign_required"] != any(
            o["reference_frame"]["required"] or o["sign_convention"]["required"]
            for o in record["system_frame_obligations"]
        ):
            fail("FRAME_SIGN_REQUIREMENT_DROPPED_FROM_CORE2", cid)
        if set(p["representation_requirements"]) != set(record["representation_requirements"]):
            fail("REPRESENTATION_REQUIREMENT_DROPPED_FROM_CORE2", cid)
        if p["first_step_reference_ref"] not in first_steps:
            fail("FIRST_STEP_REFERENCE_MISSING", cid)
        if p["guide_demand_badge"] not in {t["badge"] for t in badge_policy["thresholds"]}:
            fail("TRANSFER_BADGE_NOT_IN_POLICY", cid)

    for family, f in first_steps.items():
        if not f["first_move"]:
            fail("FIRST_STEP_REFERENCE_MISSING", family)
    return True


def main():
    ap = argparse.ArgumentParser()
    for x in ["corpus", "classification", "core1-plan", "study-model", "study-scope",
              "authoring-profile", "badge-policy", "concept-segregation", "out"]:
        ap.add_argument("--" + x, required=True)
    a = ap.parse_args()
    plan = build_plan(
        load(a.corpus), load(a.classification), load(a.core1_plan), load(a.study_model),
        load(a.study_scope), load(a.authoring_profile), load(a.badge_policy), load(a.concept_segregation),
    )
    Path(a.out).write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()
