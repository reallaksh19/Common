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
   v
WP-04    Full progress / handover / next-work       CURRENT FRONTIER
```

The CP-R004/status gate passed corrected workflow **35099657641** on head `e3dd0c7d14b2958a65427935303f481bc17a8b5d`, with compile, root units, and the dedicated synthetic stress suite all passing.

## Progress Basis

| Work package | Weight | Status |
| --- | ---: | --- |
| WP-00 Kernel baseline / object matrix | 5 | COMPLETE — CP-R001 |
| WP-01 Semantic Execution Package | 18 | COMPLETE — CP-R002 |
| WP-02 Baton readiness + Takeover Certification | 18 | COMPLETE — CP-R003 |
| WP-03 Strong phase/boundary qualification | 12 | COMPLETE — CP-R004 |
| WP-04 Full progress / handover / next-work | 12 | CURRENT FRONTIER |
| WP-05 GitHub Program Projection operations | 8 | WAITING |
| WP-06 Quality Procedure Library | 10 | WAITING |
| WP-07 Human Communication | 6 | WAITING |
| WP-08 Owner Change Intake | 3 | WAITING |
| WP-09 End-to-end Relay Certification Matrix | 5 | WAITING |
| WP-10 Self-consistency Audit | 2 | WAITING |
| WP-11 PR Readiness | 1 | WAITING |
| **Total** | **100** | |

**Earned completion: 53%.** Progress is checkpoint/acceptance-derived.

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

`CP-R002` delivered semantic EP validation: `DSTEP-*` discovery instructions, typed current-slice inputs/oracles, strong scope/anti-drift, executable steps, source-aware report contracts, `REPO_PROFILE` admission, protocol binding, and hollow-EP rejection.

### WP-02 — Baton readiness and takeover

`CP-R003` delivered candidate-independent `BATON_READY`, route-scoped `DISC-*`, route/candidate `TC-*`, independent evaluator rules, exact contract/baton digests, `HANDOVER_READY`, and live-derived `MATERIAL_WRITE_READY`.

### WP-03 — Strong qualification

`CP-R004` and `wp-03-qualification.md` deliver:

```text
qualification_boundary
 -> QSET-* prepared by outgoing agent
 -> zero-chat candidate answers
 -> independent/deterministic evaluation
 -> QUAL-* PASS/FAIL
 -> TC-* qualification id/path/digest
 -> TAKEOVER_CERTIFIED
```

Fresh qualification is required on `PHASE_CHANGED` or `MATERIAL_QUALIFICATION_BOUNDARY_CHANGED`.

Q1–Q5 enforce:

```text
Q1 actual production/source trace
Q2 engineering reconstruction; concrete payload for quantitative work
Q3 mutation + protected invariant + exact falsifier
Q4 independent benchmark/oracle verification
Q5 exact first safe implementation slice + predicted verification
```

QSET/QUAL bind to the exact route, roadmap revision, work package, and semantic EP digest. Candidate-authored criteria/self-evaluation are rejected. QUAL mutation invalidates an issued TC through receipt-digest binding. Inline `phase_transition.questions` is retired.

WP-03 evidence:

```text
pre-checkpoint aligned workflow 35098797964 — PASS
checkpoint/status workflow      35099657641 — PASS
stress surface at WP-03         99 synthetic tests
```

## WP-04 — Full progress / handover / next-work — CURRENT FRONTIER

### Outcome

The Owner and a zero-context successor can see complete project state and exact next work without reading raw YAML or trusting manually mirrored percentages.

### Authority

Human progress/reporting must derive from:

```text
OVERALL_ROADMAP
PROGRESS
EP / approved lane EP
CP
DISC / QSET / QUAL / TC when relevant
ISSUE_GRAPH
REPO_STATE only for lifecycle/routing facts it actually owns
```

Generated reports are projections, never authority.

### Required hierarchy

```text
Overall
  Objective
    Phase
      Work Package
        Task / implementation step
          Acceptance Criterion
```

Each useful level must expose calculated state/progress and evidence/disposition where applicable.

### Current execution

Render current objective, phase, WP, EP/lane, implementation step, acceptance/evidence state, and relevant baton/takeover/write readiness.

Unverified `REPO_STATE.progress.phase_percent` and `ep_percent` must not remain human-report authority.

### Detailed next-work contract

Replace vague `next_action` dependence with ordered source-derived steps containing:

```text
order
action
targets
required inputs
tests/oracles
acceptance IDs
expected result
stop/reconciliation conditions
qualification-boundary flag
```

### Structured report projection

Create a source-bound generated report. If report content disagrees with source objects, it is stale/invalid and must be regenerated; it cannot override roadmap, progress, EP, CP, issue or certification truth.

### WP-04 acceptance direction

- stale phase/EP percentage mirrors cannot mislead handover;
- Objective -> Phase -> WP -> Step -> AC checklist is complete and source-derived;
- evidence states remain distinct, including `NOT_RUN` and supersession;
- next work is ordered and bound to targets/tests/acceptance;
- structured report projection is reproducible/idempotent from source objects;
- serial, reconciliation, approved-parallel, idle and terminal states do not invent work.

Owner-language redesign beyond basic clarity remains WP-07.

## Remaining dependency topology

```text
WP-04 Progress / Handover
   |
   +---------------------------+
   |                           |
   v                           v
WP-05 GitHub Ops         WP-06 Quality Procedures
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
[ ] full roadmap/WP/task/AC handover
[ ] detailed ordered next-work projection
[ ] generated report reconciliation
[ ] operational GitHub projection procedures
[ ] scoped QRV quality procedures
[ ] plain-language Owner communication
[ ] lifecycle cold-start/certification matrix
[ ] A -> B -> C zero-chat relay
[ ] schema/template/validator/renderer/docs audit
[ ] final exact-head generic CI
[x] V2 untouched through WP-03
[x] no downstream-specific logic through WP-03
```

Do not merge automatically.
