# Physics V2 — Engineering Authority & Discovery Governance Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Physics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Consolidates**: Upstream Engineering Authority, Discovery Layer Invariants, Transitive Prerequisite Closure, and Derived Visibility.
> **Subject**: `PHYSICS` only.

---

## 1. Upstream Engineering Authority Direction

Engineering is upstream technical authority for Physics. Physics Blueprint does not invent, remember, or mutate physical laws, conservation criteria, free-body mechanics, or coordinate frame validity conditions. Blueprint consumes Engineering authority exclusively through exact, digest-bound identities, generic policy evaluation, and deterministic prerequisite closure.

```text
NATURAL-LANGUAGE QUERY / SEARCH / ALIAS / HINT / EXTERNAL RESEARCH
        │
        │ [1] Non-authoritative candidate discovery only
        ▼
RANKED ENGINEERING CANDIDATES (Authority: CANDIDATE_DISCOVERY_ONLY)
        │
        │ [2] Explicit exact-ID selection required (Technical Auth: NOT_EVALUATED)
        ▼
DIRECT ENGINEERING GATE IDENTIFIERS (e.g. PHY-WORK-ENERGY-POWER, PHY-NLM-FIRST-LAW)
        ▲
        │ [3] Validated against Canonical Registry & Depth Policy
        ▼
CANONICAL PHYSICS ENGINEERING REGISTRY (REG-PHYS-TECH-GATE-V1)
        │
        │ [4] Transitive Prerequisite Closure (<= 3 direct scope refs)
        ▼
ENGINEERING CLOSURE RECEIPT (Deterministic SHA-256 Digest)
        │
        │ [5] Exact Custody Binding (Subtopic -> Gate)
        ▼
CANONICAL DOMAIN ADMISSION (CDAU)
        │
        │ [6] Equal Custody Revalidation
        ▼
SDU (Core1A / Core1B) & LAU (Core2A / Core2B)
        │
        ▼
DERIVED ENGINEERING VISIBILITY (Publication Auth: NOT_IMPLIED)
```

### Governing Authority Invariants

1. **Direction of Authority**:
   ```text
   Engineering Registry → Closure Receipt → Domain Admission → Core Realization → Publication
   ```
   No downstream layer (SDU, LAU, TTU authoring, or renderer) may alter an Engineering precondition, omit an invariant (e.g., $W_{\text{nc}} = 0$ for mechanical energy conservation), or fabricate an Engineering identity.
2. **Subject Isolation**:
   Every request, manifest, receipt, and binding must declare `subject = PHYSICS`. Cross-subject or generic mathematical artifacts without physical model binding fail closed.
3. **Execution vs Authority Invariant**:
   *Execution order may vary; authority order may never vary.*

---

## 2. Non-Authoritative Discovery Boundary

The discovery layer provides an expressive natural-language on-ramp for students, educators, and curriculum engineers across CBSE, JEE Main, JEE Advanced, and NSEP Olympiad without compromising technical authority.

> **The Golden Boundary Rule**: *Discovery may be permissive. Authority may not be.*

```text
User / Learner Query Phrase
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
2. **Rank-1 Non-Bypass**: Rank 1 candidate status strictly never authorizes an Engineering Gate or permits pipeline entry.
3. **No Automatic Resolution**: Ambiguous or multi-domain queries (e.g. *"Work done by friction"*, *"Centripetal acceleration"*) return multiple ranked candidates and require explicit confirmed selection.
4. **Governed Vocabulary Custody**: All 365 alias terms and formulas belong exclusively in [`physics-engineering-discovery-vocabulary.v1.json`](policies/physics-engineering-discovery-vocabulary.v1.json). Runtime orchestration code (`engine/*.py`) contains **0** topic literals.
5. **Digest Binding & Drift Protection**: Mutating the registry or vocabulary catalog automatically invalidates prior discovery receipts.

---

## 3. Authoritative Workbench Architecture & Prerequisite Closure

Once an exact Engineering Gate ID is explicitly selected, the authoritative Workbench processes the request deterministically:

1. **Request Formulation**:
   The caller submits a `PhysicsEngineeringRequest` specifying exact `scope_refs`, requested `engineering_depth` (`FOUNDATION | STANDARD | RESEARCH`), and `learning_purpose`.
2. **Registry Validation**:
   The registry is verified against [`physics-technical-engineering-gate.schema.json`](contracts/physics-technical-engineering-gate.schema.json). Every gate must have non-empty `learner_title`, `physical_objective`, and `mandatory_equations`.
3. **Depth Policy Admission**:
   Gates are evaluated against generic depth criteria in [`physics-engineering-depth-policy.v1.json`](policies/physics-engineering-depth-policy.v1.json).
4. **Transitive Prerequisite Closure**:
   Prerequisites are recursively closed. Circular dependencies or missing prerequisite gates trigger deterministic fatal errors. The maximum direct scope references are capped at 3 to prevent unbounded scope inflation.
5. **Closure Receipt Issuance**:
   A tamper-proof `PhysicsEngineeringClosureReceipt` is generated containing the canonical digest of all admitted gates and closure order.

---

## 4. Canonical Domain Binding & Derived Visibility

1. **CDAU Admission**:
   The `PhysicsEngineeringBinding` binds exact Canonical Domain subtopics to closure receipt gate digests. Downstream compilers re-validate that the binding is current before compiling SDU or LAU units.
2. **Derived Engineering Visibility**:
   Engineering Gate metadata may be displayed in learner or teacher appendices under `physics-engineering-visibility-manifest.schema.json`.
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
| **Gate Schema** | `contracts/physics-technical-engineering-gate.schema.json` | Normative gate contract |
| **Discovery Schemas** | `contracts/physics-engineering-discovery-*.schema.json` | Request, receipt, selection, and vocabulary schemas |
| **Workbench Schemas** | `contracts/physics-engineering-request.schema.json` | Generic engineering request schema |
| **Gate Registry Policy** | `policies/physics-technical-engineering-gates.v1.json` | Authoritative 43 coherent gates across Grades 9–11 |
| **Discovery Vocabulary** | `policies/physics-engineering-discovery-vocabulary.v1.json` | Governed 43 gate targets & 365 terms |
| **Gate Validator** | `engine/validate_engineering_gates.py` | Rigorous gate contract validator |
| **Discovery Engine** | `engine/compile_physics_engineering_discovery.py` | Generic scoring and candidate generator |
| **Falsification Battery** | `tests/test_physics_engineering_gates.py` | Gate contract & registry falsification tests |
| **Discovery Benchmark** | `benchmarks/discovery/tests/test_engineering_discovery_benchmark.py` | 167-query 100% recall stress suite |
| **Run Builder Test Suite** | `tools/run_builder/tests/test_run_builder.py` | Determinism & fixture validation suite |
| **Architecture Explorer Test Suite** | `tools/architecture_explorer/tests/test_architecture_explorer.py` | Manifest integrity & graph relationship tests |
