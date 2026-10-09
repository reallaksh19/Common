# INDEPENDENT_RECONSTRUCTION_V1

**Fixture:** BR-STAGE1-COMMON-733-V1  
**Case:** Common Engineering Relay V3.2; ESC-3 / R-PROJECTION / Common #733; parent Common #718  
**Stage:** 1 of 2 — independently reconstructed from allowed historical evidence  
**Source cutoff:** exact frozen commit 80a9c03d8f33ace129d21cb868c93e9359a8868a (historical simulation baseline, timestamp identified by fixture as 2026-10-08T04:44:06Z)  
**Authority:** analysis and issue-ready implementation-plan DRAFT only; no source-write, issue/PR, takeover, or merge authorization  
**Evidence integrity:** retrospective source-grounded simulation; **not** authenticated Agent 1 history, actual 70%-life event, or accepted TASK_EVIDENCE. This report deliberately does not use later source, live issue/PR/CI, Agent 1 code, or the sealed evaluator oracle.

## 1. Cutoff, inspected manifest and exact source/function evidence

The source basis was read directly by immutable GitHub file ref at the commit above (equivalent to a pinned read-only source checkout for the inspected paths). A full local working-tree checkout and execution were not performed; nothing here implies a runtime test result. Original Stage 1 input BR-STAGE1-COMMON-733-v1.md was previously read and not modified.

| Key | Inspected allowed source at frozen commit | Historical Git blob SHA | Source anchors used |
| --- | --- | --- | --- |
| S1 | skills/engineering-pr-delivery-v3.2/SKILL.md | c6cbe524915281760b516660d4330ba0f51d44b4 | L11-35 recorder/authorities; L208-242 DELP and decomposed claim contract; L244-262 checkpoint |
| S2 | skills/engineering-pr-delivery-v3.2/operating-model/durable-execution-lineage-projection-v32.md | 26954c342377001faaf2d1607bcba97f63706518 | L5-56 facts/authority; L58-112 graph/evidence/title; L129-161 CAS/admission; L163-207 materialization/frontier; L351-412 invariants |
| S3 | skills/engineering-pr-delivery-v3.2/scripts/delp_projection_v32.py | d1f71b18733d9ffc833e91b12cd0792d3ad2bed2 | validate_facts L520 onward; validate_graph L1330; compute_leaf L2695-3045; partition_ledger L3164-3199; project L3202-3449; expected_titles L3492-3498; frontier L3857-3973; GitHubStore L4334-4383 |
| S4 | skills/engineering-pr-delivery-v3.2/scripts/continuity_projection.py | 39fe2747acf04fb4c1f42fa2ed105740d81ac455 | _derived_evidenced L48-54; normalize_units L57-92; reproject L120-127; markdown L399-445; sync_github L574-665 |
| S5 | skills/engineering-pr-delivery-v3.2/scripts/handover_context.py | 083d74723a2345a583c7969c493b87075793caeb | validate_visibility L102-145; _successor_entry L150-220; build_context L397-490; build_request L568-636 |
| S6 | .github/v32-evidence-spine/718-proposal-v2.json | f4055eb0e8d47e87c59cbd0ccf0b4ce56654a5d3 | ESC-3 at L23; R-PROJECTION at L167-207; release digest L382; #733 bound node L507-556 |

Reference root for every anchor: https://github.com/reallaksh19/Common/blob/80a9c03d8f33ace129d21cb868c93e9359a8868a/ . For example, S3:L3202 means this root followed by skills/engineering-pr-delivery-v3.2/scripts/delp_projection_v32.py#L3202. Line coordinates refer to the retrieved frozen UTF-8 files, not current main.

**Explicit absence check at the frozen commit:** both proposed future files, scripts/pr_responsibility_view_v32.py and tests/test_continuity_v32_cross_surface_view.py within skills/engineering-pr-delivery-v3.2, returned NOT_FOUND (404) at the frozen ref. Their implementation and test outcomes are therefore UNKNOWN/ABSENT at this cutoff; their filenames in S6 are proposed write surfaces, not observed features. The sealed .github/v32-evidence-spine/718-golden-fixtures-v1.json was **not** opened. Its existence/blob ID and restricted acceptance interface are known solely from the released Stage 1 prompt.

