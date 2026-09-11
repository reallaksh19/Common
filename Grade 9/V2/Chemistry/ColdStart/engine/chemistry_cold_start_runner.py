#!/usr/bin/env python3
import argparse, copy, hashlib, json, sys
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve()
CHEM=HERE.parents[2]
REPO=HERE.parents[5]
sys.path[:0]=[
 str(CHEM/'AssessmentIntake'/'engine'),str(CHEM/'AssessmentReview'/'engine'),
 str(CHEM/'AssessmentScope'/'engine'),str(CHEM/'ReasoningSemantics'/'engine'),
 str(CHEM/'LearnerEvidence'/'engine'),str(CHEM/'LearnerStudy'/'engine'),
 str(CHEM/'CoreAuthoring'/'engine'),str(CHEM/'Representation'/'engine'),
 str(CHEM/'Core2Transfer'/'engine'),str(CHEM/'CoverageClosure'/'engine')]
from build_chemistry_assessment_intake import build as build_intake
from review_chemistry_assessment import build_review,load_registry as load_review_registry
from build_chemistry_scope import build_scope
from build_chemistry_reasoning_semantics import build_semantics
from infer_chemistry_learner_evidence import build_snapshot
from build_chemistry_learner_study_model import derive_study_scope,build_model
from build_chemistry_core1 import build_plan as build_core1,load_pck_registry
from build_chemistry_representations import build_bundle as build_representations
from build_chemistry_core2_transfer import build_plan as build_core2
from build_chemistry_coverage_closure import build_closure

ELIGIBLE='ELIGIBLE_IN_SCOPE'; OUT='OUT_OF_SCOPE'; UNRESOLVED='SOURCE_UNRESOLVED'

