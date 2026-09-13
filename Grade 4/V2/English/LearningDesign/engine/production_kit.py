"""Grade 4 English production-kit reference engine.

Fail-closed cold-start handoff:
source/answer contract -> task archetype -> scaffold profile ->
learning representation -> page plan.
"""
from __future__ import annotations
import copy, json, sys
from pathlib import Path

class ProductionKitError(ValueError): pass

def require(ok, code, detail=""):
    if not ok: raise ProductionKitError(f"{code}: {detail}".rstrip(": "))

def by_id(rows): return {row["id"]:row for row in rows}

def classify_task(task, archetype_doc):
    rows=archetype_doc["archetypes"]
    explicit=task.get("task_archetype")
    if explicit:
        found=[r for r in rows if r["id"]==explicit]
        require(len(found)==1,"UNKNOWN_TASK_ARCHETYPE",str(explicit)); return found[0]
    matches=[]
    for row in rows:
        sig=row.get("signature") or {}
        if all(task.get(k)==v for k,v in sig.items()): matches.append(row)
    require(matches,"TASK_ARCHETYPE_UNRESOLVED",task.get("task_id",""))
    require(len(matches)==1,"TASK_ARCHETYPE_AMBIGUOUS",task.get("task_id",""))
    return matches[0]

def validate_source_answer(task):
    src=task.get("source_reference"); require(isinstance(src,dict),"SOURCE_REFERENCE_MISSING")
    kind=src.get("source_kind"); require(kind in {"WORKBOOK","WORKSHEET","GENERATED"},"SOURCE_KIND_INVALID")
    display=str(src.get("display_ref") or ""); require(display,"SOURCE_DISPLAY_REF_MISSING")
    if kind in {"WORKBOOK","WORKSHEET"}:
        require(any(v not in (None,"") for v in (src.get("section_label"),src.get("question_number"),src.get("organizer_box"))),"SOURCE_LOCATOR_MISSING")
        if src.get("section_label") not in (None,""): require(str(src["section_label"]) in display,"SOURCE_SECTION_DROPPED",display)
        if src.get("question_number") not in (None,""): require(str(src["question_number"]) in display,"SOURCE_NUMBER_REWRITTEN",display)
        if src.get("organizer_box") not in (None,""): require(str(src["organizer_box"]) in display,"SOURCE_BOX_REWRITTEN",display)
    else:
        require(display.lower().startswith(("fresh ","practice ","generated ")),"GENERATED_ITEM_USING_SOURCE_NUMBER",display)
    ans=task.get("answer"); require(isinstance(ans,dict),"ANSWER_CONTRACT_MISSING")
    status=ans.get("status"); allowed={"VERIFIED_SOURCE","DERIVED_FROM_SOURCE","VERIFIED_RULE","RUBRIC","SOURCE_UNRESOLVED"}
    require(status in allowed,"ANSWER_STATUS_INVALID",str(status))
    expected=ans.get("expected_response")
    if status=="SOURCE_UNRESOLVED": require(expected in (None,""),"SOURCE_UNRESOLVED_WITH_ASSERTED_ANSWER")
    elif status!="RUBRIC": require(expected not in (None,""),"ANSWER_EXPECTED_RESPONSE_MISSING")
    if status=="DERIVED_FROM_SOURCE":
        ev=task.get("evidence") or {}; require(bool(ev.get("source_lines")) and bool(ev.get("highlight_spans")),"DERIVED_READING_ANSWER_WITHOUT_EVIDENCE")

def build_representation(task, archetypes, scaffold_doc, components_doc):
    validate_source_answer(task); route=classify_task(task,archetypes)
    profiles=by_id(scaffold_doc["profiles"]); profile=profiles.get(route["scaffold_profile"])
    require(profile is not None,"SCAFFOLD_PROFILE_MISSING",route["scaffold_profile"])
    ids={x["id"] for x in components_doc["components"]}; unknown=[x for x in profile.get("required_components",[]) if x not in ids]
    require(not unknown,"UNKNOWN_COMPONENT",str(unknown))
    rep={"schema_version":"1.0.0","task_id":task["task_id"],"task_archetype":route["id"],"scaffold_profile":profile["id"],"source_reference":copy.deepcopy(task["source_reference"]),"answer":copy.deepcopy(task["answer"]),"preteach":copy.deepcopy(profile.get("preteach_sequence") or []),"model":copy.deepcopy(profile.get("teach_sequence") or []),"guided":copy.deepcopy(profile.get("guided_sequence") or []),"independent_try":task.get("child_prompt"),"help":{"reveal_mode":"ON_DEMAND","steps":copy.deepcopy(profile.get("help_sequence") or [])},"fresh_retry":copy.deepcopy(task.get("fresh_retry")),"components":copy.deepcopy(profile.get("required_components") or []),"evidence":copy.deepcopy(task.get("evidence")),"render_constraints":{"preserve_source_reference":True,"answer_reveal_policy":profile.get("answer_reveal_policy"),"one_dominant_move_per_page":True}}
    if profile.get("fresh_retry_required"): require(bool(rep.get("fresh_retry")),"FRESH_RETRY_REQUIRED")
    validate_representation(rep,components_doc); return rep

