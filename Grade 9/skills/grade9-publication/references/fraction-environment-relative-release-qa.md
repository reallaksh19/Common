# Fraction, Environment, Relative-Motion, and Carrier-Release QA

Use this checkpoint set whenever a student-facing batch contains speed-fraction versus height-fraction reasoning, comparison of the same motion model across environments with different `g`, equal-acceleration relative motion, delayed launch followed by relative motion, or release from a moving carrier/platform.

These checks are additive to source fidelity, math typography, artifact separation, and general Student Page QA.

## AD-65 SQUARED-FRACTION TRANSFORMATION INTEGRITY

When the source uses the no-time relation `v² = u² - 2gy` to connect a speed fraction to a height fraction, preserve the quadratic structure.

Required checks:
- define the speed fraction first, e.g. `v = ku`;
- square that fraction before converting it into a height fraction;
- preserve `y/H = 1 - k²` when `H = u²/(2g)` is the same maximum-height model;
- never publish a linear shortcut such as `y/H = 1-k` unless the source explicitly defines a different model.

Fail if the visual or text suggests that halving speed means halving height.

## AD-66 REACHED / REMAINING COMPLEMENT INTEGRITY

When `v = ku` under the same ideal vertical-motion model:
- reached fraction of maximum height = `1-k²`;
- remaining fraction above the object = `k²`.

These two meanings must be visually labelled and must sum to 1. Do not swap them.

Use a worked check such as `k=1/2`: reached `3/4`, remaining `1/4`.

## AD-67 SINGLE-PARAMETER ENVIRONMENT COMPARISON

A change of planet/environment does not create a new kinematic law when the source keeps the constant-acceleration model.

Required checks:
- write the same governing equation in both environments;
- label the parameter that changes (`g`) and the quantity held fixed (`u`, `H`, etc.);
- for same `u`, preserve `H ∝ 1/g`;
- for same `H`, preserve `u ∝ √g`;
- form ratios before inserting numbers whenever the source uses comparison reasoning.

Fail if the publication invents a new formula merely because the context changes.

## AD-68 ENVIRONMENT-RATIO PROVENANCE

Numerical environment constants or ratios must not be silently supplied by the publisher.

For values such as `g_Moon ≈ g_Earth/6`:
- use the ratio only when the source/question supplies it or the project explicitly treats it as prerequisite knowledge;
- if the source contains a caution that a ratio is not visibly supplied, preserve that caution in the audit and do not conceal the dependency;
- never convert a qualitative comparison into a numerical answer by inventing an external constant.

## AD-69 RELATIVE-ACCELERATION CANCELLATION SCOPE

For two bodies under the same gravitational acceleration:
- preserve `a_rel = a_A - a_B`;
- show that equal `-g` terms cancel only in the relative/separation equation;
- keep each body's absolute acceleration nonzero in the ground frame;
- constant relative velocity follows only while the two bodies actually share the same acceleration.

Fail if `a_rel=0` is presented as meaning gravity is absent.

## AD-70 COMMON-CLOCK TO RELATIVE-MOTION HANDOFF

For delayed launch or delayed release followed by equal-acceleration relative motion:
1. use the common clock to identify the handoff instant;
2. snapshot the earlier body's position and velocity at that instant;
3. only after both bodies share the same acceleration may the publication switch to the relative-motion simplification.

Fail if the earlier body's state is skipped or relative motion is applied before the second body becomes active.

## AD-71 RELEASE-FRAME VELOCITY INHERITANCE

For an object simply released from a moving carrier:
- `dropped/released` means zero extra velocity relative to the carrier at the instant of release;
- the object's ground-frame initial velocity equals the carrier's instantaneous ground-frame velocity when no extra throw is given;
- state the chosen frame before assigning the initial velocity sign.

Fail if every occurrence of the word `dropped` is converted to `u=0` in the ground frame.

## AD-72 NO-RESET CARRIER-RELEASE CONTINUITY

A release event changes the forces/constraints acting on the object, not its instantaneous velocity.

Required checks:
- carry the carrier's instantaneous velocity into the free-flight stage;
- if the carrier is rising, the released object may continue rising before gravity reverses it;
- ground-frame equations must start with the inherited `u`, e.g. `y = y0 + Vt - 1/2 gt²` for upward-positive release from a rising carrier;
- do not visually imply that velocity jumps to zero at release unless the source explicitly describes an impulse that causes that change.

## Required review sequence

1. Freeze source equations, fractions, environment assumptions, frame language, and timing conditions.
2. For fraction pages, verify `k -> k² -> reached/remaining` in that order.
3. For environment pages, mark what is held fixed before forming ratios and verify any numerical `g` ratio is source-supported.
4. For relative motion, verify both absolute accelerations and the relative subtraction.
5. For delayed launch, verify the state snapshot before switching models.
6. For moving-carrier release, verify the chosen frame and velocity inheritance at the release instant.
7. Render and inspect all formulas, radicals, subscript labels, arrows and frame diagrams at normal viewing size.
8. Record zero findings for AD-65 through AD-72 before release.
