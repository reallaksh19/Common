# BUDDY RUNNER V3.2 / COMMON #733 — HOW THE TWO GOLDEN PROMPTS WERE BUILT, AND WHAT A ROBUST PAIR REQUIRES

DOCUMENT_ID: BR-DESIGN-COMMON-733-V1
TYPE: ENGINEERING DESIGN RATIONALE + TEST/PROVENANCE CONTRACT
STATUS: RESEARCH FIXTURE / DRAFT PR REVIEW; NOT A DELIVERED RUNNER SYSTEM
AUTHORSHIP: ChatGPT's documented, reproducible prompt-design method; not a reproduction of hidden internal reasoning
SCOPE: Engineering Relay V3.2 / Common #718 → Common #733, R-PROJECTION, ESC-3
DATE: 2026-10-09

## 0. Why this exists

The Owner proposes a **delayed Buddy Runner**: Agent 1 (striker) works alone until roughly 70% of its reliable episode life is consumed, requests a Runner through TASK_EVIDENCE, and keeps working. Agent 2 begins **Stage 1** independently from original engineering intent, its historically original source baseline, WHAT/WHY and known/pending/parked problems, *without seeing* the predecessor's code HOW, PR/CI statistics or final plan. Only after the independent plan is sealed is **Stage 2** released: the Runner receives actual current repository state and the predecessor's final plan, reconciles rather than copies, records justified high-ROI absorption and parked medium-ROI ideas, and becomes striker only with exclusive execution authorization. Agent 2 should in turn prepare Runner 2 when appropriate.

This mechanism is **not**: two-pass reasoning; a concurrent second developer; a standing independent reviewer; a conventional last-minute handover; an automatic task-reassignment trigger; or an authorization substitute for Owner decisions.

This dossier is a retrospective fixture built on genuine Common #733 source and Owner records. The nominal 70% trigger and the Agent 1 WHAT/WHY packet are **constructed case-study input**, not a recovered, authenticated Agent 1 private session. We lack real context telemetry, genuine Agent 1's original session-start SHA, original ChatGPT-message permalink and an authenticated historical Stage 2 disclosure. Therefore the pilot can test independent source reconstruction and plan reconciliation, not yet prove improvement in recovery from a real agent injury.

## 1. Canonical fixture artifacts and custody

The PR adds *copies and specifications*, not modifications of the existing Stage 1 execution result:

- **STAGE1_RUNNER_PROMPT_V1.md**: byte-identical copy of original prompt relay/BUDDY_RUNNER/CHATGPT_COMMON_733/BR-STAGE1-COMMON-733-v1.md. Original source Git blob: 42c3dc4d119ac2e16d94f97b65e5f79ed13f1c47.
- **STAGE2_RUNNER_PROMPT_V1.md**: new successor prompt, withheld from Runner until Stage 1 output and allowed-source evidence are sealed. Contains instructions for reality disclosure, independent reconciliation, revised workpack and a separately governed promotion barrier. It is not an Agent 1 final disclosure.
- **PROMPT_DESIGN_METHOD_AND_ROBUSTNESS.md**: this design source/methodology, requirements and independent test catalogue.
- **FIXTURE_MANIFEST.json** and **SHA256SUMS**: provenance labels and actual committed-byte receipts, to be checked against the exact PR commit.

Existing, DO NOT EDIT in this PR:
- Stage 1 input: relay/BUDDY_RUNNER/CHATGPT_COMMON_733/BR-STAGE1-COMMON-733-v1.md.
- Stage 1 Runner output: relay/BUDDY_RUNNER/CHATGPT_COMMON_733/INDEPENDENT_RECONSTRUCTION_V1.md.
- Stage 1 Runner output byte receipt: relay/BUDDY_RUNNER/CHATGPT_COMMON_733/INDEPENDENT_RECONSTRUCTION_V1.sha256.

