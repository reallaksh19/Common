# Multi-Object Time and Geometry QA

Use these checkpoints when a student-facing batch contains delayed starts, catch-up/meeting events, multiple moving bodies, braking objects, or any problem that combines separate motion models with later geometry.

## AD-42 COMMON-CLOCK INTEGRITY

A shared observation instant does not imply identical elapsed time for every body or stage.

Before equations are written, identify:

- one global clock for the story;
- each body's start instant;
- each body's local elapsed time at the event;
- every stage boundary that resets local elapsed time.

Typical delayed-start mapping:

```text
A starts at global 0  -> elapsed time = T
B starts at global τ  -> elapsed time = T - τ
```

Fail if a delayed body is silently assigned the same elapsed time as an earlier-starting body.

## AD-43 MEETING-EVENT LINKAGE

At a meeting/catch-up event, two facts must be represented together:

1. the positions are equal at one common global instant;
2. the local elapsed times appearing inside the two motion equations may differ.

Do not collapse these into one generic `t` unless the start histories really are identical.

For a delayed body, a valid meeting model may look conceptually like:

```text
x_A(T) = x_B(T - τ)
```

with the appropriate motion law used inside each side.

Fail if the publication emphasizes equal position but hides the clock translation, or emphasizes the delay but never links it to the meeting condition.

## AD-44 PATH-LENGTH VS SIGNED-DISPLACEMENT INTEGRITY

When two vehicles brake toward each other and the final question is geometric separation, distinguish signed coordinate displacement from positive stopping path length.

For the compact path-length method:

```text
s1 > 0
s2 > 0
remaining gap = D - (s1 + s2)
```

Interpretation:

- remaining gap > 0 -> positive separation remains;
- remaining gap = 0 -> just-touch threshold;
- remaining gap < 0 -> required stopping paths exceed the initial separation, so collision occurs before both stop.

A signed-coordinate method is also valid, but one sign convention must be maintained throughout. Do not calculate signed displacements and then switch to unsigned geometry mid-solution without an explicit conversion.

Fail if one stopping path is made negative merely because that vehicle moves left while the final comparison uses geometric path lengths.

## AD-45 MODEL-COMPOSITION ORDER

For multi-object or multi-stage problems, solve each valid local physics model before applying cross-object geometry or ratios.

Required order:

```text
identify each object/stage
-> assign local time and sign convention
-> solve each motion model independently
-> combine positions/path lengths only afterward
-> interpret the final geometry
```

Examples:

- delayed starts: translate T into each local elapsed time before applying kinematics;
- two braking cars: compute each stopping path before subtracting from the initial separation;
- multistage journeys: solve each stage before averaging or combining totals.

Fail if one giant equation mixes incompatible time origins, sign conventions, or stages.

## Required review sequence

1. Draw or inspect the global timeline.
2. Verify every local elapsed-time expression.
3. Check that meeting equality, if present, uses one global instant.
4. Inspect whether path length versus signed displacement is explicit.
5. Confirm each object/stage is solved before geometry/comparison.
6. Verify displayed formulas are complete and legible at normal viewing size.
7. Record the following counters/statuses before release:

```text
common_clock_findings = 0
meeting_event_findings = 0
path_length_sign_findings = 0
model_composition_findings = 0
```
