#!/usr/bin/env python3
import copy, hashlib, json, sys, tempfile
from pathlib import Path
D=Path(__file__).resolve().parents[1]; REPO=D.parents[3]
sys.path.insert(0,str(D/'engine'))
from evaluate_chemistry_exact_product import digest,machine_validate,build_release_decision,validate_release_decision

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
policy=load(D/'registry'/'chemistry-exact-product-quality-policy.json')

def h(x): return hashlib.sha256(x.encode()).hexdigest()
def expect(code,fn):
    try: fn()
    except ValueError as e:
        assert str(e).split(':',1)[0]==code,(code,str(e)); return
    raise AssertionError('expected '+code)

def cold():
    x={'run_id':'CHEM-C-L-COLD','schema_version':'1.0.0','subject':'CHEMISTRY','input_custody':{'source_set_digest':h('source'),'question_set_digest':h('questions'),'corpus_digest':h('corpus'),'declared_topic_scope_digest':h('scope')},'derived_authority':{'source_ledger_digest':h('ledger')},'stage_outputs':{'scope_bundle_digest':h('scope-model'),'study_model_digest':h('study'),'core1_plan_digest':h('core1'),'core2_plan_digest':h('core2'),'coverage_closure_digest':h('closure')},'report_digest':''}
    x['report_digest']=digest(x,'report_digest'); return x

def pdf(root,name,tag):
    p=root/name; p.write_bytes(b'%PDF-1.4\n% Chemistry C-L '+tag.encode()+b'\n%%EOF\n'); return p,hashlib.sha256(p.read_bytes()).hexdigest()

def candidate(root,klass='CURRENT_COLD_START'):
    c=cold(); p1,s1=pdf(root,'core1.pdf','core1'); p2,s2=pdf(root,'core2.pdf','core2')
    e={'answer_separation_pass':True,'handout_answer_leakage':False,'handout_scope_leakage':False,'formula_typography_pass':True,'ionic_charge_unambiguous':True,'reaction_notation_fidelity_pass':True,'ascii_chemistry_leaks':0,'off_page_text_count':0,'collision_count':0,'minimum_font_pt':9.0,'broken_internal_links':0,'wrong_external_source_uris':0,'source_hash_match':True,'source_obligations_required':10,'source_obligations_closed':10,'external_candidates_total':6,'eligible_external_total':5,'eligible_external_placed_unique':5,'duplicate_primary_placements':0,'eligible_missing_core2':0,'hint_failures':0,'solution_failures':0,'primary_supports_correct':True,'macro_particle_symbolic_realized':True,'core1_instructional_depth':'FULL_INSTRUCTIONAL','visual_usable_actual_size':True,'source_structure_formula_fidelity':True,'hints_distinct_from_solution':True,'teaching_primitive_kinds_selected':['A','B','C','D','E','F','G','H'],'teaching_primitive_kinds_realized':['A','B','C','D','E','F','G','H'],'teaching_primitives_drawn':24,'teaching_primitives_label_only':[],'registry_primitive_total':20,'learner_internal_identifier_leaks':0,'actual_placement_evidence':True,'placement_bounds_violations':0,'orphan_continuations':0,'visual_semantic_validator_ref':'MasterTemplates.VisualSemanticValidator'}
    x={'candidate_id':'CHEM-C-L-CAND','schema_version':'1.0.0','subject':'CHEMISTRY','candidate_class':klass,'cold_start_report_ref':c['run_id'],'cold_start_report_digest':c['report_digest'],'input_custody':copy.deepcopy(c['input_custody']),'semantic_custody':{'source_obligation_ledger_digest':c['derived_authority']['source_ledger_digest'],'assessment_scope_digest':c['stage_outputs']['scope_bundle_digest'],'learner_study_model_digest':c['stage_outputs']['study_model_digest'],'pck_authority_digest':h('pck'),'problem_family_authority_digest':h('families'),'core1_semantic_digest':c['stage_outputs']['core1_plan_digest'],'representation_bundle_digest':h('reps'),'teaching_primitive_registry_digest':h('prims'),'appendix_a_semantic_digest':h('appa'),'appendix_b_semantic_digest':h('appb'),'appendix_c_semantic_digest':h('appc'),'core2_semantic_digest':c['stage_outputs']['core2_plan_digest'],'coverage_closure_digest':c['stage_outputs']['coverage_closure_digest']},'artifacts':[{'product_id':'CORE_STUDY_GUIDE','path':p1.name,'sha256':s1,'page_count':12,'required_sections':['MAIN_TEACHING','APPENDIX_A_CORE_PRACTICE','APPENDIX_B_CORE_SOLUTIONS','APPENDIX_C_PRINTABLE_HANDOUT'],'physical_page_map_digest':h('map1'),'render_audit_digest':h('audit1')},{'product_id':'EXAMSIDE_SOLUTION_TRANSFER_BOOK','path':p2.name,'sha256':s2,'page_count':8,'required_sections':['TRANSFER_QUESTIONS','COMPLETE_SOLUTIONS'],'physical_page_map_digest':h('map2'),'render_audit_digest':h('audit2')}],'machine_evidence':e,'source_qc_event_refs':[],'package_digest':''}
    x['package_digest']=digest(x,'package_digest'); return x,c