The Runner response was committed at Common 0b1c9d2b032aa82e5c98d38cd67af33b59642427, and independently verified as SHA-256:
fca6cc5994d79716f1f05304611f1f520f18a7ca47b60803c943fbda88ae59c4

The external **allowed-input manifest seal** was NOT proved by this SHA; it remains PENDING. A hash establishes fixed bytes, not the history of what the agent could read.

## 2. HOW the Stage 1 prompt was constructed (reproducible procedure)

1. **Start with Owner language rather than the issue/PR title.** Preserve V3.2 Owner instructions from the archive at Common #718, including the complaint that statistics and issue titles had not achieved real parent→evidence→PR→handover/agent-metric integration. Preserve separate "verbatim archive" and "authenticated original chat" states. The latter is UNKNOWN; never assert it was independently authenticated.
2. **Select an actual historical source anchor.** Use Common source commit 80a9c03d8f33ace129d21cb868c93e9359a8868a (2026-10-08T04:44:06Z), containing an actual precommitted V3.2 golden-source record. It is a research cutoff, not proof of Agent 1's true original session-start.
3. **Pin the actual semantic responsibilities.** Read .github/v32-evidence-spine/718-proposal-v2.json at that commit. It binds Common #733 to R-PROJECTION / ESC-3 with VIEW-CONSISTENCY (34), VIEW-PR (33) and VIEW-DRIFT (33). It also identifies ESC-1/2 producers and ESC-4/5/6 consumers or joined acceptance, preventing unauthorized scope spread.
4. **Build an information firewall.** Split available facts into Stage 1 (original intent, original source, what/why, pending/known/parked, fixture INPUT identifiers) and Stage 2 (predecessor HOW, current implementation, current PR/CI, final plan, current source and test reality). Never include the successor answers, later patches or current-state statistics in Stage 1.
5. **Produce a non-solution WHAT/WHY packet.** Describe conflicts among parent/child/PR/status/handover representations and why they matter. Do not say "use adapter X", "change function Y" or pretend a reconstructed packet is a verbatim Agent 1 statement.
6. **Name the real golden-input boundary, not golden expected outputs.** The historical fixture file .github/v32-evidence-spine/718-golden-fixtures-v1.json exists at the cutoff with blob 278cd053a15ac8a87db1426c9de5e55acf1d283f. Provide permitted OR/ESC and GF-SMART-SURFACES, GF-PR-HEAD, GF-PUBLISH-RACE IDs and test families, but do not disclose expected strings/material identities. Label that raw file EVALUATOR-ONLY in Stage 1.
7. **Require active independent source investigation.** Have the Runner inspect frozen V3.2 modules and source consumers, cite functions and lines, evaluate at least two genuine architectures, propose positive/negative tests, select an implementation approach and produce a GitHub-ready plan without mutating an existing responsibility.
8. **Design stop and seal.** The Runner must return twelve sections and STAGE1_READY_FOR_SEAL. Its full bytes are committed and separately hashed before the Agent 1 final plan/current state is shown. Store missing telemetry and unknown original source authentically as UNKNOWN.
9. **Control source exposure in the experiment harness.** A repo path reference and "do not look" instruction are insufficient: the harness must furnish an isolated snapshot and restrict tools, not the entire live repo. This fixture is an instruction-level Stage 1 prompt; it does not implement that access-control harness.
10. **Assess the output without supplying answers.** Check independently whether source files were actually read, whether the plan differs from paraphrasing WHAT/WHY, whether it traces immutable Owner acceptance obligations and whether uncertainties remain explicit. Use withheld golden expected outputs and independent source verification.

The actual Agent 2 Stage 1 output was read back from GitHub and verified against its receipt, and six historical source file blob SHAs matched its claimed inspection list. This supports source grounding and output integrity, **not** full access isolation, source-test execution or live takeover.

## 3. HOW the Stage 2 prompt was constructed (reproducible procedure)

