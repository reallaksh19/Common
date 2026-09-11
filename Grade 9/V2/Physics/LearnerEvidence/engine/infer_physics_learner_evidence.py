#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import defaultdict
from pathlib import Path
from jsonschema import Draft202012Validator

D = Path(__file__).resolve().parents[1]
PHYSICS = D.parent
V2 = PHYSICS.parent
SHARED = V2 / "Shared" / "LearnerIntelligence" / "contracts"
CONTRACTS = D / "contracts"
sys.path.insert(0, str(PHYSICS / "AssessmentIntake" / "engine"))
from build_physics_assessment_intake import validate_attempt_set, validate_question_set  # noqa:E402

FORBIDDEN_TEXT = ("PR #156", "PR156", "benchmark_template", "mature_reference")

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()

def digest_without_field(value, field, sort_array=None, key=None):
    clone = copy.deepcopy(value)
    clone.pop(field, None)
    if sort_array and key:
        clone[sort_array] = sorted(clone[sort_array], key=lambda row: row[key])
    return digest(clone)

def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)

def validate_schema(value, path):
    Draft202012Validator(load(path)).validate(value)

def scope_fingerprint(problem_semantics):
    rows = []
    for item in problem_semantics["items"]:
        rows.append({
            "item_ref": item["item_ref"],
            "mapping_state": item["mapping_state"],
            "resolution_status": item["resolution_status"],
            "source_integrity_state": item["source_integrity_state"],
            "validity_state": item["validity_state"],
            "diagnostic_use": item["diagnostic_use"],
            "family_refs": item["family_refs"],
            "primary_family_ref": item["primary_family_ref"],
        })
    payload = {
        "question_set_ref": problem_semantics["question_set_ref"],
        "scope_model_ref": problem_semantics["scope_model_ref"],
        "scope_coverage_ref": problem_semantics["scope_coverage_ref"],
        "items": sorted(rows, key=lambda row: row["item_ref"]),
    }
    return problem_semantics["scope_model_ref"], digest(payload)

def attempt_item_ref(attempt):
    part = attempt.get("part_ref")
    if part is None:
        return attempt["question_ref"]
    if str(part).startswith(attempt["question_ref"] + "."):
        return str(part)
    return f"{attempt['question_ref']}.{part}"

def initial_capability_state(problem_semantics):
    refs = set()
    for item in problem_semantics["items"]:
        for step in item["reasoning_route"]["steps"]:
            refs.update(step.get("capability_refs", []))
    return {
        ref: {
            "capability_ref": ref,
            "state": "UNKNOWN",
            "confidence": 0.0,
            "positive_evidence_refs": [],
            "negative_evidence_refs": [],
        }
        for ref in sorted(refs)
    }

def validate_registries(registry, policy):
    if registry["subject"] != "PHYSICS" or registry["schema_version"] != "1.0.0":
        fail("PHYSICS_OBSERVATION_REGISTRY_IDENTITY")
    if registry["registry_digest"] != digest_without_field(registry, "registry_digest"):
        fail("PHYSICS_OBSERVATION_REGISTRY_DIGEST_MISMATCH")
    codes = {row["code"]: row for row in registry["codes"]}
    if len(codes) != len(registry["codes"]):
        fail("DUPLICATE_PHYSICS_OBSERVATION_CODE")
    required = {
        "CORRECT_SYSTEM_SELECTION", "CORRECT_REFERENCE_FRAME", "CORRECT_MODEL_SELECTION",
        "CORRECT_RELATION_SELECTION", "CORRECT_STATE_EXTRACTION",
        "CORRECT_REPRESENTATION_TRANSLATION", "INVALID_STATE_RESET",
        "OMITTED_PHASE_HANDOFF", "SIGN_DIRECTION_MISMATCH",
        "DISTANCE_DISPLACEMENT_CONFUSION", "GRAPH_HEIGHT_SLOPE_AREA_CONFUSION",
        "APEX_COMPONENT_AMBIGUITY", "ARITHMETIC_EXECUTION_ERROR",
        "MODEL_VALIDITY_IGNORED", "VERIFICATION_NOT_PERFORMED", "VERIFICATION_FAILED",
    }
    if set(codes) != required:
        fail("PHYSICS_OBSERVATION_VOCABULARY_COVERAGE",
             f"missing={sorted(required-set(codes))},extra={sorted(set(codes)-required)}")
    valid_effects = {"POSITIVE", "NEGATIVE", "AMBIGUITY_ONLY", "SHARED_EXTERNAL"}
    for row in codes.values():
        if row["state_effect"] not in valid_effects or not row["allowed_roles"]:
            fail("PHYSICS_OBSERVATION_CODE_INVALID", row["code"])
    if policy["subject"] != "PHYSICS" or policy["schema_version"] != "1.0.0":
        fail("PHYSICS_DIAGNOSTIC_POLICY_IDENTITY")
    if policy["policy_digest"] != digest_without_field(policy, "policy_digest"):
        fail("PHYSICS_DIAGNOSTIC_POLICY_DIGEST_MISMATCH")
    if policy.get("benchmark_inputs"):
        fail("BENCHMARK_PRODUCER_INPUT_FORBIDDEN")
    raw = canonical({"registry": registry, "policy": policy})
    if any(token in raw for token in FORBIDDEN_TEXT):
        fail("BENCHMARK_PRODUCER_INPUT_FORBIDDEN")
    return codes

