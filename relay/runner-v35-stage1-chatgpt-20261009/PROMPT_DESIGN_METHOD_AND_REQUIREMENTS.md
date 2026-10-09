# How the V3.5 Runner Stage 1 and Stage 2 Golden Prompts Were Constructed

**Record type:** Authoring-method disclosure, source-provenance ledger, robustness contract and future evaluation guidance.  
**Date:** 2026-10-09  
**Scope:** Runner-first V3.5 continuity experiment; **two operating stages, not two passes**.  
**Location:** `relay/runner-v35-stage1-chatgpt-20261009/`.  
**Authority:** Documentation-only research; this record does not release V3.5 WP1, activate production writes, qualify AC1–AC8, assign a leaf or admit Stage 2.

## 1. Exact fixture inventory and immutability

| Role | Repository file | Commitment |
|---|---|---|
| Frozen original Stage 1 prompt | `STAGE1_RUNNER_PROMPT.md` | Existing, never modified in this PR |
| Golden Stage 1 input | `fixtures/STAGE1_RUNNER_PROMPT.md` | Exact UTF-8 byte copy of the frozen original |
| Golden Stage 2 input | `fixtures/STAGE2_RUNNER_PROMPT.md` | Newly authored successor reconciliation prompt |
| Actual prior Stage 1 runner result | `RUNNER_RECONSTRUCTION_V1.md` | Existing frozen research output, unchanged |
| This construction and quality record | `PROMPT_DESIGN_METHOD_AND_REQUIREMENTS.md` | Documents source reasoning and validation |

**Stage 1 SHA-256:** `3d76575be628666b323f887a1d33716b172e5b836b789be57d69614a6e54d649` (actual committed bytes).  
**Stage 1 Git blob SHA:** `0e6a71623a1ad03b1bf29eba54a503d396f2084f`.  
**Stage 2 SHA-256:** `f867751d5edbc23403ae64cfcddebd7511ef93172126bbee6ef1543e67071ad1` (actual committed bytes).  
**Stage 2 Git blob SHA:** `76a841dd2c43a9acd901ebec8fdc9f2e313a295e`.  
**Frozen Runner reconstruction:** `Common@38ffb797a0993320ce198ddcd414e14856966251`, SHA-256 `7c2903666c47f5ab1e5f7579a612d045cc8ee86b4f844abbdc17121f6c0c0056`.

These are content-integrity receipts, **not** verified Owner identity, code completion, blind independence, review approval, source authenticity or permission to write. A runner should independently recalculate bytes and compare before use.

## 2. HOW Stage 1 was developed — the actual derivation sequence

The first prompt was produced **from the project's Owner conversation and my prior V3.5 context**, followed by explicit read-only checks against real GitHub sources. It was not derived by watching Agent A at an authenticated live 70% context-consumption event.

