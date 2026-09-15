#!/usr/bin/env python3
"""P-J — Physics coverage closure, evidence feedback and longitudinal update.

    P-A question set            (the assessment denominator)
  + P-B item validity registry  (what review excluded, and why)
  + P-G Core1 study plan        (lessons + Appendix A practice)
  + P-H representation bundle   (+ optional PhysicalPageMap for realized closure)
  + P-I Core2 transfer plan     (external candidate denominator and pages)
  + P-J transfer-evidence policy (+ optional evidence ledger)
  -> PhysicsSourceCoverageMatrix
  -> PhysicsExternalCorpusCoverageMatrix
  -> PhysicsLearnerStateUpdate + PhysicsLongitudinalUpdate
  -> PhysicsPublicationCoverageClosure

The governing invariant carried forward from P-F is that **one current success
does not close a future obligation**. Every longitudinal dimension declares the
event classes, success count, distinct-instance count and delay that could close
it, and a dimension named in ``never_closable_by_single_current_success`` can
never move to CLOSED on one event.
"""
import argparse, copy, hashlib, json
from collections import Counter, defaultdict
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


# ------------------------------------------------------------ source coverage


def build_source_coverage(question_set, review_registry, core1_plan, core2_plan, study_scope, policy):
    """Every assessment item must be covered, or carry an explicit review disposition."""
    items = [q["question_id"] for q in question_set["questions"]]
    covered_core1_lessons = defaultdict(list)
    for lesson in core1_plan["lessons"]:
        for ref in lesson["scope_trace"]["source_scope_trace_item_refs"]:
            covered_core1_lessons[ref].append(lesson["lesson_id"])
    covered_practice = defaultdict(list)
    lesson_by_cap = {l["capability_ref"]: l for l in core1_plan["lessons"]}
    for item in core1_plan["appendices"]["appendix_a"]["items"]:
        lesson = lesson_by_cap.get(item["primary_capability_ref"])
        if not lesson:
            continue
        for ref in lesson["scope_trace"]["source_scope_trace_item_refs"]:
            covered_practice[ref].append(item["item_id"])

    excluded = {}
    for row in review_registry.get("items", []):
        item_ref = row.get("item_ref") or row.get("question_id")
        state = row.get("validity_state") or row.get("state")
        if item_ref and state and state not in {"VALID", "VALID_WITH_NOTE"}:
            excluded[item_ref] = row.get("reason") or state

    rows, gaps = [], []
    for ref in items:
        core1 = uniq(covered_core1_lessons.get(ref, []))
        practice = uniq(covered_practice.get(ref, []))
        if core1:
            disposition = "COVERED_IN_CORE1_LESSON"
        elif practice:
            disposition = "COVERED_IN_CORE1_PRACTICE"
        elif ref in excluded:
            disposition = "EXCLUDED_BY_REVIEW"
        else:
            disposition = "UNCOVERED"
            gaps.append({"gap_class": "SOURCE_ITEM_UNCOVERED", "ref": ref,
                         "detail": "No Core1 lesson, Core1 practice item or review exclusion covers this item."})
        if disposition not in policy["coverage_dispositions"]:
            fail("COVERAGE_DISPOSITION_NOT_IN_POLICY", disposition)
        rows.append({
            "item_ref": ref,
            "disposition": disposition,
            "core1_lesson_refs": core1,
            "core1_practice_item_refs": practice,
            "exclusion_reason": excluded.get(ref),
        })
    matrix = {
        "matrix_id": "PHY-P-J-SOURCE-COVERAGE-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "question_set_ref": question_set["question_set_id"],
        "denominator": len(items),
        "rows": sorted(rows, key=lambda r: r["item_ref"]),
        "uncovered_item_refs": sorted(r["item_ref"] for r in rows if r["disposition"] == "UNCOVERED"),
        "matrix_digest": "",
    }
    matrix["matrix_digest"] = digest(matrix, "matrix_digest")
    return matrix, gaps


