---

## REQUEST MODE DISPATCH — FIRST ACTION

### PLAN_FOR_HANDOVER — COMBINED CONTROL TRANSACTION

If the Owner says:

```text
Plan for Handover
```

or:

```text
Plan for Handover, complex project
```

this is an explicit **combined engineering-delivery + prompt-generation workflow**. It is the narrow exception to the normal three-pass isolation rule below.

Execute in this order:

```text
normal Owner progress publication
→ freeze current source-derived handover basis
→ resolve owned work: verified current GitHub issue, else active task/EP, else current roadmap WP
→ derive all still-pending INTENT from current repository truth
→ create or incrementally update the handover GitHub issue through the existing GHGEN/GHOP publication path
→ verify issue identity and relationship/reference by provider readback
→ only then enter the standalone three-pass generator using the verified handover issue as TARGET
→ return the schema-defined copy-pasteable artifact
```

Use:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/plan_handover.py <repo-root> \
  --command "Plan for Handover" \
  --owner-requirement "<user-authored requirement from this session>"
```

The planner is derived coordination state. Its INTENT does not replace roadmap, EP, PROGRESS, checkpoint/evidence, ISSUE_GRAPH, or ODR authority.

For the same active ownership boundary, the stable handover key means a later command updates the same valid open handover issue rather than creating a duplicate. Recompute pending INTENT every time; completed work must not remain pending merely because older issue prose still lists it.

The handover issue must retain durable input/benchmark locations, expected outcomes, textual constraints/boundaries, and relevant user-authored core requirements from the current session. Never publish credentials/secrets or assistant hidden reasoning.

After verified handover-issue readback, rerun the planner with `--handover-issue-url <verified-url>` to produce the exact standalone-generator input.

The legacy V2.5 three-pass path is a redirect only. For the generator substep fetch current `main`:

```text
skills/three-pass-prompt-generator/SKILL.md
skills/three-pass-prompt-generator/schema.md
```

and obey the live schema revision/SHA. Do not reconstruct it from this skill.

If the command includes the explicit word **complex** (for example `Plan for Handover, complex project`), set complex mode ON. The final artifact still has exactly three prompts; Prompt 1 additionally shows visible target-specific Q1–Q5 as required by the live standalone schema. Plain `Plan for Handover` does not inherit complex mode.

The GitHub issue publication performed inside this compound transaction must not recursively trigger another full `Plan for Handover` transaction.

### THREE_PASS_GENERATOR

If the user asks for three-pass prompt generation, names the legacy three-pass schema path, asks for Prompt 1 / Prompt 2 / Prompt 3, or requests complex Q1–Q5 under the three-pass method **and this is not the `Plan for Handover` combined command above**:

**leave this skill immediately.**

Canonical standalone launcher:

```text
skills/three-pass-prompt-generator/SKILL.md
```

Canonical standalone schema:

```text
skills/three-pass-prompt-generator/schema.md
```

Do not read or apply the engineering-delivery sections below for that request.

Three-pass generation and engineering-delivery execution are mutually exclusive modes.

### ENGINEERING_DELIVERY

Only continue below when the user is actually asking to execute/manage engineering delivery rather than generate three-pass prompts.

## Governing objective

A replacement agent with no conversational history must be able to recover Owner intent, roadmap position, authorized work, inputs/oracles, scope, predecessor custody, evidence, quality obligations, acceptance, and exact next work from repository state alone; independently prove takeover; execute only when live write readiness permits; checkpoint reality; reconcile roadmap/progress/issues; and leave an equally strong baton.

Conversation is acceleration, never custody.

## Repository-agnostic core

Common contains portable relay policy, schemas, templates, validators, renderers, and synthetic tests. Do not encode downstream repository names, issue IDs, product formulas, or workflow-specific exceptions. Real repositories are read-only black-box stress sources unless the Owner separately authorizes adoption. Reduce every discovered weakness to a repository-neutral invariant plus synthetic regression before changing Common protocol logic.

## Authority chain

```text
explicit Owner intent / ODR
→ OVERALL_ROADMAP.yaml + roadmap revision
→ executable frontier
→ semantic EP or Owner-approved parallel router
→ BATON_READY
→ execution candidate DISC / QUAL / TC evidence
→ TAKEOVER_CERTIFIED(route,candidate)
→ live route + Git basis + MATERIAL_WRITE_READY
→ implementation / read-only reconciliation as authorized
→ applicable quality procedures + tests/oracles
→ QRV-* quality review
→ checkpoint/evidence
→ roadmap / progress / issue reconciliation
→ required external projection convergence
→ source-derived report / communication / Owner-change views
→ ZERO_CONTEXT_RECONSTRUCTION
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
    ROADMAP_EVENTS.yaml        # optional append-only material-event history
    revisions/**
    owner-decisions/**
  execution-packages/**
  certifications/
    discovery/**
    qualification/**
    takeover/**
  quality/**
  checkpoints/**
  parallel/**
  drift/**
  projection/
    generations/**
  reports/**
  generated/**
```

`REPO_STATE.yaml` is the deterministic bootstrap locator. It does not replace the authority objects it references.

## Lifecycle and execution policy

Relay lifecycle:

```text
INITIALIZING — scaffold exists; no material EP is executable
ACTIVE       — one serial frontier WP and one active EP
PARALLEL     — Owner-approved parallel router; lane EPs live in the plan
IDLE         — no executable material work currently exists
TERMINAL     — roadmap work is complete
```

`INITIALIZING | IDLE | TERMINAL` have no active material EP. `ACTIVE` requires `SERIAL`. `PARALLEL` requires `OWNER_APPROVED_PARALLEL`, an approved plan, and at least two current frontier WPs.

Material execution is **serial by default**. Do not infer parallelism from apparent independence.

## Mandatory task status heartbeat

For every active task, publish an Owner progress status at **minute 25 from task start** unless the Owner explicitly overrides the cadence.

At task start:

1. create a one-time 25-minute status timer;
2. continue work normally;
3. publish material events immediately when they occur;
4. if the task is still active when the timer fires, run the Owner publication path with `--force-record` so even no-change state is visible;
5. if the task completed earlier, its completion publication satisfies the requirement and the timer may be cancelled.

Owner overrides may set another interval or disable the time-based heartbeat for that task. The override must be explicit and attributable to the Owner.

Missing timer capability must be reported as `STATUS_TIMER_UNAVAILABLE`; never pretend a timer was scheduled.

## Task → roadmap admission gate

Every incoming task must be reconciled to roadmap authority **before an executable EP is accepted**.

The agent must:

1. search for the current V2.5 roadmap from `REPO_STATE.roadmap.path` and inspect any existing roadmap/history needed to understand the task;
2. determine whether the task:
   - maps to an existing work package;
   - requires revising an existing work package;
   - requires adding a new execution work package under an existing concept;
   - or arrives in a repository with no usable roadmap and therefore requires roadmap creation/bootstrap;
3. update/create the roadmap when the task is not already represented;
4. reconcile Progress Basis, issue projection, frontier and active EP continuity when the roadmap changes;
5. record `roadmap_source.task_admission` in the EP with the disposition, searched paths and durable basis.

Allowed dispositions:

```text
MAPPED_EXISTING_WP
REVISED_EXISTING_WP
ADDED_EXECUTION_WP
CREATED_ROADMAP
```

Silence is invalid.

`NO_CONCEPT_CHANGE` does **not** mean `NO_ROADMAP_UPDATE`. A newly discovered execution task can leave Owner intent/objective/phase unchanged while still requiring a new or revised work package in `OVERALL_ROADMAP.yaml`.

If no V2.5 roadmap exists, first search for existing repository planning/roadmap material that may need reconciliation. If no usable authority exists, use the safe bootstrap path and reconcile it into a DETAILED executable roadmap; do not fabricate an executable EP directly from the user's sentence.

## Dynamic roadmap

The roadmap is concept/outcome authority, not a task diary. In the current hierarchy, objectives and phases are the concept-level anchors; work packages are execution units.

Material programme history may be appended to `agents/relay/roadmap/ROADMAP_EVENTS.yaml`. Events link upward to objective/phase concepts and sideways to WP/EP/checkpoint/issue/PR execution facts. They are a derived durable history index and never mutate concept truth by themselves.

Major work events follow:

```text
record material event
→ reconcile execution
→ evaluate concept impact
→ revise roadmap only when the concept itself changed
```

A discovered additional task under an existing concept is normally `NO_CONCEPT_CHANGE + NEW_EXECUTION_WORK`, not a structural roadmap rewrite. `CONCEPT_CHANGE_PROPOSED` does not apply a change; `CONCEPT_CHANGE_APPLIED` must point to the real roadmap revision.

Read `operating-model/dynamic-roadmap.md`.

Roadmap mutation classes:

```text
EXECUTION_DERIVED_STATUS
ENGINEERING_DISCOVERY_PROPOSAL
OWNER_INTENT_MUTATION
```

Agents may apply factual status updates, may propose structural discoveries, and require an applied Owner Decision Record for Owner-intent mutations. Material revisions reconcile dependencies, active-EP continuity/staleness, issues, Progress Basis, and the computed frontier. `frontier_after` must equal the frontier computed from the resulting roadmap.

Owner deferral is not technical satisfaction. A `DEFERRAL` keeps named items pending and does not itself grant write authority.

For an Owner-intent mutation, `ODR.change_intake` records the semantic before/after concept while the roadmap revision remains authoritative for actual structural effects. `OWNER_CHANGE.md` is derived only.

## Semantic Execution Package

Every serial EP and approved parallel lane EP is a forward work contract for one roadmap work package. It contains:

- identity and exact Git basis;
- roadmap source/frontier origin;
- outcome and context capsule;
- executable `DSTEP-*` repository discovery;
- typed current/future inputs with authority, source, editability, applicability, resolution, and stale conditions;
- benchmark/oracle contracts with payload, expected result, tolerance/exactness, and independence;
- allowed writes/reads, protected invariants, prohibited scope, and Owner-reserved scope;
- structured anti-drift;
- exact implementation steps mapped to inputs, ACs, and tests;
- complete quality applicability routing;
- acceptance and validation contracts;
- optional `qualification_boundary`;
- source-bound report payloads;
- ordered `next_work.steps[]` with targets, inputs, tests/oracles, acceptance, expected result, and stop/reconciliation conditions;
- checkpoint and successor duties.

Exactly one predecessor baton is active: checkpoint, parallel join, or parallel replan. EP and CP are different objects and never substitute for each other.

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
+ current-slice inputs/oracles ready
+ complete discovery/scope/report/successor contract
+ valid QSET when fresh qualification is required
+ no chat dependency
```

A baton can be ready before the future replacement agent exists.

### TAKEOVER_CERTIFIED(route,candidate)

Candidate-specific proof:

```text
BATON_READY
+ current DISC receipt PASS
+ current QUAL receipt PASS when required
+ current TC receipt PASS
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

EP discovery instructions use `DSTEP-*`. Execution-candidate evidence uses `DISC-*`.

A Discovery Receipt is bound to candidate, exact route, roadmap/protocol/material basis, semantic EP digest, `REPO_PROFILE` digest, predecessor-baton digest, required DSTEP coverage, and expected output names. `conversation_context_used: false` means the receipt is grounded in repository sources rather than chat authority; the candidate may be incoming or continuing.

A `TC-*` Takeover Certification records candidate, document preparer, evaluator, DISC pointer, optional QUAL pointer/digest, exact route/basis, objective checks, and final PASS/FAIL. The candidate may assemble its own TC record, including after preparing the EP; document authorship is not certification authority. Self-evaluation remains invalid, and validators reopen evidence and recompute current basis.

## Three-pass prompt-generator compatibility note

Three-pass prompt generation is not defined in this skill.

Use only:

```text
skills/three-pass-prompt-generator/SKILL.md
```

Do not continue reading this skill for three-pass generation.

## Owner progression without Q1–Q5

The following Owner phrases are semantic aliases, case-insensitive and punctuation-insensitive:

```text
Proceed next, No Qs
Proceed next No Qs
Proceed next, No Q1 to Q5
Proceed next No Q1 to Q5
Proceed next, No Q1-Q5
```

Meaning:

```text
continue the authorized task
+ do not create, refresh or display Q1–Q5 for this progression step
```

If a completed standalone three-pass sequence already carries `THREE_PASS_COMPLETE`, QSET/QUAL is genuinely not applicable.

Otherwise, when fresh qualification is still required, record `question_policy: SUPPRESSED_BY_OWNER`, explicit Owner basis, and no question-set reference.

This is a defer/suppress command, not a PASS. Safe read-only, coordination, evidence-gathering or other non-material work may continue, but `BATON_READY`, `TAKEOVER_CERTIFIED`, and material WRITE remain unavailable when they depend on unsatisfied qualification.

Do not respond to these commands by asking another set of questions.

## Engineering qualification — QSET / QUAL

Fresh qualification is mandatory when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

**except when the current task carries the completed standalone three-pass terminal disposition**:

```text
THREE_PASS_REASONING_STATUS: THREE_PASS_COMPLETE
FOLLOW_ON_QUALIFICATION_QUESTION_SET: NOT_APPLICABLE
```

For that case, the incoming EP records:

```yaml
qualification_boundary:
  required: false
  not_applicable_reason: THREE_PASS_COMPLETE
  basis:
    - "THREE_PASS_COMPLETE: <durable task/issue/session basis>"
  question_set: null
```

Do not create a `QSET-*` or `QUAL-*` after a completed three-pass sequence, whether Prompt 1 used visible Q1–Q5 or not. The three-pass exemption removes redundant questioning only; DISC/TC, evidence, Owner authority, source authority, tests, local execution and `MATERIAL_WRITE_READY` still apply.

A same-phase material boundary change includes material change in production path, engineering authority, numerical method, protected invariant, input authority, or verification/oracle class.

Inline `phase_transition.questions` is retired. A required EP boundary references a durable `QSET-*` bound to the exact route and EP contract digest.

The transaction is:

```text
outgoing/authorized preparer creates QSET
→ incoming candidate answers from repository only
→ independent/deterministic evaluation
→ QUAL-* receipt
→ TC cites QUAL id/path/digest
```

Q1–Q5 semantics:

```text
Q1 actual production path, state owner, authority source, downstream consumer
Q2 engineering reconstruction; quantitative work carries concrete payload values
Q3 explicit mutation + protected invariant + exact falsifier
Q4 independent verification using incoming benchmark/oracle evidence
Q5 exact first bounded change + predicted before/after verification
```

The candidate cannot prepare its own QSET or be its own `INDEPENDENT_AGENT` evaluator. QUAL PASS requires all five evaluations PASS. Editing QUAL after TC issuance invalidates takeover via digest mismatch.

Read `operating-model/phase-transition.md`.

## Live Git routing and drift

Before material writes:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py <repo-root> --candidate-id <agent-instance-id>
python skills/engineering-pr-delivery-v2.5/scripts/resolve_execution_route.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/inspect_git_context.py <repo-root>
```

Every EP declares expected branch, material ref, base branch, observed base ref, `RECHECK_BEFORE_WRITE`, and optional drift receipt.

Base drift classifications:

```text
DISJOINT
WITHIN_QUALIFIED_BOUNDARY
OVERLAPPING
UNKNOWN
```

`DISJOINT` may preserve writes. `WITHIN_QUALIFIED_BOUNDARY` requires durable qualification and confirmation; pending confirmation is READ_ONLY. `OVERLAPPING | UNKNOWN` withhold WRITE until reconciliation. Commit count is never safety evidence.

## Environment-blocked work — delegate, publish, and check back

When an authorized next action cannot execute in the current environment — for example Python cannot launch the required `.mjs` tooling, a browser/UI check needs a real desktop/browser session, or a local Git/runtime dependency is unavailable — do not stop at `NOT_RUN` and do not ask the Owner to reconstruct the task.

Represent the blocked action as `next_work.steps[].execution_requirement` and include a `delegation` contract.

The executing agent must:

1. create a complete copy-pasteable prompt for a local agent with the exact repository/ref/basis, working directory, command or instruction, boundaries, expected evidence, success condition and response format;
2. publish that prompt to the **current work issue**:
   - use a COMMENT for a bounded one-shot validation/check;
   - use a SUB_ISSUE when the delegated work has multiple steps, its own lifecycle, or needs independently trackable follow-up;
   - if native sub-issue creation/readback is unavailable, fall back to a verified issue COMMENT rather than claiming an unverified relationship;
3. read back the GitHub publication before claiming delegation exists;
4. require the local agent to post its result/evidence back to that same issue/sub-issue location;
5. create a one-time response-check timer:
   - **30 minutes** for a short direct command, focused browser check, or small verification expected to finish quickly;
   - **60 minutes** for setup/build/install/manual UI or multi-step local verification;
   - for longer work, use 60 minutes as the first check and re-evaluate from actual progress rather than scheduling an unbounded polling loop;
6. when the timer fires, read the issue/sub-issue:
   - if evidence is present, validate it and resume/reconcile the blocked work;
   - if no response is present, report WAITING truthfully and schedule another check only when it remains useful.

If timer/scheduling capability is genuinely unavailable, do not claim a timer exists. Publish the intended 30/60-minute check interval and surface `TIMER_UNAVAILABLE` to the Owner.

The local-agent prompt is an execution handoff, not a new qualification questionnaire.

## State planes

`REPO_STATE` carries independent planes:

```text
EXECUTION — state, can_continue, material_authority, machine next-action hint
QUALITY   — maintainability/design/UX findings
EVIDENCE  — what actually ran/proved/did not run
STOP      — true hard stop only
```

`can_continue: true + READ_ONLY` is valid. `NOT_RUN` is evidence truth, not automatically a stop.

`material_authority` is route/repository-level, not candidate-specific. Missing DISC/QUAL/TC for one candidate must not be encoded by downgrading the route to READ_ONLY; candidate-specific admission is handled by `TAKEOVER_CERTIFIED` and the live write gate.

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

## Quality procedures and QRV

Every executable EP partitions the entire built-in quality procedure library exactly once into `quality.applicable[]` and `quality.not_applicable[]`. Applicable procedures require reason + review focus; explicit non-applicability requires a reason and does not trigger ceremonial execution.

Before checkpoint publication, applicable procedures are evidenced in `QRV-*`, bound to exact EP digest, roadmap revision, material ref, and router snapshot.

Procedure results are `CLEAR | FINDINGS | NOT_RUN`. `NOT_RUN` remains evidence/quality truth and is not automatically a stop. Severity alone never creates a hard stop. A quality finding may block execution only through a valid existing hard-stop category with durable basis.

Unresolved findings transfer exactly through successor handover. Read `operating-model/quality-procedures.md`.

## Checkpoints and exact evidence

Checkpoint successor modes:

```text
SERIAL
PARALLEL
JOIN
NONE
```

Checkpoint evidence is bound to `execution_basis.material_ref`. PASS/FAIL/NOT_RUN observed on another material head cannot silently qualify the current checkpoint. NOT_RUN carries an explicit reason. Checkpoints bind QRV by id/path/digest when quality review is applicable.

## Parallel execution

Parallel work requires explicit Owner approval of a named plan and ASCII topology. Each lane declares unique route/branch/worktree, WP/EP, exclusive write domains, and shared read domains. Overlapping writes require a specific Owner-approved exception.

Lane completion uses `JOIN`; integration starts only after all approved lane checkpoints converge and integration is the sole computed frontier.

If any lane becomes stale/invalid/unauthorized before convergence, the old plan loses material-write authority as a whole. A `PARALLEL_REPLAN` classifies every predecessor lane, retains completed checkpoints, transfers unresolved acceptance/evidence exactly, recomputes the frontier, and produces either no route, one serial successor, or a newly Owner-approved parallel plan. Old plan branches/worktrees do not remain executable merely because they still exist.

## Progress and source-derived handover

Progress is calculated only:

```text
Acceptance Criterion → implementation step → EP → Work Package → Phase → Objective → Overall Roadmap
```

`PROGRESS.yaml` is authority. `REPO_STATE` percentages are checked mirrors only. Approved denominator changes create a new Progress Basis; never preserve a flattering percentage by rewriting completed work.

Every executable EP has structured ordered `next_work.steps[]`. Report/status/handover renderers derive from repository authority objects rather than generated prose.

## Issue graph and GitHub projection

`ISSUE_GRAPH.yaml` models coordination relationships and keeps engineering lifecycle separate from verified GitHub state:

```text
github_state = ABSENT | OPEN | CLOSED | UNKNOWN
```

Parent/child projection is acyclic and single-parent. Parent closure cannot hide a non-closed child. Multi-generation supersession preserves unresolved acceptance/evidence exactly or records explicit durable resolution.

When external GitHub coordination is required, `REPO_STATE.projection` points to one current immutable `GHGEN-*` containing stable `GHOP-*` operations:

```text
CREATE | LINK | UPDATE | PUBLISH_HANDOVER |
SUPERSEDE | REVISE | CLOSE | REOPEN
```

Mutation order is:

```text
validate current generation
→ select one dependency-ready GHOP
→ persist ATTEMPTED_UNCONFIRMED before external write
→ perform exactly that provider action
→ read external state back
→ write GITHUB_OBSERVATION
→ reconcile verified result
→ only then select another GHOP
```

Connector response alone is not convergence. A timeout/unknown outcome must reconcile the same stable operation before retry. A body hyperlink is not proof of a provider-native relationship. Superseded generations lose retry authority.

Read `operating-model/github-program-projection.md` and `operating-model/issue-projection.md`.

## Projection convergence

Required external projections use:

```text
NOT_REQUIRED
PENDING
PUBLISHED_UNCONFIRMED
IN_SYNC
STALE
```

Repository truth may advance while external coordination is stale. Projection lag does not rewrite engineering truth or automatically create a hard stop, but required lag prevents `HANDOVER_READY`.

## Human communication and Owner changes

One source-bound report projection feeds one communication projection:

```text
repository authorities
→ report projection
→ communication projection
   ├── TECHNICAL_STATUS.md
   └── OWNER_STATUS.md
```

Technical status retains protocol precision. Owner status uses plain engineering/product language for capability, purpose, protected scope, evidence gaps, quality risks, genuine decisions, stops, progress, and exact next work. Owner-reserved choices are not fabricated as immediate decision requests.

Material Owner changes use ODR authority + roadmap transaction authority. `OWNER_CHANGE.md` is a derived impact view showing previous/requested concept, retained/invalidated behavior, scope, roadmap/progress/issue impact, active-work disposition, resulting frontier, and whether the decision is applied.

Generated views never become authority.

## Zero-context release certification

The defining release proof is repository-only A → B → C across dependency-ordered work packages:

```text
Agent A with conversation
→ CP-A / EP-B / QSET-B
→ conversation removed
Agent B repository only
→ ZERO_CONTEXT_RECONSTRUCTION
→ DISC / QUAL / TC PASS
→ completes WP-B
→ CP-B / EP-C / QSET-C
→ conversation removed
Agent C repository only
→ ZERO_CONTEXT_RECONSTRUCTION
→ independent QUAL / TC PASS
```

The reconstruction must answer task purpose, Owner decisions, predecessor facts/limitations, uncertainty, input authority/editability, independent oracle, allowed/protected/prohibited scope, quality obligations/findings, evidence present/missing, tests/acceptance, first action, stale conditions, and exact next work.

Lifecycle certification covers ACTIVE, ACTIVE + RECONCILING, PARALLEL, ACTIVE + required projection STALE, IDLE, TERMINAL, with INITIALIZING covered by bootstrap/core tests. Recovery must never invent write permission.

Commands:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/zero_context_reconstruction.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_zero_context_reconstruction.py <repo-root>
```

Read `operating-model/relay-certification-matrix.md`.

## Safe bootstrap and V2 migration

Bootstrap is dry-run by default and never fabricates executable work. It creates `INITIALIZING`, no EP, and `material_authority: NONE` until roadmap/frontier reconciliation creates a genuine V2.5 work contract.

V2 migration is evidence-first: inventory legacy state, reconcile Owner intent/unresolved work, establish an explicit V2.5 Progress Basis, compute a DETAILED frontier, and create a genuine semantic V2.5 EP. Never auto-promote a V2 endpoint or copy narrative progress as calculated progress.

## Validation entrypoints

```bash
python skills/engineering-pr-delivery-v2.5/scripts/validate_relay_conformance.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/cold_start_check.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_zero_context_reconstruction.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_baton_readiness.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_discovery_receipt.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_question_set.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_qualification_receipt.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_takeover_certification.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/material_write_ready.py <repo-root> --candidate-id <agent-instance-id>
python skills/engineering-pr-delivery-v2.5/scripts/validate_quality_review.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_projection_convergence.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_github_projection.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_parallel_join.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_parallel_replan.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/bootstrap_relay.py <manifest> <repo-root>
```

For Common development / release consistency:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/self_consistency_audit.py .
```

The scoped workflow `.github/workflows/engineering-pr-delivery-v2.5.yml` must execute compilation, the self-consistency audit, root unit discovery, and dedicated `tests/stress/` discovery. Compilation alone is not test evidence. See `operating-model/ci-evidence-correction.md`.

A green generic workflow proves only that the repository-neutral protocol suite executed successfully; it does not substitute for downstream product, engineering calculation, release, or human UX acceptance.


### OWNER PROGRESS PUBLICATION — CONTROL RETURN

Before returning control to the Owner after a material work unit, use the canonical publisher:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/publish_owner_progress.py <repo-root> --apply
```

The publisher compares current source-derived report truth with the last durable Owner publication baseline at:

```text
agents/relay/publication/OWNER_PUBLICATION.yaml
```

The cursor is **derived coordination state only**. It records what source-derived state was last shown; it does not define what is currently true.

A publication is materially due after a change to accepted task progress, implementation result, evidence, quality/blocker/control state, current issue/delivery/custody, roadmap disposition, required Owner decision, external/local obligation, or exact next-work contract.

Repeated unchanged polling/retries do not advance the cursor. If control is returned with no material change, render the explicit `NO_MATERIAL_PROGRESS` Owner status; do not manufacture progress. Use `--force-record` only for an intentional heartbeat that should itself become the new publication receipt.

The Owner view must expose the deterministic delta before the normal current-state sections. It must explicitly say when acceptance/progress and implementation/files did not move.

`Plan for Handover` begins with this same publication transaction. Use:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/plan_handover.py <repo-root> \
  --command "Plan for Handover" \
  --apply-publication \
  --owner-requirement "<relevant user-authored requirement>"
```

The handover INTENT is derived only after that baseline has been published.


### PR DESCRIPTION CORRELATION — TASK-CLOSE INVARIANT

When PR delivery is required, every active engineering PR must contain the canonical V2.5 Issue↔EP correlation block.

Generate from repository truth:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/render_pr_correlation.py <repo-root>
```

A valid correlation is not merely an issue number and EP token in prose. Each row must prove:

```text
verified GitHub issue number
↔ ISSUE_GRAPH node
↔ roadmap work package
↔ EP roadmap_source.work_package
↔ EP id/path
```

with an explicit relationship (`IMPLEMENTS | INTEGRATES | VERIFIES | REMEDIATES`) and plain-language meaning.

After updating the provider PR body, read it back into `DELIVERY_OBSERVATION.description_contract`, then verify:

```bash
python skills/engineering-pr-delivery-v2.5/scripts/validate_delivery_observation.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/validate_pr_correlation.py <repo-root>
```

This verification is required at the end of each task/checkpoint before claiming delivery handback complete when PR delivery is applicable.

Every current active EP must be represented in at least one non-terminal tracked PR. The latest task-close checkpoint EP must be represented in a tracked PR correlation.

Track all current PR observations in `REPO_STATE.delivery.observations[]`. Every PR last observed as `DRAFT`, `OPEN`, or `UNKNOWN` must be carried forward in every Owner summary with its Issue↔EP correlation until provider readback records `MERGED` or `CLOSED`.

Do not infer disappearance from chat, branch changes, or a newer PR.