def validate_ledger(ledger, attempts, question_set, problem_semantics, registry, policy):
    validate_schema(ledger, SHARED / "learner-evidence-ledger.schema.json")
    if ledger["ledger_digest"] != digest_without_field(
        ledger, "ledger_digest", "observations", "observation_id"
    ):
        fail("LEARNER_EVIDENCE_LEDGER_DIGEST_MISMATCH")
    if ledger["subject"] != "PHYSICS" or ledger["attempt_set_ref"] != attempts["attempt_set_id"]:
        fail("EVIDENCE_ATTEMPT_SET_MISMATCH")
    validate_question_set(question_set)
    validate_attempt_set(attempts, question_set)
    if problem_semantics["question_set_ref"] != question_set["question_set_id"]:
        fail("PROBLEM_SEMANTICS_QUESTION_SET_MISMATCH")

    codes = validate_registries(registry, policy)
    attempt_by = {a["attempt_id"]: a for a in attempts["attempts"]}
    item_by = {x["item_ref"]: x for x in problem_semantics["items"]}
    seen = set()
    normalized = []

    for obs in ledger["observations"]:
        validate_schema(obs, CONTRACTS / "physics-reasoning-observation.schema.json")
        oid = obs["observation_id"]
        if oid in seen:
            fail("DUPLICATE_REASONING_OBSERVATION", oid)
        seen.add(oid)
        if obs["attempt_ref"] not in attempt_by:
            fail("OBSERVATION_WITHOUT_ATTEMPT", oid)
        attempt = attempt_by[obs["attempt_ref"]]
        if attempt_item_ref(attempt) != obs["item_ref"]:
            fail("OBSERVATION_ITEM_BINDING_MISMATCH", oid)
        if obs["item_ref"] not in item_by:
            fail("OBSERVATION_WITHOUT_P_D_SEMANTICS", obs["item_ref"])
        if obs["observation_code"] not in codes:
            fail("UNKNOWN_PHYSICS_OBSERVATION_CODE", obs["observation_code"])
        meta = codes[obs["observation_code"]]
        if obs["polarity"] != meta["polarity"]:
            fail("OBSERVATION_POLARITY_MISMATCH", oid)

        item = item_by[obs["item_ref"]]
        steps = {s["step_id"]: s for s in item["reasoning_route"]["steps"]}
        if obs["route_step_ref"] not in steps:
            fail("OBSERVATION_ROUTE_STEP_MISMATCH", oid)
        step = steps[obs["route_step_ref"]]
        if step["role"] != obs["route_role"]:
            fail("OBSERVATION_ROUTE_ROLE_MISMATCH", oid)
        if obs["route_role"] not in meta["allowed_roles"]:
            fail("OBSERVATION_CODE_ROLE_MISMATCH", oid)

        allowed_caps = {
            cap
            for route_step in item["reasoning_route"]["steps"]
            for cap in route_step.get("capability_refs", [])
        }
        if not set(obs["capability_refs"]).issubset(allowed_caps):
            fail("OBSERVATION_CAPABILITY_BINDING_MISMATCH", oid)
        if meta["state_effect"] in {"POSITIVE", "NEGATIVE", "AMBIGUITY_ONLY"} and not obs["capability_refs"]:
            fail("PHYSICS_OBSERVATION_WITHOUT_CAPABILITY", oid)

        rep = obs["representation_ref"]
        if rep is not None:
            source_reps = set(attempt.get("representation_refs", []))
            semantic_reps = set(step.get("representation_refs", []))
            if rep not in source_reps and rep not in semantic_reps:
                fail("OBSERVATION_REPRESENTATION_BINDING_MISMATCH", oid)

        effective = min(
            obs["observation_confidence"],
            obs["extraction_confidence"],
            obs["transcription_confidence"],
            attempt["extraction_confidence"],
        )
        blocked = item["resolution_status"] == "BLOCKED"
        negative_blocked = item["diagnostic_use"] in {
            "EXCLUDE_FROM_NEGATIVE_INFERENCE", "POSITIVE_EVIDENCE_ONLY"
        }

        if blocked:
            disposition = "IGNORED_INVALID_ITEM"
        elif effective < policy["minimum_confidence_for_state"]:
            disposition = "LOW_CONFIDENCE_PROBE_REQUIRED"
        elif meta["state_effect"] == "SHARED_EXTERNAL":
            disposition = "SHARED_EXECUTION_ERROR_LOCALIZED"
        elif meta["state_effect"] == "AMBIGUITY_ONLY":
            disposition = "AMBIGUITY_PROBE_REQUIRED"
        elif meta["state_effect"] == "POSITIVE":
            disposition = "CREDITED"
        elif negative_blocked:
            disposition = "IGNORED_INVALID_ITEM"
        else:
            disposition = "NEGATIVE_EVIDENCE"

        normalized.append({
            "observation_ref": oid,
            "attempt_ref": obs["attempt_ref"],
            "item_ref": obs["item_ref"],
            "observation_code": obs["observation_code"],
            "capability_refs": list(obs["capability_refs"]),
            "effective_confidence": effective,
            "state_effect": meta["state_effect"],
            "probe_family": meta["probe_family"],
            "disposition": disposition,
        })
    return normalized, codes