def build_external_coverage(core2_plan, classification, policy):
    rows, gaps = [], []
    pages = {p["candidate_ref"]: p for p in core2_plan["transfer_pages"]}
    for row in classification["classifications"]:
        cid = row["candidate_id"]
        if row["scope_status"] == "ELIGIBLE_IN_SCOPE":
            if cid in pages:
                disposition = "COVERED_IN_CORE2_TRANSFER"
            else:
                disposition = "UNCOVERED"
                gaps.append({"gap_class": "EXTERNAL_CANDIDATE_UNCOVERED", "ref": cid,
                             "detail": "Eligible external candidate has no Core2 transfer page."})
        else:
            disposition = "EXCLUDED_BY_REVIEW"
        rows.append({
            "candidate_ref": cid,
            "scope_status": row["scope_status"],
            "disposition": disposition,
            "core2_page_ref": pages[cid]["page_id"] if cid in pages else None,
            "exclusion_reason": row.get("out_of_scope_reason"),
        })
    matrix = {
        "matrix_id": "PHY-P-J-EXTERNAL-COVERAGE-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "corpus_ref": core2_plan["corpus_ref"],
        "denominator": len(rows),
        "rows": sorted(rows, key=lambda r: r["candidate_ref"]),
        "uncovered_candidate_refs": sorted(r["candidate_ref"] for r in rows
                                           if r["disposition"] == "UNCOVERED"),
        "matrix_digest": "",
    }
    matrix["matrix_digest"] = digest(matrix, "matrix_digest")
    return matrix, gaps


# ----------------------------------------------------- longitudinal feedback


def validate_ledger(ledger, study_scope, policy):
    if ledger is None:
        return []
    if ledger.get("production_claim") is not False:
        fail("SYNTHETIC_EVIDENCE_CLAIMED_AS_PRODUCTION")
    if ledger.get("ledger_digest") != digest(ledger, "ledger_digest"):
        fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", "ledger digest")
    caps = {r["capability_ref"] for r in study_scope["capability_scope_records"]}
    classes = set(policy["event_classes"])
    outcomes = set(policy["outcomes"])
    seen = set()
    for e in ledger["events"]:
        if e["event_id"] in seen:
            fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", "duplicate " + e["event_id"])
        seen.add(e["event_id"])
        if e.get("event_digest") != digest(e, "event_digest"):
            fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", e["event_id"] + ":digest")
        if e["capability_ref"] not in caps:
            fail("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", e["event_id"] + ":unknown capability")
        if e["event_class"] not in classes:
            fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", e["event_id"] + ":unknown event class")
        if e["outcome"] not in outcomes:
            fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", e["event_id"] + ":unknown outcome")
        if not e.get("source_trace_refs"):
            fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", e["event_id"])
        if not e.get("instance_ref"):
            fail("EVIDENCE_EVENT_WITHOUT_SOURCE_TRACE", e["event_id"] + ":no instance")
    return ledger["events"]


def dimension_state(dimension, events, policy, prior_state):
    """Decide whether accumulated evidence may move a dimension to CLOSED."""
    rule = policy["dimension_closure_rules"][dimension]
    eligible = [e for e in events
                if e["event_class"] in rule["closable_by_event_classes"] and e["outcome"] == "CORRECT"]
    successes = len(eligible)
    instances = len({e["instance_ref"] for e in eligible})
    max_delay = max((e["days_since_core1"] for e in eligible), default=0)
    single_success_forbidden = dimension in policy["never_closable_by_single_current_success"]

    if successes == 0:
        return prior_state, {"successes": 0, "distinct_instances": 0, "max_delay_days": 0,
                             "blocked_reason": None if prior_state != "OPEN" else "NO_QUALIFYING_EVIDENCE"}
    blocked = None
    if single_success_forbidden and successes < 2:
        blocked = "SINGLE_CURRENT_SUCCESS_MAY_NOT_CLOSE_THIS_DIMENSION"
    elif successes < rule["minimum_successes"]:
        blocked = "BELOW_MINIMUM_SUCCESSES"
    elif instances < rule["minimum_distinct_instances"]:
        blocked = "BELOW_MINIMUM_DISTINCT_INSTANCES"
    elif max_delay < rule["minimum_delay_days"]:
        blocked = "BELOW_MINIMUM_DELAY"
    state = "OPEN_WITH_PARTIAL_EVIDENCE" if blocked else "CLOSED"
    if prior_state == "NOT_APPLICABLE":
        state = "NOT_APPLICABLE"
    return state, {"successes": successes, "distinct_instances": instances,
                   "max_delay_days": max_delay, "blocked_reason": blocked}


