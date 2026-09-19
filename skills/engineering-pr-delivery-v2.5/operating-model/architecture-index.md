# Engineering Relay V2.5 architecture index

## Purpose

This is the stable navigation map for the released V2.5 control model. It points operators and maintainers to the authoritative concepts, executable validators, and derived projections without requiring completion-program history.

## Start here

| Need | Primary document | Executable check / producer |
| --- | --- | --- |
| Understand the whole relay | `../SKILL.md` | `scripts/validate_relay_conformance.py` |
| Recover a repository with no chat | `operator-quick-start.md` | `scripts/cold_start_check.py`, `scripts/zero_context_reconstruction.py` |
| See a repository-neutral relay walkthrough | `synthetic-relay-example.md` | stress tests under `tests/stress/` |
| Understand authority ownership | `object-authority-matrix.md` | `scripts/self_consistency_audit.py` |
| Understand roadmap/frontier | `roadmap-first-model.md`, `dynamic-roadmap.md`, `execution-frontier.md` | `scripts/validate_roadmap.py`, `scripts/validate_roadmap_events.py`, `scripts/validate_execution_frontier.py` |
| Author/validate an EP | `execution-package.md` | `scripts/validate_ep_semantics.py` |
| Prove baton/takeover/write readiness | `takeover-certification.md` | `scripts/validate_baton_readiness.py`, `scripts/validate_takeover_certification.py`, `scripts/material_write_ready.py` |
| Run phase/material-boundary qualification | `phase-transition.md` | `scripts/validate_question_set.py`, `scripts/validate_qualification_receipt.py` |
| Understand progress and exact next work | `progress-accounting.md`, `wp-04-progress-handover.md` | `scripts/validate_progress.py`, `scripts/render_handover.py` |
| Route and evidence quality work | `quality-procedures.md` | `scripts/validate_quality_router.py`, `scripts/validate_quality_review.py` |
| Operate issue/GitHub projection | `issue-projection.md`, `github-program-projection.md` | `scripts/validate_github_projection.py`, `scripts/github_projection_next.py` |
| Observe PR delivery/readiness | `../blueprints/github-delivery.md`, `human-communication.md` | `scripts/validate_delivery_observation.py`, `scripts/delivery_projection.py` |
| Audit Owner field lineage | `owner-field-lineage.md`, `owner-field-lineage.yaml` | `scripts/validate_owner_field_lineage.py`, `scripts/self_consistency_audit.py` |
| Correlate PR ↔ Issue ↔ EP | `../blueprints/github-delivery.md`, `operator-quick-start.md` | `scripts/render_pr_correlation.py`, `scripts/validate_pr_correlation.py` |
| Handle Owner intent change | `owner-change-intake.md` | `scripts/validate_owner_change_intake.py`, `scripts/render_owner_change.py` |
| Understand parallel fork/join/replan | `serial-execution.md`, `parallel-replan.md` | `scripts/validate_parallel_plan.py`, `scripts/validate_parallel_join.py`, `scripts/validate_parallel_replan.py` |
| Understand drift/continuity | `git-observation.md`, `roadmap-continuity.md` | `scripts/inspect_git_context.py`, `scripts/validate_roadmap_continuity.py` |
| Understand human projections | `human-communication.md` | `scripts/render_owner_status.py`, `scripts/render_technical_status.py` |
| Understand the zero-chat release proof | `relay-certification-matrix.md` | `scripts/validate_zero_context_reconstruction.py` |
| Audit implementation consistency | `wp-10-self-consistency-audit.md` | `scripts/self_consistency_audit.py` |

## Authority layers

```text
OWNER INTENT / ODR
    ↓
OVERALL ROADMAP + REVISION
    ↓
EXECUTABLE FRONTIER
    ↓
SEMANTIC EP / APPROVED PARALLEL PLAN
    ↓
BATON_READY
    ↓
DISC / QUAL / TC FOR CURRENT CANDIDATE
    ↓
TAKEOVER_CERTIFIED
    ↓
LIVE GIT ROUTE + MATERIAL_WRITE_READY
    ↓
IMPLEMENTATION + APPLICABLE QUALITY / TEST / ORACLE EVIDENCE
    ↓
QRV + CHECKPOINT
    ↓
ROADMAP / PROGRESS / ISSUE RECONCILIATION
    ↓
REQUIRED EXTERNAL PROJECTION CONVERGENCE
    ↓
SOURCE-DERIVED REPORT / HUMAN VIEWS
    ↓
ZERO-CONTEXT SUCCESSOR RECONSTRUCTION
```

Generated Markdown and GitHub Issues are projections. They never replace Owner intent, roadmap, EP/plan, evidence receipts, checkpoint, progress, or issue-graph authority.

## Durable object families

```text
ODR-*    Owner Decision Record
EP-*     Execution Package
DSTEP-*  discovery instruction inside EP
DISC-*   Discovery Receipt
QSET-*   Qualification Question Set
QUAL-*   Qualification Receipt
TC-*     Takeover Certification
QRV-*    Quality Review
QF-*     Quality Finding
CP-*     Checkpoint
GHGEN-*  GitHub projection generation
GHOP-*   GitHub projection operation
```

Parallel plan/join/replan, drift, roadmap revision/continuity, progress basis, issue graph, repository state, and repository profile retain their documented namespaces. `EVT-*` identifies material roadmap-event ledger entries; these are history/index records, not roadmap authority.

## Enforcement layers

1. **Schemas/templates** describe durable shape and operator starting points.
2. **Procedural validators** enforce semantic and cross-object invariants.
3. **Aggregate conformance** composes material validators for repository admission.
4. **Runtime gates** inspect the live checkout and candidate before material writes.
5. **Synthetic stress tests** prove repository-neutral failure modes and zero-chat relay behavior.
6. **Self-consistency audit** checks that schemas, templates, validators, renderers, docs, entrypoints, and CI still describe one control model.

## Historical completion documents

Files named `wp-01-*` through `wp-11-*`, `completion-architecture.md`, `catchup-completion-roadmap.md`, and `completion-checkpoints/**` are durable implementation history and release evidence. Operators should use the stable documents above for normal downstream execution.