1. **Start from the sealed *independent* plan**, not from Agent 1's handover. Pin the exact Stage 1 artifact/receipt to prevent after-the-fact rewriting of the Runner's hypothesis.
2. **Require an external admission seal.** File SHA, allowed source/tool manifest, record of Stage 1 visibility and the operator's disclosure authorization are separate evidence. Failure to verify them is a blocker or expressly limited retrospective demo.
3. **Define what a truthful incumbent packet needs.** Request the original/current commits, verified releases/amendments, actual HOW and WHY, code/diffs/consumers, named tests and golden fixtures, accepted facts, PR/CI/provider observations, known failures, in-flight writes, pending work and parked ROI. Attribute the original Agent 1 transcript only if actually obtained.
4. **Allow current reality AFTER the gate.** Re-read the latest applicable repository code and governance; inspect issues, PRs, source heads, tests and real downstream consumers. Do not mistake the frozen Stage 1 source for the current implementation.
5. **Reconcile THREE things, not two summaries.** For every material difference compare: sealed Stage 1 plan ↔ Agent 1 plan ↔ independent observation of actual source/Owner contract. Decide ACCEPT_STAGE1, ACCEPT_AGENT1, REVISE_BOTH, OUTDATED, UNPROVEN or OUT_OF_SCOPE, with evidence.
6. **Preserve real dissent.** The Stage 1 submission treated a smart PR title as an optional derived projection; the Owner's preserved instructions require real smart issue/draft PR presentation. The Stage 2 prompt includes this as a source-backed reconciliation challenge, not as an implementation command or invitation to rewrite Stage 1.
7. **Prepare a revised workpack, not a status narrative.** Require task dependencies, exact write-surface assumptions, source files/functions/consumers, positive and negative tests, real provider/Chromium acceptance where applicable, known risks, High-ROI reasoning and parked Medium-ROI with reentry criteria.
8. **Separate three authorities.** (a) READY_TO_RECONCILE does not mean (b) PROMOTED_AS_STRIKER and neither implies (c) EXECUTION_VERIFIED. Exclusive branch/lease authority, freeze grants, Owner approval and current HEAD readback are separate gates.
9. **Protect V3.2 semantics.** Do not modify the original Stage 1 or Owner message; do not create duplicate issue ownership; do not compute P/E/D from prose; preserve distinct PR lifecycle versus engineering completion and exact-head evidence; do not self-authorize a new roadmap.
10. **Use a final independent receipt and explicit stopping conditions.** Stage 2 must produce its own reconciling artifact before source edits if takeover is blocked. It must not claim that this retrospective exercise proves recovery from a genuine context injury.

## 4. WHAT was necessary for robust prompts (evidence classes)

| Required class | Specific material or invariant | Reason |
| --- | --- | --- |
| Owner intent and authenticity | Verbatim historical quotation, original chat link UNKNOWN, source archive refs | Prevent inherited agent interpretations replacing Owner asks |
| True immutable baseline | Exact repository/commit, Git blob identities, permitted paths, historical cutoff | Avoid hindsight/source drift |
| Responsibility authority | Root #718, child #733, released proposal digest, ESC-3 and three weights | Avoid duplicate task, reweighting and scope creep |
| Limited WHAT/WHY input | Problems and rationale; pending, known and parked; non-verbatim provenance | Allows independent design without copying predecessor HOW |
| Source code and downstream consumers | Actual parser/projector/evidence/observer/issue/PR/handover call paths at allowed snapshot | Engineering plan must be source-grounded, not title-grounded |
| Independent acceptance oracles | Authentic golden-input IDs, withheld outputs, negative mutations, clean controls | Prevent tests tailored to implementation |
| Information firewall | No later branch, PR, CI, incumbent HOW, final plan or hidden fixture expected outputs | Preserves Stage 1 independence |
| Frozen output | 12-section plan, immutable commit, byte hash, allowed-input manifest seal | Makes independent comparison possible |
| Real current-state disclosure | Real or explicitly third-party reconstructed Agent 1 packet and verifiable provider/material truth | Prevent invented handover |
| Three-way reconciliation | Stage 1, incumbent approach, observed source and Owner acceptance | Avoid blind copying and false independence |
| High/Medium ROI discipline | Within-scope high-ROI justified and absorbed; medium-ROI explicitly parked | Preserve useful new ideas without patchwork or unauthorized feature growth |
| Publication and execution fencing | Single active writer, changed-HEAD checks, Owner approval, frozen paths, no synthetic P/E/D | Safe actual transfer instead of two competing coders |
| Context-life estimate | Approximate 70% usage; provider token telemetry when available; working-episode proxy and cognitive warnings | Trigger Runner while incumbent can still explain WHAT/WHY |
| Independent accountability | Distinct actor/credential or independently attested Owner-origin decisions | Prevent an agent approving itself |
| Failure outcomes | BLOCKED/UNKNOWN/STALE/CONTAMINATED are valid results | Fail closed; do not manufacture PASS from missing evidence |

