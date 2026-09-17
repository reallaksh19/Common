# Physics Core2B v3 — Generative Transfer Coach

## Learner-product purpose

Core2B is a **self-guided generative transfer product**.

> Can the learner recognize, select and transfer the capability when the surface changes?

The learner meets the problem before being told the model.

## Required adaptation input

Exactly one basis is required:

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
- whether H1/H2/H3 are visible or hidden by default;
- reveal timing;
- repair density.

It may not change the legal pool.

## Canonical transfer episode

```text
UNFAMILIAR QUESTION
-> FIRST MOVE ATTEMPT
-> SOLUTION ATTEMPT
-> H1 NOTICE
-> H2 REPRESENT
-> H3 START
-> TRY AGAIN
-> CHECK AFTER ATTEMPT
-> WHAT STAYED THE SAME?
-> WHAT CHANGED?
-> repair route
```

## Band behavior

### FOUNDATION_HIGH_SUPPORT

Near transfer first; H1/H2 readily available; H3 available; full solution after attempt; repair on failure.

### GUIDED

Near -> structural progression; H1/H2/H3 optional.

### STANDARD

Structural variation; hints hidden by default; full solution after attempt.

### CHALLENGE_MINIMAL

Highest evidence-eligible structural demand; hints on demand; mixed retrieval when legal.

## Self-guided solution block

Every challenge needs:

1. recognition;
2. representation;
3. model selection;
4. full working;
5. physical/limiting/dimensional check where relevant;
6. what stayed invariant;
7. what changed;
8. repair pointer.

## Runtime authority remains unchanged

- exact Core2A legal-pool ref + digest and exact item ID remain mandatory;
- Core2B may not create or legalize transfer items;
- owner override cannot expand legality;
- incorrect/full-solution exposure cannot count as representation mastery;
- only successful sufficiently low-hint observed transfer may advance robustness.
