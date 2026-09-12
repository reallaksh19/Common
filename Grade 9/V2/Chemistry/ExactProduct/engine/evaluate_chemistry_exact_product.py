#!/usr/bin/env python3
import argparse, copy, hashlib, json
from pathlib import Path

HUMAN_TO_QUALITY={
 'AUTHORIZED_CHEMISTRY_SUBJECT':'SUBJECT_CORRECTNESS',
 'AUTHORIZED_PEDAGOGY':'PEDAGOGICAL_DESIGN',
 'AUTHORIZED_ASSESSMENT':'ASSESSMENT_DESIGN',
 'AUTHORIZED_VISUAL_USABILITY':'VISUAL_USABILITY'}

def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def artifact_map(candidate): return {x['product_id']:x for x in candidate['artifacts']}

def bind_to_cold_start(candidate,cold):
    if cold['report_digest']!=digest(cold,'report_digest'): fail('SOURCE_HASH_MISMATCH','cold-start report digest')
    if candidate['cold_start_report_ref']!=cold['run_id'] or candidate['cold_start_report_digest']!=cold['report_digest']: fail('EXACT_ARTIFACT_HASH_MISMATCH','cold-start report')
    for k in ['source_set_digest','question_set_digest','corpus_digest','declared_topic_scope_digest']:
        if candidate['input_custody'][k]!=cold['input_custody'][k]: fail('SOURCE_HASH_MISMATCH',k)
    s=candidate['semantic_custody']; st=cold['stage_outputs']; der=cold['derived_authority']
    expected={
      'source_obligation_ledger_digest':der['source_ledger_digest'],
      'assessment_scope_digest':st['scope_bundle_digest'],
      'learner_study_model_digest':st['study_model_digest'],
      'core1_semantic_digest':st['core1_plan_digest'],
      'core2_semantic_digest':st['core2_plan_digest'],
      'coverage_closure_digest':st['coverage_closure_digest']}
    for k,v in expected.items():
        if s[k]!=v: fail('EXACT_ARTIFACT_HASH_MISMATCH',k)
    # Appendix identities are explicit sub-identities of the frozen Core1 semantic source.
    for k in ['appendix_a_semantic_digest','appendix_b_semantic_digest','appendix_c_semantic_digest']:
        if len(s[k])!=64: fail('EXACT_ARTIFACT_HASH_MISMATCH',k)
    return True

