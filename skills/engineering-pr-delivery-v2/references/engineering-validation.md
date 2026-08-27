# Engineering Validation

## Evidence dimensions

For every material validation record preserve:

```text
STATUS
  PASS | FAIL | NOT_RUN | NOT_APPLICABLE

OBSERVATION
  LOCAL_EXECUTION | REMOTE_EXECUTION | SOURCE_INSPECTION
  ARTIFACT_INSPECTION | USER_SUPPLIED | INFERRED | NOT_OBSERVED

ORACLE
  NONE | IMPLEMENTATION_COUPLED | INDEPENDENT_REPRODUCTION
  ANALYTICAL | AUTHORITATIVE_REFERENCE | CROSS_SOLVER | EXPERIMENTAL
```

Also record where applicable:

```text
TESTED_HEAD
command/evidence
expected
actual
tolerance
units/sign convention
limitations
failure origin
```

## Engineering-critical boundaries

For FEA, stress, load, numerical, geometry, code-assessment, or engineering-publication work, be able to distinguish relevant boundaries such as:

```text
source authority
-> canonical data
-> geometry/topology
-> transformation
-> assembly/calculation
-> solver
-> recovery
-> coordinate/sign mapping
-> publication/export/UI
```

Identify the first wrong boundary before changing upstream mechanisms.

## Independent evidence

Software regression and independent engineering verification are different.

A test that imports the same implementation or derives expected values from production output is not an independent oracle.

Use independent evidence where the engineering consequence requires it, such as:

- analytical hand calculation;
- published/reference example;
- independently frozen source value;
- cross-solver comparison;
- free-body/equilibrium reconstruction;
- independent source arithmetic.

## Numerical integrity

Where applicable protect:

- units;
- coordinate-system conventions;
- DOF/order/end conventions;
- sign conventions;
- local/global transformations;
- moment transport/reference points;
- tolerance provenance;
- benchmark independence;
- deterministic ordering/hash identity.

## Negative assurance

For a material engineering change state both:

```text
WHAT CHANGED
WHAT MUST REMAIN UNCHANGED
```

The latter belongs in the endpoint's protected invariants / do-not-change sections.

## NOT_RUN

`NOT_RUN` must remain visible across every relay endpoint until replaced by actual observation or explicitly classified `NOT_APPLICABLE` with rationale.

Do not let a later agent inherit a vague phrase such as `tests okay` when the prior evidence was only source inspection or infrastructure prevented execution.
