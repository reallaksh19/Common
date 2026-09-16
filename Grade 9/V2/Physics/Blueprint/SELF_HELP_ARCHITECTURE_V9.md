# Physics Self-Help Architecture V9 — CCU/CDAU/SDU/LAU/TTU + CAL

V9 supersedes V8 for learner-product governance. V8 remains the historical introduction of CCU. V9 adds an explicit **Calibration & Audit Layer (CAL)** and corrects one important boundary: provisional similarity/difficulty/fit heuristics are not validated scientific thresholds and may not silently become automatic hard gates.

## 0. Canonical flow

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
PHYSICS TECHNICAL ENGINEERING GATES
        ↓
       CCU
coverage • custody • source/answer traceability • anti-duplication
        ↓
       CDAU
purpose • cross-Core differentiation • bounded owner decisions
        ↓
   SDU or LAU
        ↓
CONCEPT_TTU or PROBLEM_TTU
        ↓
publication / learner runtime
        ↓
observed learner evidence
        ↓
       CAL
threshold calibration • difficulty calibration • learner-fit audit
        └──────────────→ versioned policy updates
```

CAL may update future policy versions. It may not rewrite source truth, historical evidence, legal-pool custody or already-observed learner events.

## 1. Deterministic gates versus engineering heuristics

Two classes of release logic are mandatory.

### Constitutional / deterministic hard gates

These require no empirical calibration and may block immediately:

- missing applicable canonical-asset disposition;
- `REQUIRED` asset without realization;
- released learner question without canonical answer/resolution;
- frozen source question number changed;
- author/generated item impersonating source material;
- frozen source wording/custody violation;
- declared `PEDAGOGICAL_DUPLICATION`;
- exact adjacent numeric dataset reuse without declared `FADING_ANCHOR`;
- exact example fingerprint + equivalent learner usage without declared `FADING_ANCHOR`;
- Core2B fading anchor claimed as independent transfer evidence;
- learner-adaptive routing with neither usable learner evidence nor explicit owner override.

These remain hard gates regardless of later calibration.

### Engineering heuristics

These are useful candidate/review signals but are not validated automatic verdicts:

- lexical n-gram/Jaccard similarity thresholds;
- weighted structural-fingerprint thresholds;
- embedding/semantic similarity;
- authored 0–3 difficulty profile → EASY/MEDIUM/HARD mapping;
- pre-use learner-fit predictions.

At maturity `ENGINEERING`, heuristic thresholds may produce `CANDIDATE`, `REVIEW`, or `HIGH_REVIEW`; they may not auto-block solely because a score crossed a provisional threshold.

## 2. CCU v2 similarity semantics

CCU still uses multiple signals:

`asset identity + example fingerprint + lexical similarity + semantic review signal + usage mode + learner action + solution path`.

Current engineering thresholds remain useful triage values:

- lexical 5-shingle Jaccard `>=0.65` candidate;
- lexical `>=0.80` review;
- lexical `>=0.90` high review;
- structural fingerprint `>=0.70` review;
- structural fingerprint `>=0.85` high review.

**They are review thresholds, not validated block thresholds.**

A review signal must either:

1. remain `PENDING`, forcing CCU `duplication_receipt = REVIEW`; or
2. be adjudicated `ADJUDICATED_ALLOW` with reviewer provenance/reason; or
3. be adjudicated `ADJUDICATED_BLOCK`, which blocks release.

No universal semantic-embedding cosine threshold is permitted.

## 3. CAL maturity states

Every non-deterministic decision family is labelled:

`ENGINEERING | CALIBRATING | VALIDATED`.

### ENGINEERING

Domain-informed rule. Suitable for warning/review/routing. Cannot claim empirical validation.

### CALIBRATING

Labelled/observed evidence exists and threshold/model performance is being estimated. Threshold changes remain versioned and reviewable.

### VALIDATED

Requires evidence refs, a completed held-out evaluation, a versioned validated-policy ref and approval provenance. Merely renaming an engineering rule as validated is release-invalid.

## 4. Duplication calibration

A Physics duplication calibration corpus should intentionally cover:

- semantic reuse;
- pedagogical transformation;
- fading anchors;
- structural siblings;
- far-transfer siblings;
- near duplicates;
- pedagogical duplicates.

Boundary cases are required; random easy pairs are insufficient.

Each pair should retain component scores rather than only one composite score. Independent reviewer labels and adjudication are required for disagreement. Before `VALIDATED`, a held-out evaluation must report at least precision, recall and false-block behaviour, plus threshold-selection rationale.

Similarity alone never overrides declared source/custody invariants.

## 5. Difficulty calibration

SDU difficulty remains an intrinsic authoring-governance profile, not empirical item difficulty.

The 0–3 dimensions remain useful:

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

At `ENGINEERING`, the mapping to EASY/MEDIUM/HARD governs research/depth and prompts review. Later expert calibration requires multiple independent ratings, dimension-level ratings, overall labels, adjudication and held-out cases.

Empirical item difficulty is a separate downstream construct and requires observed learner response data. Authored difficulty and empirical difficulty must never be silently merged.

## 6. Learner-fit calibration

LAU pre-use outputs remain routing predictions:

`LIKELY_UNDERCHALLENGE | GOOD_FIT | PRODUCTIVE_STRETCH | LIKELY_OVERLOAD | BLOCKED_PREREQUISITE | OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED`.

CAL compares predictions with observed:

- correctness;
- representation correctness;
- model selection;
- first move;
- hint level;
- completion;
- explanation;
- verification;
- later retrieval.

Prediction/outcome pairs are retained for calibration. A knowledge percentage is not mastery by itself. Automatic error hypotheses are not diagnoses. No universal mastery cutoff is permitted without explicit validated policy.

## 7. Technical Engineering Gates remain upstream

Physics Technical Engineering Gates answer what a technically coherent subtopic must contain before downstream products may claim technical completeness. Their maturity is `ENGINEERING` unless later calibrated/validated under an explicit subject-specific process.

A product cannot bypass an applicable technical gate merely because TTU/CCU/CDAU are otherwise complete.

## 8. Release gates

Pre-release:

1. `G-DOMAIN`;
2. `G-TECHNICAL-ENGINEERING`;
3. `G-CUSTODY-COVERAGE`;
4. `G-PURPOSE`;
5. `G-DIFFERENTIATION`;
6. `G-TTU`;
7. `G-DIFFICULTY`;
8. `G-FIT` where applicable;
9. `G-PUBLICATION`.

Post-use:

10. `G-CALIBRATION` updates future policy confidence/versioning only.

## 9. Normative V9 files

- `policy/content-custody-coverage-unit.v2.json`
- `policy/calibration-audit-layer.v1.json`
- `contracts/calibration-audit-state.schema.json`
- `calibration/physics-calibration-state.v1.json`
- `engine/validate_ccu_v2.py`
- `engine/validate_calibration_audit.py`
- `tests/test_blueprint_calibration_v9.py`

All V8 custody/source/answer guarantees remain in force. V9 changes only the maturity semantics of non-deterministic heuristic gates and introduces explicit calibration governance.
