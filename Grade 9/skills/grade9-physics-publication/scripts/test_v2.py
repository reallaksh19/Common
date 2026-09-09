#!/usr/bin/env python3
"""Targeted negative tests: the known failure modes must remain blocked."""
import copy,json
from pathlib import Path
from jsonschema import Draft202012Validator
from validate_v2 import validate,areas
SKILL_ROOT=Path(__file__).resolve().parents[1]
d=json.loads((SKILL_ROOT/'examples/motion_B30_v2.json').read_text(encoding='utf-8'))
def drop_diagram(x):del x['lessons'][0]['figure']
def placeholder(x):x['lessons'][0]['figure']['status']='PLACEHOLDER'
def nohandout(x):del x['handout']
def wrongnumber(x):x['questions']['core_calibrated'][0]['numeric_check']['distance']=999
def brokenrepair(x):x['questions']['core_calibrated'][0]['repair_target']='missing'
def nographtask(x):x['questions']['core_calibrated'][5]['figure']=None
def mismatch(x):x['questions']['core_calibrated'][5]['figure']['segments'][0][1]=3
def duplicate(x):x['questions']['core_calibrated'][1]['id']=x['questions']['core_calibrated'][0]['id']
def repeatedhint(x):x['questions']['core_calibrated'][0]['hints'][1]['text']=x['questions']['core_calibrated'][0]['hints'][0]['text']
def hinttierbroken(x):x['questions']['core_calibrated'][0]['hints'][0]['tier']='H2'  # H2,H2,H3: not the required H1->H2->H3 progression
def denominator(x):x['questions']['core_calibrated'].pop()
def unknown(x):x['unrendered_hidden_field']='must fail'
def missingregion(x):x['questions']['core_calibrated'][5]['figure']['segments'].pop()
def missingcitation(x):
    q=x['questions']['core_calibrated'][0]
    q.update(source_status='SOURCE_VERIFIED',provenance_class='OFFICIAL_PYQ',transcription_status='VERIFIED_TRANSCRIPTION')
