# V3.5-R14 — STAGE 1 RUNNER PROMPT (FROZEN GOLDEN INPUT)

**Fixture ID:** `V35-R14-RUNNER-S1-20261009-A`  
**Fixture class:** source-grounded rehearsal of a real V3.5 continuity problem, **not** evidence that Agent A or Runner B actually ran this scenario.  
**Role:** `RUNNER_PREPARING` · **Authority:** `READ_ONLY_RECONSTRUCTION`  
**Primary:** Agent A (continues engineering; retains the task/execution lease)  
**Next role if later admitted:** Agent B (outside this Stage 1 prompt)  
**Stage:** 1 of 2 — INDEPENDENT RECONSTRUCTION, **not** a two-pass prompt generator.

## 0. Why you have been engaged

Agent A has requested **“Time for runner”** during work on the V3.5 Engineering Relay lifecycle. The scenario places the request at **about 70% of estimated agent life *consumed***, leaving roughly 30% estimated runway. **These are rehearsal assumptions, not measured token telemetry.** The only honest measurement grade for this fixture is `ESTIMATED_UNVERIFIED`; a live implementation must record `UNKNOWN` if no effective-context or runway telemetry is available. The established V3.5 seven-component engineering delivery-health score is **not** a measurement of remaining context tokens.

You are the intended successor, but you are **not** the successor executor yet. Agent A remains in command, continues work and may reach the next checkpoint while you independently understand the problem. Your current duty is to reconstruct **what ought to exist, what matters, and what should happen next** from the permitted evidence. It is not to reconstruct, imitate, or complete Agent A's implementation.

This intake is a deliberately restricted WHAT/WHY view. You will see no current implementation PR, branch/diff, PR status, CI pass/fail statistics, current implementation plan, or final predecessor handover. You cannot infer them. The withheld material is deliberately revealed only in Stage 2.

## 1. Repository and source envelope — stage-1 readable only

