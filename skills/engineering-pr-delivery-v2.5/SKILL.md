---
name: engineering-pr-delivery-v2.5
description: Roadmap-first engineering relay for durable zero-chat multi-agent delivery, with semantic execution packages, independent takeover certification, evaluated engineering qualification, calculated progress, crash-safe GitHub projection, drift/continuity control, and serial-by-default material execution.
---

# Engineering PR Delivery v2.5 — engineering relay with a dynamic overall roadmap

## Governing objective

A replacement agent with no conversational history must be able to recover Owner intent, roadmap position, authorized work, inputs/oracles, scope, predecessor custody, evidence and exact next work from repository state alone; independently prove takeover; execute only when live write readiness permits; checkpoint reality; reconcile roadmap/progress/issues; and leave an equally strong baton.

Conversation is acceleration, never custody.

## Repository-agnostic core

Common contains portable relay policy, schemas, templates, validators and synthetic tests. Do not encode downstream repository names, issue IDs, product formulas or workflow-specific exceptions. Real repositories are read-only black-box stress sources unless the Owner separately authorizes adoption. Reduce every discovered weakness to a repository-neutral invariant plus synthetic regression before changing Common protocol logic.

## Authority chain

```text
explicit Owner intent / ODR
→ OVERALL_ROADMAP.yaml
→ executable frontier
→ semantic EP or Owner-approved parallel router
→ BATON_READY
→ incoming candidate DISC / QUAL / TC evidence
→ TAKEOVER_CERTIFIED(route,candidate)
→ live route + Git basis + MATERIAL_WRITE_READY
→ implementation / read-only reconciliation as authorized
→ checkpoint/evidence
→ roadmap / progress / issue reconciliation
→ required external projection convergence
→ successor baton
```

GitHub Issues and generated Markdown are projections, not roadmap authority.

## Required relay root

```text
agents/relay/
  REPO_STATE.yaml
  REPO_PROFILE.yaml
  roadmap/
    OVERALL_ROADMAP.yaml
    PROGRESS.yaml
    ISSUE_GRAPH.yaml
    revisions/**
    owner-decisions/**
  execution-packages/**
  certifications/
    discovery/**
    qualification/**
    takeover/**
  checkpoints/**
  parallel/**
  drift/**
  projection/
    generations/**
  reports/**
  generated/**
```

`REPO_STATE.yaml` is the deterministic bootstrap locator.

## Lifecycle and execution policy

Relay lifecycle:

```text
INITIALIZING — scaffold exists; no material EP is executable
ACTIVE       — one serial frontier WP and one active EP
PARALLEL     — Owner-approved parallel router; lane EPs live in the plan
IDLE         — no executable material work currently exists
TERMINAL     — roadmap work is complete
```

`INITIALIZING | IDLE | TERMINAL` have no active material EP. `ACTIVE` requires `SERIAL`. `PARALLEL` requires `OWNER_APPROVED_PARALLEL`, an approved plan and at least two current frontier WPs.

Material execution is **serial by default**. Do not infer parallelism from apparent independence.

## Dynamic roadmap

Roadmap mutation classes:

```text
EXECUTION_DERIVED_STATUS
ENGINEERING_DISCOVERY_PROPOSAL
OWNER_INTENT_MUTATION
```

Agents may apply factual status updates, may propose structural discoveries, and require an applied Owner Decision Record for Owner-intent mutations. Material revisions reconcile dependencies, EP continuity/staleness, issues, Progress Basis and the computed frontier. `frontier_after` must equal the frontier computed from the resulting roadmap.

Owner deferral is not technical satisfaction. A `DEFERRAL` keeps named items pending and does not itself grant write authority.

## Semantic Execution Package

Every serial EP and approved parallel lane EP is a forward work contract for one roadmap work package. It contains:

- identity and exact Git basis;
- roadmap source/frontier origin;
- outcome and context capsule;
- executable `DSTEP-*` repository discovery;
- typed current/future inputs with authority, source, editability, applicability, resolution and stale conditions;
- benchmark/oracle contracts with payload, expected result, tolerance/exactness and independence;
- allowed writes/reads, protected invariants, prohibited and Owner-reserved scope;
- structured anti-drift;
- exact implementation steps mapped to inputs, ACs and tests;
- quality applicability;
- acceptance and validation contracts;
- optional `qualification_boundary`;
- source-bound report payloads;
- ordered `next_work.steps[]` with targets, inputs, tests/oracles, acceptance, expected result and stop/reconciliation conditions;
- checkpoint and successor duties.