def machine_validate(candidate,cold,policy,artifact_root='.',required_qc_refs=None):
    failures=[]; root=Path(artifact_root)
    if candidate['package_digest']!=digest(candidate,'package_digest'): failures.append('EXACT_ARTIFACT_HASH_MISMATCH')
    try: bind_to_cold_start(candidate,cold)
    except ValueError as e: failures.append(str(e).split(':',1)[0])
    arts=artifact_map(candidate)
    if len(arts)!=2 or set(arts)!=set(policy['required_product_ids']):
        if 'CORE_STUDY_GUIDE' not in arts: failures.append('MISSING_CORE1_PDF')
        if 'EXAMSIDE_SOLUTION_TRANSFER_BOOK' not in arts: failures.append('MISSING_CORE2_PDF')
        if len(candidate['artifacts'])>2: failures.append('THIRD_REQUIRED_PRODUCT_INSTEAD_OF_APPENDIX_C')
    core=arts.get('CORE_STUDY_GUIDE'); transfer=arts.get('EXAMSIDE_SOLUTION_TRANSFER_BOOK')
    if core:
        sections=set(core['required_sections'])
        req=set(policy['required_core1_sections'])
        if 'APPENDIX_A_CORE_PRACTICE' not in sections: failures.append('APPENDIX_A_MISSING')
        if 'APPENDIX_B_CORE_SOLUTIONS' not in sections: failures.append('APPENDIX_B_MISSING')
        if 'APPENDIX_C_PRINTABLE_HANDOUT' not in sections: failures.append('APPENDIX_C_MISSING')
        if not req<=sections: pass
    for pid,code in [('CORE_STUDY_GUIDE','MISSING_CORE1_PDF'),('EXAMSIDE_SOLUTION_TRANSFER_BOOK','MISSING_CORE2_PDF')]:
        a=arts.get(pid)
        if not a: continue
        p=root/a['path']
        if not p.exists(): failures.append(code); continue
        b=p.read_bytes()
        if not b.startswith(b'%PDF'): failures.append(code)
        if sha_file(p)!=a['sha256']: failures.append('EXACT_ARTIFACT_HASH_MISMATCH')
    e=candidate['machine_evidence']
    checks=[
      (not e['answer_separation_pass'],'APPENDIX_A_B_ANSWER_SEPARATION_FAILURE'),
      (e['handout_answer_leakage'],'HANDOUT_ANSWER_LEAKAGE'),
      (e['handout_scope_leakage'],'HANDOUT_SCOPE_LEAKAGE'),
      (not e['formula_typography_pass'],'FORMULA_SUBSCRIPT_SUPERSCRIPT_FAILURE'),
      (not e['ionic_charge_unambiguous'],'AMBIGUOUS_IONIC_CHARGE'),
      (not e['reaction_notation_fidelity_pass'],'REACTION_ARROW_STATE_CONDITION_DRIFT'),
      (e['ascii_chemistry_leaks']>0,'ASCII_CHEMISTRY_LEAK_WHEN_FORBIDDEN'),
      (e['off_page_text_count']>0,'OFF_PAGE_TEXT'),
      (e['collision_count']>0,'TEXT_OR_CARD_COLLISION'),
      (e['minimum_font_pt']<policy['minimum_font_pt'],'MIN_FONT_SIZE_FAILURE'),
      (e['broken_internal_links']>0,'BROKEN_INTERNAL_LINK'),
      (e['wrong_external_source_uris']>0,'WRONG_EXTERNAL_SOURCE_URI'),
      (not e['source_hash_match'],'SOURCE_HASH_MISMATCH'),
      (e['source_obligations_closed']!=e['source_obligations_required'],'SOURCE_OBLIGATION_RECONCILIATION_FAILURE'),
      (e['eligible_external_placed_unique']!=e['eligible_external_total'],'EXTERNAL_CORPUS_RECONCILIATION_FAILURE'),
      (e['duplicate_primary_placements']>0,'DUPLICATE_PRIMARY_PLACEMENT'),
      (e['eligible_missing_core2']>0,'ELIGIBLE_ITEM_MISSING_CORE2'),
      (e['hint_failures']>0,'HINT_SUPPORT_FAILURE'),
      (e['solution_failures']>0,'SOLUTION_FAILURE'),
      (not e['source_structure_formula_fidelity'],'SOURCE_STRUCTURE_OR_FORMULA_DRIFT_IGNORED'),
      # Engineering falsifiers added with issue #321. Read with .get so a
      # legacy candidate that predates these fields still evaluates.
      (e.get('learner_internal_identifier_leaks',0)>0,'LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK'),
      (len(e.get('teaching_primitive_kinds_realized',[]))<policy.get('minimum_realized_primitive_kinds',0),'TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED'),
      ('actual_placement_evidence' in e and not e['actual_placement_evidence'],'PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE'),
      (e.get('placement_bounds_violations',0)>0,'PLACEMENT_OUT_OF_PHYSICAL_BOUNDS'),
      (e.get('orphan_continuations',0)>0,'ORPHAN_CONTINUATION_FRAGMENT')]
    failures += [code for cond,code in checks if cond]
    required_qc_refs=set(required_qc_refs or [])
    if not required_qc_refs<=set(candidate['source_qc_event_refs']): failures.append('SOURCE_QC_EVENT_LOST_IN_FINAL_PRODUCT')
    failures=list(dict.fromkeys(failures))
    return {'status':'PASS' if not failures else 'FAIL','failures':failures}

def review_binding(review,candidate):
    arts=artifact_map(candidate); c=arts.get('CORE_STUDY_GUIDE'); t=arts.get('EXAMSIDE_SOLUTION_TRANSFER_BOOK')
    if review['candidate_ref']!=candidate['candidate_id'] or review['package_digest']!=candidate['package_digest'] or not c or not t or review['core1_pdf_sha256']!=c['sha256'] or review['core2_pdf_sha256']!=t['sha256']:
        fail('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT',review['review_id'])
    if review['review_kind']=='AI_PRE_REVIEW' and review['reviewer_role']!='AI_PRE_REVIEW': fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS')
    if review['review_kind']=='AUTHORIZED_HUMAN_REVIEW' and review['reviewer_role']=='AI_PRE_REVIEW': fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS')
    return True

