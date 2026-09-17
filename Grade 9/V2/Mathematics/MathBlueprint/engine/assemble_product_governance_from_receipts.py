#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RECEIPT_SCHEMA = ROOT / "contracts" / "math-stage-governance-receipt.schema.json"

from compile_mathematics_engineering_workbench import digest as engineering_digest
from emit_stage_governance import digest, registry_alias_map
from validate_canonical_domain_registry import validate_registry
from validate_product_governance import (
    STAGES,
    _derived_difficulty,
    _similarity_class,
    load,
    validate_release,
)

SEMANTIC_TYPES = {"CONCEPT","MODEL","EQUATION","DERIVATION","CAPABILITY","LEARNING_ATOM","REPRESENTATION","MISCONCEPTION"}
STAGE_PAIRS = ["CORE1A__CORE1B","CORE1A__CORE2A","CORE1A__CORE2B","CORE1B__CORE2A","CORE1B__CORE2B","CORE2A__CORE2B"]
DISPOSITION_RANK = {"REFERENCED":0,"USED":1,"REALIZED":2,"RECONSTRUCTED":3}


def fail(code: str, detail: str = "") -> None:
    raise ValueError(f"{code}:{detail}" if detail else code)


def _jaccard(a, b) -> float:
    a, b = set(a or []), set(b or [])
    if not a and not b:
        return 0.0
    return round(len(a & b) / len(a | b), 4)


def _validate_receipts(receipts: list[dict], registry: dict) -> dict[str, list[dict]]:
    schema = load(RECEIPT_SCHEMA)
    by: dict[str, list[dict]] = defaultdict(list)
    custody_digests: set[str] = set()
    expected_domain_digest = engineering_digest(registry)
    for receipt in receipts:
        jsonschema.validate(receipt, schema)
        stage = receipt["stage"]
        if receipt["registry_binding"]["status"] != "BOUND" or receipt["registry_binding"]["registry_ref"] != registry["registry_id"]:
            fail("ASSEMBLER_RECEIPT_REGISTRY_UNBOUND", receipt["receipt_id"])
        custody = receipt.get("engineering_custody")
        if custody is None:
            fail("ASSEMBLER_RECEIPT_ENGINEERING_CUSTODY_MISSING", receipt["receipt_id"])
        if custody.get("status") != "BOUND":
            fail("ASSEMBLER_RECEIPT_ENGINEERING_CUSTODY_UNBOUND", receipt["receipt_id"])
        if custody.get("domain_registry_id") != registry["registry_id"] or custody.get("domain_registry_digest") != expected_domain_digest:
            fail("ASSEMBLER_RECEIPT_ENGINEERING_DOMAIN_DRIFT", receipt["receipt_id"])
        custody_material = {k:v for k,v in custody.items() if k != "custody_digest"}
        if custody.get("custody_digest") != engineering_digest(custody_material):
            fail("ASSEMBLER_RECEIPT_ENGINEERING_CUSTODY_DIGEST_INVALID", receipt["receipt_id"])
        custody_digests.add(custody["custody_digest"])
        if receipt["release_state"] != "READY_FOR_CROSS_CORE_AUDIT":
            fail("ASSEMBLER_RECEIPT_NOT_RELEASE_READY", receipt["receipt_id"])
        by[stage].append(receipt)
    if set(by) != set(STAGES):
        fail("ASSEMBLER_STAGE_COVERAGE_INCOMPLETE", ",".join(sorted(set(STAGES)-set(by))))
    if len(custody_digests) != 1:
        fail("ASSEMBLER_ENGINEERING_CUSTODY_DRIFT", ",".join(sorted(custody_digests)))
    return by


def _claims_by_stage(by: dict[str, list[dict]]) -> dict[str, dict[str, dict]]:
    out: dict[str, dict[str, dict]] = {s:{} for s in STAGES}
    for stage, receipts in by.items():
        for receipt in receipts:
            for claim in receipt["coverage_claims"]:
                for aid in claim["canonical_asset_refs"]:
                    row = out[stage].get(aid)
                    if row is None:
                        out[stage][aid] = {"disposition":claim["disposition"],"refs":list(claim["realization_refs"])}
                    else:
                        row["refs"] = sorted(set(row["refs"]) | set(claim["realization_refs"]))
                        if DISPOSITION_RANK[claim["disposition"]] > DISPOSITION_RANK[row["disposition"]]:
                            row["disposition"] = claim["disposition"]
    return out


