# Physics Core2A v3 — Declarative Worked Problem-Family Learning

## Learner-product purpose

Core2A is a **self-guided declarative-dominant problem-learning product**.

> Show me how an expert recognizes and solves representative legal problem families I am ready to study.

Core2A is not an answer key and is not a fully solved duplicate of every Core2 question by default.

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

- `FOUNDATION_HIGH_SUPPORT`
- `GUIDED`
- `STANDARD`
- `CHALLENGE_MINIMAL`

There is no silent default.

The owner override waives only missing knowledge data. It does not expand transfer legality or alter frozen source questions.

See `../Blueprint/policy/core2ab-knowledge-routing.v1.json`.

## Default operational routing

These are product heuristics, not psychometric claims:

- 0–25 -> FOUNDATION_HIGH_SUPPORT
- 26–50 -> GUIDED
- 51–75 -> STANDARD
- 76–100 -> CHALLENGE_MINIMAL

## Frozen-source and legality rules

Core2 source items remain frozen authority.

Core2A must not rewrite a frozen Core2 question to make it easier.

Generated-original variants may appear only when they are already legal under Core2A.

Knowledge percentage or owner override may choose support and selection **inside** the legal pool; neither can expand that pool.

## Problem-family map first

Before publication, compile the legal pool into a problem-family map.

For each family, record:

- hidden invariant/capability;
- source items;
- structural demand;
- representation demand;
- likely misconception/wrong route;
- legal generated-original variants, if any;
- eligible support bands/purposes.

The publication then selects representative worked exemplars from that map.

## Representative selection rule

Select worked exemplars by:

- problem family;
- structural demand;
- learner knowledge/support band;
- misconception risk;
- representation need;
- owner purpose where relevant.

Do not solve every legal Core2 item by default.

An exhaustive worked atlas is allowed only when explicitly requested by the owner and still must preserve source custody.

## Worked exemplar grammar

A nontrivial representative item may use:

```text
QUESTION
→ WHAT SHOULD I NOTICE?
→ PROBLEM REPRESENTATION
→ WHY THIS MODEL?
→ FIRST MOVE
→ FULL WORKING
→ PHYSICAL / DIMENSIONAL / LIMITING CHECK
→ COMMON WRONG ROUTE
→ WHAT MAKES THIS FAMILY HARD?
→ WHAT CHANGES IN A VARIATION?
```

The grammar is a support toolbox, not a requirement to make every item visually identical.

## Support realization by band

### FOUNDATION_HIGH_SUPPORT

Prerequisite bridge -> explicit representation -> expert noticing -> worked first move -> full reasoned solution -> near-isomorphic legal practice when available.

### GUIDED

Recognition cue -> representation -> partially faded working -> full solution after learner attempt.

### STANDARD

Attempt first -> compact expert solution -> checks -> variation note.

### CHALLENGE_MINIMAL

Attempt first with minimal pre-solution cueing -> compact expert solution -> error analysis -> structural variation.

## Dominant mode, not exclusive content

Core2A is declarative-dominant but may include a short attempt before revealing a worked solution.

The learner should still be shown expert recognition and reasoning at solution level.

## Relationship to Core2B

Core2A teaches representative legal problem families.

Core2B should **not** merely replay the same worked exemplars item-for-item.

Where the legal pool allows, reserve different legal items or variants for Core2B transfer so success cannot be reduced to memorising the Core2A solution.

## Authority remains unchanged

- Core2A remains the transfer-legality authority downstream of Core2 + Core1A taught-state receipts.
- Knowledge percentage and owner override cannot expand legality.
- A worked Core2A publication does not prove learner transfer or mastery.