def reduce_normalized_records(capability_refs, normalized, policy):
    state = {
        cap: {
            "capability_ref": cap,
            "state": "UNKNOWN",
            "confidence": 0.0,
            "positive_evidence_refs": [],
            "negative_evidence_refs": [],
        }
        for cap in sorted(capability_refs)
    }
    grouped = defaultdict(list)
    probes = set()

    for row in normalized:
        disp = row["disposition"]
        if disp == "CREDITED":
            for cap in row["capability_refs"]:
                if cap in state:
                    state[cap]["positive_evidence_refs"].append(row["observation_ref"])
                    state[cap]["confidence"] = max(state[cap]["confidence"], row["effective_confidence"])
        elif disp == "NEGATIVE_EVIDENCE":
            for cap in row["capability_refs"]:
                if cap in state:
                    state[cap]["negative_evidence_refs"].append(row["observation_ref"])
                    state[cap]["confidence"] = max(state[cap]["confidence"], row["effective_confidence"])
            grouped[(row["observation_code"], tuple(sorted(row["capability_refs"])))].append(row)
        elif disp in {"LOW_CONFIDENCE_PROBE_REQUIRED", "AMBIGUITY_PROBE_REQUIRED"}:
            grouped[(row["observation_code"], tuple(sorted(row["capability_refs"])))].append(row)
            if row["probe_family"]:
                probes.add(row["probe_family"])
        elif disp == "IGNORED_INVALID_ITEM":
            grouped[("IGNORED:" + row["observation_code"], tuple(sorted(row["capability_refs"])))].append(row)
        elif disp == "SHARED_EXECUTION_ERROR_LOCALIZED":
            grouped[("SHARED:" + row["observation_code"], tuple(sorted(row["capability_refs"])))].append(row)

    for cap in state.values():
        cap["positive_evidence_refs"] = sorted(set(cap["positive_evidence_refs"]))
        cap["negative_evidence_refs"] = sorted(set(cap["negative_evidence_refs"]))
        p = bool(cap["positive_evidence_refs"])
        n = bool(cap["negative_evidence_refs"])
        cap["state"] = "MIXED" if p and n else "DEMONSTRATED" if p else "EVIDENCE_OF_DIFFICULTY" if n else "UNKNOWN"

    cases = []
    for idx, (key, rows) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0]), 1):
        code_key, caps = key
        first = rows[0]
        evidence_refs = sorted(r["observation_ref"] for r in rows)
        confidence = max(r["effective_confidence"] for r in rows)
        probe = first["probe_family"]
        raw_code = code_key.split(":", 1)[-1]
        if code_key.startswith("IGNORED:"):
            status = "IGNORED_INVALID_ITEM"
            probe = None
            rationale = "Upstream P-B/P-D source integrity or diagnostic-use state blocks learner-negative inference."
        elif code_key.startswith("SHARED:"):
            status = "HYPOTHESIS"
            probe = None
            rationale = "Shared arithmetic/algebra execution is localized outside Physics capability state."
        elif any(r["disposition"] in {"LOW_CONFIDENCE_PROBE_REQUIRED", "AMBIGUITY_PROBE_REQUIRED"} for r in rows):
            status = "PROBE_REQUIRED"
            rationale = "Evidence is ambiguous or below the confidence threshold; targeted probing is required."
            if probe:
                probes.add(probe)
        else:
            independent = {r["attempt_ref"] for r in rows}
            if len(independent) >= policy["confirmed_misconception_min_independent_negative_evidence"]:
                status = "CONFIRMED"
                probe = None
                rationale = "Independent high-confidence negative evidence meets the confirmation threshold."
            else:
                status = "PROBE_REQUIRED"
                rationale = "One negative observation is insufficient to confirm a misconception."
                if probe:
                    probes.add(probe)
        case = {
            "case_id": f"PHY-P-E-CASE-{idx:03d}-{raw_code}",
            "subject": "PHYSICS",
            "hypothesis_code": raw_code,
            "capability_refs": list(caps),
            "evidence_refs": evidence_refs,
            "status": status,
            "confidence": confidence,
            "probe_requirement": probe,
            "rationale": rationale,
        }
        validate_schema(case, SHARED / "diagnostic-case.schema.json")
        cases.append(case)

    return [state[k] for k in sorted(state)], cases, sorted(probes)

