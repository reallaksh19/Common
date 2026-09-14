# Physics Core2A v2 — Declarative Worked Transfer Atlas

## Learner-product purpose

Core2A is a **self-guided declarative problem-learning product**.

> Show me how an expert recognizes, represents and solves this problem family.

## Required adaptation input

Core2A requires exactly one adaptation basis.

### 1. KNOWLEDGE_PERCENT

Provide `student_knowledge_pct` from 0 to 100.

### 2. OWNER_OVERRIDE

When knowledge percentage is unknown, the owner may waive it by supplying:

- `owner_ref`;
- `reason`;
- `support_band`.

Allowed support bands:

- FOUNDATION_HIGH_SUPPORT
- GUIDED
- STANDARD
- CHALLENGE_MINIMAL

There is no silent default.

The owner override waives only missing knowledge data. It does not expand transfer legality or alter frozen source questions.

See `../Blueprint/policy/core2ab-knowledge-routing.v1.json`.

## Default operational routing

These bands are product heuristics, not psychometric claims:

- 0–25 -> FOUNDATION_HIGH_SUPPORT
- 26–50 -> GUIDED
- 51–75 -> STANDARD
- 76–100 -> CHALLENGE_MINIMAL

## Frozen-source rule

Core2 source items remain frozen authority.

Core2A must not rewrite a frozen Core2 question to make it easier.

Adaptation changes only:

- support density;
- ordering;
- prerequisite bridge;
- completion level;
- visual support;
- clearly labelled GENERATED_ORIGINAL variants already legal under Core2A.

## Canonical worked-problem grammar

```text
QUESTION
-> REQUIRED KNOWLEDGE
-> WHAT SHOULD I NOTICE?
-> PROBLEM REPRESENTATION
-> WHY THIS MODEL?
-> FIRST MOVE
-> FULL WORKING
-> PHYSICAL / DIMENSIONAL / LIMITING CHECK
-> COMMON WRONG ROUTE
-> WHY THIS QUESTION IS HARD
-> WHAT WOULD CHANGE IN A VARIATION?
```

## Support realization by band

### FOUNDATION_HIGH_SUPPORT

Prerequisite bridge -> full visual representation -> expert noticing -> worked first move -> full reasoned solution -> near-isomorphic legal generated practice when available.

### GUIDED

Recognition cue -> visual representation -> partially faded working -> full solution after learner attempt.

### STANDARD

Attempt first -> compact expert solution -> checks -> variation note.

### CHALLENGE_MINIMAL

Attempt first with minimal pre-solution cueing -> compact expert solution -> error analysis -> structural variation.

## Authority remains unchanged

Core2A remains the transfer-legality authority downstream of Core2 + Core1A taught-state receipts.

Knowledge percentage and owner override may choose support and selection **inside** that legal pool. They may never expand it.

A worked Core2A publication does not prove learner transfer or mastery.
