# Physics Self-Help Architecture V3 — family-first, asymmetric A/B realization

## Premise

Every learner product must be usable without a teacher physically present.

The architecture is built around a **shared bucket learning model**, not around parallel books of equal depth.

```text
SUBTOPIC / SBA BUCKET
        ↓
HIDDEN INVARIANT(S)
        ↓
PREREQUISITE BRIDGES
        ↓
INFERENTIAL JUMPS
        ↓
REPRESENTATIONS + MISCONCEPTIONS
        ↓
PROBLEM FAMILIES
        ↓
        ├──────────────→ CORE1A  declarative-dominant teaching
        │
        └──────────────→ CORE1B  generative-dominant reconstruction

CORE2 FROZEN QUESTION SET
        ↓
LEGAL PROBLEM-FAMILY MAP
        ↓
student knowledge % OR owner override
        ↓
        ├──────────────→ CORE2A  declarative worked problem learning
        │
        └──────────────→ CORE2B  generative attempt-first transfer
```

The A/B distinction is a **dominant learner mode**, not an exclusivity rule.

- A-layers are declarative-dominant, but may contain prediction, quick checks and short completion tasks.
- B-layers are generative-dominant, but may explain after an attempt, show a worked reconstruction, and reteach the smallest failed bridge.

The architecture must not create two near-duplicate books.

---

## 1. Shared bucket learning model

Before Core1A or Core1B publication, each bucket must expose the same authoring map:

1. **hidden invariants** — the ideas that survive surface change;
2. **prerequisite bridges** — what earlier knowledge must be activated;
3. **inferential jumps** — non-obvious reasoning steps that cannot be left implicit;
4. **representations** — diagrams, graphs, tables, equations, event lines or verbal models that close those jumps;
5. **misconceptions** — predictable incorrect models that need contrast;
6. **problem families** — structurally distinct ways the capability appears in questions;
7. **source/Core2 linkage** — exact question ownership, held states and source-integrity boundaries;
8. **fragile checkpoints** — the jumps or families most likely to fail under independent use.

This map is the stable bridge between Core1A and Core1B.

---

## 2. Core1A / Core1B control plane

Core1A and Core1B are always built subtopic/SBA-bucket-wise.

Student knowledge percentage does **not** control their authored depth.

The bucket has one intrinsic publication badge:

- `EASY`
- `MEDIUM`
- `HARD`

Legacy `LOW` aliases to `EASY`.

### What the badge controls

The badge controls primarily:

- how much declarative closure Core1A needs;
- how many prerequisite bridges and inferential jumps must be made explicit;
- whether web research is required for representation/pedagogy planning;
- how much sub-subtopic decomposition is needed;
- which jumps/families Core1B must exercise generatively.

The badge does **not** require Core1A and Core1B to have equal page counts.

---

## 3. Difficulty means inferential closure, not visual quantity

### EASY

- Core1A soft capacity ceiling: about **10 pages**;
- explicit but compact teaching;
- web research not required unless source integrity, factual uncertainty or a missing representation requires it;
- close every necessary inferential jump;
- use the minimum set of meaningful representations.

### MEDIUM

- Core1A soft capacity ceiling: about **20 pages**;
- web research required before finalising pedagogy/representation strategy;
- decompose when several distinct inferential jumps or problem families exist;
- close each major jump with an adequate explanation/representation;
- include misconception contrast and representative worked reasoning.

### HARD

- Core1A soft capacity ceiling: about **30 pages**;
- web research required;
- sub-subtopic decomposition expected where jumps can be isolated;
- every major inferential jump must be explicitly closed;
- multiple problem families may require separate visual/reasoning narratives;
- depth may be high, but padding, decorative visuals and repeated explanations are forbidden.

The page numbers are **soft Core1A capacity ceilings, not targets**. If the teaching is complete earlier, stop. If a coherent bucket cannot fit without hiding reasoning, split it further or obtain an explicit owner exception.

### Representation sufficiency rule

Do not use `visual_intensity` as a proxy for quality.

The normative rule is:

> Every major inferential jump must have an adequate representation or explanation when a representation materially helps the learner cross that jump.

One excellent diagram may close several jumps. Ten decorative diagrams do not satisfy the rule.

---

## 4. Core1A — declarative-dominant deep teaching

Core1A asks:

> Teach me this subtopic completely enough that I can form the right mental model and see how the problem families work.

Core1A normally contains:

- physical idea / phenomenon;
- prerequisite bridge;
- representations;
- words → symbols/equations;
- model conditions;
- worked examples;
- misconception contrasts;
- problem-family methods;
- physical / dimensional / limiting checks;
- quick checks or short completion tasks where useful;
- source boundary and Core2 linkage.

Core1A may include small generative moments. It should not become passive textbook prose merely to preserve an A/B label.

Core1A publication/readiness text is a teaching target, not learner-mastery evidence.

---

## 5. Core1B — generative-dominant reconstruction

Core1B asks:

> Can I reconstruct, explain, represent and independently use the fragile parts of what Core1A taught?

Core1B inherits **capability scope and fragile checkpoints**, not Core1A's page budget.

There is no `EASY≈10 / MEDIUM≈20 / HARD≈30` page target for Core1B.

Core1B length is derived from the smallest set of generative episodes needed to cover:

- every fragile inferential jump;
- every material misconception that can corrupt later reasoning;
- every distinct problem family that needs independent recognition;
- at least one mixed/retrieval checkpoint when multiple families can be confused.