def human_states(candidate,reviews,policy):
    states={v:'PENDING' for v in HUMAN_TO_QUALITY.values()}; by={}
    for r in reviews:
        review_binding(r,candidate)
        if r['review_kind']!='AUTHORIZED_HUMAN_REVIEW': continue
        role=r['reviewer_role']
        if role not in policy['required_human_roles']: continue
        if role in by: fail('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT','duplicate '+role)
        by[role]=r; states[HUMAN_TO_QUALITY[role]]=r['state']
    return states,by

def build_release_decision(candidate,machine_gate,reviews,reference_comparison,policy,learning_effectiveness=None,decision_id='CHEM-C-L-RELEASE-v1'):
    hstates,hby=human_states(candidate,reviews,policy)
    quality={'PUBLICATION_ENGINEERING':'PASS' if machine_gate['status']=='PASS' else 'FAIL',**hstates,'MATURE_DESIGN_QUALITY':'BLOCKED','REFERENCE_COMPARABILITY':'NOT_RUN'}
    blocking=[]
    if machine_gate['status']!='PASS': blocking+=machine_gate['failures']
    all_human=all(hstates[x]=='PASS' for x in ['SUBJECT_CORRECTNESS','PEDAGOGICAL_DESIGN','ASSESSMENT_DESIGN','VISUAL_USABILITY'])
    if reference_comparison.get('raw_reference_used_as_runtime_input'): fail('RAW_PR157_USED_AS_RUNTIME_TEMPLATE')
    if reference_comparison.get('state')!='NOT_RUN' and not all_human: fail('PR157_COMPARISON_RUN_BEFORE_HUMAN_GATES')
    if not all_human:
        blocking += ['AUTHORIZED_HUMAN_GATES_INCOMPLETE']
        quality['REFERENCE_COMPARABILITY']='BLOCKED'
    else:
        quality['REFERENCE_COMPARABILITY']=reference_comparison['state']
    if machine_gate['status']=='PASS' and all_human and reference_comparison['state']=='PASS':
        e=candidate['machine_evidence']
        if candidate['candidate_class']=='LEGACY_NONCONFORMING_REDOX': fail('LEGACY_NONCONFORMING_REDOX_SNAPSHOT_RECEIVES_MATURE_PASS')
        if candidate['candidate_class']=='KNOWN_THIN_SMOKE' or e['core1_instructional_depth']!='FULL_INSTRUCTIONAL': fail('KNOWN_THIN_SMOKE_SPECIMEN_RECEIVES_MATURE_DESIGN_PASS')
        if not e['macro_particle_symbolic_realized']: fail('MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED')
        if e.get('teaching_primitives_label_only') and len(e['teaching_primitives_label_only'])>len(e.get('teaching_primitive_kinds_realized',[])): fail('TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED')
        if e.get('learner_internal_identifier_leaks',0)>0: fail('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK')
        if not e['primary_supports_correct']: fail('PRIMARY_SUPPORTS_LABELS_INCORRECT')
        if not e['visual_usable_actual_size']: fail('VISUAL_UNUSABLE_AT_ACTUAL_OUTPUT_SIZE')
        if not e['hints_distinct_from_solution']: fail('HINTS_DUPLICATE_SOLUTION_BUT_MARKED_MATURE')
        quality['MATURE_DESIGN_QUALITY']='PASS'; classification=policy['mature_classification']; exit_code=0
    elif machine_gate['status']=='FAIL':
        quality['MATURE_DESIGN_QUALITY']='FAIL'; classification='VALIDATION_FAIL'; exit_code=1
    else:
        classification=policy['blocked_classification']; exit_code=2
    le=learning_effectiveness or {'state':'STUDY_REQUIRED','study_evidence_ref':None}
    if le['state']=='VALIDATED' and not le.get('study_evidence_ref'): fail('LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY')
    out={'decision_id':decision_id,'schema_version':'1.0.0','subject':'CHEMISTRY','candidate_ref':candidate['candidate_id'],'package_digest':candidate['package_digest'],'machine_gate':copy.deepcopy(machine_gate),'quality_states':quality,'learning_effectiveness':le,'reference_comparison':copy.deepcopy(reference_comparison),'classification':classification,'exit_code':exit_code,'blocking_reasons':list(dict.fromkeys(blocking)),'decision_digest':''}
    out['decision_digest']=digest(out,'decision_digest'); return out

