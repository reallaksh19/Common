#!/usr/bin/env python3
"""Check a frozen external-corpus ledger; declarations still need source-page review."""
import json,sys
from pathlib import Path
def check(d):
    expected=d['expected_ids'];records=d['records'];ids=[r['id'] for r in records]
    assert len(expected)==len(set(expected)) and len(ids)==len(set(ids)),'duplicate identities'
    assert set(expected)==set(ids),'unexplained corpus loss/addition'
    for r in records:
        assert r['primary_concept'],'missing primary concept'
        assert len(set(r['hints'].values()))==3 and set(r['hints'])=={'h1','h2','h3'},'hint progression fields'
        assert all(r['solution'].get(x) for x in ['why','method','answer','keep']),'solution incomplete'
        assert r['solution']['method']!=r['solution']['answer'],'method equals answer'
        assert r['links_closed'] and not r['editorial_issue'],'unclosed dependency or issue'
        if r['dependency']!='NONE':assert r['question_representation'] and r['solution_representation'],'missing representation'
        if d['claim']=='SOURCE_RECONCILED':
            assert r['state']=='SOURCE_RECONCILED' and r['source_url'].startswith('https://') and r['exam_metadata_verified'],'source not verified'
        else:assert d['claim']=='PILOT_ORIGINAL' and r['state']=='ORIGINAL' and not r['exam_metadata_verified'],'invalid pilot attribution'
    return {'records_checked':len(ids),'claim':d['claim'],'source_truth_and_hint_leakage':'MANUAL_REVIEW_REQUIRED'}
if __name__=='__main__':print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())),indent=2))
