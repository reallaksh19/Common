/* Node-only U4 conformance negative controls. The Python cross-language suite
 * exercises actual U1/U2/U3 fixture validation. This file never asserts source
 * authenticity, native DELP acceptance or reviewer/write authority.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import {canonicalJSON,fingerprint,checkConformance,ConformanceError} from './lifecycle-conformance-v1.mjs';

const error = code => e => e instanceof ConformanceError && e.code === code;
function packet() {
  const identity={schema:'synthetic-fixture-only',programme:{id:'p',root_issue:7}};
  const owner_session={identity,owner_events:[{id:'O001',claim:'unknown'}]};
  const evidence_review={owner_session,checkpoint_facts:{units:[{id:'U1',state:'FAILED'}]}};
  return {
    schema:'relay-lifecycle-cross-language-v1',
    identity,owner_session,evidence_review,
    expected:{identity_sha256:fingerprint(identity),history_sha256:fingerprint(owner_session),
              evidence_claim_sha256:fingerprint(evidence_review)}
  };
}
test('positive: three consistent canonical hashes never authorize',()=>{
  const r=checkConformance(packet());
  assert.equal(r.digest_agreement,'MATCHED_CALLER_SUPPLIED_DIGESTS_ONLY');
  assert.equal(r.source_authenticity,'NOT_CHECKED');
  assert.equal(r.python_contract_status,'NOT_CHECKED_BY_NODE');
  assert.equal(r.native_delp_execution,'NOT_PERFORMED_BY_NODE');
  assert.equal(r.reviewer_authorization,'NOT_GRANTED');
  assert.equal(r.exclusive_writer_lease,'NOT_PROVEN');
  assert.equal(r.canonical_programme_projection,'NOT_CALCULATED');
  assert.equal(r.programme_progress,null);
});
test('key order does not change portable digest',()=>{
  const a={a:7,z:{b:'café 🐈',a:2}};
  const b={z:{a:2,b:'café 🐈'},a:7};
  assert.equal(fingerprint(a),fingerprint(b));
  assert.equal(canonicalJSON(a),canonicalJSON(b));
});
test('negative: moved candidate under nested history refuses',()=>{
  const p=JSON.parse(JSON.stringify(packet()));
  p.owner_session.identity.programme.root_issue=9;
  assert.throws(()=>checkConformance(p),error('NESTED_SOURCE_DRIFT'));
});
test('negative: changed owner amendment invalidates old golden',()=>{
  const p=JSON.parse(JSON.stringify(packet()));
  p.owner_session.owner_events[0].claim='changed';
  p.evidence_review.owner_session.owner_events[0].claim='changed';
  assert.throws(()=>checkConformance(p),error('CONFORMANCE_DIGEST_MISMATCH:history_sha256'));
});
test('negative: forged reviewer grant cannot be a conformance field',()=>{
  const p=packet();p.approved_writer=true;
  assert.throws(()=>checkConformance(p),error('BAD_PACKET_SHAPE'));
});
test('negative: caller changes expected hash to malformed length',()=>{
  const p=packet();p.expected.identity_sha256='sha256:evil';
  assert.throws(()=>checkConformance(p),error('BAD_DIGEST_FORMAT'));
});
test('negative: malicious input with accessor key refused',()=>{
  const o=Object.create(null);
  Object.defineProperty(o,'foo',{enumerable:true,get(){throw Error('should not be read');}});
  assert.throws(()=>canonicalJSON(o),error('ACCESSOR_PROPERTY'));
});
test('negative: cyclic object refused',()=>{
  const o={};o.self=o;
  assert.throws(()=>canonicalJSON(o),error('UNSAFE_JSON_TYPE'));
});
test('negative: sparse array refused',()=>{
  const a=[];a[1]='x';
  assert.throws(()=>canonicalJSON(a),error('SPARSE_OR_ACCESSOR_ARRAY'));
});
test('negative: nonportable integer/negative-zero/floats refused',()=>{
  for(const v of [NaN,Infinity,Number.MAX_SAFE_INTEGER+1,3.14,-0])
    assert.throws(()=>canonicalJSON({n:v}),error('NON_PORTABLE_NUMBER'));
});
test('negative: isolated Unicode surrogate refused',()=>{
  assert.throws(()=>canonicalJSON({a:'\ud800'}),error('UNPAIRED_UNICODE_SURROGATE'));
});
test('negative: nonportable Unicode object keys refused',()=>{
  assert.throws(()=>canonicalJSON({'🐈':'cat'}),error('NON_PORTABLE_KEY'));
});
test('negative: detached identity cannot be conflated with validated Python facts',()=>{
  const p=packet();p.evidence_review.owner_session.identity.programme.root_issue=55;
  assert.throws(()=>checkConformance(p),error('CONFORMANCE_DIGEST_MISMATCH:identity_sha256'));
});
