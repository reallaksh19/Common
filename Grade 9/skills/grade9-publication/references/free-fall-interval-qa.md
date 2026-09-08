# Free-Fall Scaling and Gravity-Interval QA

Use this checkpoint set whenever a student-facing batch contains free fall from rest, height-time scaling, multiple released bodies under gravity, last-distance/final-time slices, between-point fall distances, or droplet-spacing questions.

These checks are additive to source fidelity, math typography, artifact separation, and the general Student Page QA gates.

## AD-51 FREE-FALL SCALING INTEGRITY

The proportional statements `v ∝ t` and `s ∝ t²` are not universal motion rules. Publish them only when the source/model conditions support them: true drop from rest (`u = 0`), constant near-Earth `g`, and negligible air resistance unless the source states otherwise.

Required checks:

- the page identifies the motion as free fall from rest before using the pure scaling laws;
- if downward is chosen positive, `u = 0`, `a = +g`, `v = gt`, and `s = 1/2 gt²` remain sign-consistent;
- equal time increments produce equal velocity increments under constant `g`;
- cumulative displacement grows quadratically rather than linearly;
- a worked scaling statement such as `2× time -> 2× speed -> 4× distance` agrees with the equations;
- no teacher-added visual implies that equal time intervals contain equal distances.

Fail if the publication visually or verbally generalizes the pure `1 : 4 : 9 ...` / `t²` growth to a nonzero initial velocity or changing acceleration without an explicit model change.

## AD-52 LOCAL ELAPSED TIME FOR MULTIPLE DROPS

Bodies observed at the same global instant can have different local elapsed times.

For regularly released drops or delayed-release gravity problems:

- construct or preserve one global release clock;
- assign each drop its own elapsed time before substituting into free-fall equations;
- use the same physical acceleration `g` but not automatically the same `t`;
- preserve the semantic link to common-clock/delayed-start reasoning when the source contains it;
- if positions or spacings are compared at one instant, compute each cumulative position with its own local time first.

Fail if two drops released at different instants are silently given the same elapsed time because they are observed together.

## AD-53 LAST / BETWEEN INTERVAL NO-RESET

Phrases such as `last x metres`, `during the final Δt`, `between point A and point B`, or `spacing between drops` describe an interval inside an already-running motion. A new calculation interval is not a physical restart.

Required checks:

- resolve the interval to explicit start/end times before calculation;
- default to `S(end) - S(start)` when cumulative free-fall position is available;
- or, if switching to a local kinematic stage, carry the actual entry velocity into that stage;
- never silently set `u = 0` at the start of a late interval;
- keep interval displacement distinct from total displacement from release;
- for droplet spacing, subtract the two bodies' cumulative positions at the same global instant.

Examples that must remain semantically intact:

- last `0.2 s`: `S(T) - S(T - 0.2)`;
- A-to-B interval of `2 s`: `S(T + 2) - S(T)`;
- two-drop spacing: difference of two cumulative `1/2 gt²` positions using different local times.

Fail if the learner is shown `S(0.2)` as the displacement during the last `0.2 s` of a fall, or if an interval diagram visually suggests the object restarts from zero velocity.

## AD-54 HEIGHT-TIME RADICAL AND SCALING LINKAGE

For a drop from rest, `h = 1/2 gt²` and `t = √(2h/g)` must be shown as the same model in two forms.

Check that:

- the radical is typeset as a true square root rather than source-authoring syntax such as `sqrt(...)`;
- the numerator and denominator remain visually unambiguous;
- the page links the equation to the scaling consequence `height × 4 -> time × 2`;
- the explanation that the second half of a fall takes less time than the first half does not imply a reset at the midpoint;
- any comparison is clearly about fall duration under the same `g` and rest-release condition.

Fail if a layout separates the radical from its fraction, clips the denominator, or presents a linear height-time ratio.

## Required review sequence

1. Freeze the source equations, numbers, interval wording, and model conditions.
2. Verify axis/sign convention before rendering any gravity formula.
3. Render all free-fall scaling figures and compare them against the source semantics.
4. For multiple drops, verify global release times and each local elapsed time.
5. For last/between/final-interval problems, mark start/end boundaries explicitly and verify no hidden `u = 0` reset.
6. Inspect all radicals, superscripts, proportional symbols, and time subscripts at normal student viewing size.
7. Run the general overlap/bounds/math checks.
8. Record `free_fall_scaling_findings = 0`, `local_elapsed_time_findings = 0`, `interval_no_reset_findings = 0`, and `height_time_radical_findings = 0` before release.
