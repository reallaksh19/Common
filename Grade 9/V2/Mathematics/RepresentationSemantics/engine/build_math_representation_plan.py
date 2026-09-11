#!/usr/bin/env python3
import argparse
import copy
import hashlib
import json
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value, omit=None):
    value = copy.deepcopy(value)
    if omit and isinstance(value, dict):
        value.pop(omit, None)
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()

def verify_digest(value, field, code):
    if value.get(field) != digest(value, field):
        raise ValueError(code)

def index_registry(registry):
    verify_digest(registry, "registry_digest", "TEACHING_PRIMITIVE_REGISTRY_DIGEST_MISMATCH")
    out = {}
    for p in registry["primitives"]:
        verify_digest(p, "primitive_digest", f"TEACHING_PRIMITIVE_DIGEST_MISMATCH:{p['primitive_id']}")
        if p["primitive_id"] in out:
            raise ValueError(f"DUPLICATE_TEACHING_PRIMITIVE:{p['primitive_id']}")
        out[p["primitive_id"]] = p
    return out

def index_profile(profile):
    verify_digest(profile, "profile_digest", "PAGE_INTENT_PROFILE_DIGEST_MISMATCH")
    out = {}
    for b in profile["requirement_bindings"]:
        ref = b["representation_requirement_ref"]
        if ref in out:
            raise ValueError(f"DUPLICATE_PAGE_INTENT_BINDING:{ref}")
        out[ref] = set(b["allowed_primitive_refs"])
    return out

def validate_spec(spec, context, primitives, bindings, profile):
    verify_digest(spec, "spec_digest", f"REPRESENTATION_SPEC_DIGEST_MISMATCH:{spec['representation_id']}")
    if spec["semantic_role"] != "INSTRUCTIONAL":
        raise ValueError(f"DECORATIVE_VISUAL_COUNTS_AS_REPRESENTATION_PASS:{spec['representation_id']}")
    if spec["surface_role"] != context["surface_role"]:
        raise ValueError(f"SURFACE_ROLE_MISMATCH:{spec['representation_id']}")
    if spec["capability_ref"] != context["capability_ref"]:
        raise ValueError(f"VISUAL_WITHOUT_CAPABILITY_BINDING:{spec['representation_id']}")
    family = spec.get("problem_family_ref")
    if family is not None and family not in set(context.get("problem_family_refs", [])):
        raise ValueError(f"REPRESENTATION_PROBLEM_FAMILY_OUT_OF_SCOPE:{spec['representation_id']}")
    req = spec["semantic_requirement_ref"]
    required = set(context["representation_requirements"])
    if req not in required:
        raise ValueError(f"REPRESENTATION_REQUIREMENT_OUT_OF_SCOPE:{req}")
    if req not in bindings:
        raise ValueError(f"UNRESOLVED_REPRESENTATION_REQUIREMENT:{req}")
    if spec["primitive_id"] not in primitives:
        raise ValueError(f"UNKNOWN_TEACHING_PRIMITIVE:{spec['primitive_id']}")
    if spec["primitive_id"] not in bindings[req]:
        raise ValueError(f"PRIMITIVE_NOT_ALLOWED_FOR_REQUIREMENT:{req}:{spec['primitive_id']}")
    primitive = primitives[spec["primitive_id"]]
    if spec["instructional_job"] not in primitive["supported_instructional_jobs"]:
        raise ValueError(f"PRIMITIVE_JOB_MISMATCH:{spec['representation_id']}")
    payload = spec["source_semantic_data"]["payload"]
    missing = [f for f in primitive["required_source_fields"] if f not in payload]
    if missing:
        raise ValueError(f"SOURCE_SEMANTIC_DATA_INCOMPLETE:{spec['representation_id']}:{','.join(missing)}")
    rc = spec["renderer_constraints"]
    if not rc["must_not_infer_mathematical_content"] or not rc["must_render_from_source_semantic_data"]:
        raise ValueError(f"RENDERER_INVENTS_UNDECLARED_MATH_MEANING:{spec['representation_id']}")
    required_constraints = set(primitive["renderer_constraints"])
    if not required_constraints.issubset(set(rc["layout_constraints"])):
        raise ValueError(f"RENDERER_CONSTRAINT_MISSING:{spec['representation_id']}")
    contrast = spec["instructional_job"] == "DISCRIMINATE_CASES" or spec.get("misconception_or_contrast_ref") is not None
    if contrast:
        if not primitive["supports_contrast"]:
            raise ValueError(f"CONTRAST_REQUIRED_BUT_SINGLE_CASE_VISUAL_USED:{spec['representation_id']}")
        missing_contrast = [f for f in primitive["contrast_source_fields"] if f not in payload]
        if missing_contrast:
            raise ValueError(f"CONTRAST_SOURCE_INCOMPLETE:{spec['representation_id']}:{','.join(missing_contrast)}")

