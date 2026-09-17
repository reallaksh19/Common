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
CP-R008  WP-07 Human Communication                  CHECKPOINT WRITTEN — EXACT-HEAD CI REQUIRED
   |
   v
WP-08    Owner Change Intake                        CONDITIONAL NEXT FRONTIER
```

WP-07 documentation-aligned implementation passed workflow **35176089341** on head `49d0e52ee81e34ddf4152927456a4f4e4bdef665`: compile PASS, 7 root units PASS, 125 repository-neutral synthetic stress tests PASS. CP-R008 is not formally closed until the exact head containing this checkpoint and program-state reconciliation passes the same corrected workflow.

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
| WP-07 Human Communication | 6 | CHECKPOINT WRITTEN — CI PENDING |
| WP-08 Owner Change Intake | 3 | CONDITIONAL NEXT |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Checkpointed earned completion before CP-R008: 83%. Target after CP-R008 exact-head PASS: 89%.** Progress remains acceptance/checkpoint-derived.

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

`CP-R007` and `wp-06-quality-procedures.md` deliver applicability-routed engineering quality and first-class `QRV-*` evidence. Every EP partitions the built-in procedure library exactly once; applicable procedures require reason + review focus, and a quality finding blocks execution only through a valid existing hard-stop mapping with durable basis.

### WP-07 — Human Communication

`CP-R008`, `wp-07-human-communication.md`, and `human-communication.md` deliver two generated views from one source-bound communication projection:

```text
report projection
  -> communication projection
      -> TECHNICAL_STATUS.md
      -> OWNER_STATUS.md
```

Technical status preserves protocol precision. Owner status uses plain language for current capability, purpose, protected/non-change scope, evidence/missing evidence, material quality risks/limitations, roadmap/progress reconciliation, genuine Owner decisions, exact next work and active stops. Owner-reserved scope does not fabricate a decision request. Non-blocking quality risk remains visible without becoming a fake stop. Aggregate conformance validates that material truth cannot be hidden.

Pre-checkpoint evidence:

```text
repaired implementation
  0b5c38f008d670ab9db24cf7b3fe4fccba07893b
  workflow 35166010334 — PASS

documentation-aligned implementation
  49d0e52ee81e34ddf4152927456a4f4e4bdef665
  workflow 35176089341 — PASS

root units: 7
stress tests: 125
```

Formal WP-07 closure still requires the exact checkpoint/program-state CI gate.

## Remaining dependency topology

```text
WP-08 Owner Change Intake             CONDITIONAL AFTER CP-R008 CI
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
[x] operational GitHub projection — CP-R006
[x] scoped procedural QRV quality system — CP-R007
[~] plain-language Owner communication — CP-R008 written, exact-head CI pending
[ ] Owner change-intake projection
[ ] lifecycle cold-start/certification matrix
[ ] A -> B -> C zero-chat relay
[ ] schema/template/validator/renderer/docs audit
[ ] final exact-head generic CI
[x] V2 untouched through WP-07 implementation
[x] no downstream-specific logic through WP-07 implementation
```

Do not merge automatically.