## 2. Original Owner contract, verbatim references and falsifiable interpretation

The archived original Owner request from the Stage 1 input, preserving wording and spelling:

> now think of v3.2 only, do you see a common integration point Issue score board vs PR title... Same way issue readmap/status update.... same way... parent issue decompostion vs task evidance vs issue scroboard vs new concept or PR titlevs handover prompt vs agent matrix.. Think one by one in, not hurry like chatbot bit... this is engineering

Owner correction OI-718-03, verbatim from the authorized Stage 1 packet:

> full of stats...
> i dont see any integration on github issue decompostion, issue title scorboard, task evidence, handover prompt and agent metric which is the core...
> i also don't see smart title in issue and draft... I also donot see "My intent" or"Wowner inent" presenvation i parent issue along with source links and golden fixtures which is mandatory.

Owner demand OI-718-04, verbatim:

> update git hub issue... walk the talk,  i.e, show how your implemented cycle will show in issue/OR/task evidence etc.... ensure that stress check achieves the same ie, self run via module once coded and achive same...

**Provenance limit:** these are quotations recorded in the authorized fixture as archived on Common #718. An independently authenticated original ChatGPT message permalink and its original timestamp remain UNKNOWN; no new source URL or Owner approval is invented.

**Actual requested behavior:** one coherent, recomputable chain from preserved human Owner intent and source-linked accepted obligations, through decomposed leaf identity and candidate-bound task evidence, to truthful child/parent issue views, a separately qualified PR read view and later successor/agent consumers. Titles and status are representations of the same accepted data, **not** new claims. The Owner wants observable, exercised end-to-end behavior, not prettier statistics or unrelated green tests.

**Falsifiable ESC-3 slice:** (a) the parent and #733 child agree on lineage, accepted obligations, evidence and next frontier for a single input digest; (b) a PR view names its own material and delivery/review/verification gap, never claims responsibility completion solely from green CI, merged state, or a smart title; (c) stale input or conflicting provider updates produce detectable divergence, trigger fresh derivation and preserve Owner-authored intent/human narrative. Each claim must be rejectable by negative tests on actual projection code. Owner-intent envelope custody remains upstream; ESC-3 must carry immutable source references without attempting to own/change the Owner text.

## 3. Parent/leaf/claim identity, graph dependencies and parked boundaries

**Observed in S6:** programme COMMON-718-V32-EVIDENCE-SPINE, root Common#718, repository reallaksh19/Common, base_ref main, total programme weight 100, proposal-v2 release digest sha256:f86b7caf62dfbea4df9b1e342a6c306fd0abe708a973d84f75df8c0fbf27c3bd. Both decomposition policy and claim-first mode are ENFORCED (S6 programme block). The proposed responsibility R-PROJECTION is PRODUCT, owns only semantic claim ESC-3 (claim weight 20), and is provider-bound to existing Common#733. No replacement issue or new responsibility should be created.

The released leaf's semantic units are **VIEW-CONSISTENCY (34), VIEW-PR (33), VIEW-DRIFT (33)**, totalling its own unit denominator 100, with no unit above 40%. #733's programme weight is 20; percentages across those distinct denominators must never be equated. Its declared target/hard budget is 450/1000 changed lines and 15/20 minutes per bounded effort; actual sizing requires source reconciliation before any authorized implementation. Its proposed write surfaces in S6 are exactly S3, new pr_responsibility_view_v32.py, and new test_continuity_v32_cross_surface_view.py.