def build(context, specs, registry, profile):
    primitives = index_registry(registry)
    bindings = index_profile(profile)
    required = sorted(set(context["representation_requirements"]))
    if not required:
        raise ValueError("REPRESENTATION_SCOPE_EMPTY")
    for req in required:
        if req not in bindings:
            raise ValueError(f"UNRESOLVED_REPRESENTATION_REQUIREMENT:{req}")
        unknown = sorted(x for x in bindings[req] if x not in primitives)
        if unknown:
            raise ValueError(f"PAGE_INTENT_REFERENCES_UNKNOWN_PRIMITIVE:{req}:{','.join(unknown)}")
    seen = set()
    for spec in specs:
        if spec["representation_id"] in seen:
            raise ValueError(f"DUPLICATE_REPRESENTATION_ID:{spec['representation_id']}")
        seen.add(spec["representation_id"])
        validate_spec(spec, context, primitives, bindings, profile)

    by_req = {r: [] for r in required}
    for spec in specs:
        by_req[spec["semantic_requirement_ref"]].append(spec["representation_id"])
    uncovered = [r for r, ids in by_req.items() if not ids]
    if uncovered:
        raise ValueError("REPRESENTATION_REQUIREMENT_UNCOVERED:" + ",".join(uncovered))

    pck_jobs = set(context.get("required_pck_jobs", []))
    contrast_job = profile["cross_cutting_rules"]["error_contrast_job_ref"]
    if contrast_job in pck_jobs and not any(s["instructional_job"] == profile["cross_cutting_rules"]["contrast_instructional_job"] for s in specs):
        raise ValueError("ERROR_CONTRAST_REQUIRED_BUT_NOT_REPRESENTED")
    verification_jobs = set(profile["cross_cutting_rules"]["verification_job_refs"])
    if verification_jobs.intersection(pck_jobs) and not any(s["instructional_job"] == profile["cross_cutting_rules"]["verification_instructional_job"] for s in specs):
        raise ValueError("VERIFICATION_REPRESENTATION_REQUIRED_BUT_MISSING")

    specs_sorted = sorted(specs, key=lambda x: x["representation_id"])
    input_payload = {
        "context": context,
        "spec_digests": [x["spec_digest"] for x in specs_sorted],
        "primitive_registry_digest": registry["registry_digest"],
        "page_intent_profile_digest": profile["profile_digest"],
    }
    out = {
        "representation_plan_id": "MATH-RPLAN-" + digest(input_payload)[:16],
        "schema_version": "1.0.0",
        "subject": "MATHEMATICS",
        "surface_role": context["surface_role"],
        "lesson_or_transfer_ref": context["lesson_or_transfer_ref"],
        "capability_ref": context["capability_ref"],
        "required_representation_refs": required,
        "coverage": [{"semantic_requirement_ref": r, "representation_ids": sorted(by_req[r])} for r in required],
        "representations": specs_sorted,
        "input_digest": digest(input_payload),
    }
    out["plan_digest"] = digest(out, "plan_digest")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--primitive-registry", required=True)
    ap.add_argument("--page-intent-profile", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    source = load(args.input)
    result = build(source["context"], source["representations"], load(args.primitive_registry), load(args.page_intent_profile))
    Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
