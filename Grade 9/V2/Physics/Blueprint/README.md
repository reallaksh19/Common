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
CORE1A released semantics → Publication IR → composition-only renderer → render custody/preflight
```

Execution order may vary. **Authority order may not.** A-layers authorize; B-layers execute authorized experiences and capture observed evidence.

## Core1B — ACTIVE

Core1B now implements the PR #368 concept with stricter Blueprint custody:

- exact released Core1A ref + digest required;
- fine-grained atom graph with evidence-backed prerequisite skipping;
- readiness fields are requirements, never mastery evidence;
- learner state changes only from observed `LEARNER_RESPONSE`, `DIAGNOSTIC`, or `TEACHER_OBSERVATION` events;
- event identity/order and evidence/event digests are append-only;
- `APPLICABILITY` is required when upstream model validity is required;
- `EXPLAIN` follows the upstream capability contract;
- `INDEPENDENT` release requires a successful independent/retrieval event satisfying all required criteria with sufficiently low hint dependence;
- internal runtime labels are blocked from learner-facing text.

## Core2B — ACTIVE

Core2B consumes the actual Core2A product rather than accepting a local legality flag:

- exact Core2A legal-pool ref + digest and exact item ID required;
- every required capability is checked independently against a bound Core1B release plus observed transfer events;
- scalar `T0…T8` labels are descriptive only; authorization uses structural distance, representation change, model discrimination, multi-step bridge, synthesis and competitive mixing;
- representation shift cannot be invented downstream and requires upstream authorization plus successful observed representation use;
- purpose/retrieval only choose within the legal/evidence-eligible pool;
- error classification remains an explicit hypothesis;
- repair requests target the smallest explanatory atom set and cannot mutate Core1A/Core2A authority;
- incorrect representation exposure cannot become representation mastery.

The Blueprint workflow runs both runtime falsifier suites before continuing through the existing routing, Join, Core1A, Core2A, Publication IR and render/composition chain.

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

Runtime activation cannot substitute for pedagogical/manuscript release evidence.

## Next Blueprint tranche

Continue the real Core1A migration beginning with `M2D-SBA-04`: convert its existing learning atoms, misconceptions and H1/H2/H3 traces into repository-backed `1A0…1A11` evidence, expose genuine missing stages, and only then open its real `1A12` manuscript/publication path.
