from __future__ import annotations
import hashlib, re

def difficulty_packet(mode:str, AUTH):
    return {'schema_version':'7.0.0','kind':'INTRINSIC_DIFFICULTY','product_mode':mode,
            'dimensions':AUTH['difficulty']['dimensions'],'derived_badge':'MEDIUM','final_badge':'MEDIUM',
            'disagreement_reason':'','explicit_owner_confirmation':False}

def purpose_packet(mode:str):
    if mode=='CORE1A': return {'schema_version':'7.0.0','product_mode':mode,'observed_actions':['EXPLAIN','REPRESENT','JUSTIFY_OR_DERIVE','CONTRAST','MODELED_EXAMPLE'],'dominant_mode':'DECLARATIVE_REFERENCE','major_ttu_count':4,'learner_generated_major_ttu_count':1}
    if mode=='CORE1B': return {'schema_version':'7.0.0','product_mode':mode,'observed_actions':['PREDICT_OR_RETRIEVE','RECONSTRUCT','EXPLAIN_OR_JUSTIFY','VERIFY'],'dominant_mode':'CONSTRUCTIVE_TUTOR','major_ttu_count':5,'learner_generated_major_ttu_count':4}
    if mode=='CORE2A': return {'schema_version':'7.0.0','product_mode':mode,'observed_actions':['EXPERT_RECOGNITION','SETUP','FULL_SOLUTION','WHY_STEPS','VERIFY'],'dominant_mode':'GUIDED_REFERENCE','major_ttu_count':4,'learner_generated_major_ttu_count':1}
    return {'schema_version':'7.0.0','product_mode':mode,'observed_actions':['ATTEMPT','MODEL_OR_REPRESENTATION_CHOICE','FIRST_MOVE_COMMITMENT','JUSTIFY','VERIFY'],'dominant_mode':'OPEN_PROBLEM_TUTOR','major_ttu_count':5,'learner_generated_major_ttu_count':4}

def learner_fit(mode:str, qid:str, demand:int, support='GUIDED'):
    return {'schema_version':'7.0.0','product_mode':mode,'question_id':qid,'purpose':'REVISION','purpose_used':True,
            'task_demand_score':demand,'compiler_support':support,'fit_focus':['recognition','representation','model_selection'],
            'conditioning':{'mode':'OWNER_OVERRIDE','support_band':support,
                            'reason':'Validation fixture: learner knowledge unavailable; owner selects a review support profile.',
                            'knowledge_percent':None}}

def question_custody(q):
    return {'schema_version':'7.0.0','question_id':q['question_id'],'source_class':'SOURCE_FROZEN',
            'learner_visible_source':q['learner_visible_source'],'source_title':q['source_title'],
            'source_unit_or_chapter':q['source_unit_or_chapter'],'source_question_number':q['source_question_number'],
            'source_locator':q['source_locator'],'source_stem_hash':q['source_stem_hash'],'stem_identity_status':'EXACT',
            'answer_status':'CLOSED','answer_ref':q['answer_ref'],'canonical_solution_ref':q['canonical_solution_ref'],
            'verification_ref':q['verification_ref']}

def badge_packet(mode):
    if mode.startswith('CORE1'):
        badges=['BUCKET','CONCEPT','INTRINSIC_DIFFICULTY','PURPOSE','REPRESENTATION_TTU','LEARNER_ACTION']
    else:
        badges=['BUCKET','CONCEPT','TASK_DEMAND','PURPOSE','SOURCE','SUPPORT']
    return {'schema_version':'7.0.0','product_mode':mode,'learner_visible_badges':badges,'student_knowledge_percent_visible':False}

def norm_tokens(text): return re.findall(r"[a-z0-9]+", text.lower())
def ngrams(tokens,n=5): return set(tuple(tokens[i:i+n]) for i in range(max(0,len(tokens)-n+1)))
def lcs_words(a,b):
    A=norm_tokens(a); B=norm_tokens(b); best=0; prev={}
    for x in A:
        cur={}
        for j,y in enumerate(B,1):
            if x==y:
                cur[j]=prev.get(j-1,0)+1; best=max(best,cur[j])
        prev=cur
    return best

def nonfrozen_text(pages):
    return '\n'.join(b['text'] for p in pages for b in p['blocks'] if not b.get('frozen') and b['kind'] in {'PROSE','PROMPT','HELP','SOLUTION','TRAP','VERIFY'})

def similarity_packet(models):
    texts={k:nonfrozen_text(v) for k,v in models.items()}
    pairs=[]; max_overlap=0; max_run=0; keys=list(texts)
    for i in range(len(keys)):
      for j in range(i+1,len(keys)):
        a,b=keys[i],keys[j]; ga=ngrams(norm_tokens(texts[a])); gb=ngrams(norm_tokens(texts[b])); denom=max(1,min(len(ga),len(gb)))
        ov=len(ga&gb)/denom; run=lcs_words(texts[a],texts[b]); max_overlap=max(max_overlap,ov); max_run=max(max_run,run)
        pairs.append({'a':a,'b':b,'overlap':round(ov,4),'max_identical_run':run})
    return {'schema_version':'7.0.0','non_frozen_prose':{'exclusions_applied':True,'verbatim_5gram_overlap':round(max_overlap,4),'max_identical_contiguous_words':max_run},
            'generated_example_comparisons':[],
            'ab_comparisons':[
              {'relation_type':'PEDAGOGICAL_TRANSFORMATION','review_reason':'Core1A supplies canonical model; Core1B reconstructs it','components':{'example':.35,'representation':.45,'learner_action':.15,'sequence':.2}},
              {'relation_type':'PEDAGOGICAL_TRANSFORMATION','review_reason':'Frozen stem is exact by custody; the surrounding representation, learner action and sequence differ by A/B contract','components':{'example':1.0,'representation':.45,'learner_action':.15,'sequence':.2}}
            ],'pair_diagnostics':pairs}

def validate_source_hashes(QUESTIONS):
    for q in QUESTIONS.values():
        actual='sha256:'+hashlib.sha256(q['stem'].encode('utf-8')).hexdigest()
        if q.get('source_stem_hash') != actual:
            raise RuntimeError(f'SOURCE_STEM_HASH_DRIFT:{q["question_id"]}')

def validate_authority_and_pal(models, AUTH, QUESTIONS, CCBOM, POLICY, v7):
    validate_source_hashes(QUESTIONS)
    v7.validate_ccbom(CCBOM,POLICY)
    for mode in ('CORE1A','CORE1B'):
        v7.validate_difficulty(difficulty_packet(mode, AUTH),POLICY); v7.validate_purpose(purpose_packet(mode),POLICY); v7.validate_badges(badge_packet(mode),POLICY)
    for mode in ('CORE2A','CORE2B'):
        v7.validate_purpose(purpose_packet(mode),POLICY); v7.validate_badges(badge_packet(mode),POLICY)
    for q in QUESTIONS.values(): v7.validate_question_custody(question_custody(q),POLICY)
    for mode in ('CORE2A','CORE2B'):
        v7.validate_learner_fit(learner_fit(mode,'CHEM-C2A-SRC-U2Q15C',5,'GUIDED'),POLICY)
        v7.validate_learner_fit(learner_fit(mode,'CHEM-C2A-SRC-U2Q35',9,'GUIDED'),POLICY)
    sim=similarity_packet(models); v7.validate_similarity(sim,POLICY)
    return sim
