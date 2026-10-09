# HOW I constructed the Stage 1 and Stage 2 successor prompts — real LFJ engineering case

**Case:** `v32-succession-lfj-real-2026-10-09`  
**Owner request:** preserve two reusable Stage 1/Stage 2 golden prompts in Common PR #880, and explain both the actual construction process (**HOW**) and the necessary robust-prompt requirements (**WHAT**).  
**Document class:** author-methodology/fixture-design evidence — **not** an Agent A implementation plan, a claimed successful Runner B handover, a Stage 1 input, a TASK_EVIDENCE publication, or an execution controller.  
**Protocol:** `Common@13989969f6b7e432c4f7c1ddfe975449dba53593:skills/engineering-pr-delivery-v3.2`, whose `SKILL.md` identifies it as a candidate until independently cut over.

## 1. What I actually created — distinguish historical inputs from authored outputs

| Artifact in this draft PR | Source/creation method | Visibility when executed | Status |
| --- | --- | --- | --- |
| [`GOLDEN_STAGE1_RUNNER_B_PROMPT.md`](GOLDEN_STAGE1_RUNNER_B_PROMPT.md) | **Byte-for-byte copy** of real `Common/relay/AGENT_A_LFJ_20261009/STAGE1_RUNNER_B_PROMPT.md` at `Common@5067aa1b408973102dccb20e684d9de5689af23a`, Git blob `7504bff62d0e6a495299019e88ee47541443acdb`. No silent rewrite. | Runner B may see only this approved Stage 1 prompt and its separately allowed original source/Owner/fixture material. | Historical authoritative input, copied for regression testing |
| [`GOLDEN_STAGE2_RUNNER_B_PROMPT.md`](GOLDEN_STAGE2_RUNNER_B_PROMPT.md) | **New prompt authored for this PR**, based on the real Agent A succession checkpoint, Stage 2 reality evidence, V3.2 authority rules and observed failure cases. It is NOT a copy of an already executed Stage 2 conversation. | **Never** released before an independently verified Stage 1 freeze and Controller/Owner approval. | Specimen prompt for a future controlled Stage 2 |
| [`STAGE2_AGENT_A_REALITY_PACKET.md`](STAGE2_AGENT_A_REALITY_PACKET.md) | Earlier historical packet from the same project, capturing actual draft PR/source/CI claims and unresolved defects as of its recorded time. Not a second prompt; it is **Stage 2 input data**. | Stage 2 only, released together with the Stage 2 prompt after the gate. | Historical snapshot requiring LIVE re-observation |
| [`OBSERVED_NEGATIVE_STAGE1_CONTAMINATION.md`](OBSERVED_NEGATIVE_STAGE1_CONTAMINATION.md) | Owner-supplied transcript excerpt of a prospective agent that read a Stage 2-only Agent A checkpoint before freezing Stage 1. | Evaluator/controller only; never part of Stage 1 input. | Negative acceptance case; observation reported by Owner |
| [`STAGE1_RUNNER_B_FRESH_SESSION_V2.md`](STAGE1_RUNNER_B_FRESH_SESSION_V2.md) and original `STAGE1_RUNNER_B_PROMPT.md` | Earlier authored candidate/rehearsal prompts. Retained for construction provenance and comparison; **not interchangeable** with the exact historical relay Stage 1 frozen prompt. | Not passed alongside the selected Stage 1 golden during a single controlled run. | Historical variants, not the single official golden input |

**Important:** Storing both prompts in the same GitHub PR is an archival convenience, **not technical information isolation**. The controller must curate a separate Stage 1 read mount; it must never give a blind Runner B access to the entire fixture directory or PR.

## 2. HOW I developed Stage 1 — reality-first reconstruction, not an Agent A recipe

### Step S1 — Start from actual Owner utterances, preserve distinctions

I took the Owner's question about downstream fields — `DTXR`, branch name, `SPREF`, `*SUP*` and repeatedly processing `30MB+` staged JSON — as an outcome requirement, **not** a direct instruction to use sparse pages, Blob slices, IndexedDB records or any Agent A solution. I preserved the broader requirements already stated for `XML → CII 2019`: a working Resolver, original XML, both CSV exports, source/branch provenance, actual Chromium behavior and separate Enrichment/Preview/Weight semantics.

