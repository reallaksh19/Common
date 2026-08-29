# Domain-specific takeover qualification profiles

Structural Q1–Q5 compliance is not enough for engineering-critical work. Each current v3 question set declares:

```text
QUALIFICATION_PROFILE: FEA | WRC_LOCAL_STRESS | LOAD_CALC | FIXED_FORMAT_WRITER | PARSER_TOPOLOGY | SOURCE_GOVERNANCE | GENERAL_ENGINEERING
```

Every Q1–Q5 body also carries:

```text
Domain challenge:
Exact repository data required:
```

Q2 and Q4 additionally carry:

```text
Calculation/reconstruction:
```

The field must state the actual calculation or exact reconstruction the candidate must perform; `describe`, `explain`, `list`, or source-reading alone is not sufficient when stronger technical evidence is available.

## FEA

Q1 should bind to an actual retained element/member/node/load case and trace it through model/assembly/solve/recovery/presentation. Q2 and Q4 should normally require two independent numerical acts such as Jacobian/det(J), stiffness/end-force, equilibrium/reaction, transformation, recovery, strain energy or analytical/cross-solver reproduction.

Expected vocabulary/evidence includes actual element/node/mesh/DOF/stiffness/Jacobian/equilibrium/reaction/recovery/transformation data.

## WRC_LOCAL_STRESS

Bind to actual shell/attachment geometry, reference station/axes and load vector. Require exact local-axis/load-reference reconstruction and, where method authority permits, load transfer, dimensionless parameter/coefficient/stress reconstruction or published-case reproduction. Numerical software tolerances may not be promoted into physical applicability limits.

## LOAD_CALC

Bind to actual supports/components/load cases. Require free-body/equilibrium, force/moment transport, allocation/unallocated demand, CoG/gravity or result-contract reconstruction as applicable. Presentation-only work must still prove the numerical/result object is unchanged and identify the exact custody loss boundary.

## FIXED_FORMAT_WRITER

Require byte/column/field-width/pointer/cardinality/record arithmetic using actual source rows and physical spans. Candidate must prove unchanged-byte invariants and identify the first illegal writer/arbitration boundary. Parser success alone is not an oracle.

## PARSER_TOPOLOGY

Require exact record/schema/topology/pointer/cardinality/hash reconstruction using actual repository input. Candidate should predict intermediate graph/state values and identify the first parser/adapter ownership boundary.

## SOURCE_GOVERNANCE

Source-only work is still technical. Q1 must reconstruct source-locator → ledger/claim → implementation-consumer custody. Q2/Q4 must require exact source-locator, applicability/input-inventory, dimensional/axis/sign or implementation-custody reconstruction as appropriate. Pure prompts such as `list the newly true claims` or `re-read the paragraph` are insufficient when the repository exposes a stronger implementation boundary.

## GENERAL_ENGINEERING

Use only when none of the named profiles fits. The question author must still provide two exact technical reconstructions, repository anchors, independent oracle, falsifier and safe-patch/NO-PATCH boundary.

## Fail-closed quality rule

A set is `INSUFFICIENT_TECHNICAL_DEPTH` if it has the right headings but does not force profile-specific engineering work. In particular, a question pack cannot satisfy an FEA/WRC/load-calc/fixed-format profile by substituting generic governance prose.