def build_longitudinal_update(study_model, events, policy):
    by_cap = defaultdict(list)
    for e in events:
        by_cap[e["capability_ref"]].append(e)
    prior = {row["capability_ref"]: row for row in study_model["longitudinal_initializations"]}
    updates = []
    for row in study_model["longitudinal_initializations"]:
        cap = row["capability_ref"]
        dims_before = row["dimensions"]
        if set(dims_before) != set(policy["longitudinal_dimensions"]):
            fail("LONGITUDINAL_DIMENSION_DROPPED", cap)
        dims_after, evidence = {}, {}
        for dim in policy["longitudinal_dimensions"]:
            before = dims_before[dim]
            after, detail = dimension_state(dim, by_cap.get(cap, []), policy, before)
            if before in {"CURRENT_EVIDENCE", "PARTIAL_CURRENT_EVIDENCE"} and after == "OPEN":
                after = before
            dims_after[dim] = after
            evidence[dim] = detail
        updates.append({
            "capability_ref": cap,
            "dimensions_before": dict(dims_before),
            "dimensions_after": dims_after,
            "evidence_detail": evidence,
            "future_evidence_obligations": list(row["future_evidence_obligations"]),
            "event_refs": sorted(e["event_id"] for e in by_cap.get(cap, [])),
        })
    out = {
        "update_id": "PHY-P-J-LONGITUDINAL-UPDATE-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "study_model_ref": study_model["study_model_id"],
        "study_model_digest": study_model["study_model_digest"],
        "policy_ref": policy["policy_id"],
        "capability_updates": sorted(updates, key=lambda x: x["capability_ref"]),
        "update_digest": "",
    }
    out["update_digest"] = digest(out, "update_digest")
    return out


def build_learner_state_update(study_model, longitudinal, events, policy):
    by_cap = defaultdict(list)
    for e in events:
        by_cap[e["capability_ref"]].append(e)
    rows = []
    for rec in study_model["capability_records"]:
        cap = rec["capability_ref"]
        evs = by_cap.get(cap, [])
        correct = sum(1 for e in evs if e["outcome"] == "CORRECT")
        incorrect = sum(1 for e in evs if e["outcome"] == "INCORRECT")
        if not evs:
            state = rec["learner_state"]
            reason = "No transfer evidence has been recorded for this capability."
        elif incorrect and correct:
            state = "MIXED"
            reason = "Transfer evidence is mixed; the capability stays in scope and a probe remains appropriate."
        elif incorrect:
            state = "EVIDENCE_OF_DIFFICULTY"
            reason = "Transfer evidence shows difficulty; the capability stays in scope."
        else:
            state = "DEMONSTRATED"
            reason = "Transfer evidence is currently correct; future obligations remain open."
        rows.append({
            "capability_ref": cap,
            "prior_state": rec["learner_state"],
            "updated_state": state,
            "reason": reason,
            "event_refs": sorted(e["event_id"] for e in evs),
            "remains_in_assessment_scope": True,
        })
    out = {
        "update_id": "PHY-P-J-LEARNER-STATE-UPDATE-v1",
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "study_model_ref": study_model["study_model_id"],
        "longitudinal_update_ref": longitudinal["update_id"],
        "capability_updates": sorted(rows, key=lambda x: x["capability_ref"]),
        "assessment_scope_unchanged": True,
        "update_digest": "",
    }
    out["update_digest"] = digest(out, "update_digest")
    return out


# ---------------------------------------------------------------- closure


