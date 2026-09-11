#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

POLICY_VERSION = "MATH-ME-DIAGNOSTIC-v1"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value, omit=None):
    if isinstance(value, dict) and omit:
        value = {k: v for k, v in value.items() if k != omit}
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def item_ref(question_ref, part_ref):
    return part_ref or question_ref


def build_scope_fingerprint(questions, reviews, authority, item_semantics):
    payload = {
        "question_set_ref": questions["question_set_id"],
        "question_set_digest": questions.get("question_set_digest") or digest(questions, "question_set_digest"),
        "review_registry_digest": reviews.get("registry_digest") or digest(reviews, "registry_digest"),
        "scope_authority_digest": authority.get("authority_digest") or digest(authority, "authority_digest"),
        "item_semantics_digest": item_semantics.get("registry_digest") or digest(item_semantics, "registry_digest"),
    }
    return digest(payload)


def build_ledger(questions, attempts):
    qconf = {q["question_id"]: q["source_provenance"]["extraction_confidence"] for q in questions["questions"]}
    records = []
    if attempts:
        for attempt in attempts.get("attempts", []):
            for step in attempt["response"].get("work_steps", []):
                records.append({
                    "evidence_id": f"EVID-{attempt['attempt_id']}-{step['step_id']}",
                    "attempt_id": attempt["attempt_id"],
                    "question_ref": attempt["question_ref"],
                    "part_ref": attempt.get("part_ref"),
                    "step_ref": step["step_id"],
                    "observed_text": step["text"],
                    "source_locator": attempt["source_locator"],
                    "attempt_extraction_confidence": attempt["extraction_confidence"],
                    "question_extraction_confidence": qconf[attempt["question_ref"]],
                })
    ledger = {
        "ledger_id": "MATH-ME-LEDGER-" + digest(records)[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "question_set_ref": questions["question_set_id"],
        "attempt_mode": "PRESENT" if attempts else "ABSENT",
        "attempt_set_ref": attempts.get("attempt_set_id") if attempts else None,
        "records": records,
    }
    ledger["ledger_digest"] = digest(ledger, "ledger_digest")
    return ledger


def review_map(reviews):
    return {r["item_ref"]: r for r in reviews["reviews"]}


def registry_map(registry):
    return {x["observation_type"]: x for x in registry["types"]}


def capability_ids(authority):
    return [x["capability_id"] for x in authority["capabilities"]]


def build_observations(ledger, reviewed_fixture, reviews, authority, item_semantics, obs_registry):
    if not reviewed_fixture:
        return []
    evidence = {(r["attempt_id"], r["step_ref"]): r for r in ledger["records"]}
    valid_items = {x["item_ref"] for x in item_semantics["profiles"]}
    valid_caps = set(capability_ids(authority))
    types = registry_map(obs_registry)
    rmap = review_map(reviews)
    output = []
    seen = set()
    for raw in reviewed_fixture["observations"]:
        key = (raw["attempt_id"], raw["step_ref"])
        if key not in evidence:
            raise ValueError(f"OBSERVATION_WITHOUT_EVIDENCE:{raw['observation_id']}")
        ev = evidence[key]
        if raw["question_ref"] != ev["question_ref"] or raw.get("part_ref") != ev.get("part_ref"):
            raise ValueError(f"OBSERVATION_BINDING_MISMATCH:{raw['observation_id']}")
        iref = item_ref(raw["question_ref"], raw.get("part_ref"))
        if iref not in valid_items:
            raise ValueError(f"OBSERVATION_UNKNOWN_ITEM:{iref}")
        if raw["observation_type"] not in types:
            raise ValueError(f"OBSERVATION_UNKNOWN_TYPE:{raw['observation_type']}")
        unknown_caps = set(raw["capability_refs"]) - valid_caps
        if unknown_caps:
            raise ValueError("OBSERVATION_UNKNOWN_CAPABILITY:" + ",".join(sorted(unknown_caps)))
        if raw["observation_id"] in seen:
            raise ValueError(f"DUPLICATE_OBSERVATION:{raw['observation_id']}")
        seen.add(raw["observation_id"])
        polarity = types[raw["observation_type"]]["default_polarity"]
        diagnostic_use = rmap[iref]["diagnostic_use"]
        negative_like = polarity in {"NEGATIVE", "AMBIGUOUS"}
        diagnostic_eligible = not negative_like or diagnostic_use not in {"POSITIVE_EVIDENCE_ONLY", "EXCLUDE_FROM_NEGATIVE_INFERENCE"}
        effective_confidence = min(
            float(raw["reviewer_confidence"]),
            float(ev["attempt_extraction_confidence"]),
            float(ev["question_extraction_confidence"]),
        )
        output.append({
            "observation_id": raw["observation_id"],
            "evidence_ref": ev["evidence_id"],
            "attempt_id": raw["attempt_id"],
            "item_ref": iref,
            "step_ref": raw["step_ref"],
            "observation_type": raw["observation_type"],
            "capability_refs": raw["capability_refs"],
            "polarity": polarity,
            "expected_relation": raw["expected_relation"],
            "observed_relation": raw["observed_relation"],
            "reviewer_confidence": raw["reviewer_confidence"],
            "effective_confidence": effective_confidence,
            "diagnostic_eligible": diagnostic_eligible,
            "diagnostic_use": diagnostic_use,
        })
    return sorted(output, key=lambda x: x["observation_id"])


def alternatives(observation_type):
    if observation_type == "ARITHMETIC_DIVISION_ERROR":
        return ["ARITHMETIC_SLIP", "EXECUTION_SLIP"]
    if observation_type == "INCORRECT_BINOMIAL_EXPANSION":
        return ["EXECUTION_SLIP", "INCOMPLETE_PREREQUISITE"]
    if observation_type in {"ORDERED_PAIR_ROLE_CONFUSION", "SLOPE_ORIENTATION_ERROR"}:
        return ["MISREAD_CONDITION", "INCOMPLETE_PREREQUISITE", "WRONG_MODEL"]
    return ["EXECUTION_SLIP", "INCOMPLETE_PREREQUISITE", "WRONG_MODEL"]


def derive_cases(observations):
    grouped = {}
    for obs in observations:
        if not obs["diagnostic_eligible"] or obs["polarity"] not in {"NEGATIVE", "AMBIGUOUS"}:
            continue
        for cap in obs["capability_refs"]:
            grouped.setdefault(cap, []).append(obs)
    cases = []
    for cap in sorted(grouped):
        obs = grouped[cap]
        attempt_count = len({x["attempt_id"] for x in obs})
        ambiguous = any(x["polarity"] == "AMBIGUOUS" for x in obs)
        if ambiguous:
            status, strength = "UNRESOLVED", "AMBIGUOUS_OBSERVATION"
        elif attempt_count >= 2:
            status, strength = "CORROBORATED", "REPEATED_INDEPENDENT_OBSERVATIONS"
        else:
            status, strength = "SUSPECTED", "SINGLE_ORDINARY_OBSERVATION"
        alt = sorted({a for x in obs for a in alternatives(x["observation_type"])})
        cases.append({
            "diagnostic_case_id": "MATH-DC-" + digest([cap] + [x["observation_id"] for x in obs])[:16],
            "target_capability_ref": cap,
            "observation_refs": sorted(x["observation_id"] for x in obs),
            "hypothesis_status": status,
            "evidence_strength": strength,
            "probe_required": True,
            "probe_target_capability_refs": [cap],
            "alternative_explanations": alt,
            "diagnostic_policy_version": POLICY_VERSION,
        })
    return cases


def derive_states(authority, observations):
    by_cap = {cap: [] for cap in capability_ids(authority)}
    for obs in observations:
        if obs["polarity"] in {"QUALITY_RISK", "BEHAVIOR"}:
            continue
        if not obs["diagnostic_eligible"] and obs["polarity"] in {"NEGATIVE", "AMBIGUOUS"}:
            continue
        for cap in obs["capability_refs"]:
            by_cap[cap].append(obs)
    states = []
    for cap in capability_ids(authority):
        obs = by_cap[cap]
        pos = [x for x in obs if x["polarity"] == "POSITIVE"]
        neg = [x for x in obs if x["polarity"] == "NEGATIVE"]
        amb = [x for x in obs if x["polarity"] == "AMBIGUOUS"]
        if neg:
            readiness = "DEVELOPING"
        elif amb:
            readiness = "UNKNOWN"
        elif pos:
            readiness = "READY"
        else:
            readiness = "UNKNOWN"
        confidence = min((x["effective_confidence"] for x in obs), default=0.0)
        states.append({
            "capability_ref": cap,
            "readiness": readiness,
            "confidence": confidence,
            "positive_independent_count": len(pos),
            "negative_independent_count": len(neg),
            "ambiguous_count": len(amb),
            "observation_refs": sorted(x["observation_id"] for x in obs),
        })
    return states


def verification_behavior(observations):
    not_done = any(x["observation_type"] == "VERIFICATION_NOT_PERFORMED" for x in observations)
    failed = any(x["observation_type"] == "VERIFICATION_FAILED" for x in observations)
    return {
        "self_initiated_verification_observed": False if not_done else None,
        "verification_failure_observed": True if failed else None,
    }


def derive(questions, reviews, authority, item_semantics, obs_registry, attempts=None, reviewed_fixture=None):
    scope_fp = build_scope_fingerprint(questions, reviews, authority, item_semantics)
    ledger = build_ledger(questions, attempts)
    observations = build_observations(ledger, reviewed_fixture, reviews, authority, item_semantics, obs_registry) if attempts else []
    cases = derive_cases(observations)
    snapshot = {
        "snapshot_id": "MATH-ME-SNAPSHOT-" + digest([scope_fp, ledger["ledger_digest"], [x["observation_id"] for x in observations]])[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "question_set_ref": questions["question_set_id"],
        "attempt_mode": "PRESENT" if attempts else "ABSENT",
        "scope_fingerprint": scope_fp,
        "evidence_ledger_digest": ledger["ledger_digest"],
        "diagnostic_policy_version": POLICY_VERSION,
        "capability_states": derive_states(authority, observations),
        "diagnostic_cases": cases,
        "verification_behavior": verification_behavior(observations),
    }
    snapshot["snapshot_digest"] = digest(snapshot, "snapshot_digest")
    return {"evidence_ledger": ledger, "observations": observations, "learner_state_snapshot": snapshot}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--reviews", required=True)
    ap.add_argument("--authority", required=True)
    ap.add_argument("--item-semantics", required=True)
    ap.add_argument("--observation-registry", required=True)
    ap.add_argument("--attempts")
    ap.add_argument("--reviewed-observations")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if bool(args.attempts) != bool(args.reviewed_observations):
        raise SystemExit("Attempt mode requires both --attempts and --reviewed-observations; no-attempt mode requires neither.")
    result = derive(
        load(args.questions), load(args.reviews), load(args.authority), load(args.item_semantics),
        load(args.observation_registry), load(args.attempts) if args.attempts else None,
        load(args.reviewed_observations) if args.reviewed_observations else None,
    )
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
