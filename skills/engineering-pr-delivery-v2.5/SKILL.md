---

## REQUEST MODE DISPATCH — FIRST ACTION

Before applying any other section of this skill, classify the user's request.

### THREE_PASS_GENERATOR

Enter this mode when the user asks to use, generate from, apply, or review:

```text
skills/engineering-pr-delivery-v2.5/schemas/three-pass-prompt-generator.schema.md
```

or explicitly asks for "3 pass", "three-pass", "Prompt 1 / Prompt 2 / Prompt 3", or complex Q1–Q5 questions under that schema.

In this mode:

1. fetch the current schema from `main`;
2. before target reasoning, emit/verify the schema's mandatory execution handshake with protocol revision `TPG-3P-2026-09-19-R1`, `GENERATOR MODE = THREE_PASS_ONLY`, `LIVE_THIS_RUN`, and the actual fetched schema SHA;
3. set `GENERATOR MODE = THREE_PASS_ONLY`;
4. follow that schema as the complete local protocol;
5. use repository/issue material only as target evidence;
6. do **not** apply the engineering-delivery certification/takeover sections of this skill;
7. validate the generated artifact with `validate_three_pass_prompt_output.py`;
8. return the artifact and STOP.

No other section below may add stages, gates, receipts, qualification packages, route metadata, evaluator requirements, or takeover machinery to a THREE_PASS_GENERATOR artifact.

### ENGINEERING_DELIVERY

Use the remaining engineering-delivery protocol only when the user is actually asking to execute/manage engineering delivery rather than generate three-pass prompts.

---

name: engineering-pr-delivery-v2.5
description: Roadmap-first engineering relay for durable zero-chat multi-agent delivery, with semantic execution packages, independent takeover certification, evaluated engineering qualification, calculated progress, crash-safe GitHub projection, quality evidence, and serial-by-default material execution.
---

# Engineering PR Delivery v2.5 — engineering relay with a dynamic overall roadmap

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
→ incoming candidate DISC / QUAL / TC evidence
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

## Dynamic roadmap

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

EP discovery instructions use `DSTEP-*`. Incoming candidate evidence uses `DISC-*`.

A Discovery Receipt is bound to candidate, exact route, roadmap/protocol/material basis, semantic EP digest, `REPO_PROFILE` digest, predecessor-baton digest, required DSTEP coverage, and expected output names. `conversation_context_used` must be false.

A `TC-*` Takeover Certification records candidate, preparer, evaluator, DISC pointer, optional QUAL pointer/digest, exact route/basis, objective checks, and final PASS/FAIL. Candidate self-preparation/self-certification is invalid. Validators reopen evidence and recompute current basis; YAML assertions are not authority.

## Three-pass prompt-generator bootstrap

The three-pass prompt generator is a **standalone live-schema workflow**, not a remembered prompting pattern.

When this mode is active, the schema is the exclusive repository-local protocol for the generated artifact; the normal engineering-delivery QSET/QUAL/takeover machinery below is inactive.

Canonical schema:

```text
skills/engineering-pr-delivery-v2.5/schemas/three-pass-prompt-generator.schema.md
```

When a user asks to generate, regenerate, review, or apply the three-pass prompts/schema:

1. **Fetch the canonical schema from current `main` in the same run.**
2. Before reading the target, produce the schema execution handshake required by the live schema, including protocol revision `TPG-3P-2026-09-19-R1` and the actual fetched SHA.
3. Record the same fetched content/blob SHA in the generated output's shared `SCHEMA BASIS`.
4. Never reconstruct the generator from conversation memory, a previous generated answer, an assistant summary, an older commit, or an earlier fetched copy.
5. Resolve targets only from user authority: current user message → earlier user-supplied target/lot → user-supplied canonical URL/name. A previous assistant guess is never target authority.
6. Execute the fetched schema literally, including its visible preflight and all gates.
7. Before returning the generated prompts, validate the complete draft with:
   ```bash
   python skills/engineering-pr-delivery-v2.5/scripts/validate_three_pass_prompt_output.py <generated-markdown> --expected-schema-sha <fetched-content-sha>
   ```
