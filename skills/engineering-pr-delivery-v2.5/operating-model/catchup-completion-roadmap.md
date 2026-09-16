# V2.5 catch-up / completion roadmap

## Purpose

Complete the operational relay on top of the V2.5 control-plane kernel. This is not a rewrite of V2. PR #396 remains draft; downstream repositories remain read-only stress targets unless separately authorized.

> First make the baton trustworthy. Then prove a replacement can pick it up. Then prove engineering qualification. Then make the relay complete and legible.

## Current program state

```text
CP-R001  WP-00 Kernel baseline / object matrix      COMPLETE
   |
CP-R002  WP-01 Semantic Execution Package           COMPLETE
   |
CP-R003  WP-02 Baton readiness / Takeover Cert      COMPLETE
   |
CP-R004  WP-03 Strong qualification                 COMPLETE
   |
CP-R005  WP-04 Progress / handover / next-work      COMPLETE — exact-head CI pending
   |
   v
WP-05    GitHub Program Projection operations       NEXT FRONTIER AFTER CP-R005 CI PASS
```

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | COMPLETE — CP-R004 |
| WP-04 Full progress / handover / next-work | 12 | COMPLETE — CP-R005; final CI pending |
| WP-05 GitHub Program Projection operations | 8 | NEXT FRONTIER AFTER CP-R005 CI PASS |
| WP-06 Quality Procedure Library | 10 | WAITING |
| WP-07 Human Communication | 6 | WAITING |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Checkpointed completion after CP-R005 exact-head CI: 65%.** Progress is acceptance/checkpoint-derived.

## CI evidence rule

A whole-suite claim requires both explicit test surfaces:

```text
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests -p 'test*.py' -v
python -m unittest discover -s skills/engineering-pr-delivery-v2.5/tests/stress -p 'test*.py' -v
```

Historical interpretation is corrected in `ci-evidence-correction.md`.

## Completed catch-up layers

### WP-00 — Kernel baseline

`CP-R001` froze the actual branch/object authority model and assigned findings BA-001 through BA-013.

### WP-01 — Semantic EP

`CP-R002` delivered `DSTEP-*` discovery instructions, typed current-slice inputs/oracles, bounded scope/anti-drift, executable steps, source-aware report contracts, `REPO_PROFILE` admission, protocol binding, and hollow-EP rejection.

### WP-02 — Baton readiness and takeover

`CP-R003` delivered candidate-independent `BATON_READY`, route-scoped `DISC-*`, route/candidate `TC-*`, independent evaluator rules, exact contract/baton digests, `HANDOVER_READY`, and live-derived `MATERIAL_WRITE_READY`.

### WP-03 — Strong qualification

`CP-R004` delivered the durable `qualification_boundary -> QSET-* -> candidate answers -> QUAL-* -> TC-*` transaction. Fresh qualification is required for `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED` and Q1-Q5 require actual production tracing, engineering reconstruction, falsifier reasoning, independent verification and the exact first safe slice.

### WP-04 — Full progress / handover / next-work

`CP-R005` and `wp-04-progress-handover.md` deliver source-derived progress and handover:

```text
PROGRESS.yaml
  -> Objective
  -> Phase
  -> Work Package
  -> EP
  -> Implementation Step
  -> Acceptance Criterion
```

`PROGRESS.yaml` is progress authority. `REPO_STATE.progress` percentages are checked mirrors only. Missing roadmap/current-EP progress rows fail conformance.

Every executable EP now carries structured ordered `next_work.steps[]` with action, targets, inputs, tests, benchmarks/oracles, acceptance, expected result and stop/reconciliation conditions. The scalar execution `next_action` is only a short machine hint.

`report_projection.py` derives one structured report from repository authority objects and records source digests. `validate_report_projection.py` participates in aggregate conformance. Generated report/YAML/Markdown cannot override roadmap, progress, EP/plan, checkpoint, issue or repository truth.

`render_status.py` and `render_handover.py` consume the source-derived projection. Handover exposes Objective -> Phase -> WP -> Step -> AC progress/status/basis plus exact ordered next work while retaining parallel/join/replan custody detail.

Bootstrap creates complete zero-weight roadmap progress rows without fabricating executable work. Parallel convergence creates integration EP/step/acceptance progress rows before cold start.

WP-04 pre-checkpoint evidence:

```text
head     fabcb280167fbc1a8d95d120d4e88d242e1cd211
workflow 35104423581 — PASS
stress   105 repository-neutral synthetic tests
```

Formal CP-R005 validity still requires PASS on the exact checkpoint/program-state head.

## WP-05 — GitHub Program Projection operations — conditional next frontier

WP-05 operationalizes GitHub as an external coordination projection, never roadmap authority.

Required operation classes:

```text
CREATE
LINK
UPDATE
PUBLISH_HANDOVER
SUPERSEDE
REVISE
CLOSE
REOPEN
```

The transaction must prepare a durable desired operation, preserve stable generation identity, perform/publish externally, capture a receipt, verify the result, reconcile `ISSUE_GRAPH.yaml`, and converge the external projection idempotently. Parent/subissue linking, evidence-preserving supersession, closure and reopen must use the already-delivered issue/projection semantics rather than inventing a second authority plane.

No real downstream GitHub adoption belongs in WP-05 implementation; prove generic transactions synthetically first.

## Remaining dependency topology

```text
WP-05 GitHub Ops
   |
   +---------------------------+
   |                           |
   v                           v
             WP-06 Quality Procedures
   |                           |
   +-------------+-------------+
                 v
        WP-07 Human Communication
                 |
                 v
        WP-08 Owner Change Intake
                 |
                 v
     WP-09 End-to-end Certification
                 |
                 v
       WP-10 Self-consistency Audit
                 |
                 v
          WP-11 PR Readiness
```

Serial execution remains default. Defined future work is not executable work.

## Merge gate

PR #396 remains draft until:

```text
[x] Semantic EP
[x] BATON_READY / takeover certification
[x] live write-readiness gate
[x] evaluated QUAL receipt when required
[x] full roadmap/WP/task/AC handover
[x] detailed ordered next-work projection
[x] generated report reconciliation
[ ] operational GitHub projection procedures
[ ] scoped QRV quality procedures
[ ] plain-language Owner communication
[ ] lifecycle cold-start/certification matrix
[ ] A -> B -> C zero-chat relay
[ ] schema/template/validator/renderer/docs audit
[ ] final exact-head generic CI
[x] V2 untouched through WP-04
[x] no downstream-specific logic through WP-04
```

Do not merge automatically.