def validate_representation(rep, components_doc):
    require((rep.get("help") or {}).get("reveal_mode")=="ON_DEMAND","HINTS_NOT_ON_DEMAND")
    require(len((rep.get("help") or {}).get("steps") or [])>=3,"HELP_SEQUENCE_TOO_SHORT")
    if rep.get("scaffold_profile")=="SOURCE_EVIDENCE_LADDER":
        ev=rep.get("evidence") or {}
        if (rep.get("answer") or {}).get("status")!="SOURCE_UNRESOLVED":
            require(bool(ev.get("source_lines")),"SOURCE_LINES_MISSING"); require(bool(ev.get("highlight_spans")),"EVIDENCE_HIGHLIGHTS_MISSING")
        require("SOURCE_STRIP" in rep["components"] and "EVIDENCE_HIGHLIGHT" in rep["components"],"READING_COMPONENTS_MISSING")
    return True

def compile_page_plan(rep):
    ref=rep["source_reference"]["display_ref"]; comps=rep["components"]
    pages=[
      {"page_role":"MODEL","dominant_move":"MODEL","source_ref":ref,"components":["WORKBOOK_REFERENCE_BADGE"]+[c for c in comps if c not in {"TRY_FIRST","ANSWER_CHECK","FRESH_RETRY"}],"answer_visibility":"MODEL_ONLY"},
      {"page_role":"TRY_ONE","dominant_move":"APPLY","source_ref":ref,"components":["WORKBOOK_REFERENCE_BADGE","TRY_FIRST"],"answer_visibility":"HIDDEN","help_visibility":"ON_DEMAND"},
      {"page_role":"CHECK","dominant_move":"CHECK","source_ref":ref,"components":["WORKBOOK_REFERENCE_BADGE","ANSWER_CHECK"],"answer_visibility":"SHOW_AFTER_ATTEMPT"}
    ]
    if rep.get("fresh_retry"): pages.append({"page_role":"FRESH_RETRY","dominant_move":"APPLY","source_ref":rep["fresh_retry"].get("display_ref","Fresh Retry"),"components":["FRESH_RETRY"],"answer_visibility":"HIDDEN"})
    return {"schema_version":"1.0.0","task_id":rep["task_id"],"scaffold_profile":rep["scaffold_profile"],"pages":pages}

def validate_kit(archetypes, scaffolds, components, fixture_doc):
    reps=[build_representation(t,archetypes,scaffolds,components) for t in fixture_doc["fixtures"]]
    def expect_fail(task,code):
        try: build_representation(task,archetypes,scaffolds,components)
        except Exception as exc:
            require(code in str(exc),"NEGATIVE_GATE_WRONG_ERROR",f"{code} -> {exc}"); return
        raise ProductionKitError(f"NEGATIVE_GATE_DID_NOT_FAIL: {code}")
    adjective=next(copy.deepcopy(x) for x in fixture_doc["fixtures"] if x["task_id"]=="G4-ENG-ADJ-WKS-6"); adjective["source_reference"]["display_ref"]="Worksheet Adjective Order-99"; expect_fail(adjective,"SOURCE_NUMBER_REWRITTEN")
    reading=next(copy.deepcopy(x) for x in fixture_doc["fixtures"] if x["task_id"]=="G4-ENG-MIGRATION-P98-B5"); reading["evidence"]["highlight_spans"]=[]; expect_fail(reading,"DERIVED_READING_ANSWER_WITHOUT_EVIDENCE")
    unresolved=next(copy.deepcopy(x) for x in fixture_doc["fixtures"] if x["task_id"]=="G4-ENG-MIGRATION-P98-B1"); unresolved["answer"]["expected_response"]="guessed answer"; expect_fail(unresolved,"SOURCE_UNRESOLVED_WITH_ASSERTED_ANSWER")
    return reps

def main():
    if len(sys.argv)!=5: raise SystemExit("usage: production_kit.py archetypes.json scaffold_profiles.json component_library.json fixtures.json")
    docs=[json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:]]
    reps=validate_kit(*docs)
    for rep in reps: print(f"PASS {rep['task_id']} -> {rep['scaffold_profile']} -> {len(compile_page_plan(rep)['pages'])} pages")
    print(f"PASS: production kit ({len(reps)} fixtures + negative gates)")
if __name__=="__main__": main()
