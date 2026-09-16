# Physics Self-Help Architecture V2 — difficulty-driven Core1A/1B, knowledge-driven Core2A/2B

## Canonical split

Every learner product must be usable without a teacher physically present.

There are now **two different adaptation control planes**.

| Family | Adaptation driver | Student knowledge % |
|---|---|---|
| Core1A / Core1B | intrinsic **bucket difficulty badge** | does **not** determine publication depth |
| Core2A / Core2B | **student knowledge %** | required unless explicitly waived by owner input |

This separation is intentional.

Core1A/Core1B answer: **how deeply must this subtopic itself be taught?**

Core2A/Core2B answer: **how much support and what challenge level should this learner receive?**

The two signals must not be collapsed.

## Core1A / Core1B — always subtopic-bucket-wise

Every Core1A/Core1B product is built around a stable subtopic/SBA bucket.

The bucket owns one intrinsic publication badge:

- `EASY`
- `MEDIUM`
- `HARD`

Legacy `LOW` is treated as an alias for `EASY`.

Learner knowledge percentage is not a depth control for these products. Existing historical `prior_knowledge_pct` fields may remain temporarily for migration compatibility, but new Core1A/Core1B publication decisions must not depend on them.

### EASY

- soft capacity ceiling: about **10 pages**;
- visual and step-by-step teaching still required where useful;
- no web research requirement for representation design unless source integrity or factual uncertainty requires it;
- keep the explanation compact and complete;
- no decorative images.

### MEDIUM

- soft capacity ceiling: about **20 pages**;
- web research required before finalising representation/diagram strategy;
- decompose into sub-subtopics when several distinct inferential jumps exist;
- use dedicated diagrams for major representation/model changes;
- step-by-step explanation should be detailed.

### HARD

- soft capacity ceiling: about **30 pages**;
- web research required before finalising pedagogy and visual strategy;
- sub-subtopic decomposition is expected when conceptual jumps can be isolated;
- use dedicated diagrams/visual sequences for major transitions;
- maximise explanatory granularity without padding or repetition.

These page numbers are **capacity ceilings, not targets**. There is no educational evidence that page count itself creates depth. If the concept is complete in fewer pages, stop. If a coherent bucket requires more than the ceiling, split it further or obtain an explicit owner exception rather than compressing away necessary reasoning.

### Layer distinction inside the same bucket

**Core1A — declarative deep teaching**

Teach the subtopic completely: physical idea, prerequisite bridge, representations, equations, model conditions, worked reasoning, misconception contrast, checks.

**Core1B — generative concept coach**

Use the same bucket depth, but make the learner actively reconstruct it:

`OPEN PROMPT → ATTEMPT → H1 NOTICE → H2 REPRESENT → H3 START → RETRY → LOCAL CHECK → REPAIR`

Core1B must not become a chatbot transcript and must not strand the learner.

## Core2A / Core2B — learner knowledge is required

Core2 adaptation requires exactly one declared basis:

### `KNOWLEDGE_PERCENT`

Provide:

`student_knowledge_pct: 0..100`

The percentage controls support density and challenge selection **within the already legal Core2A pool**.

### `OWNER_OVERRIDE`

Use only when the knowledge percentage is unknown or deliberately unavailable.

Required owner input:

- `owner_ref`;
- `reason`;
- `support_band`.

Allowed support bands:

- `FOUNDATION_HIGH_SUPPORT`
- `GUIDED`
- `STANDARD`
- `CHALLENGE_MINIMAL`

The override waives only the missing knowledge percentage. It cannot:

- expand the Core2A legal pool;
- rewrite frozen Core2 questions;
- manufacture learner mastery;
- bypass Core1B evidence requirements in Core2B.

No silent default is allowed.

## Default operational knowledge bands

These are product-routing heuristics, not psychometric claims:

- `0–25` → `FOUNDATION_HIGH_SUPPORT`
- `26–50` → `GUIDED`
- `51–75` → `STANDARD`
- `76–100` → `CHALLENGE_MINIMAL`

Owner policy may tune these thresholds without changing Physics authority.

## Core2A realization

Core2A remains declarative and solution-level.

Lower knowledge means more prerequisite bridge, visual representation, expert noticing, worked first move and full reasoning.

Higher knowledge means more attempt-first exposure and a more compact expert solution after the attempt.

The source question itself remains frozen.

## Core2B realization

Core2B remains open-ended and attempt-first at every knowledge band.

Knowledge/support level changes:

- which legal challenge appears first;
- how quickly structural distance increases;
- whether hints are visible or hidden by default;
- reveal timing;
- repair density.

It never changes the legal pool.

## Research basis for the Core1A/1B difficulty policy

The policy uses several well-supported instructional-design principles:

1. **Segmenting:** complex material benefits from meaningful learner-paced segments rather than one continuous block.
2. **Signaling/cueing:** visuals and text should direct attention to relevant structure.
3. **Multiple representations in Physics:** diagrams, graphs, mathematics and words can improve problem solving when they are complete and correct.
4. **No visual inflation:** supplying more diagrams is not automatically beneficial; visuals must perform an instructional function.

Therefore Hard/Medium buckets require research-led representation planning, but they do not receive arbitrary image quotas.

## Normative machine policies

- `Blueprint/policy/self-help-core-publication.v2.json`
- `Blueprint/policy/core1ab-bucket-depth.v1.json`
- `Blueprint/policy/core2ab-knowledge-routing.v1.json`

Existing authority/runtime custody remains unchanged.
