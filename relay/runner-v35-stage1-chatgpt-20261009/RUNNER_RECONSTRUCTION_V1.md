# RUNNER_RECONSTRUCTION_V1

**Fixture ID:** `V35-R14-RUNNER-S1-20261009-A`  
**STAGE:** `1 / INDEPENDENT_RECONSTRUCTION` — no successor admission  
**RUNNER_ROLE:** `RUNNER_PREPARING` (prospective Agent B); Agent A retains the execution lease  
**SOURCE_BASELINE:** `reallaksh19/Common@13989969f6b7e432c4f7c1ddfe975449dba53593` — an observed protocol reference, **not** Agent A's proven original task-start commit  
**OWNER_SOURCE_GRADE:** `MIRRORED_VERBATIM` for the quoted Owner utterances in the frozen packet; original private-chat permalink `UNKNOWN`; the associated problem paraphrase is `AGENT_PARAPHRASE`  
**INFORMATION_BOUNDARY:** frozen prompt + its reproduced/curated Owner and roadmap passages + immutable baseline files only; no active implementation branch, diff, PR statistics, Agent A plan, handover, current Actions, issue-history tail or live provider inspection  
**HEALTH_TRIGGER_GRADE:** `ESTIMATED_UNVERIFIED` (fixture assumes approximately 70% of agent life **consumed**, not a measured 70% remaining); operational token runway is `UNKNOWN` absent actual telemetry  
**RECONSTRUCTION_GRADE:** source-grounded baseline / independent proposed path, **not** proof of current implementation  
**PUBLICATION_CLASS:** `STAGE1_RESEARCH_ARTIFACT_ONLY`; publishing this document does not create a responsibility, modify the programme plan or transfer the lease  
**Observed at:** 2026-10-09, Asia/Muscat. Exact source line of enquiry: immutable baseline.  
**STAGE1_INDEPENDENCE:** `CONTAMINATED — AMBIENT_CONTEXT_RISK` (see §11): the surrounding conversational context contains prior V3.5 project summaries outside the sealed Stage 1 packet. They were not used as evidence or queried, but the runner cannot honestly certify a sealed blind examination.

---

## 1. Owner-intent reconstruction

### 1.1 Evidence separated by provenance

**Owner utterance, verbatim as mirrored in the frozen prompt from Common#787 §0:**

> “do you see interlink from parent issue> task decomposition........->task evidence>live scoreboards in issues>smart PR title>->this research->handover?”

> “lets us discard all old issues. lets start afresh”

**Later Owner correction, verbatim as mirrored in the frozen prompt from Common#878:**

> this does not show that v3.5 work from parent issue creation-> decomposition of task->child issues/comment blocks->dynamic PR title, scoreboard git issues->task evidence, update of repowise index/ownerintent file->handover.

These are **Owner-sourced words in a GitHub mirror**, not authenticated original-chat messages. The frozen prompt labels the related statement about fresh agents needing full purpose, roadmap, prior sessions, deviations, changes and source evidence as a **paraphrase**. It must not be elevated to a verbatim instruction.

**Derived WHAT:** one functioning, inspectable execution chain, beginning at a real Owner request and parent issue, through an approved versioned execution graph and bounded leaves/comment blocks, source-bound leaf evidence, one authoritative derived status and smart PR/issue representation, a repo-wise Owner/session/change/decision index, then a handover that a different executor can challenge against a moved repository.

**Derived WHY:** a successor must not infer duties from a title, trust an agent's completion narrative, or confuse a locally generated dashboard with provider-observed engineering truth. The Owner's correction specifically rejects a demonstration that skips the **physical links** between phases.

**Acceptance boundaries:** (a) fidelity to Owner wording and amendments, (b) one graph/progress authority rather than competing calculators, (c) actual GitHub parent-child and leaf/PR objects plus readback, (d) tests and evidence qualified on exact materials and current source, (e) index entries differentiating Owner facts, agent claims, git changes and unresolved decisions, (f) challengeable successor handover, and (g) explicit Owner/security/independent-review control for sensitive writes and merge.

### 1.2 Facts, interpretations and unknowns

| Classification | Assertion |
|---|---|
| `OWNER_MIRROR_VERBATIM` | The three quotations above are the only reproduced exact Owner wording authorized in the Stage 1 packet. |
| `BASELINE_SOURCE_VERIFIED` | A normative DELP projection contract, graph/facts/status schemas, Python projector/CLI and related tests **exist at the frozen commit**. This says nothing about Agent A's current implementation. |
| `TEST_DEFINITION_ONLY` | Source tests cover projector, drift, decomposition, handover and provider-store behaviors. Their existence is not a passing run or real-GitHub full-chain proof. |
| `HYPOTHESIS` | The main product gap is likely *integration and governance of the chain*, not a missing percentage formula alone. Stage 2 must falsify or confirm this. |
| `UNKNOWN` | Agent A's start commit, active branch/diff/PR, live issue and reviewer state, true source of original private chat, current acceptance run, custody lease, and repo-wise index status. |

### 1.3 Non-negotiable actor split

