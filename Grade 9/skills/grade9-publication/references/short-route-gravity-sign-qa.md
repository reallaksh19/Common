# Short-Route and Gravity-Sign QA

Use this checkpoint set whenever a student-facing batch uses compressed definition-based motion routes (for example, velocity change + acceleration + average velocity) or introduces gravity through sign conventions.

## AD-46 SAME-INTERVAL ALIGNMENT

Before using a compact relation chain such as

`time = velocity change / acceleration`

followed by

`displacement = average velocity x time`,

verify that every quantity belongs to the same physical interval.

Pass only if:

- `Δv` is measured over the interval being solved;
- the acceleration belongs to that same interval and is constant when `t = Δv/a` is used;
- the average velocity belongs to that same interval;
- if the data cross stage boundaries, the page explicitly splits the motion before applying the route;
- units confirm the intended meanings.

Fail if a learner could combine a velocity change from one stage with an average velocity from another stage simply because the symbols fit algebraically.

## AD-47 DEFINITION-CHAIN INTEGRITY

When a source intentionally uses a compact definitions-first route, preserve the causal chain rather than showing two disconnected formulas.

Required visual logic:

`velocity change + rate of change -> elapsed time -> average velocity + elapsed time -> displacement`

Check that:

- the operative relations are visible on full-support or worked pages;
- the first result feeds the second relation;
- unnecessary endpoint variables are not invented when the source explicitly avoids them;
- a familiar UVATS/SUVAT template is not presented as mandatory when the source teaches model economy;
- any later reconstruction of `u` and `v` occurs only after the interval has been decoded, if the task actually needs those endpoints.

Fail if the publication replaces the source’s reasoning with generic formula hunting.

## AD-48 AXIS-BEFORE-SIGN COMMITMENT

For vertical-motion/gravity pages, the positive axis must be established before signed values of `u`, `v`, displacement, or acceleration are assigned.

Check that:

1. the positive direction is visible or stated;
2. gravity is shown physically downward;
3. acceleration is then written as `+g` or `-g` according to the chosen axis;
4. velocity/displacement signs use the same axis consistently;
5. the sign convention does not silently change mid-example.

Fail if a page writes `a = -g` without first making the chosen positive direction recoverable to the learner.

## AD-49 MAGNITUDE / DIRECTION / SIGN SEPARATION

Keep these three ideas distinct:

- magnitude of gravitational acceleration: approximately `9.8 m/s²` near Earth’s surface;
- physical direction: downward;
- algebraic sign: determined by the chosen coordinate axis.

Do not phrase `-g` as weaker gravity or as a negative physical magnitude. If the source includes that misconception, present it explicitly as a wrong idea and repair it.

A strong student page should allow the learner to say:

> `g` is a positive magnitude, gravity points downward, and `a` may be `+g` or `-g` depending on my axis.

## AD-50 GRAVITY EQUATION-FAMILY CONSISTENCY

Gravity is not a separate formula family. Verify that every gravity equation shown is a consistent substitution into the already-approved constant-acceleration model.

For an upward-positive axis, the standard source relations should remain semantically equivalent to:

- `v = u - gt`
- `y = ut - 1/2 gt²`
- `v² = u² - 2gy`

For a downward-positive axis, sign changes must follow the same coordinate choice consistently.

Check that:

- `a = ±g` is the bridge from the constant-acceleration equation family;
- `y`, `u`, `v`, and `a` all use one axis convention;
- the publication does not mix upward-positive displacement with downward-positive acceleration notation;
- the near-Earth / negligible-air-resistance model gate is preserved when present in the source;
- magnitude `g` itself is not assigned a negative value.

Fail if visually polished equations cannot be traced back to one coherent coordinate convention.

## Required review sequence

1. Render every affected page.
2. Verify the physical interval highlighted by each compact route.
3. Trace each definition-chain result into the next line.
4. Check that axes are visible before signed gravity quantities are introduced.
5. Read each `+g/-g` statement as a student: confirm direction, magnitude, and sign cannot be confused.
6. Verify each gravity equation against the selected axis.
7. Record zero findings for AD-46 through AD-50 before release.