def validate_release_decision(decision,candidate,reviews,policy):
    if decision['decision_digest']!=digest(decision,'decision_digest'): fail('EXACT_ARTIFACT_HASH_MISMATCH','decision digest')
    if decision['candidate_ref']!=candidate['candidate_id'] or decision['package_digest']!=candidate['package_digest']: fail('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT','decision')
    hstates,_=human_states(candidate,reviews,policy)
    q=decision['quality_states']; e=candidate['machine_evidence']; mg=decision['machine_gate']; rc=decision['reference_comparison']
    if mg['status']=='PASS' and q['PEDAGOGICAL_DESIGN']=='PASS' and hstates['PEDAGOGICAL_DESIGN']!='PASS': fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS')
    if q['SUBJECT_CORRECTNESS']=='PASS' and hstates['SUBJECT_CORRECTNESS']!='PASS': fail('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT','subject')
    if decision['classification']==policy['mature_classification']:
        if mg['status']!='PASS': fail('SUBJECT_ERROR_SURVIVES_TO_MATURE_STATE')
        if not e['source_structure_formula_fidelity'] or not e['formula_typography_pass'] or not e['ionic_charge_unambiguous']: fail('SUBJECT_ERROR_SURVIVES_TO_MATURE_STATE')
        if e['core1_instructional_depth']!='FULL_INSTRUCTIONAL': fail('CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE')
        if not e['macro_particle_symbolic_realized']: fail('MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED')
        if 'APPENDIX_C_PRINTABLE_HANDOUT' not in set(artifact_map(candidate)['CORE_STUDY_GUIDE']['required_sections']): fail('APPENDIX_C_MISSING_BUT_PRODUCT_MARKED_MATURE')
        if e['handout_answer_leakage']: fail('HANDOUT_CONTAINS_SOLUTIONS')
        if not e['hints_distinct_from_solution']: fail('HINTS_DUPLICATE_SOLUTION_BUT_MARKED_MATURE')
        if not e['primary_supports_correct']: fail('PRIMARY_SUPPORTS_LABELS_INCORRECT')
        if not e['visual_usable_actual_size']: fail('VISUAL_UNUSABLE_AT_ACTUAL_OUTPUT_SIZE')
        if not e['source_structure_formula_fidelity']: fail('SOURCE_STRUCTURE_OR_FORMULA_DRIFT_IGNORED')
        if candidate['candidate_class']=='LEGACY_NONCONFORMING_REDOX': fail('LEGACY_NONCONFORMING_REDOX_SNAPSHOT_RECEIVES_MATURE_PASS')
        if candidate['candidate_class']=='KNOWN_THIN_SMOKE': fail('KNOWN_THIN_SMOKE_SPECIMEN_RECEIVES_MATURE_DESIGN_PASS')
        if not all(hstates[x]=='PASS' for x in hstates): fail('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT','human gates incomplete')
        if rc['state']!='PASS' or not rc['run_after_human_gates']: fail('PR157_COMPARISON_RUN_BEFORE_HUMAN_GATES')
        if decision['exit_code']!=0: fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS','mature exit')
    if rc['raw_reference_used_as_runtime_input']: fail('RAW_PR157_USED_AS_RUNTIME_TEMPLATE')
    if rc['state']!='NOT_RUN' and not rc['run_after_human_gates']: fail('PR157_COMPARISON_RUN_BEFORE_HUMAN_GATES')
    if decision['learning_effectiveness']['state']=='VALIDATED' and not decision['learning_effectiveness'].get('study_evidence_ref'): fail('LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY')
    if decision['classification']!=policy['mature_classification'] and decision['exit_code']==0: fail('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS','blocked cannot exit 0')
    return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--candidate',required=True); ap.add_argument('--cold-start-report',required=True); ap.add_argument('--policy',required=True); ap.add_argument('--artifact-root',default='.'); ap.add_argument('--reviews',nargs='*',default=[]); ap.add_argument('--reference-comparison'); ap.add_argument('--out',required=True); a=ap.parse_args()
    cand=load(a.candidate); cold=load(a.cold_start_report); policy=load(a.policy); mg=machine_validate(cand,cold,policy,a.artifact_root)
    reviews=[load(p) for p in a.reviews]; rc=load(a.reference_comparison) if a.reference_comparison else {'comparator_id':policy['reference_comparator_id'],'state':'NOT_RUN','run_after_human_gates':False,'raw_reference_used_as_runtime_input':False}
    decision=build_release_decision(cand,mg,reviews,rc,policy); validate_release_decision(decision,cand,reviews,policy); Path(a.out).write_text(json.dumps(decision,indent=2,sort_keys=True)+'\n',encoding='utf-8'); raise SystemExit(decision['exit_code'])
if __name__=='__main__': main()