Programme Owner/delegated Coordinator governs intent, scope, graph, weight, decomposition and explicit plan revisions. The one current leaf executor publishes its own task/evidence claims only. A reviewer independently qualifies claims and source; Local v1.1 controls broader reviewer/super-reviewer and merge lifecycle. The DELP projector owns **no** permission: it derives titles and statuses. A runner at Stage 1 has no implementation or publication authority beyond this specifically authorized research artifact.

---

## 2. Immutable source/baseline inventory

All paths below are under `reallaksh19/Common@13989969f6b7e432c4f7c1ddfe975449dba53593`. A listed blob is evidence of the *file version read*, not of runtime success.

| Baseline path under `skills/engineering-pr-delivery-v3.5/` | Git blob SHA (prefix) | Relevant inspected contract |
|---|---|---|
| `SKILL.md` | `202a2858d841` | Active V3.5 selector, nested Local boundary, DELP, publication family and health |
| `operating-model/durable-execution-lineage-projection-v35.md` | `b032bfde3f84` | Normative graph→facts→observation→status authority; explicitly documents limitations |
| `schemas/delp-execution-graph-v35.schema.yaml` | `ef7fcab2a071` | Typed ROOT/INTERMEDIATE/LEAF, stable identities, acceptance claims, topology and plan gates |
| `schemas/delp-checkpoint-facts-v35.schema.yaml` | `6327f711aefb` | Only leaf facts, candidate/contract binding, optional execution and handover/entry metadata |
| `schemas/delp-live-status-v35.schema.yaml` | `add6ddcd8921` | Derived `LIVE_STATUS_V1` output shape |
| `scripts/delp_projection_v35.py` | `a6eb1219e736` | `validate-graph`, `validate-facts`, `bind-facts`, `project`, `admit`, `frontier`, `frontier-verify`, `decompose-check`, `graph-diff`, `sync-github`; provider/store paths |
| `scripts/owner_commands.py` | `293834e1e448` | Direct-Owner envelope, recovery/continuation/handover command classification; supplied refs are not fabricated |
| `scripts/continuity_projection.py` | `39fe2747acf0` | DERIVED_FROM_FACTS compatibility and legacy handling |
| `scripts/embedded_coder_v35.py` | `5b2d4b1bf465` | Local PRD vs namespaced Coder identity and explicit denial of Local completion/merge authority |
| `scripts/decomposition_classifier_v35.py` | `f0f21a29016c` | Pure `PASS/SPLIT/MERGE/DISCOVER_FIRST/REPLAN` classification |
| `scripts/decomposition_assembler_v35.py` | `bc155cef4c87` | Typed claim/topology admission assembly |
| `scripts/decomposition_observer_v35.py` | `84d790e31cf` | Read-only repository-based topology observation/currentness |
| `templates/checkpoint-facts-v35.md` | `4cdabceea40b` | Leaf checkpoint publication format and START/materialization rules |
| `templates/delp-cron-workflow-v35.yml` | `52141eafd8e6` | **Inert** example runner: not an active GitHub workflow |
| `PROGRAMME_DECOMPOSITION_PROGRESS.md` | `44aaed1c5067` | Planning/denominator/size and stable-cut research; portions explicitly future/candidate, superseded title grammar |
| `OWNER_CHECKPOINT_PROJECTION.md` | `f12b3ad6d717` | Three-view Owner title/chat/durable evidence separation |
| `CHECKPOINT_AND_LIVENESS_CONTRACT.md` | `b87696442751` | Interruption/checkpoint and observer liveness design |
| `tests/test_delp_projection_v35.py` | `529c120b5662` | Extensive definitions for projector, negative cases, graph evolution, live sync fakes, successor/reconstruction cases |
| `tests/test_owner_commands_continuation.py` | `14404861959f` | Continuation, direct Owner command, entry requirements |
| `tests/test_continuity_derived_projection.py` | `9ad15e185f71` | Derived vs legacy snapshot assertions |
| `tests/test_embedded_coder_v35.py` | `7b1f330c96fd` | Nested Local custody and result authority assertions |

**Source-input provenance:** the frozen prompt supplies curated `Common#787` §0 and `Common#878` Owner text, plus `Common#864` desired outcome and broad WP0–WP10 phase *categories*. Their live issue bodies and comments were **not opened**; no mapping of individual current WP numbers to live status is asserted. The optional disposable `relay-v35-e2e-lab@3392dc2147988492c54af2f1baa53aacd22fdcbe` was **not inspected** or run; its inventory CSV can be a bounded regression, not V3.5 acceptance.

**Excluded deliberately:** current default-branch source, branch listings, live PR/CI, Agent A implementation notes, mutable issues beyond quoted curated passages, unpublished handover, private chat, current-head tests. No GitHub issue/PR/status was written during research.

---

## 3. Agent A WHAT/WHY claims ledger — all unverified

The frozen prompt explicitly labels Agent A's Stage 1 briefing a **constructed rehearsal**, not an authenticated statement by Agent A. No row is upgraded to “implemented.”

