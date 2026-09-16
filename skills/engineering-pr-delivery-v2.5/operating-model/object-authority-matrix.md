# V2.5 object / authority matrix

## Purpose

This is the reconciled WP-00 baseline map for the catch-up/completion roadmap. It records the actual kernel objects present on the branch, their authority role, current enforcement, and the revamp action assigned to them. Target objects that do not yet exist remain explicitly marked `ADD`.

Legend:

```text
KEEP        retain current concept and authority role
STRENGTHEN  retain concept but deepen validation/semantics
REPLACE     retire weak current behavior/meaning behind a stronger contract
DEPRECATE   remove as an authority mechanism after its replacement is live
ADD         target object does not yet exist in the kernel
DERIVED     projection only; never authority
```

## Authority hierarchy

```text
OWNER INTENT / ODR
        |
        v
OVERALL ROADMAP
        |
        v
EXECUTABLE FRONTIER
        |
        v
EP / APPROVED PARALLEL PLAN
        |
        +--> BATON semantic validation
        |
        v
candidate discovery / qualification / takeover certification
        |
        v
live route + material basis + write readiness
        |
        v
IMPLEMENTATION
        |
        v
QUALITY REVIEW + TEST/BENCHMARK EVIDENCE
        |
        v
CHECKPOINT
        |
        v
ROADMAP / PROGRESS / ISSUE RECONCILIATION
```

Generated reports and external projections sit downstream of these objects and may not override them.

## Actual kernel + target matrix

