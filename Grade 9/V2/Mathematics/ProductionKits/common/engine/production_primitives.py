#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
from typing import Any

PURPOSES = ("STARTER", "PRACTICE", "REVISION", "COMPETITION")
REPRESENTATION_PURPOSES = PURPOSES + ("CORE1A_TEACHING",)
REPRESENTATION_STAGES = (
    "SEE_THE_OBJECT","SEPARATE_THE_PARTS","SHOW_INFORMATION_FLOW","MAP_TO_SYMBOLS",
    "REBUILD_THE_MODEL","CHECK_UNDERSTANDING","CONNECT_TO_CORE2",
)
CORE2A_PURPOSE_PROMPT = "Is this for Starter, Practice, Revision, or Competition?"

def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value: Any, omit: str | None = None) -> str:
    item = copy.deepcopy(value)
    if omit and isinstance(item, dict): item.pop(omit, None)
    return hashlib.sha256(canonical(item).encode("utf-8")).hexdigest()

def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)

def route_task(intent: dict) -> dict:
    stage = intent.get("requested_stage")
    if stage not in {"CORE1","CORE1A","CORE2","CORE2A"}: fail("TASK_ROUTER_UNKNOWN_STAGE", str(stage))
    purpose = intent.get("purpose")
    if stage == "CORE2A" and purpose not in PURPOSES:
        return {"status":"NEEDS_USER_INPUT","code":"CORE2A_USER_PURPOSE_REQUIRED","question":CORE2A_PURPOSE_PROMPT,"allowed_answers":list(PURPOSES)}
    if stage != "CORE2A" and purpose is not None:
        fail("TASK_ROUTER_PURPOSE_NOT_APPLICABLE", f"{stage}:{purpose}")
    return {"status":"ROUTED","stage":stage,"purpose":purpose,"scope":copy.deepcopy(intent.get("scope") or {})}

def validate_source_bundle(bundle: dict, required_roles: set[str]) -> dict:
    if bundle.get("subject") != "MATHEMATICS": fail("SOURCE_BUNDLE_NON_MATH")
    by_role = {}
    for item in bundle.get("authority_items") or []:
        role=item.get("role"); by_role.setdefault(role,[]).append(item)
        if item.get("required") and (not item.get("ref") or not item.get("digest")): fail("SOURCE_BUNDLE_REQUIRED_BINDING_MISSING", str(role))
        d=item.get("digest")
        if d is not None and (len(d)!=64 or any(ch not in "0123456789abcdef" for ch in d)): fail("SOURCE_BUNDLE_DIGEST_INVALID", str(role))
    missing=sorted(r for r in required_roles if not by_role.get(r))
    if missing: fail("SOURCE_BUNDLE_ROLE_MISSING", ",".join(missing))
    dup=sorted(r for r,v in by_role.items() if len(v)>1)
    if dup: fail("SOURCE_BUNDLE_DUPLICATE_ROLE", ",".join(dup))
    return bundle

def authority_item(bundle: dict, role: str) -> dict:
    rows=[x for x in bundle.get("authority_items",[]) if x.get("role")==role]
    if len(rows)!=1: fail("SOURCE_BUNDLE_ROLE_MISSING", role)
    return rows[0]

def validate_bound_object(bundle: dict, role: str, obj: dict, *, ref_fields: tuple[str,...]=(), digest_fields: tuple[str,...]=()) -> None:
    row=authority_item(bundle,role)
    if row.get("ref") is not None and ref_fields:
        actual_ref=next((obj.get(k) for k in ref_fields if obj.get(k) is not None),None)
        if actual_ref != row.get("ref"): fail("SOURCE_BUNDLE_REF_MISMATCH", f"{role}:{actual_ref}!={row.get('ref')}")
    if row.get("digest") is not None:
        if row.get("digest_kind") == "CANONICAL_JSON_SHA256": actual_digest=digest(obj)
        else: actual_digest=next((obj.get(k) for k in digest_fields if obj.get(k) is not None),None)
        if actual_digest != row.get("digest"): fail("SOURCE_BUNDLE_DIGEST_MISMATCH", f"{role}:{actual_digest}!={row.get('digest')}")

def load_scaffold_profiles(path: str|Path) -> dict[str,dict]:
    data=json.loads(Path(path).read_text(encoding="utf-8")); out={}
    for row in data.get("profiles") or []:
        purpose=row["purpose"]
        if purpose in out: fail("SCAFFOLD_PROFILE_DUPLICATE",purpose)
        out[purpose]=row
    if set(out)!=set(PURPOSES): fail("SCAFFOLD_PROFILE_COVERAGE_DRIFT", ",".join(sorted(set(PURPOSES)-set(out))))
    return out

def build_scaffold_plan(purpose: str, profiles: dict[str,dict], bucket_ref: str) -> dict:
    if purpose not in profiles: fail("SCAFFOLD_PROFILE_MISSING",purpose)
    row=copy.deepcopy(profiles[purpose])
    return {"scaffold_plan_id":"MATH-SCF-"+digest({"purpose":purpose,"bucket":bucket_ref,"profile":row})[:16],"purpose":purpose,"bucket_ref":bucket_ref,"profile_id":row["profile_id"],"settings":row["settings"]}

