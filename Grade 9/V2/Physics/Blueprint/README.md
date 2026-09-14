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

## Learner-product topology — SELF-HELP V1

The learner-facing definition is now explicit and separate from runtime authority.

Every Core learner product must be usable without a teacher physically present. The canonical learner modes are:

| Core | Learner mode | Primary question |
|---|---|---|
| Core1 | Basic declarative notes | What is true? |
| Core1A | Declarative deep teaching | Teach me this subtopic completely. |
| Core1B | Generative concept coach | Can I reconstruct, explain, represent and independently use what was taught? |
| Core2 | Frozen source-question authority | What is being tested? |
| Core2A | Declarative worked transfer atlas | Show me how an expert recognizes and solves this problem family. |
| Core2B | Generative transfer coach | Can I recognize, select and transfer it when the surface changes? |

This learner-product split does **not** weaken the authority split. Core1B still cannot author Physics semantics; Core2B still cannot legalize transfer.

The machine-readable policy is:

`policy/self-help-core-publication.v1.json`

The policy standardizes:

- self-help resolution for every open-ended prompt;
- `H1 NOTICE → H2 REPRESENT → H3 START`;
- answer/check/repair availability without requiring a teacher;
- declarative A-layer products versus generative B-layer products;
- difficulty adaptation by support density rather than mutation of frozen Core2 source;
- explicit visual function tags;
- immediate, later, mixed and Core2B retrieval;
- full-solution exposure as teaching, never independent mastery evidence.

## Core1B — ACTIVE runtime + v2 learner-product grammar

Core1B now combines strict runtime custody with a generative self-teaching learner surface:

- exact released Core1A ref + digest required;
- fine-grained atom graph with evidence-backed prerequisite skipping;
- readiness fields are requirements, never mastery evidence;
- learner state changes only from observed `LEARNER_RESPONSE`, `DIAGNOSTIC`, or `TEACHER_OBSERVATION` events;
- event identity/order and evidence/event digests are append-only;
- `APPLICABILITY` is required when upstream model validity is required;
- `EXPLAIN` follows the upstream capability contract;
- `INDEPENDENT` release requires successful sufficiently low-hint independent/retrieval evidence;
- internal runtime labels are blocked from learner-facing text;
- learner episodes use open-ended attempt → progressive help → retry → local worked check → repair route;
- the product must not read as a chatbot transcript or minimally guided discovery.

See `../Core1B/LEARNER_PRODUCT_SPEC_v2.md`.

## Core2A — ACTIVE legality + declarative worked-atlas grammar

Core2A remains the transfer-legality compiler. Its learner-facing publication grammar now requires expert problem decomposition:

`QUESTION → NOTICE → REPRESENT → MODEL → FIRST MOVE → FULL WORKING → CHECK → WRONG ROUTE → HARDNESS → VARIATION`

Frozen Core2 source questions are not rewritten to make them easier. Difficulty adaptation changes support, reveal order, completion level, ordering and clearly-labelled generated-original variants.

See `../Core2A/LEARNER_PRODUCT_SPEC_v1.md`.

## Core2B — ACTIVE runtime + v2 learner-product grammar

Core2B consumes the actual Core2A product rather than accepting a local legality flag:

- exact Core2A legal-pool ref + digest and exact item ID required;
- every required capability is checked independently against a bound Core1B release plus observed transfer events;
- scalar `T0…T8` labels are descriptive only; authorization uses structural distance, representation change, model discrimination, multi-step bridge, synthesis and competitive mixing;
- representation shift cannot be invented downstream;
- purpose/retrieval only choose within the legal/evidence-eligible pool;
- error classification remains an explicit hypothesis;
- repair requests target the smallest explanatory atom set and cannot mutate Core1A/Core2A authority;
- incorrect/full-solution representation exposure cannot become representation mastery;
- learner episodes are attempt-first and must end with recognition, representation, model-selection, full working, transfer statement and repair route.

See `../Core2B/LEARNER_PRODUCT_SPEC_v2.md`.

## Three-topic falsification pilot

Before chapter-wide standardization, the self-help grammar must survive three different Physics structures:

1. projectile vertical-event/apex reasoning;
2. moving-launcher relative velocity;
3. Newton model-selection / free-body reasoning as a cross-topic design stress test.

The pilot is intentionally non-production where exact upstream authority is missing. SBA23 retains the exact-Q15 source hold.

Machine-readable pilot:

`topics/self-help-three-topic-falsification-pilot.v1.json`

Promotion requires machine policy PASS **and** human pedagogy review. A process-golden PASS is not evidence of real learner efficacy.

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

Run the three-topic falsification pilot. For each topic, produce one Core1B generative concept-coach slice, one Core2A declarative worked-atlas slice and one Core2B attempt-first transfer slice. Reject the grammar if it only works for projectile motion, if hints collapse into answer disclosure, if source-question immutability drifts, or if B-layer presentation leaks runtime internals.