def build_closure(question_set, review_registry, core1_plan, representation_bundle, core2_plan,
                  classification, study_scope, study_model, policy, ledger=None, page_map=None,
                  closure_id="PHY-P-J-COVERAGE-CLOSURE-v1"):
    if policy.get("policy_digest") != digest(policy, "policy_digest"):
        fail("COVERAGE_POLICY_DIGEST_MISMATCH")
    if core1_plan["study_model_digest"] != study_model["study_model_digest"]:
        fail("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", "core1 drift")
    if representation_bundle["core1_plan_digest"] != core1_plan["plan_digest"]:
        fail("CLOSURE_CLAIMED_WITHOUT_PHYSICAL_REALIZATION", "representation drift")
    if core2_plan["core1_plan_digest"] != core1_plan["plan_digest"]:
        fail("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", "core2 drift")

    source_matrix, source_gaps = build_source_coverage(
        question_set, review_registry, core1_plan, core2_plan, study_scope, policy)
    external_matrix, external_gaps = build_external_coverage(core2_plan, classification, policy)

    # representation coverage: every required capability must have a realized representation
    rep_by_cap = defaultdict(list)
    for spec in representation_bundle["representations"]:
        rep_by_cap[spec["capability_ref"]].append(spec["representation_id"])
    rep_gaps = []
    for rec in study_scope["capability_scope_records"]:
        if not rep_by_cap.get(rec["capability_ref"]):
            rep_gaps.append({"gap_class": "CAPABILITY_WITHOUT_REPRESENTATION_COVERAGE",
                             "ref": rec["capability_ref"],
                             "detail": "No P-H representation covers this required capability."})

    realization_gaps = []
    realized = False
    if policy["closure_requires_physical_realization"]:
        if page_map is None:
            realization_gaps.append({
                "gap_class": "PHYSICAL_REALIZATION_ABSENT", "ref": representation_bundle["bundle_id"],
                "detail": "Closure requires a PhysicalPageMap proving the representations were rendered."})
        else:
            if page_map["bundle_digest"] != representation_bundle["bundle_digest"]:
                fail("CLOSURE_CLAIMED_WITHOUT_PHYSICAL_REALIZATION", "page map bundle drift")
            placed = {p["content_ref"] for p in page_map["content_placements"]}
            missing = {s["representation_id"] for s in representation_bundle["representations"]} - placed
            if missing:
                realization_gaps.append({
                    "gap_class": "REPRESENTATION_NOT_PHYSICALLY_PLACED", "ref": sorted(missing)[0],
                    "detail": f"{len(missing)} representation(s) have no physical placement."})
            if page_map["realization_summary"]["label_only_figure_count"]:
                realization_gaps.append({
                    "gap_class": "TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED",
                    "ref": page_map["physical_page_map_id"],
                    "detail": "At least one figure emitted no vector graphics."})
            realized = not realization_gaps

    events = validate_ledger(ledger, study_scope, policy)
    longitudinal = build_longitudinal_update(study_model, events, policy)
    learner_state = build_learner_state_update(study_model, longitudinal, events, policy)

    gaps = source_gaps + external_gaps + rep_gaps + realization_gaps
    closure_state = "CLOSED" if not gaps else "OPEN"
    closure = {
        "closure_id": closure_id,
        "schema_version": "1.0.0",
        "subject": "PHYSICS",
        "policy_ref": policy["policy_id"],
        "study_scope_ref": study_scope["study_scope_id"],
        "study_scope_digest": study_scope["study_scope_digest"],
        "core1_plan_ref": core1_plan["plan_id"],
        "representation_bundle_ref": representation_bundle["bundle_id"],
        "core2_plan_ref": core2_plan["plan_id"],
        "physical_page_map_ref": page_map["physical_page_map_id"] if page_map else None,
        "artifact_sha256": page_map["artifact_sha256"] if page_map else None,
        "source_coverage_matrix": source_matrix,
        "external_corpus_coverage_matrix": external_matrix,
        "longitudinal_update": longitudinal,
        "learner_state_update": learner_state,
        "closure_state": closure_state,
        "physically_realized": realized,
        "gaps": sorted(gaps, key=lambda g: (g["gap_class"], g["ref"])),
        "summary": {
            "source_denominator": source_matrix["denominator"],
            "source_uncovered": len(source_matrix["uncovered_item_refs"]),
            "external_denominator": external_matrix["denominator"],
            "external_uncovered": len(external_matrix["uncovered_candidate_refs"]),
            "capability_count": len(study_scope["capability_scope_records"]),
            "evidence_event_count": len(events),
            "dimensions_closed": sum(
                1 for u in longitudinal["capability_updates"]
                for v in u["dimensions_after"].values() if v == "CLOSED"
            ),
            "dimensions_open": sum(
                1 for u in longitudinal["capability_updates"]
                for v in u["dimensions_after"].values() if v.startswith("OPEN")
            ),
        },
        "human_expert_review_states": {
            "SUBJECT_EXPERT_PASS": "PENDING",
            "PEDAGOGY_EXPERT_PASS": "PENDING",
            "ASSESSMENT_EXPERT_PASS": "PENDING",
        },
        "closure_digest": "",
    }
    closure["closure_digest"] = digest(closure, "closure_digest")
    validate_closure(closure, study_scope, study_model, policy)
    return closure


