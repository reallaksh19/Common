/* RELAY RESET R4 Batch-01 — PURE proposals only, no GitHub access or writes.
 * One immutable R3-A native/provider-injected snapshot -> issue, PR, handover.
 * Source/provider truth != human review, Owner authenticity, or accepted evidence.
 */
import {createHash} from 'node:crypto';
import {canonicalJSON} from './provenance-v1.mjs';

export class PreviewError extends Error {
  constructor(code,why){super(code+': '+why);this.name='PreviewError';this.code=code;}
}
const fail=(code,why)=>{throw new PreviewError(code,why);};
const HASH=/^[0-9a-f]{64}$/,SHA=/^[0-9a-f]{40}$/;
const REPO=/^[a-zA-Z0-9-]{1,39}\/[a-zA-Z0-9_.-]{1,100}$/;
const STATES=new Set(['PASS','FAIL','PENDING','UNKNOWN']);
function sha(x){return createHash('sha256').update(canonicalJSON(x)).digest('hex');}
function exact(o,keys,label){
  if(!o||typeof o!=='object'||Array.isArray(o)||
    Object.keys(o).some(k=>!keys.includes(k))||
    keys.some(k=>!Object.hasOwn(o,k)))fail('INVALID',label+' missing or unknown property');
}
function freeze(root){
  const seen=new Set(),stack=[root];
  while(stack.length){
    const v=stack.pop();if(!v||typeof v!=='object'||seen.has(v))continue;
    seen.add(v);for(const w of Object.values(v))if(w&&typeof w==='object')stack.push(w);
    Object.freeze(v);
  }
  return root;
}
function utc(value){
  return typeof value==='string'&&/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(value)
    &&Number.isFinite(Date.parse(value));
}
function safeString(v){return typeof v==='string'&&v.length>0;}
function checkSnapshot(input){
  let s;
  try{s=JSON.parse(canonicalJSON(input));}catch{fail('INVALID','snapshot not canonical-safe JSON');}
  exact(s,['schema','repository','observed_at','parent_issue','child_issues','pr_facts',
    'relationship_assertion','provider_transport','read_count','source_state','consistency',
    'evidence_acceptance','human_review','owner_intent','independent_journal_tip','actual_next',
    'authorization_granted','independently_accepted','live_writer_enabled','snapshot_sha256'],'R3 snapshot');
  if(s.schema!=='relay-provider-facts-v1'||!HASH.test(s.snapshot_sha256)||
    !REPO.test(s.repository)||!utc(s.observed_at)||
    !['PROVIDER_OBSERVED','INJECTED_UNVERIFIED'].includes(s.source_state)||
    (s.source_state==='PROVIDER_OBSERVED')!==(s.provider_transport==='NATIVE_GITHUB_GET')||
    s.consistency!=='PR_DOUBLE_READ_NON_ATOMIC'||
    s.relationship_assertion!=='CALLER_SCOPED_UNVERIFIED'||
    s.evidence_acceptance!=='NOT_EVALUATED'||s.human_review!=='NOT_EVALUATED'||
    s.owner_intent!=='NOT_AUTHENTICATED'||s.independent_journal_tip!=='NOT_ANCHORED'||
    s.authorization_granted!==false||s.independently_accepted!==false||
    s.live_writer_enabled!==false||!Number.isSafeInteger(s.read_count)||s.read_count<4)
    fail('UNTRUSTED','R3 snapshot cannot be an accepted/atomic/authorizing source');
  const declared=s.snapshot_sha256;delete s.snapshot_sha256;
  if(sha(s)!==declared)fail('DIGEST_MISMATCH','snapshot was mutated after its digest was published');
  s.snapshot_sha256=declared;
  const base='https://github.com/'+s.repository+'/';
  if(!s.parent_issue||!Number.isSafeInteger(s.parent_issue.number)||
    s.parent_issue.number<1||s.parent_issue.source_url!==base+'issues/'+s.parent_issue.number||
    !['open','closed'].includes(s.parent_issue.state)||
    !Array.isArray(s.child_issues)||s.child_issues.length>3||
    !Array.isArray(s.pr_facts)||s.pr_facts.length<1||s.pr_facts.length>4)
    fail('UNTRUSTED','parent/children/PR shape invalid');
  const ids=new Set([s.parent_issue.number]);
  for(const c of s.child_issues){
    if(!c||!Number.isSafeInteger(c.number)||c.number<1||
      ids.has(c.number)||c.source_url!==base+'issues/'+c.number||
      !['open','closed'].includes(c.state))fail('UNTRUSTED','child issue invalid or repeated');
    ids.add(c.number);
  }
  const prs=new Set();
  for(const p of s.pr_facts){
    if(!p||!Number.isSafeInteger(p.number)||p.number<1||prs.has(p.number)||
      p.source_url!==base+'pull/'+p.number||!SHA.test(p.head_sha)||
      !SHA.test(p.base_sha)||typeof p.draft!=='boolean'||
      typeof p.merged!=='boolean'||!['open','closed'].includes(p.state)||
      !['MATCH','STALE','UNPINNED'].includes(p.currentness)||
      (p.currentness==='MATCH'&&p.expected_head_sha!==p.head_sha)||
      (p.currentness==='STALE'&&(!SHA.test(p.expected_head_sha)||p.expected_head_sha===p.head_sha))||
      (p.currentness==='UNPINNED'&&p.expected_head_sha!==null)||
      (p.merged&&p.state!=='closed')||
      !Array.isArray(p.ci_workflows)||p.ci_workflows.length<1||p.ci_workflows.length>8)
      fail('UNTRUSTED','PR observation or currentness invalid');
    prs.add(p.number);
    const paths=new Set();
    for(const w of p.ci_workflows){
      if(!w||!safeString(w.path)||paths.has(w.path)||!STATES.has(w.state)||
        w.head_sha!==p.head_sha||
        (w.run_id!==null&&(!Number.isSafeInteger(w.run_id)||w.run_id<1))||
        (w.state==='PASS'&&w.run_conclusion!=='success')||
        (w.state==='PENDING'&&w.run_status==='completed')||
        (w.state==='UNKNOWN'&&w.run_id!==null))
        fail('UNTRUSTED','CI observation inconsistent with selected PR HEAD');
      paths.add(w.path);
    }
  }
  return freeze(s);
}
function freshness(snapshot,options){
  exact(options,['evaluated_at','max_age_seconds'],'evaluation');
  if(!utc(options.evaluated_at)||!Number.isInteger(options.max_age_seconds)||
    options.max_age_seconds<1||options.max_age_seconds>3600)
    fail('INVALID','evaluation time or maximum age invalid');
  const delta=Date.parse(options.evaluated_at)-Date.parse(snapshot.observed_at);
  if(delta < -5000)fail('INVALID','evaluation precedes snapshot observation');
  return delta>options.max_age_seconds*1000?'STALE':'WITHIN_CONFIGURED_WINDOW';
}
function status(p,observedFresh,native){
  // Passing GitHub CI is neither approval nor independent acceptance.
  if(!native)return 'UNVERIFIED_TRANSPORT';
  if(observedFresh==='STALE'||p.currentness!=='MATCH')return 'STALE_OR_UNPINNED';
  const states=p.ci_workflows.map(w=>w.state);
  if(states.includes('UNKNOWN'))return 'UNKNOWN';
  if(states.includes('FAIL'))return 'CI_NON_SUCCESS';
  if(states.includes('PENDING'))return 'PENDING';
  // Scope lists selected workflow paths, not the repo's authoritative required checks.
  return states.every(x=>x==='PASS')?'SELECTED_CI_PASS_ONLY':'UNKNOWN';
}
function compactTitle(parts){
  const out=parts.join(' | ');
  if(out.length>235)fail('LIMIT','preview title exceeds safe bounded size');
  return out;
}