## 5. Health trigger calibration — why 70% is a hypothesis

Do not confuse V3.2's seven engineering-health dimensions (materialization, evidence, checkpoint distance, size, base drift, interruptions and liveness) with remaining conversational/context budget. Nor is task completion percent equivalent to usable episode life consumed.

Proposed advisory event:
  RUNNER_SIGNAL: TIME_FOR_RUNNER
  runner_stage: STAGE1_READ_ONLY
  life_consumed_band: APPROX_65_TO_75_PERCENT
  estimate_method: PROVIDER_TELEMETRY | EPISODE_PROXY | AGENT_SELF_WARNING
  estimated_confidence: LOW | MEDIUM | HIGH
  actual_context_tokens: UNKNOWN_UNLESS_TELEMETRY_EXISTS
  progress_credit: NONE
  transfer_of_authority: false

Use reported provider context usage if trustworthy; otherwise record a coarse working-episode budget. Trigger early for repeated research, contradictions, context compression warnings, large next-work-unit demand or expected interruption. Do not wait for agent failure to request Stage 1. Experiment with 50%, 70%, 85% and a no-injury 70% control; compare total tokens/compute cost of both agents, time to first valid action, source correctness, false claims, and human interventions. Threshold optimum is UNKNOWN.

This event may be included as an advisory section of ordinary TASK_EVIDENCE, but must not mutate accepted CHECKPOINT_FACTS_V1 schema, computed P/E/D or accepted engineering-unit state. The agent's message does not automatically launch or authorize another agent without actual orchestration.

## 6. Robust negative tests and stage gates — proposed qualification

These are **proposed oracles**, not tests executed by this PR.

