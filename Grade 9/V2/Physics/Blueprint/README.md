# Physics V2 Blueprint — evidence-adaptive orchestration

`Grade 9/V2/Physics/Blueprint/` is the canonical orchestration root. Role-specific sibling directories are subordinate execution kits. Execution order may vary; **authority order may not**.

## Authority topology

```text
ORIGINAL / OBSERVED GROUND TRUTH
        ↓
      CORE0
        ↓
CORE1 ↔ independent second pass ↔ CORE2
        ↓
       JOIN
        ↓
CANONICAL DOMAIN REGISTRY
        ↓
       CCU
coverage / custody / source-answer traceability / anti-duplication
        ↓
       CDAU
purpose / differentiation / bounded owner decisions
        ↓
   ┌────┴────┐
   ↓         ↓
  SDU       LAU
Core1       Core2
track       track
   ↓         ↓
CONCEPT    PROBLEM
  TTU        TTU
 /   \      /   \
1A   1B    2A   2B
```

Product-design layers never manufacture truth, rewrite frozen source wording, create observed learner evidence, or expand Core2A legality.

Publication remains separate:

```text
released Core1A semantics
        ↓
Publication IR
        ↓
composition-only renderer
        ↓
render custody / preflight
```

---

# Physics Technical Engineering Gate Registry (Upstream of Authored TTUs)

Normative specification: `PHYSICS_TECHNICAL_ENGINEERING_GATES.md`.  
Schema contract: `contracts/physics-technical-engineering-gate.schema.json`.  
Canonical policy & registry: `policy/physics-technical-engineering-gates.v1.json`.  
Deterministic validator: `engine/validate_engineering_gates.py`.  
Test suite & falsifiers: `tests/test_physics_engineering_gates.py`.

At the **CANONICAL DOMAIN REGISTRY** boundary (upstream of CCU, CDAU, and authored TTUs), technical readiness requires fail-closed engineering validation. A physics subtopic cannot pass technical readiness without satisfying its 16-point technical gate structure:
- **Technical Core**: Canonical statements, explicit reasons required, exact failure modes if omitted.
- **Mandatory Equations**: Every symbol defined with units, conditions of validity, and obligations (`EXPLAIN`, `DERIVE`, `INTERPRET`, `REPRESENT`, `APPLY`, `INVERT`, `VERIFY`).
- **Canonical Representations**: Geometry, axes, vectors, FBDs; declared mandatory labels, what cannot be omitted, and common incorrect versions.
- **Model Applicability & Boundary Conditions**: Validity envelope, breakdown points, asymptotic behaviors, limiting cases.
- **Reasoning Sequence**: Ordered derivation/concept flow with zero inferential jumps or hand-waving.
- **Transformations & Learning Actions**: Explicit mapping across Core1A, Core1B, Core2A, and Core2B.
- **Misconceptions & Traps**: Canonical errors, why intuitive, discrimination tasks, and refutation demonstrations.
- **Mandatory Verifications**: Dimensional analysis, limiting cases, directional/sign checks, conservation constraints, order-of-magnitude estimates.
- **Canonical Problem Families**: Identification, standard solution template, variation axes, common traps.
- **Difficulty Profile**: 10-dimension engineering scale (0–3), `maturity: ENGINEERING` (strictly zero psychometric overclaim).
- **Release Checklist**: 100% complete across all 10 criteria before marked `ENGINEERING_GATE_READY`.
- **Falsification Battery**: Traps prompt-mandated omission defects (vector sign/direction omission, resultant reconstruction omission, scalar blur, NLM without FBD, third-law pair conflation on one body, automatic $N=mg$ assumption, blind static friction thresholding, Atwood tension fallacy, cross-topic clock desynchronization, dissipative energy conservation omission).

---

# Canonical learner-product architecture — V8

Normative architecture: `SELF_HELP_ARCHITECTURE_V8.md`.

V8 preserves V7's CDAU/SDU/LAU/TTU architecture and adds **CCU — Content Custody & Coverage Unit**.

## CCU — custody, coverage, question traceability

