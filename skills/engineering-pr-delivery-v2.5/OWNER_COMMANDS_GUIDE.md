# Owner Command Guide — Engineering Relay V2.5

A practical cheat sheet for steering agents in complex coding, engineering, and schema/blueprint projects.

These commands are intended to be typed directly by the Owner. Most are **reasoning controls**. Four additional control phrases express bounded execution/defer/record intent; they require validated durable V2.5 state and are never authority merely because the words were typed.

## Quick reference

| If the agent is... | Type this |
| --- | --- |
| doing the obvious next step | `Proceed next` |
| interrupting with Q1–Q5 you do not want | `Proceed next, No Qs` |
| playing with tiny subtasks | `Proceed next complex task` |
| too focused on the current file/bug | `Step back` |
| defending a questionable plan | `Critique` |
| jumping to a patch before understanding the path | `Trace` |
| claiming something is fixed/ready/correct too easily | `Prove it` |
| building too much machinery | `Simplify` |
| debugging a huge confusing failure | `Reduce` |
| schema/docs/validator/runtime disagree | `Reconcile all surfaces` |
| architecture sounds good but may fail in real use | `Run scenario` |
| edge cases / stale state / optional fields are risky | `Boundary check` |
| a blueprint/spec has vague "should/may/must" language | `Normalize the contract` |
| a deferrable validation/custody gate is blocking bounded coding you explicitly want to start | `Owner override, start` |
| the same unresolved validation/evidence item must survive handover without stopping every fresh agent | `Record pending` |
| a known non-blocking defect/risk should survive handover without becoming today's blocker | `Record known issue` |
| an inherited pending gate has reached its resolution boundary | `Resolve pending <PEND-id>` |

## My recommended power commands

### Agent is becoming too local

```text
Step back. Critique. Proceed next complex task, No Qs.
```

### Architecture/schema is growing without clarity

```text
Step back. Reconcile all surfaces. Normalize the contract.
Critique the architecture. Simplify.
Run one real scenario. Boundary check it.
Prove the resulting smaller architecture.
Proceed next complex task, No Qs.
```

### Bug/failure is large and confusing

```text
Trace the failure end to end. Reduce it to the smallest reproducer.
Critique the current explanation. Prove the cause before patching.
Proceed next complex task, No Qs.
```

### Agent says "ready", "fixed", "mergeable", "qualified"

```text
Critique. Prove it.
```

## Owner control phrases for blocker loops

### Continue bounded coding without falsifying a gate

Use:

```text
Owner override, start.
Record this validation/custody blocker as pending until PR-ready.
```

Common variants:

```text
Owner override: proceed
Owner override continue
Start under Owner override
Proceed under the Owner override
Owner-authorized start
Start with Owner override
```

This does not mean "ignore validation". The agent must create/validate an APPLIED bounded execution override plus an OPEN `PEND-*` record. The result remains visibly pending and the recorded readiness/merge/checkpoint/release boundary stays blocked.

### Carry a validation obligation forward

Use any of:

```text
Record as pending
Record this as pending
Record pending
Record pending item
Add this to pending items
Carry it as pending
Defer this validation and record pending
```

A fresh agent must consume the existing PEND record instead of creating another candidate/certification/delegation loop.

### Carry a non-blocking known issue

Use any of:

```text
Record as a known issue
Record this in known issues
Add it to the known issues
Carry this as known issue
Log this as a known issue
```

Known issues require a revisit condition. They are not a place to hide validation that must resolve before a named boundary.

### Resolve inherited pending work

Use:

```text
Resolve pending PEND-...
Resolve the pending item
Clear pending PEND-...
Close pending PEND-...
```

The agent must re-run/reconcile the actual obligation. `SATISFIED` requires current evidence.

### What the agent should reconstruct on a cold start

```text
current roadmap / route
+ active execution custody
+ APPLIED Owner execution overrides
+ OPEN PEND-* deferred validations
+ OPEN KI-* known issues
+ OPEN DLG-* delegated checks
+ each item's allowed work and resolution boundary
```

A fresh status/timer/observer agent stays read-only. It does not become a new execution candidate just because it is a new process.

### Grade9V3 corrective-branch example

For the #162 pointer-click-dedupe case, a suitable Owner command is:

```text
Owner override, start.
Record V2.5 route/custody reconciliation as pending until PR-ready.
Continue the bounded #162 pointer-dedupe implementation on draft PR #180.
Do not replace the #169 serial route, mark the PR ready, or merge until the pending item is resolved.
```

The durable truth should remain:

