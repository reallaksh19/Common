# V2.5 object / authority matrix

## Purpose

This is the current authority and producer/consumer map for Engineering Relay V2.5. It is reconciled through the merged completion checkpoint `CP-R010`; historical work-package reports record how individual layers were introduced.

Classification:

```text
AUTHORITY     may define repository engineering truth within its bounded role
EVIDENCE      records observed/evaluated facts but cannot rewrite authority
DERIVED       recomputed projection/predicate; never an editable authority
RUNTIME       depends on the live checkout/external observation
NON_AUTHORITY convenience surface only
```

## Authority hierarchy

```text
OWNER INTENT / ODR                                      AUTHORITY
        ↓
OVERALL ROADMAP / ROADMAP REVISION                     AUTHORITY
        ↓
EXECUTABLE FRONTIER                                    DERIVED
        ↓
SEMANTIC EP / OWNER-APPROVED PARALLEL PLAN             AUTHORITY FOR CURRENT SLICE
        ├── DSTEP-* discovery contract
        ├── QSET-* when qualification is required
        └── quality applicability router
        ↓
BATON_READY                                            DERIVED
        ↓
candidate DISC-* / QUAL-* / TC-*                      EVIDENCE
        ↓
TAKEOVER_CERTIFIED(route,candidate)                    DERIVED
        ↓
live route / Git / drift / continuity                  RUNTIME + EVIDENCE
        ↓
MATERIAL_WRITE_READY(route,candidate,live Git)          RUNTIME DERIVED
        ↓
IMPLEMENTATION
        ↓
QRV-* + TEST / BENCHMARK EVIDENCE                      EVIDENCE
        ↓
CHECKPOINT                                              AUTHORITY FOR EXECUTION HISTORY
        ↓
ROADMAP / PROGRESS / ISSUE RECONCILIATION              AUTHORITY / DERIVED AS DEFINED BELOW
        ↓
EXTERNAL + HUMAN PROJECTIONS                            DERIVED / NON_AUTHORITY
```

Generated Markdown, GitHub state, and chat never override repository authority objects.

## Current matrix after CP-R010

