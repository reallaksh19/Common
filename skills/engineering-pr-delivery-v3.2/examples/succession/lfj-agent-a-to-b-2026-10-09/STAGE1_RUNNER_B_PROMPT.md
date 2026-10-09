# GOLDEN FIXTURE — RUNNER B STAGE 1 INPUT (BLIND RECONSTRUCTION)

**CASE_ID:** `v32-succession-lfj-real-2026-10-09`  
**SENDER:** trusted succession controller, transmitting the Owner and Agent A's strictly bounded **WHAT/WHY** briefing  
**RECIPIENT:** Runner B (not Agent A)  
**PERMISSION:** `READ_RECONSTRUCT_PLAN_ONLY`  
**VISIBILITY:** `STAGE1_ONLY` — no current code/PR/evidence/current issue feed  
**RECONSTRUCTION_BASE:** `reallaksh19/3D_Converters@1205639a43e9ce1589360479d2558678aebcfab7`  
**PROTOCOL_PROVENANCE:** `reallaksh19/Common@13989969f6b7e432c4f7c1ddfe975449dba53593:skills/engineering-pr-delivery-v3.2`  
**HEALTH:** `CONTEXT_BUDGET_CONSUMED=UNKNOWN`, `V3.2_AGENT_HEALTH=NOT_DERIVED`. Succession was explicitly requested by Owner; **do not pretend a measured 70% threshold was crossed**.

> **STOP:** You are **Runner B** in Stage 1. You have NOT received permission to modify application source, choose Agent A's next PR, or take over Agent A's write epoch. Treat all text below as requirements and source context, not implementation authority.

## A. Unmodified Owner utterances

### Original LFJ efficiency question preserved in governing issue

> My simple question, based on downstream consumer data required ex: DTXR, branch name, SPREF,*SUP* etc i.e, fields that are required, can the indexing and storage be not smarter ... instead of handling 30MB+ Data at every stage?

### Original direction to develop the governed plan

> now create a detailed plan, can you decompose task in efficient way and follow coding protocols in https://github.com/reallaksh19/Common/tree/main/skills/engineering-pr-delivery-v3.2

> ensure your new issue, capture this entire plan , my intent and all the techical details.  
> ok start batch 0

### Owner's successor-runner conception — verbatim, 9 October 2026

> you have done a great job, but to continue, we need to have like this..
>
> In this block you are agent A
>
> 1. Primary Agent A — normal execution
>
>    Works under its existing V3.x responsibility, publishing ordinary task evidence and checkpoints.
> 2. Approximately 70% of usable life consumed
>
>    Agent A emits `TIME_FOR_RUNNER_REQUESTED`. This is a preparation request, not a permission transfer.
> 3. Stage 1 — Runner B reconstructs independently
>
>    Uses a strictly allowlisted initial repository, Owner intent, roadmap, WHAT/WHY briefing and golden fixtures. Freezes an independent plan before seeing Agent A's current work.
> 4. Stage 2 — planned or emergency reconciliation
>
>    Inspects live source, existing implementation, evidence and Agent A's final plan if available. Identifies gaps, unnecessary changes and the correct next action.
> 5. Exclusive promotion
>
>    An enforceable execution controller revokes Agent A's write authority and grants Agent B a new execution epoch.
> 6. Agent B becomes primary
>
>    Publishes the reconciled plan where authorized, continues the legitimate responsibility, and eventually prepares Runner C.
>
> My original idea:
>
> runner should start at about 70% of agent life (Based on agent health metric).\
> Runner should be aware in stage 1 broader repo info and task, no PR stats. \
> Basically stage 1 should not allow runner to copy but reconstruct the way agent has done and to know what is next (as per roadmap or parent issue).\
> Sequence: agent 1 (~70% health)->Runner (Stage 1 data shown: i.e, present agent's original commit, what were the issues addressed (Not how), only what and why, present agent tells, pending action, known issues, parked data, source input, golden fixture). This will the core for runner's reconstruction)->Runner understands and make a plan->Agent 2 also creates a new github issue or detailed further activity implementation plan.\
> Stage 2: present agent  handover the current repo state with his plan->runner agent, step back, reconcile his plan (Not copy) and updates the github issue with revised plan and starts with task decomposition as per v3.x. update roadmap if required. adds Medium ROI which were not taken up during reconciliation. High ROI might have been absorbed.\
>
> How do you calibrate agent/content window length, not precise but a basic way, agent himself should say "Time for runner" in Task evidence.

**Owner's latest instruction:** "yes .. need to save this in golden fixture... so be real as possible"

Do not normalize away the Owner's original wording or reinterpret a requested successor as authorization to expose Agent A's solution.