1. **Extracted the actual Owner problem rather than beginning from a PR title.** The Owner wanted a physically connected lifecycle: Owner original intent → parent → task decomposition → child issues/comments → source-bound TASK_EVIDENCE → derived issue scoreboards and smart PR metadata → repo-wise intent/session/changed-module index → successor handover. The user's correction rejected mere component demonstrations.
2. **Preserved first-person Owner words separately from interpretations.** The exact language mirrored in [Common #787 §0](https://github.com/reallaksh19/Common/issues/787) and the later correction mirrored in [Common #878](https://github.com/reallaksh19/Common/issues/878) were supplied as attributed quotations. The original authenticated private-chat permalink remains UNKNOWN; the GitHub copies are mirrors. My summaries of why successors struggle are marked interpretations, not new Owner quotations.
3. **Chose one immutable source boundary:** `Common@13989969f6b7e432c4f7c1ddfe975449dba53593`. This was a defensible historical V3.5 protocol reference, **NOT proven Agent A's first work commit**. The prompt expressly prohibits conflating them. The freeze prevents a runner from quietly learning Agent A's later implementation through a moving `main`.
4. **Translated the permissible requirements into a staged source packet:** scoped original Owner text, curated #864 roadmap *categories*, Owner correction from #878, baseline V3.5 source and contracts, an optional separate lab golden oracle. Suppressed later GitHub issue tails, branches, active PR stats, current diff, CI totals, Agent A's algorithm and final plan.
5. **Supplied Agent A's WHAT/WHY as a constructed rehearsal briefing, not evidence.** Topics: original intent custody, parent/child graph, evidence eligibility, live status, index, handover and whole-system acceptance. We had no authenticated live Agent A briefing. The prompt labels the text `CLAIM_ONLY` or problem analyzed and prohibits inferred implementation success.
6. **Captured pending, known and parked separately:** obligations to verify interfaces; risk hypotheses and unknowns; optional medium ROI and production permissions parked without inflating scope. This forces independent prioritization instead of reciting a purported predecessor TODO list.
7. **Defined seven source-agnostic but falsifiable acceptance oracles:** G-INTENT, G-PLAN, G-EVIDENCE, G-STATUS, G-INDEX, G-HANDOVER, G-NEGATIVE. They specify *what success would show*, not *how Agent A built it*.
8. **Designed a bounded output contract:** 12 sections, source inventory and claim grades, independent architecture map, ordered continuation plan, complete **unpublished** implementation issue, ROI register, EXACTLY THREE live-source Stage 2 questions, absent-source requests, contamination disclosure and freeze receipt.
9. **Maintained research/publication separation:** The golden Stage 1 says no source, issue, PR, plan, roadmap or execution mutation. A later, separately authorized exception allowed publication of `RUNNER_RECONSTRUCTION_V1.md` as research only, without modifying its frozen prompt or granting Stage 2 execution.
10. **Audited the outcome without overstating independence:** The runner published a 361-line, 43,450-byte reconstruction. Twelve baseline blob prefixes and its SHA-256/readback were checked. The runner explicitly declared `STAGE1_INDEPENDENCE=CONTAMINATED — AMBIENT_CONTEXT_RISK`, since earlier V3.5 context existed. It is a useful qualified rehearsal, **not** a clean-blind controlled experiment.

**Crucial insight:** Stage 1 should independently determine **what ought to be built and verified**. Giving the runner current implementation strategy or PR completion details would convert it into a handover paraphraser and corrupt the intended comparison.

## 3. HOW Stage 2 was developed — actual derivation sequence

Stage 2 was **not** constructed by writing a generic "continue the task" prompt. It was derived as the complement of the *actual frozen Stage 1 output* and the Owner's required reconciliation/takeover sequence.

1. **Pinned the Stage 1 output first.** The prompt names the committed `RUNNER_RECONSTRUCTION_V1.md`, exact commit and content digest. Runner B must check the freeze before learning Agent A's implementation. No retrospective plan editing.
2. **Read what Runner B really proposed:** its C0–C9 ordered obligations, seven G-oracles, unpublished continuation issue, High/Medium/Low ROI register and **the three actual Q1–Q3 questions**. Stage 2 explicitly uses them rather than easier successor-created questions.
3. **Defined the missing input:** `AGENT_A_STAGE2_REALITY_PACKET_V1`, requesting original assignment/task-start SHA, live branch/HEAD, plan revisions, actual WHAT/WHY/**HOW**, changed modules/consumers, tests/fixtures/evidence, known issues/parked work, in-flight GitHub operations, reviewer/lease state and next plan. Predecessor assertions remain unverified until current source/provider inspection.
4. **Made reconciliation genuinely independent:** four columns must remain distinguishable—Owner authority, Runner B frozen belief, Agent A plan/claim, real provider/source evidence. Every difference needs ACCEPT/REVISE/REJECT/UNKNOWN/OWNER_DECISION_REQUIRED, with a falsifier and concrete next action. Runner B must record its *own* wrong beliefs, not only predecessor flaws.
5. **Required a complete user-visible chain, not just local tests:** native Owner→parent→graph→child issues/comments→candidate and qualified task evidence→ONE DELP status→issue/PR readback→safe repo index→current handover/cold successor. Missing physical producer-to-consumer links cannot receive inferred PASS.
6. **Added exact-material and time boundaries:** differentiate Agent A's *true* starting SHA from the frozen protocol baseline, current `main`, graph/spec generation, candidate PR SHA, changed golden/consumer dependencies, evidence-covered SHA, test/run/reviewer material and observed-at timestamp.
7. **Specified ROI and roadmap decisions:** HIGH verified = ABSORBED, HIGH missing in scope = proposed INTEGRATE, scope-changing HIGH = OWNER_DECISION_REQUIRED, MEDIUM = PARK with reason/revisit trigger, LOW = DECLINE. A new agent session never manufactures a new parent, leaf or denominator. Prefer a governed `PLAN_UPDATE` to an already authorized issue/graph after inspection.
8. **Designed failure when there is no final Agent A handover:** a crashed/expired agent cannot be forced to summarize. The runner must reconstruct via durable source/provider evidence and expose UNKNOWN dirty worktree/pending writes; no invented final packet.
9. **Separated reconciliation admission from execution admission:** Stage 2 may be *read-only* and produce a complete revised plan even if the old executor cannot be fenced. No actual code/GitHub mutation until exclusive source/lease/scope permission is shown. GitHub comments are insufficient to atomically revoke another running agent.
10. **Made success falsifiable:** the runner passes by finding and resolving disagreement, detecting stale HEAD/evidence, rejecting unauthorized work and identifying a legitimate next unit or HOLD. It does not pass just because the two agent plans agree.

**Crucial insight:** Stage 2 should reconcile **SHOULD EXIST vs DOES EXIST**, not simply convert Agent A's final handover into a new implementation plan.

## 4. WHAT robust prompts require — minimum contracts

| Requirement | Why it matters | Required guard |
|---|---|---|
| Real Owner words and provenance | Avoid agent-invented intent becoming Owner policy | Direct/mirror/paraphrase/UNKNOWN grades and amendment order |
| Exact source/time anchor | Avoid learning current Agent A code in Stage 1 or using stale Stage 2 facts | Immutable baseline Stage 1; live exact readbacks Stage 2; separate task-start SHA |
| Purpose and acceptance, not method | Protect independent problem reconstruction | Stage 1 WHAT/WHY only; algorithm, plan, diff, PR stats withheld |
| Actual information boundary | Prompt-only "do not look" is not technical isolation | Stage 1 allowlisted offline checkout / immutable source, restricted tool access; flag contamination if exposure possible |
| Frozen independent answer | Stop ex post rationalization when solution is revealed | Recorded SHA-256 + Git blob + readback, immutable original, new Stage 2 document |
| Predecessor reality as claims | Agents can report success without source proof | Separate AGENT_CLAIM / SOURCE_OBSERVED / TEST_RUN / REVIEWED and UNKNOWN |
| Four-way reconciliation | Detect both agents' missed requirements, not just copy implementation | Owner vs frozen Runner vs Agent A vs current material, with tests/falsifiers |
| Native lifecycle contract | A successful component test is not whole-system integration | Actual GitHub parent/child/PR/readback + one DELP snapshot + index + handover |
| Real fixtures and negative oracles | Prevent pleasing prose with no reproducible engineering proof | Source/golden hash, changed consumer, stale HEAD, forged evidence, failed CI cases |
| Governance and one writer | Prevent runner from taking over while Agent A can still write | Explicit read-vs-write admission, actor/lease epoch, fencing/revocation and provider readback |
| ROI and roadmap discipline | Prevent patchwork, shadow scopes and gratuitous tickets | Absorbed HIGH, parked MEDIUM, declined LOW, approved graph changes only |
| Emergency continuation | No guarantee an exhausted agent can write a handover | Durable observation, interrupted transaction reconciliation, UNKNOWN local-only state |
| Token budget honesty | "70% life" is not directly known on all platforms | Consume/remaining convention explicit; measured/estimated/UNKNOWN, no false telemetry |
| Reviewer/Owner/privacy boundaries | Green tests or mirror text do not confer consent | Separate authorization for sensitive index/writer/merges; independent principal required |
| Clear deliverables and stops | Agents otherwise just acknowledge or narrate | Named artifact, required sections, exact three questions, explicit HOLD rules |
| Reproducible evaluation | One plausible plan cannot establish runner advantage | Independent frozen run vs handover/checkpoints/cold successor on same acceptance oracle |

## 5. Grounding: observed source, memory and architectural inference

**Primary case inputs:**
- [V3.5 programme #787](https://github.com/reallaksh19/Common/issues/787) — Owner mirror and original lifecycle problem; **not** authenticated original chat.
- [Canonical V3.5 #864](https://github.com/reallaksh19/Common/issues/864) — normative design/roadmap and required one-authority chain.
- [Recovery #878](https://github.com/reallaksh19/Common/issues/878) — the Owner correction and pending live end-to-end acceptance; later progress text was deliberately *not* Stage 1 input.
- `Common@13989969` `SKILL.md`, DELP operating model, graph/facts/live-status schemas, projector, owner commands, continuity, decomposition and handover code.
- Frozen [Runner Stage 1 output at 38ffb797](https://github.com/reallaksh19/Common/blob/38ffb797a0993320ce198ddcd414e14856966251/relay/runner-v35-stage1-chatgpt-20261009/RUNNER_RECONSTRUCTION_V1.md).

**Prior conversation/memory contribution:** I already knew the Owner's broader complaint about agents reading titles rather than true intent, unwanted self-directed "overcautious" or patchwork work, and the desired V3.5 causal chain. I used that to *choose research questions and source locations*, not to grant source-verified status. Some prior session summaries contained agent-reported progress; they were **not** treated as Stage 1 independent implementation evidence. This is why a clean-blind independence claim cannot be made for this first rehearsal.

**Architectural inference (not verified implementation):** the 70%-consumed trigger, Stage 1/2 information firewall, two-phase admission, four-view reconciliation, emergency succession and ROI disposition are designed contracts needing experimental validation. They are not facts that V3.5 already runs such a runner. The current pilot has **not** established a real health signal, production dual-writer fence, successful takeover or comparative performance.

## 6. Structural and golden acceptance checks for these prompts

### Stage 1 input checks

- Original source prompt and `fixtures/STAGE1_RUNNER_PROMPT.md` must have identical Git blob SHA/content. Any difference is fixture failure.
- Fixture declares ~70% **consumed**, with grade `ESTIMATED_UNVERIFIED`; no made-up health telemetry.
- It supplies the historical source baseline and cites Owner wording while marking original-chat provenance UNKNOWN.
- It explicitly excludes Agent A implementation HOW/current PR/branch/CI/final plan; even indirect exposure forces contaminated declaration.
- It requires 12 sections, an unpublished continuation issue, ROI and exactly three Stage 2 questions.
- It demands positive/negative oracles and denies current coding/write authority.

### Stage 2 input checks

- Stage 1 frozen SHA is verified and never rewritten.
- Agent A reality packet and any actual handover are treated as unverified until live GET/source/CI review; missing packet follows emergency branch.
- Runner answers the original Q1/Q2/Q3 instead of generating replacement questions.
- A four-lens matrix records ACCEPT/REVISE/REJECT/UNKNOWN/OWNER_DECISION_REQUIRED with falsifiers.
- Native GitHub live issue/PR status, candidate SHA, exact task evidence, repo-wise index and successor must be evaluated as distinct physically connected edges.
- ROI preserves validated HIGH work, parks MEDIUM with revisit triggers and avoids new leaf/weights without graph permission.
- Without verified one-writer admission, output is a frozen read-only reconciliation and HOLD; no task edits or coding.

### Adversarial golden scenarios (NOT results of executed tests)

| Attack/failure | Expected response |
|---|---|
| Stage 1 learns Agent A's algorithm or current PR indirectly | Mark contaminated; do not claim clean independent discovery |
| Agent A says "done" with no accepted current material | UNVERIFIED; demand exact source/test/provider receipt |
| Stage 1 plan conflicts with verified better source design | Correct Runner B's plan; ACCEPT Agent A evidence rather than defend a bias |
| Agent A recommends implementing downstream child under another responsibility | REJECT or OWNER_DECISION_REQUIRED; don't steal task |
| Candidate moves after task evidence | Stale proof and DELP-currentness reconciliation; no hand-authored status |
| Golden input/dependency changes but candidate HEAD does not | Flag dependency/currentness gap; independently requalify |
| Agent A crashes before final handover | Native evidence reconstruction, UNKNOWN local state, reconcile in-flight effects |
| Old Agent A can still write after successor admission request | HOLD_DUAL_WRITER_RISK, never assert exclusive automatic transfer |
| Stage 2 proposal creates second parent or new weights because new agent starts | Preserve existing responsibility; controlled roadmap decision |
| Repo Owner-intent file contains private transcript | Block publication pending explicit privacy/custody decision |
| Passing component tests but absent physical status→index→handover path | End-to-end NOT_QUALIFIED, regardless of local green |
| A reviewer is the same actor or only inferred from a test name | Not independently reviewed |

## 7. How to run and evaluate without breaking the experiment

1. Start a fresh, isolated Runner B session; supply only Stage 1 fixture plus approved immutable baseline and curated Owner sources. Enforce a real allowlist where tools support it. **This historical Stage 1 runner is contaminated by ambient context; do not erase the flag.**
2. Allow research-artifact publication only if separately scoped. Freeze `RUNNER_RECONSTRUCTION_V1.md`; collect exact raw bytes, receipt, commit and readback.
3. Inspect/evaluate Stage 1 *before* releasing Agent A HOW or current PR; keep a sealed evaluator separate from runner input. Assessment covers actual intent reconstruction, source accuracy, plan quality, negatives, ROI and three strong questions.
4. Explicitly admit Stage 2 read access; supply Agent A's honest current-state packet if possible and allow current provider/source reads. Run Stage 2 prompt. Verify its reconciliation *against independently observed material*.
5. Keep Stage 2 publication and execution blocked until real Owner/Local/custody scope and single-writer fencing are proven. A good plan alone is not authority.
6. Compare against a terminal handover, periodic event/checkpoint memory and cold GitHub reconstruction under the same cases. Vary rehearsal trigger at 50/70/85% consumed if telemetry is available; measure total token cost, next-unit accuracy, duplicated work, Owner corrections, source-current tests, wrong claims and unauthorized writes.
7. Preserve prompt versions, candidate material and evaluator reports. A different prompt version or new baseline defines a new experiment; never silently revise the golden fixture.

**Final design principle:** A runner is prepared *independently* to understand the Owner's real objective; only later does it learn the predecessor's HOW. Its value is measured by the quality of source-grounded reconciliation and the correctness of authorized continuation—not by how smoothly it can retell Agent A's story.