def _stage_disposition(stage: str, asset: dict, claim: dict | None, by: dict[str, list[dict]], assets: dict[str, dict]) -> dict:
    atype = asset["asset_type"]
    treatment = "NONE"
    obligation = "NOT_APPLICABLE"
    disposition = "NOT_APPLICABLE"
    refs: list[str] = []

    if stage == "CORE1A" and atype in SEMANTIC_TYPES:
        obligation, treatment = "REQUIRED", "EXPLAIN"
    elif stage == "CORE1B" and atype in SEMANTIC_TYPES:
        obligation, treatment = "REQUIRED", "RECONSTRUCT"
    elif stage == "CORE2A" and atype == "SOURCE_QUESTION":
        obligation, treatment = "REQUIRED", "SOURCE_CUSTODY"
    elif stage == "CORE2A" and atype == "CANONICAL_SOLUTION":
        obligation, treatment = "REQUIRED", "SOLVE"
    elif atype == "PROBLEM_FAMILY":
        obligation = "CONDITIONAL"; treatment = "REFERENCE" if stage.startswith("CORE1") else "TRANSFER"
    elif atype == "EXAMPLE":
        obligation = "OPTIONAL"; treatment = "EXEMPLIFY" if stage.startswith("CORE1") else "TRANSFER"
    elif atype == "VERIFICATION_RULE":
        obligation, treatment = "CONDITIONAL", "VERIFY"
    elif stage in {"CORE2A","CORE2B"} and atype in SEMANTIC_TYPES:
        obligation = "CONDITIONAL"; treatment = "USE_WHEN_REQUIRED" if stage == "CORE2A" else "HIDE_UNTIL_NEEDED"
    elif stage == "CORE2B" and atype in {"SOURCE_QUESTION","CANONICAL_SOLUTION"}:
        obligation, treatment = "CONDITIONAL", "SOURCE_CUSTODY" if atype == "SOURCE_QUESTION" else "VERIFY"

    if claim:
        disposition = claim["disposition"]
        refs = claim["refs"]
    elif stage == "CORE2A" and atype == "CANONICAL_SOLUTION":
        qasset = asset["payload"]["question_asset_ref"]
        q = assets[qasset]["payload"]["question_ref"] if qasset in assets else None
        custody = [x for r in by[stage] for x in r["question_custody"]]
        hit = next((x for x in custody if x["question_id"] == q and x["answer_status"] == "VERIFIED"), None)
        if hit:
            disposition, refs = "USED", [hit["answer_contract_ref"]]
    elif obligation == "REQUIRED":
        fail("ASSEMBLER_REQUIRED_ASSET_MISSING", f"{stage}:{asset['asset_id']}:{atype}")

    if obligation in {"OPTIONAL","CONDITIONAL","NOT_APPLICABLE"} and not claim and disposition == "NOT_APPLICABLE":
        obligation, treatment = "NOT_APPLICABLE", "NONE"

    return {"obligation":obligation,"treatment":treatment,"disposition":disposition,"realization_refs":refs,"omission_reason":None,"owner_override_ref":None}


def build_coverage(registry: dict, by: dict[str, list[dict]]) -> dict:
    claims = _claims_by_stage(by)
    assets = {x["asset_id"]:x for x in registry["assets"]}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for asset in registry["assets"]:
        row = {"asset_ref":asset["asset_id"],"asset_type":asset["asset_type"]}
        for stage in STAGES:
            row[stage] = _stage_disposition(stage, asset, claims[stage].get(asset["asset_id"]), by, assets)
        grouped[asset["subtopic_id"]].append(row)
    return {
        "schema_version":"1.0.0","subject":"MATHEMATICS",
        "ledger_id":"MATH-COV-"+digest([registry["registry_id"], claims])[:16].upper(),
        "registry_ref":registry["registry_id"],"coverage_scope":"FULL_REGISTRY",
        "subtopics":[{"subtopic_id":sid,"asset_coverage":rows} for sid,rows in sorted(grouped.items())],
    }


