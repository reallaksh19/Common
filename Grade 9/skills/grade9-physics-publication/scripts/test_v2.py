#!/usr/bin/env python3
"""Targeted negative tests: the known failure modes must remain blocked."""
import copy,json
from pathlib import Path
from validate_v2 import validate,areas
d=json.loads((Path(__file__).resolve().parents[1]/'examples/motion_B30_v2.json').read_text())
def drop_diagram(x):del x['lessons'][0]['figure']
def placeholder(x):x['lessons'][0]['figure']['status']='PLACEHOLDER'
def nohandout(x):del x['handout']
def wrongnumber(x):x['questions']['core_calibrated'][0]['numeric_check']['distance']=999
def brokenrepair(x):x['questions']['core_calibrated'][0]['repair_target']='missing'
def nographtask(x):x['questions']['core_calibrated'][5]['figure']=None
def mismatch(x):x['questions']['core_calibrated'][5]['figure']['segments'][0][1]=3
def duplicate(x):x['questions']['core_calibrated'][1]['id']=x['questions']['core_calibrated'][0]['id']
def repeatedhint(x):x['questions']['core_calibrated'][0]['hints'][1]=x['questions']['core_calibrated'][0]['hints'][0]
def denominator(x):x['questions']['core_calibrated'].pop()
def unknown(x):x['unrendered_hidden_field']='must fail'
def missingregion(x):x['questions']['core_calibrated'][5]['figure']['segments'].pop()
def missingcitation(x):x['questions']['core_calibrated'][0]['source_status']='SOURCE_VERIFIED'
for fn in [drop_diagram,placeholder,nohandout,wrongnumber,brokenrepair,nographtask,mismatch,duplicate,repeatedhint,denominator,unknown,missingregion,missingcitation]:
    v=copy.deepcopy(d);fn(v)
    try:validate(v)
    except (AssertionError,ValueError):print('REJECTED',fn.__name__)
    else:raise AssertionError('Unexpected acceptance: '+fn.__name__)
assert areas([[0,6,4,-2]])==(10,8),'crossing inside unsplit segment'
assert areas([[0,-3,2,-3]])==(6,-6),'negative rectangle'
assert areas([[0,0,3,0]])==(0,0),'rest'
validate(d)
print('13 negative cases rejected; three physics boundary cases and positive model passed.')
# Synthetic source-link fixture tests plumbing, not attribution or an actual exam.
import tempfile
from render_v2 import Book
from audit_v2 import audit
v=copy.deepcopy(d);q=v['questions']['core_calibrated'][0];q['source_status']='ADAPTED';q['provenance_class']='RECONSTRUCTED_FROM_SCAN'
q['source_citation']={'title':'TEST FIXTURE — not an exam source','url':'https://example.org/physics-test-fixture','locator':'synthetic test only','verification':'VERIFIED','adaptation_note':'Fixture tests citation rendering; no source-truth claim.'}
validate(v)
with tempfile.TemporaryDirectory(dir=Path.cwd()) as td:
    p=Path(td);(p/'model.json').write_text(json.dumps(v))
    out=Book(v,p/'book.pdf').render();(p/'book.layout.json').write_text(json.dumps(out))
    result=audit(p/'model.json',p/'book.pdf')
    assert len(out['external_links'])==2 and not result['text_overlap_findings'],'external citation rendering'
print('Synthetic citation fixture: question and solution URI links verified in actual PDF.')
