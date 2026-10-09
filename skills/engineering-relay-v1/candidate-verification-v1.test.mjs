import test from 'node:test';
import assert from 'node:assert/strict';
import {reconcileGitHubFacts} from './provider-facts-v1.mjs';
import {deriveCandidateState,verifyCandidateState,CandidateStateError} from './candidate-verification-v1.mjs';

const repo='reallaksh19/Common',HEAD='a'.repeat(40),OTHER='b'.repeat(40);
const wf='.github/workflows/relay-reset-full-chain-rehearsal.yml';
const when='2026-10-09T02:00:00Z',api='https://api.github.com/repos/'+repo+'/';
function issue(number){return {number,url:api+'issues/'+number,
 html_url:'https://github.com/'+repo+'/issues/'+number,
 state:'open',title:'AGENT CLAIMS OWNER APPROVED AC8/8',body:'PRIVATE SOURCE CANARY',
 created_at:when,updated_at:when};}
function pr(head,merged){return {number:859,url:api+'pulls/859',
 html_url:'https://github.com/'+repo+'/pull/859',state:merged?'closed':'open',
 draft:false,merged,title:'FAKE EVIDENCE GREEN',created_at:when,updated_at:when,
 head:{sha:head,ref:'feat/candidate',repo:{full_name:repo}},
 base:{sha:OTHER,ref:'main',repo:{full_name:repo}}};}
async function facts({head=HEAD,merged=false,status='completed',conclusion='success',missing=false,expected=HEAD}={}){
 const scope={repository:repo,parent_issue:787,child_issues:[860],
 pull_requests:[{number:859,expected_head_sha:expected}],workflow_paths:[wf]};
 return reconcileGitHubFacts(scope,{observedAt:when,fetchImpl:async url=>{
   const rel=url.slice(api.length);
   const body=rel==='issues/787'?issue(787):rel==='issues/860'?issue(860):
     rel==='pulls/859'?pr(head,merged):rel.startsWith('actions/runs?')?
     {total_count:missing?0:1,workflow_runs:missing?[]:[
       {id:77,head_sha:head,path:wf+'@refs/heads/main',
        html_url:'https://github.com/'+repo+'/actions/runs/77',
        status,conclusion,created_at:when}]}:null;
   assert.ok(body,rel);
   return {status:200,url,redirected:false,headers:{get:()=>null},
    text:async()=>JSON.stringify(body)};
 }});
}
test('one canonical R12 schema supports PENDING, PASS, FAIL and UNKNOWN without conflating human evidence',async()=>{
 const cases=[
  [{status:'in_progress',conclusion:null},'PENDING','PENDING',false],
  [{status:'completed',conclusion:'success'},'PASS','SELECTED_CI_PASS_ONLY',true],
  [{status:'completed',conclusion:'failure'},'FAIL','CI_NON_SUCCESS',false],
  [{missing:true},'UNKNOWN','UNKNOWN',false]
 ];
 for(const [input,ci,material,qualified] of cases){
  const source=await facts(input),state=deriveCandidateState(source),candidate=state.pr_candidates[0];
  assert.equal(candidate.selected_ci_state,ci);
  assert.equal(candidate.material_status,material);
  assert.equal(candidate.selected_ci_qualified,qualified);
  assert.equal(state.accepted_claim_count,null);
  assert.equal(state.accepted_evidence_count,null);
  assert.equal(state.acceptance_denominator_state,'NOT_ADJUDICATED');
  assert.equal(state.live_writer_enabled,false);
  assert.equal(state.independently_accepted,false);
  assert.equal(state.authorization_granted,false);
  assert.equal(state.next_candidate_verification,ci==='PASS'?null:'QUALIFY_SELECTED_CURRENT_HEAD_CI');
  assert.equal(state.blockers.includes('SELECTED_CI_NOT_ALL_PASS'),ci!=='PASS');
  assert.deepEqual(verifyCandidateState(state,source),state);
  assert.equal(Object.isFrozen(state.pr_candidates[0].selected_workflows),true);
  assert.equal(JSON.stringify(state).includes('PRIVATE SOURCE CANARY'),false);
 }
});
test('merged PR with completed PASS remains selected-CI-pass-only, never Owner-accepted',async()=>{
 const provider=await facts({merged:true});
 const state=deriveCandidateState(provider),unit=state.pr_candidates[0];
 assert.equal(unit.merged,true);
 assert.equal(unit.head_state,'CURRENT');
 assert.equal(unit.material_status,'SELECTED_CI_PASS_ONLY');
 assert.equal(unit.selected_ci_qualified,true);
 assert.equal(state.acceptance_contract,'PARENT_787_AC1_AC8_UNADJUDICATED');
 assert.equal(state.accepted_evidence_count,null);
});
test('stale or unpinned PR head defeats selected green CI, no material acceptance',async()=>{
 for(const input of [{head:OTHER,expected:HEAD},{expected:null}]){
  const source=await facts(input),s=deriveCandidateState(source),c=s.pr_candidates[0];
  assert.notEqual(c.head_state,'CURRENT');
  assert.equal(c.material_status,'STALE_OR_UNPINNED');
  assert.equal(c.selected_ci_qualified,false);
  assert.equal(s.next_candidate_verification,'REFRESH_PROVIDER_CURRENT_PR_AND_EVIDENCE');
  assert.ok(s.blockers.includes('PROVIDER_HEAD_STALE_OR_UNPINNED'));
 }
});
test('changed provider digest, forged CI outcome and forged Owner decision fail before R4',async()=>{
 const provider=await facts(),s=deriveCandidateState(provider);
 for(const bad of [
  {...s,accepted_claim_count:8},{...s,authorization_granted:true},
  {...s,pr_candidates:[{...s.pr_candidates[0],selected_ci_qualified:false}]}
 ]){
  assert.throws(()=>verifyCandidateState(bad,provider),
   e=>e instanceof CandidateStateError&&e.code==='STATE_MISMATCH');
 }
 const mutated=JSON.parse(JSON.stringify(provider));
 mutated.pr_facts[0].ci_workflows[0].state='FAIL';
 assert.throws(()=>deriveCandidateState(mutated),
  e=>e instanceof CandidateStateError&&e.code==='SNAPSHOT_DIGEST_MISMATCH');
});
test('repeated observation with same source is stable and content addressed',async()=>{
 const provider=await facts({merged:true});
 const a=deriveCandidateState(provider),b=deriveCandidateState(provider);
 assert.equal(a.candidate_state_sha256,b.candidate_state_sha256);
 assert.match(a.candidate_state_sha256,/^[a-f0-9]{64}$/);
});