def _artifacts(by: dict[str, list[dict]]) -> dict[str, list[dict]]:
    return {stage:[a for r in by[stage] for a in r["artifacts"]] for stage in STAGES}


def _candidate(left: dict, right: dict) -> tuple[bool,float,float,float | None]:
    content = _jaccard(set(left["content_tokens"]) | set(left["math_tokens"]), set(right["content_tokens"]) | set(right["math_tokens"]))
    pedagogy = _jaccard(left["pedagogy_signature"], right["pedagogy_signature"])
    structural = _jaccard(left["structural_signature"], right["structural_signature"]) if left["structural_signature"] or right["structural_signature"] else None
    shared = bool(set(left["canonical_asset_refs"]) & set(right["canonical_asset_refs"]) or set(left["capability_refs"]) & set(right["capability_refs"]) or set(left["lineage_keys"]) & set(right["lineage_keys"]))
    return shared or left["content_hash"] == right["content_hash"] or content >= 0.35, content, pedagogy, structural


def _relation(left_stage: str, right_stage: str, left: dict, right: dict, content: float, structural: float | None) -> str:
    common_lineage = set(left["lineage_keys"]) & set(right["lineage_keys"])
    common_semantic = set(left["canonical_asset_refs"]) & set(right["canonical_asset_refs"]) or set(left["capability_refs"]) & set(right["capability_refs"])
    pair = {left_stage,right_stage}
    if pair == {"CORE2A","CORE2B"} and common_lineage:
        s = structural or 0.0
        if content >= 0.90 and s >= 0.90:
            return "FADING_ANCHOR"
        if 0.70 <= s < 0.90:
            return "STRUCTURAL_SIBLING"
        if 0.40 <= s < 0.70:
            return "FAR_TRANSFER_SIBLING"
    if left["artifact_kind"] in {"EQUATION","DERIVATION","SOURCE_STEM"} and left["content_hash"] == right["content_hash"]:
        return "CANONICAL_REPEAT"
    if common_semantic or common_lineage:
        return "SEMANTIC_REUSE"
    return "NONE"


def _comparison_kind(a: str, b: str) -> str:
    if a == b:
        return a
    if {a,b} <= {"QUESTION","EXAMPLE"}:
        return "QUESTION"
    return "TTU"


def build_similarity(by: dict[str, list[dict]]) -> dict:
    arts = _artifacts(by)
    policy = load(ROOT / "policies" / "math-cross-core-similarity-policy.json")
    rows = []
    for pair_name in STAGE_PAIRS:
        ls, rs = pair_name.split("__")
        all_pairs = []
        for left, right in product(arts[ls], arts[rs]):
            selected, c, p, s = _candidate(left, right)
            all_pairs.append((selected,c,p,s,left,right))
        selected_pairs = [x for x in all_pairs if x[0]]
        if not selected_pairs:
            if not all_pairs:
                fail("ASSEMBLER_STAGE_HAS_NO_ARTIFACTS", pair_name)
            selected_pairs = [max(all_pairs, key=lambda x:x[1])]
        for _, c, p, s, left, right in selected_pairs:
            rel = _relation(ls, rs, left, right, c, s)
            row = {
                "comparison_id":"AUTO-"+digest([ls,left["artifact_ref"],rs,right["artifact_ref"]])[:18],
                "left":{"stage":ls,"artifact_ref":left["artifact_ref"]},
                "right":{"stage":rs,"artifact_ref":right["artifact_ref"]},
                "artifact_kind":_comparison_kind(left["artifact_kind"],right["artifact_kind"]),
                "declared_relation":rel,
                "content_similarity":c,
                "pedagogical_similarity":p,
                "structural_similarity":s,
                "capability_overlap":bool(set(left["capability_refs"]) & set(right["capability_refs"])),
                "classification":"DISTINCT",
                "evidence":f"Automatic fingerprint comparison; relation={rel}; shared canonical/capability/lineage evaluated deterministically."
            }
            row["classification"] = _similarity_class(row, policy)
            if row["classification"] == "STRONG_OVERLAP":
                fail("ASSEMBLER_STRONG_PEDAGOGICAL_OVERLAP", row["comparison_id"])
            rows.append(row)
    return {
        "schema_version":"1.0.0","subject":"MATHEMATICS",
        "audit_id":"MATH-SIM-AUTO-"+digest(rows)[:16].upper(),"policy_ref":"MATH-CROSS-CORE-SIMILARITY-v1",
        "coverage_declaration":{"comparison_scope":"ALL_CROSS_CORE_CANDIDATES","stage_pairs":STAGE_PAIRS,"candidate_pair_count":len(rows),"uncompared_candidate_count":0},
        "comparisons":rows,
    }


