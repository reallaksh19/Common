# Chemistry V2 — Engineering Authority & Workbench Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Chemistry V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Subject**: `CHEMISTRY` only.

---

## 1. Authority Hierarchy & Invariant Direction

```text
ENGINEERING REGISTRY (chemistry-technical-engineering-gates.v1.json)
        ↓
ENGINEERING CLOSURE RECEIPT (Deterministic SHA-256 Digest)
        ↓
CANONICAL DOMAIN ADMISSION (CDAU Binding)
        ↓
CORE REALIZATION (Core1A, Core1B, Core2A, Core2B)
        ↓
DERIVED ENGINEERING VISIBILITY (Publication Auth: NOT_IMPLIED)
```

1. **Direction of Authority**: No downstream layer (SDU, LAU, or renderer) may alter an Engineering precondition, omit an invariant, or fabricate an Engineering identity.
2. **Subject Isolation**: Every request, manifest, receipt, and binding must declare `subject = CHEMISTRY`.
3. **Deterministic Closure**: Prerequisites are transitively closed across all 52 gates with cycle detection.

---

## 2. Non-Authoritative Discovery Boundary

The discovery engine provides a tolerant on-ramp for user queries while preserving the strict engineering authorization boundary:
- Carries `AUTHORITY: CANDIDATE_DISCOVERY_ONLY` and `TECHNICAL_AUTHORIZATION: NOT_EVALUATED`.
- Governed vocabulary catalog in [`chemistry-engineering-discovery-vocabulary.v1.json`](policies/chemistry-engineering-discovery-vocabulary.v1.json) (52 entries, 368 terms).
- Requires explicit selection upstream of Workbench admission.

---

## 3. Canonical Domain Projection Lifecycle (V1 & V2)

- **Domain Projection V2 (Normative)**: [`chemistry-engineering-domain-projection-v2.schema.json`](contracts/chemistry-engineering-domain-projection-v2.schema.json) compiled via [`project_engineering_to_domain_registry_v2.py`](engine/project_engineering_to_domain_registry_v2.py).
- **Domain Projection V1 (Transitional)**: [`chemistry-engineering-domain-projection.schema.json`](contracts/chemistry-engineering-domain-projection.schema.json).
- **Derived Visibility Manifest**: [`chemistry-engineering-visibility-manifest.schema.json`](contracts/chemistry-engineering-visibility-manifest.schema.json) compiled via [`compile_engineering_visibility_manifest.py`](engine/compile_engineering_visibility_manifest.py).
