# Common Validation Protocol

Separate software verification, engineering verification, observation method, and oracle independence.

## Validation status

- `PASS`
- `FAIL`
- `NOT_RUN`
- `NOT_APPLICABLE`

Never write only `tests pass`. Name the exact test/check and tested HEAD where practical.

## Observation method

- `LOCAL_EXECUTION`
- `REMOTE_EXECUTION`
- `SOURCE_INSPECTION`
- `ARTIFACT_INSPECTION`
- `USER_SUPPLIED`
- `INFERRED`
- `NOT_OBSERVED`

Do not describe source inspection as an executed PASS.

## Oracle independence

- `NONE`
- `IMPLEMENTATION_COUPLED`
- `INDEPENDENT_REPRODUCTION`
- `ANALYTICAL`
- `AUTHORITATIVE_REFERENCE`
- `CROSS_SOLVER`
- `EXPERIMENTAL`

A test is not independent validation when its expected value is generated from the same algorithm, formulation, transformation, data source, or code path being tested.

## Validation record

Record where material:

```text
Validation
Status
Observation
Oracle
Expected
Actual
Tolerance / acceptance rule
HEAD
Evidence / artifact / command
```

## Software validation examples

- unit tests;
- integration tests;
- regression tests;
- type checking;
- linting;
- build;
- runtime smoke tests.

## Explicitly not validated

Maintain a visible list of significant properties that remain unproven.

Never turn `not checked` into `assumed correct`.
