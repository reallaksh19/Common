/* R14 WP2/U01: non-production R12→V3.2 DELP diagnostic call edge.
 * R12 derives its native-in-process candidate before JSON serialization;
 * Python receives only data, never that in-process native provider capability.
 * No DELP acceptance, source authentication, PR/issue writers or plan mutation.
 */
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';

export class DiagnosticJoinError extends Error {
  constructor(code) { super(code); this.name = 'DiagnosticJoinError'; this.code = code; }
}
const fail = code => { throw new DiagnosticJoinError(code); };
const pythonScript = join(dirname(fileURLToPath(import.meta.url)), 'diagnostic_delp_bridge_v1.py');
const MAX_BYTES = 2 * 1024 * 1024;

export async function rehearseR12ToDelp(provider, graph, evidenceReview, opts={}) {
  // A pluggable Python binary is only for the controlled test/CI runner. No
  // shell, arbitrary command args, user-selected URL, network or GitHub writes.
  if (!opts || typeof opts !== 'object' || Array.isArray(opts) ||
      Object.keys(opts).some(k => k !== 'pythonBinary' && k !== 'timeoutMs')) fail('INVALID_OPTIONS');
  const binary = opts.pythonBinary ?? (process.platform === 'win32' ? 'python' : 'python3');
  if (typeof binary !== 'string' || !/^(?:python|python3|py)$/.test(binary)) fail('INVALID_PYTHON_BINARY');
  const timeout = opts.timeoutMs ?? 15000;
  if (!Number.isSafeInteger(timeout) || timeout < 500 || timeout > 30000) fail('INVALID_TIMEOUT');
  // Production R12 is imported from the existing RELAY source, NOT a copy.
  // It retains in-process native acquisition attestation at this JS edge;
  // Python deliberately downgrades the serialized result to UNATTESTED.
  let candidate;
  try {
    const native = await import('../candidate-verification-v1.mjs');
    candidate = native.deriveCandidateState(provider);
  } catch { fail('R12_CANDIDATE_VERIFICATION_FAILED'); }
  const packet = {schema:'relay-diagnostic-delp-bridge-v1', graph,
                  evidence_review:evidenceReview, candidate_state:candidate};
  let input;
  try { input = JSON.stringify(packet); }
  catch { fail('INPUT_NOT_JSON'); }
  if (Buffer.byteLength(input,'utf8') > MAX_BYTES) fail('INPUT_BYTES_LIMIT');
  const result = spawnSync(binary,[pythonScript],{
    input,encoding:'utf8',shell:false,maxBuffer:MAX_BYTES,timeout,
    env:{PATH:process.env.PATH ?? '',PYTHONDONTWRITEBYTECODE:'1'}
  });
  if (result.error || result.status !== 0 || !result.stdout) fail('NATIVE_DELP_DIAGNOSTIC_NOT_VERIFIED');
  let body;
  try { body = JSON.parse(result.stdout); } catch { fail('MALFORMED_PYTHON_DIAGNOSTIC'); }
  // A corrupted or falsely permissive Python output fails closed as a whole.
  if (body?.schema !== 'relay-diagnostic-delp-bridge-v1-result' ||
      body.r12_candidate_state_sha256 !== candidate.candidate_state_sha256 ||
      body.actual_delp_source !== 'EXISTING_V3_2_PROJECT' ||
      body.provider_authenticity !== 'NOT_ATTESTED_AFTER_SERIALIZATION' ||
      body.reviewer_admission !== 'NOT_QUALIFIED' || body.publishable_snapshot !== false ||
      body.live_status_writer !== 'OFF' || body.quarantined_ledger_claims !== 1 ||
      body.diagnostic_leaf?.P !== 0 || body.diagnostic_leaf?.E !== 0 ||
      body.diagnostic_root?.D !== 0 || body.diagnostic_root?.E !== 0) fail('NONQUARANTINED_OR_FORGED_PYTHON_RESULT');
  return Object.freeze(body);
}