The task is **consumer-driven, lossless source handling**. The words "30MB+" describe an intended product-scale burden, not verification that an authentic 30MB source has passed.

### Step S2 — Select a real, immutable pre-work source baseline

The frozen application revision is `3D_Converters@1205639a43e9ce1589360479d2558678aebcfab7`. The frozen candidate protocol source is `Common@13989969f6b7e432c4f7c1ddfe975449dba53593`. Their **role** matters: these are Stage 1 reconstructable reference commits, not a claim that Agent A began all engineering at precisely the protocol commit.

I selected baseline source contracts by **downstream consumer responsibility**, not by scanning a current Agent A PR. The prompt points to original functions and modules for:
- `xml-cii-trace-resolution-ledger.js` — original staged-json traversal, branch/position support and XML resolution evidence;
- `xml-cii-resolver-json-trace.js` — actual Resolver matching surface;
- `xml-cii-json-trace-fields.js` — configured capture/decoration and support field semantics;
- `xml-cii-json-hierarchy-scope.js` — hierarchy/scope contract;
- `xml-cii-trace-export.js` — two real CSV outputs;
- `converters/xml-cii2019-core/source-schema-adapter.js` — configurable source-role aliases/conflict semantics;
- `stagedjson-enrichment` modules — a distinct downstream consumer;
- pinned original `lfj/` source/runtimes — interfaces to inspect independently, not a prescribed new architecture.

A Runner must cite **actual frozen symbols and observations** to prove it read these files. Listing filenames is not an answer to Q1.

### Step S3 — Use authentic fixtures and preserve uncertain pairing

Allowed input candidates include:
- `Benchmarks/1885Sjson/Sjson.json` — 733,806 original bytes, SHA-256 `6b2c8b01ab0ba6ec8e9e7c42eb4a719668ffd2dc4dbe4790d27cf426a1f60288`;
- `Benchmarks/1885Sjson/FirstpassXML` and `ExpectedXML` — **distinct authentic files**, not automatically equivalent positive goldens;
- `Benchmarks/1885_NC/1885_NC.json` — 10,232,634 original bytes, SHA-256 `89f9c2ab7a9f1df15c1b9e1e0e30a8ca6c97ef994dcd56aec86c3a90f7d71646`;
- `Benchmarks/1885_NC/1885_NC.topology.input.xml` — genuine original XML whose source pairing must be established.

I deliberately did **not** claim authentic 30MB/90MB acceptance sources were present. A generated dataset is a valid adversarial/stress control only when marked generated, not a substitute for real Owner data.

### Step S4 — Strip solution leakage, NOT the engineering problem

The Stage 1 prompt retains original task WHAT/WHY, source/fixture input, roadmap/dependencies, known uncertainties and parked scope. It **excludes** Agent A's PRs/heads, chosen algorithm, implementation diffs, test results, current checklists, stage-2 currentness and suggested fix order. The chosen Golden Stage 1 file was copied byte-for-byte from the protected prompt and was checked not to contain contemporary Agent A PR identifiers.

The distinction is architectural: B must reconstruct what to build from **original consumers**, not deduce "the right answer" by seeing what A already wrote. Providing a list of fields alone is too weak: the Runner must independently inspect alias conflicts, inherited context, branch/occurrence identity, geometry and CSV semantics.

### Step S5 — Make the output falsifiable rather than a generic summary

The three Q1/Q2/Q3 challenges were chosen so a fluent but non-source-grounded agent cannot pass by repeating Owner vocabulary:

- **Q1 (source authority):** identify actual matching/hierarchy/CSV functions at the frozen baseline, with path/symbol references and falsifiers;
- **Q2 (consumer semantics):** show how a naive `DTXR/SPREF/*SUP*` whitelist can lose dynamic aliases, free-text support attachments, global node fallback, geometry inheritance or ambiguous component evidence;
- **Q3 (real acceptance):** distinguish complete source corpus, positive matched XML engineering records, true negatives, both complete CSV byte streams, stale-config/source rejection and a real served Build/download.

Require **two materially different designs** and a reasoned choice, bounded V3.x semantic workplan, explicit unknowns, high/medium ROI and parked work. The Stage 1 plan is not permission to implement or alter the existing programme graph.