## B. Immutable application context — WHAT and WHY ONLY

**Repository:** `reallaksh19/3D_Converters`. Engineering application: **XML → CII 2019 Standalone**, consuming original XML and staged structured JSON; other original consumers include the StagedJSON → Enriched XML workflow. The broader LFJ/1.0 programme aims to offer reusable large structured-data intake across multiple applications while preserving original source identity and downstream domain authority.

**Task outcome:** Achieve actual large-data handling, not a demonstration that one isolated parser is fast. A large JSON original (30MB+ in Owner's scenario) must be fully preserved without repeatedly parsing/materializing/writing/sending all of it at each downstream consumer stage. Real consumer demands include configured `DTXR`, `DTXR_POS`, `DTXR_PS`, `SPREF`, support refs/tags, engineering node and component references, branch/ancestor identity, coordinate/bore fields, and user-selected scope. Source aliases and enabled fields are configurable; `*SUP*` is an illustrative requirement, **not a permitted hardcoded wildcard as domain truth**.

**Must not regress:** exact source data/provenance, distinction between invalid source and zero matches, branch occurrence identity and own-vs-ancestor Site/Zone, approved engineering matching and tolerance/precedence, original/combined XML, both Node-wise Trace and Evidence Tree CSV, distinct downstream Enrichment/PSI/XML, Preview and Weight source-basis and engineering authority. An end-user release requires actual application functionality in a genuine served Chromium journey.

**Why this matters:** The same original large source is reused by different consumers. Material overhead may be wasteful, but a source-specific optimization can silently drop required fields/relationships or change actual engineering meaning. The Owner wants a source-backed, verifiable, pragmatic recovery that respects existing product contracts.

### Agent A WHAT/WHY-only briefing

Agent A was asked to address repeated large-source handling, investigate the downstream field requirements and expected engineering parity, and distinguish source-only qualification from the real product. The remaining problem includes authentic XML/JSON matching, both actual CSV outputs, source lifetime and interruption correctness, 30MB+ authenticity, and actual deployed browser behavior. Do not infer from this briefing that A's approach was correct, complete, merged, deployed, or accepted.

**Known issues to assess independently:**
- An apparent field name match does not prove the consumer's semantic alias/precedence rule.
- Hierarchical ancestry and duplicate branch names may create false matches.
- A matching CSV hash may conceal a degenerate case in which every XML node was unresolved.
- Original XML and original JSON drawn from the same benchmark folder may not be the right engineering-positive pair.
- Failed to run, runtime verification failed, and engineering semantic mismatch are different failure categories.
- A successful source catalog or test fixture is not authorization for the live Resolver Build or either CSV download.

**Pending outcome:** Real positive and negative engineering matching using original source/goldens; exact full-output oracles; resilient source/selection/configuration invalidation and cancellation; actual application integration/deployment and 30MB+ acceptance.

**Parked from the immediate Resolver release but NOT forgotten:** separately governed Enrichment/PSI/XML, cross-repository LFJ deployment, any Preview/Weight architectural change. Reconstruct dependency order rather than silently deleting these requirements.

## C. Strict Stage 1 read allowlist

**Fixed original source revision (do not auto-update to main):** `reallaksh19/3D_Converters@1205639a43e9ce1589360479d2558678aebcfab7`.

Read these paths **at the fixed revision only** (plus directly imported dependency files at that same revision when needed to explain original function behavior):

```text
tabs/xml-cii-2019-standalone/xml-cii-json-trace-fields.js
tabs/xml-cii-2019-standalone/xml-cii-trace-resolution-ledger.js
tabs/xml-cii-2019-standalone/xml-cii-resolver-json-trace.js
tabs/xml-cii-2019-standalone/xml-cii-json-hierarchy-scope.js
tabs/xml-cii-2019-standalone/xml-cii-trace-export.js
tabs/xml-cii-2019-standalone/xml-cii-trace-spatial-index.js
tabs/xml-cii-2019-standalone/stagedjson-enrichment/stagedjson-branch-context.js
tabs/xml-cii-2019-standalone/stagedjson-enrichment/stagedjson-enrichment-engine.js
converters/xml-cii2019-core/source-schema-adapter.js
lfj/ (only original neutral source/runtime/port interface contracts at the frozen revision)
```

**Source/fixture registry, ORIGINAL files at frozen revision** (read actual bytes; verify source hashes and fixture suitability yourself):

| Input | Authentic source / expected purpose | Source identity |
| --- | --- | --- |
| `Benchmarks/1885Sjson/Sjson.json` | Original smaller real staged JSON, semantic fixture candidate | 733,806 bytes; SHA-256 `6b2c8b01ab0ba6ec8e9e7c42eb4a719668ffd2dc4dbe4790d27cf426a1f60288` |
| `Benchmarks/1885Sjson/FirstpassXML` | Authentic XML candidate; **verify** true pairing before calling positive | Original file; SHA/length must be computed by Runner |
| `Benchmarks/1885Sjson/ExpectedXML` | Different authentic XML; **do not assume** every same-folder file is a positive golden | Original file; SHA/length must be computed by Runner |
| `Benchmarks/1885_NC/1885_NC.json` | Original larger real staged JSON, stress input | 10,232,634 bytes; SHA-256 `89f9c2ab7a9f1df15c1b9e1e0e30a8ca6c97ef994dcd56aec86c3a90f7d71646` |
| `Benchmarks/1885_NC/1885_NC.topology.input.xml` | Original large XML candidate | Original file; SHA/length must be computed by Runner |

The authentic Owner 30MB/90MB sources are **not asserted present**. Do not invent them, pad files and call them authentic, or treat 10MB as release-scale qualification.

**Stable programme roadmap envelope:** original large-source custody and profile → source hierarchy/selection → consumer domain fields → original XML match and two CSV outputs → real served app source+Worker/deployment → independent Enrichment → authentic large-file/fault acceptance. This describes outcome/dependencies only, not Agent A's implementation recipe.

**V3.2 source:** `Common@13989969f6b7e432c4f7c1ddfe975449dba53593`, `skills/engineering-pr-delivery-v3.2/SKILL.md`, source/progress/decomposition contracts as needed. V3.2 is a candidate implementation line unless accepted/cut over; this Owner explicitly directed V3.2 treatment in this engineering work.

## D. Hard blind-reconstruction rule

Your Stage 1 tool surface must block:
- Agent A's live branches, current code/diffs, PR lists/statistics, work issues/comments, exact current heads, screenshots or tests;
- successor/handover **Stage 2** content; agent commentary claiming which design won;
- unrestricted GitHub search or live `main` lookups that could accidentally show current work;
- any automatic/current issue scoreboard or programme report authored after the original freeze.

**This is a test contract, not an access-control implementation.** Even though the case is stored in a public GitHub repository, a trusted runner must physically filter all tool inputs and mount only allowlisted pinned-source copies. If you have unrestricted GitHub tools, explicitly report `STAGE1_ISOLATION_NOT_ENFORCED` and refuse to claim a blind reconstruction. Do not pretend a written rule is a sandbox.

## E. Your independent output — freeze before seeing Stage 2

Create your own **independent engineering assessment** with the following substantive content, with original path+symbol/fixture source anchors, not a generic answer:

1. Explain the original Owner's outcome, objective/cost and safety constraints, and which real application artifact proves completion.
2. Draw an original consumer/source ownership graph from *your own* reading. Distinguish structural source fact, configured engineering interpretation, derived match result, exported artifact and Preview/Weight authority.
3. Independently evaluate plausible data handling architectures; do not automatically propose Agent A's approach. Justify chosen candidate against exact original source semantics, IDB, Worker, archive/readback/cancel and old/new source identity.
4. Design a new decomposed V3.x workplan that respects current PRODUCT vs DELIVERY_GATE claims, existing denominator/ownership, bounded exclusive write surfaces, independent positive/negative source oracles, real Chromium, and no guessed programme progress/weights.
5. Answer these three **source reconstruction questions**:
   - **Q1:** Which exact original source modules/functions control XML matching, JSON branch/ancestor identity and both CSVs? What code observation could disprove your understanding?
   - **Q2:** Which original source fields, field configurations, ancestor context and free-text support rules must survive sparse indexing? Give at least three realistic counterexamples that defeat a naive field whitelist.
   - **Q3:** How can original JSON/real XML fixtures independently falsify source-only correctness, actual resolved engineering match parity, negative/no-match handling, both exact CSV bytes and real deployed browser behavior? Identify sample-pair risk.
6. Document medium/high ROI candidates as **hypotheses**, unsupported ideas as parked, genuine ambiguities as questions. Do not invent acceptance evidence.
7. Write/freeze your own `IMPLEMENTATION_PLAN` in a **distinct Runner B issue or immutable plan object**, with evidence that Stage 2 has not been exposed. Supply `STAGE1_PLAN_FROZEN` with a SHA-256 of the frozen plan, source baseline and issue/immutable URL.

**Until you freeze:** `NO_STAGE2_READ`, `NO_PRODUCTION_WRITE`, `NO_OWNERSHIP_TRANSFER`. Stage 1 preparation must not change the existing LFJ programme denominator or claim that a new Runner issue earns progress. If the allowed source/custody information is insufficient, state the uncertainty and freeze a falsifiable conditional plan rather than copying someone else's.
