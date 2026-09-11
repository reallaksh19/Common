#!/usr/bin/env python3
import copy, json, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'engine')); sys.path.insert(0,str(ROOT/'validator'))
from build_semantic_product import build
from realize_math_publication import realize
from validate_candidate import validate_dir

def load(p): return json.loads(Path(p).read_text())
design=load(ROOT/'fixtures'/'learning_design_result.unit.synthetic.json'); policy=load(ROOT/'fixtures'/'publication_policy.synthetic.json'); target=load(ROOT/'fixtures'/'publication_target.synthetic.json')
product=build(design); by={x['content_id']:x for x in product['content_items']}
assert len(product['content_items'])==17
assert all(x['learning_design_refs'] for x in product['content_items'])
assert by['C05']['metadata']['one_legal_operation_per_line'] is True
assert by['C04']['metadata']['prediction_before_resolution'] is True and by['C04']['metadata']['focal_distinction'] and by['C04']['metadata']['concrete_pair']
assert by['C11']['metadata']['concrete_pair'] is True
assert by['C02']['metadata']['concrete_proposed_move'] is True and any('Proposed move:' in s for s in by['C02']['body'])
assert any(s.startswith('Move A:') for s in by['C04']['body']) and any(s.startswith('Move B:') for s in by['C04']['body'])
assert any(s.startswith('Expansion A:') for s in by['C11']['body']) and any(s.startswith('Expansion B:') for s in by['C11']['body'])
assert by['C06']['support_level']>by['C07']['support_level']>by['C08']['support_level']==0
assert by['C08']['metadata']['conceptual_hints']==[]
assert by['C14']['learning_design_refs']==['P01'] and by['C14']['metadata']['explanation_before_probe'] is False
assert by['C15']['metadata']['separate_from_probe'] is True
assert by['C09']['primitive']=='SELF_CHECK_STRIP' and 'V01' in by['C09']['learning_design_refs']
assert by['C16']['metadata']['number_only'] is False
assert by['C17']['metadata']['prompted'] is False and by['C17']['metadata']['concrete_task'] is True
assert not any(w in ' '.join(by['C17']['body']).lower() for w in ('check','verify','verification','substitut','equivalence'))
assert len(policy['page_groups'])==5
bad=copy.deepcopy(design); bad['learning_design_plan']['steps']=[s for s in bad['learning_design_plan']['steps'] if s['step_id']!='E06']
try: build(bad); raise AssertionError('missing E06 accepted')
except ValueError: pass
badtarget=copy.deepcopy(target); badtarget['benchmark_inputs']=['PR #156']
with tempfile.TemporaryDirectory() as d:
    try: realize(product,badtarget,policy,d); raise AssertionError('benchmark contamination accepted')
    except ValueError: pass
with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
    realize(product,target,policy,a); validate_dir(a); realize(product,target,policy,b); validate_dir(b)
    assert (Path(a)/'candidate.pdf').read_bytes()==(Path(b)/'candidate.pdf').read_bytes()
    assert (Path(a)/'publication_manifest.json').read_bytes()==(Path(b)/'publication_manifest.json').read_bytes()
    assert json.loads((Path(a)/'physical_page_map.json').read_text())['page_count']==5
    p=Path(a)/'candidate.pdf'; p.write_bytes(p.read_bytes()+b'X')
    try: validate_dir(a); raise AssertionError('byte drift accepted')
    except ValueError: pass
for mode in ('omit','duplicate'):
    p=copy.deepcopy(policy)
    if mode=='omit': p['page_groups'][0]['content_refs'].remove('C01')
    else: p['page_groups'][1]['content_refs'].append('C01')
    with tempfile.TemporaryDirectory() as d:
        try: realize(product,target,p,d); raise AssertionError(mode+' custody failure accepted')
        except ValueError: pass
print('MATH-V2-06 revised publication falsifiers = 23 PASS')