CCU prevents silent omission and silent copying before CDAU sees the product.

Every canonical asset receives an explicit per-Core disposition:

`REQUIRED | OPTIONAL | TRANSFORMED | SOURCE_ONLY | NOT_APPLICABLE | PROHIBITED | HELD`

Blank disposition is illegal. Required assets need realization refs; transformed assets need lineage; held assets need blocking reasons.

Every learner-facing question/task carries a stable Question Custody Record with:

- question ID and displayed number;
- source class and visible source label;
- original source question number where applicable;
- bucket/problem family/capabilities;
- canonical answer/solution/diagram/derivation/rubric;
- legal status;
- badges;
- fingerprint and lineage when applicable.

A released/design-pilot learner question may not have a held/missing answer. Frozen source numbering is immutable. Author-created/generated items may not impersonate official/source questions.

### Similarity and anti-duplication

Similarity is multi-signal, never one score:

- asset identity;
- structural example fingerprint;
- lexical 5-shingle Jaccard;
- semantic similarity as a calibrated review signal;
- usage mode;
- learner action;
- solution path.

Initial deterministic thresholds:

- lexical Jaccard `>=0.90`: high duplicate risk;
- lexical Jaccard `>=0.80`: review;
- structural score `>=0.85` with equivalent pedagogical usage: block unless explicit fading anchor;
- structural score `>=0.70`: review.

A universal semantic cosine threshold is deliberately forbidden; semantic thresholds must be calibrated on labelled Physics pairs.

Allowed relationships: `SEMANTIC_REUSE`, `PEDAGOGICAL_TRANSFORMATION`, `FADING_ANCHOR`, `STRUCTURAL_SIBLING`, `FAR_TRANSFER_SIBLING`. `NEAR_DUPLICATE` requires review; `PEDAGOGICAL_DUPLICATION` blocks release.

---

## CDAU v2 — Core purpose and differentiation

CDAU now consumes CCU receipts. It validates that content belongs in the intended Core and is genuinely differentiated from neighboring Cores.

- Core1 — compact orientation;
- Core1A — complete conceptual construction;
- Core1B — concept reconstruction;
- Core2 — frozen source question;
- Core2A — expert problem learning;
- Core2B — transfer and independent modelling.

Every substantive unit declares usage mode and learner action. Core1B fragile checkpoints require generative transformation. Core2B must prefer a fresh legal sibling when available; a fading anchor cannot count as transfer evidence.

Owner control remains global but bounded and records:

`SYSTEM_FINDING → OWNER_DECISION → FINAL_ACTION`

Owner control cannot override Physics/Mathematics correctness, frozen source wording, source-integrity classification, provenance, observed evidence, legal-pool custody, CCU receipts or authority order.

---

## SDU v2 — intrinsic difficulty for Core1A/Core1B

Student knowledge percentage may not drive authored Core1A/Core1B depth.

Difficulty uses an evidence profile on a 0–3 engineering scale:

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

Derived design rules:

- Hard: at least two score-3 dimensions, or a declared critical bottleneck controlling the capability, or synthesis 3 with multi-step dependency >=2;
- Medium: not Hard and at least one dimension score 2/3;
- Easy: no dimension above 1 and no critical bottleneck.

These are governance heuristics, not psychometric claims. Owner/source-supplied badges remain authoritative but disagreement must be recorded.

Both Core1A and Core1B share the soft maximum depth envelope Easy ~10 / Medium ~20 / Hard ~30 pages. These are ceilings, not quotas; actual lengths are independently derived.

---

## LAU v2 — learner-fit for Core2A/Core2B

Exactly one adaptation basis is required:

1. capability-specific `KNOWLEDGE_PERCENT` with provenance/confidence/evidence count/recency; or
2. explicit `OWNER_OVERRIDE` when usable knowledge evidence is unavailable.

No silent default.

Learner subdimensions may include recognition, representation, model selection, first move, execution, explanation and verification.

Task demand is separately recorded on 0–3 dimensions: structural distance, representation change, model discrimination, sign/direction reversal, reversed target, constraint inversion, multi-step bridge, synthesis, competitive mixing and calculation load.

