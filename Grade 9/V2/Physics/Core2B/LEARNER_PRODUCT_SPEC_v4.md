# Physics Core2B v4 — Generative Transfer Coach

## Learner-product purpose

Core2B is a **self-guided generative-dominant transfer product**.

> Can the learner recognize, select and transfer the capability when the surface, target, representation or structure changes?

The learner meets the problem before being told the model.

Core2B is not an open-ended rewrite of every Core2A worked example.

## Required adaptation input

Exactly one basis is required.

### KNOWLEDGE_PERCENT

`student_knowledge_pct` must be 0..100.

### OWNER_OVERRIDE

If knowledge percentage is unknown, owner input may waive it with:

- `owner_ref`;
- `reason`;
- `support_band`.

Allowed bands:

`FOUNDATION_HIGH_SUPPORT | GUIDED | STANDARD | CHALLENGE_MINIMAL`

There is no silent default.

The override does not waive exact Core2A pool custody, Core1B learner-evidence requirements, or source immutability.

See `../Blueprint/policy/core2ab-knowledge-routing.v1.json`.

## Attempt-first invariant

All support bands remain attempt-first.

Knowledge/support level may change:

- which eligible legal item appears first;
- structural-distance progression;
- hint visibility;
- reveal timing;
- repair density.

It may not change the legal pool.

## Do not mirror Core2A one-for-one

Core2A teaches representative legal problem families.

Core2B should use the legal pool to test transfer across changed demands.

Where the pool permits, prefer items different from the worked Core2A exemplar so the learner must recognize structure rather than replay a memorized solution.

A direct/near-transfer item may still be used as a baseline, but the sequence should then move across one or more independent demand dimensions.

## Transfer dimensions

Vary dimensions deliberately rather than treating difficulty as a scalar ladder:

- structural distance;
- direction/sign reversal;
- reversed target;
- representation change;
- model discrimination;
- constraint inversion;
- multi-step bridge;
- synthesis;
- competitive mixing.

`T0...T8` may remain descriptive/order vocabulary only.

## Conditional task grammar

Do not force every Core2B interaction into the same long form.

### Recognition / discrimination micro-task

```text
UNFAMILIAR PROMPT
→ FIRST CHOICE / REASON
→ LOCAL CHECK
→ WHY THIS MODEL / WHY NOT THE OTHER
```

### Representation transfer task

```text
QUESTION
→ REPRESENTATION ATTEMPT
→ CHECK REPRESENTATION
→ SOLVE OR EXPLAIN
```

### Substantive transfer problem

```text
UNFAMILIAR QUESTION
→ FIRST MOVE ATTEMPT
→ SOLUTION ATTEMPT
→ H1 NOTICE
→ H2 REPRESENT
→ H3 START
→ TRY AGAIN
→ FULL CHECK
→ WHAT STAYED THE SAME?
→ WHAT CHANGED?
→ REPAIR ROUTE
```

### Mixed retrieval

```text
UNLABELED MIXED ITEM
→ ATTEMPT
→ COMPACT CHECK
→ IDENTIFY THE HIDDEN FAMILY / INVARIANT
```

`H1 NOTICE → H2 REPRESENT → H3 START` is the standard rescue ladder for substantive tasks when progressive help is needed. It is not mandatory for every micro-task.

## Band behavior

### FOUNDATION_HIGH_SUPPORT

Near transfer first; recognition/representation prompts readily available; H1/H2/H3 available for substantive tasks; full solution after attempt; targeted repair on failure.

### GUIDED

Near -> structural progression; optional progressive rescue; explicit invariant/variation check after substantive tasks.

### STANDARD

Structural variation earlier; hints hidden by default; compact post-attempt solution and transfer analysis.

### CHALLENGE_MINIMAL

Highest evidence-eligible structural demand; hints on demand; mixed retrieval and model discrimination when legal.

## Self-guided resolution

Every open-ended challenge has a local resolution on the same page or immediately following.

For substantive transfer problems, the resolution should normally contain:

1. recognition — what hidden structure is present?
2. representation — how should it be shown?
3. model selection — why this model and not a competitor?
4. full working;
5. physical/limiting/dimensional check where relevant;
6. what stayed invariant;
7. what changed;
8. smallest repair pointer.

Micro-tasks may use a shorter resolution if the learner is not stranded.

## Repair behavior

A wrong answer is an **error hypothesis**, not a diagnosis.

Repair must target the smallest explanatory prerequisite in Core1B. After repair, verify with a different legal item when possible rather than replaying only the identical worked solution.

## Runtime authority remains unchanged

- exact Core2A legal-pool ref + digest and exact item ID remain mandatory;
- Core2B may not create or legalize transfer items;
- owner override cannot expand legality;
- incorrect/full-solution exposure cannot count as representation mastery;
- only successful sufficiently low-hint observed transfer may advance robustness.