def validate_closure(closure, study_scope, study_model, policy):
    if closure["closure_digest"] != digest(closure, "closure_digest"):
        fail("COVERAGE_POLICY_DIGEST_MISMATCH", "closure digest")
    for state in closure["human_expert_review_states"].values():
        if state == "PASS":
            fail("FAKE_HUMAN_REVIEW_STATE", "closure claims an expert pass")

    if closure["closure_state"] == "CLOSED":
        if closure["source_coverage_matrix"]["uncovered_item_refs"]:
            fail("SOURCE_ITEM_UNCOVERED_BUT_CLOSURE_CLAIMED",
                 ",".join(closure["source_coverage_matrix"]["uncovered_item_refs"]))
        if closure["external_corpus_coverage_matrix"]["uncovered_candidate_refs"]:
            fail("EXTERNAL_CANDIDATE_UNCOVERED_BUT_CLOSURE_CLAIMED",
                 ",".join(closure["external_corpus_coverage_matrix"]["uncovered_candidate_refs"]))
        if closure["gaps"]:
            fail("CLOSURE_CLAIMED_WITH_OPEN_GAPS", closure["gaps"][0]["gap_class"])
        if policy["closure_requires_physical_realization"] and not closure["physically_realized"]:
            fail("CLOSURE_CLAIMED_WITHOUT_PHYSICAL_REALIZATION", closure["closure_id"])

    if closure["learner_state_update"]["assessment_scope_unchanged"] is not True:
        fail("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", "learner state update")
    scope_caps = {r["capability_ref"] for r in study_scope["capability_scope_records"]}
    updated = {r["capability_ref"] for r in closure["learner_state_update"]["capability_updates"]}
    if updated != scope_caps:
        fail("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", "capability coverage")
    for row in closure["learner_state_update"]["capability_updates"]:
        if row["remains_in_assessment_scope"] is not True:
            fail("TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE", row["capability_ref"])

    forbidden = set(policy["never_closable_by_single_current_success"])
    for u in closure["longitudinal_update"]["capability_updates"]:
        if set(u["dimensions_after"]) != set(policy["longitudinal_dimensions"]):
            fail("LONGITUDINAL_DIMENSION_DROPPED", u["capability_ref"])
        for dim, state in u["dimensions_after"].items():
            detail = u["evidence_detail"][dim]
            if state == "CLOSED":
                rule = policy["dimension_closure_rules"][dim]
                # delayed retention keeps its own falsifier name, because "one success now
                # closes a delayed obligation" is the specific defect P-F named.
                code = ("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL"
                        if dim == "delayed_retention" else "ONE_CURRENT_SUCCESS_CLOSES_FUTURE_EVIDENCE")
                if dim in forbidden and detail["successes"] < 2:
                    fail(code, f"{u['capability_ref']}:{dim}")
                if detail["successes"] < rule["minimum_successes"]:
                    fail(code, f"{u['capability_ref']}:{dim}:successes")
                if detail["distinct_instances"] < rule["minimum_distinct_instances"]:
                    fail(code, f"{u['capability_ref']}:{dim}:instances")
                if detail["max_delay_days"] < rule["minimum_delay_days"]:
                    fail("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL",
                         f"{u['capability_ref']}:{dim}:delay")
    return True


def main():
    ap = argparse.ArgumentParser()
    for x in ["question-set", "review-registry", "core1-plan", "representation-bundle",
              "core2-plan", "classification", "study-scope", "study-model", "policy", "out"]:
        ap.add_argument("--" + x, required=True)
    ap.add_argument("--evidence-ledger")
    ap.add_argument("--page-map")
    a = ap.parse_args()
    closure = build_closure(
        load(a.question_set), load(a.review_registry), load(a.core1_plan),
        load(a.representation_bundle), load(a.core2_plan), load(a.classification),
        load(a.study_scope), load(a.study_model), load(a.policy),
        load(a.evidence_ledger) if a.evidence_ledger else None,
        load(a.page_map) if a.page_map else None,
    )
    Path(a.out).write_text(json.dumps(closure, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()