| ID | Attempt to break the design | Required rejection / evidence |
| --- | --- | --- |
| BR-G01 | Stage 1 prompt includes current PR number/head/CI | STAGE1_CONTAMINATED |
| BR-G02 | Stage 1 runner can open this PR, Stage 2 prompt or golden expected outcomes | STAGE1_ISOLATION_NOT_ENFORCED (do not pretend a successful blind run) |
| BR-G03 | Stage 1 uses current source instead of pinned historical commit | STAGE1_CONTAMINATED |
| BR-G04 | WHAT/WHY packet quotes predecessor HOW or prescribes code fix | STAGE1_CONTAMINATED |
| BR-G05 | Original chat permalink silently invented or GitHub mirror called original | PROVENANCE_FAIL |
| BR-G06 | Fake 70%-life reading or simulated Agent 1 session claimed live | FALSE_TRIGGER_EVIDENCE |
| BR-G07 | Runner reproduces Agent 1's plan without independent source/alternatives | INDEPENDENT_RECONSTRUCTION_FAIL |
| BR-G08 | Runner modifies engineering code or PR while preparing | STAGE1_AUTHORITY_FAIL |
| BR-G09 | Stage 1 result changes after it is hashed/sealed | RECEIPT_MISMATCH |
| BR-G10 | Stage 1 SHA matches but allowed-input manifest/tool audit absent | FILE_INTEGRITY_PASS / BLINDNESS_UNVERIFIED |
| BR-G11 | Stage 2 packet not authentically from Agent 1, but written as his words | PREDECESSOR_PROVENANCE_FAIL |
| BR-G12 | GitHub HEAD moved after final packet; Runner does not recheck | STAGE2_STALE_SOURCE |
| BR-G13 | Agent 1 still writing while Runner starts source modification | TAKEOVER_LEASE_CONFLICT |
| BR-G14 | Runner invents missing CHECKPOINT_FACTS, named tests, green CI or P/E/D | FALSE_PROGRESS_FAIL |
| BR-G15 | Runner creates duplicate #733 issue without independent new claim/approval | DUPLICATE_RESPONSIBILITY_FAIL |
| BR-G16 | Medium-ROI proposal silently becomes acceptance work or new roadmap | SCOPE_CREEP_FAIL |
| BR-G17 | Smart PR title left optional despite preserved mandatory Owner contract | OWNER_INTENT_RECONCILIATION_FAIL |
| BR-G18 | Source-correct but golden acceptance skipped; only screenshots/UI checked | VERIFICATION_INCOMPLETE |
| BR-G19 | No injury actually occurred but test claims demonstrated recovery | OVERCLAIMED_RECOVERY |
| BR-G20 | Successor cannot reconstruct next valid source change or cannot fence writes | TAKEOVER_NOT_QUALIFIED |
| BR-G21 | Clean control at same input produces inconsistent projections | DETERMINISM_FAIL |
| BR-G22 | Incomplete ESC-2 qualification treated as R-PROJECTION or PR VERIFIED | EVIDENCE_BOUNDARY_FAIL |
| BR-G23 | Mixed-epoch GitHub title/comment/PR updates declared atomic success | MIXED_BASIS_FAIL |
| BR-G24 | Fixture producer supplies Stage 2 in the same runner-readable workspace | FAIL_ISOLATION_BY_DESIGN |

For a full live trial, precommit each intervention's source/fixture SHA and the observable pass/fail oracle; run across multiple episodes/agent models; compare late-handover control with 50/70/85% activation and no-injury cost. Independent evaluator must not use Stage 2 knowledge when scoring Stage 1.

## 7. Security / publication / implementation boundaries

**Crucial limitation:** both prompts are archived in ONE GitHub PR and may become accessible through GitHub search or ordinary repo browsing. This is **not** a secured two-stage delivery mechanism. A trusted controller must create a sanitized Stage 1 workspace/snapshot at the historical commit and expose only Stage 1 permitted inputs, while withholding the Stage 2 fixture and all later content. The stage transition releases Stage 2 only after the receipt + input-manifest seal. A verbal "don't look" promise does not enforce blindness.

This PR changes ONLY relay/BUDDY_RUNNER/CHATGPT_COMMON_733/GOLDEN_FIXTURES/ research artifacts. It does not alter the frozen engineering-pr-delivery-v3.2 scripts, accepted graph, Owner issues, source publisher, telemetry, merge policy or PR production code. Fixture files are not independent publication authority.

Do not use this PR as acceptance of V3.2 production ESC-3, ESC-6 or the Buddy system. PR being draft, reviewed, merged or CI green does not prove a live two-stage recovery.

## 8. How to run the fixture responsibly

**Preparation:** Validate exact Stage 1 source/fixture blob against frozen 80a9c03...; create a clean Runner session; provide ONLY the archived Stage 1 prompt and allowlisted historical source snapshot; enforce technical tool restrictions; keep this PR and Stage 2 file invisible in that session. Record the allowed-input manifest and operator identity.

**Stage 1:** Run independent reconstruction, ask at most three WHAT/WHY questions, publish its plan under designated permitted experiment path only, hash actual committed bytes, independently verify GitHub readback, and seal. For the historical run recorded here, the Runner's output already exists with SHA fca6cc... but there is no independent proof of full tool-access isolation; do not misclassify it.

