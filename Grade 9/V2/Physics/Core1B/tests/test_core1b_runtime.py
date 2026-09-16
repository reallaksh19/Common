#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"engine"))
from core1b_runtime import *

def load(p): return json.loads(Path(p).read_text())
REG=load(ROOT/"registry"/"projectile-vertical-event-atoms-v1.json")
G=ROOT/"golden"/"projectile-vertical-event"
AUTH=load(G/"core1a-authority.json"); UNIT=load(G/"core1b-unit.json"); EVENTS=load(G/"observed-events.json")

def schema(name):
    s=load(ROOT/"contracts"/name);Draft202012Validator.check_schema(s);return Draft202012Validator(s)
def expect(code,fn):
    try: fn()
    except Core1BRuntimeError as e:
        assert str(e).startswith(code),(code,str(e)); return
    raise AssertionError("expected "+code)

AUTH_V=schema("physics-core1b-authority-release.schema.json")
UNIT_V=schema("physics-core1b-unit.schema.json")
EVENT_V=schema("physics-core1b-observed-event.schema.json")
RECEIPT_V=schema("physics-core1b-release-receipt.schema.json")
AUTH_V.validate(AUTH);UNIT_V.validate(UNIT)
for e in EVENTS:EVENT_V.validate(e)

validate_registry(REG); validate_unit(UNIT,REG,AUTH,[])
assert derive_state(UNIT,AUTH,[])=="NOT_EXPOSED"
receipt=build_release_receipt(UNIT,REG,AUTH,EVENTS);RECEIPT_V.validate(receipt)
assert receipt["state"]=="INDEPENDENT" and receipt["core1a_release_digest"]==AUTH["authority_digest"]
assert receipt["representation_evidence"]==["EVENT_TIMELINE"]

bad=copy.deepcopy(AUTH); bad["authority_digest"]="0"*64
expect("CORE1B_CORE1A_AUTHORITY_DIGEST_MISMATCH",lambda:validate_unit(UNIT,REG,bad,[]))

bad_event=copy.deepcopy(EVENTS[0]); bad_event["basis"]="TEACHING_RECEIPT"; bad_event["event_digest"]=digest_without(bad_event,"event_digest")
expect("CORE1B_OBSERVED_EVIDENCE_BASIS_REQUIRED",lambda:validate_event(bad_event,[]))

bad_seq=copy.deepcopy(EVENTS[0]); bad_seq["event_sequence"]=2; bad_seq["event_digest"]=digest_without(bad_seq,"event_digest")
expect("CORE1B_EVENT_SEQUENCE_NOT_APPEND_ONLY",lambda:validate_event(bad_seq,[]))

bad_unit=copy.deepcopy(UNIT); bad_unit["readiness_requirements"].remove("applicability")
expect("CORE1B_APPLICABILITY_REQUIRED",lambda:validate_unit(bad_unit,REG,AUTH,[]))

bad_unit=copy.deepcopy(UNIT); bad_unit["learner_surface"]["teacher_moves"].append("STATE_FRAGILE")
expect("CORE1B_INTERNAL_LABEL_LEAK",lambda:validate_unit(bad_unit,REG,AUTH,[]))

skip_unit=copy.deepcopy(UNIT); skip_unit["atom_refs"].remove("PHY-A-DIR-01")
expect("CORE1B_PREREQUISITE_SKIP_UNGROUNDED",lambda:validate_unit(skip_unit,REG,AUTH,[]))
secure=copy.deepcopy(EVENTS[0]); secure["event_id"]="C1B-EVT-PHY-M2D-SBA04-SECURE"; secure["atom_refs"]=["PHY-A-DIR-01"]; secure["event_kind"]="ATOM_CHECK"; secure["event_digest"]=digest_without(secure,"event_digest")
skip_unit["prerequisite_skip_evidence"]=[{"atom_ref":"PHY-A-DIR-01","event_ref":secure["event_id"],"event_digest":secure["event_digest"]}]
validate_unit(skip_unit,REG,AUTH,[secure])

guided=copy.deepcopy(secure); guided["event_id"]="C1B-EVT-PHY-M2D-SBA04-GUIDED"; guided["event_kind"]="GUIDED_ATTEMPT"; guided["hint_level_used"]="FULL_SOLUTION"; guided["event_digest"]=digest_without(guided,"event_digest")
skip_guided=copy.deepcopy(skip_unit); skip_guided["prerequisite_skip_evidence"]=[{"atom_ref":"PHY-A-DIR-01","event_ref":guided["event_id"],"event_digest":guided["event_digest"]}]
expect("CORE1B_PREREQUISITE_SKIP_UNGROUNDED",lambda:validate_unit(skip_guided,REG,AUTH,[guided]))

supported=copy.deepcopy(EVENTS[0]); supported["hint_level_used"]="MODEL_CUE"; supported["event_digest"]=digest_without(supported,"event_digest")
assert derive_state(UNIT,AUTH,[supported])=="SUPPORTED"
expect("CORE1B_OBSERVED_INDEPENDENT_EVIDENCE_REQUIRED",lambda:build_release_receipt(UNIT,REG,AUTH,[supported]))
print("Physics Core1B runtime tests: PASS (11 guards + schema validation)")