| Object / control | Role | Current enforcement / observed gap | Classification | Successor WP |
| --- | --- | --- | --- | --- |
| Owner Decision Record (`ODR`) | Explicit Owner intent/disposition | Dedicated validator; roadmap intent mutations bind to applied ODRs | KEEP | — |
| `OVERALL_ROADMAP.yaml` | Authoritative objectives/phases/WPs/dependencies/state | Roadmap/frontier/transaction validators | KEEP | — |
| Roadmap revision | Immutable mutation receipt | Transaction and continuity validation | KEEP | — |
| Roadmap continuity receipt | Active-EP disposition across revisions | Dedicated validator; WRITE/READ_ONLY reconciliation | KEEP | — |
| Executable frontier | Derived eligible WP set | Deterministically recomputed from roadmap | KEEP / DERIVED | — |
| `REPO_STATE.yaml` | Bootstrap locator, current route/batons/state summaries | Strong lifecycle/routing checks, but protocol binding and several mirrored summaries are not fully reconciled | STRENGTHEN | WP-02 / WP-04 / WP-10 |
| `REPO_STATE.relay_protocol` | Pins relay protocol version/Common basis | Template/bootstrap produce it; current repo-state validator/schema do not validate it | STRENGTHEN | WP-00 finding, implement WP-01/WP-10 |
| `REPO_PROFILE.yaml` | Repository discovery/profile metadata | Bootstrap produces it; schema exists; no dedicated validator or aggregate-conformance check | STRENGTHEN | WP-01 |
| Execution Package (`EP`) | One-WP forward executable contract | Current validators enforce shape/context/anchors more strongly than semantic input/benchmark/discovery/plan content | STRENGTHEN | WP-01 |
| EP repository-discovery step | Executable discovery instruction | Present as free-form-ish step rows; current IDs use `DISC-*` | STRENGTHEN and rename step namespace to `DSTEP-*` | WP-01 |
| Discovery Receipt (`DISC-*`) | Candidate's durable discovery result | Not implemented; namespace reserved for receipt, distinct from `DSTEP-*` | ADD | WP-02 |
| Parallel Plan | Owner-approved multi-WP router | Dedicated validator; exact frontier/lane isolation/approval rules | KEEP | — |
| Parallel Join Receipt | Multi-parent convergence baton | Dedicated convergence validator | KEEP | — |
| Parallel Replan Receipt | Retire invalid topology + preserve/transfer custody | Dedicated validator + history checks | KEEP | — |
| Drift Receipt | Base-movement classification | Dedicated validator; live Git observation is intentionally separate | KEEP | — |
| Git observation / route resolution | Live branch/worktree/material/base facts | Runtime scripts; static conformance deliberately cannot prove checkout | KEEP | — |
| Checkpoint (`CP`) | Backward execution truth | Exact material basis + successor-link validation | KEEP | — |
| Progress Basis | Revisioned progress denominator/numerator basis | Roadmap/progress transaction checks | KEEP | — |
| `PROGRESS.yaml` | Calculated progress projection | Internal buckets validated; `REPO_STATE.overall_percent` cross-checked only | KEEP + STRENGTHEN projections | WP-04 |
| `REPO_STATE.progress.phase_percent` | Mirrored phase percentage | Handover renderer trusts it; current progress validator does not cross-check it | REPLACE as derived/reconciled projection | WP-04 |
| `REPO_STATE.progress.ep_percent` | Mirrored EP percentage | Handover renderer trusts it; current progress validator does not cross-check it | REPLACE as derived/reconciled projection | WP-04 |
| `ISSUE_GRAPH.yaml` | Repository model of GitHub coordination relationships | Strong relationship/tree/closure/supersession validation | KEEP | WP-05 operations only |
| Projection generation state | Desired/observed external publication custody | Strong current generation/idempotency/staleness checks | KEEP | — |
| State planes | Execution/quality/evidence/stop truth dimensions | Strong separation and authority/stop consistency | KEEP | — |
| `repository_ready` kernel field | Current repository-recovery summary | Currently derived mainly from lifecycle (`relay_state != INITIALIZING`) rather than semantic baton proof | REPLACE SEMANTICS | WP-02 |
| `projection_ready` kernel field | External projection-current summary | Consistent with projection state | MAP to `PROJECTION_READY` | WP-02 |
| `handover_ready` kernel field | Current combined summary | Currently `repository_ready AND projection_ready` | REPLACE left operand with `BATON_READY` | WP-02 |
| `BATON_READY` | Complete baton for unknown future candidate | Not implemented | ADD | WP-02 |
| Qualification Question Set | Prepared admission criteria | Current Q1-Q5 validator checks focus/anchors/shape, not candidate comprehension | STRENGTHEN | WP-03 |
| Qualification Receipt (`QUAL-*`) | Candidate answers + independent evaluation | Not implemented | ADD | WP-03 |
| Takeover Certification (`TC-*`) | Candidate-specific admission proof | Not implemented | ADD | WP-02 |
| `TAKEOVER_CERTIFIED` | Candidate-specific summary predicate | Not implemented | ADD | WP-02 |
| `MATERIAL_WRITE_READY` | Final current-candidate write predicate | Current kernel has distributed checks but no single reconciled predicate | ADD | WP-02 |
| `cold_start_check.py` | Current context-sufficiency check | Runs aggregate conformance plus a few semantic presence checks; not part of aggregate conformance itself | STRENGTHEN, then DEPRECATE as final admission authority | WP-01/WP-02 |
| Quality blueprint applicability | Selects relevant procedures | EP has quality section but no rigorous applicability router | STRENGTHEN | WP-06 |
| Quality Review (`QRV-*`) | Procedure execution/findings artifact | Not implemented | ADD | WP-06 |
| Blueprint library | Engineering-quality procedures | Ten useful principle documents exist; most are too thin for operational large-project use | STRENGTHEN | WP-06 |
| `REPORT.md` template | Human report headings | Markdown headings only; report validator checks section-name set, not source reconciliation | REPLACE | WP-04/WP-07 |
| Structured report | Reconciled source-derived machine report | Not implemented | ADD / DERIVED | WP-04 |
| `render_status.py` | Human/machine status projection | Reads raw machine state; no Owner/technical separation | REPLACE projection layer | WP-07 |
| `render_handover.py` | Handover projection | Exposes control-plane jargon and trusts mirrored progress; acceptance rows are not complete evidence-aware checklist | STRENGTHEN then split views | WP-04/WP-07 |
| `render_roadmap.py` | Roadmap projection | Derived view | KEEP / DERIVED | WP-04 polish only |
| `OWNER_STATUS.md` | Plain-language Owner view | Not implemented | ADD / DERIVED | WP-07 |
| `TECHNICAL_STATUS.md` | Detailed machine/engineering view | Not implemented | ADD / DERIVED | WP-07 |
| `BOOTSTRAP_MANIFEST.yaml` | Bootstrap input contract | Template/schema + procedural bootstrap validation; protocol basis is written downstream but not later enforced | KEEP + STRENGTHEN binding | WP-10 |
| `MIGRATION_RECONCILIATION.yaml` | V2→V2.5 migration reconciliation artifact | Dedicated migration tooling/schema | KEEP | WP-10 recovery audit |
| `AGENTS_RELAY_SNIPPET.md` | Repository entry guidance | Generated/operator guidance, not authority | KEEP / DERIVED | WP-07/WP-10 |
| JSON/YAML schema layer | Declarative object contracts | 17 schemas exist, but CI/aggregate conformance does not execute JSON Schema validation; PyYAML is the only validator dependency | STRENGTHEN | WP-10, with WP-01/02 schema updates as objects change |
| Procedural validator layer | Semantic/cross-object conformance | Main current enforcement mechanism; some source/projection gaps remain | KEEP + STRENGTHEN | all WPs |
| `validate_relay_conformance.py` | Aggregate static kernel conformance | Broad procedural aggregation; does not include `cold_start_check` or schema execution by design/current implementation | KEEP as kernel aggregator; extend completion checks | WP-01/WP-02/WP-10 |
| CI workflow | Compile + full unittest/stress suite | Good scoped guardrail; no schema-validation stage today | KEEP + STRENGTHEN | WP-10 |
| Chat conversation | Convenience context only | Explicitly non-authoritative | KEEP NON-AUTHORITY | — |

