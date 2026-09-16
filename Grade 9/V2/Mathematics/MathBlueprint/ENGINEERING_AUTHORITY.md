# Mathematics V2 — Engineering Authority & Workbench Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Mathematics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Consolidates**: `ENGINEERING_GATE_BLUEPRINT_AUTHORITY.md`, `ENGINEERING_WORKBENCH.md`, and `ENGINEERING_DISCOVERY.md`.
> **Subject**: `MATHEMATICS` only.

---

## 1. Upstream Engineering Authority Direction

Engineering is upstream technical authority for Mathematics. MathBlueprint does not invent, remember, or mutate mathematical definitions, formulas, or preconditions. Blueprint consumes Engineering authority exclusively through exact, digest-bound identities, generic policy evaluation, and deterministic prerequisite closure.

```text
NATURAL-LANGUAGE QUERY / SEARCH / ALIAS / HINT / EXTERNAL RESEARCH
        |
        | [1] Non-authoritative candidate discovery only
        v
RANKED ENGINEERING CANDIDATES (Authority: CANDIDATE_DISCOVERY_ONLY)
        |
        | [2] Explicit exact-ID selection required (Technical Auth: NOT_EVALUATED)
        v
DIRECT ENGINEERING GATE IDENTIFIERS (e.g. MATH-QUAD-EQUATIONS)
        ^
        | [3] Validated against Canonical Registry & Depth Policy
        v
CANONICAL MATHEMATICS ENGINEERING REGISTRY (REG-MATH-TECH-GATE-V1)
        |
        | [4] Transitive Prerequisite Closure (<= 3 direct scope refs)
        v
ENGINEERING CLOSURE RECEIPT (Deterministic SHA-256 Digest)
        |
        | [5] Exact Custody Binding (Subtopic -> Gate)
        v
CANONICAL DOMAIN ADMISSION (CDAU)
        |
        | [6] Equal Custody Revalidation
        v
SDU (Core1A / Core1B) & LAU (Core2A / Core2B)
        |
        v
DERIVED ENGINEERING VISIBILITY (Publication Auth: NOT_IMPLIED)
```

### Governing Authority Invariants

1. **Direction of Authority**:
   ```text
   Engineering Registry → Closure Receipt → Domain Admission → Core Realization → Publication
   ```
   No downstream layer (SDU, LAU, TTU authoring, or renderer) may alter an Engineering precondition, omit an invariant, or fabricate an Engineering identity.
2. **Subject Isolation**:
   Every request, manifest, receipt, and binding must declare `subject = MATHEMATICS`. Physics or cross-subject artifacts fail closed.
3. **Execution vs Authority Invariant**:
   *Execution order may vary; authority order may never vary.*

---

## 2. Non-Authoritative Discovery Boundary

The discovery layer provides a flexible, natural-language on-ramp for learners, authors, and AI agents while strictly preventing unverified queries from creating technical authority.

> **The Golden Boundary Rule**: *Discovery may be permissive. Authority may not be.*

```text
Query Phrase
     ↓
Tokenization & Governed Vocabulary Lookup
     ↓
Deterministic Candidate Scoring (Title Exact, Vocabulary Exact, Substring, Overlap)
     ↓
Ranked Candidates Receipt (max_candidates <= 6)
     ↓
Explicit Exact-ID Selection (Required upstream of Workbench Admission)
```

### Non-Authoritative Invariants
1. **Candidate Discovery Ranking**: Carries `AUTHORITY: CANDIDATE_DISCOVERY_ONLY` and `TECHNICAL_AUTHORIZATION: NOT_EVALUATED`.
2. **Rank-1 Non-Bypass**: Rank 1 candidate status strictly never authorizes an Engineering Gate.
3. **No Automatic Resolution**: Ambiguous queries (e.g. *"Roots"*) return multiple ranked candidates and require explicit confirmed selection.
4. **Governed Vocabulary Custody**: All alias terms belong exclusively in [`mathematics-engineering-discovery-vocabulary.v1.json`](policies/mathematics-engineering-discovery-vocabulary.v1.json). Runtime orchestration code (`engine/*.py`) contains **0** topic literals.
5. **Digest Binding & Drift Protection**: Mutating the registry or vocabulary catalog automatically invalidates prior discovery receipts.

---

## 3. Authoritative Workbench Architecture & Closure

Once an exact Engineering Gate ID is explicitly selected, the authoritative Workbench processes the request deterministically:

1. **Request Formulation**:
   The caller submits a `MathematicsEngineeringRequest` specifying exact `scope_refs`, requested `engineering_depth` (`FOUNDATION | STANDARD | RESEARCH`), and `learning_purpose`.
