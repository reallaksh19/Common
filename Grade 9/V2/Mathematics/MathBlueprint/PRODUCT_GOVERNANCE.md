# Mathematics V2 — Product Governance Gate

This contract sits after the Canonical Domain Registry and before deterministic Publication.

It answers four release questions:

1. Did any validated concept, equation, representation, misconception, problem family, source question or verification asset disappear?
2. Did two Core products copy the same material without a declared pedagogical transformation?
3. Do difficulty badges and Core-purpose labels produce observable product behavior rather than decorative metadata?
4. For Core2A/Core2B, does every learner-facing item fit the governed learner calibration and retain question/answer/source custody?

## 1. Coverage ledger

Every asset admitted to the Canonical Domain Registry receives a disposition in Core1A, Core1B, Core2A and Core2B.

Legal dispositions are:

```text
REALIZED
RECONSTRUCTED
REFERENCED
USED
PROHIBITED
NOT_APPLICABLE
INTENTIONALLY_OMITTED
```

There is no legal unresolved/unseen state at release.

A required asset may not be `NOT_APPLICABLE` or `PROHIBITED`. `INTENTIONALLY_OMITTED` requires an explicit owner override plus a reason; the underlying system finding remains unchanged.

Semantic registry assets (`CONCEPT / MODEL / EQUATION / DERIVATION / CAPABILITY / LEARNING_ATOM / REPRESENTATION / MISCONCEPTION`) must remain represented in both Core1A and Core1B. Their treatment may differ; their mathematical depth may not silently disappear.

## 2. Similarity and lineage

Similarity is not a single text score.

Each cross-Core candidate comparison records:

```text
content_similarity
pedagogical_similarity
structural_similarity (for examples/questions where applicable)
capability_overlap
declared lineage relation
```

The audit must declare `ALL_CROSS_CORE_CANDIDATES`, zero uncompared candidates, and coverage of all six stage pairs:

```text
Core1A ↔ Core1B
Core1A ↔ Core2A
Core1A ↔ Core2B
Core1B ↔ Core2A
Core1B ↔ Core2B
Core2A ↔ Core2B
```

Initial thresholds are policy values, not universal research claims:

```text
content >= 0.90                     hard-duplicate candidate
content >= 0.75                     near-duplicate candidate
pedagogy >= 0.80                    same-realization candidate
pedagogy >= 0.60                    strong-overlap candidate
structural >= 0.90                  same/near-copy problem
0.70 <= structural < 0.90           structural sibling
0.40 <= structural < 0.70           far-transfer sibling
structural < 0.40                    family-drift review
```

Canonical equations and frozen source stems may repeat exactly only with explicit lineage. Exact mathematics is not penalized for being exact; copying the surrounding pedagogy is.

Legal lineage relations:

```text
SEMANTIC_REUSE
CANONICAL_REPEAT
FADING_ANCHOR
STRUCTURAL_SIBLING
FAR_TRANSFER_SIBLING
```

`FADING_ANCHOR` may reuse the same question intentionally but does not count as transfer evidence.

## 3. Difficulty governance

Core1A/Core1B use intrinsic subtopic difficulty only.

A difficulty audit records both:

```text
DECLARED / OPERATIONAL BADGE
DERIVED DIFFICULTY PROFILE
```

The derived profile uses 0..4 dimensions:

```text
prerequisite depth
element interactivity
inferential-jump severity
representation translation
abstraction
method discrimination
notation density
derivation burden
misconception density
special-case sensitivity
```

The initial policy normalizes the ten dimensions to 0..100 and maps:

```text
0..32   EASY
33..65  MEDIUM
66..100 HARD
```

These are owner-calibratable policy thresholds, not claims about universal educational constants.

Operational consequences are mandatory:

```text
EASY   -> <=10-page ceiling, no pedagogy-enrichment web research
MEDIUM -> <=20-page ceiling, TARGETED research
HARD   -> <=30-page ceiling, DEEP research
```

If owner/source authority overrides the derived badge, both findings remain visible. The operational badge controls production; the derived profile remains in the audit.

## 4. Core-purpose validation

Core labels are validated through learner actions, not headings.

```text
Core1A  BUILD_UNDERSTANDING
Core1B  RECONSTRUCT_CONCEPT
Core2A  SOLUTION_APPRENTICESHIP
Core2B  TRANSFER_TUTOR
```

Core1B must contain at least two meaningful reconstruction actions such as prediction, generation, selection, discrimination, diagnosis, derivation, connection, verification or transfer, and canonical reveal follows an attempt.

Core2A must expose expert solution anatomy including first-move analysis and verification.

Core2B requires an attempt, model/method selection, a first move and verification before canonical reveal.

## 5. Learner-fit validation

Learner fit applies only to Core2A/Core2B.

Every item must bind exactly one legal calibration basis:

```text
KNOWLEDGE_PERCENT + source + named policy + capability-specific knowledge
OR
OWNER_OVERRIDE + owner reference + reason
```

The validator fails when:

```text
actual demand > maximum allowed demand
required capability is not in the Canonical Domain Registry
capability-specific knowledge is missing on the percentage path
item requires untaught scope
```

The percentage is a generation-calibration input, not a mastery declaration.

## 6. Question custody

Every supplied source question keeps its permanent identity and remains present in the custody ledger even when a derivative product does not select it for display.

For a source question the audit requires:

```text
source question number
source reference
EXACT_SOURCE relation
frozen stem hash
verified AnswerContract
learner-facing source label
```

Generated questions receive new identities. They may reference source parents through `FADING_ANCHOR / STRUCTURAL_SIBLING / FAR_TRANSFER_SIBLING`, but may never inherit the source question number or masquerade as source.

Every learner-facing question requires a verified answer contract and a learner-visible source/origin label.

## 7. Badge taxonomy

Learner-facing badges are intentionally smaller than the machine metadata set.

Recommended learner-facing badges:

```text
Difficulty
Concept
Linkage
Bucket/Subtopic
Problem family
Source
Support (Core2A/Core2B where useful)
```

Machine/audit metadata additionally tracks:

```text
Capability
Prerequisite
Equation
Representation
Misconception
Demand level
Core role
Learner action
Transfer lineage
Answer status
Verification method
Novelty/similarity class
Validity/scope
Evidence confidence
Research level
Lifecycle
Owner override
```

Badge references must resolve to correctly typed Canonical Domain Registry assets.

## 8. Release command

The executable gate is:

```bash
python Grade\ 9/V2/Mathematics/MathBlueprint/engine/validate_product_governance.py \
  --registry <canonical-domain-registry.json> \
  --coverage <core-coverage-ledger.json> \
  --similarity <cross-core-similarity-audit.json> \
  --governance <product-governance-audit.json>
```

Publication must fail closed when any of these audits fail.