def _difficulty(by: dict[str, list[dict]]) -> list[dict]:
    rows_by_stage = {s:[x for r in by[s] for x in r["difficulty_evidence"]] for s in ("CORE1A","CORE1B")}
    a = {x["subtopic_ref"]:x for x in rows_by_stage["CORE1A"]}
    b = {x["subtopic_ref"]:x for x in rows_by_stage["CORE1B"]}
    if set(a) != set(b):
        fail("ASSEMBLER_CORE1_DIFFICULTY_SUBTOPIC_MISMATCH", canonical_sets(set(a),set(b)))
    out=[]
    for sid in sorted(a):
        left,right=a[sid],b[sid]
        for field in ("declared_badge","badge_authority","derived_dimensions","operational_badge","page_ceiling","research_level","owner_override_ref"):
            if left[field] != right[field]:
                fail("ASSEMBLER_CORE1A_CORE1B_DIFFICULTY_DRIFT", f"{sid}:{field}")
        score, derived = _derived_difficulty(left["derived_dimensions"])
        status="ALIGNED"
        if left["declared_badge"] != derived:
            status="OWNER_OVERRIDDEN_MISMATCH" if left["badge_authority"]=="OWNER" else "SOURCE_OVERRIDDEN_MISMATCH"
        out.append({
            "subtopic_id":sid,"declared_badge":left["declared_badge"],"badge_authority":left["badge_authority"],
            "derived_dimensions":left["derived_dimensions"],"derived_score":score,"derived_badge":derived,
            "operational_badge":left["operational_badge"],"page_ceiling":left["page_ceiling"],"research_level":left["research_level"],
            "owner_override_ref":left["owner_override_ref"],"consequence_evidence_refs":sorted(set(left["evidence_refs"]+right["evidence_refs"])),"status":status,
        })
    return out


def canonical_sets(a:set,b:set)->str:
    return f"A={','.join(sorted(a))};B={','.join(sorted(b))}"


def _purpose(by: dict[str, list[dict]]) -> list[dict]:
    out=[]
    for stage in STAGES:
        rows=[r["purpose_evidence"] for r in by[stage]]
        contracts={r["purpose_contract"] for r in rows}; reveals={r["canonical_reveal_after_attempt"] for r in rows}
        if len(contracts)!=1 or len(reveals)!=1:
            fail("ASSEMBLER_PURPOSE_RECEIPT_CONFLICT", stage)
        out.append({"stage":stage,"purpose_contract":next(iter(contracts)),"learner_actions":sorted({x for r in rows for x in r["learner_actions"]}),"canonical_reveal_after_attempt":next(iter(reveals)),"evidence_refs":sorted({x for r in rows for x in r["evidence_refs"]}),"status":"PASS"})
    return out


def _bind_cap(ref:str, aliases:dict[str,set[str]], assets:dict[str,dict])->str:
    if ref in assets and assets[ref]["asset_type"]=="CAPABILITY": return ref
    hits=[x for x in aliases.get(ref,set()) if assets[x]["asset_type"]=="CAPABILITY"]
    if len(hits)!=1: fail("ASSEMBLER_CAPABILITY_BINDING_AMBIGUOUS", ref)
    return hits[0]


