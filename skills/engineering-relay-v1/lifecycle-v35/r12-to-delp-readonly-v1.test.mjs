import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {rehearseR12ToDelp,DiagnosticJoinError} from './r12-to-delp-readonly-v1.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const r12 = join(here,'../candidate-verification-v1.mjs');
const nativeDelp = join(here,'../../engineering-pr-delivery-v3.2/scripts/delp_projection_v32.py');
const PY = process.platform === 'win32' ? 'python' : 'python3';
const rejects = code => e => e instanceof DiagnosticJoinError && e.code === code;

test('rejects invalid python binary before any R12 source read',async()=>{
  await assert.rejects(rehearseR12ToDelp({}, {}, {}, {pythonBinary:'sh'}),rejects('INVALID_PYTHON_BINARY'));
});
test('rejects unauthorized option names',async()=>{
  await assert.rejects(rehearseR12ToDelp({}, {}, {}, {publisher:true}),rejects('INVALID_OPTIONS'));
});
test('rejects nonsensical timeout',async()=>{
  await assert.rejects(rehearseR12ToDelp({}, {}, {}, {timeoutMs:0}),rejects('INVALID_TIMEOUT'));
});
test('full Common actual R12 provider → Python actual DELP.project, quarantined',async t=>{
  if(!existsSync(r12)||!existsSync(nativeDelp)) {
    t.skip('Native R12 and V3.2 DELP absent from minimal local workspace: NOT_RUN');return;
  }
  const [{reconcileGitHubFacts}] = await Promise.all([import('../provider-facts-v1.mjs')]);
  // Import ONLY synthetic input from local Python test fixture, not historical
  // green outputs or a surrogate projector; real R12 + DELP run in this test.
  const code='import json,sys;sys.path.insert(0,'+JSON.stringify(here)+');from test_diagnostic_delp_bridge_v1 import bundle;print(json.dumps(bundle()))';
  const source=spawnSync(PY,['-c',code],{
    encoding:'utf8',shell:false,timeout:10000
  });
  assert.equal(source.status,0,source.stderr);
  const packet=JSON.parse(source.stdout);
  const repo='reallaksh19/Common', head='c'.repeat(40), base='a'.repeat(40);
  const api='https://api.github.com/repos/'+repo+'/', when='2026-10-09T02:00:00Z';
  const workflow='.github/workflows/relay-reset-full-chain-rehearsal.yml';
  function issue(number){return {number,url:api+'issues/'+number,html_url:'https://github.com/'+repo+'/issues/'+number,
    state:'open',title:'SYNTHETIC ONLY',body:'NOT AN ORIGINAL OWNER CHAT',created_at:when,updated_at:when};}
  function pr(){return {number:891,url:api+'pulls/891',html_url:'https://github.com/'+repo+'/pull/891',
    state:'open',draft:true,merged:false,title:'SYNTHETIC PR',created_at:when,updated_at:when,
    head:{sha:head,ref:'fixture',repo:{full_name:repo}},base:{sha:base,ref:'main',repo:{full_name:repo}}};}
  const scope={repository:repo,parent_issue:787,child_issues:[878],
    pull_requests:[{number:891,expected_head_sha:head}],workflow_paths:[workflow]};
  const provider=await reconcileGitHubFacts(scope,{observedAt:when,fetchImpl:async url=>{
    const rel=url.slice(api.length);
    const data=rel==='issues/787'?issue(787):rel==='issues/878'?issue(878):
      rel==='pulls/891'?pr():rel.startsWith('actions/runs?')?
      {total_count:1,workflow_runs:[{id:77,head_sha:head,path:workflow+'@refs/heads/main',
        html_url:'https://github.com/'+repo+'/actions/runs/77',status:'completed',conclusion:'success',created_at:when}]}:null;
    assert.ok(data,rel);
    return {status:200,url,redirected:false,headers:{get:()=>null},text:async()=>JSON.stringify(data)};
  }});
  const got=await rehearseR12ToDelp(provider,packet.graph,packet.evidence_review,{pythonBinary:PY});
  assert.equal(got.actual_delp_source,'EXISTING_V3_2_PROJECT');
  assert.equal(got.provider_authenticity,'NOT_ATTESTED_AFTER_SERIALIZATION');
  assert.equal(got.quarantined_ledger_claims,1);
  assert.equal(got.diagnostic_root.E,0);
  assert.equal(got.diagnostic_leaf.E,0);
  assert.equal(got.publishable_snapshot,false);
  assert.equal(got.live_status_writer,'OFF');
});