def reviews(c):
    a={x['product_id']:x for x in c['artifacts']}; out=[]
    for role in policy['required_human_roles']:
        out.append({'review_id':'TEST-'+role,'schema_version':'1.0.0','subject':'CHEMISTRY','review_kind':'AUTHORIZED_HUMAN_REVIEW','reviewer_role':role,'candidate_ref':c['candidate_id'],'package_digest':c['package_digest'],'core1_pdf_sha256':a['CORE_STUDY_GUIDE']['sha256'],'core2_pdf_sha256':a['EXAMSIDE_SOLUTION_TRANSFER_BOOK']['sha256'],'state':'PASS','findings':[],'production_claim':False})
    return out

def ref(state='PASS',after=True,raw=False): return {'comparator_id':policy['reference_comparator_id'],'state':state,'run_after_human_gates':after,'raw_reference_used_as_runtime_input':raw}
def refresh_candidate(c): c['package_digest']=digest(c,'package_digest'); return c
def mature(root,c=None):
    if c is None: c,cr=candidate(root)
    else: cr=cold()
    rs=reviews(c); mg=machine_validate(c,cr,policy,root); assert mg['status']=='PASS',mg
    dec=build_release_decision(c,mg,rs,ref(),policy); assert dec['classification']==policy['mature_classification'] and dec['exit_code']==0
    validate_release_decision(dec,c,rs,policy); return c,cr,rs,dec

def rebind(c,dec):
    refresh_candidate(c); rs=reviews(c); dec=copy.deepcopy(dec); dec['candidate_ref']=c['candidate_id']; dec['package_digest']=c['package_digest']; dec['decision_digest']=digest(dec,'decision_digest'); return rs,dec