| Briefed WHAT/WHY | Stage 1 grade | Necessary Stage 2 observation |
|---|---|---|
| Capture original Owner purpose and amendments | `UNVERIFIED` | Compare source-grade Owner record and amendment chain with original/mirror locators, classify trust/unknown |
| Establish parent→plan→bounded children | `UNVERIFIED` | Read approved execution graph, actual GitHub parent/child identities and issue/comment readback |
| Tie task evidence to delivery progress | `UNVERIFIED` | Trace one accepted leaf fact through exact candidate, tests, material refs, projector and ancestors |
| Connect live status and smart PR naming | `UNVERIFIED` | Show generated inputs/digest and real provider title/comment readbacks; prove PR coverage separately |
| Preserve repo-wise sessions, changes, decisions and Owner amendments | `UNVERIFIED` | Find indexed schema, writer, source-of-truth links, generated content, privacy guard and consumer |
| Make handover survive repo drift | `UNVERIFIED` | Recompute predecessor frontier and invalidate after base/head/facts/plan changes |
| Whole-system acceptance | `UNVERIFIED` | Fresh real-GitHub end-to-end journey with captures of both source and provider artifacts |

---

## 4. Independent problem architecture and boundary map

### 4.1 Minimal desired causal chain

```text
Owner utterance [verbatim + authentic source grade + amendments]
   → governed parent issue [Owner purpose, authority, root identity]
   → canonical plan graph [approved generations, responsibility IDs, denominators]
   → bounded leaves / comment blocks [outcomes, gates, dependencies, write surfaces]
   → actual candidate change and verification [commit, tests, golden inputs]
   → leaf TASK_EVIDENCE + CHECKPOINT_FACTS_V1 [typed, current, trusted author]
   → provider observations + qualification [PR head/state, refs, negative checks]
   → one pure DELP projection [leaf P/E; ancestor delivery D/E]
   → GitHub issue statuses and generated titles; feature PR association/title
   → repo-wise Owner/session/module/decision index [graded provenance, no secret leakage]
   → derived frontier + source-qualified handover + successor challenge
   → compare with *live* graph/source/provider; HOLD or admit exactly one next unit
```

A connection counts as **physical** only when its producer's actual object, stable identifier or digest is consumed by its successor and, where provider-facing, can be read back from GitHub. A document claiming the arrows is not a demonstration of the arrows.

### 4.2 Verified baseline implementation seams and limits

1. **Input/intent.** `owner_commands.parse_owner_command` accepts direct Owner text and supplied `source_ref`/`authority_ref`; it does not authenticate private chat provenance or turn the envelope into permission. A linked end-to-end Owner intake and parent-issue creation path is **not established by inspected files**.
2. **Plan/authority.** The graph schema supplies root, hierarchy, leaf semantic identity, units and gates. DELP's `validate_graph`, `graph_diff` and `decomposition_report` are concrete mechanisms; the plan still needs human authorization and native issue relation validation. A `plan_updates.owner_authorized` literal is a **recorded claim**, not proof of Owner approval.
3. **Decomposition.** A pure topology classifier, repository observer and assembler exist at baseline. Mechanical `decompose-check` enforces units, verification, budgets and write-surface ordering subject to mode. There is an important distinction between the separate semantic `PASS/SPLIT/…` recommendation and actual admission; the source's explicit integration must be traced, not assumed from a test name. A declared size estimate is not a measured diff.
4. **Evidence.** `ledger_from_github` reads `CHECKPOINT_FACTS_V1` in declared leaf issue comments and evaluates GitHub author association or allowlist; `compute_leaf` binds claimed units to candidate/contract. The normative DELP document expressly states it does **not** establish the truth of each evidence reference. An independent test/golden/source oracle remains required.
5. **Observation.** `observe_github` presently supplies material candidate SHA, PR state/base and branch divergence; it does **not** fabricate checks, diff, liveness or custody when not observed. An absent observation must not become PASS or zero.
6. **Projection.** `project` and title rendering derive one graph-led status. `sync-github` reads facts and candidates and writes generated **issue** titles and managed status comments via a detect-and-retry/version/readback store. GitHub does not offer fully atomic comment/title writes; conflict recovery and final source re-observation are indispensable. The inspected writer does **not** prove a feature-PR title is generated as part of the same transaction.
7. **Continuity/handover.** `frontier` captures an instant with input digests; `frontier-verify` detects `BASE/CANDIDATE_HEAD/PR_STATE/LIVENESS/FACTS/PLAN` movement and asks for reconciliation. It is **not itself** a complete owner/session/index/handover package.
8. **Custody.** `embedded_coder_v35.py` keeps `ENG-PRD-*-CODER` below Local `PRD-*`; `TASK_RESULT` never completes Local responsibility or confers merge permission. Agent A and B must not independently infer a release from projector output.
9. **Runner deployment.** The inspected DELP scheduled publisher template explicitly says `INERT TEMPLATE`. Therefore presence of `sync-github` source and fake-store tests is not proof of a deployed, approved producer for real dynamic titles.
10. **Repo-wise index.** No physical producer→storage→consumer/index refresh path was established from the inspected baseline entrypoints. That is an **unverified integration seam**, not a claim that the whole repository lacks index-related files.

