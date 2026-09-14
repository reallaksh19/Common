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
technical engineering readiness boundary
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
        ↓
publication / learner runtime
        ↓
observed learner evidence
        ↓
       CAL
calibration / audit / versioned policy updates
```

Product-design layers never manufacture truth, rewrite frozen source wording, create observed learner evidence, or expand Core2A legality.

Publication remains separate:

```text
released governed semantics
        ↓
Publication IR
        ↓
composition-only renderer
        ↓
render custody / preflight
```

---

# Canonical learner-product architecture — V9

Normative architecture: `SELF_HELP_ARCHITECTURE_V9.md`.

V9 preserves all V8 CCU/CDAU/SDU/LAU/TTU guarantees and adds **CAL — Calibration & Audit Layer**. The key correction is that provisional similarity/difficulty/fit heuristics are explicitly distinguished from deterministic hard gates.

## Deterministic hard gates

The following do not require empirical calibration and may block immediately:

- missing applicable canonical-asset disposition;
- required asset with no realization;
- learner-facing released question with no canonical answer/resolution;
- frozen source question number changed;
- author/generated item impersonating source material;
- frozen source wording/custody violation;
- declared `PEDAGOGICAL_DUPLICATION`;
- exact adjacent numeric dataset reuse without declared `FADING_ANCHOR`;
- exact example fingerprint + equivalent learner usage without declared `FADING_ANCHOR`;
- Core2B fading anchor claimed as independent transfer evidence;
- learner-adaptive routing with neither usable learner evidence nor explicit owner override.

These are constitutional release invariants and are not relaxed by later calibration.

## Engineering heuristic gates

Lexical/structural similarity scores, authored difficulty mappings and pre-use learner-fit predictions are currently `ENGINEERING` maturity.

Current similarity values are triage thresholds:

- lexical 5-shingle Jaccard `>=0.65`: candidate signal;
- lexical `>=0.80`: review;
- lexical `>=0.90`: high review;
- structural fingerprint `>=0.70`: review;
- structural fingerprint `>=0.85`: high review.

**These do not auto-block solely because a score crosses the threshold.** At engineering maturity they create a review obligation. A review is either pending, adjudicated allow with reviewer provenance/reason, or adjudicated block.

A universal semantic-embedding cosine threshold is forbidden.

---

## CCU v2 — custody, coverage and calibrated anti-duplication boundary

Every canonical asset receives an explicit per-Core disposition:

`REQUIRED | OPTIONAL | TRANSFORMED | SOURCE_ONLY | NOT_APPLICABLE | PROHIBITED | HELD`

Blank disposition is illegal. Required assets need realization refs; transformed assets need lineage; held assets need blocking reasons.

Every learner-facing question/task carries a stable Question Custody Record with question/source identity, bucket/problem family/capabilities, canonical resolution, legal status, learner-visible source label, badges and fingerprint/lineage where applicable.

A released/design-pilot learner question may not have a held/missing answer. Frozen source numbering is immutable. Author-created/generated items may not impersonate source questions.

Similarity remains multi-signal:

`asset identity + structural fingerprint + lexical signal + semantic review signal + usage mode + learner action + solution path`.

Allowed relationships remain `SEMANTIC_REUSE`, `PEDAGOGICAL_TRANSFORMATION`, `FADING_ANCHOR`, `STRUCTURAL_SIBLING`, `FAR_TRANSFER_SIBLING`. `NEAR_DUPLICATE` requires review; `PEDAGOGICAL_DUPLICATION` blocks.

---

## CDAU v2 — Core purpose and differentiation

CDAU consumes CCU receipts and validates that content belongs in the intended Core and is genuinely differentiated from neighboring Cores.

- Core1 — compact orientation;
- Core1A — complete conceptual construction;
- Core1B — concept reconstruction;
- Core2 — frozen source question;
- Core2A — expert problem learning;
- Core2B — transfer and independent modelling.

Every substantive unit declares usage mode and learner action. Core1B fragile checkpoints require generative transformation. Core2B should prefer a fresh legal sibling when available; a fading anchor cannot count as transfer evidence.

Owner control remains global but bounded and records:

`SYSTEM_FINDING → OWNER_DECISION → FINAL_ACTION`

Owner control cannot override Physics/Mathematics correctness, frozen source wording, source-integrity classification, provenance, observed evidence, legal-pool custody, CCU receipts or authority order.

---

## SDU v2 — intrinsic difficulty for Core1A/Core1B

Student knowledge percentage may not drive authored Core1A/Core1B depth.

Difficulty uses the existing 0–3 engineering evidence profile across prerequisite depth, element interactivity, inferential-jump severity, representation translation, model discrimination, sign/frame sensitivity, multi-step dependency, abstraction, misconception density and synthesis.

The EASY/MEDIUM/HARD mapping remains an **authoring-governance heuristic**, not empirical item difficulty. It may govern research/depth now, but later expert calibration must remain distinct from learner-response-based empirical difficulty.

Both Core1A and Core1B share the soft maximum depth envelope Easy ~10 / Medium ~20 / Hard ~30 pages. These are ceilings, not quotas; actual lengths are independently derived.

---

## LAU v2 — learner-fit for Core2A/Core2B

Exactly one adaptation basis is required:

1. capability-specific `KNOWLEDGE_PERCENT` with provenance/confidence/evidence count/recency; or
2. explicit `OWNER_OVERRIDE` when usable knowledge evidence is unavailable.

No silent default.

Task demand is separate from learner state. Pre-use fit labels are routing predictions, not mastery claims:

`LIKELY_UNDERCHALLENGE | GOOD_FIT | PRODUCTIVE_STRETCH | LIKELY_OVERLOAD | BLOCKED_PREREQUISITE | OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED`.

Observed learner behavior updates/challenges the predicted fit; knowledge percentage alone is never mastery.

---

## TTU v3 — Concept TTU and Problem TTU

`CONCEPT_TTU → Core1A/Core1B`

`PROBLEM_TTU → Core2A/Core2B`

Every substantive TTU binds:

`semantic target → canonical expert state → technical representation → representation/relation bindings → reasoning-state graph → learner transformation → bounded help → canonical reveal → independent verification → repair`.

A diagram, equation, blank or hint alone does not constitute a TTU.

B-layer transformation modes include:

`PREDICTION | COMPLETION | GENERATION | SELECTION | DISCRIMINATION | DIAGNOSIS | DERIVATION_CONNECTION | VERIFICATION | TRANSFER`.

Full-solution exposure is learning support, not mastery or transfer evidence.

---

## CAL — Calibration & Audit Layer

CAL governs only non-deterministic policy maturity.

Maturity states:

`ENGINEERING | CALIBRATING | VALIDATED`.

A domain may not become `VALIDATED` merely by changing a label. Validation requires evidence refs, completed held-out evaluation, a versioned validated-policy reference and approval provenance.

Duplication calibration requires labelled Physics pairs covering all reuse/duplicate classes, boundary cases, independent reviewers, disagreement adjudication, agreement reporting, held-out evaluation and threshold-performance reporting.

Difficulty calibration keeps authored difficulty separate from empirical item difficulty. Learner-fit calibration retains prediction/outcome pairs from observed correctness, representation/model selection, first move, hint level, completion, explanation, verification and later retrieval.

CAL may update future versioned policy. It may not rewrite historical evidence, source truth, frozen source wording or legal-pool custody.

---

## Question badges

Required learner-facing badges for every released question:

`CORE | BUCKET | CONCEPT | SOURCE | ANSWER_STATUS`.

Conditional badges:

`DIFFICULTY | QUESTION_NUMBER | PROBLEM_FAMILY | LINKAGES | PREREQUISITES | LEARNER_ACTION | REPRESENTATION | TRANSFER_DISTANCE | MODEL_CONDITION | HINT_AVAILABILITY | EXAM_DEMAND`.

Source identity must always be visible. Internal knowledge %, confidence, digests, override state, similarity scores and calibration metadata remain internal by default.

---

## Release gates

Pre-release:

1. `G-DOMAIN` — source/semantic grounding valid;
2. `G-TECHNICAL-ENGINEERING` — applicable technical readiness gate closes where implemented;
3. `G-CUSTODY-COVERAGE` — CCU coverage, question custody, answer/source and duplication receipts close;
4. `G-PURPOSE` — learner action belongs in the Core;
5. `G-DIFFERENTIATION` — no accidental neighboring-Core duplication;
6. `G-TTU` — technical interaction complete;
7. `G-DIFFICULTY` — intrinsic difficulty/task demand evidenced;
8. `G-FIT` — Core2 support justified by knowledge evidence or explicit owner override;
9. `G-PUBLICATION` — rendered product legible, integrated and collision-free.

Post-use:

10. `G-CALIBRATION` — observed evidence updates/challenges future policy confidence/versioning; it never creates semantic/source authority retroactively.

---

## Normative V9 files

- `SELF_HELP_ARCHITECTURE_V9.md`
- `contracts/content-custody-coverage-unit.schema.json`
- `contracts/calibration-audit-state.schema.json`
- `policy/content-custody-coverage-unit.v2.json`
- `policy/calibration-audit-layer.v1.json`
- `policy/question-badge-metadata.v1.json`
- `policy/core-governance-cdau.v2.json`
- `policy/study-differentiation-unit.v2.json`
- `policy/learner-adaptation-unit.v2.json`
- `policy/technical-teaching-unit.v3.json`
- `calibration/physics-calibration-state.v1.json`
- `engine/validate_ccu_v2.py`
- `engine/validate_calibration_audit.py`
- `tests/test_blueprint_calibration_v9.py`

V2–V8 remain historical transition documents. **V9 is canonical for learner-product custody, differentiation, adaptation, technical realization and calibration maturity.**

---

## Artifact-generation rule

Learner artifacts must be regenerated from governed Blueprint state. The intended path is:

`source/domain → technical gate → CCU → CDAU → SDU/LAU → TTU → Publication IR → renderer → preflight`.

When an output defect is found, repair the first upstream logic/data object that permitted it, then regenerate. Direct artifact patching must not substitute for fixing product-generation logic.

---

## Visual publication gate

Successful PDF generation is not a visual pass. Production learner PDFs require flow layout or collision validation, legible labels/equations, meaningful figure area, representation-to-working adjacency, page-by-page render review and montage review for new figure grammars.

Fail closed on microscopic labels, oversized low-information figures, excessive unused plotting space, clipped content, text/figure collision, orphaned figures and unreadable equations.

---

## Real M2D publication boundary

Representation readiness may exist while publication remains independently blocked until repository-backed manuscript/source authority exists. Learner-product architecture, runtime activation, owner decisions and visual quality cannot substitute for missing source/manuscript release evidence.
