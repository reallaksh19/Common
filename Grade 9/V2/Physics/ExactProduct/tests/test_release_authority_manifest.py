#!/usr/bin/env python3
import copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[3]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
m=load(ROOT/'RELEASE_AUTHORITY_MANIFEST.json'); x=copy.deepcopy(m); got=x.pop('manifest_digest'); assert got==hashlib.sha256(canonical(x)).hexdigest()
assert m['subject']=='PHYSICS' and m['stage']=='P-L ExactProduct'
assert m['engines']['governed_release'].endswith('evaluate_physics_governed_release.py')
assert m['engines']['shared_human_review_intake'].endswith('ingest_human_reviews.py')
for group in ('engines','contracts'):
    for ref in m[group].values(): assert (REPO/ref).is_file(), ref
r=m['review_intake']; policy=load(REPO/r['policy']); real=load(REPO/r['real_reviewer_registry']); test=load(REPO/r['test_reviewer_registry'])
assert tuple(policy['required_pass_submissions'])==tuple(r['required_dimensions'])==('SUBJECT','PEDAGOGY','ASSESSMENT','VISUAL')
assert real['registry_class']=='REAL' and all(real['authorized_reviewers'][k]==[] for k in ('HUMAN_SUBJECT','HUMAN_PEDAGOGY','HUMAN_ASSESSMENT','HUMAN_VISUAL'))
assert test['registry_class']=='TEST_ONLY' and r['test_only_release_eligible'] is False
assert m['reference_comparator']=={'access_phase':'FINAL_COMPARATIVE_VALIDATION','allowed_only_after_all_governed_human_gates_pass':True,'comparator_id':'FROZEN_PR156_MATURE_DESIGN_COMPARATOR','current_state':'NOT_AUTHORIZED_TO_READ','producer_input':False}
assert m['real_release_current_state']=='BLOCKED_PENDING_AUTHORIZED_REVIEW_OR_EXACT_ARTIFACT'
print('PHY P-L release authority manifest = PASS (real human/comparator evidence still absent)')