with tempfile.TemporaryDirectory() as td:
    root=Path(td); c,cr=candidate(root); mg=machine_validate(c,cr,policy,root); assert mg=={'status':'PASS','failures':[]}
    blocked=build_release_decision(c,mg,[],ref('NOT_RUN',False),policy); assert blocked['exit_code']==2 and blocked['classification']==policy['blocked_classification']
    mature_c,cr,rs,dec=mature(root,c)

    # 1 MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS
    bad=copy.deepcopy(blocked); bad['exit_code']=0; bad['decision_digest']=digest(bad,'decision_digest')
    expect('MACHINE_GREEN_CLAIMED_AS_PEDAGOGY_PASS',lambda: validate_release_decision(bad,c,[],policy))
    # 2 HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT
    badr=copy.deepcopy(rs); badr[0]['core1_pdf_sha256']=h('wrong')
    expect('HUMAN_REVIEW_NOT_BOUND_TO_EXACT_ARTIFACT',lambda: build_release_decision(c,mg,badr,ref(),policy))
    # 3 SUBJECT_ERROR_SURVIVES_TO_MATURE_STATE
    x=copy.deepcopy(c); x['machine_evidence']['formula_typography_pass']=False; r2,d2=rebind(x,dec)
    expect('SUBJECT_ERROR_SURVIVES_TO_MATURE_STATE',lambda: validate_release_decision(d2,x,r2,policy))
    # 4 SOURCE_QC_EVENT_LOST_IN_FINAL_PRODUCT
    assert 'SOURCE_QC_EVENT_LOST_IN_FINAL_PRODUCT' in machine_validate(c,cr,policy,root,['QC-1'])['failures']
    # 5 CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE
    x=copy.deepcopy(c); x['machine_evidence']['core1_instructional_depth']='SUMMARY_LEVEL'; r2,d2=rebind(x,dec)
    expect('CORE1_SUMMARY_LEVEL_BUT_MARKED_MATURE',lambda: validate_release_decision(d2,x,r2,policy))
    # 6 MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED
    x=copy.deepcopy(c); x['machine_evidence']['macro_particle_symbolic_realized']=False; r2,d2=rebind(x,dec)
    expect('MACRO_PARTICLE_SYMBOLIC_BRIDGE_ONLY_LABELLED_NOT_REALIZED',lambda: validate_release_decision(d2,x,r2,policy))
    # 7 APPENDIX_C_MISSING_BUT_PRODUCT_MARKED_MATURE
    x=copy.deepcopy(c); x['artifacts'][0]['required_sections'].remove('APPENDIX_C_PRINTABLE_HANDOUT'); r2,d2=rebind(x,dec)
    expect('APPENDIX_C_MISSING_BUT_PRODUCT_MARKED_MATURE',lambda: validate_release_decision(d2,x,r2,policy))
    # 8 HANDOUT_CONTAINS_SOLUTIONS
    x=copy.deepcopy(c); x['machine_evidence']['handout_answer_leakage']=True; r2,d2=rebind(x,dec)
    expect('HANDOUT_CONTAINS_SOLUTIONS',lambda: validate_release_decision(d2,x,r2,policy))
    # 9 HINTS_DUPLICATE_SOLUTION_BUT_MARKED_MATURE
    x=copy.deepcopy(c); x['machine_evidence']['hints_distinct_from_solution']=False; r2,d2=rebind(x,dec)
    expect('HINTS_DUPLICATE_SOLUTION_BUT_MARKED_MATURE',lambda: validate_release_decision(d2,x,r2,policy))
    # 10 PRIMARY_SUPPORTS_LABELS_INCORRECT
    x=copy.deepcopy(c); x['machine_evidence']['primary_supports_correct']=False; r2,d2=rebind(x,dec)
    expect('PRIMARY_SUPPORTS_LABELS_INCORRECT',lambda: validate_release_decision(d2,x,r2,policy))
    # 11 VISUAL_UNUSABLE_AT_ACTUAL_OUTPUT_SIZE
    x=copy.deepcopy(c); x['machine_evidence']['visual_usable_actual_size']=False; r2,d2=rebind(x,dec)
    expect('VISUAL_UNUSABLE_AT_ACTUAL_OUTPUT_SIZE',lambda: validate_release_decision(d2,x,r2,policy))
    # 12 SOURCE_STRUCTURE_OR_FORMULA_DRIFT_IGNORED
    x=copy.deepcopy(c); x['machine_evidence']['source_structure_formula_fidelity']=False; refresh_candidate(x)
    assert 'SOURCE_STRUCTURE_OR_FORMULA_DRIFT_IGNORED' in machine_validate(x,cr,policy,root)['failures']
    # 13 RAW_PR157_USED_AS_RUNTIME_TEMPLATE
    expect('RAW_PR157_USED_AS_RUNTIME_TEMPLATE',lambda: build_release_decision(c,mg,rs,ref('PASS',True,True),policy))
    # 14 PR157_COMPARISON_RUN_BEFORE_HUMAN_GATES
    expect('PR157_COMPARISON_RUN_BEFORE_HUMAN_GATES',lambda: build_release_decision(c,mg,[],ref('PASS',False),policy))
    # 15 LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY
    expect('LEARNING_EFFECTIVENESS_CLAIMED_WITHOUT_STUDY',lambda: build_release_decision(c,mg,rs,ref(),policy,{'state':'VALIDATED','study_evidence_ref':None}))
    # 16 LEGACY_NONCONFORMING_REDOX_SNAPSHOT_RECEIVES_MATURE_PASS
    x=copy.deepcopy(c); x['candidate_class']='LEGACY_NONCONFORMING_REDOX'; refresh_candidate(x); r2=reviews(x)
    expect('LEGACY_NONCONFORMING_REDOX_SNAPSHOT_RECEIVES_MATURE_PASS',lambda: build_release_decision(x,mg,r2,ref(),policy))
    # 17 KNOWN_THIN_SMOKE_SPECIMEN_RECEIVES_MATURE_DESIGN_PASS
    x=copy.deepcopy(c); x['candidate_class']='KNOWN_THIN_SMOKE'; refresh_candidate(x); r2=reviews(x)
    expect('KNOWN_THIN_SMOKE_SPECIMEN_RECEIVES_MATURE_DESIGN_PASS',lambda: build_release_decision(x,mg,r2,ref(),policy))

    # 18 LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK
    x=copy.deepcopy(c); x['machine_evidence']['learner_internal_identifier_leaks']=1; refresh_candidate(x)
    assert 'LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK' in machine_validate(x,cr,policy,root)['failures']
    # 19 TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED
    x=copy.deepcopy(c); x['machine_evidence']['teaching_primitive_kinds_realized']=['A']; x['machine_evidence']['teaching_primitives_label_only']=['B','C','D','E','F','G','H']; refresh_candidate(x)
    assert 'TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED' in machine_validate(x,cr,policy,root)['failures']
    # 20 PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE
    x=copy.deepcopy(c); x['machine_evidence']['actual_placement_evidence']=False; refresh_candidate(x)
    assert 'PLANNED_PLACEMENT_PRESENTED_AS_PHYSICAL_EVIDENCE' in machine_validate(x,cr,policy,root)['failures']
    # 21 PLACEMENT_OUT_OF_PHYSICAL_BOUNDS
    x=copy.deepcopy(c); x['machine_evidence']['placement_bounds_violations']=2; refresh_candidate(x)
    assert 'PLACEMENT_OUT_OF_PHYSICAL_BOUNDS' in machine_validate(x,cr,policy,root)['failures']
    # 22 ORPHAN_CONTINUATION_FRAGMENT
    x=copy.deepcopy(c); x['machine_evidence']['orphan_continuations']=1; refresh_candidate(x)
    assert 'ORPHAN_CONTINUATION_FRAGMENT' in machine_validate(x,cr,policy,root)['failures']
    # 23 a mature decision cannot survive a learner-facing identifier leak
    x=copy.deepcopy(c); x['machine_evidence']['learner_internal_identifier_leaks']=1; refresh_candidate(x); r2=reviews(x)
    expect('LEARNER_FACING_INTERNAL_IDENTIFIER_LEAK',lambda: build_release_decision(x,{'status':'PASS','failures':[]},r2,ref(),policy))

print('CHEMISTRY C-L exact-product falsifiers = 23 PASS')
print('CHEMISTRY C-L machine gate = PASS; production release without authorized reviews = BLOCKED/2')