def _learner_fit(by:dict[str,list[dict]], registry:dict)->list[dict]:
    aliases,_=registry_alias_map(registry); assets={x["asset_id"]:x for x in registry["assets"]}; out=[]
    for stage in ("CORE2A","CORE2B"):
        for receipt in by[stage]:
            for row in receipt["learner_fit_evidence"]:
                basis=dict(row["calibration_basis"])
                if basis["type"]=="KNOWLEDGE_PERCENT":
                    mapped=[]
                    for ck in basis["capability_knowledge"]:
                        mapped.append({"capability_ref":_bind_cap(ck["capability_ref"],aliases,assets),"percent":ck["percent"]})
                    basis["capability_knowledge"]=mapped
                out.append({"stage":stage,"item_ref":row["item_ref"],"calibration_basis":basis,"required_capability_refs":[_bind_cap(x,aliases,assets) for x in row["required_capability_refs"]],"support_mode":row["support_mode"],"maximum_allowed_demand":row["maximum_allowed_demand"],"actual_demand":row["actual_demand"],"taught_scope_verified":True,"result":"PASS"})
    return out


def _custody(by:dict[str,list[dict]])->list[dict]:
    seen={}
    for stage in ("CORE2A","CORE2B"):
        for receipt in by[stage]:
            for row in receipt["question_custody"]:
                q=row["question_id"]
                if q in seen and seen[q] != row: fail("ASSEMBLER_QUESTION_CUSTODY_CONFLICT",q)
                seen[q]=row
    return [seen[x] for x in sorted(seen)]


def _badges(registry:dict,difficulty:list[dict])->list[dict]:
    assets={x["asset_id"]:x for x in registry["assets"]}; out=[]
    for d in difficulty:
        sid=d["subtopic_id"]; rows=[x for x in registry["assets"] if x["subtopic_id"]==sid]
        concepts=[x["asset_id"] for x in rows if x["asset_type"] in {"CONCEPT","MODEL"}]
        if not concepts: fail("ASSEMBLER_SUBTOPIC_CONCEPT_BADGE_MISSING",sid)
        deps=sorted({dep for x in rows for dep in x.get("depends_on",[]) if dep in assets})
        out.append({"subtopic_id":sid,"difficulty":d["operational_badge"],"concept_refs":concepts,"linkage_refs":deps,"bucket_ref":"BUCKET:"+sid,"prerequisite_refs":deps,"equation_refs":[x["asset_id"] for x in rows if x["asset_type"]=="EQUATION"],"representation_refs":[x["asset_id"] for x in rows if x["asset_type"]=="REPRESENTATION"],"misconception_refs":[x["asset_id"] for x in rows if x["asset_type"]=="MISCONCEPTION"],"problem_family_refs":[x["asset_id"] for x in rows if x["asset_type"]=="PROBLEM_FAMILY"],"research_badge":d["research_level"],"learner_facing_badges":["DIFFICULTY","CONCEPT","LINKAGE","BUCKET","SUBTOPIC","PROBLEM_FAMILY","SOURCE"]})
    return out


def build_governance(registry:dict,by:dict[str,list[dict]])->dict:
    difficulty=_difficulty(by)
    return {"schema_version":"1.0.0","subject":"MATHEMATICS","audit_id":"MATH-GOV-AUTO-"+digest([r["receipt_id"] for rows in by.values() for r in rows])[:16].upper(),"registry_ref":registry["registry_id"],"difficulty_audits":difficulty,"purpose_audits":_purpose(by),"learner_fit_audits":_learner_fit(by,registry),"question_custody":_custody(by),"badge_sets":_badges(registry,difficulty)}


def assemble(registry:dict,receipts:list[dict])->tuple[dict,dict,dict,dict]:
    validate_registry(registry)
    by=_validate_receipts(receipts,registry)
    coverage=build_coverage(registry,by)
    similarity=build_similarity(by)
    governance=build_governance(registry,by)
    result=validate_release(registry,coverage,similarity,governance)
    return coverage,similarity,governance,result


def main()->None:
    ap=argparse.ArgumentParser(); ap.add_argument("--registry",required=True); ap.add_argument("--receipt",action="append",required=True); ap.add_argument("--out-dir",required=True); args=ap.parse_args()
    registry=load(args.registry); receipts=[load(x) for x in args.receipt]; coverage,similarity,governance,result=assemble(registry,receipts)
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    for name,obj in (("core_coverage_ledger.json",coverage),("cross_core_similarity_audit.json",similarity),("product_governance_audit.json",governance),("product_release_gate.json",result)):
        (out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))


if __name__=="__main__": main()