/** Pure/immutable: never fetch, write, or infer a human acceptance. */
export function renderRelayPreviews(rawSnapshot,rawOptions){
  const s=checkSnapshot(rawSnapshot);
  let o;
  try{o=JSON.parse(canonicalJSON(rawOptions));}catch{fail('INVALID','evaluation parameters invalid');}
  const fresh=freshness(s,o),native=s.source_state==='PROVIDER_OBSERVED';
  const source=s.snapshot_sha256;
  const prTitles=s.pr_facts.map(p=>{
    const health=status(p,fresh,native);
    return {number:p.number,source_url:p.source_url,head_sha:p.head_sha,
      state:health,original_provider_state:p.state,
      workflow_scope:'CALLER_SELECTED_NOT_REQUIRED_POLICY',
      checked_workflow_paths:p.ci_workflows.map(w=>w.path),
      consistency:s.consistency, freshness:fresh,
      title:compactTitle(['RELAY PROPOSED ONLY','PR#'+p.number,
        'HEAD '+p.head_sha.slice(0,8),'CI '+health,'REVIEW NOT_EVALUATED']),
      snapshot_sha256:source,proposal_only:true};
  });
  const children=s.child_issues.map(c=>({
    number:c.number,source_url:c.source_url,state:c.state,
    title:compactTitle(['RELAY PROPOSED ONLY','ISSUE#'+c.number,
      'STATE '+c.state.toUpperCase(),'ACCEPTANCE NOT_EVALUATED']),
    snapshot_sha256:source,proposal_only:true,
    freshness:fresh,consistency:s.consistency
  }));
  const parent=s.parent_issue;
  const summary={
    parent_number:parent.number,source_url:parent.source_url,
    title:compactTitle(['RELAY PROPOSED ONLY','PARENT#'+parent.number,
      'PRs '+s.pr_facts.length,'REVIEWS NOT_EVALUATED','ACCEPTANCE UNKNOWN']),
    child_count:children.length,pr_count:prTitles.length,
    freshness:fresh,consistency:s.consistency,
    states:prTitles.map(p=>({number:p.number,state:p.state})),
    snapshot_sha256:source,proposal_only:true,
    managed_block_preview:'<!-- RELAY_R4_DRAFT_ONLY; DO NOT WRITE -->\n'+
      'R3 observed: '+s.observed_at+'\n'+
      'Snapshot SHA256: '+source+'\n'+
      'Provider: '+s.source_state+'; '+s.consistency+'\n'+
      'Reviewer status: NOT_EVALUATED; Owner authority: NOT_AUTHENTICATED\n'+
      'CI paths are CALLER_SELECTED, NOT proven required policy checks\n'+
      prTitles.map(p=>'PR #'+p.number+' '+p.head_sha.slice(0,8)+' '+p.state).join('\n')+
      '\n<!-- END RELAY_R4_DRAFT_ONLY -->'
  };
  const handover={
    title:'RELAY successor fact-only preview — NOT AN OWNER-AUTHORIZED HANDOVER',
    parent_url:parent.source_url,
    evidence_refs:[parent.source_url,...children.map(x=>x.source_url),
      ...prTitles.map(x=>x.source_url)],
    pr_heads:prTitles.map(p=>({number:p.number,head_sha:p.head_sha,state:p.state})),
    instructions:[
      'Fetch canonical parent and original Owner instructions; source chat permalink UNKNOWN',
      'Do not treat issue/PR titles, selected hosted green CI or this preview as accepted TaskEvidence',
      'CI workflow paths are caller-selected, NOT independently verified required checks',
      'Qualify independent source reviewers and merge/restack dependencies before R3-B integration',
      'Preserve human privacy/retention/Owner grant HOLD; do not activate R5 writer',
      'Read a new provider-current snapshot; this is bounded and non-atomic'
    ],
    source_status:s.source_state,consistency:s.consistency,
    freshness:fresh,observed_at:s.observed_at,evaluated_at:o.evaluated_at,
    owner_message_authenticated:false,independently_accepted:false,
    authorization_granted:false,live_writer_enabled:false,
    snapshot_sha256:source,proposal_only:true
  };
  const core={
    schema:'relay-projection-preview-v1',snapshot_sha256:source,
    source_state:s.source_state,freshness:fresh,
    observed_at:s.observed_at,evaluated_at:o.evaluated_at,
    parent_issue:summary,child_issues:children,pr_titles:prTitles,
    successor_handover:handover,
    proposal_only:true,
    owner_message_authenticated:false,authorization_granted:false,
    independently_accepted:false,live_writer_enabled:false
  };
  const result={...core,projection_sha256:sha(core)};
  return freeze(result);
}