```text
IMPLEMENTATION              ALLOWED within recorded branch/path scope
PRODUCT TESTING             ALLOWED
DRAFT PR UPDATES            ALLOWED
V2.5 ROUTE RECONCILIATION   OPEN / NOT PASS
PR_READY                    BLOCKED by PEND
MERGE                       BLOCKED by PEND
ACTIVE #169 SERIAL ROUTE    UNCHANGED
```

For the #173 fresh-agent loop, the important rule is different: a heartbeat/delegation timer is a **read-only monitor**. If the delegated condition is already satisfied/superseded, it terminates. It does not invent another candidate identity or restart DISC/QUAL/TC.

---

---

# Practical example 1 — Advanced_Analysis

Repository:

https://github.com/reallaksh19/Advanced_Analysis

The repository already contains good evidence that these commands fit the real work:

- LAFEA UX programme: issue #1820.
- LAFEA model-input waterfall: #1839.
- misleading/undiscoverable blocked-state flow: #1840 and #1841.
- LAFEA.4 formulation qualification: #1763.
- LAFEA.4 solver scalability/equivalence: #1764.
- LAFEA recovery sequencing: #1846.
- Load Calc zero-blocker architecture: #1321.
- Load Calc phased architecture fix: #1844.

## A. LAFEA.3 UI is bad and the agent keeps fixing isolated controls

Use:

```text
Step back.

Run scenario: take a practising engineer from opening LAFEA.3 with no prepared file
through model → mesh → solve → results.

Trace the user-visible state and authority end to end.
Reconcile every place that renders status, blocked state, next action, and results.
Critique the current navigation / disclosure / status architecture.
Simplify it without moving solver or qualification authority.

Proceed next complex task, No Qs.
```

Why this is stronger than "fix the UI":

```text
Step back
→ reconnect UI work to "engineer reaches a trustworthy result"

Scenario
→ prevents local CSS/button fixes from masquerading as workflow repair

Trace
→ finds where actual state comes from

Reconcile
→ catches duplicated/inconsistent status vocabulary

Critique
→ tests whether the current interaction architecture deserves to survive

Simplify
→ removes waterfall/disclosure/status duplication

Complex next
→ agent owns a coherent user-outcome slice, not one button
```

A shorter version:

```text
Step back. Scenario the LAFEA.3 zero-to-first-result journey.
Reconcile all UI/status surfaces. Critique. Simplify.
Proceed next complex task, No Qs.
```

## B. LAFEA.4 code feels patchy / difficult to trust

Issues #1763 and #1764 show that the real boundary is larger than one element function:
formulation, geometry, loads, assembly, backend selection, reactions, recovery, evidence and applicability all interact.

Use:

```text
Trace the current LAFEA.4 production route end to end:
model/geometry → mesh → load/BC transfer → element formulation →
global assembly → solver backend → recovery → result publication/evidence.

Critique the current implementation boundaries.
Boundary check every fallback, unsupported family, stale parent, solver failure,
frame transformation and result-authority transition.

If a benchmark fails, Reduce it before patching.
Prove the selected root cause independently.

Simplify only after the correct ownership boundary is clear.
Proceed next complex task, No Qs.
```

This prevents the common pattern:

```text
benchmark fails
→ patch assertion / adapter / special case
→ one test turns green
→ deeper production-route inconsistency remains
```

The intended pattern becomes:

```text
trace
→ isolate boundary
→ reduce failure
→ critique explanation
→ prove cause
→ fix at owning layer
→ prove route
```

## C. Load Calc has endless blockers

For issues such as #1321 and #1844, use:

```text
Step back.

Trace one real Load Calc job from imported/source data through master enrichment,
effective-value/default resolution, route/chainage, preflight, calculation and result.

Reconcile every blocker source and every place that can independently decide
"missing", "invalid", "not ready", or "cannot run".

Critique the blocker model:
which blockers represent genuine engineering absence,
and which are architecture/state-resolution defects?

Simplify toward one authoritative effective-value / readiness path.

Run the real scenario again.
Prove that the case reaches calculation with no false blocker and that a genuinely
missing engineering input still fails closed.

Proceed next complex task, No Qs.
```

Useful when the agent starts treating individual blocker messages as separate bugs:

```text
Do not fix the next blocker yet.
Trace. Reconcile all blocker authority. Critique. Simplify.
Then Prove one zero-false-blocker real case.
```

---

# Practical example 2 — Grade9V3

Repository:

https://github.com/reallaksh19/Grade9V3

If you are unsure whether to call the growing thing a "schema", "blueprint", "architecture", or "framework", do **not** force the name first.