## Confirmed WP-00 authority / enforcement findings

1. **Protocol pin is produced but not enforced.** `relay_protocol.version` and `relay_protocol.basis_ref` are written by bootstrap/template but omitted from the current repo-state validator and repo-state schema contract.
2. **REPO_PROFILE is an under-enforced producer output.** It has a template/schema but no dedicated validator in aggregate conformance.
3. **Schemas are advisory today.** The repository carries schemas, but CI and aggregate conformance execute procedural validators only; schema/template drift can therefore remain invisible.
4. **EP shape exceeds EP semantics.** Inputs, benchmarks, anti-drift, implementation steps, quality, and report payload are weakly typed/validated compared with the zero-chat promise.
5. **Cold-start is a separate check, not a readiness certificate.** Aggregate conformance does not make cold-start proof part of readiness.
6. **Current repository readiness is lifecycle-derived.** It does not prove semantic baton completeness.
7. **Phase/EP progress mirrors can diverge.** `PROGRESS.yaml` is validated, but only overall progress is cross-checked into `REPO_STATE`; handover renders phase/EP mirrors directly.
8. **Report validation proves headings, not reconciled content.** Current `REPORT.md` is not yet a source-derived structured projection.
9. **Qualification is metadata-level.** Q1-Q5 grounding is validated, but candidate answers/evaluation/independence are absent.
10. **Human handover is coupled to machine vocabulary.** It does not yet provide a complete evidence-aware Objective→Phase→WP→Task→AC Owner checklist.
11. **Discovery ID namespace collides with the completion target.** Existing EP steps use `DISC-*`; completion architecture reserves `DISC-*` for Discovery Receipts. Target convention is `DSTEP-*` for EP discovery steps and `DISC-*` for receipts.

## Source-of-truth rules

1. Owner intent and applied ODRs govern intent changes.
2. The Overall Roadmap governs engineering plan/topology.
3. EP/Parallel Plan governs the currently authorized execution slice but cannot redefine roadmap intent.
4. Candidate DISC/QUAL/TC objects prove candidate admission; they cannot rewrite the EP or roadmap.
5. Checkpoints record what actually happened; they cannot silently redefine Owner intent.
6. Progress and issue graph are reconciled repository state derived from roadmap/execution facts.
7. GitHub is an external coordination projection, not an alternate roadmap authority.
8. Structured reports and generated Markdown are projections. If they disagree with source objects, they are stale/invalid.
9. Conversation is never custody.

## Replacement map

```text
key-presence EP validation
    -> semantic EP validation

DISC-* discovery step IDs
    -> DSTEP-* step IDs
       + DISC-* candidate receipt IDs

repository_ready inferred mainly from lifecycle
    -> BATON_READY from semantic baton proof

candidate understanding implicit in cold-start
    -> DISC + QUAL + TC candidate admission

section-name report validation
    -> source-reconciled structured report contract

Q1-Q5 metadata grounding only
    -> question set + evaluated QUAL receipt

single control-plane-oriented renderer
    -> technical projection + plain-language Owner projection

unreconciled progress mirrors
    -> source-derived progress/checklist projection
```

The roadmap, serial/parallel control model, exact-head evidence, drift/continuity, checkpoint custody, progress basis, issue relationship model, and projection-generation idempotency remain foundations rather than targets for rewrite.
