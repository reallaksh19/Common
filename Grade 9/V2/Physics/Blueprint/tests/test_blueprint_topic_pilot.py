#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'engine'));from validate_topic_blueprint import validate_topic,digest_without_field
def topic():return json.loads((ROOT/'topics'/'motion-in-a-plane.v1.json').read_text(encoding='utf-8'))
def test_motion_in_plane_route_is_derived_core2_first():r=validate_topic(topic());assert r['derived_route']=='CORE2_FIRST' and r['matched_rule_id']=='ROUTE-C2-RICH-QUESTIONS'
def test_topic_name_does_not_control_route():b=topic();b['topic_id']='PHY-RENAMED';b['evidence']['topic_id']='PHY-RENAMED';b['title']='Renamed topic';b['topic_blueprint_digest']=digest_without_field(b,'topic_blueprint_digest');assert validate_topic(b)['derived_route']=='CORE2_FIRST'
def test_route_changes_when_evidence_changes_not_name():b=topic();b['evidence']['metrics']['SA']['value']=3;b['evidence']['metrics']['SS']['value']=3;b['expected_route']='CORE1_FIRST';b['topic_blueprint_digest']=digest_without_field(b,'topic_blueprint_digest');assert validate_topic(b)['derived_route']=='CORE1_FIRST'
def test_stale_digest_fails():
    b=topic();b['title']='changed'
    try:validate_topic(b)
    except AssertionError as e:assert str(e)=='TOPIC_BLUEPRINT_DIGEST_DRIFT'
    else:raise AssertionError('EXPECTED_DIGEST_FAILURE')
def test_pilot_bindings_point_to_blueprint_and_runtime():b=topic();p=b['pilot_bindings'];assert p['join_fixture'].startswith('Grade 9/V2/Physics/Blueprint/');assert p['control_state_fixture'].startswith('Grade 9/V2/Physics/Blueprint/');assert p['core1a_stage_fixture'].startswith('Grade 9/V2/Physics/Blueprint/');assert p['core2a_runtime_root']=='Grade 9/V2/Physics/Core2A'
def main():
    ts=[v for k,v in globals().items() if k.startswith('test_') and callable(v)]
    for t in ts:t()
    print(f'Blueprint topic-pilot tests: PASS ({len(ts)} tests)')
if __name__=='__main__':main()