### 4.3 Proof required at each user-visible transition

| Transition | Minimum provider/source proof | Insufficient substitute |
|---|---|---|
| Owner→parent | Verbatim/mirror provenance, authorized parent ID, immutable plan-intent link | An issue title claiming Owner approval |
| Parent→children | Graph parentage + native GitHub child refs/readback + stable claim ownership, no duplicate leaf | Manual checklist of issue numbers |
| Child→code | Actual repository diff, declared write surface, exact old/new commits | Agent “done” statement |
| Code→evidence | Candidate SHA, input fixtures/golden oracle, exact commands and outcomes, trusted facts ref | Tests named in source or fabricated run counts |
| Evidence→status | Same graph/fact/candidate input digest and derived leaf/ancestor numbers | Hand-maintained percentage |
| Status→PR | Feature PR metadata and latest title/description readback linked to same responsibility and material SHA | Issue title only |
| Material→index | Repo/module diff provenance, Owner amendment chain, decision lineage and checked-updated index record | Session prose without source links |
| Index→handover | Exact-index snapshot, observed frontier, unresolved blockers, provenance and authorized next leaf | Old transcript pasted as handover |
| Handover→successor | Fresh provider/source reads; falsifiable 3-question challenge; exclusive admitted lease | Predecessor's own acceptance assertion |

### 4.4 Architectural risk register

- **R1 CRITICAL — disconnected success:** individual components pass but no live graph of consumption connects Owner intake, issues, index and handover.
- **R2 CRITICAL — forged authority:** mirror text/agent paraphrase or `owner_authorized: true` becomes de facto permission.
- **R3 HIGH — false evidence currentness:** refs exist but target unrelated fixtures, fail, cover a previous SHA, or are not reproducible.
- **R4 HIGH — dual status authority:** issue/PR titles or repo index calculate status outside DELP, or two writers race.
- **R5 HIGH — material drift:** base/PR/plan/source dependency moves and handover/benchmarks remain apparently current.
- **R6 HIGH — double execution:** Runner B acquires write privilege while Agent A continues.
- **R7 HIGH — privacy/custody leakage:** private chat or credentials copied to a repo-wise index without authorization.
- **R8 MEDIUM — false health signal:** seven-part delivery health misread as context-token runway or engineering quality.
- **R9 MEDIUM — topology mismatch:** nominally disjoint leaves write same real files or omitted downstream consumer dependencies.

No failure in this register is asserted as an observed *current implementation defect*. Each is a falsifiable acceptance risk.

---

## 5. Prioritized independent continuation plan

**Execution rule:** the following is a **proposal**, not an assignment, new denominator or publication authority. Owner/Coordinator must reconcile it against the live graph and existing responsibility IDs in Stage 2; preserve completed work rather than mint duplicate leaves. “Next” under Stage 1 is source/authority investigation, **not coding**.

| Order | Proposed bounded obligation | Dependencies / permitted future actor | Positive oracle | Negative/fail-closed oracle |
|---|---|---|---|---|
| C0 | **Authority/source census.** Pin actual Owner source grade, baseline vs Agent A start, authoritative repo, Local/V3.5 refs, acceptance epoch, actor/lease. | Owner/Coordinator review; read-only runner | Resolved source matrix; every UNKNOWN explicitly tracked | Mirror is falsely treated as authenticated private source; two live write leases |
| C1 | **Stable lifecycle contract & current responsibility reconciliation.** Inventory parent, children/comment blocks, ID, spec generations, claim ownership and plan source. | C0; plan author only | Every leaf has unique lineage, bounded outcome, dependency, write surface and accepted profile | Duplicate nonshared claim, orphan issue, wrong repository, unapproved denominator change |
| C2 | **Plan release and decomposition validity.** Use classifier/assembler/observer plus `decompose-check` and `graph-diff`; admit only a closed bounded leaf. | C1; Coordinator authorizes plan | Stable cut only when justified; no collision or missing gate; weight conserved | Unknown consumer, undeclared write surface, cheap split creating redundant issue, policy weakening without basis |
| C3 | **Evidence qualification and material truth.** Define exact candidate + source/input/golden dependencies, re-run or reproducible log, and trusted signed/attributed facts. | C2; leaf executor + independent reviewer | Reproducible success and negative controls at exact head; `E` qualified only while current | Fake/stale/wrong-author facts, nonmatching fixture, failed check labeled PASS, ref merely present |
| C4 | **Single graph-led status contract.** Verify status inputs, projection, consumer use and missing-data modes before enabling publication. | C1–C3; projector consumer, no new calculator | Issue title and `LIVE_STATUS_V1` derived from one input digest; ancestor roll-up and invalidation correct | Agent-authored numbers, title drift persisted, provider outage converted to fake zero/current |
| C5 | **Real GitHub lifecycle provider readback.** Exercise child creation/linkage (only if explicitly authorized), evidence comments and feature PR association; evaluate generated PR metadata as a separate consumer. | C4 + write/review/privacy authorization | Real IDs, revisions, readbacks and audit receipts; same snapshot across surfaces | Fake-store-only pass, wrong repo, stale compare-and-swap, partial mutation called transaction success |
| C6 | **Repo-wise Owner/session/change/decision index.** Specify safe schema with verbatim-vs-mirror-vs-agent source grades, per-module commit provenance, material decisions, next action. | C0,C3,C5 + custody/privacy ruling | Fresh index computed/reconciled from authorized sources, reproducible snapshot digest | Sensitive transcript leakage, orphan records, index asserts source status without proof |
| C7 | **Source-current handover & independent successor.** Derive frontier+index evidence, freeze predecessor view, run 3 source questions on fresh head, enforce one custodian. | C3–C6 + Local transfer authority | Reconciliation identifies next authorized unit or HOLD; stale base/head/plan is named | Reused old handover, sole predecessor claim accepted, dual lease, guessed next task |
| C8 | **Whole-system acceptance.** Replay one authorized fresh physical end-to-end case through real GitHub+repo, with independent review and privacy-safe evidence. | C0–C7 + allowed sandbox/provider | Each G-oracle and every causal link observed and read back; negative injections pass | All unit tests green while index/PR title/parent relation is disconnected |
| C9 | **Gated rollout decision.** Propose optional publisher and production enablement separately. | C8 + explicit security/Owner/Local approval | Limited-scope authorized permission, rollback, replay, independent reviewer | Automatic merge/writer or multi-repo propagation inferred from tests |

