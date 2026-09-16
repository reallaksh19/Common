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
CP-R006  WP-05 GitHub Program Projection            COMPLETE — exact-head CI pending
   |
   v
WP-06    Quality Procedure Library                  NEXT FRONTIER after CP-R006 CI PASS
```

WP-05 pre-checkpoint implementation verification passed workflow **35140358167** on head `f63fbf8fbf71a3ad24ce0fd57e4e97a584d8c02b`, with compile, root units and all 111 repository-neutral synthetic stress tests passing.

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | COMPLETE — CP-R004 |
| WP-04 Full progress / handover / next-work | 12 | COMPLETE — CP-R005 |
| WP-05 GitHub Program Projection operations | 8 | COMPLETE — CP-R006, exact-head CI pending |
| WP-06 Quality Procedure Library | 10 | NEXT FRONTIER AFTER CP-R006 CI PASS |
| WP-07 Human Communication | 6 | WAITING |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Checkpointed content completion: 73%; formal CP-R006 closure awaits exact-head CI.** Progress is acceptance/checkpoint-derived.

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

`CP-R005` delivered authoritative Objective -> Phase -> WP -> EP -> Step -> AC progress, checked REPO_STATE mirrors, exact structured `next_work.steps[]`, source-digest report projection, and source-derived status/handover while preserving parallel/join/replan custody.

### WP-05 — GitHub Program Projection operations

`CP-R006` and `wp-05-github-program-projection.md` operationalize GitHub as a crash-safe coordination projection rather than authority.

The current desired external generation is an immutable `GHGEN-*` bound to roadmap revision, execution ref and issue-graph revision. It contains ordered stable `GHOP-*` operations:

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

Each write follows:

```text
select GHOP
 -> persist ATTEMPTED_UNCONFIRMED
 -> external mutation
 -> GITHUB_OBSERVATION readback
 -> verify
 -> reconcile ISSUE_GRAPH / projection readiness
```

Missing connector response never proves no mutation happened. Uncertain CREATE is reconciled by durable operation identity/marker before retry. Verified readback can recover a lost connector receipt explicitly. Old generations remain durable history and lose publication authority when superseded.

`ISSUE_GRAPH.github_state` now means last verified external state: `ABSENT | OPEN | CLOSED | UNKNOWN`. Native parent/sub-issue or other relationship success may be claimed only when the adapter can create and read back that native relationship; prose/body links are not equivalent.

WP-05 pre-checkpoint evidence:

```text
f63fbf8fbf71a3ad24ce0fd57e4e97a584d8c02b
workflow 35140358167 — PASS
root units + 111 dedicated stress tests
```

## Remaining dependency topology

```text
WP-06 Quality Procedures          NEXT after CP-R006 CI PASS
   |
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
[x] operational GitHub projection procedures — CP-R006 content complete, final checkpoint CI pending
[ ] scoped QRV quality procedures
[ ] plain-language Owner communication
[ ] Owner change-intake projection
[ ] lifecycle cold-start/certification matrix
[ ] A -> B -> C zero-chat relay
[ ] schema/template/validator/renderer/docs audit
[ ] final exact-head generic CI
[x] V2 untouched through WP-05
[x] no downstream-specific logic through WP-05
```

Do not merge automatically.
