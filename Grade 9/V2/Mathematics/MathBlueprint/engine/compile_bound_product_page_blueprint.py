#!/usr/bin/env python3
"""Compile real bound producer outputs into one content-complete LearnerPageBlueprint.

This is a publication compiler, not an author. It may classify and compose content
that already exists in Core1A/Core1B/Core2A/Core2B outputs; it may not invent new
learner mathematics, examples, hints or answers. The first production slice is
intentionally fail-closed for mixed intrinsic-difficulty runs. That keeps the
publication proof honest while the per-bucket multi-badge publication bundle is
implemented separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from blueprint_common import fail, load
from validate_content_complete_page_blueprint import validate_content_complete_blueprint, digest as content_digest

POLICY_PATH = HERE.parent / "policies" / "math-technical-composition-policy.json"


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sig(nodes: list[dict]) -> str:
    return "sig-" + digest(nodes)[:20]


def clean_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9-]+", "-", str(value)).strip("-")[:72]


def node(ntype: str, text: object) -> dict:
    value = str(text or "").strip()
    if not value:
        fail("MATH_BLUEPRINT_EMPTY_RENDER_NODE", ntype)
    return {"type": ntype, "text": value}


def block(block_id: str, kind: str, role: str, refs: list[str], nodes: list[dict], *, upstream=None, transform="BUILD", authority_refs=None) -> dict:
    if not refs:
        fail("MATH_BLUEPRINT_BLOCK_MATH_REFS_REQUIRED", block_id)
    auth = [str(x) for x in (authority_refs or refs) if str(x).strip()]
    if not auth:
        fail("MATH_BLUEPRINT_BLOCK_AUTHORITY_REQUIRED", block_id)
    return {
        "block_id": block_id,
        "kind": kind,
        "content_role": role,
        "content_signature": sig(nodes),
        "math_refs": list(dict.fromkeys(refs)),
        "upstream_ref": upstream,
        "transformation": transform,
        "authority_refs": list(dict.fromkeys(auth)),
        "render_nodes": nodes,
        "render_digest": content_digest(nodes),
    }


def prose(block_id: str, role: str, refs: list[str], nodes: list[dict], *, upstream=None, transform="BUILD", authority_refs=None) -> dict:
    row = block(block_id, "_PROSE", role, refs, nodes, upstream=upstream, transform=transform, authority_refs=authority_refs)
    row.pop("kind")
    return row


def representation(rep_id: str, refs: list[str], visible: list[str], not_imply: list[str], kind="SYMBOL_MAP") -> dict:
    return {
        "representation_id": rep_id,
        "kind": kind,
        "math_refs": list(dict.fromkeys(refs)),
        "semantic_geometry_refs": ["governed-mathematical-object", "relation-map"],
        "must_make_visible": [str(x) for x in visible if str(x).strip()] or ["The governed mathematical relationship between the referenced quantities."],
        "must_not_imply": [str(x) for x in not_imply if str(x).strip()] or ["A representation may not replace the governing mathematical conditions."],
        "clip_to_viewport": True,
        "viewport": {"x": 0.08, "y": 0.12, "width": 0.84, "height": 0.24},
    }


def ttu(ttu_id: str, refs: list[str], prompt: str, completed_ref: str, verification_ref: str, *, source=None, transform="BUILD", fading="GUIDED") -> dict:
    return {
        "ttu_id": ttu_id,
        "kind": "PROOF_CHAIN",
        "math_refs": list(dict.fromkeys(refs)),
        "source_ttu_ref": source,
        "lineage_transform": transform,
        "fading_level": fading,
        "reconstructable": True,
        "given_parts": [{"part_id": "GIVEN", "semantic_role": "problem_or_known_structure", "content_ref": completed_ref}],
        "missing_parts": [{"part_id": "MISSING", "semantic_role": "next_mathematical_structure", "content_ref": completed_ref}],
        "target_relations": ["Reconstruct the governed relation or reasoning chain before checking the completion."],
        "reconstruction_prompt": prompt,
        "completion_key": {"completed_parts": [{"part_id": "MISSING", "completed_content_ref": completed_ref}], "final_check": "Use the governed answer/check object referenced by this TTU."},
        "verification_refs": [verification_ref],
        "clip_to_viewport": True,
        "viewport": {"x": 0.08, "y": 0.40, "width": 0.84, "height": 0.24},
    }


def page(page_id: str, stage: str, page_kind: str, purpose: str, technical: list[dict], prose_blocks: list[dict], reps: list[dict], ttus: list[dict], workspaces=None) -> dict:
    return {
        "page_id": page_id,
        "stage": stage,
        "page_kind": page_kind,
        "page_purpose": purpose,
        "pagination": {"mode": "FLOW", "break_reason": None, "manual_spacers_used": False},
        "technical_blocks": technical,
        "prose_blocks": prose_blocks,
        "representations": reps,
        "reconstructable_ttus": ttus,
        "workspace_blocks": workspaces or [],
    }


def _unit_authority(unit: dict, cap: str) -> list[str]:
    trace = unit.get("source_trace") or {}
    out = [cap, str(trace.get("core1_lesson_ref") or "")]
    out.extend(trace.get("pck_asset_refs") or [])
    out.append(str(unit.get("family_ref") or ""))
    return [x for x in out if x]


def _practice(unit: dict, *roles: str) -> dict | None:
    for role in roles:
        row = (unit.get("practice") or {}).get(role)
        if row:
            return row
    return None


def compile_core1a_pages(book: dict) -> tuple[list[dict], dict[str, str], dict[str, dict]]:
    pages = []
    ttu_by_bucket = {}
    unit_by_cap = {}
    for bi, bucket in enumerate(book["buckets"], 1):
        bid = bucket["bucket_id"]
        caps = list(bucket["member_capability_refs"])
        tech = []
        prose_rows = []
        visible = []
        verification_ref = None
        ttu_prompt = None
        ttu_completion = None
        ttu_refs = list(caps)
        for ui, unit in enumerate(bucket["capability_units"], 1):
            cap = unit["capability_ref"]
            unit_by_cap[cap] = unit
            auth = _unit_authority(unit, cap)
            prefix = f"C1A-{bi:02d}-{ui:02d}"
            intro_nodes = [node("HEADING", unit.get("title") or bucket["title"]), node("PARAGRAPH", unit.get("opening") or unit.get("concept_explanation") or bucket["bucket_invariant"]["text"])]
            if unit.get("concept_explanation"):
                intro_nodes.append(node("PARAGRAPH", unit["concept_explanation"]))
            for x in unit.get("what_to_notice") or []:
                intro_nodes.append(node("BULLET", x)); visible.append(x)
            if unit.get("why_it_works"):
                for x in unit["why_it_works"]:
                    intro_nodes.append(node("STEP", x))
            tech.append(block(prefix+"-MODEL", "CASE_ANALYSIS", "DERIVED_MATHEMATICS", [cap], intro_nodes, authority_refs=auth))

            for ei, ex in enumerate(unit.get("worked_examples") or [], 1):
                ex_nodes = [node("QUESTION", ex["prompt"])] + [node("STEP", x) for x in ex.get("steps") or []] + [node("ANSWER", ex["answer"])]
                tech.append(block(prefix+f"-EX{ei}", "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", [cap], ex_nodes, authority_refs=auth+[f"CORE1A_AUTHORED_INSTANCE:{unit['lesson_id']}:WORKED:{ei}"]))
                if ttu_prompt is None:
                    ttu_prompt = ex["prompt"]; ttu_completion = prefix+f"-EX{ei}"

            if unit.get("common_mistake"):
                wrong_nodes = [node("PARAGRAPH", unit["common_mistake"])] + [node("STEP", x) for x in unit.get("repair") or []]
                tech.append(block(prefix+"-COUNTER", "COUNTEREXAMPLE", "DERIVED_MATHEMATICS", [cap], wrong_nodes, authority_refs=auth))

            verify_nodes = [node("CHECK", x) for x in unit.get("verification") or []]
            if verify_nodes:
                verification_ref = prefix+"-VERIFY"
                tech.append(block(verification_ref, "VERIFICATION", "ANSWER_IDENTITY", [cap], verify_nodes, authority_refs=auth))

            practice = _practice(unit, "GUIDED", "FADED", "INDEPENDENT", "TRANSFER", "VERIFY")
            if practice and ttu_prompt is None:
                p_nodes = [node("QUESTION", practice["prompt"])] + [node("HINT", x) for x in practice.get("hints") or []] + [node("ANSWER", practice["answer"])]
                pid = prefix+"-PRACTICE"
                tech.append(block(pid, "WORKED_EXAMPLE", "DERIVED_MATHEMATICS", [cap], p_nodes, authority_refs=auth+[f"CORE1A_AUTHORED_INSTANCE:{unit['lesson_id']}:PRACTICE"]))
                ttu_prompt = practice["prompt"]; ttu_completion = pid

        if not tech:
            fail("MATH_BLUEPRINT_CORE1A_BUCKET_EMPTY", bid)
        if ttu_prompt is None or ttu_completion is None:
            fail("MATH_BLUEPRINT_CORE1A_RECONSTRUCTION_SOURCE_MISSING", bid)
        if verification_ref is None:
            verification_ref = tech[-1]["block_id"]
        rep_id = f"REP-C1A-{bi:02d}"
        tid = f"TTU-C1A-{bi:02d}"
        tt = ttu(tid, caps, ttu_prompt, ttu_completion, verification_ref, source=None, transform="BUILD", fading="GUIDED")
        ttu_by_bucket[bid] = tid
        pages.append(page(f"C1A-P{bi:02d}", "CORE1A", "TEACHING", f"Teach the governed mathematical structure for {bucket['title']} from the bound Core1A manuscript.", tech, prose_rows, [representation(rep_id, caps, visible or [bucket["bucket_invariant"]["text"]], ["Do not treat a visual or symbolic shortcut as valid outside its governed conditions."])], [tt]))
    return pages, ttu_by_bucket, unit_by_cap


def load_core1b_plans(root: Path, bucket_titles: list[str]) -> dict[str, dict]:
    plans = [load(p) for p in sorted(root.glob("bucket-*-plan.json"))]
    if len(plans) != len(bucket_titles):
        fail("MATH_BLUEPRINT_CORE1B_PLAN_COUNT_DRIFT", f"{len(plans)}!={len(bucket_titles)}")
    remaining = list(plans)
    out = {}
    for title in bucket_titles:
        expected = "reconstruction — " + title.strip().lower()
        matches = [p for p in remaining if str(p.get("title", "")).strip().lower() == expected]
        if len(matches) != 1:
            fail("MATH_BLUEPRINT_CORE1B_BUCKET_BINDING_AMBIGUOUS", title)
        out[title] = matches[0]
        remaining.remove(matches[0])
    return out


def compile_core1b_pages(bucket_plan: dict, plans_by_title: dict[str, dict], c1a_ttu_by_bucket: dict[str, str]) -> tuple[list[dict], dict[str, str]]:
    pages=[]; ttu_by_bucket={}
    for bi,bucket in enumerate(bucket_plan["buckets"],1):
        bid=bucket["bucket_id"]; caps=list(bucket["member_capability_refs"]); plan_doc=plans_by_title[bucket["title"]]
        by_kind={row["kind"]:row for row in plan_doc["blocks"]}
        source = by_kind.get("COMPLETION") or by_kind.get("FADED") or by_kind.get("CLOSE_INDEPENDENT")
        answer = by_kind.get("ANSWER_CHECK")
        if source is None or answer is None:
            fail("MATH_BLUEPRINT_CORE1B_RECONSTRUCTION_OR_ANSWER_MISSING", bid)
        open_nodes=[node("QUESTION", source.get("learner_text") or source.get("title"))]
        open_nodes += [node("MATH", x) for x in source.get("math_lines") or []]
        frame=source.get("self_guided_frame") or {}
        for label in frame.get("help_sequence") or []:
            txt=(frame.get("help") or {}).get(label)
            if txt: open_nodes.append(node("HINT", txt))
        answer_nodes=[node("ANSWER", answer.get("learner_text") or answer.get("title"))] + [node("MATH", x) for x in answer.get("math_lines") or []]
        contrast=by_kind.get("METHOD_COMPARISON") or by_kind.get("ERROR_CONTRAST")
        contrast_nodes=[node("PARAGRAPH", contrast.get("learner_text"))] + [node("MATH", x) for x in contrast.get("math_lines") or []] if contrast else [node("PARAGRAPH", source.get("learner_text"))]
        open_id=f"C1B-{bi:02d}-OPEN"; work_id=f"C1B-{bi:02d}-WORK"; answer_id=f"C1B-{bi:02d}-ANSWER"; verify_id=f"C1B-{bi:02d}-VERIFY"; contrast_id=f"C1B-{bi:02d}-CONTRAST"
        auth=[plan_doc["source_core1a_authority_ref"], *caps]
        tech=[
            block(open_id,"OPEN_TASK","INSTRUCTION",caps,open_nodes,upstream=None,transform="RECONSTRUCT",authority_refs=auth),
            block(work_id,"TECHNICAL_WORKSPACE","INSTRUCTION",caps,[node("PARAGRAPH",source.get("learner_text") or source.get("title"))],upstream=open_id,transform="RECONSTRUCT",authority_refs=auth),
            block(contrast_id,"COUNTEREXAMPLE","DERIVED_MATHEMATICS",caps,contrast_nodes,upstream=open_id,transform="CONTRAST",authority_refs=auth),
            block(answer_id,"ANSWER_DERIVATION","DERIVED_MATHEMATICS",caps,answer_nodes,upstream=open_id,transform="VERIFY",authority_refs=auth),
            block(verify_id,"VERIFICATION","ANSWER_IDENTITY",caps,[node("CHECK",answer.get("learner_text") or answer.get("title"))],upstream=answer_id,transform="VERIFY",authority_refs=auth),
        ]
        tid=f"TTU-C1B-{bi:02d}"; ttu_by_bucket[bid]=tid
        tt=ttu(tid,caps,source.get("learner_text") or source.get("title"),answer_id,verify_id,source=c1a_ttu_by_bucket[bid],transform="RECONSTRUCT",fading="FADED")
        visible=[frame.get("reconstruction_focus") or source.get("learner_text")]
        pages.append(page(f"C1B-P{bi:02d}","CORE1B","OPEN_TUTOR",f"Reconstruct the governed concept for {bucket['title']} before checking the canonical completion.",tech,[],[representation(f"REP-C1B-{bi:02d}",caps,visible,["Do not reveal the completed route before the learner attempts reconstruction."])],[tt],[{"workspace_id":f"WS-C1B-{bi:02d}","purpose":"RECONSTRUCTION","math_refs":caps}]))
    return pages,ttu_by_bucket


def _wrong_route_for_caps(caps:list[str],unit_by_cap:dict[str,dict])->str:
    for cap in caps:
        txt=str((unit_by_cap.get(cap) or {}).get("common_mistake") or "").strip()
        if txt:return txt
    return "The governed producer did not emit a misconception route for these capabilities."


def compile_core2a_pages(bp:dict,unit_by_cap:dict[str,dict])->tuple[list[dict],dict[str,str],dict[str,list[str]]]:
    pages=[]; ttu_by_q={}; bucket_by_q={}
    for qi,q in enumerate(bp.get("question_specs") or [],1):
        qid=q["question_id"]; caps=list(q.get("required_capability_refs") or []); bucket_by_q[qid]=list(q.get("bucket_refs") or [])
        if not caps:fail("MATH_BLUEPRINT_CORE2A_CAPABILITY_REFS_MISSING",qid)
        support=q.get("learner_support") or {}; full=support.get("FULL WORKING") or []; think=support.get("THINK IT THROUGH") or []; quick=support.get("QUICK CHECK") or []
        problem_nodes=[node("QUESTION",q["prompt"]),node("SOURCE",(q.get("provenance") or {}).get("learner_label") or q.get("learner_source_label") or q.get("question_class"))]
        solve_nodes=[node("STEP",x) for x in full] or [node("STEP",x) for x in think]
        if not solve_nodes:fail("MATH_BLUEPRINT_CORE2A_SOLUTION_CHAIN_MISSING",qid)
        why_nodes=[node("PARAGRAPH",x) for x in think] or [node("HINT",support.get("HOW DO I START?"))]
        wrong_nodes=[node("PARAGRAPH",_wrong_route_for_caps(caps,unit_by_cap))]
        check_nodes=[node("CHECK",x) for x in quick]
        if not check_nodes:
            ans=q.get("answer_contract") or {}; checks=ans.get("verification_checks") or []
            check_nodes=[node("CHECK",x.get("evidence") if isinstance(x,dict) else x) for x in checks]
        if not check_nodes:fail("MATH_BLUEPRINT_CORE2A_VERIFICATION_MISSING",qid)
        p=f"C2A-{qi:02d}"
        tech=[
            block(p+"-PROBLEM","PROBLEM","IMMUTABLE_SOURCE" if q.get("question_class")=="SOURCE_CORE2" else "DERIVED_MATHEMATICS",caps,problem_nodes,upstream=None,transform="BUILD",authority_refs=[qid,*caps]),
            block(p+"-SOLVE","SOLUTION_CHAIN","DERIVED_MATHEMATICS",caps,solve_nodes,upstream=p+"-PROBLEM",transform="SOLUTION_ANATOMY",authority_refs=[qid,*caps]),
            block(p+"-WHY","WHY_MOVE_WORKS","EXPLANATION",caps,why_nodes,upstream=p+"-SOLVE",transform="SOLUTION_ANATOMY",authority_refs=[qid,*caps]),
            block(p+"-WRONG","WRONG_CHAIN","DERIVED_MATHEMATICS",caps,wrong_nodes,upstream=p+"-PROBLEM",transform="CONTRAST",authority_refs=[qid,*caps]),
            block(p+"-VERIFY","VERIFICATION","ANSWER_IDENTITY",caps,check_nodes,upstream=p+"-SOLVE",transform="VERIFY",authority_refs=[qid,*caps]),
        ]
        tid=f"TTU-C2A-{qi:02d}"; ttu_by_q[qid]=tid
        tt=ttu(tid,caps,q["prompt"],p+"-SOLVE",p+"-VERIFY",source=None,transform="SOLUTION_ANATOMY",fading="GUIDED")
        pages.append(page(f"C2A-P{qi:02d}","CORE2A","SOLUTION_APPRENTICESHIP",f"Study and reconstruct the expert solution anatomy for {qid}.",tech,[],[representation(f"REP-C2A-{qi:02d}",caps,[support.get("HOW DO I START?") or think[0] if think else q["prompt"]],["Do not expose the final result as part of the representation cue."])],[tt]))
    return pages,ttu_by_q,bucket_by_q


def compile_core2b_pages(plan_doc:dict,c2a_ttu_by_q:dict[str,str])->list[dict]:
    pages=[]
    for i,item in enumerate(plan_doc.get("items") or [],1):
        iid=item["item_id"]; parent=item["core2a_item_ref"]; caps=list(item.get("capability_refs") or [])
        if parent not in c2a_ttu_by_q:fail("MATH_BLUEPRINT_CORE2B_PARENT_TTU_MISSING",parent)
        frame=item.get("self_guided_frame") or {}; help_map=frame.get("help") or {}
        problem=[node("QUESTION",item["stem"]),node("SOURCE",item["learner_source_label"])]
        classify=[node("PARAGRAPH",frame.get("transfer_focus") or item.get("learner_label") or item["demand_level"])]
        work=[node("HINT",help_map[k]) for k in frame.get("help_sequence") or [] if k in help_map and k!="ANSWER_VERIFICATION"]
        if not work: work=[node("HINT",x) for x in item.get("support") or []]
        if not work: fail("MATH_BLUEPRINT_CORE2B_HELP_MISSING",iid)
        answer=[node("ANSWER",item["answer_check"])]
        p=f"C2B-{i:02d}"
        tech=[
            block(p+"-PROBLEM","PROBLEM","DERIVED_MATHEMATICS",caps,problem,upstream=parent,transform="TRANSFER",authority_refs=[parent,*caps]),
            block(p+"-CLASSIFY","TRANSFER_CLASSIFICATION","INSTRUCTION",caps,classify,upstream=parent,transform="TRANSFER",authority_refs=[parent,*caps]),
            block(p+"-WORK","TECHNICAL_WORKSPACE","INSTRUCTION",caps,work,upstream=p+"-PROBLEM",transform="RECONSTRUCT",authority_refs=[parent,*caps]),
            block(p+"-ANSWER","ANSWER_DERIVATION","DERIVED_MATHEMATICS",caps,answer,upstream=p+"-PROBLEM",transform="VERIFY",authority_refs=[item["answer_contract_ref"],*caps]),
            block(p+"-VERIFY","VERIFICATION","ANSWER_IDENTITY",caps,[node("CHECK",item["answer_check"])],upstream=p+"-ANSWER",transform="VERIFY",authority_refs=[item["answer_contract_ref"],*caps]),
        ]
        tid=f"TTU-C2B-{i:02d}"
        tt=ttu(tid,caps,item["stem"],p+"-ANSWER",p+"-VERIFY",source=c2a_ttu_by_q[parent],transform="TRANSFER",fading="FADED")
        pages.append(page(f"C2B-P{i:02d}","CORE2B","TRANSFER_TUTOR",f"Recognise and transfer the governed structure from {parent} before using bounded help.",tech,[],[representation(f"REP-C2B-{i:02d}",caps,[frame.get("transfer_focus") or item["demand_level"]],["Do not name a hidden family or method before the learner classifies the structure."])],[tt],[{"workspace_id":f"WS-C2B-{i:02d}","purpose":"RECONSTRUCTION","math_refs":caps}]))
    return pages


def depth_obligations(badge:str,pages:list[dict])->list[dict]:
    if badge!="EASY":
        fail("MATH_BLUEPRINT_MIXED_OR_NON_EASY_BOUND_PUBLICATION_NOT_YET_SUPPORTED",badge)
    policy=load(POLICY_PATH)
    by_stage={s:[] for s in ("CORE1A","CORE1B")}
    for pg in pages:
        if pg["stage"] in by_stage:by_stage[pg["stage"]].append(pg)
    evidence={
        "CORE1A":{
            "OBJECT_MODEL":by_stage["CORE1A"][0]["technical_blocks"][0]["block_id"],
            "PRIMARY_RELATION":by_stage["CORE1A"][0]["technical_blocks"][0]["block_id"],
            "PRIMARY_REPRESENTATION":by_stage["CORE1A"][0]["representations"][0]["representation_id"],
            "WORKED_ANCHOR":next(b["block_id"] for p in by_stage["CORE1A"] for b in p["technical_blocks"] if b["kind"]=="WORKED_EXAMPLE"),
            "RECONSTRUCTABLE_TTU":by_stage["CORE1A"][0]["reconstructable_ttus"][0]["ttu_id"],
            "VERIFICATION":next(b["block_id"] for p in by_stage["CORE1A"] for b in p["technical_blocks"] if b["kind"]=="VERIFICATION"),
        },
        "CORE1B":{
            "OPEN_RECONSTRUCTION":by_stage["CORE1B"][0]["technical_blocks"][0]["block_id"],
            "REPRESENTATION_REBUILD":by_stage["CORE1B"][0]["representations"][0]["representation_id"],
            "RECONSTRUCTABLE_TTU":by_stage["CORE1B"][0]["reconstructable_ttus"][0]["ttu_id"],
            "INDEPENDENT_USE":by_stage["CORE1B"][0]["technical_blocks"][0]["block_id"],
            "ANSWER_VERIFICATION":next(b["block_id"] for p in by_stage["CORE1B"] for b in p["technical_blocks"] if b["kind"]=="VERIFICATION"),
        }
    }
    rows=[]
    for stage in ("CORE1A","CORE1B"):
        for obligation in policy["depth_obligations"][stage][badge]:
            oid=obligation["id"]
            ref=evidence[stage].get(oid)
            if obligation["required"] and not ref:fail("MATH_BLUEPRINT_REQUIRED_DEPTH_EVIDENCE_UNAVAILABLE",f"{stage}:{oid}")
            rows.append({"stage":stage,"badge":badge,"obligation_id":oid,"disposition":"SATISFIED" if ref else "NOT_APPLICABLE","evidence_refs":[ref] if ref else [],"not_applicable_reason":None if ref else "Optional obligation is not required for this EASY bound publication."})
    return rows


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--bucket-plan",required=True)
    ap.add_argument("--core1a-manuscript",required=True)
    ap.add_argument("--core1b-dir",required=True)
    ap.add_argument("--core2a-blueprint",required=True)
    ap.add_argument("--core2b-plan",required=True)
    ap.add_argument("--generation-spec",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    bucket_plan=load(args.bucket_plan); book=load(args.core1a_manuscript); c2a=load(args.core2a_blueprint); c2b=load(args.core2b_plan); gen=load(args.generation_spec)
    badges={row["difficulty_badge"] for row in gen["core1_buckets"]}
    if len(badges)!=1:fail("MATH_BLUEPRINT_MIXED_DIFFICULTY_PUBLICATION_REQUIRES_BUNDLE",",".join(sorted(badges)))
    badge=next(iter(badges))
    if badge!="EASY":fail("MATH_BLUEPRINT_NON_EASY_PUBLICATION_COMPILER_PENDING",badge)
    c1a_pages,c1a_ttu,unit_by_cap=compile_core1a_pages(book)
    plans=load_core1b_plans(Path(args.core1b_dir),[b["title"] for b in bucket_plan["buckets"]])
    c1b_pages,_=compile_core1b_pages(bucket_plan,plans,c1a_ttu)
    c2a_pages,c2a_ttu,_=compile_core2a_pages(c2a,unit_by_cap)
    c2b_pages=compile_core2b_pages(c2b,c2a_ttu)
    pages=[*c1a_pages,*c1b_pages,*c2a_pages,*c2b_pages]
    doc={"schema_version":"1.0.0","subject":"MATHEMATICS","blueprint_id":"","difficulty_badge":badge,"pages":pages,"depth_obligations":depth_obligations(badge,pages)}
    doc["blueprint_id"]="MATH-PAGE-BP-BOUND-"+digest(doc)[:16]
    audit=validate_content_complete_blueprint(doc)
    Path(args.out).write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2,ensure_ascii=False))


if __name__=="__main__":main()
