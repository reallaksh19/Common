# Vertical Stage, Turning-Point, and Same-Height Symmetry QA

Use this checkpoint set whenever a student-facing batch contains window crossing after a prior fall, vertical throw turning points, time-to-top/maximum-height/flight-time results, same-height double passages, or root-based vertical-motion symmetry.

These checks are additive to source fidelity, math typography, artifact separation, and the general Student Page QA gates.

## AD-55 STAGE-CONTINUITY INTEGRITY

A new calculation stage is not automatically a physical restart.

For window-crossing or approach-then-cross problems:

- identify the approach stage and the local crossing stage explicitly;
- compute or preserve the entry speed at the stage boundary;
- carry that entry speed into the next-stage equation;
- never silently set `u = 0` at a window/top-edge/checkpoint unless the source states the object is released there;
- if a stage boundary is only a calculation convenience, preserve the object’s physical continuity through it.

Fail if the learner sees a new stage that visually or algebraically resets the body to rest without source support.

## AD-56 LOCAL-VS-TOTAL TIME DISTINCTION

When comparing release heights and local crossing intervals, distinguish total journey time from time spent in the local interval.

Check that:

- a higher release may increase total fall time while also increasing entry speed;
- for the same local distance `H` under the same `g`, larger entry speed implies a smaller positive crossing time;
- diagrams label the local interval clearly instead of visually merging it with the whole fall;
- explanations do not claim that a longer total journey must mean a longer local crossing.

Fail if total time and local interval time are conflated.

## AD-57 TURNING-POINT STATE INTEGRITY

At the highest point of an ideal vertical throw with upward-positive coordinates:

- `v = 0` at the turning instant;
- `a = -g` remains nonzero;
- the sign convention remains unchanged through the top;
- the page does not visually imply that gravity stops when velocity reaches zero.

Fail if `v = 0` is paired with `a = 0` or if acceleration is omitted in a way that reinforces that misconception.

## AD-58 v-t SLOPE INTEGRITY

If a velocity-time graph is used for the vertical throw:

- it must be a straight line of constant slope `-g` under the ideal model;
- it must cross `v = 0` rather than flatten at the top;
- the zero crossing must correspond to the turning instant;
- the negative slope must continue through the zero crossing.

Fail if the graph becomes horizontal at the top or suggests acceleration changes there.

## AD-59 TURNING-CONDITION DERIVATION INTEGRITY

Time to top and maximum height should remain visibly linked to the turning-point condition rather than appearing as unrelated memorised formulas.

Required chain:

- `v = u - gt` with `v = 0` at the top -> `t_up = u/g`;
- `v² = u² - 2gH` with `v = 0` at the top -> `H = u²/(2g)`.

Fail if the derived results are shown without their source relation when the page is explanatory/worked/full-support.

## AD-60 SAME-LEVEL SYMMETRY GATE

The result `T = 2u/g` is conditional.

Use it only when:

- launch and landing heights are equal;
- the same constant `g` model applies throughout;
- air resistance is neglected unless the source says otherwise.

If the landing level differs from launch level, solve the actual position equation.

Fail if `T = 2u/g` is presented as a universal vertical-throw formula.

## AD-61 POWER-LAW SCALING INTEGRITY

When publishing scaling relations, keep the held-fixed parameters explicit.

For the same `g`:

- `H ∝ u²`;
- same-level `T ∝ u`.

For the same `u`:

- `H ∝ 1/g`;
- `t_up ∝ 1/g`.

Fail if a linear and quadratic scaling law are visually mixed or if the page hides which parameter is fixed.

## AD-62 TWO-ROOT PASSAGE INTEGRITY

For one fixed height below the maximum in ideal vertical motion:

- the position equation becomes a quadratic in time;
- two physical roots correspond to the upward and downward passages;
- the earlier root is the upward passage and the later root is the downward passage;
- a figure, when used, should show the same horizontal level intersecting the trajectory twice.

Fail if two roots are presented as duplicate algebraic artifacts without physical interpretation.

## AD-63 ROOT-SUM / FLIGHT-TIME LINK

For `1/2 gt² - ut + y = 0`:

- `t1 + t2 = -B/A = 2u/g`;
- the publication should state that this agrees with the total same-level flight time under the same model;
- root-sum use must preserve the actual quadratic coefficients.

Fail if the root sum is quoted without matching the published quadratic.

## AD-64 SPEED-VS-VELOCITY AT SAME HEIGHT

At the same height in the ideal model:

- the no-time relation gives the same `v²` for both passages;
- speed magnitudes are equal;
- with upward-positive coordinates, upward velocity is positive and downward velocity is negative;
- student wording must distinguish `speed` from `velocity` when the sign matters.

Fail if the page says the velocities are the same when only the speed magnitudes are the same.

## Required review sequence

1. Freeze stage boundaries, sign convention, equations, endpoints, and model conditions from source.
2. Verify every local stage carries the correct entry state.
3. For turning-point pages, verify `v = 0` and `a = -g` are both visible where needed.
4. For time/height results, trace each result back to the turning-point condition.
5. For same-level flight time, verify endpoint equality before using symmetry.
6. For repeated-height pages, verify two roots, their time ordering, and opposite velocity signs.
7. Inspect every graph/arc at normal viewing size.
8. Run general overlap, bounds, formula-completeness, and math-typography checks.
9. Record all AD-55 through AD-64 findings as zero before release.
