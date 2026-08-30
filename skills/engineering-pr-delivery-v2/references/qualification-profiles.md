# Domain-specific takeover qualification profiles

Structural Q1–Q5 compliance is not enough for engineering-critical work. Each current question set declares:

```text
QUALIFICATION_PROFILE: FEA | WRC_LOCAL_STRESS | LOAD_CALC | FIXED_FORMAT_WRITER | PARSER_TOPOLOGY | SOURCE_GOVERNANCE | GENERAL_ENGINEERING
QUALIFICATION_PROFILE_VERSION: 2
```

Historical profile-v1 endpoints remain immutable. The next material leg adopts profile version 2.

Every Q1–Q5 body carries:

```text
Domain challenge:
Exact repository data required:
Concrete payload:
Required derivation:
```

Q2 and Q4 also retain the explicit `Calculation/reconstruction:` field used by the earlier protocol.

`Concrete payload` must state the actual values/coordinates/loads/dimensions/record spans/offsets/IDs or equivalent exact data the candidate must use. `Required derivation` states the calculation or exact reconstruction to perform. `describe`, `explain`, `list`, `re-read`, or a topic label is not sufficient when stronger evidence is available.

For `FEA`, `WRC_LOCAL_STRESS`, `LOAD_CALC` and `FIXED_FORMAT_WRITER`, at least two questions must contain a hand-computable concrete payload. Q2 and Q4 must each contain non-empty concrete payload and derivation unless the Owner baseline explicitly maps the numerical work to other questions and the union still satisfies the minimum.

## FEA

Q1 binds to an actual retained element/member/node/load case and traces it through model/assembly/solve/recovery/presentation. At least two questions require numerical acts such as Jacobian/det(J), stiffness/end-force, equilibrium/reaction, transformation, recovery, strain energy, analytical/cross-solver reproduction or convergence calculation.

A prompt like `Reconstruct the distorted T6 Jacobian` is insufficient by itself when the relevant node coordinates/integration point are already known. Carry those values into the active prompt or Owner-baseline coverage fails.

Expected evidence includes actual element/node/mesh/DOF/material/load/integration-point data, not only the words `element`, `mesh` or `Jacobian`.

## WRC_LOCAL_STRESS

Bind to actual shell/attachment geometry, reference station/axes and load vector. Require exact local-axis/load-reference reconstruction and, where method authority permits, `r x F` transfer, dimensionless parameter/coefficient/stress reconstruction or published-case reproduction. Numerical software tolerances may not be promoted into physical applicability limits.

At least two questions should normally include concrete geometry/load values.

## LOAD_CALC

Bind to actual supports/components/load cases. Require free-body/equilibrium, force/moment transport, allocation/unallocated demand, CoG/gravity or result-contract reconstruction as applicable. Presentation-only work must still prove the numerical/result object is unchanged and identify the exact custody loss boundary.

At least two questions should normally include concrete forces/moments/coordinates/status values from the bounded case.

## FIXED_FORMAT_WRITER

Require byte/column/field-width/pointer/cardinality/record arithmetic using actual source rows and physical spans. Candidate must prove unchanged-byte invariants and identify the first illegal writer/arbitration boundary. Parser success alone is not an oracle.

At least two questions carry real byte/column/pointer/cardinality values.

## PARSER_TOPOLOGY

Require exact record/schema/topology/pointer/cardinality/hash reconstruction using actual repository input. Candidate predicts intermediate graph/state values and identifies the first parser/adapter ownership boundary. Exact record IDs/hashes/state transitions can substitute for ordinary numerical payload where arithmetic is not meaningful.

## SOURCE_GOVERNANCE

Source-only work is still technical. Q1 reconstructs source-locator → ledger/claim → implementation-consumer custody. Q2/Q4 require exact source-locator, applicability/input-inventory, dimensional/axis/sign or implementation-custody reconstruction as appropriate. Pure prompts such as `list the newly true claims` or `re-read the paragraph` are insufficient when the repository exposes a stronger implementation boundary.

## GENERAL_ENGINEERING

Use only when none of the named profiles fits. The question author still provides two exact technical reconstructions, repository anchors, independent oracle, falsifier and safe-patch/NO-PATCH boundary.

## Owner baseline has precedence over compression

If an Owner issue/roadmap/instruction supplies expert questions, follow `owner-qualification-baseline.md`. The active pack may reorganize or strengthen them but may not drop supplied numerical data, requested derivations, mechanisms, oracle requirements or negative controls.

## Fail-closed quality rule

A set is `INSUFFICIENT_TECHNICAL_DEPTH` if it has correct headings/verbs but does not force profile-specific engineering work. Technical vocabulary without concrete payload is not proof of qualification depth.