Call it provisionally:

```text
the current architecture/schema system
```

and use the commands to discover what the real boundaries should be.

Useful live anchors include:

- #118 — cross-subject Topic Atlas / diagnostics / gap intake / Core request architecture.
- #159 — subtopic-session router, explicitly warning against a second curriculum/mastery model.
- #162 — Semantic Transformation Workbench, whose revalidation already narrowed several over-broad architecture ideas.

## A. The schema/blueprint keeps growing and nobody knows what is canonical

Use:

```text
Step back.

Reconstruct the actual product aim before touching the architecture/schema system.

Reconcile all surfaces:
role specs, package schema, subject adapters, canonical library records,
matrix/rungs, learner evidence, routing/session state, publication/runtime projections,
validators, generated web data, architecture manifest, docs and tests.

Normalize the contract:
for every rule, identify what is authoritative, derived, optional, required,
runtime-only, content truth, or UI projection.

Trace one learner need end to end from source/spec
→ canonical content/library
→ capability/rung
→ evidence
→ router
→ support/hint
→ representation/workbench
→ published learner artifact.

Run that scenario with one real NLM case.

Critique the architecture:
construct the strongest case that the current design contains duplicate models,
unnecessary schemas, or abstractions created before a real falsifier required them.

Reduce the architecture to the smallest canonical set that can carry the scenario.
Simplify duplicated state and speculative extension points.
Boundary check subject-neutral vs subject-specific ownership and canonical vs runtime state.

Prove the smaller architecture against the real scenario and existing required contracts.

Proceed next complex task, No Qs.
```

## B. When an agent proposes another field/schema because one case needs it

Use:

```text
Critique.

Before adding the field:
Trace the requirement to its original spec/Owner need.
Reconcile existing homes for that truth.
Run scenario using the concrete learner case that allegedly needs it.
Boundary check whether the field is canonical content, subject-adapter truth,
runtime/session state, evidence, or merely presentation.

If an existing authority can express it, do not add a parallel field.
If not, Reduce the missing contract to the smallest requirement.
Normalize the new requirement and Prove it with at least one real case and one negative.

Simplify.
```

## C. When the architecture sounds impressive but you cannot tell whether it helps a learner

Use:

```text
Step back. Run scenario.

Pick one actual Grade 9 learner problem and walk:
source truth → teaching intent → canonical record → learner evidence →
next action → help/hint → representation → question → learner-facing publication.

At every transition ask:
who owns this truth?
what is derived?
what can go stale?
what would falsify this design?

Critique.
Reconcile all surfaces.
Simplify.
Prove the learner-visible outcome.
```

## D. Strong reset command for Grade9V3

When the whole design feels like it is growing faster than understanding:

```text
Step back. Critique.

Reconcile all architecture/schema/spec/runtime surfaces.
Normalize the contract.
Trace one real learner journey end to end.
Reduce to the minimum canonical model that can support it.
Simplify.
Boundary check it.
Prove it.

Then update the roadmap from what survived and
Proceed next complex task, No Qs.
```

---

# Choosing the right command

A useful mental model:

```text
Step back
    changes the FRAME

Critique
    challenges the REASONING

Trace
    follows the PATH

Reconcile
    finds DRIFT

Scenario
    tests the WHOLE DESIGN

Boundary check
    attacks EDGES

Reduce
    isolates the CAUSE

Simplify
    removes MACHINERY

Normalize
    clarifies the CONTRACT

Prove
    demands EVIDENCE

Proceed next complex task
    changes the selected WORK GRANULARITY

No Qs
    changes the INTERACTION MODE

Owner override, start
    changes the BOUNDED EXECUTION CONTROL STATE after durable recording

Record pending
    carries an UNRESOLVED CONTROL OBLIGATION forward

Record known issue
    carries a NON-BLOCKING KNOWN RISK forward

Resolve pending
    changes the CURRENT RECONCILIATION TARGET
```

## One caution

Do not stack every keyword automatically.

Use the smallest combination that attacks the actual failure mode.

Examples:

```text
UI workflow fragmented
→ Step back + Scenario + Reconcile + Simplify

mysterious coding failure
→ Trace + Reduce + Prove

architecture/schema sprawl
→ Step back + Reconcile + Normalize + Critique + Simplify + Scenario

agent doing tiny leaf tasks
→ Step back + Proceed next complex task

plausible but unproven claim
→ Critique + Prove it
```

The goal is not to make the agent perform more ceremony. The goal is to force a **different cognitive move** exactly when normal local optimisation is failing.
