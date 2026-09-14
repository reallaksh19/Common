# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the **canonical orchestration root for Physics Blueprint work**. Role-specific sibling directories (`CoreAuthoring/`, `Core2Transfer/`, `Core1A/`, `Core1B/`, `Core2A/`, `Core2B/`, `Representation/`) are subordinate execution kits.

## Active authority topology and learner runtime

```text
ORIGINAL / OBSERVED GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 ↔ independent second pass ↔ CORE2
        ↓
       JOIN
        ↓
learner state × purpose
        ↓
CORE1A 1A0…1A11
        ↓
1A12 manuscript + T receipts ─────────────→ CORE2A legal transfer pool
        ↓                                      ↓
released teaching authority                 exact legal-pool custody
        ↓                                      ↓
      CORE1B ── observed learner evidence ─→ CORE2B
        ↑                                      │
        └──── targeted repair request ─────────┘
                                               ↓
                                  attempts / retrieval evidence
                                               ↓
                                      EVIDENCE + CONTROL

Publication remains separate:
Core1A released semantics → Publication IR → composition-only renderer → render custody/preflight
```

Execution order may vary. **Authority order may not.**

---

## Learner-product topology — SELF-HELP V3

Every learner product must be usable without a teacher physically present.

The learner-facing architecture is now **family-first and asymmetric**. Core1A/Core1B are not parallel books of equal depth; Core2A/Core2B are not solved/open-ended copies of the same item set.

The authoring hierarchy is:

```text
SUBTOPIC BUCKET
   ↓
hidden invariant(s)
   ↓
prerequisite bridges
   ↓
inferential jumps
   ↓
representations + misconceptions
   ↓
problem families
   ↓
Core1A declarative-dominant teaching
   ↓
Core1B generative reconstruction checkpoints
   ↓
Core2A representative worked problem-family learning
   ↓
Core2B transfer across changed surfaces
```

Normative learner-product architecture:

`SELF_HELP_ARCHITECTURE_V3.md`

Machine-readable policies:

- `policy/self-help-core-publication.v3.json`
- `policy/core1ab-bucket-authoring.v2.json`
- `policy/core2ab-knowledge-routing.v1.json`

### Core1A / Core1B control plane

Core1A/Core1B are always subtopic/SBA-bucket-wise. Student knowledge % does **not** drive their authored depth.

The bucket receives one intrinsic `EASY | MEDIUM | HARD` badge.

The badge controls **inferential closure**, not page inflation or visual quantity.

Core1A uses soft capacity ceilings of about 10 / 20 / 30 pages for Easy / Medium / Hard. These are ceilings, not targets.

Core1B does **not** inherit those page ceilings. Its length is derived from the smallest set of generative checkpoints needed to cover:

- fragile inferential jumps;
- material misconceptions;
- distinct problem-family recognition;
- mixed/retrieval discrimination when families can be confused.

A Hard 28-page Core1A may legitimately have an 11-page Core1B.

### A/B are dominant modes, not exclusive content types

- **Core1A** is declarative-dominant, but may include prediction, quick checks, short completion and self-explanation prompts.
- **Core1B** is generative-dominant, but may include post-attempt explanation, worked reconstruction and targeted reteaching.
- **Core2A** is declarative-dominant problem learning and may let the learner attempt before revealing an expert solution.
- **Core2B** is generative-dominant transfer and may explain after the attempt.

The architecture must not create duplicate A/B books.

### Hint ladder — conditional, not universal

`H1 NOTICE → H2 REPRESENT → H3 START` remains the standard progressive rescue ladder for substantive tasks.

It is **not mandatory for every prompt**.

Micro prediction, explanation or representation tasks may use a shorter grammar as long as the learner receives an explicit local resolution.

---

## Core1B — ACTIVE runtime + v4 learner-product grammar

Core1B combines strict runtime custody with selective generative reconstruction:

- exact released Core1A ref + digest required;
- fine-grained atom graph with evidence-backed prerequisite skipping;
- readiness fields are requirements, never mastery evidence;
- learner state changes only from observed `LEARNER_RESPONSE`, `DIAGNOSTIC`, or `TEACHER_OBSERVATION` events;
- event identity/order and evidence/event digests are append-only;
- `APPLICABILITY` is required when upstream model validity is required;
- `EXPLAIN` follows the upstream capability contract;
- `INDEPENDENT` requires successful sufficiently low-hint independent/retrieval evidence;
- internal runtime labels are blocked from learner-facing text;
- authored learner episodes target fragile jumps and problem-family recognition rather than repeating the full Core1A publication;
- full H1/H2/H3 is reserved for substantive rescue tasks, not every micro-prompt.