**Dependencies:** R-BASIS / Common#720 (ESC-1; contract/proposal identity and bindings) and R-PROOF / Common#724 (ESC-2; exact-candidate qualification). Stage 1 does not assert those neighbors are completed, merged, or verified. Their **interfaces** are required; their current state is withheld. Consumer boundaries are R-RECONSTRUCTION / ESC-4 (successor context), R-QUALITY / ESC-5 (advisory agent observations), and G-REPLAY / ESC-6 (joined-live delivery gate); these are not additional duties assigned to #733.

**Non-progress actions:** graph binding, PR opening, UI/status publication, title edits, test counts, a merge, publication volume and executor handover earn zero P/E by themselves (S1:L208-242; S2:L82-96). Scope change, claim reallocation, denominator change, and approval remain programme/Owner matters via authorized plan updates, not inferred from Stage 1.

## 4. Independent source-to-consumer reconstruction: OBSERVED, INFERRED, UNKNOWN

### 4.1 Baseline data-flow hypothesis

1. **Owner / graph authority — OBSERVED.** S1:L11-35 separates Owner/programme authority, material truth and disposable projections. S6 declares claim-first acceptance claims and a released proposal digest with child bindings. S3 validate_graph L1330 and proposal/decomposition functions L998-2294 read/validate this plan; planning denominators and dependencies are graph-defined, not title-defined.
2. **Leaf evidence admission — OBSERVED.** S2:L26-56 specifies CHECKPOINT_FACTS_V1 inside existing TASK_EVIDENCE. S3 validate_facts L520 onward rejects agent-authored projections; partition_ledger L3164-3199 rejects untrusted/misaddressed records and orders accepted facts. S3 compute_leaf L2695-2815 computes unit claims against the declared unit contract; material head, evidence refs, verification result and optional contract digest govern E.
3. **Provider/material observer — OBSERVED.** S3 observe_github L4253-4283 reads primary PR head and state or branch candidate, plus base; GitHub transport L4286-4331 is a thin provider interface. The observer does not prove that required tests actually ran, which belongs to ESC-2.
4. **Deterministic read projection — OBSERVED.** S3 project L3202-3449 builds leaves, recomputes weighted ancestors L3323-3393 and attaches identity/lineage/material/title prefix L3395-3449; one input_digest covers graph, ledger and observations. Expected issue titles derive from one public projection and separately preserved base text (S3:L3466-3498).
5. **Issue publication — OBSERVED.** S3 status_document L4027-4053 creates managed LIVE_STATUS_V1; sync_projection L4154-4178 processes leaves before root. GitHubStore L4334-4383 performs version/digest readback and detect/retry. S2:L129-133 warns GitHub updates are not atomic conditional transactions; title/comment observations can transiently disagree.
6. **Responsibility current-view compatibility — OBSERVED.** S4:L48-127 supports legacy snapshots and DERIVED_FROM_FACTS re-projection. S4:L399-445 emits FURTHER_TASK_SNAPSHOT; S4:L634-641 deliberately leaves issue-title ownership to DELP in derived mode, avoiding competing writers. This snapshot is a separate continuity representation, not the same as DELP root rollup.
7. **Handover consumer — OBSERVED, separate pipeline.** S3 frontier L3857-3973 derives input digests/currentness from graph, accepted facts, dependencies and provider observation and marks changed inputs. S5 build_context L397-490 combines snapshot/reconciliation materials; validate_visibility L102-145 protects blind-vs-reality boundaries, and build_request L568-636 is an explicit, separate reasoning request. No automatic injection of the ESC-3 PR view into S5 was established by the inspected paths.
8. **PR-specific ESC-3 read view — ABSENT/UNKNOWN.** S3 currently uses PRs as material **inputs** and in child issue title paths, but its observed provider write target is an ISSUE and LIVE_STATUS comment, not a distinct PR qualification read model. At the frozen ref, the proposed adapter file and specified cross-surface test file do not exist. Therefore source inspection does not establish that PR titles, PR descriptions or PR comments are already synchronized with the issue projection.
9. **Agent matrix and downstream joint replay — NOT INSPECTED/UNKNOWN.** S6 assigns ESC-5/ESC-6 separately. No claim that advisory agent metrics or joined E2E tests operate through this ESC-3 projection is justified by our read set.

