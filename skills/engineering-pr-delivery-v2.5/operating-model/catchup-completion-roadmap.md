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
CP-R005  WP-04 Progress / handover / next-work      COMPLETE
   |
CP-R006  WP-05 GitHub Program Projection            COMPLETE
   |
CP-R007  WP-06 Quality Procedure Library            COMPLETE
   |
CP-R008  WP-07 Human Communication                  COMPLETE
   |
CP-R009  WP-08 Owner Change Intake                  COMPLETE
   |
CP-R010  WP-09 End-to-end Relay Certification       COMPLETE PENDING EXACT-HEAD CI
   |
   v
WP-10    Self-consistency Audit                     NEXT AFTER CP-R010 CI PASS
```

WP-09 pre-checkpoint implementation passed workflow **35192108782** on head `3ff5b26281078822c9965c4048c5f6b3bc8c851d`: compile PASS, 7 root units PASS, 135 repository-neutral synthetic stress tests PASS.

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | COMPLETE — CP-R004 |
| WP-04 Full progress / handover / next-work | 12 | COMPLETE — CP-R005 |
| WP-05 GitHub Program Projection operations | 8 | COMPLETE — CP-R006 |
| WP-06 Quality Procedure Library | 10 | COMPLETE — CP-R007 |
| WP-07 Human Communication | 6 | COMPLETE — CP-R008 |
| WP-08 Owner Change Intake | 3 | COMPLETE — CP-R009 |
| WP-09 End-to-end Relay Certification Matrix | 5 | COMPLETE — CP-R010 PENDING EXACT-HEAD CI |
| WP-10 Self-consistency Audit | 2 | WAITING FOR CP-R010 CI |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Conditional earned completion: 97%.** Formal WP-09 closure requires exact-head CI containing CP-R010 and this reconciliation.

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
`CP-R002` delivered executable `DSTEP-*`, typed current-slice inputs/oracles, bounded scope/anti-drift, executable implementation steps, source-aware reports, `REPO_PROFILE` admission and hollow-EP rejection.

### WP-02 — Baton readiness and takeover
`CP-R003` delivered candidate-independent `BATON_READY`, route-scoped `DISC-*`, candidate/route `TC-*`, independent evaluator rules, exact contract/baton digests, `HANDOVER_READY`, and live-derived `MATERIAL_WRITE_READY`.

### WP-03 — Strong qualification
`CP-R004` delivered `qualification_boundary -> QSET-* -> candidate answers -> QUAL-* -> TC-*`; fresh qualification is required for phase or material qualification-boundary change.

### WP-04 — Full progress / handover / next-work
`CP-R005` delivered authoritative Objective -> Phase -> WP -> EP -> Step -> AC progress, checked REPO_STATE mirrors, structured `next_work.steps[]`, source-digest report projection, and source-derived status/handover.

### WP-05 — GitHub Program Projection
`CP-R006` operationalized GitHub as a crash-safe coordination projection using immutable `GHGEN-*`, stable `GHOP-*`, pre-write `ATTEMPTED_UNCONFIRMED`, durable readback observations, verified reconciliation, `ABSENT | OPEN | CLOSED | UNKNOWN`, native-relationship verification, and superseded-generation retry revocation.

### WP-06 — Quality Procedure Library
`CP-R007` delivers applicability-routed engineering quality and first-class `QRV-*` evidence. Every EP partitions the built-in procedure library exactly once; applicable procedures require reason + review focus, and a quality finding blocks execution only through a valid existing hard-stop mapping with durable basis.

### WP-07 — Human Communication
`CP-R008` delivers `TECHNICAL_STATUS.md` and plain-language `OWNER_STATUS.md` from one source-bound communication projection. Material execution, evidence, quality, stop, scope, roadmap and next-work truth cannot be hidden by the Owner view.

### WP-08 — Owner Change Intake
`CP-R009` delivers an Owner-facing change report over ODR + roadmap-transaction authority, including semantic before/after intent, retained/invalidated behavior, scope, roadmap/progress/issue effects, active-work disposition and resulting frontier without creating a second authority source.

### WP-09 — End-to-end Relay Certification Matrix

`CP-R010`, `wp-09-end-to-end-certification.md`, and `relay-certification-matrix.md` deliver the defining zero-chat release proof.

```text
Agent A works with chat
  -> CP-A / EP-B / QSET-B persisted
  -> chat deleted
Agent B receives repository only
  -> reconstructs current work
  -> DISC / QUAL / TC PASS
  -> completes WP-B
  -> CP-B / EP-C / QSET-C persisted
  -> chat deleted
Agent C receives repository only
  -> reconstructs current work
  -> independently qualifies/certifies
```

The strict repository-only boundary deliberately discards predecessor helper return values: B and C reopen persisted EP/QSET state and derive certification inputs from repository files only. Agent C can reconstruct the defining release questions for task purpose, Owner decisions, predecessor facts, uncertainty, input authority/editability, independent oracle, scope, quality obligations, evidence, tests/acceptance, first action/staleness and exact next work.

Lifecycle certification covers ACTIVE, ACTIVE+RECONCILING, PARALLEL, ACTIVE+required projection STALE, IDLE and TERMINAL; INITIALIZING remains covered by bootstrap/core tests. RECONCILING remains READ_ONLY, stale required projection remains not handover-ready, and IDLE/TERMINAL expose no material route.

WP-09 pre-checkpoint evidence:

```text
implementation + docs
  3ff5b26281078822c9965c4048c5f6b3bc8c851d
  workflow 35192108782 — PASS

root units: 7
stress tests: 135
```

## Remaining dependency topology

```text
CP-R010 exact-head verification
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
[x] operational GitHub projection — CP-R006
[x] scoped procedural QRV quality system — CP-R007
[x] plain-language Owner communication — CP-R008
[x] Owner change-intake projection — CP-R009
[x] lifecycle cold-start/certification matrix — CP-R010
[x] A -> B -> C zero-chat relay — CP-R010
[ ] schema/template/validator/renderer/docs audit
[ ] final exact-head generic CI
[x] V2 untouched through WP-09
[x] no downstream-specific logic through WP-09
```

Do not merge automatically.
