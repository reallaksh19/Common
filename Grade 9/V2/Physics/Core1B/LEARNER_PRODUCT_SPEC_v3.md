# Physics Core1B v3 — Generative Concept Coach

## Learner-product purpose

Core1B is a **self-guided generative teaching product**.

> Can the learner reconstruct, explain, represent and independently use what Core1A taught?

Core1B is not a chatbot transcript and it is not minimally guided discovery.

## Depth control: bucket difficulty only

Core1B is always built subtopic/SBA-bucket-wise.

Its content depth is inherited from the bucket difficulty badge, **not** from student knowledge percentage:

- EASY: compact explicit teaching; soft ceiling ~10 pages;
- MEDIUM: researched visual/step design; soft ceiling ~20 pages;
- HARD: researched, highly segmented visual/step design; soft ceiling ~30 pages.

The page counts are capacity ceilings, not targets.

For MEDIUM/HARD, web research is required before finalising the representation/diagram strategy. Hard buckets should split into sub-subtopics when distinct conceptual jumps can be isolated.

See `../Blueprint/policy/core1ab-bucket-depth.v1.json`.

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

H1/H2/H3 are optional reveals and should not all be visible at once by default.

## Prompt families

Use a deliberate mix of:

- PREDICT;
- EXPLAIN;
- REPRESENT;
- MODEL_SELECT;
- FIRST_MOVE.

Do not turn every paragraph into a question. Use coherent episodes.

## Local self-help requirement

Every open-ended prompt must have a local resolution on the same page or immediately following:

1. correct reasoning;
2. representation where useful;
3. compact symbolic form if needed;
4. physical meaning;
5. common wrong route when material;
6. smallest repair destination.

Never end with only “ask your teacher”.

## Fading and independence

Default progression:

`reconstruct concept -> guided use -> faded completion -> independent use -> later retrieval`

Observed evidence may shorten the learner route, but it must not change the authored bucket depth contract itself.

## Visual policy

Every figure must serve at least one explicit function:

`REPRESENT | EXPLAIN | COMPARE | PREDICT | DERIVE | CHECK`

Decorative visuals do not satisfy the requirement.

## Runtime authority remains unchanged

- exact Core1A authority ref + digest remains mandatory;
- Core1B may not author new Physics semantics;
- INDEPENDENT still requires observed sufficiently low-hint evidence;
- full-solution exposure is teaching, not mastery evidence;
- Core1B cannot legalize Core2A/Core2B transfer.