### 4.2 Required joining invariant (independent inference)

Introduce one immutable **CrossSurfaceBasis** created per logical projection attempt: programme ID; released proposal/graph digest; responsibility ID and leaf ref; parent lineage; accepted fact set digest; provider observation generation and candidate SHA/PR state; ESC-2 qualification-basis reference/status (when actually supplied); root projection input digest; and derived next frontier. Then project **IssueLeafView**, **IssueParentView** and **PrResponsibilityView** from that same basis. Each view declares basis_digest plus its own view_kind, source_status and freshness; all values are recomputable. This is **INFERRED proposed architecture**, not a pre-existing schema or an observed implementation. Never treat a caller-supplied PR title/body as a fact source.

Unknowns that must stay unknown: external Owner-message authenticity; ESC-2 actual qualification interface/schema and completed implementation; exact PR provider surface authorized for publication; whether any permitted code outside the inspected modules already implements a partial PR adapter; the sealed evaluator's precise expected output strings; Agent 1's decisions and present state.

## 5. Failure models and source-grounded falsifiable hypotheses

| ID | Failure hypothesis | Why plausible at baseline | Rejecting observation |
| --- | --- | --- | --- |
| F1 | Child and parent show different accepted epochs after a push or facts update | S3 project is internally coherent but GitHubStore writes separate issue surfaces sequentially (S3:L4154-4178) | A stale view is marked stale or blocked until same-basis readback; NEVER silently labeled reconciled |
| F2 | A PR green/merged title is mistaken for responsibility completion | S3 observe_github reads provider lifecycle; ESC-2 is separate | PR read view says delivery/verification UNKNOWN or GAP until candidate-bound required evidence qualifies |
| F3 | Reusing leaf P/E as PR lifecycle is false | S2:L82-96 distinguishes P/E from D/DE and candidate/gates | PR fields separately show draft/open/merged and qualification basis, not R:P/E as PR authority |
| F4 | An old candidate's passing evidence is carried to a new head | S3 compute_leaf L2778-2792 candidate check | Changed SHA leaves P untouched and lowers/invalidates evidence E as appropriate; PR qualification not current |
| F5 | Provider race silently overwrites human or newer machine state | S3 GitHubStore L4334-4383 has detect/retry, not atomic CAS | stale read/write triggers conflict, new input read, bounded retry, no fabricated synchronized state |
| F6 | Owner narrative/accepted plan is overwritten by status formatter | S3 split_title L3101-3145 is title-specific, not an Owner-body authority layer | Managed delimiters updated only; verbatim intent and human base preserved and separately read back |
| F7 | Missing facts or missing required tests gets shown as zero/done | S2:L163-183 UNMATERIALIZED; ESC-2 holds test coverage | expose UNKNOWN/UNMATERIALIZED/NOT_RUN and named gaps, not an authoritative zero or "passed" |
| F8 | A visually correct view is produced from a wrong proposal binding | S6 released digest/bindings, S3 validates graph | wrong claim owner/digest/leaf ref refused or visibly UNRESOLVED |
| F9 | Identical human-readable titles hide changed accepted inputs | S3 input_digest L3439-3448 and frontier drift L3932-3973 | cross-surface digest/currentness comparison detects changed basis despite unchanged display |
| F10 | A test passes without calling the production projector/publisher | S6 acceptance is semantic, not test-count-based | instrumentation/spy records real calls and provider readback on both negative and clean executions |

Limit of claim: S2:L404-412 expressly states DELP cannot validate the truth of an evidence reference or prevent all GitHub edits. The PR adapter must not improve its apparent status by assuming what ESC-2 has not qualified.

## 6. Genuine architectural alternatives and selection

