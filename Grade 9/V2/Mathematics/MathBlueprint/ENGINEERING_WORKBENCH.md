# Mathematics Engineering Workbench

## Subject ownership

This Workbench is **MATHEMATICS-only**.

- Canonical implementation PR: **#351**.
- Mathematics Technical Engineering Gate data: **#379 / `REG-MATH-TECH-GATE-V1`**.
- Physics PR #350 is a **read-only architecture reference only**. No Physics gate, manifest, receipt, or policy is an authority in this Workbench.

Every Workbench request, manifest, closure receipt, passport and binding carries `subject = MATHEMATICS`; non-Mathematics artifacts fail closed.

## Authority model

```text
ORIGINAL / VALIDATED MATHEMATICS GROUND TRUTH
                ↓
       Core1 × Core2 validated join
                ↓
        Engineering Request
                ↓
        Engineering Manifest
                ↓
REG-MATH-TECH-GATE-V1  ×  EXTERNAL INVARIANT PROFILE
                ↓
      VALIDATOR-DERIVED GATE STATES
                ↓
     TRANSITIVE PREREQUISITE CLOSURE
                ↓
       ENGINEERING CLOSURE RECEIPT
                ↓
          EXACT CUSTODY BINDING
                ↓
  Canonical Domain Registry / CDAU / SDU / LAU
```

The gate registry provides technical data. It does **not** authorize itself.

`technical_readiness` and `release_checklist` inside the PR #379 registry are retained for compatibility and historical inspection, but the Workbench deliberately ignores both when deriving readiness.

```text
GATE CONTENT
   ×
EXTERNAL INVARIANT PROFILE
   ×
PROVENANCE / PREREQUISITE / CROSS-REFERENCE VALIDATION
   ↓
DERIVED ENGINEERING_GATE_READY | INCOMPLETE | SOURCE_SCOPE_HELD
```

## External invariant profile

`policies/mathematics-engineering-gate-invariants.v1.json` is independent of the self-authored gate checklist. It names required canonical concepts/equations/representations/misconceptions/prerequisites for the ten PR #379 gates and imposes generic reasoning, transformation, verification, problem-family and difficulty-profile requirements.

A gate cannot rescue missing content by setting `technical_readiness = ENGINEERING_GATE_READY` or by marking its checklist true.

Conversely, a stale declared `ENGINEERING_GATE_INCOMPLETE` cannot demote technically complete content: the Workbench re-derives state.

## Bounded manifest

The manifest may declare at most three direct gates. The Workbench recursively computes all Mathematics prerequisites. Direct-gate count is a relay bound, not a limit on transitive technical closure.

## Exact closure custody

Downstream consumers do not redeclare prerequisite closure. `mathematics-engineering-binding.schema.json` stores exact custody of:

- request and manifest refs;
- closure receipt ID and digest;
- technical registry digest;
- external invariant-profile digest;
- named downstream consumer.

`validate_mathematics_engineering_binding.py` recompiles the current Workbench closure. Any registry/profile/closure drift makes the binding stale and blocks consumption.

## Authorization boundary

A READY engineering closure means only:

> the requested Mathematics scope is technically engineered with validated prerequisite closure.

It does not prove pedagogy, learner mastery, transfer legality, source legality beyond recorded provenance, visual usability, or publication readiness.

Every Passport therefore carries:

`publication_authorization = NOT_IMPLIED`.

## Initial vertical slice

`MATH-QUAD-EQUATIONS` is the first Workbench vertical slice because it has a real Mathematics prerequisite:

```text
MATH-ALG-POLYNOMIALS
        ↓
MATH-QUAD-EQUATIONS
```

The test suite proves recursive closure, validator-derived readiness, external-profile authority, source-scope holds, subject rejection, cycle rejection, and exact stale-binding rejection.
