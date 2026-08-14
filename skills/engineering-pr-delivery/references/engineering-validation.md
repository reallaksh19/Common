# Engineering-Critical Validation

Load this reference when criticality is `ENGINEERING_CRITICAL` or `SAFETY_CRITICAL`.

Software correctness and engineering correctness are separate claims.

## Freeze the basis before changing mechanics

Record as applicable:

- governing units;
- coordinate axes and handedness;
- DOF ordering;
- sign conventions;
- element/end conventions;
- geometry and topology authority;
- material/section/property authority;
- load and restraint authority;
- governing code/standard edition;
- expected physical behavior;
- independent expected-value source;
- acceptance tolerance and why it is appropriate.

Missing or ambiguous engineering authority must fail closed. Do not silently substitute defaults.

## Numerical validation

Require the relevant combination of:

- closed-form/analytical benchmark;
- independent numerical reproduction;
- force equilibrium;
- moment equilibrium;
- six-DOF residual checks where applicable;
- free-body cuts;
- dimensional consistency;
- energy consistency where applicable;
- rigid-body/mechanism checks;
- mesh convergence where applicable;
- orientation/member-reversal invariance where applicable;
- limiting/special-case behavior;
- cross-solver or commercial comparison where applicable.

For finite-element/end-action recovery work, trace the failed reported quantity back to the raw solver quantity. Distinguish stiffness/load assembly, solver equilibrium, local/global transformation, fixed/initial actions, end-I/end-J signs, moment transport, result recovery, and report mapping rather than changing several mechanisms simultaneously.

Where appropriate verify the relationship:

```text
q = K u - f_fixed - f_initial
```

using the repository's declared conventions.

## Commercial-program comparison

A commercial comparison is meaningful only when the following are matched or explicitly reconciled:

- geometry;
- material/section properties;
- loads;
- restraints/springs/gaps;
- element formulation and flexibility factors;
- pressure/thermal/Bourdon options where relevant;
- units;
- coordinate system;
- result location;
- sign/end convention.

## Expected values

Do not generate the expected value from the implementation under test and then call the match independent verification.

## UI / publication authority

Rendering, contouring, smoothing, averaging, autoscaling, display projection, report mapping, or preview state must not silently become numerical authority.

## Capability maturity

Track separately:

```text
IMPLEMENTATION: NOT_STARTED / PARTIAL / IMPLEMENTED
INTEGRATION: NOT_INTEGRATED / PARTIAL / INTEGRATED
SOFTWARE_VALIDATION: NOT_RUN / FAIL / PASS
ENGINEERING_VALIDATION: NOT_REQUIRED / NOT_RUN / PARTIAL / FAIL / PASS
RELEASE_STATE: NOT_READY / BLOCKED / READY
```

Do not collapse these into one `DONE` state.