**A — Three independent surface formatters with a shared metadata contract.** Issue projector keeps parent/child numbers; a PR renderer separately reads issue status, and handover retrieves both by reference. Advantages: minimally invasive short-term changes, easy UI customization. Risks: each formatter has its own temporal read, creates dual derivations, may accidentally interpret an issue-title percentage as PR proof, and cannot guarantee compatible basis on a moved head. A common field name alone is not enough. **Not selected.**

**B — One immutable semantic projection, typed view adapters and guarded provider publishers.** Reuse S3's validated graph/facts/material projector as the authoritative **derived read basis**. Extend or add a pure join layer exposing normalized CrossSurfaceBasis, parent/child and separate PR read view; a PR adapter maps material stage and ESC-2 qualification without rewriting acceptance truth. Publish issue LIVE_STATUS and PR managed read surfaces from the same basis digest, with per-surface version, readback, freshness verification and retry/invalidation. Advantages: one explanation for every displayed fact; testable pure transformations, direct reuse of current issue projection and evidence-staleness rules; least possible intrusion into neighbor ownership. Risks: provider is eventually consistent, a missing ESC-2 contract must fail closed, and an overly broad shared model might couple unrelated surfaces. Mitigate with small typed adapters and explicit UNKNOWN. **SELECTED.**

**C — New canonical event ledger driving all issues, PRs, handover and agent metrics.** Advantages: potential replayability and transactional record model. Risks: a second source of truth, schema migration, displaced fact/authority boundaries, far larger write/deployment surface, and accidental ownership of ESC-4/5/6. **Park for a separately approved architectural programme; not selected.**

**Important trade-off:** "one input basis" means all rendered payloads carry the same identity/generation and can be compared; it does **not** assert GitHub issues and PRs update atomically. Where concurrent writes defeat reliable readback, the adapter must expose MIXED_BASIS/RECONCILE or abort publication. No single global CAS guarantee is claimed.

## 7. Independent draft IMPLEMENTATION_PLAN / further-activity workpack

**Status: DRAFT only.** Existing responsibility Common#733 must own this plan after authorization, subject to its released claim and program gate; no duplicate issue or mutation of graph. Proposed future write surfaces are limited to S6's three named files; any schema change or additional file must be explicitly reconciled with the released contract, freeze allowlist and owner/dependency constraints first.

### Pre-work (read-only, earns zero units)

- Reconfirm at an authorized future implementation boundary that the exact accepted S6 release/claim binding remains applicable; read R-BASIS and R-PROOF **interfaces and accepted artifacts**, not their unverified headline status. Stop on absent/stale release, mismatched repository, unqualified ESC-2 input, or conflicting allowed write authority.
- Identify production callers of S3 project, status_document, sync_projection, GitHubStore, expected_titles, S4 derived Further Task, and S5 handover only to define interface compatibility. Inspect prospective schema/test consumers before changing a signature. Freeze explicit input/output schema contract, absent-value rules and PR association cardinality.
- Run source-level baseline test selection and a no-write demonstration through production pure functions. Record exact test discovery and candidate head when authorized; there is **no Stage 1 execution/result claim**.

### U1 / VIEW-CONSISTENCY — semantic weight 34

Outcome: compatible parent+child issue read models expose one claim/responsibility/lineage contract, qualified facts, provider candidate, and active frontier on a common input digest.

Implementation sketch: add pure CrossSurfaceBasis normalization around S3 project output; expose child/ancestor views with shared basis digest and **scope-distinguished** R:P/E and parent Π:D/E, not duplicated calculations. Respect ENFORCED claim release, unknown material, unreleasable dependency and UNMATERIALIZED lower-bound semantics. Keep Owner intent as immutable link/verbatim-custody reference, never regenerated text. Add deterministic, cross-node, wrong-parent and moved-source unit tests in the new cross-surface test file.

Acceptance: child #733 and root #718 from identical facts/observations share the basis; weighted parent values agree with S3 and differ appropriately from child percent; changed fact/plan/candidate invalidates stale basis; missing facts cannot assert completion; stable rerender has same canonical output.

