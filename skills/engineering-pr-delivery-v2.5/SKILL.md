---
name: engineering-pr-delivery-v2.5
description: Roadmap-first engineering relay for durable multi-agent delivery. The repository owns a dynamic overall roadmap, deterministic executable frontier, self-contained execution packages, checkpoints, calculated progress, issue projection, owner-decision transactions, phase-transition qualification, and serial-by-default material execution.
---

# Engineering PR Delivery v2.5 — engineering relay with a dynamic overall roadmap

## Governing objective
A replacement agent entering the repository with no conversational history must be able to locate the authoritative overall roadmap, determine the current roadmap position/frontier, execute the authorized work, validate it, checkpoint reality, reconcile the roadmap, recompute the frontier, and leave a validated successor relay. Conversation is acceleration, never custody.

## Repository-agnostic core
The Common implementation is portable policy, not downstream-project code. Generic skill logic, schemas, templates and validators must not encode downstream repository names, issue numbers, branch names, product domains, formulas or application-specific workflow semantics. Real repositories are black-box validation/stress targets. When a stress target exposes a weakness, repair the generic invariant/validator and add a synthetic reproduction; do not special-case that repository. Read `operating-model/repository-agnosticism.md`.

## Authority order
```text
explicit Owner intent / Owner Decision Record
→ OVERALL_ROADMAP.yaml
→ executable frontier
→ current serial EP or Owner-approved parallel router
→ implementation
→ checkpoint/evidence
→ roadmap reconciliation
```
GitHub Issues are a coordination projection. They do not replace roadmap or repository authority.

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
  checkpoints/**
  parallel/**
  reports/**
  generated/**
```
`REPO_STATE.yaml` is the deterministic bootstrap locator: which roadmap, lifecycle state, current position, execution policy, and what—if anything—can execute now.

## Relay lifecycle
`REPO_STATE.relay_state` is exactly one of:
```text
INITIALIZING — relay scaffold exists; no material EP is executable yet
ACTIVE       — serial material work; exactly one frontier WP and one active EP
PARALLEL     — Owner-approved fork; REPO_STATE is a router and lane EPs live in the parallel plan
IDLE         — no executable material work currently exists
TERMINAL     — roadmap work is complete; no material successor exists
```
`INITIALIZING | IDLE | TERMINAL` require an empty computed frontier and `active_ep.state: NONE`. `ACTIVE` requires `SERIAL`. `PARALLEL` requires `OWNER_APPROVED_PARALLEL`, `active_ep.state: ROUTER`, an approved plan, and at least two computed frontier nodes.

## Core objects
- Overall Roadmap: authoritative objectives, phases, work packages, dependencies, definition maturity, status and execution eligibility.
- Executable frontier: work package(s) whose prerequisites are satisfied and current execution policy permits.
- EP: forward-looking executable work contract derived from a frontier node.
- CP: backward-looking checkpoint of what actually happened.
- ODR: durable Owner Decision Record for Owner-intent changes.
- Progress Basis: revisioned denominator/numerator basis for calculated progress.
- Issue Graph: GitHub relationship projection.
- Parallel Plan: Owner-approved router for a multi-node frontier, including lane EPs, isolation and integration semantics.

EP and CP are different objects and must never substitute for each other.

## Dynamic roadmap
Roadmap mutation has three classes:
```text
A. EXECUTION_DERIVED_STATUS
B. ENGINEERING_DISCOVERY_PROPOSAL
C. OWNER_INTENT_MUTATION
```
Agents may apply factual A updates, may propose B structural changes, and require explicit Owner authority through an ODR for C changes. Every material revision reconciles dependencies, stale EPs, issue projection, progress basis and frontier.

A revision is not reconciled merely because it names a new frontier or progress basis. `frontier_after` must equal the frontier computed from the resulting roadmap. If the progress denominator changes, the revision must create a new Progress Basis ID bound to the new roadmap revision.

## Serial execution
Default is `SERIAL`. In `relay_state: ACTIVE`, exactly one material executable frontier node and one active material EP exist. Read-only exploration may be broad. An agent does not start another material stream merely because it appears independent.

## Owner-approved parallel execution
Parallel material work requires explicit Owner approval of a named plan with an ASCII topology. `REPO_STATE.active_ep` becomes a router and must not contain a lane EP path. The plan must exactly cover the computed frontier and declares, for every lane:
- unique lane ID, WP, EP ID/path, branch and optional worktree;
- exclusive write domains and shared read domains;
- normal self-contained EP, acceptance and roadmap binding;
- the same prior checkpoint baton when a fork follows a checkpoint.

Any overlapping write domains require a specific Owner-approved shared-write exception naming the lane pair, overlap domain and reason. Otherwise overlap is invalid. The integration WP must depend on every lane WP and must remain non-executable until lane completion makes it the recomputed frontier. The integration EP is created only then (`WHEN_FRONTIER`). Ambiguous branch/worktree routing means no material execution.

## EP contract
Every EP contains: identity, roadmap_source, outcome, context_capsule, repository_discovery, inputs, benchmarks, scope.allowed, scope.prohibited, anti_drift, implementation_plan, quality, acceptance, validation, failure_and_stop_conditions, report_contract, checkpoint_contract and successor_relay.

`identity.previous_checkpoint` ties the EP to the durable baton that produced it. The first EP uses `NONE`. Every serial EP and every parallel lane EP must be executable without chat context. Every acceptance criterion maps to verification.

## Checkpoint successor contract
Every checkpoint declares `successor.mode`:
```text
SERIAL   — one frontier work package and one successor EP
PARALLEL — one approved parallel plan plus exact lane {WP, EP} receipts
NONE     — no material successor (idle/initializing/terminal custody)
```
Checkpoint mode, REPO_STATE lifecycle, current position/router and successor EP/lane checkpoint references must agree.

## Separate state planes
`REPO_STATE.yaml` carries four independent status planes:
```text
EXECUTION — what is happening and whether work can continue
QUALITY   — maintainability/design/UX findings
EVIDENCE  — what was actually run/proven/not run
STOP      — true hard-stop condition only
```
Do not use one overloaded `BLOCKED` state. `NOT_RUN` is evidence truth and is not a hard stop by itself. A hard stop must name an allowed category, reason and durable basis, and must set execution `can_continue: false`. Read `operating-model/state-planes.md`.

Validation truth is `PASS | FAIL | NOT_RUN | NA`; test obligation is `MUST_PASS | SHOULD_RUN | INFORMATIONAL`.

Hard stops are reserved for true inability to proceed safely: `OWNER_DECISION_REQUIRED`, `ESSENTIAL_INPUT_MISSING`, `AUTHORITY_VIOLATION`, `PROTECTED_INVARIANT_FAILURE`, `WRITE_COLLISION`, `SUPERSEDED_EP`, `ROADMAP_CONFLICT`, `REPOSITORY_STATE_CONFLICT`, `UNSAFE_ENGINEERING_RESULT`.

## Progress
Calculated only:
```text
Acceptance Criteria → EP → Work Package → Phase → Objective → Overall Roadmap
```
Approved scope changes create a new Progress Basis; completed work is not rewritten to make percentages look stable.

## Phase transitions
Fresh Q1-Q5 are mandatory when the frontier enters a new phase and must derive from the incoming work contract:
```text
Q1 Production path
Q2 Incoming engineering problem
Q3 Boundaries and invariants
Q4 Verification
Q5 First safe implementation slice
```
Each question declares a fixed focus and one or more durable anchors from the incoming EP (phase/work-package IDs, AC IDs, TEST IDs, INPUT IDs or STEP IDs). Historical-domain reuse, unknown anchors, or a `to_phase` that differs from the incoming EP is invalid.

## Relay durability
Assume conversation termination cannot be predicted. Before material changes, durable roadmap/REPO_STATE/EP-or-plan/scope/inputs/acceptance must exist. At custody transfer: checkpoint → roadmap/progress/issues reconciliation → frontier recomputation → successor serial EP or approved parallel plan → successor validation → cold-start PASS → REPO_STATE transfer. Code completion alone is not relay completion.

For a continuing serial relay, `REPO_STATE.last_checkpoint`, that checkpoint's `SERIAL` successor, `REPO_STATE.current_position/active_ep`, and the active EP's `identity.previous_checkpoint` form one consistent baton link. For a parallel fork, the checkpoint's `PARALLEL` successor, active plan lane receipts and every lane EP `previous_checkpoint` must agree. For a terminal/idle relay, the final checkpoint uses `successor.mode: NONE`.

## Safe bootstrap and migration
Bootstrap must not invent executable work. Use a reviewed `BOOTSTRAP_MANIFEST.yaml`; `bootstrap_relay.py` is dry-run by default and `--apply` refuses to overwrite an existing relay. It creates `relay_state: INITIALIZING`, an empty executable frontier and no EP.

V2 migration is evidence-first:
```text
inventory_v2_relay.py
→ prepare_v2_migration.py
→ human/agent reconciliation of Owner intent + roadmap + unresolved work
→ explicit V2.5 Progress Basis
→ first DETAILED frontier
→ first genuine V2.5 EP
→ conformance + cold-start PASS
```
A V2 endpoint is never automatically promoted to a V2.5 EP and narrative progress is never copied as calculated progress.

## Human handover
Always show relay lifecycle, overall roadmap %, current phase %, current serial EP or parallel lane list, plain-language execution/quality/evidence/stop status, exact next actions, integration/next roadmap node, phase-transition YES/NO, new Q1-Q5 when required, successor readiness, and `conversation context required: NO`. Initializing/idle/terminal handovers explicitly say there is no active material EP.

## Validation and lifecycle entrypoints
```bash
python skills/engineering-pr-delivery-v2.5/scripts/validate_relay_conformance.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/cold_start_check.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/stress_test_relay.py <repo-root> [<repo-root> ...]
python skills/engineering-pr-delivery-v2.5/scripts/bootstrap_relay.py <manifest> <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/inventory_v2_relay.py <repo-root>
python skills/engineering-pr-delivery-v2.5/scripts/prepare_v2_migration.py <inventory>
```
