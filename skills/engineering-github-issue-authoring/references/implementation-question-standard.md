# Implementation Qualification Question Standard

## Purpose

The five questions at the end of an engineering issue are a **senior-engineer implementation screen**. They should reveal whether the incoming agent understands the actual production path, can reconstruct critical engineering/semantic quantities independently, can detect stale authority, and can propose the smallest safe patch.

They are not textbook questions and not a task checklist.

## Exactly five questions

Use this conversational intent:

```text
Q1  Walk me through the actual case.
Q2  Do this calculation/reconstruction before touching the code.
Q3  Show me where the wrong/stale state gets stopped.
Q4  Prove the benchmark independently.
Q5  What is the smallest patch you would make?
```

The headings may be made domain-specific, but the five functions must survive.

## Human-like style

Write the questions as a senior engineer speaking to another engineer:

Good:

> Take the actual T6 element from the regression fixture with nodes ... . Before looking at the solver output, calculate `J` and `det J` at the centroid and the first Hammer point. Then show me the exact production function that should produce the same sign/order and tell me what single intermediate value would prove the node ordering is wrong.

Bad:

> Explain T6 elements and Jacobians.

Good:

> For the actual 80-byte record in `fixtures/...`, start at byte 24 and apply the live field widths/alignment rules by hand. What offset should the parser reach after fields A/B/C, and which function should reject the record if it lands at 78 instead of 80?

Bad:

> How does the parser work?

Good:

> With the issue loads `Fx=...`, `Fy=...`, `M=...` at the stated reference point, close the free body by hand and transport the moment to the support. Which production intermediate must equal your result, including sign convention, before you would touch presentation code?

Bad:

> Describe equilibrium.

## Question construction sequence

For each question:

1. Pick an **actual bounded object/case** from the live repository or issue input.
2. Include concrete payload: IDs, coordinates, loads, dimensions, byte offsets, hashes, states, record widths, expected-value source, or other exact data.
3. Ask for a predicted intermediate/result **before** reading production output where possible.
4. Require one exact live repository anchor: path/function/type/state boundary.
5. Require a falsifier or first-wrong-boundary statement.
6. Make generic prose insufficient to pass.

## Numerical engineering profile

For `QUESTION_PROFILE: NUMERICAL_ENGINEERING`:

- at least two questions require genuine hand calculation;
- normally Q2 and Q4 are the main calculations;
- use actual issue/repository values, not invented classroom numbers when live values exist;
- include units, axes/sign convention and tolerances where applicable;
- ask for intermediate values, not only the final scalar;
- require comparison to a named production boundary after the hand result is established.

Useful domains include:

```text
FEA element/Jacobian/B-matrix/integration
statics/equilibrium/load transfer/moment transport
WRC/local-stress coordinate reconstruction
shell/continuum benchmark response
geometry/topology area/normal/orientation
thermal/pressure/section calculations
numerical convergence/order/error estimates
```

## Software engineering profile

For `QUESTION_PROFILE: SOFTWARE_ENGINEERING`, use exact deterministic reconstruction when hand physics/math is not meaningful:

```text
byte/record offset arithmetic
parser cursor evolution
hash/canonicalization derivation
state-machine transitions
cache/key invalidation
database row/version evolution
protocol/frame length arithmetic
coordinate/index transformation
fixed-format output positions
```

At least two questions should require the candidate to produce exact intermediate values/states, not merely describe architecture.

## Source-governance profile

For `QUESTION_PROFILE: SOURCE_GOVERNANCE`, require exact provenance reconstruction:

```text
source -> normalized fact -> authority record -> production consumer
```

Use concrete source IDs/claims/revisions. Ask the candidate to identify which claim is admissible, which is conflicted, and what exact evidence would falsify the chosen disposition. If numerical source data exists, include a hand reconstruction rather than making all five questions documentary.

## Q1 — actual production trace

Must include:

- actual object/case/fixture/input;
- exact production path from source to output;
- important IDs/hashes/states at boundaries;
- first ownership/authority transition;
- one observation that would falsify the trace.

Reject:

```text
Explain the architecture.
Describe the workflow.
Which modules are involved?
```

## Q2 — hand calculation / exact reconstruction

Must include actual payload and ask for intermediate values.

Examples:

```text
calculate J, det(J), B or shape derivatives for the supplied element
close the stated free body and transport moment to the exact reference
reconstruct byte offsets/field widths for the supplied record
compute expected canonical hash ingredients/order before hashing
derive exact parser/state transitions from the supplied token sequence
```

Require:

- predicted intermediate values;
- first production function/lineage that should agree;
- first-wrong-boundary interpretation if it does not;
- falsifier.

## Q3 — authority / stale-state / failure isolation

Give one concrete wrong-state mutation:

```text
source revision changes but mesh stays old
record schema changes but cached parse stays old
roadmap/source authority changes but result remains publishable
benchmark source changes but expected registry does not
```

Ask:

- which exact parent IDs/revisions/hashes should disagree;
- where the live code must block;
- expected failure/state/error;
- one test that would prove the candidate's model is wrong.

## Q4 — independent benchmark reconstruction

Require an oracle independent of the production path under test.

Strong:

```text
analytical hand calculation
code/standard equation evaluated independently
external frozen reference value
cross-solver value with independent model custody
experimental/frozen dataset
```

Weak/not independent:

```text
current production output copied into expected JSON
same implementation helper used in both solver and expected-value generator
moving maximum selected after seeing solution
UI contour/value used as validation
```

Require inputs, units/sign convention, tolerance and an explicit anti-circularity statement.

## Q5 — smallest safe patch

The candidate must state:

```text
first exact function/file to change
why that is the first wrong boundary
expected failing evidence before patch
expected PASS after patch
protected files/domains that remain unchanged
negative/neighbor regression
a rollback/falsifier condition
NO-PATCH condition
```

A valid `NO-PATCH` answer should be possible when the observed issue is environment/source/authority drift rather than a production-code defect.

## Difficulty floor

A five-question set should normally satisfy:

```text
>= 2 hand calculations or exact deterministic reconstructions
>= 3 questions with concrete live-repository anchors
>= 1 end-to-end production trace
>= 1 independent oracle
>= 1 explicit falsifier
>= 1 safe-patch + rollback + NO-PATCH boundary
```

For numerical engineering, at least one question should be difficult enough that a candidate who cannot do the underlying engineering by hand cannot bluff through it using repository prose.

## Anti-patterns

Reject questions whose answer is essentially a definition, list, or file lookup:

```text
What is FEA?
What does this function do?
Which file contains the solver?
What is a benchmark?
Why are tests important?
What would you change?
```

Reject vague calculation prompts:

```text
Calculate the Jacobian.
Check equilibrium.
Verify the benchmark.
```

unless the actual data, conventions and expected production boundary are supplied.

## Owner-authored question preservation

If the Owner supplied questions or a reference issue contains Owner-approved questions, treat them as a minimum baseline. Strengthen them with concrete live values/reconstruction where possible; do not replace a hard numeric question with a broad topic label.

## Final self-check

Before posting the issue, ask:

> Could a smart generalist answer these five questions convincingly without reading the live repository and without doing the requested calculation/reconstruction?

If yes, the questions are too weak.