### U2 / VIEW-PR — semantic weight 33

Outcome: an associated PR has its own explicit material state and delivery/qualification gap while identifying the responsibility and common basis.

Implementation sketch: add pure scripts/pr_responsibility_view_v32.py. Input is the trusted CrossSurfaceBasis plus a typed material observation and a separately accepted ESC-2 qualification descriptor (if available). Output separates **PR state** (draft/open/closed/merged, candidate SHA), **review/verification** (known required gates, observed/not-run/qualified/stale/unknown), **responsibility link** (issue #733, ESC-3), and **rendering provenance** (basis_digest). Unknown ESC-2 coverage must stay UNKNOWN; no green-from-green inference. Prefer a bounded managed PR comment/read model; a smart PR title is a derived optional projection with its own safe grammar and human base, **not** a responsibility percentage or accepted merge criterion. Exact PR surface and title policy are an outstanding WHAT question, not authorization to edit either.

Acceptance: green unrelated CI plus omitted required verification does not qualify the PR; merged with missing deliverable remains unqualified; new SHA invalidates qualification; draft/open transitions affect PR state but not leaf P; stable semantic inputs produce stable PR read view. A missing/ambiguous PR association fails closed.

### U3 / VIEW-DRIFT — semantic weight 33

Outcome: parent, child and PR updates are self-consistent or conspicuously stale under mutation, provider failure and races; user-authored content survives.

Implementation sketch: reuse S3 _InputCache/invalidation, frontier_drift and compare-and-retry pattern. Attach schema/version/basis_digest to all surface read models; compare expected-vs-readback digest and candidate generation before and after publication. Treat changing graph, provider head, accepted facts and ESC-2 qualifier as reasons to re-derive. Enforce one issue title writer (S4 derived mode already cedes it); never replace Owner-owned issue description, plan text, golden links or PR human description. Managed comments may only replace bounded marker regions. A repeated conflict produces an explicit stale/conflict result, not a successful sync. Add fake-transport race, duplicate-managed-comment and Owner-content preservation tests.

Acceptance: pre-write mutated SHA and post-write race both cannot be reported as same-basis success; readback proves expected payload; rerun is idempotent; provider unavailable causes no false zero or false qualification; human sections byte-for-byte preserved.

### Implementation/verification protocol

Work units follow U1 → U2 → U3 as a serial bounded sequence on #733, though isolated tests may be prepared independently. S6 proposes **target 450 / hard 1000 changed lines and target 15 / hard 20 minutes**; these are execution constraints from the frozen contract, not a prediction that work is complete within a session. Under actual scope, split oversized activity into internal checkpoints without adding or reweighting semantic units. Restrict changes to the released write surfaces; require Owner/Coordinator plan update before changing scope or overlapping another responsibility's write surface. For each unit: write RED assertion, exercise real production function/adapter, implement smallest change, rerun positive+negative+clean controls, inspect diff/source and benchmark no-op projection determinism, publish candidate-bound TASK_EVIDENCE with actual discovered tests and negative knowledge. Unrelated CI success is not qualification.

**Future acceptance matrix (must be independently exercised after authorization):** pure projection tests; fake-provider end-to-end materialization of parent+child+PR; race/failure tests; real GitHub dry-run with repository guard, then managed provider writes/readback only after permission and approved surface policy; browser-visible readback via actual issue/PR views when required by Owner; exact-head regression and dependency qualification for ESC-1/ESC-2. Required full ESC-6 joined replay remains a downstream gate, never auto-credited to ESC-3.

**Next safe action after this Stage 1 seal:** operator freezes this plan's bytes/input manifest; in Stage 2 reveal only authorized Agent 1 facts and separately reconcile this independent design with exact current responsibility contract, source/diff and material qualification before allowing any engineering work. Until then: STOP.

## 8. Positive, negative, stale-input, missing-evidence and clean-control test design

The printed golden interface names GF-SMART-SURFACES, GF-PR-HEAD and GF-PUBLISH-RACE under ESC-3; its expected outputs remain sealed. Proposed tests below are independently designed, **not** assertions that these pass or that sealed oracle fields were read.

| Test | Controlled input / action | Required observable oracle |
| --- | --- | --- |
| T01 clean fixed-basis | Valid #718/#733 graph; accepted #733 facts; same SHA/qualifier | Parent/child/PR share digest, valid typed views, no drift |
| T02 repeat clean | Recompute and republish unchanged data | Bit-stable pure output; provider no-op, unchanged human text |
| T03 parent rollup | Add independently qualified predecessor/another leaf with known weights | Root D/E recomputed by exact graph weights, not copied from #733 P/E |
| T04 wrong binding | Claim, contract digest, repository or leaf association swapped | Rejected/UNRESOLVED; no invented owner/success |
| T05 projected fact injection | Agent facts contain title/percent/parent P/E | validate_facts rejects whole record; no number/title altered |
| T06 missing ledger | PR exists but accepted facts empty | UNMATERIALIZED/lower-bound/MATERIALIZE_FACTS, not P0 as authoritative complete picture |
| T07 missing verification | Required check unobserved; unrelated CI green | PR qualification NOT_RUN/UNKNOWN; associated obligation not complete |
| T08 green-but-omitted | Required deliverable absent despite green unrelated tests or merge | Delivery gap shown, no qualification or progress promotion |
| T09 head move | Claim/evidence bound to SHA A; provider moves to B | E and PR qualification stale/unverified; P unchanged; shared basis invalidated |
| T10 plan move | Change released graph, claim ownership or proposal digest | Changed source digest; stale surface requires RECONCILE; no silent reuse |
| T11 PR lifecycle | Same candidate transitions draft → open → merged without new accepted proof | PR material stage changes; responsibility completion and Owner authority do not |
| T12 concurrent writer | Writer A prepares N, writer B changes marker/head before or during A write | Conflict detected, refreshed recompute/retry or explicit failure; never silent last-writer-wins |
| T13 provider outage | Candidate/source or readback unavailable | No false projected progress drop or green; explicit FAILED_OBSERVABILITY/UNKNOWN |
| T14 title/body preservation | Owner/human text contains nontrivial punctuation, source/golden links | Human content preserved verbatim outside generated markers; smart title only in owned prefix |
| T15 no PR / two PRs | Missing PR or ambiguous association | PR view UNKNOWN/AMBIGUOUS, not arbitrarily chosen head |
| T16 cross-surface test integrity | Invoke production projector/adapter with fake transport, track call/readback | Test fails if production adapter skipped or mocks merely replay expected strings |

**Golden boundary:** only fixture names and families above were exposed; exact sealed output tokens, historical PR IDs, expected titles and positive-answer corpus remain Stage 2/independent evaluator questions. Do not tune tests by peeking at sealed oracle.

## 9. Up to three WHAT/WHY questions for healthy striker / Owner

1. For ESC-3, is the intended PR-visible product **a managed read-model comment**, a carefully generated PR-title prefix, or both, and what Owner-visible information must be preserved verbatim in the PR's human narrative? This decides the acceptance surface, not the algorithm.
2. Which **authoritative ESC-2 qualification facts** must be reflected in the PR view (required method coverage, review gate, artifact completeness), and when should the display explicitly say UNKNOWN rather than GAP? This is an input/acceptance contract question, not a request for the incumbent's implementation.
3. What exact Owner-intent/source-link custody surface is required to remain stable for #718 while projected issues/PR titles change, and is cross-surface **eventual consistency with digest/freshness warnings** acceptable given GitHub's lack of atomic multi-surface writes?

No request for Agent 1 methods, code, PR heads, CI, plan, statistics or answer keys is made.

## 10. ROI reconciliation, parking and genuinely new scope

**High ROI within ESC-3:** a single immutable digest across child/parent/PR read models; explicit PR stage vs verification/acceptance separation; stable generated smart-title grammar with human-base custody; a missing-qualifier UNKNOWN state; readback-verified, idempotent provider sync; drift dashboard generated from derived fields only; actual production-path negative tests and source-level assertion that adapter was invoked. These directly strengthen VIEW-CONSISTENCY, VIEW-PR or VIEW-DRIFT without reallocating claims.

**Medium ROI parked (not acceptance blockers):** richer PR visual presentation; UI badge colors or icon polish; larger historical title migration coverage; optional digest-driven dashboard; extra human-friendly comparison summaries; cross-programme reporting beyond #718; performance tuning if profiling later justifies it. None earns units merely by being implemented.

**New-scope proposals requiring a separate Owner/Coordinator decision:** complete ESC-4 handover generation/entry protocol; ESC-5 agent-quality/adjudication framework; ESC-6 full integrated replay/product cutover; new cross-repository event store; verification of external original ChatGPT permalink; an independent immutable GitHub transactional publisher; changes to R-BASIS or R-PROOF semantic contracts. Record as possibilities, do not silently add to #733.

**Unanswered questions:** exact intended PR provider UI and title syntax; missing ESC-2 accepted interface; whether project policy permits extra PR managed-comment schema files; how to expose mixed-generation states during multi-surface publication; which Owner-custody reference is canonical in the historical parent; sealed acceptance strings and runtime behavior not exercised at this stage.

## 11. Explicit forbidden assumptions and authority boundary

- **NOT observed / NOT claimed:** present Common main code, Agent 1 implementation or HOW, current #733 issue body/comments, actual PR or PR head, current CI, mergeability, tests passed, released current plan amendments, current agent health, accepted P/E, current production cutover, or actual handover/takeover.
- **NOT inferred:** tests are valid because CI is green; work is done because a PR merged; Owner approved because a title changed; an absent fact is zero; evidence refs prove their own truth; a fixture simulation is a live event; a GitHub comment is an independently authenticated original ChatGPT link.
- **NOT authorized:** modifying engineering source, adding/changing issues or PRs, editing Owner text/graph/golden fixtures, writing TASK_EVIDENCE, asserting earned units, publishing a smart title, merging, granting custody, releasing Stage 2, or using sealed test outputs in Stage 1.
- **Preserve:** the four actual engineering publication families IMPLEMENTATION_PLAN / PLAN_UPDATE / TASK_EVIDENCE / TASK_RESULT; no fifth status publication as authority. Generated status and titles are caches. An executor replacement does not create a responsibility. Technical review/verification and Owner approval remain separate.
- The *only* permitted publication in this run is this independent reconstruction plus its digest receipt in the designated experiment folder; that publication confers no source-write or delivery authorization.

## 12. Stage 1 sealing receipt, limitations and stop

**STAGE1_PLAN_RECEIPT_DIGEST: PENDING_EXTERNAL_SEAL.** This placeholder is required until the experiment operator's trusted fixture harness seals the actual Markdown with the permitted-input-manifest digest. The companion INDEPENDENT_RECONSTRUCTION_V1.sha256 is a byte-level **file-integrity receipt**, to be generated from the committed Markdown and verified by GitHub readback; it is **not** a substitute for the operator's independent Stage 1 authorization/manifest seal.

**Manifest boundary:** S1–S6 at historical commit 80a9c03d8f33ace129d21cb868c93e9359a8868a plus the explicitly released Stage 1 prompt; proposed PR view/test paths only checked for absence; no golden-oracle contents or other issue/PR/CI/agent facts consumed. Retrospective fixture remains a simulation. Full local checkout, runtime test execution and source of original human chat message remain unverified. External operator must freeze this plan and record both its allowed-input manifest digest and committed-output receipt before Stage 2 disclosures.

**Stage boundary decision:** Stage 1 independent design is prepared for immutable sealing; no permission to pursue U1–U3 and no factual assertion about Agent 1.

STAGE1_READY_FOR_SEAL — awaiting Stage 2 disclosure; runner write authority NONE.