def build_snapshot(problem_semantics, question_set, registry, policy, attempts=None, ledger=None,
                   snapshot_id="PHY-P-E-SNAPSHOT"):
    codes = validate_registries(registry, policy)
    del codes  # coverage validation side effect only
    scope_ref, scope_digest = scope_fingerprint(problem_semantics)
    state_template = initial_capability_state(problem_semantics)

    if attempts is None:
        if ledger is not None:
            fail("EVIDENCE_PRESENT_WITHOUT_ATTEMPT_SET")
        snapshot = {
            "snapshot_id": snapshot_id,
            "subject": "PHYSICS",
            "assessment_scope_ref": scope_ref,
            "assessment_scope_digest": scope_digest,
            "attempt_mode": "ABSENT",
            "scope_unchanged": True,
            "support_policy": policy["no_attempt_support_policy"],
            "capability_states": [state_template[k] for k in sorted(state_template)],
            "diagnostic_cases": [],
            "probe_requirements": [policy["no_attempt_probe_requirement"]],
        }
        validate_schema(snapshot, SHARED / "learner-state-snapshot.schema.json")
        payload = {
            "snapshot": snapshot,
            "processed_evidence": [],
            "attempt_set_ref": None,
            "evidence_ledger_ref": None,
            "policy_ref": policy["policy_id"],
            "problem_semantics_ref": problem_semantics["package_id"],
        }
        return {**payload, "inference_digest": digest(payload)}

    if ledger is None:
        fail("ATTEMPT_PRESENT_WITHOUT_EVIDENCE_LEDGER")
    normalized, _ = validate_ledger(
        ledger, attempts, question_set, problem_semantics, registry, policy
    )
    states, cases, probes = reduce_normalized_records(state_template.keys(), normalized, policy)
    snapshot = {
        "snapshot_id": snapshot_id,
        "subject": "PHYSICS",
        "assessment_scope_ref": scope_ref,
        "assessment_scope_digest": scope_digest,
        "attempt_mode": "PRESENT",
        "scope_unchanged": True,
        "support_policy": policy["attempt_support_policy"],
        "capability_states": states,
        "diagnostic_cases": cases,
        "probe_requirements": probes,
    }
    validate_schema(snapshot, SHARED / "learner-state-snapshot.schema.json")
    payload = {
        "snapshot": snapshot,
        "processed_evidence": sorted(normalized, key=lambda row: row["observation_ref"]),
        "attempt_set_ref": attempts["attempt_set_id"],
        "evidence_ledger_ref": ledger["ledger_id"],
        "policy_ref": policy["policy_id"],
        "problem_semantics_ref": problem_semantics["package_id"],
    }
    return {**payload, "inference_digest": digest(payload)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--problem-semantics", required=True)
    ap.add_argument("--questions", required=True)
    ap.add_argument("--observation-registry", required=True)
    ap.add_argument("--diagnostic-policy", required=True)
    ap.add_argument("--attempts")
    ap.add_argument("--evidence")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    result = build_snapshot(
        load(args.problem_semantics),
        load(args.questions),
        load(args.observation_registry),
        load(args.diagnostic_policy),
        load(args.attempts) if args.attempts else None,
        load(args.evidence) if args.evidence else None,
    )
    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

if __name__ == "__main__":
    main()