def build_learning_representation(*,bucket_ref:str,purpose:str,stage_inputs:dict[str,dict],required_atom_refs:list[str]) -> dict:
    if purpose not in REPRESENTATION_PURPOSES: fail("REPRESENTATION_UNKNOWN_PURPOSE",purpose)
    stages=[]; covered=set()
    for stage in REPRESENTATION_STAGES:
        row=copy.deepcopy(stage_inputs.get(stage) or {}); status=row.get("status")
        if status not in {"REQUIRED","NOT_APPLICABLE"}: fail("REPRESENTATION_STAGE_MISSING",stage)
        if status=="NOT_APPLICABLE":
            if not str(row.get("not_applicable_reason") or "").strip(): fail("REPRESENTATION_NOT_APPLICABLE_REASON_MISSING",stage)
            content=row.get("content") or "Not applicable for this bucket."
        else:
            content=str(row.get("content") or "").strip()
            if not content: fail("REPRESENTATION_CONTENT_MISSING",stage)
        atom_refs=list(dict.fromkeys(row.get("atom_refs") or [])); covered.update(atom_refs)
        stages.append({"stage":stage,"status":status,"learner_job":str(row.get("learner_job") or stage.replace("_"," ").title()),"content":content,"atom_refs":atom_refs,"not_applicable_reason":row.get("not_applicable_reason")})
    missing=sorted(set(required_atom_refs)-covered)
    if missing: fail("REPRESENTATION_REQUIRED_ATOM_MISSING", ",".join(missing))
    payload={"bucket_ref":bucket_ref,"purpose":purpose,"stages":stages,"covered_atom_refs":sorted(covered),"status":"PASS"}
    payload["representation_id"]="MATH-REP-"+digest(payload)[:16]
    return payload

def validate_learning_representation(plan: dict, required_atom_refs: list[str]) -> None:
    actual=[x.get("stage") for x in plan.get("stages") or []]
    if actual != list(REPRESENTATION_STAGES): fail("REPRESENTATION_SEQUENCE_BROKEN", ",".join(str(x) for x in actual))
    missing=sorted(set(required_atom_refs)-set(plan.get("covered_atom_refs") or []))
    if missing: fail("REPRESENTATION_REQUIRED_ATOM_MISSING", ",".join(missing))
    for row in plan.get("stages") or []:
        if row.get("status")=="REQUIRED" and not str(row.get("content") or "").strip(): fail("REPRESENTATION_CONTENT_MISSING",row.get("stage", ""))
        if row.get("status")=="NOT_APPLICABLE" and not str(row.get("not_applicable_reason") or "").strip(): fail("REPRESENTATION_NOT_APPLICABLE_REASON_MISSING",row.get("stage", ""))

def validate_answer_contract(answer: dict) -> None:
    if answer.get("independent_solver_status") != "PASS": fail("ANSWER_INDEPENDENT_SOLVER_NOT_PASS", answer.get("question_ref", ""))
    if not answer.get("solution_paths"): fail("ANSWER_SOLUTION_PATH_MISSING", answer.get("question_ref", ""))
    checks=answer.get("verification_checks") or []
    if not checks: fail("ANSWER_VERIFICATION_MISSING", answer.get("question_ref", ""))
    for c in checks:
        if c.get("status") != "PASS": fail("ANSWER_VERIFICATION_FAILED", answer.get("question_ref", ""))
    if answer.get("solution_multiplicity")=="UNDERDETERMINED" and answer.get("canonical_answer") not in (None,"",[],{}): fail("ANSWER_UNDERDETERMINED_HAS_CANONICAL_VALUE", answer.get("question_ref", ""))

def validate_provenance(prov: dict, purpose: str|None=None) -> None:
    citations=prov.get("citations") or []
    if not prov.get("display_inline"): fail("QUESTION_CITATION_NOT_INLINE")
    if not citations: fail("QUESTION_CITATION_MISSING")
    if prov.get("question_origin")=="GENERATED_ORIGINAL":
        if prov.get("official_past_question_claim"): fail("GENERATED_ITEM_FALSE_OFFICIAL_ATTRIBUTION")
        if not any(c.get("text_relation")=="FRESH_ORIGINAL" for c in citations): fail("GENERATED_ITEM_ORIGIN_DISCLOSURE_MISSING")
    if purpose!="COMPETITION" and any(c.get("citation_kind")=="COMPETITION_BENCHMARK" for c in citations): fail("COMPETITION_BENCHMARK_OUTSIDE_COMPETITION_MODE",str(purpose))
    for c in citations:
        if c.get("citation_kind")=="COMPETITION_BENCHMARK":
            if c.get("use") not in {"STYLE_BENCHMARK","ARCHETYPE_DERIVATION"}: fail("COMPETITION_SOURCE_ROLE_UNCLEAR")
            if c.get("text_relation") not in {"STYLE_ONLY","ARCHETYPE_ONLY"}: fail("COMPETITION_SOURCE_RELATION_INVALID")

def build_blueprint_id(payload: dict) -> str:
    return "MATH-BP-"+digest(payload)[:16]
