import argparse, copy, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

TREATMENTS = {"READY_VERIFY_ONLY","ACTIVE_STUDY","REPAIR_BEFORE","REPAIR_IN_UNIT","PROBE_FIRST"}
FUTURE_DIMENSIONS = [
    "acquisition","independent_reconstruction","delayed_retention","near_transfer",
    "far_transfer","mixed_model_discrimination","representation_translation","fluency","timed_performance",
]

def canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",",":"))

def digest(o, field=None):
    x = copy.deepcopy(o)
    if field:
        x.pop(field, None)
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def fail(code, detail=""):
    raise ValueError(f"{code}: {detail}" if detail else code)

def uniq(values):
    return sorted(set(values))

def validate_policy(policy):
    if policy.get("subject") != "PHYSICS" or policy.get("schema_version") != "1.0.0":
        fail("PHYSICS_TREATMENT_POLICY_IDENTITY")
    if policy.get("policy_digest") != digest(policy, "policy_digest"):
        fail("PHYSICS_TREATMENT_POLICY_DIGEST_MISMATCH")
    if policy.get("benchmark_inputs"):
        fail("BENCHMARK_PRODUCER_INPUT_FORBIDDEN")
    states = {"UNKNOWN", "DEMONSTRATED", "EVIDENCE_OF_DIFFICULTY", "MIXED"}
    if set(policy.get("state_to_treatment", {})) != states:
        fail("PHYSICS_TREATMENT_POLICY_STATE_COVERAGE")
    if set(policy.get("required_pck_jobs_by_treatment", {})) != TREATMENTS:
        fail("PHYSICS_TREATMENT_POLICY_TREATMENT_COVERAGE")
    if set(policy.get("priority_by_treatment", {})) != TREATMENTS:
        fail("PHYSICS_TREATMENT_POLICY_PRIORITY_COVERAGE")
    if policy.get("longitudinal_dimensions") != FUTURE_DIMENSIONS:
        fail("PHYSICS_LONGITUDINAL_DIMENSION_COVERAGE")
    if policy.get("current_success_may_close_future_obligations") is not False:
        fail("ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL", "policy")
    return True

def capability_map(authority):
    rows = authority["capabilities"]
    out = {x["capability_id"]: x for x in rows}
    if len(out) != len(rows):
        fail("DUPLICATE_SCOPE_CAPABILITY")
    return out

def transitive_prereqs(capability_ref, cmap, trail=None):
    trail = set(trail or ())
    if capability_ref in trail:
        fail("CAPABILITY_DEPENDENCY_CYCLE", capability_ref)
    if capability_ref not in cmap:
        fail("UNKNOWN_CAPABILITY", capability_ref)
    trail.add(capability_ref)
    out = set()
    for prereq in cmap[capability_ref]["prerequisite_capability_refs"]:
        if prereq not in cmap:
            fail("UNKNOWN_PREREQUISITE", prereq)
        out.add(prereq)
        out.update(transitive_prereqs(prereq, cmap, trail))
    return out

def learner_evidence_scope_fingerprint(problem_semantics):
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

def _binding_related_to_cap(binding, cap, closures):
    direct_caps = binding["canonical_capability_refs"]
    if cap in direct_caps:
        return True
    return any(cap in closures.get(direct, set()) for direct in direct_caps)