2. **Manifest Formulation**:
   `compile_mathematics_engineering_workbench.py` compiles the request into a `MathematicsEngineeringManifest` binding exact base registry and extension digests.
3. **Registry Validation**:
   The registry is verified against [`mathematics-technical-engineering-gate.schema.json`](contracts/mathematics-technical-engineering-gate.schema.json). Every gate must have non-empty `learner_title`, `mathematical_objective`, and `mandatory_equations`.
4. **Depth Policy Admission**:
   Gates are evaluated against generic depth criteria in [`mathematics-engineering-depth-policy.v1.json`](policies/mathematics-engineering-depth-policy.v1.json).
5. **Transitive Prerequisite Closure**:
   Prerequisites are recursively closed. Circular dependencies or missing prerequisite gates trigger deterministic fatal errors.
6. **Closure Receipt Issuance**:
   A tamper-proof `MathematicsEngineeringClosureReceipt` is generated containing the canonical digest of all admitted gates and closure order.

---

## 4. Canonical Domain Binding & Derived Visibility

1. **CDAU Admission**:
   The `MathematicsEngineeringBinding` binds exact Canonical Domain subtopics to closure receipt gate digests. Downstream compilers re-validate that the binding is current before compiling SDU or LAU units.
2. **Derived Engineering Visibility**:
   Engineering Gate metadata may be displayed in learner or teacher appendices (e.g. in generated workbooks or teacher dashboards) under `math-engineering-visibility-manifest.schema.json`.
   This visibility is explicitly marked:
   ```json
   {
     "authority": "DERIVED_ENGINEERING_VISIBILITY",
     "publication_authorization": "NOT_IMPLIED"
   }
   ```
   Visibility displays what was approved; it is not a secondary authoring or release mechanism.

---

## 5. Executable Contracts, Engines & Test Suites

| Component | Executable File | Purpose |
|---|---|---|
| **Domain Projection V2 (Normative)** | `contracts/math-engineering-domain-projection-v2.schema.json` | Canonical Engineering to CDR projection v2 |
| **Domain Projector V2** | `engine/project_engineering_to_domain_registry_v2.py` | Canonical domain projection compiler v2 |
| **Domain Projection V1 (Legacy)** | `contracts/math-engineering-domain-projection.schema.json` | Legacy transitional projection v1 schema |
| **Gate Schema** | `contracts/mathematics-technical-engineering-gate.schema.json` | Normative gate contract |
| **Discovery Schemas** | `contracts/mathematics-engineering-discovery-*.schema.json` | Request, receipt, and selection schemas |
| **Workbench Schemas** | `contracts/mathematics-engineering-*.schema.json` | Manifest, binding, and closure receipt schemas |
| **Gate Registry Policy** | `policies/mathematics-technical-engineering-gates.v1.json` | Authoritative 10 coherent gates + extensions |
| **Discovery Vocabulary** | `policies/mathematics-engineering-discovery-vocabulary.v1.json` | Governed 23 gate targets & 132 terms |
| **Gate Validator** | `engine/validate_mathematics_engineering_gates.py` | Rigorous gate contract validator |
| **Discovery Engine** | `engine/compile_mathematics_engineering_discovery.py` | Generic scoring and candidate generator |
| **Workbench Compiler** | `engine/compile_mathematics_engineering_workbench.py` | Manifest compilation & transitive closure |
| **Falsification Battery** | `tests/test_mathematics_engineering_gates.py` | 29 data-derived mutation falsifiers |
| **Discovery Benchmark** | `benchmarks/discovery/tests/test_engineering_discovery_benchmark.py` | 80-query 100% recall stress suite |
| **Topic Independence** | `tests/test_blueprint_topic_independence.py` | Guard ensuring 0 topic strings in engine |

---

## 6. Canonical Domain Projection Lifecycle (V2 Production Standard)

The transition of validated Engineering Gate preconditions into rich Canonical Domain Registry (CDR) assets is governed by **Domain Projection V2**:

- **Canonical Specification**: `math-engineering-domain-projection-v2.schema.json`
- **Authoritative Compiler**: `engine/project_engineering_to_domain_registry_v2.py`
- **Transitional Backward Compatibility**: The earlier V1 projection (`math-engineering-domain-projection.schema.json` and `engine/project_engineering_to_domain_registry.py`) is preserved with `LEGACY_TRANSITIONAL` metadata. All future downstream production pipelines must consume V2 projection receipts.
- **Invariants**:
  1. Projection is exact-ID only; it walks the prerequisite closure in the authoritative Engineering graph and binds directly to `scope_memberships`.
  2. Projected assets receive deterministic asset digests with full provenance referencing `engineering_gate_id`, `primary_subtopic_id`, and `capability_refs`.
  3. No topic-specific strings or fuzzy matching are permitted during projection.

