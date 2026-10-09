/* V3.5-R14 WP1/U4 — cross-language canonical-json digest agreement ONLY.
 * This intentionally does NOT duplicate Python U1/U2/U3 schema or DELP acceptance.
 * A matching SHA-256 is content integrity, not verified source, reviewer,
 * Owner permission, exclusive execution lease, or progress/CI qualification.
 */
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';

export class ConformanceError extends Error {
  constructor(code) { super(code); this.name = 'ConformanceError'; this.code = code; }
}
const reject = code => { throw new ConformanceError(code); };
const DIGEST = /^sha256:[0-9a-f]{64}$/;
const SIMPLE_KEY = /^[A-Za-z_][A-Za-z0-9_.:-]{0,127}$/;
const SHA_SCHEMA = 'relay-lifecycle-cross-language-v1';
const MAX_BYTES = 2 * 1024 * 1024;
const has = (o,k) => Object.prototype.hasOwnProperty.call(o,k);
const plain = v => v !== null && typeof v === 'object' && !Array.isArray(v)
  && (Object.getPrototypeOf(v) === Object.prototype || Object.getPrototypeOf(v) === null);
function keysAre(v, names, code) {
  if (!plain(v) || Object.keys(v).length !== names.length ||
      !names.every(x => has(v,x))) reject(code);
}
function hasIsolatedSurrogate(s) {
  for(let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF) {
      const next = s.charCodeAt(i+1);
      if (!(next >= 0xDC00 && next <= 0xDFFF)) return true;
      i++;
    } else if (c >= 0xDC00 && c <= 0xDFFF) return true;
  }
  return false;
}
export function canonicalJSON(value) {
  const active = new Set();
  let count = 0;
  function normalize(v,depth) {
    if(depth > 128 || ++count > 100000) reject('INPUT_COMPLEXITY_LIMIT');
    if(v === null || typeof v === 'boolean') return v;
    if(typeof v === 'string') {
      if(hasIsolatedSurrogate(v)) reject('UNPAIRED_UNICODE_SURROGATE');
      return v;
    }
    if(typeof v === 'number') {
      // All numbers in the supported closed Python U1/U2/U3 schemas are integers.
      // Do not silently normalize 1.0 or lose precision across runtimes.
      if(!Number.isSafeInteger(v) || Object.is(v,-0)) reject('NON_PORTABLE_NUMBER');
      return v;
    }
    if(!v || typeof v !== 'object' || active.has(v)) reject('UNSAFE_JSON_TYPE');
    active.add(v);
    try {
      if(Array.isArray(v)) {
        if(v.length > 10000) reject('ARRAY_LIMIT');
        const a = [];
        for(let i=0;i<v.length;i++) {
          if(!has(v,i) || !Object.hasOwn(Object.getOwnPropertyDescriptor(v,String(i)), 'value'))
            reject('SPARSE_OR_ACCESSOR_ARRAY');
          a.push(normalize(v[i],depth+1));
        }
        return a;
      }
      if(!plain(v)) reject('NON_PLAIN_OBJECT');
      const ret = Object.create(null);
      for(const key of Object.keys(v).sort()) {
        if(!SIMPLE_KEY.test(key) || hasIsolatedSurrogate(key)) reject('NON_PORTABLE_KEY');
        const descriptor = Object.getOwnPropertyDescriptor(v,key);
        if(!descriptor || !has(descriptor,'value')) reject('ACCESSOR_PROPERTY');
        ret[key] = normalize(descriptor.value,depth+1);
      }
      return ret;
    } finally { active.delete(v); }
  }
  const str=JSON.stringify(normalize(value,0));
  if(Buffer.byteLength(str,'utf8') > MAX_BYTES) reject('INPUT_BYTES_LIMIT');
  return str;
}
export function fingerprint(value) {
  return 'sha256:'+createHash('sha256').update(canonicalJSON(value),'utf8').digest('hex');
}
export function checkConformance(packet) {
  keysAre(packet,['schema','identity','owner_session','evidence_review','expected'],'BAD_PACKET_SHAPE');
  if(packet.schema !== SHA_SCHEMA) reject('WRONG_PACKET_SCHEMA');
  keysAre(packet.expected,['identity_sha256','history_sha256','evidence_claim_sha256'],'BAD_EXPECTATIONS');
  for(const d of Object.values(packet.expected)) if(typeof d!=='string'||!DIGEST.test(d))reject('BAD_DIGEST_FORMAT');
  if(!plain(packet.identity) || !plain(packet.owner_session) || !plain(packet.evidence_review))
    reject('BAD_SUBJECT_SHAPE');
  if(canonicalJSON(packet.identity) !== canonicalJSON(packet.owner_session.identity) ||
     canonicalJSON(packet.owner_session) !== canonicalJSON(packet.evidence_review.owner_session))
    reject('NESTED_SOURCE_DRIFT');
  const computed={
    identity_sha256:fingerprint(packet.identity),
    history_sha256:fingerprint(packet.owner_session),
    evidence_claim_sha256:fingerprint(packet.evidence_review),
  };
  for(const [k,v] of Object.entries(computed))
    if(packet.expected[k] !== v) reject('CONFORMANCE_DIGEST_MISMATCH:'+k);
  return Object.freeze({
    schema:SHA_SCHEMA,
    digest_agreement:'MATCHED_CALLER_SUPPLIED_DIGESTS_ONLY',
    identity_sha256:computed.identity_sha256,
    history_sha256:computed.history_sha256,
    evidence_claim_sha256:computed.evidence_claim_sha256,
    source_authenticity:'NOT_CHECKED',
    python_contract_status:'NOT_CHECKED_BY_NODE',
    native_delp_execution:'NOT_PERFORMED_BY_NODE',
    reviewer_authorization:'NOT_GRANTED',
    owner_authorization:'NOT_GRANTED',
    exclusive_writer_lease:'NOT_PROVEN',
    publisher:'OFF',
    canonical_programme_projection:'NOT_CALCULATED',
    programme_progress:null,
  });
}

async function runCLI() {
  let raw='';
  for await (const chunk of process.stdin) {
    raw+=chunk;
    if(Buffer.byteLength(raw,'utf8') > MAX_BYTES) reject('INPUT_BYTES_LIMIT');
  }
  let doc;
  try { doc=JSON.parse(raw); } catch { reject('NOT_JSON'); }
  process.stdout.write(JSON.stringify(checkConformance(doc))+'\n');
}
if(process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  runCLI().catch(e=>{
    process.stderr.write((e instanceof ConformanceError ? e.code : 'UNEXPECTED_ERROR')+'\n');
    process.exitCode=2;
  });
}
