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
   v
WP-07    Human Communication                        CURRENT FRONTIER
```

CP-R007 checkpoint/status verification passed workflow **35147172696** on head `d695329c5bf69fa6c127ae2b47dc35d99227631b`: compile PASS, 7 root units PASS, 118 repository-neutral synthetic stress tests PASS.

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
| WP-07 Human Communication | 6 | CURRENT FRONTIER |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Earned completion: 83%.** Progress remains acceptance/checkpoint-derived.

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

`CP-R007` and `wp-06-quality-procedures.md` deliver applicability-routed engineering quality and first-class `QRV-*` evidence.

Every EP partitions the built-in procedure library exactly once:

```text
software-design | coding | ui-ux | testing | engineering-numerics
code-review | accessibility | performance | migration | github-delivery
```

Applicable procedures require a concrete reason and review focus. Explicit not-applicable procedures require a concrete reason but no fake review ceremony. Each blueprint contains WHEN TO APPLY, REQUIRED INPUTS, PROCEDURE, CHECKLIST, ANTI-PATTERNS, ARTIFACTS, VERIFICATION, FINDING CLASSIFICATION, TRUE HARD-STOP CONDITIONS, OWNER REPORT and SUCCESSOR HANDOVER.

A `QRV-*` is bound to exact EP contract digest, roadmap revision, material ref and router snapshot. Procedure results are `CLEAR | FINDINGS | NOT_RUN`. Quality findings use `QF-*`; severity alone never creates stop authority. A finding blocks execution only when it maps to an existing true hard-stop category with durable basis. Deferred/unresolved findings transfer exactly to successor handover.

Checkpoints cite QRV id/path/digest on the same material basis. A checkpoint cannot publish an executable successor while its QRV has a true blocking finding. Parallel lane checkpoints carry lane-specific QRVs. Report projection source-binds the checkpoint QRV instead of creating a second quality authority.

WP-06 evidence:

```text
pre-checkpoint implementation
  c5a3f8dfb9111081b15fef607dd2b6e7ba8ae868
  workflow 35146877546 — PASS

CP-R007 checkpoint/status
  d695329c5bf69fa6c127ae2b47dc35d99227631b
  workflow 35147172696 — PASS

root units: 7
stress tests: 118
```

## Remaining dependency topology

```text
WP-07 Human Communication          CURRENT
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
[x] operational GitHub projection — CP-R006
[x] scoped procedural QRV quality system — CP-R007
[ ] plain-language Owner communication
[ ] Owner change-intake projection
[ ] lifecycle cold-start/certification matrix
[ ] A -> B -> C zero-chat relay
[ ] schema/template/validator/renderer/docs audit
[ ] final exact-head generic CI
[x] V2 untouched through WP-06
[x] no downstream-specific logic through WP-06
```

Do not merge automatically.