def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(o,field=None):
    x=copy.deepcopy(o)
    if field: x.pop(field,None)
    return hashlib.sha256(canonical(x).encode()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(code,detail=''): raise ValueError(f'{code}: {detail}' if detail else code)
def uniq(xs):
    out=[]
    for x in xs:
        if x not in out: out.append(x)
    return out

def repo_path(rel,repo_root=REPO): return Path(repo_root)/rel

def verify_manifest(manifest):
    if manifest.get('subject')!='CHEMISTRY': fail('COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY','manifest subject')
    if manifest.get('manifest_digest')!=digest(manifest,'manifest_digest'): fail('COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY','manifest digest')
    forbidden=set(manifest['runtime_input_contract']['forbidden'])
    required_forbidden={'ISSUE_HISTORY','CHAT_HISTORY','RAW_PR157','MANUAL_SOURCE_OBLIGATION_LEDGER','PREFILTERED_ELIGIBLE_EXTERNAL_SET','MANUAL_LEARNER_STUDY_MODEL','MANUAL_PROBLEM_FAMILY_MAP'}
    if not required_forbidden<=forbidden: fail('COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY','forbidden boundary incomplete')
    if {'ChemistrySourceObligationLedger','ChemistryExternalCorpusClassification','LearnerStudyModel'}-set(manifest['derived_not_runtime_inputs']): fail('GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED')
    if len(manifest['two_product_topology'])!=2: fail('THIRD_HANDOUT_PDF_CREATED')
    core=next((x for x in manifest['two_product_topology'] if x['product_id']=='CORE_STUDY_GUIDE'),None)
    if not core or 'APPENDIX_C_PRINTABLE_HANDOUT' not in core['required_sections']: fail('APPENDIX_C_MISSING_FROM_CORE1')
    return True

def load_authorities(manifest,repo_root=REPO):
    out={}; reads=[]
    for key,rel in manifest['authorities'].items():
        reads.append(rel)
        if rel.endswith('.json'): out[key]=load(repo_path(rel,repo_root))
        else: out[key]=rel
    return out,reads

def match_rules(text,rules):
    t=text.lower(); return [r for r in rules if any(s.lower() in t for s in r['match_any'])]

def rep_requirements(rep,policy):
    return sorted({label for key,label in policy['representation_key_to_requirement'].items() if rep.get(key)})

def rep_levels(rep):
    levels=[]
    figs=[str(x).lower() for x in rep.get('figures',[])]
    if any('particle' in x for x in figs): levels.append('PARTICULATE')
    if rep.get('observations') or rep.get('states') or any('particle' not in x for x in figs): levels.append('MACROSCOPIC')
    if rep.get('formulas') or rep.get('charges') or rep.get('structures') or rep.get('conditions') or not levels: levels.append('SYMBOLIC')
    return uniq(levels)

def prereqs(caps,authority):
    by={x['capability_id']:x for x in authority['capabilities']}; out=[]
    for c in caps:
        if c not in by: fail('MANUAL_PROBLEM_FAMILY_MAP_REQUIRED','unknown capability '+c)
        out+=by[c]['prerequisite_capability_refs']
    return uniq(out)

def topic_valid(topic,caprefs,conceptrefs,authority,scope):
    if topic is None:return False
    supplied={x['topic_id'] for x in scope['topics']}
    if topic not in supplied or topic not in authority['declared_topic_bindings']:return False
    b=authority['declared_topic_bindings'][topic]
    return set(caprefs)<=set(b['allowed_capability_refs']) and set(conceptrefs)<=set(b['allowed_concept_refs'])

def review_maps(review):
    return ({x['source_unit_ref']:x for x in review['source_reviews']},{x['item_ref']:x for x in review['question_reviews']})

def derive_source_ledger(source_set,scope,review,authority,policy):
    sr,_=review_maps(review); obs=[]
    for u in source_set['units']:
        text=u['heading']+' '+u['statement']
        rules=match_rules(text,policy['source_rules'])
        if not rules: fail('GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED','unmapped source '+u['source_unit_id'])
        caps=uniq([x for r in rules for x in r['capability_refs']]); concepts=uniq([x for r in rules for x in r['concept_refs']]); fams=uniq([r['problem_family_ref'] for r in rules]); topics=uniq([r['topic_hint'] for r in rules if r['topic_hint'] and topic_valid(r['topic_hint'],r['capability_refs'],r['concept_refs'],authority,scope)])
        blocked=sr.get(u['source_unit_id'],{}).get('source_integrity_state')=='REVIEW_REQUIRED'
        if blocked: status=UNRESOLVED; topics=[]; reason='Source-integrity review blocks automatic scope use.'
        elif topics: status=ELIGIBLE; reason='Derived from raw source wording/representation and canonical declared-topic authority.'
        else: status=OUT; reason='Source concept is present, but its canonical capability is outside the declared topic boundary.'
        cond=uniq(list(u['representation'].get('conditions',[]))+list(u.get('exceptions',[])))
        obs.append({'obligation_id':'CO-'+u['source_unit_id'],'source_ref':u['source_unit_id'],'source_page':u['source_page'],'source_locator':u['source_provenance']['source_locator'],'scope_status':status,'scope_reason':reason,'declared_topic_refs':topics,'canonical_concept_refs':concepts,'canonical_capability_refs':caps,'prerequisite_refs':prereqs(caps,authority),'representation_levels':rep_levels(u['representation']),'representation_requirements':rep_requirements(u['representation'],policy),'condition_model_refs':cond,'required_exceptions':list(u.get('exceptions',[])),'required_examples':list(u.get('examples',[])),'required_terminology':uniq([x for r in rules for x in r.get('required_terminology',[])]) ,'problem_family_refs':fams})
    return {'ledger_id':'CHEM-C-K-DERIVED-SOURCE-'+source_set['source_set_id'],'schema_version':'1.0.0','subject':'CHEMISTRY','source_set_ref':source_set['source_set_id'],'obligations':obs}

def item_records(question):
    yield question['question_id'],None,question['stem']
    for p in question['subparts']: yield f"{question['question_id']}.{p['part_id']}",p['part_id'],p['stem']

def fallback_question_rule(q,policy):
    if q['representation'].get('charges'): return next(r for r in policy['question_rules'] if r['rule_id']=='Q-FORMULA-CHARGE')
    if q['representation'].get('structures'): return next(r for r in policy['question_rules'] if r['rule_id']=='Q-STRUCTURE-SITE')
    if q['representation'].get('figures'): return next(r for r in policy['question_rules'] if r['rule_id']=='Q-APPARATUS')
    return None

def verification_for(fams):
    if 'QF-CONSERVATION-CHECK' in fams:return ['CHECK_ATOMS']
    if 'QF-CONDITION-PRESERVATION' in fams or 'QF-RULE-EXCEPTION-GATE' in fams:return ['CHECK_CONDITIONS']
    if 'QF-FORMULA-PARSING' in fams:return ['CHECK_SPECIES_IDENTITY']
    return ['VERIFY_RESULT']

def reasoning_roles_for(fams,item_text=''):
    if fams==['QF-PARTICLE-SYMBOLIC-TRANSLATION'] and 'representation level' in item_text.lower() and 'particle picture' not in item_text.lower():
        return ['IDENTIFY_REPRESENTATION_LEVEL']
    m={'QF-FORMULA-PARSING':['PARSE_FORMULA_OR_EQUATION','CLASSIFY'],'QF-PARTICLE-SYMBOLIC-TRANSLATION':['IDENTIFY_REPRESENTATION_LEVEL','TRANSLATE_REPRESENTATION','VERIFY_RESULT'],'QF-CONSERVATION-CHECK':['PARSE_FORMULA_OR_EQUATION','APPLY_CONSERVATION','CHECK_ATOMS'],'QF-CHANGE-EVIDENCE-CLASSIFICATION':['READ_GIVEN','COMPARE','CLASSIFY'],'QF-RULE-EXCEPTION-GATE':['SELECT_RULE_OR_MODEL','CHECK_CONDITION_OR_EXCEPTION'],'QF-CONDITION-PRESERVATION':['READ_GIVEN','CHECK_CONDITION_OR_EXCEPTION','INTERPRET_CHEMICAL_MEANING'],'QF-OBSERVATION-INFERENCE':['READ_GIVEN','INFER_FROM_OBSERVATION','VERIFY_RESULT'],'QF-APPARATUS-METHOD':['IDENTIFY_REPRESENTATION_LEVEL','SELECT_RULE_OR_MODEL'],'QF-STRUCTURE-SITE-READING':['IDENTIFY_CHEMICAL_ENTITIES','PARSE_FORMULA_OR_EQUATION'],'QF-OXIDATION-STATE-TRACKING':['PARSE_FORMULA_OR_EQUATION','TRACK_SPECIES_OR_STATE_CHANGE'],'QF-SPECIES-ROLE':['IDENTIFY_CHEMICAL_ENTITIES','TRACK_SPECIES_OR_STATE_CHANGE','CLASSIFY'],'QF-VERIFICATION':['VERIFY_RESULT']}
    return uniq([x for f in fams for x in m.get(f,[])])

def derive_question_bindings(question_set,scope,review,authority,policy):
    _,qr=review_maps(review); bindings=[]
    unresolved_signals=[x.lower() for x in policy['unresolved_question_text_signals']]
    for q in question_set['questions']:
        for item_ref,part_ref,item_text in item_records(q):
            rules=match_rules(item_text,policy['question_rules'])
            if part_ref is None and q['subparts']:
                for p in q['subparts']: rules+=match_rules(p['stem'],policy['question_rules'])
            if not rules:
                fb=fallback_question_rule(q,policy); rules=[fb] if fb else []
            if not rules: fail('GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED','unmapped question '+item_ref)
            rules=uniq(rules); caps=uniq([x for r in rules for x in r['capability_refs']]); concepts=uniq([x for r in rules for x in r['concept_refs']]); fams=uniq([r['problem_family_ref'] for r in rules]); topic_hints=uniq([r['topic_hint'] for r in rules if r['topic_hint'] and topic_valid(r['topic_hint'],r['capability_refs'],r['concept_refs'],authority,scope)])
            rv=qr.get(item_ref,{})
            blocked=rv.get('validity_state')=='REVIEW_REQUIRED' or rv.get('source_integrity_state')=='REVIEW_REQUIRED' or any(s in q['stem'].lower() for s in unresolved_signals)
            if blocked: status=UNRESOLVED; primary=None; reason='Item fails closed because source/validity review or extraction uncertainty is unresolved.'
            elif topic_hints: status=ELIGIBLE; primary=('REACTION' if part_ref is None and q['subparts'] and 'REACTION' in topic_hints else topic_hints[0]); reason='Derived from raw question evidence and canonical declared-topic authority.'
            else: status=OUT; primary=None; reason='Question capability is outside the declared topic boundary.'
            cond=list(q['representation'].get('conditions',[]))
            if 'QF-RULE-EXCEPTION-GATE' in fams and not cond: cond=['EXPLICIT_EXCEPTION']
            entities=uniq(list(q['representation'].get('formulas',[]))+list(q['representation'].get('structures',[])))
            bindings.append({'item_ref':item_ref,'question_ref':q['question_id'],'part_ref':part_ref,'scope_status':status,'scope_reason':reason,'declared_topic_refs':topic_hints if status==ELIGIBLE else [],'primary_learner_unit':primary,'canonical_concept_refs':concepts,'canonical_capability_refs':caps,'prerequisite_capability_refs':prereqs(caps,authority),'problem_family_refs':fams,'reasoning_role_expectations':reasoning_roles_for(fams,item_text),'representation_levels':rep_levels(q['representation']),'representation_demands':rep_requirements(q['representation'],policy),'chemical_entity_refs':entities,'conditions_exceptions':cond,'conservation_obligations':['ATOM_COUNT'] if 'QF-CONSERVATION-CHECK' in fams else [],'process_reaction_property_refs':[],'verification_obligations':verification_for(fams)})
    return {'binding_registry_id':'CHEM-C-K-DERIVED-QUESTION-BINDINGS-'+question_set['question_set_id'],'schema_version':'1.0.0','subject':'CHEMISTRY','question_set_ref':question_set['question_set_id'],'bindings':bindings}

def body_map(source_bodies): return {x['candidate_id']:x for x in source_bodies['records']}

def external_representation_demands(fams,body):
    by_family={'QF-FORMULA-PARSING':['FORMULA','IONIC_CHARGE'],'QF-PARTICLE-SYMBOLIC-TRANSLATION':['FIGURE','FORMULA'],'QF-CONSERVATION-CHECK':['FORMULA'],'QF-CONDITION-PRESERVATION':['CONDITION'],'QF-SPECIES-ROLE':['FORMULA']}
    out=uniq([x for f in fams for x in by_family.get(f,[])])
    if body.get('figure_required') and 'FIGURE' not in out: out.append('FIGURE')
    if body.get('condition_text') and 'CONDITION' not in out: out.append('CONDITION')
    return out

def derive_external_classification(corpus,scope,authority,policy,source_bodies):
    bodies=body_map(source_bodies); rows=[]
    for c in sorted(corpus['candidates'],key=lambda x:x['source_order']):
        body=bodies.get(c['candidate_id']); text=c['source_title']+' '+(body['stem'] if body else '')
        rules=match_rules(text,policy['external_rules'])
        if not body or not rules or c['extraction_confidence']<policy['low_confidence_threshold']:
            rows.append({'candidate_id':c['candidate_id'],'scope_status':UNRESOLVED,'scope_reason':'External candidate body or extraction confidence is insufficient for source-grounded classification.','declared_topic_refs':[],'primary_learner_unit':None,'canonical_concept_refs':[],'canonical_capability_refs':[],'prerequisite_capability_refs':[],'problem_family_refs':[],'representation_levels':[],'representation_demands':[],'eligibility_basis':policy['eligibility_basis']}); continue
        caps=uniq([x for r in rules for x in r['capability_refs']]); concepts=uniq([x for r in rules for x in r['concept_refs']]); fams=uniq([r['problem_family_ref'] for r in rules]); topics=uniq([r['topic_hint'] for r in rules if r['topic_hint'] and topic_valid(r['topic_hint'],r['capability_refs'],r['concept_refs'],authority,scope)])
        if topics: status=ELIGIBLE; primary=topics[0]; reason='Eligibility derived from resolved source body plus canonical declared-topic authority; provider topic label is not authority.'
        else: status=OUT; primary=None; reason='Resolved external question requires Chemistry capability outside declared scope.'
        levels=['PARTICULATE','SYMBOLIC'] if body.get('figure_required') and body.get('figure_semantic',{}).get('model')=='PARTICLE_COUNT' else ['SYMBOLIC']
        rows.append({'candidate_id':c['candidate_id'],'scope_status':status,'scope_reason':reason,'declared_topic_refs':topics if status==ELIGIBLE else [],'primary_learner_unit':primary,'canonical_concept_refs':concepts,'canonical_capability_refs':caps,'prerequisite_capability_refs':prereqs(caps,authority),'problem_family_refs':fams,'representation_levels':levels,'representation_demands':external_representation_demands(fams,body),'eligibility_basis':policy['eligibility_basis']})
    return {'classification_id':'CHEM-C-K-DERIVED-EXTERNAL-'+corpus['corpus_id'],'schema_version':'1.0.0','subject':'CHEMISTRY','corpus_ref':corpus['corpus_id'],'classifications':rows}

def validate_source_correction_custody(source_set,qc_registry):
    known={x.get('event_id') for x in qc_registry.get('events',[])}
    for u in source_set['units']:
        for ev in u['source_provenance'].get('human_correction_events',[]):
            ref=ev if isinstance(ev,str) else ev.get('event_id')
            if ref not in known: fail('SOURCE_DAMAGE_FIXED_WITHOUT_REVIEW_EVENT',u['source_unit_id'])
    return True

def validate_runtime_reads(manifest,reads,manual_inputs=None):
    manual_inputs=list(manual_inputs or [])
    low=[x.lower() for x in reads]; forbidden=[]
    for raw in reads:
        if any(f.lower() in raw.lower() for f in manifest['forbidden_runtime_path_fragments']): forbidden.append(raw)
    if any('issue' in x for x in low) or any('chat' in x or 'conversation' in x for x in low): fail('COLD_START_REQUIRES_CHAT_OR_ISSUE_HISTORY')
    if any('pull/157' in x or 'pr157' in x for x in low): fail('RAW_PR157_READ_DURING_PRODUCTION')
    if 'ChemistrySourceObligationLedger' in manual_inputs: fail('GENERATION_STARTS_AFTER_SOURCE_OBLIGATIONS_WERE_MANUALLY_EXTRACTED')
    if 'PrefilteredEligibleExternalSet' in manual_inputs: fail('GENERATION_STARTS_FROM_PREFILTERED_ELIGIBLE_PYQS')
    if 'LearnerStudyModel' in manual_inputs: fail('MANUAL_STUDYMODEL_REQUIRED')
    if 'ProblemFamilyMap' in manual_inputs: fail('MANUAL_PROBLEM_FAMILY_MAP_REQUIRED')
    return {'runtime_reads':reads,'forbidden_reads':forbidden,'manual_precomputed_inputs_used':manual_inputs,'chat_or_issue_history_used':False,'raw_pr157_used':False}

def make_package(core1,core2,manifest,run_id):
    products=[]
    titles={'CORE_STUDY_GUIDE':'Core Study Guide','EXAMSIDE_SOLUTION_TRANSFER_BOOK':'ExamSIDE Solution & Transfer Book'}
    sources={'CORE_STUDY_GUIDE':(core1['plan_id'],core1['plan_digest']),'EXAMSIDE_SOLUTION_TRANSFER_BOOK':(core2['plan_id'],core2['plan_digest'])}
    for spec in manifest['two_product_topology']:
        ref,sd=sources[spec['product_id']]
        ident=digest({'product_id':spec['product_id'],'semantic_source_digest':sd,'required_sections':spec['required_sections'],'run_id':run_id})
        products.append({'product_id':spec['product_id'],'learner_title':titles[spec['product_id']],'media_type':'application/pdf','required_sections':list(spec['required_sections']),'semantic_source_ref':ref,'semantic_source_digest':sd,'candidate_identity_sha256':ident,'identity_class':'FROZEN_SEMANTIC_CANDIDATE','render_state':'NOT_RENDERED_C_K_SEMANTIC_CANDIDATE','rendered_byte_sha256':None})
    out={'package_id':'PKG-'+run_id,'schema_version':'1.0.0','subject':'CHEMISTRY','products':products,'product_count':len(products),'third_product_created':False,'package_digest':''}
    out['package_digest']=digest(out,'package_digest'); return out

def trace(tid,cls,subject,resolution,refs): return {'trace_id':tid,'decision_class':cls,'subject_ref':subject,'resolution':resolution,'authority_refs':uniq(refs)}

def build_authority_trace(source_ledger,external,model,core1,reps,core2,closure,manifest):
    out=[]; deriv=manifest['authorities']['derivation_policy']; canon=manifest['authorities']['canonical_chemistry']
    for o in source_ledger['obligations']:
        out.append(trace('TR-SRC-'+o['obligation_id'],'CONCEPT_SOURCE_INCLUSION',o['obligation_id'],o['scope_status']+': '+o['scope_reason'],[o['source_locator'],deriv,canon]))
    for e in external['classifications']:
        out.append(trace('TR-EXT-'+e['candidate_id'],'EXTERNAL_ELIGIBILITY',e['candidate_id'],e['scope_status']+': '+e['scope_reason'],[deriv,canon,manifest['authorities']['external_source_body_resolver']]))
    lby={x['capability_ref']:x for x in core1['lessons']}; rby=defaultdict(list)
    for r in reps['representations']: rby[r['capability_ref']].append(r)
    long={x['capability_ref']:x for x in closure['longitudinal_update']['records']}
    for m in model['capability_records']:
        cap=m['capability_ref']; lesson=lby[cap]
        out.append(trace('TR-TREAT-'+cap,'TREATMENT_DEPTH',cap,f"{m['learner_state']} -> {m['treatment']} -> {lesson['lesson_mode']}",[manifest['authorities']['treatment_policy'],model['study_model_id']]))
        out.append(trace('TR-REP-'+cap,'REPRESENTATION_CHOICE',cap,'Semantic primitives selected from capability, learner treatment and representation obligations.',[manifest['authorities']['teaching_primitives'],manifest['authorities']['page_intent']]+[x['representation_id'] for x in rby[cap]]))
        out.append(trace('TR-COND-'+cap,'CONDITION_EXCEPTION_EXPLANATION',cap,'Condition/exception obligations preserved from the study model; empty means no additional condition is authorized.',[canon,model['study_model_id']]))
        out.append(trace('TR-WORK-'+cap,'WORKED_EXAMPLE',cap,'Core1 uses a new authored problem-family instance and does not leak the original external transfer item.',[manifest['authorities']['problem_authoring'],manifest['authorities']['promoted_pck'],lesson['lesson_id']]))
        out.append(trace('TR-APPA-'+cap,'APPENDIX_A_ITEM',cap,'Appendix A item is generated from the required capability and authorized problem family.',[manifest['authorities']['problem_authoring'],core1['plan_id']]))
        out.append(trace('TR-APPC-'+cap,'APPENDIX_C_ELEMENT',cap,'Appendix C support is a compact answer-free first-move/rule/verification cue for an already authorized capability.',[manifest['authorities']['core1_completeness'],core1['plan_id']]))
        lo=long[cap]
        out.append(trace('TR-LONG-'+cap,'LONGITUDINAL_REVISIT',cap,'Future evidence obligations remain assigned after the current episode: '+', '.join(lo['remaining_future_evidence_obligations']),[manifest['authorities']['post_transfer_evidence_policy'],closure['closure_id']]))
    for p in core2['pages']:
        q=p['question_ref']
        out.append(trace('TR-PLACE-'+q,'CORE2_PLACEMENT',q,'Eligible original external question placed once in its canonical primary home.',[external['classification_id'],core2['plan_id']]))
        out.append(trace('TR-CONCEPT-'+q,'PRIMARY_SUPPORTS',q,'PRIMARY and SUPPORTS are taken from the concept-segregation authority and canonical capability bindings.',[manifest['authorities']['concept_segregation'],canon]))
        out.append(trace('TR-BADGE-'+q,'BADGE',q,'Guide reasoning-demand and transfer/source badges use versioned policy; guide demand is not psychometric difficulty.',[manifest['authorities']['demand_badges'],manifest['authorities']['transfer_badges']]))
        out.append(trace('TR-HINT-'+q,'HINTS',q,'H1 notice, H2 rule/model/representation and H3 first executable step are generated under the Core2 support contract.',[manifest['authorities']['core2_profile'],p['problem_family_ref']]))
        out.append(trace('TR-ROUTE-'+q,'REASONING_ROUTE',q,'ChemistryReasoningRoute comes from problem-family semantics and remains distinct from the hint ladder.',[manifest['authorities']['problem_families'],p['reasoning_route_ref']]))
        out.append(trace('TR-VERIFY-'+q,'VERIFICATION',q,'Verification is taken from the authorized problem-family/solution route and preserves chemical checks.',[manifest['authorities']['problem_families'],q]))
    return out

def signature(rows,fields): return digest([{k:r.get(k) for k in fields} for r in rows])

def run_cold_start(source_set,question_set,corpus,topic_scope,attempt_set=None,evidence_ledger=None,repo_root=REPO,run_id=None,runtime_read_log=None,manual_precomputed_inputs=None):
    manifest=load(repo_path('Grade 9/V2/Chemistry/CHEMISTRY_GENERATION_AUTHORITY_MANIFEST.json',repo_root)); verify_manifest(manifest)
    authorities,reads=load_authorities(manifest,repo_root); reads=['INPUT:ChemistrySourceSet','INPUT:QuestionSetOrCorpusSet','INPUT:DeclaredTopicScope']+(['INPUT:AttemptSet'] if attempt_set else [])+reads+list(runtime_read_log or [])
    audit=validate_runtime_reads(manifest,reads,manual_precomputed_inputs); validate_source_correction_custody(source_set,authorities['qc_events'])
    rid=run_id or ('CHEM-C-K-RUN-B' if attempt_set else 'CHEM-C-K-RUN-A')
    intake=build_intake(copy.deepcopy(source_set),copy.deepcopy(question_set),copy.deepcopy(corpus),copy.deepcopy(topic_scope),copy.deepcopy(attempt_set) if attempt_set else None,'INTAKE-'+rid)
    review_reg,review_manifest_digest=load_review_registry(repo_path(manifest['authorities']['review_registry'],repo_root))
    review=build_review(copy.deepcopy(source_set),copy.deepcopy(question_set),review_reg,copy.deepcopy(authorities['review_policy']),copy.deepcopy(authorities['qc_events']),registry_manifest_digest=review_manifest_digest)
    policy=authorities['derivation_policy']; canonical_authority=authorities['canonical_chemistry']; bodies=authorities['external_source_body_resolver']
    source_ledger=derive_source_ledger(source_set,topic_scope,review,canonical_authority,policy)
    qbindings=derive_question_bindings(question_set,topic_scope,review,canonical_authority,policy)
    external=derive_external_classification(corpus,topic_scope,canonical_authority,policy,bodies)
    scope_bundle=build_scope(copy.deepcopy(source_set),copy.deepcopy(question_set),copy.deepcopy(corpus),copy.deepcopy(topic_scope),copy.deepcopy(review),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(canonical_authority),'SCOPE-'+rid)
    semantics=build_semantics(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(authorities['problem_families']),copy.deepcopy(authorities['reasoning_roles']),copy.deepcopy(authorities['demand_badges']))
    snapshot=build_snapshot(copy.deepcopy(scope_bundle),copy.deepcopy(review),copy.deepcopy(semantics),copy.deepcopy(question_set),copy.deepcopy(authorities['learner_observations']),copy.deepcopy(authorities['diagnostic_policy']),copy.deepcopy(attempt_set) if attempt_set else None,copy.deepcopy(evidence_ledger) if attempt_set else None)
    study_scope=derive_study_scope(copy.deepcopy(scope_bundle),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external))
    model=build_model(copy.deepcopy(study_scope),copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(external),copy.deepcopy(semantics),copy.deepcopy(snapshot),copy.deepcopy(authorities['treatment_policy']),'STUDY-'+rid)
    pck=load_pck_registry(repo_path(manifest['authorities']['promoted_pck'],repo_root))
    core1=build_core1(copy.deepcopy(model),copy.deepcopy(study_scope),copy.deepcopy(pck),copy.deepcopy(authorities['core1_profile']),copy.deepcopy(authorities['core1_completeness']),copy.deepcopy(authorities['problem_authoring']),'CORE1-'+rid)
    representations=build_representations(copy.deepcopy(core1),copy.deepcopy(model),copy.deepcopy(authorities['teaching_primitives']),copy.deepcopy(authorities['page_intent']),copy.deepcopy(authorities['notation']),'REP-'+rid)
    core2=build_core2(copy.deepcopy(corpus),copy.deepcopy(external),copy.deepcopy(bodies),copy.deepcopy(core1),copy.deepcopy(model),copy.deepcopy(authorities['problem_families']),copy.deepcopy(authorities['demand_badges']),copy.deepcopy(authorities['transfer_badges']),copy.deepcopy(authorities['concept_segregation']),copy.deepcopy(authorities['core2_profile']),copy.deepcopy(authorities['teaching_primitives']),copy.deepcopy(authorities['notation']),'CORE2-'+rid)
    transfer_events=copy.deepcopy(authorities['post_transfer_fixture']['events']); closure=build_closure(copy.deepcopy(source_ledger),copy.deepcopy(qbindings),copy.deepcopy(corpus),copy.deepcopy(external),copy.deepcopy(model),copy.deepcopy(core1),copy.deepcopy(representations),copy.deepcopy(core2),copy.deepcopy(authorities['problem_families']),transfer_events,copy.deepcopy(authorities['post_transfer_evidence_policy']),'CLOSURE-'+rid)
    package=make_package(core1,core2,manifest,rid); traces=build_authority_trace(source_ledger,external,model,core1,representations,core2,closure,manifest)
    required=set(manifest['required_authority_trace_decisions']); got={x['decision_class'] for x in traces}
    if not required<=got or any(not x['authority_refs'] or x['resolution'].strip().lower()=='agent decided' for x in traces): fail('FINAL_PAGE_DECISION_WITHOUT_AUTHORITY_TRACE')
    derived={'source_ledger_digest':digest(source_ledger),'question_bindings_digest':digest(qbindings),'external_classification_digest':digest(external),'derivation_policy_ref':policy['policy_id']}
    stage={'intake_digest':intake['intake_digest'],'review_digest':digest(review),'scope_bundle_digest':digest(scope_bundle),'reasoning_semantics_digest':digest(semantics),'study_scope_digest':study_scope['study_scope_digest'],'study_model_digest':model['study_model_digest'],'core1_plan_digest':core1['plan_digest'],'representation_bundle_digest':representations['bundle_digest'],'core2_plan_digest':core2['plan_digest'],'coverage_closure_digest':closure['closure_digest'],'source_obligation_refs':sorted(x['obligation_id'] for x in source_ledger['obligations']),'external_candidate_refs':sorted(x['candidate_id'] for x in external['classifications']),'scope_classification_signature':digest({'source':[(x['obligation_id'],x['scope_status']) for x in source_ledger['obligations']],'questions':[(x['item_ref'],x['scope_status']) for x in qbindings['bindings']],'external':[(x['candidate_id'],x['scope_status']) for x in external['classifications']]}),'canonical_binding_signature':digest({'source':[(x['obligation_id'],x['canonical_concept_refs'],x['canonical_capability_refs']) for x in source_ledger['obligations']],'questions':[(x['item_ref'],x['canonical_concept_refs'],x['canonical_capability_refs']) for x in qbindings['bindings']],'external':[(x['candidate_id'],x['canonical_concept_refs'],x['canonical_capability_refs']) for x in external['classifications']]}),'problem_family_truth_signature':digest({'source':[(x['target_ref'],x['problem_family_ref']) for x in semantics['source_semantics']],'questions':[(x['target_ref'],x['problem_family_ref']) for x in semantics['question_semantics']]}),'primary_external_ownership_signature':digest([(p['question_ref'],p['primary_concept_ref'],p['primary_capability_ref']) for p in core2['pages']]),'canonical_chemistry_truth_signature':digest(canonical_authority),'learner_state_signature':digest([(x['capability_ref'],x['learner_state']) for x in model['capability_records']]),'treatment_signature':digest([(x['capability_ref'],x['treatment']) for x in model['capability_records']]),'support_path_signature':digest([(x['capability_ref'],x['lesson_mode']) for x in core1['lessons']])}
    summary={'source_unit_count':len(source_set['units']),'question_count':len(question_set['questions']),'external_candidate_count':len(corpus['candidates']),'eligible_external_count':sum(x['scope_status']==ELIGIBLE for x in external['classifications']),'core1_required_capability_count':len(model['capability_records']),'core2_page_count':len(core2['pages']),'appendix_a_present':core1['appendices']['appendix_a']['present'],'appendix_b_present':core1['appendices']['appendix_b']['present'],'appendix_c_present':core1['appendices']['appendix_c']['present'],'product_count':package['product_count'],'authority_trace_complete':True,'cold_start_status':'PASS'}
    report={'run_id':rid,'schema_version':'1.0.0','subject':'CHEMISTRY','run_mode':'ATTEMPT_PRESENT' if attempt_set else 'NO_ATTEMPT','manifest_ref':manifest['manifest_id'],'manifest_digest':manifest['manifest_digest'],'input_custody':{'source_set_digest':source_set['source_set_digest'],'question_set_digest':question_set['question_set_digest'],'corpus_digest':corpus['corpus_digest'],'declared_topic_scope_digest':topic_scope['scope_digest'],'attempt_set_digest':attempt_set['attempt_set_digest'] if attempt_set else None},'derived_authority':derived,'stage_outputs':stage,'authority_trace':traces,'two_product_package':package,'runtime_dependency_audit':audit,'summary':summary,'report_digest':''}
    report['report_digest']=digest(report,'report_digest')
    internal={'intake':intake,'review':review,'source_ledger':source_ledger,'question_bindings':qbindings,'external_classification':external,'scope_bundle':scope_bundle,'semantics':semantics,'learner_snapshot':snapshot,'study_scope':study_scope,'study_model':model,'core1':core1,'representations':representations,'core2':core2,'closure':closure}
    return report,internal