**C0/C1 are discovery/reconciliation, not license to create implementation tasks.** If another plan already owns C3–C8, modify its `PLAN_UPDATE` only through the governed flow, not via this document.

### 5.1 Material and source-fixture binding

A credible `TASK_EVIDENCE` should carry, or link to an immutable receipt containing:

```text
programme_root / graph_generation / graph_digest
responsibility_id / spec_generation / contract_digest / issue-ref
executor / custody_epoch / lease source (observer-qualified)
repository / base SHA / candidate SHA / material PR or branch
changed files + relevant consumer/dependency file hashes
test source + command + environment + run log/exit + test/fixture revisions
input/golden fixture content digests + comparison oracle and exclusions
result / accepted verification status / reviewer disposition / time observed
provider URLs + GitHub readback identifiers / unsupported or absent evidence
```

Binding must be *source aware*: a candidate SHA does not on its own prove that a changed fixture, parser dependency, acceptance contract or external input remains the same. Keep original engineering golden fixtures distinct from generated expectation files. Unsupported/unknown proof yields `UNKNOWN/HOLD`, not successful coverage.

### 5.2 Verification ladder — practical, independent, negative-first

**V0 static contract:** validate schema, graph, facts; inspect original Owner envelope/authority source and mapped responsibility. Reject extra fields, wrong repo, duplicate responsibility, malformed SHA, and agent-authored percent/status.

**V1 pure projection:** pin plan/facts/observations; assert `E<=P`, ancestor conservation, no false rounded full, fixed `input_digest`, deterministic titles, correct `UNMATERIALIZED` on observed work without facts. Push simulated candidate A→B: `P` held, `E` reduced; replay B and restore only justified `E`.

**V2 source-specific tests:** run focused Node/Python/Chromium or relevant real environment *for the actual product under test*, using genuine golden fixtures and exact input/expected digests. Introduce modified golden, failed test, changed dependency, unsupported optional category and wrong source-file hash; none may qualify evidence.

**V3 provider adapter contract:** use test doubles only to red-team transport rules (untrusted author, PR mismatch, stale marker, wrong repo, response missing data, writer conflict). Re-read after a conflict; do not claim API-level atomicity.

**V4 real GitHub acceptance:** in an explicitly approved disposable programme/repo, exercise parent and two bounded leaves with authentic native references; publish start and completion facts; read back created objects, status and PR association; change one candidate and one plan contract and verify invalidation; deliberately hand-edit a title and demonstrate deterministic correction if authorized; stop when provider unavailable. No actual issue/PR/status mutation is authorized by this Stage 1 draft.

**V5 handover replay:** freeze at A, advance material/base/plan to B, then require successor to locate changed input, challenge predecessor conclusions, name required evidence recovery and hold until exclusive lease granted. A perfect-looking handover that fails live reconciliation is a failure.

**Independent review:** a distinct reviewer must inspect both source and negative tests and explicitly record ACCEPT / CHANGES_REQUIRED / INSUFFICIENT_EVIDENCE; same actor's narration and “green” workflow alone are not an independent verdict. For a browser-visible integration, use actual Chromium user journeys and compare both rendered UI and downloaded output, not only synthetic isolated fixtures.

### 5.3 Stage 1 earliest legitimate next action

Record the frozen reconstruction, preserve the barrier, and request **Stage 2 admission evidence** from the governing Owner/Coordinator. At actual Stage 2, first inspect current graph, source, lease, unresolved provider actions and last accepted evidence; reconcile against C0/C1. **No implementation unit can be named as the current authorized next unit from this packet.** A correct action is `HOLD — AUTHORITY/CURRENTNESS_NOT_ESTABLISHED` until verified.

