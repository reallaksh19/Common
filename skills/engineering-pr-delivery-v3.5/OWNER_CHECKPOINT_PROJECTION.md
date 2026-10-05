# Engineering Relay V3.5 — Owner checkpoint projection contract

## Status

`engineering-pr-delivery-v3.5` is not yet a complete invocable protocol in `Common`.

This file is a **candidate future contract** for the V3.5 line. It MUST NOT be treated as an active selector or complete protocol by itself.

When V3.5 is implemented, this contract is intended to become normative alongside the checkpoint/liveness mechanics. Where the current V3.5 checkpoint seed's Owner-facing example is more verbose than this contract, this file defines the intended compact Owner projection.

## Three-view architecture

V3.5 MUST keep these distinct:

```text
1. GITHUB TITLE
   glanceable operational projection

2. OWNER CHAT CHECKPOINT
   compact delta / blocker / Owner-action / next-work projection

3. DURABLE TASK_EVIDENCE
   comprehensive successor/recovery evidence
```

Do not make one message serve all three audiences.

## GitHub title

Recommended:

```text
🟢 {P42% · E36% · A07 · U03 · ACTIVE} <issue title>
```

The title exposes liveness/motion, semantic/evidence progress, activity epoch, current unit where useful and compact work state. It is disposable projection only.

## Owner chat checkpoint

The checkpoint answers only:

> What changed since the previous checkpoint? What blocks now? Does the Owner need to act? What bounded work happens next?

Recommended shape:

```text
TASK_EVIDENCE — CHECKPOINT

🟢/🟡/🔵/🔴 {P__% · E__% · A__ · <STATE>}

UNIT
<one concise line>

DELTA
✓ <new meaningful result>
✓ <new meaningful result>
△ <new unresolved finding, only if decision-relevant>

BLOCKER
<NONE | one concise blocker>

OWNER_ACTION
<NONE | REQUIRED — one explicit decision/action>

NEXT
<one bounded next substantial work unit>

EVIDENCE
<1–3 durable refs>
```

### Information budget

Unless the Owner explicitly asks for detail:

```text
<= 12 non-blank content lines
<= 3 DELTA items
<= 1 BLOCKER
<= 1 OWNER_ACTION
<= 1 NEXT
<= 3 EVIDENCE refs
```

This is an operational dashboard, not a recovery dump.

### Delta-only projection

Do not repeatedly print unchanged:

```text
base/main SHA
branch name
PR state
provider blob digest
changed-file inventory/count
full dependency closure
full remaining denominator
historical evidence already referenced
all pending test names
command transcript
```

Include such a fact only if it changed or is needed to understand the current delta/blocker/Owner action.

### Prefer references over re-explanation

When a detailed durable record exists, say:

```text
✓ Lower-bound oracle contract PASS — evidence: <ref>
```

rather than reproducing the full method, hash closure and interpretation in chat.

## Durable TASK_EVIDENCE

Durable evidence remains comprehensive and successor-safe. It may contain all detail omitted from chat:

- exact protocol and source refs;
- candidate/base/material identities;
- blobs/trees/digests;
- changed files;
- exact tests/commands/results;
- dependency closure;
- negative knowledge;
- detailed findings/repair rationale;
- complete remaining denominator;
- recovery/provider state;
- invalidation/replay facts.

Owner brevity must never reduce durable evidence quality.

## Checkpoint versus TASK_RESULT

A waiting or blocked operational checkpoint is not automatically a final task result.

Use checkpoint states:

```text
ACTIVE
QUIET
WAITING_CI
WAITING_TOOL
WAITING_EXTERNAL
WAITING_PROVIDER_VISIBILITY
RECOVERING
```

Reserve `TASK_RESULT` for a true scoped result boundary that declares:

```text
RESULT_SCOPE: STEP | PRODUCT | RESPONSIBILITY
RESPONSIBILITY_COMPLETE: YES | NO | UNKNOWN
```

Do not emit `TASK_RESULT = BLOCKED` merely to communicate that an in-progress responsibility currently cannot execute its next unit.

## OWNER_ACTION is mandatory

Every Owner checkpoint explicitly states:

```text
OWNER_ACTION
NONE
```

or:

```text
OWNER_ACTION
REQUIRED — <specific reserved decision/action>
```

This prevents ordinary WAITING/CI/tool/provider states from being mistaken for an Owner escalation.

## Owner-required checkpoint barrier

When `CHECKPOINT_VISIBILITY_MODE=OWNER_REQUIRED`:

```text
1. observe live frontier
2. reconcile current unit and P/E/A
3. write detailed durable TASK_EVIDENCE when semantic/evidence truth advanced
4. update GitHub current-state/title projection
5. read back provider state
6. surface only the compact Owner checkpoint defined here
7. begin next substantial work unit
```

The compact chat message references detailed evidence; it does not mirror it.

## Example

```text
TASK_EVIDENCE — CHECKPOINT

🟡 {P42% · E36% · A07 · WAITING_EXTERNAL}

UNIT
Full-stack qualification of #1239 cumulative candidate.

DELTA
✓ Found #1252 import defect; isolated +1/-1 repair in draft #1253 (`ea2556d`).
✓ Persistence contract PASS.
✓ TEXPECTED lower-bound contract PASS.
△ Independent-seed authored test remains NOT_RUN; honest dependency closure is too broad for stubbing.

BLOCKER
Executable authenticated checkout / Node `@playwright/test` surface unavailable for browser + full-regression qualification.

OWNER_ACTION
NONE

NEXT
Restore executable checkout/test surface, then resume retained browser/full qualification.

EVIDENCE
#1239/5992101466 · #1239/5990185563 · PR #1253
```

## Required implementation tests for future V3.5

Future V3.5 mechanical implementation SHOULD include renderer/replay tests that reject or flag checkpoints which:

- omit known P/E/A;
- omit the current unit;
- omit `OWNER_ACTION`;
- duplicate unchanged provider/base/PR facts;
- dump the entire remaining denominator instead of one NEXT action;
- paste durable evidence prose into the Owner projection;
- label an in-progress WAITING state as final `TASK_RESULT`;
- bury the blocker below background prose;
- exceed the normal information budget without an explicit Owner request.

## Governing invariant

> **Durable evidence is comprehensive; Owner checkpoint projection is selective. Owner observability is measured by how quickly the Owner can see progress, delta, blocker, required action and next work — not by how much durable engineering detail is repeated into chat.**