Exactly one predecessor baton is active: checkpoint, parallel join or parallel replan. EP and CP are different objects and never substitute for each other.

Read `operating-model/execution-package.md`.

## Five readiness predicates

Do not collapse readiness into lifecycle.

### BATON_READY

Candidate-independent repository property:

```text
valid roadmap/frontier
+ semantic current EP/plan
+ valid predecessor custody
+ admitted profile/protocol basis
+ complete discovery/input/oracle/scope/report/successor contract
+ valid QSET when fresh qualification is required
+ no chat dependency
```

A baton can be ready before the future replacement agent exists.

### TAKEOVER_CERTIFIED(route,candidate)

Candidate-specific proof:

```text
BATON_READY
+ current DISC receipt PASS
+ current TC receipt PASS
+ current QUAL receipt PASS when required
+ all evidence bound to current route/roadmap/EP/profile/predecessor/material basis
```

It is route-scoped, including per lane under approved parallel work.

### PROJECTION_READY

Every required external coordination projection represents current repository truth.

### HANDOVER_READY

```text
HANDOVER_READY = BATON_READY AND PROJECTION_READY
```

This describes outgoing custody completeness, not arbitrary candidate write permission.

### MATERIAL_WRITE_READY

Runtime-derived only:

```text
TAKEOVER_CERTIFIED(route,candidate)
+ live route resolves exactly that route
+ live Git/material basis acceptable
+ drift/continuity permits WRITE
+ material_authority == WRITE
+ execution.can_continue == true
+ no active hard stop
```

Never persist this as a timeless boolean.

Read `operating-model/takeover-certification.md`.

## Discovery and takeover certification

EP discovery instructions use `DSTEP-*`. Incoming candidate evidence uses `DISC-*`.

A Discovery Receipt is bound to candidate, exact route, roadmap/protocol/material basis, semantic EP digest, `REPO_PROFILE` digest, predecessor-baton digest, required DSTEP coverage and expected output names. `conversation_context_used` must be false.

A `TC-*` Takeover Certification records candidate, preparer, evaluator, DISC pointer, optional QUAL pointer/digest, exact route/basis, objective checks and final PASS/FAIL. Candidate self-preparation/self-certification is invalid. Validators re-open evidence and recompute current basis; YAML assertions are not authority.

## Engineering qualification — QSET / QUAL

Fresh qualification is mandatory when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

A same-phase boundary change includes material change in production path, engineering authority, numerical method, protected invariant, input authority or verification/oracle class.

Inline `phase_transition.questions` is retired. A required EP boundary references a durable `QSET-*` bound to the exact route and EP contract digest.

The transaction is:

```text
outgoing agent prepares QSET
→ incoming candidate answers from repository only
→ independent/deterministic evaluation
→ QUAL-* receipt
→ TC cites QUAL id/path/digest
```

Q1–Q5 semantics:

```text
Q1 actual production path, state owner, authority source and downstream consumer
Q2 engineering reconstruction; quantitative work carries concrete payload values
Q3 explicit mutation + protected invariant + exact falsifier
Q4 independent verification using incoming benchmark/oracle evidence
Q5 exact first bounded change + predicted before/after verification
```

The candidate cannot prepare its own QSET or be its own `INDEPENDENT_AGENT` evaluator. QUAL PASS requires all five evaluations PASS. Editing QUAL after TC issuance invalidates takeover via digest mismatch.

Read `operating-model/phase-transition.md`.

## Live Git routing and drift

