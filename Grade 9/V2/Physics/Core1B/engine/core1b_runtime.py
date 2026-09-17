from __future__ import annotations
import hashlib, json
from typing import Mapping, Sequence

ALLOWED_BASES={"LEARNER_RESPONSE","DIAGNOSTIC","TEACHER_OBSERVATION"}
FORBIDDEN_SURFACE=("ATOM_","DIAGNOSTIC_BRANCH","STATE_FRAGILE","REPAIR_","TRANSFER_READY")
BASE_REQUIREMENTS={"recognise","represent","first_move","finish","check"}
INDEPENDENT_HINTS={"NO_HINT","RETRIEVAL_CUE"}
SECURE_EVENT_KINDS={"ATOM_CHECK","INDEPENDENT_ATTEMPT","RETRIEVAL_ATTEMPT"}

class Core1BRuntimeError(ValueError): pass

def canonical(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(v): return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()
def digest_without(row,key):
    x=dict(row); x.pop(key,None); return digest(x)

def validate_authority(authority:Mapping)->None:
    if authority.get("release_state")!="RELEASED": raise Core1BRuntimeError("CORE1B_CORE1A_AUTHORITY_NOT_RELEASED")
    if authority.get("authority_digest")!=digest_without(authority,"authority_digest"): raise Core1BRuntimeError("CORE1B_CORE1A_AUTHORITY_DIGEST_MISMATCH")
    if not authority.get("authority_ref") or not authority.get("allowed_atom_refs"): raise Core1BRuntimeError("CORE1B_CORE1A_AUTHORITY_INCOMPLETE")

def atom_map(registry:Mapping):
    out={}
    for a in registry.get("atoms",[]):
        ref=a.get("atom_id")
        if not ref or ref in out: raise Core1BRuntimeError("CORE1B_ATOM_ID_INVALID")
        out[ref]=a
    if not out: raise Core1BRuntimeError("CORE1B_ATOM_REGISTRY_EMPTY")
    return out

def validate_registry(registry:Mapping)->None:
    atoms=atom_map(registry)
    for ref,a in atoms.items():
        for k in ("proposition","representation","micro_check","merge_target"):
            if not a.get(k): raise Core1BRuntimeError(f"CORE1B_ATOM_FIELD_MISSING:{ref}:{k}")
        for p in a.get("prerequisites",[]):
            if p not in atoms: raise Core1BRuntimeError(f"CORE1B_ATOM_PREREQUISITE_UNKNOWN:{ref}:{p}")
        for p in a.get("repair_routes",[]):
            if p not in atoms: raise Core1BRuntimeError(f"CORE1B_ATOM_REPAIR_UNKNOWN:{ref}:{p}")
    visiting=set(); visited=set()
    def visit(ref):
        if ref in visited:return
        if ref in visiting: raise Core1BRuntimeError("CORE1B_ATOM_PREREQUISITE_CYCLE:"+ref)
        visiting.add(ref)
        for p in atoms[ref].get("prerequisites",[]): visit(p)
        visiting.remove(ref); visited.add(ref)
    for ref in atoms: visit(ref)

def validate_event(event:Mapping, previous_events:Sequence[Mapping]=())->None:
    if event.get("basis") not in ALLOWED_BASES: raise Core1BRuntimeError("CORE1B_OBSERVED_EVIDENCE_BASIS_REQUIRED")
    if event.get("event_digest")!=digest_without(event,"event_digest"): raise Core1BRuntimeError("CORE1B_EVENT_DIGEST_MISMATCH")
    if len(str(event.get("evidence_digest","")))!=64: raise Core1BRuntimeError("CORE1B_EVIDENCE_DIGEST_REQUIRED")
    ids={e.get("event_id") for e in previous_events}
    seqs=[int(e.get("event_sequence",0)) for e in previous_events]
    if event.get("event_id") in ids: raise Core1BRuntimeError("CORE1B_EVENT_DUPLICATE")
    expected=(max(seqs) if seqs else 0)+1
    if event.get("event_sequence")!=expected: raise Core1BRuntimeError("CORE1B_EVENT_SEQUENCE_NOT_APPEND_ONLY")
    if event.get("supersedes_event_id") is not None and event.get("supersedes_event_id") not in ids: raise Core1BRuntimeError("CORE1B_SUPERSESSION_UNKNOWN_EVENT")

def _is_secure_observed_event(event:Mapping)->bool:
    return (
        event.get("basis") in ALLOWED_BASES
        and event.get("outcome")=="PASS"
        and event.get("event_kind") in SECURE_EVENT_KINDS
        and event.get("hint_level_used") in INDEPENDENT_HINTS
        and event.get("event_digest")==digest_without(event,"event_digest")
    )

def secure_atom_refs(events:Sequence[Mapping])->set[str]:
    secure=set()
    for e in events:
        if _is_secure_observed_event(e): secure.update(e.get("atom_refs") or [])
    return secure

def required_criteria(unit:Mapping, authority:Mapping)->set[str]:
    req=set(unit.get("readiness_requirements") or [])
    if not BASE_REQUIREMENTS <= req: raise Core1BRuntimeError("CORE1B_READINESS_REQUIREMENT_INCOMPLETE")
    if authority.get("model_validity_required") and "applicability" not in req: raise Core1BRuntimeError("CORE1B_APPLICABILITY_REQUIRED")
    if authority.get("explanation_required") and "explain" not in req: raise Core1BRuntimeError("CORE1B_EXPLAIN_REQUIRED")
    return req

def validate_unit(unit:Mapping,registry:Mapping,authority:Mapping,prior_events:Sequence[Mapping]=())->None:
    validate_authority(authority); validate_registry(registry)
    if unit.get("subject")!="PHYSICS": raise Core1BRuntimeError("CORE1B_SUBJECT_INVALID")
    b=unit.get("upstream_authority") or {}
    if b.get("core1a_release_ref")!=authority.get("authority_ref") or b.get("core1a_release_digest")!=authority.get("authority_digest"): raise Core1BRuntimeError("CORE1B_CORE1A_AUTHORITY_BINDING_MISMATCH")
    if unit.get("bucket_id")!=authority.get("bucket_id") or unit.get("capability_id")!=authority.get("capability_id"): raise Core1BRuntimeError("CORE1B_AUTHORITY_SCOPE_DRIFT")
    if unit.get("problem_family_ref") not in set(authority.get("problem_family_refs") or []): raise Core1BRuntimeError("CORE1B_PROBLEM_FAMILY_NOT_AUTHORIZED")
    if unit.get("model_validity_required")!=bool(authority.get("model_validity_required")) or unit.get("explanation_required")!=bool(authority.get("explanation_required")): raise Core1BRuntimeError("CORE1B_RELEASE_CRITERIA_DRIFT")
    atoms=atom_map(registry); included=set(unit.get("atom_refs") or []); allowed=set(authority.get("allowed_atom_refs") or [])
    if not included or not included <= set(atoms) or not included <= allowed: raise Core1BRuntimeError("CORE1B_ATOM_NOT_AUTHORIZED")
    secure=secure_atom_refs(prior_events)
    skips={x.get("atom_ref"):(x.get("event_ref"),x.get("event_digest")) for x in unit.get("prerequisite_skip_evidence") or []}
    event_by_ref={e.get("event_id"):e for e in prior_events}
    for ref in included:
        for p in atoms[ref].get("prerequisites",[]):
            if p in included: continue
            ev_ref,ev_digest=skips.get(p,(None,None)); ev=event_by_ref.get(ev_ref)
            if p not in secure or ev is None or ev.get("event_digest")!=ev_digest: raise Core1BRuntimeError(f"CORE1B_PREREQUISITE_SKIP_UNGROUNDED:{ref}:{p}")
    required_criteria(unit,authority)
    surface=unit.get("learner_surface") or {}; text="\n".join([*(surface.get("teacher_moves") or []),surface.get("worked_example",""),surface.get("faded_task",""),surface.get("independent_task","")]).upper()
    leaked=[t for t in FORBIDDEN_SURFACE if t in text]
    if leaked: raise Core1BRuntimeError("CORE1B_INTERNAL_LABEL_LEAK:"+",".join(leaked))

def derive_state(unit:Mapping,authority:Mapping,events:Sequence[Mapping])->str:
    req=required_criteria(unit,authority)
    relevant=[e for e in events if e.get("capability_id")==unit.get("capability_id") and e.get("problem_family_ref")==unit.get("problem_family_ref") and e.get("basis") in ALLOWED_BASES]
    if not relevant:return "NOT_EXPOSED"
    for e in relevant:
        if e.get("event_kind") in {"INDEPENDENT_ATTEMPT","RETRIEVAL_ATTEMPT"} and e.get("outcome")=="PASS" and e.get("hint_level_used") in INDEPENDENT_HINTS and all((e.get("criteria") or {}).get(k)=="PASS" for k in req): return "INDEPENDENT"
    return "SUPPORTED" if any(e.get("outcome") in {"PASS","PARTIAL"} for e in relevant) else "EXPOSED"

def build_release_receipt(unit:Mapping,registry:Mapping,authority:Mapping,events:Sequence[Mapping])->dict:
    validate_unit(unit,registry,authority,events)
    for i,e in enumerate(events): validate_event(e,events[:i])
    state=derive_state(unit,authority,events)
    if state!="INDEPENDENT": raise Core1BRuntimeError("CORE1B_OBSERVED_INDEPENDENT_EVIDENCE_REQUIRED")
    relevant=[e for e in events if e.get("capability_id")==unit.get("capability_id") and e.get("problem_family_ref")==unit.get("problem_family_ref")]
    reps=sorted({e.get("representation_used") for e in relevant if _is_secure_observed_event(e) and e.get("representation_used")})
    out={"schema_version":"1.0.0","receipt_id":"C1B-REL-"+unit["unit_id"],"learner_profile_ref":relevant[-1]["learner_profile_ref"],"capability_id":unit["capability_id"],"problem_family_ref":unit["problem_family_ref"],"core1a_release_ref":authority["authority_ref"],"core1a_release_digest":authority["authority_digest"],"state":"INDEPENDENT","observed_events":[{"event_ref":e["event_id"],"event_digest":e["event_digest"]} for e in relevant],"representation_evidence":reps,"unresolved_required_atoms":[],"semantics":"OBSERVED_INDEPENDENT_RELEASE_NOT_TRANSFER_LEGALITY"}
    out["receipt_digest"]=digest(out); return out