See `../Core1B/LEARNER_PRODUCT_SPEC_v4.md`.

---

## Core2A — ACTIVE legality + v3 representative worked-family grammar

Core2A remains the transfer-legality compiler.

Knowledge % is required unless explicitly waived by owner input.

Its learner publication selects **representative worked exemplars by legal problem family and demand** rather than solving every legal item by default.

A representative exemplar may use:

`QUESTION → NOTICE → REPRESENT → MODEL → FIRST MOVE → WORKING → CHECK → WRONG ROUTE → VARIATION`

Frozen Core2 source questions are never rewritten to make them easier. Generated-original items must already be legal under Core2A.

See `../Core2A/LEARNER_PRODUCT_SPEC_v3.md`.

---

## Core2B — ACTIVE runtime + v4 transfer grammar

Core2B consumes the exact Core2A legal pool and observed Core1B evidence.

It is attempt-first, but it should **not mirror Core2A item-for-item**. Where the legal pool permits, use different legal items or variants so the learner must recognize structure rather than replay a memorized worked solution.

Transfer dimensions remain independent:

- structural distance;
- direction/sign reversal;
- reversed target;
- representation change;
- model discrimination;
- constraint inversion;
- multi-step bridge;
- synthesis;
- competitive mixing.

Runtime guards remain unchanged:

- exact Core2A legal-pool ref + digest and exact item ID required;
- every required capability checked against bound Core1B release/evidence;
- `T0…T8` descriptive only;
- representation shift cannot be invented downstream;
- purpose/retrieval only choose within the legal/evidence-eligible pool;
- error classification remains a hypothesis;
- repair targets the smallest explanatory atom set;
- incorrect/full-solution exposure cannot become representation mastery.

See `../Core2B/LEARNER_PRODUCT_SPEC_v4.md`.

---

## Core2 adaptation input

Core2A/Core2B require exactly one declared basis:

### KNOWLEDGE_PERCENT

`student_knowledge_pct: 0..100`

### OWNER_OVERRIDE

When knowledge % is unknown:

- `owner_ref`;
- `reason`;
- `support_band`.

Allowed support bands:

`FOUNDATION_HIGH_SUPPORT | GUIDED | STANDARD | CHALLENGE_MINIMAL`

No silent default is allowed. The owner override waives only missing knowledge data; it cannot expand legality or rewrite source questions.

---

## Three-topic falsification pilot — V3

Before chapter-wide standardization, the grammar must survive:

1. projectile vertical-event/apex reasoning;
2. moving-launcher relative velocity;
3. Newton model-selection / free-body reasoning.

The current falsifiers explicitly reject:

- Core1B duplicating Core1A page-for-page;
- forcing H1/H2/H3 on every prompt;
- treating Hard as visual/page inflation;
- Core2A solving every legal item by default;
- Core2B mirroring Core2A item-for-item;
- owner override expanding legality.

Machine-readable pilot:

`topics/self-help-three-topic-falsification-pilot.v3.json`

SBA23 retains the exact-Q15 source hold.

---

## Publication and real M2D boundary

The subject-wide 2D representation extension plus existing primitives gives the real 10-concept Motion-in-a-Plane chapter `10/10 READY_FOR_REALIZATION`, but publication remains independently blocked until a repository-backed non-golden Core1A `1A12` manuscript release exists.

```text
representation_status = READY_FOR_RENDER_ADAPTER
manuscript_release_status = ABSENT
composition_status = BLOCKED_UPSTREAM_MANUSCRIPT_RELEASE
publication_ir_gate = BLOCKED
renderer_invocation_allowed = false
release_authorized = false
```

Runtime activation and learner-product grammar cannot substitute for pedagogical/manuscript release evidence.

## Next Blueprint tranche

Rebuild the M2D-SBA-23 falsification prototype under V3. Use the benchmark-derived rhythm:

`IDEA → REPRESENTATION → WORKED EXAMPLE → PROBLEM FAMILY → ATTEMPT → OPTIONAL HINTS → ANSWER → NEXT FAMILY → MIXED SYNTHESIS`

Reject the build if Core1B repeats Core1A exposition, if Hard difficulty creates visual/page padding, if Core2A becomes an exhaustive solved duplicate by default, or if Core2B replays Core2A instead of testing transfer.
