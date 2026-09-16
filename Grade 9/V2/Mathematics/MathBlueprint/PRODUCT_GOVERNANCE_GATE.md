# Mathematics V2 — Product Governance & Release Gate Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Mathematics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Consolidates**: `PRODUCT_GOVERNANCE.md`.
> **Subject**: `MATHEMATICS` only.

---

## 1. Release Gate Questions

The Product Governance Gate operates after the Canonical Domain Registry and before deterministic Publication. It evaluates five non-negotiable release questions:

1. **Asset Completeness**: Did any validated concept, equation, representation, misconception, problem family, source question, or verification asset disappear?
2. **Pedagogical Differentiation**: Did two Core products copy the same material without a declared cognitive transformation (`BUILD / RECONSTRUCT / CONTRAST / SOLUTION_ANATOMY / TRANSFER / VERIFY`)?
3. **Behavioral Observability**: Do difficulty badges (`EASY/MEDIUM/HARD`) and learning purpose labels produce observable product differences rather than decorative metadata?
4. **Custody & Calibration**: For Core2A/Core2B, does every learner-facing item fit the governed learner calibration and retain question/answer/source custody?
5. **Engineering Authority Integrity**: If Engineering Gate metadata is displayed, is that visibility derived from exact current custody without implying publication authorization?

---

## 2. Asset Coverage Ledger

Every asset admitted to the Canonical Domain Registry receives a disposition across Core1A, Core1B, Core2A, and Core2B:

```text
REALIZED | RECONSTRUCTED | REFERENCED | USED | PROHIBITED | NOT_APPLICABLE | INTENTIONALLY_OMITTED
```

### Coverage Invariants
1. **No Unseen Assets**: There is no legal unresolved, unseen, or missing state at release time.
2. **Core1 Presence**: Semantic registry assets (`CONCEPT / MODEL / EQUATION / DERIVATION / CAPABILITY / LEARNING_ATOM / REPRESENTATION / MISCONCEPTION`) must be accounted for in both Core1A and Core1B.
3. **Omission Transparency**: `INTENTIONALLY_OMITTED` requires an explicit owner override reference plus an explanatory rationale; the underlying asset remains in the registry.

---

## 3. Cross-Core Similarity Audit & Lineage

Duplication across cores is strictly prohibited unless explicitly governed. The similarity audit evaluates candidate comparisons across all six Core pairs:
```text
Core1A ↔ Core1B  |  Core1A ↔ Core2A  |  Core1A ↔ Core2B
Core1B ↔ Core2A  |  Core1B ↔ Core2B  |  Core2A ↔ Core2B
```

Each comparison measures:
- `content_similarity`: Lexical and mathematical overlap.
- `pedagogical_similarity`: Instructional strategy alignment.
- `structural_similarity`: Problem structure and constraint overlap.
- `capability_overlap`: Shared capability references.
- `lineage_relation`: Declared cognitive transformation.

Flagged comparisons above policy thresholds block release unless accompanied by an approved pedagogical variation rationale.

---

## 4. Anti-Gaming Controls & Publication Freeze Invariants

### Anti-Gaming Rules
1. **Page-Count Independence**: Page counts are ceilings, never depth targets. Adding filler paragraphs, spacer divs, or manual padding to meet page quotas triggers deterministic validation failure.
2. **Immutable Source Questions**: Frozen source questions must never be silently modified to adjust difficulty. Variants must declare new identities and provenance.
3. **No Decorative Research**: Web research briefs must substantiate explicit claims. Citing external URLs without bound claim coverage fails validation.

### Publication Freeze Criteria
Deterministic publication compilers must not be frozen until pedagogy goldens prove:
- `EASY`, `MEDIUM`, and `HARD` bucket behavior across Core1A/Core1B.
- Core2A/Core2B generation with a calibrated learner knowledge percentage or explicit Owner Waiver.
- Self-help closure with independent answer derivation and verification.
- Reconstructable TTU coverage and cognitive fading across all stages.
- Bounded and clipped representation viewports (`clip_to_viewport = true`).

---

## 5. Executable Contracts, Engines & Test Suites

| Component | Executable File | Purpose |
|---|---|---|
| **Coverage Ledger Schema** | `contracts/math-core-coverage-ledger.schema.json` | Cross-Core coverage contract |
| **Similarity Audit Schema** | `contracts/math-cross-core-similarity-audit.schema.json` | Six-pair similarity audit contract |
| **Product Governance Schema** | `contracts/math-product-governance-audit.schema.json` | Comprehensive release audit contract |
| **Product Governance Policy** | `policies/math-product-governance-policy.json` | Thresholds, ceilings, and weights |
| **Product Governance Validator** | `engine/validate_product_governance.py` | Complete release gate validator |
| **Test Suite** | `tests/test_product_governance.py` | Automated release gate test battery |
