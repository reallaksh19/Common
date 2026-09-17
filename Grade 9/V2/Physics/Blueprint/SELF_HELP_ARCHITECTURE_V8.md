# Physics Self-Help Architecture V8 — CCU + CDAU / SDU / LAU + TTU

V8 supersedes V7 for learner-product governance. V7 remains historical architecture for CDAU/SDU/LAU/TTU. V8 adds an explicit **Content Custody & Coverage Unit (CCU)** so an agent cannot silently omit required domain assets, lose question/source identity, publish a question without a canonical resolution, or duplicate an adjacent Core under superficial wording changes.

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
observed learner evidence / calibration
```

None of CCU/CDAU/SDU/LAU/TTU may create truth, rewrite frozen source wording, manufacture observed learner evidence, or expand legal transfer custody.

## 1. CCU — Content Custody & Coverage Unit

CCU answers five release questions before CDAU:

1. **Coverage:** did every canonical concept/equation/representation/misconception/problem-family/source item receive an explicit disposition?
2. **Custody:** can every learner-facing question be traced to its source class and lineage?
3. **Resolution:** does every released learner-facing question have a canonical answer/solution/diagram/derivation/rubric?
4. **Duplication:** is cross-Core reuse legitimate semantic reuse/transformation rather than pedagogical copying?
5. **Source visibility:** does the learner see whether an item is frozen source, owner-supplied, author-created or generated?

### Coverage matrix

Every registered asset declares applicable Cores. Each applicable Core must receive exactly one disposition:

`REQUIRED | OPTIONAL | TRANSFORMED | SOURCE_ONLY | NOT_APPLICABLE | PROHIBITED | HELD`

Blank disposition is illegal.

- `REQUIRED` requires a realization reference.
- `TRANSFORMED` requires parent asset + transformation reference.
- `HELD` requires a blocking reason.
- `PROHIBITED` may not carry a realization.

Release requires zero unexplained omissions.

## 2. Question Custody Record

Every question/task shown to a learner receives a stable record containing:

- question ID;
- displayed question number;
- Core;
- source class;
- source reference and original source question number where applicable;
- bucket and problem family;
- capability IDs;
- answer/resolution object;
- legal/release status;
- visible source label;
- badges;
- example fingerprint and lineage when applicable.

Source classes:

`FROZEN_SOURCE | OWNER_SUPPLIED | AUTHOR_CREATED | GENERATED_LEGAL_SIBLING | AUTHOR_CREATED_DESIGN_PILOT`

A released question may not have `answer_status = HELD`. If its canonical resolution cannot be established, question release is blocked.

Frozen source numbering is immutable: if the source item is Q15, the learner-facing source identity remains Q15.

## 3. Answers are mandatory

Every learner-facing question resolves to one of:

`SOURCE_ANSWER | CANONICAL_ANSWER | CANONICAL_SOLUTION | CANONICAL_DERIVATION | CANONICAL_DIAGRAM | CANONICAL_RUBRIC`

Examples:

- numerical problem → answer + working;
- derivation → canonical derivation;
- drawing → canonical completed diagram;
- explanation → model response / required ideas;
- diagnosis → exact error + corrected reasoning;
- model selection → correct model + rejection reason.

`HELD` is permitted only for an unreleased/blocked source item.

## 4. Duplication is multi-signal, not one similarity score

Fundamental equations may legitimately recur. Duplication is judged from:

- canonical asset identity;
- example structural fingerprint;
- lexical 5-shingle similarity;
- semantic similarity as a calibrated review signal;
- usage mode;
- learner action;
- solution path.

### Initial deterministic thresholds

Lexical 5-shingle Jaccard:

- `>= 0.90` high duplicate risk;
- `>= 0.80` review;
- `>= 0.65` candidate signal only.

Lexical similarity alone never hard-blocks.

Structural fingerprint weights:

- problem family 20%;
- target unknown 15%;
- model sequence 15%;
- solution path 15%;
- givens 10%;
- numeric values 10%;
- representation 10%;
- context 3%;
- special condition 2%.

If structural similarity is `>= 0.85` **and pedagogical usage is the same/equivalent**, release blocks unless the relationship is an explicit `FADING_ANCHOR`. `0.70–0.85` requires review.

These are engineering starting thresholds, not psychometric constants. They must be calibrated against a manually labelled Physics question-pair corpus.

A universal semantic-embedding cosine threshold is forbidden. Semantic similarity remains `CALIBRATED_ON_LABELLED_PHYSICS_PAIRS` before becoming a hard gate.

## 5. Allowed cross-Core relationships

`SEMANTIC_REUSE` — same law/definition, legitimate changed use.

`PEDAGOGICAL_TRANSFORMATION` — same domain asset transformed for another learner action.

`FADING_ANCHOR` — intentional same item with support faded; never independent transfer evidence.

`STRUCTURAL_SIBLING` — same family, meaningfully changed instance.

`FAR_TRANSFER_SIBLING` — changed representation/target/constraint/synthesis.

`NEAR_DUPLICATE` — review required.

`PEDAGOGICAL_DUPLICATION` — release blocked.

Adjacent A/B defaults are stricter: same exact numeric example or same complete diagram is prohibited unless explicitly transformed/fading-anchored.

## 6. CDAU v2 — Core purpose and differentiation

CDAU now consumes CCU receipts before product differentiation.

Purpose remains:

- Core1 — compact orientation;
- Core1A — complete conceptual construction;
- Core1B — concept reconstruction;
- Core2 — frozen source question;
- Core2A — expert problem learning;
- Core2B — transfer and independent modelling.

Every substantive unit declares usage mode and learner action. Core1B fragile checkpoints require generative transformation; passive reference-only treatment is not sufficient. Core2B must use a fresh sibling when a legal sibling exists; a fading anchor cannot count as transfer evidence.

## 7. SDU v2 — Difficulty validation

Core1A/Core1B authored depth remains independent of learner knowledge percentage.

Difficulty evidence dimensions use a 0–3 engineering scale:

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

Derived classification rules:

- **Hard** if at least two dimensions score 3, or one declared critical bottleneck controls the capability, or synthesis is 3 with multi-step dependency >=2;
- **Medium** if not Hard and at least one dimension scores 2/3;
- **Easy** if no dimension exceeds 1 and no critical bottleneck exists.

These rules are design-governance heuristics, not psychometric claims. Supplied owner/source difficulty remains authoritative but disagreement is recorded rather than silently overwritten.

Both 1A/1B retain the same soft maximum depth envelope: Easy ~10, Medium ~20, Hard ~30, with independently derived actual lengths.

## 8. LAU v2 — Learner-fit validation

Core2A/Core2B require exactly one selection basis:

- capability-specific `KNOWLEDGE_PERCENT`; or
- explicit `OWNER_OVERRIDE` when usable evidence is unavailable.

No silent default.

Learner state records scope, provenance, confidence, evidence count, recency and subdimensions: recognition, representation, model selection, first move, execution, explanation, verification.

Task demand uses 0–3 dimensions: structural distance, representation change, model discrimination, sign/direction reversal, reversed target, constraint inversion, multi-step bridge, synthesis, competitive mixing and calculation load.

Pre-use fit labels:

`LIKELY_UNDERCHALLENGE | GOOD_FIT | PRODUCTIVE_STRETCH | LIKELY_OVERLOAD | BLOCKED_PREREQUISITE | OWNER_ROUTED_NOT_KNOWLEDGE_VALIDATED`

These are routing predictions, not mastery/psychometric claims.

A monotonic guard applies: for the same task, lower knowledge should not receive less support than higher knowledge without explicit owner reason.

Post-use observables update the learner model from actual correctness, representation/model selection, first move, hint level, explanation, verification and later retrieval.

## 9. TTU v3 remains the technical interaction contract

`CONCEPT_TTU` serves Core1A/Core1B; `PROBLEM_TTU` serves Core2A/Core2B.

A TTU requires canonical expert state, meaningful representation/relation bindings, reasoning-state graph, learner transformation, bounded help, canonical reveal, independent verification and repair.

A diagram, equation, blank or hint alone never satisfies TTU.

## 10. Badge metadata

Required learner-facing badges for every released question:

`CORE | BUCKET | CONCEPT | SOURCE | ANSWER_STATUS`

Conditional badges include:

`DIFFICULTY | QUESTION_NUMBER | PROBLEM_FAMILY | LINKAGES | PREREQUISITES | LEARNER_ACTION | REPRESENTATION | TRANSFER_DISTANCE | MODEL_CONDITION | HINT_AVAILABILITY | EXAM_DEMAND`

Source identity is always learner-visible. Author-created/generated questions may never visually impersonate frozen source questions.

Internal-only metadata includes knowledge percentage/confidence, authority/legal-pool digests, owner override, source-integrity internal state, duplication/similarity scores, calibration state and evidence basis.

## 11. Release gates

Pre-release:

1. `G-DOMAIN` — semantic/source grounding valid;
2. `G-CUSTODY-COVERAGE` — CCU coverage, custody, resolution and duplication receipts close;
3. `G-PURPOSE` — learner action belongs in the Core;
4. `G-DIFFERENTIATION` — no accidental neighboring-Core duplication;
5. `G-TTU` — technical interaction complete;
6. `G-DIFFICULTY` — difficulty/task demand evidenced;
7. `G-FIT` — Core2 support justified by learner evidence or explicit owner override;
8. `G-PUBLICATION` — rendered product legible and collision-free.

Post-use:

9. `G-CALIBRATION` — observed learner behavior updates/challenges predicted fit.

## 12. Canonical V8 invariants

- Every applicable canonical asset has an explicit Core disposition; omission by silence is impossible.
- Every learner-facing released/design-pilot question has source identity and canonical resolution.
- Frozen source question numbers are retained exactly.
- Fundamental equations may repeat; examples/data/representations may not silently duplicate across adjacent Cores.
- Similarity is multi-signal; one lexical or embedding score cannot decide duplication alone.
- Core1 difficulty is intrinsic, not knowledge-percent driven.
- Core2 fit requires learner knowledge evidence or explicit owner override.
- Owner override cannot rewrite truth, source custody, evidence or legal-pool boundaries.
- Full-solution exposure is learning support, not mastery/transfer evidence.

## 13. Normative V8 files

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

V2–V7 remain historical transition documents. V8 is canonical for learner-product custody, differentiation, adaptation and technical realization.