Before material writes, use the runtime write gate or diagnose its components:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py <repo-root> --candidate-id <agent-instance-id>
python skills/engineering-pr-delivery-v2.5/scripts/resolve_execution_route.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/inspect_git_context.py <repo-root>
```

Every EP declares expected branch, material ref, base branch, observed base ref, `RECHECK_BEFORE_WRITE` and optional drift receipt.

Base drift classifications:

```text
DISJOINT
WITHIN_QUALIFIED_BOUNDARY
OVERLAPPING
UNKNOWN
```

`DISJOINT` may preserve writes. `WITHIN_QUALIFIED_BOUNDARY` requires durable qualification and confirmation; pending confirmation is READ_ONLY. `OVERLAPPING | UNKNOWN` withhold WRITE until reconciliation. Commit count is never safety evidence.

## State planes

`REPO_STATE` carries independent planes:

```text
EXECUTION — state, can_continue, material_authority, next action
QUALITY   — maintainability/design/UX findings
EVIDENCE  — what actually ran/proved/did not run
STOP      — true hard stop only
```

`can_continue: true + READ_ONLY` is valid. `NOT_RUN` is evidence truth, not automatically a stop.

Hard stops are reserved for real inability to proceed safely:

```text
OWNER_DECISION_REQUIRED
ESSENTIAL_INPUT_MISSING
AUTHORITY_VIOLATION
PROTECTED_INVARIANT_FAILURE
WRITE_COLLISION
SUPERSEDED_EP
ROADMAP_CONFLICT
REPOSITORY_STATE_CONFLICT
UNSAFE_ENGINEERING_RESULT
```

An active hard stop cannot retain WRITE.

## Checkpoints and exact evidence

Checkpoint successor modes:

```text
SERIAL
PARALLEL
JOIN
NONE
```

Checkpoint evidence is bound to `execution_basis.material_ref`. PASS/FAIL/NOT_RUN observed on another material head cannot silently qualify the current checkpoint. NOT_RUN carries an explicit reason.

## Parallel execution

Parallel work requires explicit Owner approval of a named plan and ASCII topology. Each lane declares unique route/branch/worktree, WP/EP, exclusive write domains and shared read domains. Overlapping writes require a specific Owner-approved exception.

Lane completion uses `JOIN`; integration starts only after all approved lane checkpoints converge and integration is the sole computed frontier.

If any lane becomes stale/invalid/unauthorized before convergence, the old plan loses material-write authority as a whole. A `PARALLEL_REPLAN` classifies every predecessor lane, retains completed checkpoints, transfers unresolved acceptance/evidence exactly, recomputes the frontier and produces either no route, one serial successor, or a newly Owner-approved parallel plan. Old plan branches/worktrees do not remain executable merely because they still exist.

## Issue projection

`ISSUE_GRAPH.yaml` models GitHub coordination relationships including parent/child, dependencies and evidence-preserving supersession. GitHub state is separate from engineering lifecycle state.

The issue node records last verified external state:

```text
github_state = ABSENT | OPEN | CLOSED | UNKNOWN
```

`ABSENT` is valid before issue creation. `UNKNOWN` requires a prior locator and means the external state must be re-observed. A CREATE attempt does not make the node OPEN.

`PARENT_OF` is an acyclic single-parent projection tree with revision-bound direct-child rollups. Parent closure cannot hide a child whose GitHub projection is not CLOSED.

A → B → C supersession must preserve inherited unresolved acceptance/evidence exactly or record explicit durable resolution. Silent drop, status/basis mutation, branching successors and cycles are invalid.

## GitHub Program Projection

When external GitHub coordination is required, `REPO_STATE.projection` points to one current immutable `GHGEN-*` file. A generation contains stable `GHOP-*` operations:

```text
CREATE | LINK | UPDATE | PUBLISH_HANDOVER |
SUPERSEDE | REVISE | CLOSE | REOPEN
```

The required mutation order is:

```text
validate current generation
→ select one dependency-ready GHOP
→ persist ATTEMPTED_UNCONFIRMED BEFORE external write
→ perform exactly that GitHub action
→ read external state back
→ write GITHUB_OBSERVATION
→ reconcile verified result into GHOP / ISSUE_GRAPH / REPO_STATE
→ only then select another GHOP
```

Never treat a connector response alone as convergence. Verified readback is the reconciliation boundary.

If an external call times out or crashes after the attempt journal was written, do **not** create a fresh operation or retry blindly. Reconcile the same `GHOP-*` using its stable idempotency key, verified locator and/or `<!-- relay-operation:GHOP-* -->` marker. A verified readback may create a repository `READBACK_RECOVERY:*` receipt when the connector receipt itself was lost.

A body hyperlink is not proof of a provider-native parent/sub-issue relationship. When a required native LINK cannot be created or verified by the available integration, leave projection incomplete and report the external capability limitation rather than claiming success.

When repository desired state advances, activate a new `GHGEN-*`. The predecessor generation becomes immutable SUPERSEDED, any old retryable GHOP loses publication authority, and history preserves whether it was superseded before publication, after an uncertain attempt, or after an unconfirmed publication receipt.

Read `operating-model/github-program-projection.md` and `operating-model/issue-projection.md`.

## Projection convergence

Required external projections use stable generation IDs and states:

```text
NOT_REQUIRED
PENDING
PUBLISHED_UNCONFIRMED
IN_SYNC
STALE
```

Repository truth may advance while an external surface is stale. Top-level projection fields describe the newest desired generation; `observed` records the older verified external generation; intermediate desired generations move to immutable superseded history with no retry authority. Publish/reconcile only the newest authorized generation.

Projection lag or unavailable external relationship capability does not rewrite engineering truth or automatically create a hard stop, but it prevents `HANDOVER_READY` when the projection is required.

## Progress and source-derived handover

Progress is calculated only:

```text
Acceptance Criterion → implementation step → EP → Work Package → Phase → Objective → Overall Roadmap
```

`PROGRESS.yaml` is authority. `REPO_STATE` percentages are checked mirrors only. Status, handover and structured report projection derive from repository authority objects rather than generated prose.

Approved scope/denominator changes create a new Progress Basis. Do not preserve a flattering percentage by rewriting completed work.

## Relay durability

Assume conversation can disappear at any time.

Before engineering writes, durable roadmap/EP-or-plan/discovery/inputs/oracles/scope/acceptance must exist and `MATERIAL_WRITE_READY` must pass for the current candidate/live checkout.

At custody transfer:

```text
checkpoint
→ roadmap/progress/issues reconciliation
→ frontier recomputation
→ successor EP/parallel route/join/replan/terminal disposition
→ semantic baton validation
→ QSET when fresh qualification is required
→ BATON_READY
→ required projection convergence
```

A successor candidate later creates DISC/QUAL/TC evidence independently.

## Safe bootstrap and V2 migration

Bootstrap is dry-run by default and never fabricates executable work. It creates `INITIALIZING`, no EP and `material_authority: NONE` until roadmap/frontier reconciliation creates a genuine V2.5 work contract.

V2 migration is evidence-first: inventory legacy state, reconcile Owner intent/unresolved work, establish an explicit V2.5 Progress Basis, compute a DETAILED frontier and create a genuine semantic V2.5 EP. Never auto-promote a V2 endpoint or copy narrative progress as calculated progress.

## Human handover

Generated views report source-derived Objective → Phase → WP → Step → AC progress, lifecycle, current EP or lanes, execution/quality/evidence/stop state, baton/projection/handover readiness, ordered exact next work, predecessor join/replan/continuity where relevant, qualification evidence when relevant, and `conversation context required: NO`.

WP-07 will translate the same machine truth into plainer Owner-facing language; generated views never become authority.

## Validation entrypoints

```bash
python skills/engineering-pr-delivery-v2.5/scripts/validate_relay_conformance.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/cold_start_check.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_baton_readiness.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_discovery_receipt.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_question_set.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_qualification_receipt.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_takeover_certification.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py <repo-root> --candidate-id <agent-instance-id>
python skills/engineering-pr-delivery-v2.5/scripts/validate_projection_convergence.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_github_projection.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_github_generation_history.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/github_projection_next.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_parallel_join.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_parallel_replan.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/bootstrap_relay.py <manifest> <repo-root>
```

The Common workflow `.github/workflows/engineering-pr-delivery-v2.5.yml` must explicitly execute both root unit discovery and dedicated `tests/stress/` discovery. Compilation alone is not stress-test evidence. See `operating-model/ci-evidence-correction.md`.

A green generic workflow proves only that the repository-neutral protocol suite executed successfully; it does not substitute for downstream product/engineering validation.