---

## 6. Proposed GitHub further-activity issue / IMPLEMENTATION_PLAN (UNPUBLISHED)

> **DRAFT_NOT_PUBLISHED — NOT A NEW RESPONSIBILITY.** This block is a copy-ready prospective issue body. Root/leaf and plan revision must be reconciled in Stage 2. Do not post it or assign weights from Stage 1.

### Proposed title

`[V3.5-R14][DRAFT] Recover the physical Owner→DELP→repo-index→handover lifecycle with source-qualified acceptance`

### Proposed issue body

**Status:** `DRAFT_NOT_PUBLISHED` / **Authority:** `NOT_ADMITTED` / **Parent programme issue:** `UNKNOWN (resolve from approved Common V3.5 graph)` / **Primary implementing leaf:** `UNKNOWN` / **Current spec generation:** `UNKNOWN` / **Candidate PR/branch:** `UNKNOWN` / **Owner/source basis:** mirrored quotations Common#787 §0 and Common#878, original-chat URI `UNKNOWN` / **Governing roadmap context:** curated Common#864 desired outcome and WP0–WP10 categories; live approved plan `UNKNOWN`.

**Problem.** V3.5 must demonstrate one *physical* engineering chain from Owner purpose and issue creation through approved decomposition, bounded tasks, source-checked evidence, derived parent/child/PR status, repo-wise decision/index records and a handover that survives source drift. At the frozen protocol baseline, DELP and related schemas provide important machinery, but their existence is not a full-chain GitHub acceptance verdict. Do not treat completion percentage, smart titles or generated handover prose as proof of upstream sources.

**Desired outcome.** Any successor can reconstruct the original Owner objective with source grades; see exactly one governing graph, stable leaf ownership, current engineering evidence tied to material/golden data, real GitHub provider readbacks, index module/change/decision provenance, and the next *authorized* unit or an explicit hold.

**Acceptance claims:** G-INTENT, G-PLAN, G-EVIDENCE, G-STATUS, G-INDEX, G-HANDOVER and G-NEGATIVE are mandatory. Each must have a source ID, positive test, negative test, exact material receipt and independent verdict.

**Deliverables / proposed bounded work:**

1. A signed-off source/authority matrix, including original-chat ambiguity and exact Local/V3.5/plan refs.
2. Reconciled root/leaf graph, claim ownership, bounded child issues/comment blocks and plan generation, with `decompose-check` and `graph-diff` receipts.
3. Material-evidence qualifier linking candidate SHA, source dependencies, genuine fixtures, logs, reviewer outcomes and `CHECKPOINT_FACTS_V1`.
4. One derived snapshot consumed by parent/child issue statuses and separately verified feature-PR metadata; no alternate status calculator.
5. Repo-wise provenance index with Owner source grade, session facts, module/commit changes, acceptance history, decision ledger, safe custody rules and links to exact snapshot.
6. Handover with derived frontier, provider/readback evidence, explicit unresolved decisions, three-question independent reconstruction challenge and exclusive lease transition.
7. One real GitHub+Chromium where applicable E2E evidence package and adversarial failures, not fake-store-only proof.

**Dependency/release order:** authority → plan/identity → evidence → status/provider readback → index → handover → E2E qualification. Discovery precedes work when baseline moved, a consumer is unknown, a reviewer gate is missing or the stable-cut classifier says `DISCOVER_FIRST/REPLAN`.

**Boundaries:** do not mutate existing issue/PR/roadmap/status during research; do not activate publisher, copy private chat, create duplicate leaves, change weights, adopt acceptance policy or merge. Any new write scope, source retention policy or programme denominator requires separately recorded Owner/Local governance decision.

**Positive acceptance examples:** current exact source/test receipt counts once; current facts drive same ancestor status; a genuine GitHub issue and PR show matching snapshot; changed base triggers handover RECONCILE; successor can identify one bounded next admitted unit.

**Negative acceptance examples:** untrusted comment/forged Owner ref does not count; wrong fixture fails; branch push stales `E`; source contract changes require generation binding; empty ledger with observed PR is `UNMATERIALIZED`, not zero-work; moved plan or changed evidence invalidates handover; conflict/outage yields no false successful publication; a parent issue cannot be a leaf executor; dual executor or unapproved merge fails closed.

**Engineering evidence format:** use the established `IMPLEMENTATION_PLAN`, append-only `PLAN_UPDATE`, leaf `TASK_EVIDENCE` with typed facts, and `TASK_RESULT` only at an admitted result boundary. Reuse current responsibility IDs and weights; new issue representation/claim must be a governed semantic responsibility, not a logging convenience. All evidence includes immutable source/test/fixture refs and current provider observation.

**Review/release gates:** Coordinator source-level assessment, independent reviewer verdict, real provider readback after writes, explicit Owner/security/privacy decisions for indexing and publishers, Local reviewer/super-review/merge decision separate from Coder completion. A green test run cannot waive missing gates.