Pre-use fit labels are routing predictions, not mastery claims:

`LIKELY_UNDERCHALLENGE | GOOD_FIT | PRODUCTIVE_STRETCH | LIKELY_OVERLOAD | BLOCKED_PREREQUISITE | OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED`

For the same task, lower knowledge should not receive less support than higher knowledge without explicit owner reason.

Observed learner behavior after use updates/challenges the predicted fit; knowledge percentage alone is never mastery.

---

## TTU v3 — Concept TTU and Problem TTU

`CONCEPT_TTU → Core1A/Core1B`

`PROBLEM_TTU → Core2A/Core2B`

Every substantive TTU binds:

`semantic target → canonical expert state → technical representation → representation/relation bindings → reasoning-state graph → learner transformation → bounded help → canonical reveal → independent verification → repair`

A diagram, equation, blank or hint alone does not constitute a TTU.

B-layer transformation modes include:

`PREDICTION | COMPLETION | GENERATION | SELECTION | DISCRIMINATION | DIAGNOSIS | DERIVATION_CONNECTION | VERIFICATION | TRANSFER`

Full-solution exposure is learning support, not mastery or transfer evidence.

---

## Question badges

Required learner-facing badges for every released question:

`CORE | BUCKET | CONCEPT | SOURCE | ANSWER_STATUS`

Conditional badges:

`DIFFICULTY | QUESTION_NUMBER | PROBLEM_FAMILY | LINKAGES | PREREQUISITES | LEARNER_ACTION | REPRESENTATION | TRANSFER_DISTANCE | MODEL_CONDITION | HINT_AVAILABILITY | EXAM_DEMAND`

Source identity must always be visible. Internal knowledge %, confidence, digests, override state, similarity scores and calibration metadata remain internal by default.

---

## Release gates

Pre-release:

1. `G-DOMAIN` — source/semantic grounding valid;
2. `G-CUSTODY-COVERAGE` — CCU coverage, question custody, answer/source and duplication receipts close;
3. `G-PURPOSE` — learner action belongs in the Core;
4. `G-DIFFERENTIATION` — no accidental neighboring-Core duplication;
5. `G-TTU` — technical interaction complete;
6. `G-DIFFICULTY` — intrinsic difficulty/task demand evidenced;
7. `G-FIT` — Core2 support justified by knowledge evidence or explicit owner override;
8. `G-PUBLICATION` — rendered product legible, integrated and collision-free.

Post-use:

9. `G-CALIBRATION` — observed behavior updates/challenges predicted fit; it never creates semantic/source authority retroactively.

---

## Normative V8 files

- `SELF_HELP_ARCHITECTURE_V8.md`
- `contracts/content-custody-coverage-unit.schema.json`
- `policy/content-custody-coverage-unit.v1.json`
- `policy/question-badge-metadata.v1.json`
- `policy/core-governance-cdau.v2.json`
- `policy/study-differentiation-unit.v2.json`
- `policy/learner-adaptation-unit.v2.json`
- `policy/technical-teaching-unit.v3.json`
- `engine/validate_ccu.py`
- `topics/m2d-sba23-ccu.v1.json`
- `topics/m2d-sba23-v8-realization-plan.json`
- `tests/test_blueprint_ccu_v8.py`

V2–V7 remain historical transition documents. **V8 is canonical for learner-product custody, differentiation, adaptation and technical realization.**

---

## Visual publication gate

Successful PDF generation is not a visual pass. Production learner PDFs require flow layout or collision validation, legible labels/equations, meaningful figure area, representation-to-working adjacency, page-by-page render review and montage review for new figure grammars.

Fail closed on microscopic labels, oversized low-information figures, excessive unused plotting space, clipped content, text/figure collision, orphaned figures and unreadable equations.

---

## Real M2D publication boundary

Representation readiness may exist while publication remains independently blocked until repository-backed manuscript/source authority exists. Learner-product architecture, runtime activation, owner decisions and visual quality cannot substitute for missing source/manuscript release evidence.