### Step S6 — Freeze response bytes and separate publication from authority

The actual relay prompt directs B to produce `Common/relay/AGENT_A_LFJ_20261009/STAGE1_RUNNER_B_RESPONSE.md` via a controller-mediated publisher, keeping the protected prompt unchanged. The controller must hash the independent-plan region, read the committed bytes back and retain an immutable response ref; content integrity is **not** proof of independent context isolation.

The Owner's target around 70% context-life consumed has no measured token denominator in this incident. I therefore recorded `CONTEXT_CONSUMPTION_ESTIMATE=UNKNOWN`, and the actual succession request is `OWNER_EXPLICIT_SUCCESSION_REQUEST`, not invented 70% telemetry. `TIME_FOR_RUNNER_REQUESTED` stays inside the existing `TASK_EVIDENCE` family and does not transfer permission.

## 3. HOW I developed Stage 2 — independent-plan-first reality reconciliation

### Step T1 — Treat Stage 1 as immutable input, not a draft to overwrite

Stage 2 begins with a **controller-attested frozen Stage 1**: independent-plan SHA-256, Git readback, allowed input-manifest digest, actual read isolation and explicit Owner/Controller Stage 2 authorization. If this is missing, the Stage 2 prompt stops at `HOLD`. It does not "let B catch up" by disclosing A's work early. A plan written after the reveal can be valuable but is no longer a valid independently blind Stage 1 plan.

### Step T2 — Reveal real predecessor work ONLY after that gate

I separated the future Stage 2 prompt from its evidence packet. The real Agent A recovery work is described in [`STAGE2_AGENT_A_REALITY_PACKET.md`](STAGE2_AGENT_A_REALITY_PACKET.md): source-only exploratory #1148 → #1149 → #1150 → #1151 PRs, actual historical tests, previous RED-to-GREEN, R13 product authority and missing real user journey. This packet is historically accurate only for the described observation time. B must re-fetch live **main**, each exact PR base/head, source diffs, real Actions job-step outcomes and current programme dependencies; the packet is not a magic status oracle.

I intentionally exposed the **contradictions** B must reconcile:
- Counts match yet global fallback node identities differed.
- A safety guard created an Error but did not throw (fail-open).
- Real original XML/JSON combinations returned zero positive matches while CSV hashes agreed.
- Some earlier native Chromium work was GREEN, while a later candidate's Actions jobs failed before checkout; infrastructure `NOT_RUN` is neither semantic RED nor GREEN.
- A published original-source package can have a manifest metadata defect; SHA/blob source identity and successful actual ZIP verifier are separate checks.

No Stage 2 requirement instructs B to adopt A's branch slicing, pages, reader API or PR ordering. Those are **hypotheses to confirm, simplify, replace or reject**.

### Step T3 — Demand an explicit hypothesis-to-evidence delta

The critical artifact is the B-frozen plan versus observed reality table:
`STAGE1_HYPOTHESIS → LIVE_FINDING → VERIFIED_SOURCE → CONFIRMED | DISPROVED | UNKNOWN | MISSCOPED | UNNECESSARY | EVIDENCE_STALE → PLAN_CHANGE`.

Each conclusion must identify original Owner constraint, exact source/head/candidate, actual positive and negative oracle, write ownership and downstream effects. Labels such as "almost complete" or "tests passed" without exact basis are insufficient.

This gives an objective reason to **absorb high-ROI work already correctly done**, prioritize high-ROI gaps, park Medium-ROI opportunities with triggers, and discard needless patchwork without creating duplicate responsibilities or unsupported programme progress.

### Step T4 — Keep planning and exclusive execution promotion separate

Runner B may create a **reconciled plan revision** on a separately authorized planning surface after Stage 2. It cannot execute production or rewrite A's branch because a GitHub file says so. The real controller must revoke/fence A's write lease and any in-flight operations, verify source path/epoch ownership, then grant and read back a new B execution epoch. If those facts are unavailable, `PROMOTION=NOT_VERIFIED`. One continuing responsibility remains one responsibility across sequential A/B/C agents, and V3.2 output titles/P/E remain projector-derived from facts.

## 4. WHAT makes these prompts robust — hard requirements and failure if missing