A 28-page Hard Core1A may legitimately produce an 11-page Core1B. Another bucket may need more. Symmetry is not a quality signal.

### Core1B task grammar is conditional

Do **not** force every prompt through a full H1/H2/H3 sequence.

Use the smallest self-help grammar that fits the task:

#### Micro prediction / explanation

`PROMPT → ATTEMPT → MODEL RESPONSE / EXPLANATION`

#### Representation task

`DRAW / COMPLETE / TRANSLATE → CHECK REPRESENTATION → EXPLAIN KEY FEATURE`

#### Concept reconstruction

`OPEN PROMPT → ATTEMPT → OPTIONAL CLUE → CONCEPTUAL CHECK`

#### Substantive problem / fragile first move

`QUESTION → ATTEMPT → H1 NOTICE → H2 REPRESENT → H3 START → RETRY → FULL CHECK → REPAIR`

#### Mixed retrieval

`UNLABELED TASK → ATTEMPT → COMPACT CHECK → FAMILY / INVARIANT IDENTIFICATION`

### Hint ladder rule

`H1 NOTICE → H2 REPRESENT → H3 START` is the **standard rescue ladder for substantive tasks**, not a mandatory template for every interaction.

Every open-ended prompt still requires a local resolution on the same page or immediately following.

---

## 6. Core2A / Core2B control plane

Core2A/Core2B adaptation requires exactly one declared basis:

### `KNOWLEDGE_PERCENT`

`student_knowledge_pct: 0..100`

### `OWNER_OVERRIDE`

When knowledge percentage is unknown or deliberately unavailable:

- `owner_ref`;
- `reason`;
- `support_band`.

Allowed support bands:

- `FOUNDATION_HIGH_SUPPORT`
- `GUIDED`
- `STANDARD`
- `CHALLENGE_MINIMAL`

No silent default is allowed.

The owner override waives only missing knowledge percentage. It cannot expand legality, rewrite frozen Core2 questions, bypass evidence, or manufacture mastery.

Default routing bands remain product heuristics, not psychometric claims:

- `0–25` → `FOUNDATION_HIGH_SUPPORT`
- `26–50` → `GUIDED`
- `51–75` → `STANDARD`
- `76–100` → `CHALLENGE_MINIMAL`

---

## 7. Core2A — representative worked problem-family learning

Core2A asks:

> Show me how an expert recognises and solves the legal problem families I am ready to study.

Core2A is **not** a fully solved duplicate of every Core2 question.

From the exact legal Core2A pool, choose representative worked exemplars by:

- problem family;
- structural demand;
- learner knowledge/support band;
- misconception risk;
- representation need;
- owner purpose where applicable.

A representative item may use:

`QUESTION → NOTICE → REPRESENT → MODEL → FIRST MOVE → WORKING → CHECK → WRONG ROUTE → VARIATION`

but the support density is adapted by knowledge/owner input.

Frozen source questions remain unchanged. Generated-original variants must already be legal under Core2A.

Core2A should avoid solving every legal question unless the owner explicitly requests an exhaustive worked atlas.

---

## 8. Core2B — transfer across changed surfaces

Core2B asks:

> Can I recognise, select and transfer the capability when the surface, target, representation or structure changes?

Core2B remains attempt-first.

It should not mirror Core2A one-for-one.

Where the legal pool permits, Core2B should prefer different items from the worked Core2A exemplars so success cannot be reduced to replaying a memorised solution.

Core2B selection should deliberately vary independent dimensions such as:

- structural distance;
- direction/sign reversal;
- reversed target;
- representation change;
- model discrimination;
- constraint inversion;
- multi-step bridge;
- synthesis;
- competitive mixing.

Knowledge/support band changes item ordering, distance progression, hint visibility and repair density. It never changes legality.

For substantive transfer tasks, use the progressive rescue ladder when needed. Micro discrimination or recognition checks may use a shorter local resolution.

---

## 9. Self-help contract

All learner products must be usable without a teacher.

Therefore:

- every open-ended prompt has an explicit local answer/resolution;
- no wrong answer ends with only “ask your teacher”;
- hints are progressive when the task warrants them;
- answers explain reasoning, not only the final number;
- repair points to the smallest explanatory gap;
- model applicability is visible when material;
- full-solution exposure is teaching, not independent mastery evidence.

---

## 10. Benchmark-derived authoring rule

Mature buckets such as projectile-on-incline and timed-event projectile work demonstrate the preferred instructional rhythm:

`IDEA → REPRESENTATION → WORKED EXAMPLE → PROBLEM FAMILY → ATTEMPT → OPTIONAL HINTS → ANSWER → NEXT FAMILY → MIXED SYNTHESIS`

Do not split this rhythm mechanically into two duplicate books.

Use Core1A to establish the declarative model and Core1B to revisit only the fragile points and families generatively.

---

## 11. Authority boundaries remain unchanged

- Core1B cannot author new Physics semantics.
- Core2B cannot legalize transfer.
- Teaching configuration/readiness text is not learner mastery.
- Core2 source questions remain frozen except governed source-integrity correction.
- Core2A legal-pool custody remains exact.
- Full-solution exposure cannot become representation mastery.

## Normative machine policies

- `Blueprint/policy/self-help-core-publication.v3.json`
- `Blueprint/policy/core1ab-bucket-authoring.v2.json`
- `Blueprint/policy/core2ab-knowledge-routing.v1.json`

V3 supersedes the learner-product symmetry assumptions in V2. Existing runtime/authority custody remains unchanged.