**Owner action at publication:** determine parent/leaf binding, approve or reject any nontrivial scope/index custody rule, and identify the authorized reviewer/publisher. **Until then: HOLD.**

**Success/failure scoreboard:** derived from governed plan/facts/provider only; no manually assigned percentages, no invented completed items and no feature-PR “smart” title unless its own consumer/readback is proved.

> **End of unpublished proposed issue body.** Its construction is research, not a new task, plan revision, GitHub publication or Owner approval.

---

## 7. ROI / parked-work register

| Candidate | ROI | Basis / expected value | Scope class and disposition | Revisit trigger |
|---|---|---|---|---|
| Full-chain causal trace and real GitHub readback | **HIGH** | Direct Owner correction and G-STATUS/G-HANDOVER; reveals disconnected adapters | Core acceptance, candidate after C0 | Owner approves bounded acceptance surface |
| Independent material+fixture evidence qualifier | **HIGH** | DELP normative text explicitly cannot vouch for evidence-ref truth | Core acceptance, must reuse existing evidence semantics | At C3 scope review |
| Owner/source-grade and repo-wise index chain | **HIGH** | Explicit later Owner correction | Core objective, privacy approval prerequisite | Source and custody matrix approved |
| One snapshot for issue and PR consumers | **HIGH** | Prevents drift between DELP status and feature PR prose | Integration hypothesis; inspect extant consumers first | C4 real consumer inspection |
| Exclusive lease and moved-frontier successor exercise | **HIGH** | Prevents double executor and stale handover | Core safety/acceptance | Stage 2 source/lease readback |
| Better typed diagnostics/replay reports | MEDIUM | Saves failed-run forensics | PARKED, no scope/weight now | Two distinct real failures with ambiguous diagnosis |
| Larger randomized/adversarial fixture generation | MEDIUM | Catches rare semantic drift | PARKED, after authentic-golden cases | Real regression escapes fixed negatives |
| Additional repository variants and extension adapters | MEDIUM | Portability beyond single scoped pilot | PARKED | Full-chain acceptance of first repository |
| Cosmetic dashboards or alternative status widgets | LOW | No demonstrated authority/engineering benefit | DECLINED for this work | Owner identifies specific missing readout |
| Generalized private transcript retention/indexing | LOW until governed | High privacy and authorization risk | DECLINED absent separate decision | Formal custody/privacy policy approves |
| Production automatic issue-title publisher/auto-merge | Not a discretionary ROI item | Separate security/reviewer authority | PARKED OUTSIDE SCOPE, no default enablement | Explicit Owner/Local/security go/no-go |

A HIGH item is **not** permission to expand the current workpack. A MEDIUM item creates no new weights or issues. The independent decision to keep a semantic responsibility whole is allowed when a proposed split lacks a stable cut.

---

## 8. Exactly three falsifiable Stage 2 repository-grounded reconstruction questions

**Q1 — Provenance and actual code path.** At Agent A's **actual starting commit** and the **current candidate SHA**, which concrete source modules, APIs and exact plan/issue identities implement the path from Owner instruction and authorized parent/decomposition to a leaf and then to derived status, repo index and handover; for each claimed edge provide file/line/commit and provider readback, and identify any edge that does not physically exist?

**Q2 — Evidence/status agreement.** For one real current bounded leaf, which exact `responsibility_id/spec_generation/contract_digest`, PR head, changed input/golden hashes, accepted `TASK_EVIDENCE`, independent test/reviewer receipts and derived `input_digest` underpin the leaf and ancestor issue/PR statuses; after a controlled candidate or dependency move, what evidence is invalidated and do GitHub readbacks agree with the single projector?

**Q3 — Authorized next action.** Given the current Owner amendment basis, plan revisions, dependencies, Local acceptance and reviewer gates, outstanding provider mutations, custody/lease state and source-current frontier, what exact existing semantic unit (issue/ID/commit/write surface) may **one** successor execute next, or why must it be `HOLD/RECONCILE`; which source/provider facts would falsify that admission?

These questions are **not** answered by this Stage 1 packet; attempting specific current PR/branch or next-unit answers now would break independence.

---

## 9. Stage 2 required information — request only after admission

| Required packet | Why it matters / validation |
|---|---|
| Actual Agent A original task-start SHA; current pinned source tree and changed-module/consumer inventory | Separate pre-work source from the later protocol baseline; inspect producer→consumer links |
| Current worktree/branch, exact candidate PR/commit, diffs and source-index revision | Material truth, uncommitted changes and affected acceptance dependencies |
| Agent A's latest implementation plan, append-only plan updates and final handover if available | Compare independent approach; do not silently adopt predecessor conclusions |
| Authoritative V3.5 execution graph, Local control-plane protocol/profile, parent/child/comment-block and feature PR identities | Reconcile ownership, denominators, releases and physical GitHub links |
| Trusted `CHECKPOINT_FACTS_V1` ledger, provider observations, tests/golden inputs, CI/browser logs and reviewer qualifications | Source-bound accepted P/E and truthful completion |
| Current provider title/status readback, writer controls, trace of `sync-github` use, repo-wise index producer/consumer files | Detect disconnected projection or competing writers |
| Live Owner/reviewer/security approval scope, executor/lease/custody epochs and outstanding provider transaction IDs | Prevent dual execution or unapproved writes |
| Repo privacy/custody policy, current Owner instruction and amendment source references | Distinguish publishable provenance from protected messages |
| Fresh derived frontier and drift checks at Stage 2 observation time | Reconcile change since Agent A's last checkpoint |

