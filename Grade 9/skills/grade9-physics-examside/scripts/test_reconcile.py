#!/usr/bin/env python3
"""Targeted negative tests: reconcile.py must catch ledger/publication drift, not just
internal ledger consistency (the gap check_ledger.py alone leaves open)."""
import copy,json
from pathlib import Path
from reconcile import reconcile
ROOT=Path(__file__).resolve().parents[1]
PUBROOT=ROOT.parent/'grade9-physics-publication'
ledger=json.loads((ROOT/'references/source-ledger.example.json').read_text())
model=json.loads((PUBROOT/'examples/motion_question_bank_v2.json').read_text())

def drop_from_model(m):m['questions']['core_calibrated']=[q for q in m['questions']['core_calibrated'] if q['id']!='B80-A1']
def drop_from_ledger(l):l['expected_ids'].remove('B80-A1');l['records']=[r for r in l['records'] if r['id']!='B80-A1']
def wrong_concept(m):m['questions']['core_calibrated'][0]['primary_concept_id']='PHY-MOT-VTAREA-01'
def wrong_hint(m):m['questions']['core_calibrated'][0]['hints'][0]='A drifted hint not in the frozen ledger.'
def wrong_answer(m):m['questions']['core_calibrated'][0]['solution']['answer']='A drifted answer.'

for name,mutate,target in [('drop_from_model',drop_from_model,'model'),('drop_from_ledger',drop_from_ledger,'ledger'),
        ('wrong_concept',wrong_concept,'model'),('wrong_hint',wrong_hint,'model'),('wrong_answer',wrong_answer,'model')]:
    l,m=copy.deepcopy(ledger),copy.deepcopy(model)
    mutate(l if target=='ledger' else m)
    out=reconcile(l,m)
    assert out['counters']['LEDGER_STATUS']=='FAIL',f'{name}: drift not detected'
    print('DETECTED',name)
out=reconcile(ledger,model)
assert out['counters']['LEDGER_STATUS']=='PASS','unmodified ledger/model must reconcile cleanly'
print('5 drift cases detected; unmodified ledger/model reconciles cleanly.')