| Object / control | Classification | Producer | Primary consumers / enforcement | Authority boundary |
| --- | --- | --- | --- | --- |
| Owner Decision Record (`ODR-*`) | AUTHORITY | Owner decision capture / roadmap transaction | `validate_owner_decision.py`, roadmap transaction, Owner-change projection | Owner intent/disposition only; cannot replace roadmap topology or execution evidence |
| `ODR.change_intake` | AUTHORITY semantic summary | Owner-intent mutation capture | roadmap revision + Owner-change projection | Before/after intent meaning; structural effects remain roadmap-revision truth |
| `OVERALL_ROADMAP.yaml` | AUTHORITY | roadmap transaction / initialization | frontier, progress, EP admission, issue reconciliation | Objectives/phases/WPs/dependencies/lifecycle state |
| Roadmap revision | AUTHORITY transaction | approved/factual roadmap mutation | continuity, progress basis, issue reconciliation, Owner-change projection | Exact structural mutation and resulting frontier |
| Roadmap continuity receipt | EVIDENCE | continuity reconciliation | EP validity, material authority | Whether an active EP survives intervening revisions |
| Executable frontier | DERIVED | roadmap computation | serial/parallel admission, status, zero-context reconstruction | Must be recomputed; cannot be manually asserted as a competing plan |
| `REPO_STATE.yaml` | AUTHORITY locator + checked mirrors | relay lifecycle/reconciliation | aggregate conformance, route resolution, projections | Deterministic bootstrap locator, lifecycle/routing/state planes; percentage/readiness mirrors are checked, not independent authority |
| `REPO_STATE.relay_protocol` | AUTHORITY binding | bootstrap/admission | repo-state/profile validation | Pins protocol version and non-placeholder Common basis |
| `REPO_PROFILE.yaml` | AUTHORITY repository metadata | repository admission | discovery, EP/takeover digests | Repository discovery/profile facts only |
| Execution Package (`EP`) | AUTHORITY for current slice | outgoing relay owner | semantic EP validator, baton readiness, discovery, qualification, progress/report | One-WP forward contract; may not redefine Owner intent or roadmap topology |
| `DSTEP-*` | AUTHORITY discovery requirement inside EP | EP preparer | incoming `DISC-*` | Exact repository-only questions/outputs candidate must resolve |
| Discovery Receipt (`DISC-*`) | EVIDENCE | incoming candidate | TC validation / takeover certification | Candidate-specific observed discovery; `conversation_context_used` must be false |
| Qualification Question Set (`QSET-*`) | AUTHORITY evaluation criteria | outgoing preparer | candidate + QUAL validator | Fresh Q1–Q5 criteria bound to current route/EP; candidate cannot prepare its own set |
| Qualification Receipt (`QUAL-*`) | EVIDENCE | candidate answers + independent/deterministic evaluator | TC validation | Evaluated engineering understanding on exact QSET/EP basis |
| Takeover Certification (`TC-*`) | EVIDENCE / admission record | independent evaluator / deterministic checks | `TAKEOVER_CERTIFIED`, material write gate | Route/candidate admission only; cannot change EP/roadmap |
| `BATON_READY` | DERIVED | baton-readiness validator | handover readiness, takeover admission | Candidate-independent completeness of repository baton |
| `TAKEOVER_CERTIFIED(route,candidate)` | DERIVED | current DISC/QUAL/TC + baton/basis validation | live write gate | Candidate/route-specific; stale evidence invalidates it |
| `PROJECTION_READY` | DERIVED | projection convergence | handover readiness | Required external projection currentness only |
| `HANDOVER_READY` | DERIVED | `BATON_READY AND PROJECTION_READY` | outgoing custody reporting | Outgoing custody completeness; not write permission |
| `MATERIAL_WRITE_READY(route,candidate,live Git)` | RUNTIME DERIVED | current certification + route/Git/drift/continuity/state planes | operator before engineering writes | Never persisted as a timeless boolean |
| Parallel Plan | AUTHORITY routing contract | Owner-approved parallel transaction | route resolver, lane EP admission | Only explicit approved exception to serial material execution |
| Parallel Join | EVIDENCE + transition custody | lane completion/integration transaction | integration EP, checkpoint linkage | Converges all approved lanes before integration |
| Parallel Replan | AUTHORITY transition transaction | durable replan | old/new plans, successor EPs, route resolver | Freezes superseded topology and transfers unresolved custody exactly |
| Drift Receipt | EVIDENCE | base-drift reconciliation | live material-write gate | Classifies observed base movement; historical receipt cannot authorize a newer observation |
| Live Git observation | RUNTIME FACT | checked-out repository | route/Git inspection, material-write gate | Current branch/worktree/head/base reality |
| `QRV-*` Quality Review | EVIDENCE | applicable quality procedures | checkpoint, report/communication, successor handover | Exact EP/material/router quality evidence; severity alone cannot create a stop |
| `QF-*` finding | EVIDENCE | QRV procedure | quality state, successor transfer | Finding classification/evidence/disposition; blocking only through a valid hard-stop mapping |
| Checkpoint (`CP-*`) | AUTHORITY for backward execution truth | completing agent | successor baton, progress/evidence, issue/roadmap reconciliation | What actually happened on exact material basis; cannot redefine Owner intent |
| `PROGRESS.yaml` / Progress Basis | AUTHORITY calculated accounting | roadmap/acceptance reconciliation | report/status/handover | Acceptance → step → EP → WP → phase → objective → overall; no guessed percentages |
| `ISSUE_GRAPH.yaml` | AUTHORITY repository coordination model | issue reconciliation | GitHub projection operations, closure/supersession validators | Engineering/GitHub coordination model; GitHub UI does not become roadmap authority |
| `GHGEN-*` / `GHOP-*` | AUTHORITY desired external projection transaction | projection planner | publisher/reconciler | Desired GitHub coordination generation/operations, with retry authority only for current generation |
| `GITHUB_OBSERVATION` | EVIDENCE | external readback | GitHub reconciliation | Verified external reality; connector response alone is insufficient |
| Report projection | DERIVED | roadmap/progress/EP/CP/issue/QRV/state | status/handover/communication | Structured derived report only |
| Communication projection | DERIVED | report projection | `TECHNICAL_STATUS.md`, `OWNER_STATUS.md` | One shared human communication source; never writable truth |
| `TECHNICAL_STATUS.md` | NON_AUTHORITY DERIVED VIEW | technical renderer | engineers/agents | Detailed protocol/source view |
| `OWNER_STATUS.md` | NON_AUTHORITY DERIVED VIEW | Owner renderer | Owner | Plain-language current capability/risk/decision/next-work view |
| Owner-change projection / `OWNER_CHANGE.md` | DERIVED / NON_AUTHORITY VIEW | ODR + roadmap revision + current reconciliation | Owner | Change impact only; ODR + roadmap revision remain authority |
| `ZERO_CONTEXT_RECONSTRUCTION` | DERIVED | repository authority objects/current route | release certification, incoming agent | Repository-only reconstruction of material answers; chat is prohibited as custody |
| `cold_start_check.py` | DERIVED diagnostic | repository state | operator / lifecycle tests | Recovery diagnostic, subordinate to semantic baton and candidate certification |
| Declarative schemas | CONTRACT AID | protocol authors | tooling/audit/humans | Shape documentation; procedural/cross-object validators remain enforcement layer |
| Templates | CONTRACT AID | protocol authors | object producers | Canonical authoring shape, not proof of conformance |
| Procedural validators | ENFORCEMENT | protocol implementation | aggregate conformance / focused diagnostics | Semantic and cross-object invariants |
| Scoped CI workflow | EVIDENCE PIPELINE | repository automation | completion checkpoints / PR review | Executes compile, self-consistency audit, root units, dedicated stress suite |
| Chat conversation | NON_AUTHORITY | participants | convenience only | Acceleration, never custody |

