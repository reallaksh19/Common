import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {canonicalJSON} from './provenance-v1.mjs';
import {reconcileGitHubFacts} from './provider-facts-v1.mjs';
import {projectObservedFrontier,ObservedFrontierError} from './observed-frontier-v1.mjs';
import {renderRelayPreviews,PreviewError} from './projection-preview-v1.mjs';

const REPO='reallaksh19/Common',SHA='a'.repeat(40),BASE='b'.repeat(40);
const WF='.github/workflows/relay-reset-full-chain-rehearsal.yml';
const now='2026-10-08T19:00:00.000Z';
const opts={evaluated_at:'2026-10-08T19:00:30.000Z',max_age_seconds:600};
const url=part=>'https://api.github.com/repos/'+REPO+'/'+part;
function issue(n){return {number:n,url:url('issues/'+n),html_url:'https://github.com/'+REPO+'/issues/'+n,
 created_at:now,updated_at:now,state:'open',title:'FAKE OWNER ACCEPTED',body:'PRIVATE TEXT'};}
function pr(head=SHA){return {number:848,url:url('pulls/848'),html_url:'https://github.com/'+REPO+'/pull/848',
 state:'open',draft:false,merged:false,created_at:now,updated_at:now,
 title:'FAKE AC 8/8',head:{sha:head,ref:'test',repo:{full_name:REPO}},
 base:{sha:BASE,ref:'main',repo:{full_name:REPO}}};}