def compare_runs(a,b,comparison_id='CHEM-C-K-RUN-A-B-COMPARISON-v1'):
    def eq(path):
        xa=a; xb=b
        for k in path: xa=xa[k]; xb=xb[k]
        return xa==xb
    inv={'source_set_digest_identical':eq(['input_custody','source_set_digest']),'question_set_digest_identical':eq(['input_custody','question_set_digest']),'corpus_digest_identical':eq(['input_custody','corpus_digest']),'declared_topic_scope_digest_identical':eq(['input_custody','declared_topic_scope_digest']),'source_obligation_denominator_identical':eq(['stage_outputs','source_obligation_refs']),'external_candidate_denominator_identical':eq(['stage_outputs','external_candidate_refs']),'scope_classification_identical':eq(['stage_outputs','scope_classification_signature']),'canonical_bindings_identical':eq(['stage_outputs','canonical_binding_signature']),'problem_family_truth_identical':eq(['stage_outputs','problem_family_truth_signature']),'primary_question_ownership_identical':eq(['stage_outputs','primary_external_ownership_signature']),'canonical_chemistry_truth_identical':eq(['stage_outputs','canonical_chemistry_truth_signature'])}
    if not all(inv.values()):
        if not inv['scope_classification_identical']: fail('ATTEMPT_RUN_CHANGES_EXTERNAL_ELIGIBILITY')
        if not inv['primary_question_ownership_identical']: fail('ATTEMPT_RUN_CHANGES_PRIMARY_QUESTION_OWNERSHIP')
        if not inv['canonical_chemistry_truth_identical']: fail('ATTEMPT_RUN_CHANGES_CANONICAL_CHEMISTRY_TRUTH')
        fail('ATTEMPT_RUN_CHANGES_REQUIRED_SCOPE')
    out={'comparison_id':comparison_id,'schema_version':'1.0.0','subject':'CHEMISTRY','run_a_ref':a['run_id'],'run_b_ref':b['run_id'],'invariants':inv,'authorized_differences':{'learner_state_may_differ':True,'treatment_may_differ':True,'support_path_may_differ':True,'difference_basis':'ATTEMPTSET_EVIDENCE_ONLY'},'comparison_status':'PASS','comparison_digest':''}
    out['comparison_digest']=digest(out,'comparison_digest'); return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sources',required=True); ap.add_argument('--questions',required=True); ap.add_argument('--corpus',required=True); ap.add_argument('--topic-scope',required=True); ap.add_argument('--attempts'); ap.add_argument('--evidence-ledger'); ap.add_argument('--out',required=True); ap.add_argument('--run-id'); a=ap.parse_args()
    report,_=run_cold_start(load(a.sources),load(a.questions),load(a.corpus),load(a.topic_scope),load(a.attempts) if a.attempts else None,load(a.evidence_ledger) if a.evidence_ledger else None,REPO,a.run_id)
    Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if __name__=='__main__': main()
