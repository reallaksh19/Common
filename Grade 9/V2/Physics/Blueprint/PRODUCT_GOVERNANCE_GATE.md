# Physics V2 — Product Governance & Release Gate Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Physics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Consolidates**: Product Governance, Release Criteria, and Publication Integrity for Physics.
> **Subject**: `PHYSICS` only.

---

## 1. Release Gate Questions

The Product Governance Gate operates after the Canonical Domain Registry and before deterministic Publication. It evaluates five non-negotiable release questions:

1. **Asset Completeness**: Did any validated physical concept, law, equation, derivation, free-body diagram, representation, misconception, problem family, source question, or verification asset disappear?
2. **Pedagogical Differentiation**: Did two Core products copy the same material without a declared cognitive transformation (`BUILD / RECONSTRUCT / CONTRAST / SOLUTION_ANATOMY / TRANSFER / VERIFY`)?
3. **Behavioral Observability**: Do difficulty badges (`EASY/MEDIUM/HARD`) and learning purpose labels produce observable product differences in physical rigor and representation rather than decorative metadata?
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
Core1A ↔ Core1B  │  Core1A ↔ Core2A  │  Core1A ↔ Core2B
Core1B ↔ Core2A  │  Core1B ↔ Core2B  │  Core2A ↔ Core2B
```

Each comparison measures:
- `content_similarity`: Lexical, mathematical, and physical model overlap.
- `pedagogical_similarity`: Instructional strategy and scaffolding alignment.
- `structural_similarity`: Physical scenario and constraint overlap.
- `capability_overlap`: Shared physical capability references.
- `lineage_relation`: Declared cognitive transformation.

Flagged comparisons above policy thresholds block release unless accompanied by an approved pedagogical variation rationale.

---

## 4. Anti-Gaming Controls & Publication Freeze Invariants

### Anti-Gaming Rules
1. **Page-Count Independence**: Page counts are ceilings, never depth targets. Adding filler paragraphs, spacer divs, or manual padding to meet page quotas triggers deterministic validation failure.
2. **Immutable Source Questions**: Frozen source questions must never be silently modified to adjust difficulty. Variants must declare new identities and provenance.
3. **No Decorative Research**: Web research briefs must substantiate explicit claims. Citing external URLs without bound physical claim coverage fails validation.
4. **Physics Invariant Preservation**: Downstream compilers must never drop essential physical boundary conditions (such as $W_{\text{nc}} = 0$ for mechanical energy conservation, or inertial frame requirements for Newton's second law $\sum \vec{F} = m\vec{a}$) to simplify an explanation.

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
| **Publication IR Compiler** | `engine/compile_publication_ir.py` | Compiles publication intermediate representation |
| **B-Layer Boundary Validator** | `engine/validate_b_layer_boundary.py` | Enforces A vs B layer non-duplication |
| **Governor Engine** | `engine/governor.py` | Policy and gate governor |
| **Independent Validation Engine** | `engine/independent_validation.py` | Autonomous release validation |
| **Golden Fixture Runner** | `engine/run_golden_fixtures.py` | Validates end-to-end golden pipelines |
| **Test Suites** | `tests/test_blueprint_publication_ir.py`, `tests/test_blueprint_b_layer_boundary.py` | Release gate test batteries |
