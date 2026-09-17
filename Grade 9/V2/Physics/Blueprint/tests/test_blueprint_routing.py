#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from governor import load_json, route


def golden(name: str):
    return load_json(ROOT / "fixtures" / "golden" / name)


def test_golden_routes():
    expected={"core1-first.json":"CORE1_FIRST","core2-first.json":"CORE2_FIRST","blocked.json":"BLOCK"}
    for name,target in expected.items(): assert route(golden(name)["evidence"])["final_route"]==target

def test_topic_name_cannot_change_routing():
    evidence=golden("core2-first.json")["evidence"];renamed=deepcopy(evidence);renamed["topic_id"]="PHY-COMPLETELY-DIFFERENT-TOPIC-NAME";a=route(evidence);b=route(renamed);assert a["final_route"]==b["final_route"]=="CORE2_FIRST";assert a["matched_rule_id"]==b["matched_rule_id"]

def test_absent_questions_do_not_force_block_when_semantic_authority_is_strong():
    evidence=golden("core1-first.json")["evidence"];assert evidence["sources"]["question_corpus"]["availability"]=="ABSENT";assert evidence["metrics"]["QE"]["value"]==0;assert route(evidence)["final_route"]=="CORE1_FIRST"

def test_hard_owner_override_changes_action_not_system_finding():
    evidence=golden("core1-first.json")["evidence"];override={"override_id":"OVR-GOLDEN-001","mode":"HARD","requested_route":"CORE2_FIRST","reason":"Owner requests assessment-first execution for this proof."};decision=route(evidence,owner_override=override);assert decision["system_finding"]["recommended_route"]=="CORE1_FIRST";assert decision["final_route"]=="CORE2_FIRST"

def test_soft_override_cannot_hide_insufficient_evidence_block():
    evidence=golden("blocked.json")["evidence"];override={"override_id":"OVR-GOLDEN-002","mode":"SOFT","requested_route":"CORE1_FIRST","reason":"Preference only."};decision=route(evidence,owner_override=override);assert decision["system_finding"]["recommended_route"]=="BLOCK";assert decision["final_route"]=="BLOCK"

def test_packet_transport_bound_is_three_subtopics_not_learning_atoms():
    validator=Draft202012Validator(load_json(ROOT/"contracts"/"packet-envelope.schema.json"));packet={"packet_id":"K-GOLDEN-001","packet_type":"K_SEMANTIC","schema_version":"1.0.0","topic_id":"PHY-GOLDEN","subtopic_ids":["S1","S2","S3"],"producer_role":"CORE1","producer_run_id":"RUN-1","producer_instance_id":"INSTANCE-1","ground_truth_refs":["GT-1"],"dependencies":[],"confidence":{"level":"HIGH","basis":"Golden proof."},"validation_status":"UNVALIDATED","unresolved_issues":[],"payload":{"learning_atoms":[f"A{i}" for i in range(25)]}};validator.validate(packet);packet["subtopic_ids"].append("S4")
    try: validator.validate(packet)
    except ValidationError: pass
    else: raise AssertionError("PACKET_ALLOWED_MORE_THAN_THREE_SUBTOPICS")

def test_core2a_is_active_only_with_taught_state_guards():
    architecture=load_json(ROOT/"policy"/"architecture.v1.json");assert architecture["role_lifecycle"]["CORE2A"]=="ACTIVE";assert architecture["invariants"]["core2a_requires_taught_state_receipts"] is True;assert architecture["invariants"]["core2a_may_not_infer_learner_mastery"] is True

def main():
    tests=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:test()
    print(f"Blueprint routing tests: PASS ({len(tests)} tests)")
    for name in (
        "test_blueprint_contract_inventory_v10.py",
        "test_blueprint_scope_v10.py",
        "test_blueprint_domain_prerequisites_v10.py",
        "test_blueprint_stress_test_v10.py",
        "test_blueprint_stress_batch_v10.py",
    ):
        subprocess.run([sys.executable,str(ROOT/"tests"/name)],check=True)

if __name__=="__main__":main()