**Stage 2:** Only after sealed admission, allow Runner to inspect genuine Agent 1 disclosure and current/reconciled repository reality. Prepare three-way delta, revised plan, ROI triage and deterministic acceptance oracles. If no true predecessor remains, third-party reconstruction must be labeled as such.

**Promotion:** Obtain a separately authorized ownership transfer, fence Agent 1 writes, inspect moved HEAD and live work state, then and only then follow V3.x task decomposition, approved PLAN_UPDATE and real tests/implementation. If authority absent, stop after a proposal.

**Follow-on:** Collect timestamps, tokens (measured or UNKNOWN), duplicated reading, source correctness, human interventions, hold reasons and whether first resumed engineering action was actually valid. A single successful retrospective plan is not live takeover proof.

## 9. Evidence references and uncertainty ledger

- Canonical Owner programme: https://github.com/reallaksh19/Common/issues/718 ; original personal ChatGPT-message permalink UNKNOWN.
- Responsibility: https://github.com/reallaksh19/Common/issues/733 .
- Frozen historical code: https://github.com/reallaksh19/Common/tree/80a9c03d8f33ace129d21cb868c93e9359a8868a/skills/engineering-pr-delivery-v3.2 .
- Released source graph at freeze: https://github.com/reallaksh19/Common/blob/80a9c03d8f33ace129d21cb868c93e9359a8868a/.github/v32-evidence-spine/718-proposal-v2.json .
- Sealed historical evaluator oracle: https://github.com/reallaksh19/Common/blob/80a9c03d8f33ace129d21cb868c93e9359a8868a/.github/v32-evidence-spine/718-golden-fixtures-v1.json .
- Original Stage 1 prompt: https://github.com/reallaksh19/Common/blob/0b1c9d2b032aa82e5c98d38cd67af33b59642427/relay/BUDDY_RUNNER/CHATGPT_COMMON_733/BR-STAGE1-COMMON-733-v1.md .
- Independently authored Stage 1 reconstruction: https://github.com/reallaksh19/Common/blob/0b1c9d2b032aa82e5c98d38cd67af33b59642427/relay/BUDDY_RUNNER/CHATGPT_COMMON_733/INDEPENDENT_RECONSTRUCTION_V1.md .
- Stage 1 plan byte SHA: fca6cc5994d79716f1f05304611f1f520f18a7ca47b60803c943fbda88ae59c4.
- Broader E2E recovery programme: https://github.com/reallaksh19/Common/issues/879 .
- Related but separate LFJ Runner pilot: Common draft PR #880; its contamination lesson is relevant to isolation principles, but its source implementation/history must not be fed into this #733 Stage 1.

Open unresolved items: independent signed Stage 1 input-access manifest; authenticated original Agent 1 70%-trigger and disclosure; exact original coding-session start SHA; actual live two-agent timing/cost measurements; Stage 2 Runner response; formally approved takeover grant.

## 10. Acceptance of this PR versus success of the experiment

**Fixture PR acceptance (possible now):** Stage 1 byte-identical; Stage 2 does not predeclare current results; design methodology traces evidence and includes honest limits; protected original Stage 1/Runner output untouched; manifest/hashes agree with exact committed bytes; PR diff contains only new fixture artifacts; no accidental source-mutation/roadmap/progress claims.

**Actual Stage 1 experiment qualification (PARTIAL/UNVERIFIED):** Running independent reconstruction is observed and its bytes/source identities verified, but blindness/tool-access audit and original 70%-life invocation remain unverified.

**Actual Stage 2 experiment qualification (NOT RUN):** No authenticated Stage 2 disclosure, source reconciliation, promotion or live coding resumed by the Runner has yet been observed. A detailed prompt does not count as execution.

**Production Buddy Runner delivery (NOT IMPLEMENTED):** No monitoring/launcher/token accounting controller, read-access firewall, attested input manifest, runner lease switch, source permission upgrade or live recovery proof is introduced by this PR.

These four verdicts must remain separate. Do not upgrade any to PASS because this Markdown is complete.