| Robustness requirement | Stage 1 requirement | Stage 2 requirement | Concrete failure/falsifier |
| --- | --- | --- | --- |
| **Exact role/authority** | B is `RUNNER_PREPARING`; no code/merge/lease | B is `READ_RECONCILE_ONLY` pending explicit promotion | A request or a PR interpreted as B execution permission |
| **Source-grade provenance** | Immutable original baseline, Owner quotes/source grade, original fixture hashes | Exact live branches, commits, GitHub jobs and readback; identify source vs claim | Current PR summary copied into original-era hypothesis |
| **Strict information firewall** | Only pinned snapshot/source/fixtures, no A work/current PR metadata | Requires Stage 1 plan freeze and separate reveal approval | B reads #1147 predecessor checkpoint first |
| **Question/falsifier design** | Q1/Q2/Q3 real symbols and alternative designs | Diff each Q against current domain code and real tests | Fluent generic plan with no actual file/function evidence |
| **Consumer correctness** | Field aliases, branch provenance, source identity, original XML and both CSVs | All status/evidence/CSV bytes against true original plus genuine browser | Equal 103-byte Evidence Tree header-only CSV called match success |
| **Negative/adversarial cases** | Invalid, duplicate/ambiguous, stale, unmapped, source hierarchy limits | Regression at latest exact candidate, fail-closed, old-head evidence not transferred | Red guard, global node misnumbering, changed-config HEAD accepted |
| **Measurable output** | Frozen independent plan, two architectures, bounded units, source refs and ROI | Reconciliation table, actual qualified/evidence-debt frontier and revised plan | Percentages awarded for notes, PRs, screenshots or tests |
| **Honest telemetry** | 70% is an estimate only with evidence, else `UNKNOWN` | Re-evaluate runtime/CI/current source drift with observed grades | Invented context usage or inferred CI pass |
| **Original-input authenticity** | 733KB/10MB true fixture identities; pairing unresolved | Original goldens, actual source-backed resolved XML and real Browser builds | Generated 30MB claimed as Owner-authentic |
| **Explicit ROI and parking** | Pending/high/medium/parked outside scope | Absorb proven high, record new medium with revisit trigger | Work quietly dropped or reintroduced as extra leaf |
| **Controller-enforced custody** | Restricted read mount + response-only publisher | Readback freeze → Stage 2 reveal → A revoked → B exclusive epoch | Merely typing `I promise not to read` counted as a sandbox |
| **No self-certification** | File SHA alone is data integrity, not isolation | Plan publication ≠ production lease; issue title ≠ proof | A submitted digest described as cryptographic control of tools |

### Health calibration — workable, never counterfeit

- Track **estimated context consumption** separately from the seven V3.2 engineering-delivery-health components (materialization/evidence/checkpoint distance/size/base drift/interruptions/liveness).
- Trigger `TIME_FOR_RUNNER_REQUESTED` around **70% of a conservative usable window consumed**, or earlier when verified context recall/continuation reliability degrades. Without access to actual effective-context usage, report `UNKNOWN`.
- An explicit Owner succession request may trigger Stage 1 preparation at any point; it **does not** imply that the agent reached the estimated threshold.
- Stage 1 can run while A continues, but never grant B the same material writer simultaneously.
- No periodic heartbeat or new fifth publication family; use `TASK_EVIDENCE` only when semantic evidence or a handover checkpoint warrants it.

## 5. The actual observed lesson: research completed is not a clean blind pass

