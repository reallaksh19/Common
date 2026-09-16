# Physics Self-Help Architecture V7 — CDAU / SDU / LAU + TTU families

V7 supersedes V6 for learner-product differentiation and adaptation. V6 remains the canonical history for reconstruction-complete TTUs; V7 places TTU inside a broader governance architecture so that content cannot be duplicated across Cores, difficulty cannot drift, and learner adaptation cannot leak into Core1 authoring.

## 0. Authority starts before product design

```text
ORIGINAL / OBSERVED GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 semantic grounding ↔ independent validation ↔ CORE2 assessment grounding
        ↓
       JOIN
        ↓
CANONICAL DOMAIN REGISTRY
        ↓
       CDAU
        ↓
   SDU or LAU
        ↓
CONCEPT_TTU or PROBLEM_TTU
        ↓
publication / learner runtime
        ↓
observed learner evidence
```

CDAU, SDU, LAU and TTU are product-differentiation systems. They do not create truth, rewrite frozen sources, manufacture evidence, or bypass upstream authority.

## 1. CDAU — Core Differentiation & Adaptation Unit

CDAU is the cross-Core governance envelope. It owns concerns that span both the study-material and question tracks:

- canonical asset identities and lineage;
- Core purpose contracts;
- example fingerprints;
- representation lineage;
- cross-Core duplication classification;
- source custody;
- owner decisions and provenance;
- handoff to SDU or LAU.

### Core purpose contract

| Core | Dominant purpose | Learner action | Prohibited degeneration |
|---|---|---|---|
| Core1 | compact orientation | read / recognise | deep duplicate textbook |
| Core1A | complete conceptual construction | inspect / interpret / follow / derive | question-bank dominance |
| Core1B | concept reconstruction | predict / generate / select / diagnose / derive / verify | second copy of Core1A |
| Core2 | frozen source question | attempt with source-defined support | rewritten source question |
| Core2A | expert problem learning | study / compare / understand worked reasoning | exhaustive solved copy of every legal item |
| Core2B | transfer and independent modelling | recognise / represent / select / solve / justify / transfer | replay of Core2A worked exemplar |

## 2. Content lineage and duplication control

Fundamental equations and definitions may legitimately recur. The architecture therefore distinguishes semantic reuse from pedagogical duplication.

Every canonical asset has an identity and each layer declares a usage mode:

```text
REFERENCE | EXPLAIN | DERIVE | WORKED_EXEMPLAR | COMPARE |
COMPLETE | RECONSTRUCT | SELECT | DISCRIMINATE | DIAGNOSE |
RETRIEVE | TRANSFER | VERIFY
```

Every worked/generated example also carries an example fingerprint:

```text
problem family
context
givens
numerical values
target unknown
representation
model sequence
special condition
solution path
```

Cross-Core relationship classification:

- `SEMANTIC_REUSE` — same law/definition, different legitimate use;
- `PEDAGOGICAL_TRANSFORMATION` — same asset transformed for a different learner action;
- `FADING_ANCHOR` — intentional same-item transition; must be declared;
- `STRUCTURAL_SIBLING` — same family, meaningfully changed instance;
- `FAR_TRANSFER_SIBLING` — changed representation/target/constraint/model mixture;
- `NEAR_DUPLICATE` — warning;
- `PEDAGOGICAL_DUPLICATION` — release failure.

Same context wording with changed object names alone is not a new example.

## 3. Owner control is global but bounded

Owner decisions may alter product/routing choices, including:

- difficulty badge when owner-provided;
- research depth;
- bucket/subtopic split;
- sub-subtopic split;
- Core inclusion/exclusion;
- representation choice;
- question-family inclusion where already legal;
- support band;
- missing-knowledge waiver;
- publication choice.

Every override records:

```text
SYSTEM_FINDING
OWNER_DECISION
FINAL_ACTION
```

Owner control may **not** override:

