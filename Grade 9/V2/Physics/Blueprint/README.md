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

## Learner-product topology — SELF-HELP V5

Every learner product must be usable without a teacher physically present.

The learner-facing architecture is **family-first, asymmetric, technically explicit and fail-closed on visual quality**.

The canonical authoring hierarchy is:

```text
SUBTOPIC / SBA BUCKET
   ↓
hidden invariant(s)
   ↓
prerequisite bridges
   ↓
inferential jumps
   ↓
problem families
   ↓
TECHNICAL TEACHING UNITS (TTUs)
   ↓
Core1A / Core1B / Core2A / Core2B realization
```

Normative learner-product architecture:

`SELF_HELP_ARCHITECTURE_V5.md`

Machine-readable policies:

- `policy/self-help-core-publication.v5.json`
- `policy/technical-teaching-unit.v1.json`
- `policy/physics-representation-semantic-quality.v1.json`
- `policy/pdf-layout-integrity.v2.json`
- `policy/core1ab-bucket-authoring.v2.json`
- `policy/core2ab-knowledge-routing.v1.json`

### Technical Teaching Unit (TTU)

A technical learner unit is complete only when it binds:

`PHYSICAL SETUP → TECHNICAL REPRESENTATION → GOVERNING RELATION → MAPPING/WORKING → RESULT → VERIFICATION`

A page does **not** become technical merely because it contains a diagram and an equation.

The learner must be able to see how the variables/vectors/features in the representation map into the equation and then into the working.

### What counts as a Physics representation

Eligible technical forms include:

- vector/component construction;
- free-body diagram;
- geometry/ray construction;
- trajectory/graph with meaningful axes;
- event timeline;
- state transition;
- frame/coordinate diagram;
- physical-variable table;
- equation dependency map.

The following do not count toward technical closure:

- generic text cards;
- decorative arrows;
- unlabeled axes;
- oversized empty coordinate planes;
- decorative illustrations;
- prose converted into shapes;
- figures not used by the accompanying working;
- a final equation floating beneath an unmapped picture.

### Core1A / Core1B control plane

Core1A/Core1B are always subtopic/SBA-bucket-wise. Student knowledge % does **not** drive authored depth.

The bucket receives one intrinsic `EASY | MEDIUM | HARD` badge. The badge controls inferential/technical closure, not image count or prose length.

Core1A uses soft capacity ceilings of about 10 / 20 / 30 pages for Easy / Medium / Hard. These remain ceilings, not targets.

Core1B does not inherit those page ceilings. Its length comes from the fragile technical checkpoints and problem families that need learner reconstruction.

### A/B are dominant modes, not duplicate books

- **Core1A** — declarative-dominant complete TTUs.
- **Core1B** — generative-dominant reconstructable TTUs.
- **Core2A** — declarative-dominant worked problem TTUs selected by legal problem family and learner support route.
- **Core2B** — generative-dominant transfer TTUs using fresh legal items/variants when possible.

Core1B may contain targeted post-attempt explanation. Core1A may contain compact generative checks. The system must not create parallel duplicate books.

### Core1B — ACTIVE runtime + v6 learner-product grammar

Core1B retains strict evidence custody but now requires technical reconstruction where the capability is technical.

A Hard Core1B page is noncompliant if it is mainly prose + blank lines while an expert would naturally use a vector diagram, graph, component split, event line, geometry construction, free-body diagram or symbolic relation.

See `../Core1B/LEARNER_PRODUCT_SPEC_v6.md`.

### Core2A — ACTIVE legality + v4 worked-TTU grammar

Knowledge % is required unless explicitly waived by owner input.

Core2A selects representative legal exemplars by problem family/demand. Each exemplar must expose setup extraction, technical representation, governing relation, intermediate mapping/working, result and verification.

A large diagram plus one final equation is not a worked solution.

Model-discrimination pages must compare actual Physics structure — physical trigger, representation/model, first move and why a competing model is rejected. Generic A/B/C cards do not count as technical Physics representation.

See `../Core2A/LEARNER_PRODUCT_SPEC_v4.md`.

### Core2B — ACTIVE runtime + v5 transfer-TTU grammar

Core2B consumes the exact Core2A legal pool and observed Core1B evidence.

When representation/model choice is part of transfer, the learner must select or construct it before reveal. Core2B should avoid mirroring Core2A item-for-item where fresh legal items/variants exist.

See `../Core2B/LEARNER_PRODUCT_SPEC_v5.md`.

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

No silent default is allowed. The owner override waives only missing knowledge data; it cannot expand legality or rewrite frozen source questions.

---

## Visual publication gate

Successful PDF generation is **not** a visual pass.

Production learner PDFs require:

- flow layout or explicit collision validation;
- legible technical labels/equations at final size;
- figure labels that do not overlap vectors/objects;
- figures cropped to instructional content;
- proportional use of figure area;
- figure and bound working kept adjacent;
- page-by-page render review;
- montage/thumbnail review for new figure grammars.

Fail closed on microscopic labels, oversized low-information figures, excessive unused plotting space, clipped content, text/figure collision, orphaned figures and unreadable equations.

---

## Three-topic falsification pilot

The learner grammar must survive:

1. projectile vertical-event/apex reasoning;
2. moving-launcher relative velocity;
3. Newton model-selection / free-body reasoning.

SBA23 retains the exact-Q15 source hold. Learner-product design cannot override source custody.

Machine-readable pilot:

`topics/self-help-three-topic-falsification-pilot.v3.json`

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

Rebuild M2D-SBA-23 only after the TTU/representation/layout gates are active. Reject the build if:

- a page contains technical-looking graphics without representation-to-equation binding;
- a Hard B-layer degenerates into prose prompts;
- a worked solution skips setup extraction or intermediate mapping;
- model-discrimination uses generic cards instead of Physics structure;
- labels become microscopic or collide with vectors;
- oversized figures displace the technical working;
- Q15 source custody is weakened.
