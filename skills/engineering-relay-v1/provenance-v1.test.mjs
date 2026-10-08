import test from 'node:test';
import assert from 'node:assert/strict';
import {validate,canonicalJSON,traceClaim,ProvenanceError} from './provenance-v1.mjs';

function fixture() {
  return {
  "schema": "relay-provenance-v1",
  "parent_issue": "reallaksh19/Common#787",
  "owner_intents": [
    {
      "id": "OI-1",
      "raw_text": "start now",
      "original_source": {
        "kind": "CHAT",
        "status": "UNKNOWN",
        "locator": null
      },
      "first_durable_mirror": "https://github.com/reallaksh19/Common/issues/787"
    }
  ],
  "claims": [
    {
      "id": "AC1",
      "intent_ids": [
        "OI-1"
      ],
      "criterion": "A different agent can trace claim source"
    }
  ],
  "responsibilities": [
    {
      "id": "R1-A",
      "claim_ids": [
        "AC1"
      ],
      "depends_on": [],
      "scope": "Pure records",
      "write_surface": [
        "skills/engineering-relay-v1/provenance-v1.mjs"
      ]
    }
  ],
  "sessions": [
    {
      "id": "S1",
      "responsibility_id": "R1-A",
      "agent_id": "AGENT-1",
      "base_sha": "957377de11843f78dd7210450c8e5a99b859eea9",
      "changed_files": [
        "skills/engineering-relay-v1/provenance-v1.mjs"
      ],
      "events": [
        {
          "kind": "OWNER_PROMPT",
          "source": {
            "kind": "CHAT",
            "status": "UNKNOWN",
            "locator": null
          },
          "summary": "start now"
        },
        {
          "kind": "CODE_CHANGE",
          "source": {
            "kind": "FILE",
            "status": "CLAIMED",
            "locator": "skills/engineering-relay-v1/provenance-v1.mjs"
          },
          "summary": "Pure module"
        }
      ]
    }
  ],
  "task_evidence": [
    {
      "id": "E1",
      "responsibility_id": "R1-A",
      "session_id": "S1",
      "kind": "START",
      "source": {
        "kind": "GITHUB_COMMENT",
        "status": "CLAIMED",
        "locator": "https://github.com/reallaksh19/Common/issues/789#issuecomment-6062540809"
      },
      "commit_sha": null
    }
  ],
  "research_findings": [
    {
      "id": "F1",
      "statement": "Prior report has errors",
      "source": {
        "kind": "GITHUB_ISSUE",
        "status": "CLAIMED",
        "locator": "https://github.com/reallaksh19/Common/issues/788"
      },
      "verification": "UNVERIFIED"
    }
  ],
  "owner_decisions": []
};
}
const clone = x => JSON.parse(JSON.stringify(x));
test('valid graph with unknown original chat source never mints authority', () => {
  const report = validate(fixture());
  assert.equal(report.valid, true);
  assert.equal(report.no_authority_asserted, true);
  assert.deepEqual(traceClaim(fixture(),'AC1'), {
    claim_id:'AC1',owner_intent_ids:['OI-1'],responsibility_ids:['R1-A'],session_ids:['S1'],evidence_ids:['E1']
  });
});
test('canonical bytes independent of property ordering', () => {
  const first = fixture(), reverse=Object.fromEntries(Object.entries(first).reverse());
  assert.equal(canonicalJSON(first),canonicalJSON(reverse));
});
test('interrupted START-only session is structurally valid, not END', () => {
  const f=fixture();
  f.sessions[0].events.push({kind:'ERROR',source:{kind:'CHAT',status:'UNKNOWN',locator:null},summary:'transport unavailable'});
  assert.equal(validate(f).valid,true);
  assert.equal(f.task_evidence[0].kind,'START');
});
const negatives = ["foreign owner source","dangling claim","duplicate global ID","wrong evidence session","unsafe write surface","malformed SHA","pretend accepted","fake status","code END missing commit","dangling decision","cycle","session to other responsibility"];
const mutations = [
 x=>x.owner_intents[0].original_source={kind:'CHAT',status:'UNKNOWN',locator:'https://fake.example'},
 x=>x.responsibilities[0].claim_ids=['AC9'],
 x=>x.claims[0].id='OI-1',
 x=>x.task_evidence[0].session_id='S99',
 x=>x.responsibilities[0].write_surface=['../secrets'],
 x=>x.sessions[0].base_sha='abc',
 x=>x.claims[0].accepted=true,
 x=>x.owner_intents[0].original_source.status='VERIFIED',
 x=>x.task_evidence[0].kind='END',
 x=>x.owner_decisions.push({id:'D1',intent_id:'OI-1',finding_ids:['F999'],disposition:'ADOPT',source:{kind:'CHAT',status:'UNKNOWN',locator:null}}),
 x=>x.responsibilities[0].depends_on=['R1-A'],
 x=>{x.responsibilities.push({id:'R2',claim_ids:['AC1'],depends_on:[],scope:'Other',write_surface:['some/file']});x.task_evidence[0].responsibility_id='R2';}
];
negatives.forEach((name,i)=>test('reject '+name,()=>{
  const f=clone(fixture());mutations[i](f);
  assert.throws(()=>validate(f),ProvenanceError);
}));
test('unadopted research remains unadopted',()=>{
  const f=fixture();f.research_findings[0].verification='SUPPORTED_CLAIM';
  assert.equal(f.owner_decisions.length,0);
  assert.equal(validate(f).no_authority_asserted,true);
});

test('canonical JSON preserves special own keys without changing the prototype',()=>{
  const payload=JSON.parse('{"__proto__":{"x":1},"constructor":{"v":2}}');
  assert.equal(canonicalJSON(payload),'{"__proto__":{"x":1},"constructor":{"v":2}}');
});
test('deep dependency chain is bounded and non-recursive',()=>{
  const f=fixture();
  for(let i=0;i<5000;i++){
    f.responsibilities.push({
      id:'CHAIN-'+i,claim_ids:['AC1'],
      depends_on:i===0?['R1-A']:['CHAIN-'+(i-1)],
      scope:'Deep chain regression',write_surface:['skills/engineering-relay-v1/README.md']
    });
  }
  assert.equal(validate(f).valid,true);
  f.responsibilities[0].depends_on=['CHAIN-4999'];
  assert.throws(()=>validate(f),ProvenanceError);
});
test('unbounded event arrays are rejected before expensive validation',()=>{
  const f=fixture();
  const original=f.sessions[0].events[0];
  f.sessions[0].events=Array.from({length:10001},()=>original);
  assert.throws(()=>validate(f),ProvenanceError);
});