- Physics/Mathematics correctness;
- frozen source wording or source-integrity classification;
- provenance;
- observed evidence actually present/absent;
- exact Core2/Core2A legal-pool custody;
- upstream authority order.

An owner may choose a labelled design pilot when source custody is unresolved; the owner may not relabel unresolved source text as exact.

## 4. SDU — Study Differentiation Unit (Core1A / Core1B only)

SDU contains **no student knowledge percentage**. Core1 depth is controlled by intrinsic bucket difficulty.

Difficulty badge authority is explicit:

```text
OWNER_PROVIDED | SOURCE_PROVIDED | DERIVED | VALIDATED_DERIVED
```

If a badge is supplied by owner/source, SDU uses it and records any evidence-profile disagreement without silently changing it. If absent, SDU may derive it.

### Difficulty evidence profile

- prerequisite depth;
- element interactivity;
- inferential-jump severity;
- representation translation;
- model discrimination;
- sign/frame sensitivity;
- multi-step dependency;
- abstraction;
- misconception density;
- synthesis.

`EASY | MEDIUM | HARD` is therefore a governed classification, not a page-count proxy.

### Shared depth envelope

Both Core1A and Core1B may use the same maximum depth envelope:

- Easy: approximately up to 10 pages;
- Medium: approximately up to 20 pages;
- Hard: approximately up to 30 pages.

These are **available ceilings, never quotas**. They do not imply equal actual length, equal content, or equal learner action. Core1A and Core1B actual lengths are independently derived from closure needs.

### Research dossier

- Easy: external research not required by default unless semantic/source uncertainty exists;
- Medium: targeted semantic, misconception and representation research required;
- Hard: deep research required, with sub-subtopic decomposition when needed.

The dossier must produce design decisions, not merely a bibliography: selected/rejected representations, misconception treatments, representation-translation risks and visual implications.

## 5. LAU — Learner Adaptation Unit (Core2A / Core2B only)

Core2 adaptation requires exactly one declared selection basis:

1. `KNOWLEDGE_PERCENT`, capability-specific and 0..100; or
2. `OWNER_OVERRIDE` when usable knowledge evidence is unavailable.

No silent default such as 50% is allowed.

Learner model records:

- capability scope;
- knowledge percentage;
- provenance;
- confidence;
- evidence count / recency;
- subdimensions such as recognition, representation, model selection, first move, execution, explanation and verification.

Task demand remains multidimensional:

- structural distance;
- representation change;
- model discrimination;
- sign/direction reversal;
- reversed target;
- constraint inversion;
- multi-step bridge;
- synthesis;
- competitive mixing.

LAU routes support as a function of learner state × task demand × purpose. Support may change prerequisite bridge, representation completion, hint availability, working-step completeness, ordering and structural distance. It may not alter frozen source wording, Physics truth or legal-pool boundaries.

## 6. TTU is now a family

```text
TTU
├── CONCEPT_TTU  → Core1A / Core1B
└── PROBLEM_TTU  → Core2A / Core2B
```

Both share:

- authority binding;
- semantic target;
- canonical expert state;
- meaningful technical representation;
- representation-to-relation bindings;
- reasoning-state graph;
- verification;
- self-help closure;
- layout integrity.

### Concept TTU

Centres on conceptual change, equation meaning, representation, derivation, contrast and misconception repair.

### Problem TTU

Centres on recognition, model selection, constraint, first move, solution path, verification and transfer demand.

## 7. B-layer transformation modes

B-layer TTUs are not defined only by blanks. A learner transformation must be one or more of:

```text
PREDICTION
COMPLETION
GENERATION
SELECTION
DISCRIMINATION
DIAGNOSIS
DERIVATION_CONNECTION
VERIFICATION
TRANSFER
```

The transformation must materially change the learner's reasoning state and produce an observable learner product.