- **Programme repository:** `reallaksh19/Common`.
- **Programme:** Engineering PR Delivery V3.5-R14, canonical lifecycle / RELAY integration.
- **Frozen protocol reference baseline:** `Common@13989969f6b7e432c4f7c1ddfe975449dba53593` (an observed source-reference commit, **not proven to be Agent A's first work commit**).
- **Agent A's original task-start commit:** `UNKNOWN` — request source confirmation in Stage 2. Do **not** substitute the protocol baseline for an Agent A starting commit.
- **Governing Owner-intent GitHub mirror:** `Common#787`, **Owner instruction section 0 only**. This issue is a mirror; an independently authenticated original private-chat message URI is `UNKNOWN`.
- **Governed lifecycle problem/roadmap:** curated Owner and requirement excerpts from `Common#864`, specifically the **desired outcome and WP0–WP10 phase names only**, excluding historical/current implementation commentary and PR status.
- **Later Owner correction:** verbatim text mirrored in `Common#878`; treat the utterance as the Owner's statement in the conversation and the GitHub copy as a **mirror**, not as an authenticated original-chat source.
- **Evaluation environment:** `reallaksh19/relay-v35-e2e-lab` is a private disposable research laboratory; its original inventory-CSV requirements can serve as a bounded regression exercise later. It is **not** evidence of a functioning V3.5 lifecycle.
- **Source access restriction:** ONLY the curated packet below and a read-only *immutable snapshot* at the frozen source baseline. No live issue/PR API, default-branch floating ref, current branch enumeration, commit-log tail, Actions dashboard, unpublished transcript, predecessor plan or private agent reasoning. If this restriction is not technically enforceable, mark the Stage 1 independence test `CONTAMINATED` rather than silently proceeding.

### Owner's original instructions (verbatim as first GitHub mirror)

> “do you see interlink from parent issue> task decomposition........->task evidence>live scoreboards in issues>smart PR title>->this research->handover?”

> “lets us discard all old issues. lets start afresh”

The associated Owner problem (an explicitly labelled **GitHub paraphrase**, not verbatim original-chat text) is that a newly assigned ChatGPT/Codex/Claude coding agent must **not** begin from an issue or PR title alone. It needs the actual Owner purpose, evolving roadmap, previous sessions, agent deviations, actual code changes, and verifiable source evidence.

### Later Owner correction (verbatim)

> this does not show that v3.5 work from parent issue creation-> decomposition of task->child issues/comment blocks->dynamic PR title, scoreboard git issues->task evidence, update of repowise index/ownerintent file->handover.

Treat the corrections as an **outcome requirement**, not proof of its implementation or authorization to write GitHub objects. The exact first-chat message locator is not included.

## 2. Owner-required end state — WHAT and WHY only

**WHAT:** A genuine, connected engineering lifecycle from initial Owner requirement and GitHub parent issue through source-aware planning and responsibility decomposition; actual child issues and machine-readable comment blocks; bounded candidate work and task evidence; status and smart PR titles derived from the governed programme authority; an independently reconstructable, repo-wise Owner-intent/session/changed-module decision index; and successor handover that can withstand a changed repository.

**WHY:** Successive agents previously needed too much inference from titles, summaries and predecessor claims. Individually passing components or manually written status prose do not prove the physical end-to-end workflow. The Owner wants a successor to distinguish the Owner's original request from agent interpretations, what was claimed from what the repository demonstrates, and legitimate remaining work from drift or unapproved expansion.

**Acceptance principles to preserve:**

1. Original Owner instructions and their provenance are not interchangeable with agent summaries or mutable issue titles.
2. One governing programme progress/evidence authority; runner, continuity view and handover must not invent competing percentage, status or next-task computations.
3. Source and material currentness matter: source changes can invalidate earlier evidence; historical records remain historical.
4. Responsibility/claim/plan revisions and issue parentage must remain stable and source traceable across executor replacement.
5. Reviewer independence, Owner consent, privacy and GitHub mutation/merge authority are separate from engineering test success.
6. A successful result must be independently observable in real GitHub state, not inferred solely from a generated document or a synthetic test.

## 3. Agent A's Stage 1 WHAT/WHY situation report (claims, not evidence)

The following is a **rehearsal briefing constructed from the case-study issue history**. It is **not** a transcript of Agent A's actual words. Every purported completed action is `CLAIM_ONLY` until Stage 2 source verification.

| Problem addressed or examined (WHAT) | WHY it mattered | Verification grade available to you |
|---|---|---|
| Capturing the original Owner purpose and later amendments | Successor must not substitute an agent's paraphrase for the Owner's direction | `INTENT_REQUIREMENT`, implementation unknown |
| Establishing parent→plan→bounded child responsibilities | Issue titles alone do not explain task ancestry or authorized boundaries | `PROBLEM_ANALYSED`, implementation unknown |
| Relating task evidence to reported delivery progress | Agent claims and code/test reality can diverge | `PROBLEM_ANALYSED`, implementation unknown |
| Connecting live parent/child status and smart PR naming to task authority | A manually convincing title is not a derived, current status | `PROBLEM_ANALYSED`, implementation unknown |
| Preserving per-repository session, changed modules, owner amendments and decisions | New agents should reconstruct a project without original chat | `PROBLEM_ANALYSED`, implementation unknown |
| Making handover withstand source drift | An old summary may become stale before successor executes | `PROBLEM_ANALYSED`, implementation unknown |
| Defining real-GitHub full-chain acceptance | Component/fixture success can conceal a disconnected system | `PROBLEM_ANALYSED`, implementation unknown |

**Deliberately NOT supplied:** which code paths Agent A changed, what solution it selected, its current working plan, which tests passed, current PR metadata, worktree state, unresolved GitHub transaction IDs or code/diff details. If you need any of those to claim completion, defer to Stage 2.

## 4. Pending obligations at this Stage 1 boundary

These are **open questions / obligations**, not a claim about their present technical status:

- Reconstruct the true source-grounded parent→children→facts→status→index→handover graph, including places where a connection needs proof.
- Identify which Owner requirements require a native GitHub readback and which could be satisfied only by a local fixture (insufficient by itself).
- Establish an independently reasoned order of investigation, bounded implementation and validation against the permitted roadmap.
- Identify governing authority and review/decomposition gates before any phase may create code or GitHub objects.
- Specify how source/input/golden fixtures and exact task materials must bind to evidence and currentness.
- Specify an independently testable, three-question Stage 2 source-reconstruction challenge.
- Produce a continuation-plan proposal that can be reconciled with Agent A's implementation *later*, without treating Agent A's assertions as accepted facts.

## 5. Known issues and risks — WHAT, not implementation diagnosis

- **Original-message provenance:** GitHub contains mirrored Owner wording, but an independently verified permalink to the original private chat is unavailable in this Stage 1 packet.
- **Integration risk:** different parts of the lifecycle may work independently but not as one operating chain; require physical call and provider traces to establish connection.
- **Evidence ambiguity:** a task may appear complete in narrative while its exact material, provider status or reviewer acceptance is unverified.
- **Successor contamination:** a runner exposed to Agent A's implementation too early may merely imitate it.
- **Authority ambiguity:** a runner's reconstruction is not Owner approval, task-scoped write permission or independent review.
- **Dual-executor risk:** Stage 2 must prevent Agent A and Agent B from holding simultaneous mutation authority.
- **Index/custody risk:** repository records may contain private input or conflate Owner statements with an agent's interpretation.
- **Health estimate risk:** the 70%-consumed trigger is a policy hypothesis, not a verified context-window metric.

## 6. Parked work — do not silently absorb

- Production GitHub status writers and automatic merging without a separate Owner/security/reviewer decision.
- Any new repository-wide retention/private transcript policy without explicit source/Owner authorization.
- Changes to unrelated application repositories, even if useful for demonstrating the model.
- Cosmetic enhancements, extra dashboards or generalized multi-repository rollout ahead of full-chain evidence.
- Medium-ROI robustness ideas: broader randomized/adversarial fixtures, improved diagnostics, additional repo variants. Record with rationale and revisit trigger; do not mint new task weights or implementation scope.

## 7. Source inputs and golden acceptance references

**Permitted source inputs (at frozen / curated revisions):**

- `Common#787` Owner-verbatim section 0, reproduced above. Its later manual progress claims are **not** permitted as Stage 1 inputs.
- `Common#864` desired lifecycle outcome and *phase categories*, not its current progress and source-implementation commentary. Broad work categories: source/authority census; identity/schema; sole programme progress authority; material and evidence validation; session/Owner provenance; common snapshot; status/handover; independent successor; gated publisher; whole-system acceptance.
- `Common#878` Owner correction reproduced above, not its subsequent recovery scoreboard/comment history.
- Immutable source tree at `Common@13989969f6b7e432c4f7c1ddfe975449dba53593` strictly for **baseline architecture discovery**. Source facts at this commit are not equivalent to Agent A's current implementation, and may be newer than Agent A's true start; record this limitation.
- If a bounded lab parser scenario is used as a research fixture, the **separate** lab baseline is `relay-v35-e2e-lab@3392dc2147988492c54af2f1baa53aacd22fdcbe`, with `docs/owner-intent.md`, `fixtures/valid.csv`, and `tests/test_inventory_parser.py`. This is optional experimental input, **not** evidence for full V3.5 completion.

**Golden outcome oracles (what a true future implementation would need to demonstrate):**

- **G-INTENT:** successor preserves Owner's WHAT/WHY and amendments, separates source grades.
- **G-PLAN:** parent/child decomposition has governed claims, issue relationships and bounded acceptance; no unsolicited duplicate responsibility.
- **G-EVIDENCE:** task evidence describes source-observed candidate and test facts, not hand-authored progress/acceptance.
- **G-STATUS:** parent, child and feature-PR status/title refer to the **same governed source/progress snapshot**, including invalidation after drift.
- **G-INDEX:** repo-wise records distinguish Owner source, agent claims, actual module/commit changes and open decisions.
- **G-HANDOVER:** successor reads current source, identifies exact next admitted unit or explicitly says UNKNOWN/HOLD.
- **G-NEGATIVE:** fake evidence, stale state, unapproved scope change and missing sources cannot count as PASS.

The golden oracles are **acceptance criteria**, not an implementation recipe or a claim that a test has run.

## 8. Stage 1 — your required work

You are the Runner B. Independently:

1. Explain the Owner's objective in your own words, citing only the provided exact Owner quotations and immutable source inputs. Clearly separate facts, predecessor *claims*, your hypotheses and UNKNOWNs.
2. Reconstruct the **problem architecture**, major user-visible transitions and responsibility boundaries from the baseline, not Agent A's solution. Identify the minimum paths you must inspect during Stage 2.
3. Produce your **own** ordered continuation plan, including bounded phase goals, dependencies, positive and negative acceptance oracles. Do not assume any part was completed merely because Agent A says it was addressed.
4. Identify the earliest next *legitimate* action under the currently known governance. If authority is unproven, propose source inspection, review or Owner decision, not unapproved coding.
5. Write the complete Markdown **proposed GitHub continuation issue body**, or a detailed proposed `IMPLEMENTATION_PLAN` / `PLAN_UPDATE`, as an **unpublished** artifact; clearly show its root/leaf linkage and distinguish plan revisions from a new engineering responsibility. Publication is a Stage 2 governed operation.
6. Classify candidate improvements by HIGH/MEDIUM/LOW ROI. HIGH within approved scope is a candidate for later reconciliation, not automatic scope change; MEDIUM goes to a parked register with a revisit trigger; LOW may be declined with reason.
7. Form exactly **three independently answerable Stage 2 repository-grounded questions**. They must test current code/graph provenance, evidence/status agreement and next task authorization without guessing Agent A's implementation.
8. Freeze your independent plan and digest it **before** requesting Stage 2 data. Mark any uncertainty you cannot honestly resolve from the restricted Stage 1 view.

### Required output: `RUNNER_RECONSTRUCTION_V1`

Return a standalone document using this structure:

1. `FIXTURE_ID`, `STAGE`, `RUNNER_ROLE`, `SOURCE_BASELINE`, `OWNER_SOURCE_GRADE`, `INFORMATION_BOUNDARY`, `HEALTH_TRIGGER_GRADE`.
2. **Owner-intent reconstruction:** verbatim evidence, derived WHAT/WHY, acceptance boundaries.
3. **Source/baseline inventory:** what you read and its immutable reference; what you were not allowed to read.
4. **Agent A claims ledger:** each WHAT/WHY claim → `UNVERIFIED`, the Stage 2 observation needed to verify it.
5. **Independent architecture/problem map:** essential lifecycle transitions and their verification needs.
6. **Prioritized independent plan:** bounded next obligations, dependencies, tests, negative cases and permitted responsibility scope.
7. **Proposed continuation GitHub issue or IMPLEMENTATION_PLAN:** complete copy-ready Markdown, `DRAFT_NOT_PUBLISHED`, with source/Owner authority placeholders still labelled UNKNOWN.
8. **ROI register:** `HIGH / MEDIUM / LOW` with provenance, expected value, scope classification and revisit trigger.
9. **Three Stage 2 reconstruction questions:** exactly three, source-answerable and falsifiable.
10. **Stage 2 information requests:** current source/branch/diff, Agent A's plan and handover (if available), issue/PR/evidence/CI, current actor/lease/reviewer authority and repo session/index state.
11. **Contamination statement:** declare if any withheld material was viewed, including indirectly. If yes, set `STAGE1_INDEPENDENCE=CONTAMINATED`.
12. **Freeze receipt:** local immutable hash of your Stage 1 response, source/observed-at notes; do **not** claim identity authentication from this hash.

## 9. Hard constraints

- Do **not** read, infer from, or request current PR numbers/status, current implementation branch, Agent A code diff, original ongoing implementation strategy, final predecessor plan/handover or current CI totals until Stage 2.
- Do **not** use issue titles as proof of progress, calculate programme P/E, author a smart PR title, accept agent assertions as evidence or invent Owner/reviewer approvals.
- Do **not** create/update GitHub issues or PRs, push branches, write code, edit the roadmap, run current-head verification or acquire the task's execution lease.
- Do **not** assume the 70%-consumed signal is telemetry-confirmed; do **not** assume Agent A can finish a final handover.
- Do **not** reveal implementation methods through the golden oracle: only problem/acceptance information is in this packet. If prohibited material appears through a tool/search result, stop and report a boundary violation.
- Do **not** proceed to Stage 2 independently. You finish Stage 1 with a frozen, reviewable reconstruction and a draft continuation plan; promotion happens only after actual source re-verification and governed exclusive transfer.

**Stage 1 success means that you independently understand the Owner's problem, can identify appropriate verification and next obligations, and have a source-qualified draft plan. It does not mean Agent A's work is verified or that you have taken over.**