## Producer / consumer rules

1. Every durable authority or evidence object has at least one explicit producer and at least one validator/consumer.
2. Derived predicates are recomputed from current authority/evidence and are not persisted as independent authorization claims.
3. Generated reports/views can expose repository truth but cannot resolve conflicts by overriding their sources.
4. External GitHub observations can reconcile coordination state only through the current authorized projection transaction.
5. Runtime Git facts participate in write readiness but cannot be replaced by stale repository assertions.
6. A candidate's DISC/QUAL/TC evidence can admit that candidate; it cannot change the EP, roadmap, or Owner decision.
7. Checkpoints preserve execution/evidence custody; roadmap revisions preserve planning/intent effects. Neither substitutes for the other.

## Source-of-truth rules

1. Owner intent and applied ODRs govern intent changes.
2. Overall Roadmap plus its revision transaction governs engineering plan/topology.
3. EP/Parallel Plan governs only the currently authorized execution slice.
4. `DSTEP-*` defines discovery requirements; DISC records candidate discovery evidence.
5. QSET defines qualification criteria; QUAL records evaluated answers; TC records route/candidate admission evidence.
6. `BATON_READY`, `TAKEOVER_CERTIFIED`, `PROJECTION_READY`, `HANDOVER_READY`, and `MATERIAL_WRITE_READY` are derived predicates with distinct meanings.
7. QRV/test/benchmark evidence and CP record what actually happened without inflating quality findings into stops.
8. `PROGRESS.yaml` is calculated progress authority; report/status percentages are derived.
9. `ISSUE_GRAPH.yaml` is repository coordination truth; GitHub remains an external projection.
10. Report, communication, Owner-change, and ZERO_CONTEXT_RECONSTRUCTION outputs are derived projections.
11. Conversation is never custody.

## Historical completion mapping

The completion program introduced these layers serially: semantic EP (CP-R002), readiness/takeover (CP-R003), qualification (CP-R004), progress/handover (CP-R005), GitHub operations (CP-R006), quality/QRV (CP-R007), human communication (CP-R008), Owner change intake (CP-R009), and zero-context end-to-end certification (CP-R010). WP-10 audits their consistency; WP-11 performs final PR-readiness cleanup.