def sruselfattest(x):x['concepts'][0]['sru']={'no_naked_equation':True}  # no reviewer set: must be rejected
def mixedtestbadconcept(x):x['mixed_tests'][0]['diagnosis_map'][x['mixed_tests'][0]['question_ids'][0]]=x['concepts'][0]['concept_id']
def mixedtestunknownq(x):x['mixed_tests'][0]['question_ids'].append('B30-A99')
def mixedtestexposescues(x):x['mixed_tests'][0]['concept_hidden']=False
def methodterse(x):x['questions']['core_calibrated'][0]['solution']['method']='Distance 8 m displacement −2.'
def methodformulaonly(x):
    q=x['questions']['core_calibrated'][0];parts=q['solution']['answer'].split()
    q['solution']['method']=' '.join(parts[:max(1,len(parts)//2)])  # a truncated prefix: no vocabulary beyond the answer
def methodneardup(x):q=x['questions']['core_calibrated'][0];q['solution']['method']=q['solution']['answer']+' so.'
def depclassmismatch(x):x['lessons'][0]['figure']['dependency_class']='TABLE'  # a numberline is NUMBER_LINE, not TABLE
def unknowncanonical(x):x['concepts'][0]['canonical_concept_id']='CB99'
def registrysetdrift(x):x['canonical_concept_registry']['allowed_ids'].append('CB99')
def releasewithoutqa(x):x['status']='RELEASE_CANDIDATE'
for fn in [drop_diagram,placeholder,nohandout,wrongnumber,brokenrepair,nographtask,mismatch,duplicate,repeatedhint,hinttierbroken,denominator,unknown,missingregion,missingcitation,sruselfattest,mixedtestbadconcept,mixedtestunknownq,mixedtestexposescues,methodterse,methodformulaonly,methodneardup,depclassmismatch,unknowncanonical,registrysetdrift,releasewithoutqa]:
    v=copy.deepcopy(d);fn(v)
    try:validate(v)
    except (AssertionError,ValueError):print('REJECTED',fn.__name__)
    else:raise AssertionError('Unexpected acceptance: '+fn.__name__)
assert areas([[0,6,4,-2]])==(10,8),'crossing inside unsplit segment'
assert areas([[0,-3,2,-3]])==(6,-6),'negative rectangle'
assert areas([[0,0,3,0]])==(0,0),'rest'
validate(d)
print('25 negative cases rejected; three physics boundary cases and positive model passed.')
# Master-schema compatibility is part of the normal committed test chain, not a one-off command.
master=json.loads((SKILL_ROOT.parents[1]/'shared/grade9-master.schema.json').read_text(encoding='utf-8'))
master_validator=Draft202012Validator(master)
for model_path in sorted((SKILL_ROOT/'examples').glob('motion_*_v2.json')):
    errors=list(master_validator.iter_errors(json.loads(model_path.read_text(encoding='utf-8'))))
    assert not errors,f'{model_path.name}: master-schema drift: {errors[0].message}'
print('All three example models conform to grade9-master.schema.json.')
# Synthetic source-link fixture tests plumbing, not attribution or an actual exam.
import tempfile
from render_v2 import Book
from audit_v2 import audit
v=copy.deepcopy(d);q=v['questions']['core_calibrated'][0];q['source_status']='ADAPTED';q['transcription_status']='VERIFIED_TRANSCRIPTION';q['provenance_class']='OFFICIAL_PYQ'
q['source_citation']={'title':'TEST FIXTURE — not an exam source','url':'https://example.org/physics-test-fixture','locator':'synthetic test only','verification':'VERIFIED','source_document':'synthetic-fixture.pdf','source_sha256':'0'*64,'source_page':1,'raw_stem':q['question'],'raw_answer':q['answer'],'values_units':['synthetic'], 'options':[],'figure_locator':None,'figure_semantics':[],'target_ids':[q['id']],'adaptation_note':'Fixture tests independent provenance/adaptation and citation rendering; no source-truth claim.'}
validate(v)
with tempfile.TemporaryDirectory(dir=Path.cwd()) as td:
    p=Path(td);(p/'model.json').write_text(json.dumps(v),encoding='utf-8')
    out=Book(v,p/'book.pdf').render();(p/'book.layout.json').write_text(json.dumps(out),encoding='utf-8')
    result=audit(p/'model.json',p/'book.pdf')
    assert len(out['external_links'])==2 and not result['text_overlap_findings'],'external citation rendering'
print('Synthetic citation fixture: question and solution URI links verified in actual PDF.')
# Product profiles must survive validate, render and audit with their repair routes intact.
tb=copy.deepcopy(d);tb.update(product='transfer_book',lessons=[],lesson_ids=[],handout=None,guided_solutions=[])
for q in tb['questions']['core_calibrated']:
    q.update(repair_mode='EXTERNAL_COMPANION',repair_target='EXTERNAL-CORE-LESSON',repair_reference={'title':'Companion Motion Core','url':'https://example.org/motion-core','locator':'Lesson 1'})
validate(tb)
sg=copy.deepcopy(d);sg.update(product='study_guide',questions={'anchors':[],'core_calibrated':[],'challenges':[]},frozen_questions=0,mixed_tests=[])
for p in sg['lessons']:p['practice_ids']=[]  # a zero-question study_guide cannot link practice questions it doesn't carry
validate(sg)
print('Product profile: transfer_book (no lessons) and study_guide (no questions) both validate independently.')
# Validating is not rendering: prove both profiles actually render without crashing (this is exactly how
# the product=='core'-only gates in render_v2.py's handout/question_page logic were caught and fixed).
with tempfile.TemporaryDirectory(dir=Path.cwd()) as td:
    p=Path(td)
    (p/'tb.json').write_text(json.dumps(tb),encoding='utf-8');tb_out=Book(tb,p/'tb.pdf').render();(p/'tb.layout.json').write_text(json.dumps(tb_out),encoding='utf-8')
    assert 'handout' not in tb_out['destinations'],'transfer_book must not render Appendix B'
    assert len([r for r in tb_out['external_links'] if r['kind']=='repair'])==len(tb['questions']['core_calibrated']),'external repair links missing'
    assert not audit(p/'tb.json',p/'tb.pdf')['text_overlap_findings'],'transfer_book audit failed'
    (p/'sg.json').write_text(json.dumps(sg),encoding='utf-8');sg_out=Book(sg,p/'sg.pdf').render();(p/'sg.layout.json').write_text(json.dumps(sg_out),encoding='utf-8')
    assert 'handout' in sg_out['destinations'] and not any(k.startswith('questions-') for k in sg_out['destinations']),'study_guide must render Appendix B and no question pages'
    assert not audit(p/'sg.json',p/'sg.pdf')['text_overlap_findings'],'study_guide audit failed'
print('Product profile: transfer_book and study_guide pass validate, render and audit.')
# Mixed tests must be learner-facing, with diagnosis withheld until after the solutions.
with tempfile.TemporaryDirectory(dir=Path.cwd()) as td:
    p=Path(td);out=Book(d,p/'mixed.pdf').render()
    set_id=d['mixed_tests'][0]['set_id']
    assert any(k.startswith('mixed-'+set_id+'-') for k in out['destinations']),'mixed attempt pages missing'
    assert out['destinations']['diagnosis-'+set_id]>max(out['destinations']['solution-'+q['id']] for q in d['questions']['core_calibrated']),'diagnosis must follow solutions'
print('Mixed-transfer attempt and post-marking diagnosis pages render in the correct order.')
# PR #155 follow-up item 1: prove the schema/renderer has no hidden ceiling around the pilot's
# 8-questions-per-band size before a full ~68-question chapter is authored. This is a structural
# readiness proof, not a claim that a full chapter has been authored - that content-authorship task
# stays explicitly out of scope for a schema+skill+sample deliverable.
scale=copy.deepcopy(d)
scale.update(product='question_bank',lessons=[],lesson_ids=[],handout=None,guided_solutions=[],mixed_tests=[])
for q in scale['questions']['core_calibrated']:q.update(repair_mode='SELF_CONTAINED',repair_target='SELF_CONTAINED_SOLUTION')
grown=[]
for rep in range(9):  # 8 questions * 9 = 72, comfortably over the real 68-question chapter target
    for q in scale['questions']['core_calibrated']:
        nq=copy.deepcopy(q);nq['id']=f"{q['id']}-S{rep}";nq['label']=f"{q['label']}-S{rep}";grown.append(nq)
scale['questions']['core_calibrated']=grown;scale['frozen_questions']=len(grown)
validate(scale)
with tempfile.TemporaryDirectory(dir=Path.cwd()) as td:
    p=Path(td)
    scale_out=Book(scale,p/'scale.pdf').render()
    assert scale_out['pages']>0 and len(scale_out['destinations'])>=len(grown)
print(f'Scale readiness: a synthetic {len(grown)}-question question_bank (> 68-question chapter target) validates and renders with no structural ceiling.')