**Promotion precondition:** a separately authorized transition must prove Agent A's write lease is closed/transferred before Runner B can write. Stage 2 is not begun by filing this document.

---

## 10. Acceptance decision matrix and stop rules

| Golden oracle | Current Stage 1 evidence | Required whole-chain acceptance | Stop condition |
|---|---|---|---|
| G-INTENT | Mirrored exact wording; baseline Owner parser | Authenticated or correctly graded Owner source and amendments consumed by plan/index/handover | Paraphrase given original authority |
| G-PLAN | Graph schema, classifier/assembler/observer, diff/gate source | Real bound children and conserved approved claims with provider readback | Orphan/duplicate responsibility or unknown consumer |
| G-EVIDENCE | Facts schema, ledger/provider code, source tests | Independent exact candidate/fixture/test and reviewer qualification | Fake/stale/unreproducible result |
| G-STATUS | Projector and issue-sync source, inert template | Same digest drives actual child/parent issue and verified feature PR metadata | Manual numbers or discordant snapshots |
| G-INDEX | Owner requirement; no end-to-end index path established in inspected entrypoints | Index built from authorized source/commit/decision facts and consumed by handover | Sensitive leakage or unsupported status |
| G-HANDOVER | Frontier/verify and successor test definitions | Independent successor detects moved inputs, answers challenge and is exclusively admitted | Predecessor snapshot assumed current |
| G-NEGATIVE | Normative fail-closed rules and test definitions | All negative injections at real provider/boundary where applicable | A fake source/permission/CI/lease yields PASS |

**Overall Stage 1 engineering verdict:** `PROBLEM_RECONSTRUCTED; BASELINE_PARTIAL_CONTRACTS_OBSERVED; CURRENT_IMPLEMENTATION_UNKNOWN; REAL_GITHUB_END_TO_END_NOT_ESTABLISHED; NO_EXECUTION_ADMISSION`. This is not a programme score or a declaration that Agent A has failed.

---

## 11. Contamination and information-barrier declaration

**Direct inspections conducted for this artifact:** only the prior frozen `STAGE1_RUNNER_PROMPT.md` (already read in the immediate preceding turn), the curated text reproduced there and the explicitly immutable `Common@13989969f6b7e432c4f7c1ddfe975449dba53593` source files listed in §2. No Stage 2 source, implementation PR, current issue status, active CI or predecessor handover was **queried**. Attempts to open the immutable GitHub tree through the public web interface returned a disabled-fetch error; the read-only GitHub connector was instead used with the **exact immutable SHA**. No moving default-branch code search was used.

**Ambient exposure limitation:** preceding context available to this conversation includes historical V3.5 project summaries not part of the sealed fixture. Those summaries were deliberately excluded from research conclusions, PR identification and continuation planning. Nevertheless there is no technical context isolation that could guarantee the model was blind to them. In accordance with the frozen prompt's fail-honestly rule: `STAGE1_INDEPENDENCE=CONTAMINATED` (ambient-context qualification), not `CLEAN`. This does **not** assert that Agent A's current code, implementation method or final handover was inspected; it means a rigorous blind-independence claim cannot be made in this chat environment.

All proposed current-state observations remain `UNKNOWN`; the plan is based on permitted evidence, not the ambient summaries. An auditor needing a strict clean-blind Stage 1 run should replay the same frozen packet in an isolated context.

---

## 12. Freeze and custody receipt

**Artifact:** `RUNNER_RECONSTRUCTION_V1.md`  
**Digest scope:** exact UTF-8 bytes of this Markdown payload as submitted to GitHub; the transport-level SHA-256 and Git blob SHA are recorded in the publication/readback receipt outside this self-hashing document (avoids self-referential digest).  
**Freeze status:** `FROZEN_STAGE_1`, immediately before the **sole** authorized artifact-only GitHub publication.  
**Fixture and protocol inputs:** frozen prompt `V35-R14-RUNNER-S1-20261009-A`; immutable baseline `13989969f6b7e432c4f7c1ddfe975449dba53593`; selected file blob SHAs recorded in §2.  
**Observed-at note:** 2026-10-09 (Asia/Muscat); not a claim about exact current provider state.  
**Receipt meaning:** a local content hash + Git blob hash and post-commit readback establish byte integrity, **not** identity authentication, independent reviewer approval, clean blind independence or an implementation acceptance result.  
**Authority after freeze:** Agent A retains execution; Runner B has no lease and cannot execute or start Stage 2. Further revisions require a visibly new artifact/version and an authorized process, not silent edits to this frozen document.