For reconstruction/completion tasks, omissions must reference canonical semantic element IDs and may not be cosmetic, arbitrary-number blanks or answer-copy tasks.

For generation/selection/discrimination/diagnosis/derivation tasks, the TTU must define the canonical expert state, expected learner product, bounded help, reveal rule and independent verification even when no literal omission exists.

## 8. Tutor dialogue is target-driven, not a rigid script

A substantive B-layer TTU may use authored prompts such as:

```text
P0 ATTEMPT
P1 NOTICE
P2 REPRESENT
P3 EXPLAIN
P4 CONNECT
P5 START
```

Only the prompts needed for the target reasoning are required. A graph reconstruction may use ATTEMPT → REPRESENT → CONNECT → CHECK; a misconception contrast may use PREDICT → EXPLAIN → CONTRAST → REVEAL.

Help is preauthored and bounded. Dynamic new semantics may not be invented by the runtime before canonical reveal.

## 9. Self-help closure

Every substantive learner unit must close the loop:

- task understandable without a teacher physically present;
- help route defined;
- canonical state/answer available under a defined reveal rule;
- misconception/repair route available;
- at least one independent verification route when technically applicable;
- next action defined.

`Compare with the answer` is not independent verification.

## 10. Core2A → Core2B lineage modes

Three relationships are permitted:

### FADING_ANCHOR
Same problem intentionally reused with support removed. Useful for transition; may **not** count as transfer evidence.

### STRUCTURAL_SIBLING
Same legal problem family, changed instance. May count as transfer evidence when all other evidence requirements are met.

### FAR_TRANSFER_SIBLING
Changed representation, target, constraint, structural distance or synthesis demand. May count as stronger transfer evidence when legal and observed.

Core2B should normally avoid exact item replay when a legal sibling exists.

## 11. Release gates

Pre-release:

1. `G-DOMAIN` — source/semantic grounding is valid;
2. `G-PURPOSE` — learner action belongs in this Core;
3. `G-DIFFERENTIATION` — no accidental neighboring-Core duplication;
4. `G-TTU` — technical teaching/problem interaction is complete;
5. `G-DIFFICULTY` — intrinsic difficulty or task demand is evidenced;
6. `G-FIT` — Core2 support is justified by learner knowledge or owner override;
7. `G-PUBLICATION` — rendered product is legible, integrated and collision-free.

Post-use:

8. `G-CALIBRATION` — observed learner behavior updates or challenges the predicted fit; it never retroactively creates source/semantic authority.

## 12. Canonical invariants

- Core1A/Core1B authored depth is never driven by student knowledge %.
- Core2A/Core2B adaptation never silently defaults when knowledge is unknown.
- Same equation across Cores is not automatically duplication; same equation + same example + same learner action + same solution path usually is.
- Owner override never rewrites truth, source custody or observed evidence.
- B-layer reconstruction is broader than omission/completion.
- Full-solution exposure is learning support, not mastery/transfer evidence.
- TTU technical completeness does not substitute for visual publication quality.
- CDAU/SDU/LAU cannot bypass the original ground-truth → Core1/Core2 → Join authority chain.

## 13. Normative V7 files

- `Blueprint/contracts/core-differentiation-adaptation-unit.schema.json`
- `Blueprint/contracts/study-differentiation-unit.schema.json`
- `Blueprint/contracts/learner-adaptation-unit.schema.json`
- `Blueprint/contracts/technical-teaching-unit-v3.schema.json`
- `Blueprint/policy/core-governance-cdau.v1.json`
- `Blueprint/policy/study-differentiation-unit.v1.json`
- `Blueprint/policy/learner-adaptation-unit.v1.json`
- `Blueprint/policy/technical-teaching-unit.v3.json`
- `Blueprint/tests/test_blueprint_cdau_sdu_lau_ttu_v7.py`

V7 preserves V6's reconstruction-complete TTU guarantees and broadens them into a governed cross-Core differentiation/adaptation system.