8. If validation fails, do **not** return the draft. Rebuild it from the fetched current schema.

The validator is deliberately structural. It rejects stale control-path signatures before prose quality is considered, including missing schema basis/preflight, retired `TASK_ARTIFACT`/target-scope machinery, register-centric blind-pass wording, missing issue problem-kernel/quarantine gates, or a Prompt 3 that predetermines a reconciled register.

For `ISSUE_TASK`, the required blind-pass control is:

```text
Prompt 1 =
ISSUE TASK CONTRACT
+ PROBLEM KERNEL
+ TARGET ANCHORS
+ PROBLEM WITNESS when available
+ HUMAN OUTCOME
+ GENUINE CONSTRAINTS
- CURRENT ANSWER QUARANTINE
- WITNESS INTERPRETATION QUARANTINE
```

A current artifact being a register, matrix, roadmap, checklist, or decision package does not make that artifact type the Prompt-1 imagination object.

Prompt 1 must also be **method-invisible**. The future agent should receive the human/domain situation directly. Do not narrate the generator mechanics with phrases such as "later pass", "fixed independent reference", "do not inspect the repository", or "you will be held to this picture". The outer bootstrap/schema controls blindness; Prompt 1 should feel like a real practitioner problem.

For `ISSUE_TASK`, the ISSUE TASK CONTRACT is mandatory: why the issue exists now, its stated starting scenario, responsible actor/job, exact owned question, non-goals/ownership boundary, and why it differs from parent/sibling issues. Do not abstract those away merely because they came from the target issue.

For `ISSUE_TASK`, actively search the target for a **PROBLEM WITNESS**: benchmark case, hand-calculation case, drawing, failing input, trace, dataset, screenshot/journey, dependency case, or other concrete example that materially exposes the owned question. When one exists, Prompt 1 should normally make the future agent independently work/reproduce that witness before returning to the issue-level judgement. Keep the witness payload and reported result-as-claim; quarantine today's interpretation/recommendation. If a real witness exists, do not replace it with invented plausible values or abstract consultancy questions.

A selected witness must have an **INDEPENDENT WORK PRODUCT** such as a hand calculation, derivation, comparison table, trace, reconstructed journey, dependency map, or falsifier set.

When the user invokes `complex` three-pass mode, Q1–Q5 means the schema's **human Prompt-1 reasoning lenses only**. If Q1–Q5 labels are shown, they must be short, natural, target-specific practitioner questions/tasks. Never surface taxonomy labels such as `PRODUCTION_PATH`, `ENGINEERING_PROBLEM`, `BOUNDARIES_INVARIANTS`, `VERIFICATION`, or `FIRST_SAFE_SLICE`, and never emit protocol metadata such as `required_output_keys`, `payload.source`, or `evidence_required`. Do not create a formal relay `QSET-*`, qualification/admission gate, route/EP/digest metadata, `TO_BE_BOUND` placeholders, or evaluator requirement. Formal QSET/QUAL belongs to relay takeover certification, not three-pass prompt generation.

This bootstrap requirement sits **outside** the schema by design: a stale copy of the schema cannot be trusted to tell an agent to fetch a newer copy of itself.

## Engineering qualification — QSET / QUAL

Fresh qualification is mandatory when:

```text
PHASE_CHANGED
OR
MATERIAL_QUALIFICATION_BOUNDARY_CHANGED
```

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

## State planes

`REPO_STATE` carries independent planes:

```text
EXECUTION — state, can_continue, material_authority, machine next-action hint
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
python skills/engineering-pr-delivery-v2.5/scripts/validate_three_pass_prompt_output.py <generated-markdown> --expected-schema-sha <current-schema-sha>
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
