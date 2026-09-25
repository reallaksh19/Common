# Two-Pass Prompt Generator Schema

CANONICAL LAUNCHER:
`skills/two-pass-prompt-generator/SKILL.md`

CANONICAL SCHEMA:
`skills/two-pass-prompt-generator/schema.md`

# SCHEMA EXECUTION HANDSHAKE

A generated artifact must begin with:

```text
# SCHEMA EXECUTION HANDSHAKE

PROTOCOL REVISION:
TPG-2P-2026-09-25-R1

GENERATOR MODE:
TWO_PASS_ONLY

SCHEMA FETCH STATUS:
LIVE_THIS_RUN

SCHEMA CONTENT SHA:
<actual current blob/content SHA>

HANDSHAKE STATUS:
PASS
```

If the live schema cannot be fetched or its SHA cannot be established, emit only:

```text
# SCHEMA EXECUTION HANDSHAKE
HANDSHAKE STATUS:
FAIL
```

and stop.

## Purpose

Generate exactly two prompts.

### PASS 1 — INDEPENDENT SYSTEM BASELINE

The future agent is told the repository/application/system and broad human outcome, but **not** the actual issue/task, current PR, requested fix, Improvement Proposal, desired implementation, or next action.

Pass 1 must sound like one experienced human asking another to understand the system. It must tell the agent to inspect live repository/application reality and independently establish:

- what the user experiences today;
- where authoritative truth/state comes from;
- how the important path flows from input/evidence to result/consumer;
- one representative real witness worked end-to-end;
- one load-bearing variation and the invariant/falsifier it exposes;
- one genuinely independent verification route;
- known facts versus uncertainty/contradiction;
- the exact live material/runtime basis inspected.

Pass 1 must end at understanding. It must not recommend an improvement, select a next task, draft an implementation plan, or infer the hidden issue.

Required Pass-1 output concept:

```text
INDEPENDENT_SYSTEM_BASELINE

SYSTEM / USER OUTCOME
CURRENT BEHAVIOUR
REAL PATH / AUTHORITY FLOW
CONCRETE WITNESS
INVARIANTS / FAILURE BEHAVIOUR
INDEPENDENT VERIFICATION
CURRENT MATERIAL BASIS
KNOWN
UNCERTAIN
```

No "what we should do next" section.

### PASS 2 — IMPROVE, RECONCILE, PLAN

Pass 2 receives:

- the actual Pass-1 baseline;
- the actual next issue/task;
- current repository/application/provider evidence;
- programme/Owner constraints and approved authority.

The future agent must first refresh live reality, then step back far enough to challenge the task's assumptions without expanding ownership.

#### A. High-ROI improvement scan

Find **zero or more** legitimate improvements. Prefer no proposal to a speculative proposal.

Reject:

- rewrites merely because a cleaner architecture is imaginable;
- cosmetic cleanup presented as strategic improvement;
- scope expansion;
- novelty quotas;
- telemetry such as PR/file/commit counts used as capability evidence.

Every proposal must use:

```text
IMPROVEMENT PROPOSAL — IP-XX

OBSERVED GAP
LIVE EVIDENCE
WHY IT MATTERS
CURRENT → PROPOSED

QUANTITATIVE EFFECT
Use actual before/after measures where available.
If a quantity cannot be established, write UNKNOWN.
Never invent precision.

ESTIMATED CHANGE SIZE
files / approximate LOC / test surfaces / interfaces, where evidence permits.

IMPACT
1–5

EVIDENCE STRENGTH
1–5

REUSE / CROSS-TASK VALUE
1–5

EFFORT
1–5, where 1 is very small

CHANGE RISK
1–5

CONFIDENCE
0–100%

RELATIVE ROI
(impact × evidence_strength × reuse × confidence_fraction)
/
(effort × change_risk)

FALSIFIER
What would show the proposal is unnecessary or wrong.

SCOPE RELATION
IN_SCOPE | ADJACENT | UNRELATED | FALSIFIED
```

The score is a relative heuristic; concrete before/after quantities are more important.

#### B. Reconcile the actual task

Determine from live evidence:

- what the issue actually owns;
- whether its assumptions are still true;
- whether its responsibility should be PRESERVE, AMEND, SPLIT, SUPERSEDE, or is already SATISFIED;
- which proposals are actually in scope;
- which approved adjacent proposals require a separate child responsibility/EP rather than contaminating the issue.

#### C. Draft plan in chat

Before any durable issue mutation, EP creation/binding, branch/PR creation, or material implementation, show:

```text
DRAFT IMPLEMENTATION_PLAN — NOT YET PUBLISHED

BASIS
MY UNDERSTANDING
ISSUE DISPOSITION
IMPROVEMENT PROPOSALS
OWNED OUTCOME
APPROACH
PLAN SLICES (stable STEP-* IDs)
EXPECTED CHANGED SURFACES
DEPENDENCIES
INDEPENDENT WORK
FALSIFIER
VALIDATION
PRESERVE
UNCERTAINTIES
EXPECTED NEXT OBSERVABLE
CONSUMER / HANDOFF
```

Then finish the first Pass-2 response with:

```text
APPROVAL REQUIRED

No durable plan publication, EP creation/binding, or material implementation has been performed from this proposal response.
```

#### D. After explicit Owner approval — same Pass 2

This is a continuation of Pass 2, not a third pass.

1. Refresh live issue/repository/PR/runtime state.
2. If a material change invalidates the approved plan, show the approval delta and stop for renewed approval.
3. Otherwise publish `IMPLEMENTATION_PLAN — rev 1` (or the appropriate revision) on the **original owned issue**.
4. Include only approved Improvement Proposal(s) in the plan, with their quantitative basis, scope relation, falsifier, and expected benefit.
5. Reuse the existing EP for the same bounded responsibility; create a new EP only for a genuinely new responsibility.
6. If an approved proposal is ADJACENT, create/use a separate child responsibility and EP rather than silently widening the original issue.
7. Refresh the issue-local Task Snapshot and programme Handover index so the coordinator can consume:
   issue → plan → expected observable → PR/head/result → consumer consequence.
8. Execute only if the Owner's approval/authorized actions include execution. V3.1/Relay metadata is never production permission.
9. During execution keep the four durable publication types: `IMPLEMENTATION_PLAN`, `PLAN_UPDATE`, `TASK_EVIDENCE`, `TASK_RESULT`.

## Required generated artifact shape

After the handshake and a short schema basis, emit only:

```text
## PASS 1 — INDEPENDENT SYSTEM BASELINE

<one complete copy-pasteable prompt>

## PASS 2 — IMPROVE, RECONCILE, PLAN

<one complete copy-pasteable prompt>
```

Do not emit a third prompt, Prompt 0.5/1/2/2.5/3, a qualification questionnaire, or extra admission/certification stage.

## Pass-1 visibility rule

Pass 1 may include the repository/application/system identity and broad human outcome.

Pass 1 must not contain:

- issue or pull-request URLs/numbers;
- current branch/PR status;
- issue acceptance criteria;
- the hidden task title;
- "Improvement Proposal";
- implementation-plan instructions;
- proposed next action;
- requested change.

The generator may know these internally; it must quarantine them until Pass 2.

## Pass-2 evidence rule

Pass 2 must tell the future agent to distrust stale prose when live provider/material evidence is available. Historical handoff explains what to inspect next; live reality determines what is true now.

## Approval rule

Human approval governs the transition from proposal to durable engineering intent.

Relay/coordinator approval is not required after Owner approval. After the plan is durably published and bound to the responsibility, execution may continue within actual production authority and the approved action boundary.
