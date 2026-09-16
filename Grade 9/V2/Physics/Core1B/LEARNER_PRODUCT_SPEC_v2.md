# Physics Core1B v2 — Generative Concept Coach

## Learner-product purpose

Core1B is a **self-guided generative teaching product**. It asks:

> Can the learner reconstruct, explain, represent and independently use what Core1A taught?

Core1B is not a chatbot transcript and it is not minimally guided discovery. It must be usable by a learner without a teacher physically present.

## Canonical episode grammar

Every substantial learner episode follows:

```text
OPEN-ENDED PROMPT
  -> learner attempt / prediction / diagram / explanation
  -> H1 NOTICE
  -> H2 REPRESENT
  -> H3 START
  -> TRY AGAIN
  -> CHECK AFTER ATTEMPT
  -> conceptual reconstruction
  -> repair route
```

`H1/H2/H3` are optional reveals. They must not all be exposed at once by default.

### Prompt families

Use a deliberate mix of:

- **PREDICT** — what will happen before calculation?
- **EXPLAIN** — why does this happen?
- **REPRESENT** — draw/complete a diagram, graph, table or component model.
- **MODEL_SELECT** — which model applies and why?
- **FIRST_MOVE** — what should be done first before calculation?

Do not turn every paragraph into a question. Core1B should operate in coherent teaching episodes.

## Local self-help requirement

Every open-ended prompt must have a local resolution, either at the bottom of the same page or immediately following:

1. correct reasoning;
2. visual/representation where useful;
3. compact symbolic form if needed;
4. physical meaning;
5. common wrong route or misconception when material;
6. smallest repair destination.

A publication may never end a learner dead-end with only “ask your teacher”.

## Fading and independence

The default sequence is:

```text
reconstruct concept
-> guided use
-> faded completion
-> independent use
-> later retrieval
```

A learner may skip already-secure prerequisite episodes only from provenance-backed observed evidence. Authored readiness/configuration alone is not evidence.

## Visual policy

Every learner-facing figure must serve at least one explicit function:

`REPRESENT`, `EXPLAIN`, `COMPARE`, `PREDICT`, `DERIVE`, or `CHECK`.

Decorative visuals do not satisfy representation requirements.

## Runtime authority remains unchanged

This learner-product grammar does **not** relax Core1B custody:

- exact Core1A authority ref + digest remains mandatory;
- Core1B may not author new Physics semantics;
- `INDEPENDENT` still requires observed low-hint evidence satisfying the configured criteria;
- full-solution exposure is teaching, not mastery evidence;
- Core1B cannot legalize Core2A/Core2B transfer.
