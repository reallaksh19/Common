# Golden example — parallel focused child

```text
ISSUE_ROLE: PARALLEL_FOCUSED
PROGRAMME: github:owner/repo#210
WORKSTREAM_ID: F
RELAY_PROTOCOL: V3.1_ONLY
```

## Outcome
Make one declared falsifier executable.

## Owned responsibility
Focused mutation helper/registration and assertions.

## Ownership boundary
Do not change the canonical declaration or unrelated runtime surfaces.

## Acceptance Contract

| ID | Criterion | Parent mapping | Weight |
|---|---|---|---:|
| AC-F-01 | bounded mutation exists | EXIT-P5 | — |
| AC-F-02 | exact declared violation observed | EXIT-P5 | — |
| AC-F-03 | neighboring mutation cases remain green | EXIT-P5 | — |
| AC-F-04 | producer output is durably delivered | EXIT-P5 | — |

## Falsifier
If the bounded mutation does not generate the declared violation, stop and reframe the assumed defect.

## Implementation Plan
Agent-authored `STEP-*` slices map to the `AC-*` criteria.

## Expected handoff
Exact material, validation, proved/not-proved, consumer consequence.