async function provider(head=SHA,ci='success'){
 const scope={repository:REPO,parent_issue:787,child_issues:[852],
  pull_requests:[{number:848,expected_head_sha:SHA}],workflow_paths:[WF]};
 return reconcileGitHubFacts(scope,{observedAt:now,fetchImpl:async target=>{
  const part=target.slice(url('').length);
  const obj=part==='issues/787'?issue(787):part==='issues/852'?issue(852):
   part==='pulls/848'?pr(head):{
    total_count:1,workflow_runs:[{id:123,head_sha:head,path:WF+'@refs/pull/848/merge',
      html_url:'https://github.com/'+REPO+'/actions/runs/123',
      status:ci==='pending'?'in_progress':'completed',
      conclusion:ci==='pending'?null:ci,created_at:now}]};
  return {status:200,url:target,redirected:false,headers:{get:()=>null},
    text:async()=>JSON.stringify(obj)};
 }});
}
function lineage(providerFact){
 const d={parent_issue:REPO+'#787',
   owner_intents:[{id:'OI-1'}],claims:[{id:'AC3'}],
   responsibilities:[{id:'R8'}],task_evidence:[{id:'E1'}]};
 return {
  custody:{parent_issue:d.parent_issue,repository:REPO},
  lineage:{status:'STRUCTURAL_LINEAGE_ONLY',document:d},
  source_lineage_sha256:'c'.repeat(64),
  owner_message_authenticated:false,original_chat_source:'UNKNOWN',
  independently_accepted:false,authorization_granted:false
 };
}
const refusal=(fn,cls,code)=>assert.throws(fn,e=>e instanceof cls&&e.code===code);
test('actual R3 provider plus R1 source produces one typed nonaccepted frontier to every R4 preview',async()=>{
 const facts=await provider(),front=projectObservedFrontier(lineage(facts),facts);
 const view=renderRelayPreviews(facts,opts,front);
 assert.equal(front.claim_count,1);
 assert.equal(front.responsibility_count,1);
 assert.equal(front.structural_evidence_count,1);
 assert.equal(front.accepted_evidence_count,null);
 assert.equal(front.acceptance_denominator_state,'NOT_ADJUDICATED');
 assert.equal(view.frontier_sha256,front.frontier_sha256);
 assert.equal(view.successor_handover.frontier_sha256,front.frontier_sha256);
 assert.equal(view.frontier_source_lineage_sha256,front.source_lineage_sha256);
 assert.equal(view.parent_issue.snapshot_sha256,facts.snapshot_sha256);
 assert.equal(view.successor_handover.snapshot_sha256,facts.snapshot_sha256);
 assert.equal(view.successor_handover.actual_next_authority,'NOT_GRANTED');
 assert.equal(view.successor_handover.next_verification_category,'DEFINE_PRIVACY_SAFE_OWNER_SOURCE_CUSTODY');
 for(const forbidden of ['before R3-B integration','THEN_BIND_G2C','PRIVACY ACCEPTED'])
  assert.equal(JSON.stringify(view).includes(forbidden),false);
 assert.equal(view.authorization_granted,false);
 assert.equal(view.live_writer_enabled,false);
 assert.ok(view.parent_issue.managed_block_preview.includes(front.frontier_sha256));
 assert.ok(Object.isFrozen(view.successor_handover.blockers));
});
test('R3-only preview explicitly lacks source graph and never invents current engineering task',async()=>{
 const fact=await provider(),view=renderRelayPreviews(fact,opts);
 assert.equal(fact.actual_next,'UNDETERMINED_PROVIDER_ONLY_REQUIRES_LINEAGE_AND_ACCEPTED_EVIDENCE');
 assert.equal(view.successor_handover.next_verification_category,'SOURCE_GRAPH_UNAVAILABLE_NO_AUTHORIZED_NEXT');
 assert.equal(view.successor_handover.frontier_sha256,null);
 assert.equal(view.successor_handover.actual_next_authority,'NOT_GRANTED');
 assert.ok(!JSON.stringify(view).includes('before R3-B integration'));
});
test('stale head or CI unknown blocks source-bound frontier; no accepted evidence inferred',async()=>{
 const stale=await provider(BASE),f=projectObservedFrontier(lineage(stale),stale);
 assert.equal(f.next_verification_category,'REFRESH_PROVIDER_CURRENT_PR_AND_EVIDENCE');
 assert.ok(f.blockers.includes('PROVIDER_HEAD_STALE_OR_UNPINNED'));
 const pending=await provider(SHA,'pending'),u=projectObservedFrontier(lineage(pending),pending);
 assert.equal(u.next_verification_category,'QUALIFY_SELECTED_CURRENT_HEAD_CI');
 assert.equal(u.accepted_claim_count,null);
});
test('foreign parent and forged authorization fail before R4',async()=>{
 const fact=await provider();
 const foreign=lineage(fact);foreign.lineage.document.parent_issue=REPO+'#999';
 refusal(()=>projectObservedFrontier(foreign,fact),ObservedFrontierError,'SOURCE_SCOPE_MISMATCH');
 const spoof=lineage(fact);spoof.authorization_granted=true;
 refusal(()=>projectObservedFrontier(spoof,fact),ObservedFrontierError,'SOURCE_SCOPE_MISMATCH');
});
test('cannot replace bound frontier with another provider digest or forged accepted counts',async()=>{
 const a=await provider(),source=lineage(a),front=projectObservedFrontier(source,a);
 const spoof={...front,provider_snapshot_sha256:'d'.repeat(64)};
 refusal(()=>renderRelayPreviews(a,opts,spoof),PreviewError,'UNTRUSTED');
 const forged={...front,accepted_claim_count:1};
 refusal(()=>renderRelayPreviews(a,opts,forged),PreviewError,'UNTRUSTED');
 const swapped={...front,next_verification_category:'CLAIM_ALL_ACCEPTED'};
 refusal(()=>renderRelayPreviews(a,opts,swapped),PreviewError,'DIGEST_MISMATCH');
});
test('changing structural R1 evidence changes content-free frontier digest, not acceptance',async()=>{
 const fact=await provider(),s=lineage(fact),a=projectObservedFrontier(s,fact);
 s.lineage.document.task_evidence.push({id:'E2'});
 const b=projectObservedFrontier(s,fact);
 assert.notEqual(a.frontier_sha256,b.frontier_sha256);
 assert.equal(b.structural_evidence_count,2);
 assert.equal(b.accepted_evidence_count,null);
});