An earlier prospective Runner was shown [#1152](https://github.com/reallaksh19/3D_Converters/issues/1152) and subsequently [Agent A's Stage 2-only #1147 checkpoint](https://github.com/reallaksh19/3D_Converters/issues/1147#issuecomment-6080011972) before completing independent reconstruction. It correctly identified that context as contaminated. See [`OBSERVED_NEGATIVE_STAGE1_CONTAMINATION.md`](OBSERVED_NEGATIVE_STAGE1_CONTAMINATION.md).

Two other Common source-grounded Runner studies [V3.5 R14](https://github.com/reallaksh19/Common/tree/main/relay/runner-v35-stage1-chatgpt-20261009) and [Common #733 Buddy Runner](https://github.com/reallaksh19/Common/tree/main/relay/BUDDY_RUNNER/CHATGPT_COMMON_733) showed that useful architecture/plan artifacts can be prepared while honestly declaring incomplete isolation. **A provisional engineering reconstruction may be useful, but it must not be labeled a certified blind Stage 1.** Content quality, context isolation, byte-level plan sealing and exclusive execution promotion are separate verdicts.

For this LFJ case a fixture-preparer later published historical-source package `3D_Converters@838a1f1c545ced21d19cfa049bcffb4b7329a3ac`. A subsequent source metadata check found a `SKILL.md` size mismatch (31,386 manifest vs 31,395 actual Git blob). Its 98-file layout and original blob identities could be useful as inputs, but **actual extracted-archive `verify_package.py` success was not independently established at that check**. Do not claim this package provides an already successful fresh Runner B test.

## 6. Practical reproducible operator sequence

1. **PIN:** Freeze Owner intent, original application and protocol SHA, allowlisted source/fixture files and authentic source hashes. Record exactly what is known and UNKNOWN.
2. **ISOLATE:** For certified Stage 1, launch a **new** model context with a genuinely restricted read-only snapshot, no current PR/branch/Stage 2 data and no access to A's prior conversation; B must not have general GitHub write or search.
3. **RECONSTRUCT:** Run only `GOLDEN_STAGE1_RUNNER_B_PROMPT.md`; B produces original source-grounded Q1/Q2/Q3, alternatives, independent plan, ROI and the read-control declaration.
4. **SEAL:** Controller separately hashes and publishes B's unchanged response at `Common/relay/AGENT_A_LFJ_20261009/STAGE1_RUNNER_B_RESPONSE.md` or the exact authorized immutable surface. Read it back; record real SHA and allowed-input manifest. If not isolated, label provisional/contaminated, not a certified blind freeze.
5. **AUTHORIZE:** Owner/controller confirms independently valid Stage 1 freeze; then release `GOLDEN_STAGE2_RUNNER_B_PROMPT.md` **and** the Stage 2 reality packet. Never put the evaluator answer key or this HOW document in Stage 1.
6. **RECONCILE:** B challenges its frozen plan against live source and verified Agent A work, produces source-grounded plan delta and revisions; records High/Medium ROI and authentic acceptance. Verify all current material at exact heads.
7. **PROMOTE:** Separate exclusive controller action revokes A's write authority, fences in-flight operations and issues B an epoch with readback. Only then can B continue the engineering responsibility.

**Gate verdict for the published artifacts themselves:** the prompts and this explanation are archival draft PR inputs, **not** a claim that steps 2–7 were executed or that source-based live product acceptance passed. The V3.2 production skill, relay operational state, protected Stage 1 prompt and all LFJ application sources remain unchanged by this fixture PR.

## 7. Source traceability (historical vs current)

| Source | How used |
| --- | --- |
| `Common/relay/AGENT_A_LFJ_20261009/STAGE1_RUNNER_B_PROMPT.md` @ `5067aa1b408973102dccb20e684d9de5689af23a` (blob `7504bff62d0e6a495299019e88ee47541443acdb`) | Exact byte-preserved Stage 1 golden |
| `3D_Converters` #1152 (sanitized Owner intent) | Stage 1 original Owner context only |
| `3D_Converters@1205639a43e9ce1589360479d2558678aebcfab7` | Stage 1 immutable baseline module/fixture source |
| `Common@13989969f6b7e432c4f7c1ddfe975449dba53593` | V3.2 recorder, health, DELP/claim-first decomposition and handover boundaries |
| `3D_Converters` #1147, #1104 and Stage 2 packet | Stage 2 only: Agent A's research, current application boundaries, product debt and exact source/CI validation obligations |
| Real research PRs #1148–#1151 and Actions #37915926502 / #37916468898 | Historical verification examples and stale-evidence negatives; Stage 2 must re-observe |
| [Observed contamination fixture](OBSERVED_NEGATIVE_STAGE1_CONTAMINATION.md) | Negative evaluator case, never fed to Runner in Stage 1 |
| `3D_Converters@838a1f1c545ced21d19cfa049bcffb4b7329a3ac` package manifest | Source-package provenance and a metadata-integrity adversarial example, **not a blind Runner B success** |

This explanation is deliberately **about prompt construction** and security/engineering acceptance. It is not the implementation HOW that the Stage 1 runner is barred from seeing.
