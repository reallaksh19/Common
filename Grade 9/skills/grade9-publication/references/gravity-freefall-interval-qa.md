# Gravity, Free-Fall, and Late-Interval QA

Use this checkpoint set whenever a student-facing batch contains free fall, gravity scaling, multiple releases, last-distance intervals, between-point intervals, or droplet-spacing problems.

## AD-51 FREE-FALL SCALING INTEGRITY

For a true drop from rest under constant near-Earth gravity, preserve the distinct growth laws:

- `v = gt` so velocity magnitude grows linearly with elapsed time;
- `s = 1/2 gt^2` so cumulative displacement grows quadratically with elapsed time;
- `t = sqrt(2h/g)` so fall time scales with the square root of height.

Fail if a page visually or verbally implies:

- distance is proportional to time for accelerated free fall;
- doubling fall time only doubles displacement;
- multiplying height by four multiplies fall time by four;
- a scaling diagram uses geometry inconsistent with the stated square or square-root law.

If a support diagram shows equal-time snapshots, the displacement gaps must increase consistently with the quadratic model when quantitative positions are shown.

## AD-52 MULTI-DROP LOCAL-TIME INTEGRITY

When several drops are released at different global times, the same observation instant does not give them the same elapsed time.

Check that:

- one global clock locates the observation event;
- each drop gets its own local elapsed time;
- every drop still uses the same free-fall law with its own `t_i`;
- the publication does not silently reuse the oldest drop's time for later drops;
- common-clock logic and free-fall physics remain conceptually separate but visibly linked.

Fail if two differently released drops are assigned the same elapsed time without source support.

## AD-53 GRAVITY INTERVAL-BOUNDARY INTEGRITY

Words such as `last`, `between`, `during the final`, and `spacing between` must be translated into explicit start and end instants before a formula is applied.

Examples:

- last `Δt` before impact: `T-Δt -> T`;
- between A and B: `T_A -> T_B`;
- a 2 s interval beginning at `T`: `T -> T+2`.

For cumulative free-fall position `S(t)`, the default interval model is:

`interval displacement = S(end) - S(start)`.

Fail if the final interval is treated as if it begins at release.

## AD-54 NO FALSE MID-FALL RESET

A new calculation interval is not automatically a new physical motion stage.

Do not set `u = 0` at the start of a late interval unless the source explicitly states that the body stops or restarts there.

Two safe routes are allowed:

1. cumulative subtraction: `S(end) - S(start)`;
2. local-stage calculation using the actual velocity at interval start as the new initial velocity.

Fail if:

- `u=0` is silently reintroduced mid-fall;
- the learner is told to use a local-stage equation without carrying the inherited entry velocity;
- a diagram visually suggests a restart at the interval boundary.

## AD-55 CUMULATIVE / LOCAL-ROUTE EQUIVALENCE

When both cumulative subtraction and a local-stage route are shown, they must describe the same physical interval and be mathematically consistent.

Audit:

- identical start and end instants;
- identical gravity sign convention;
- correct inherited velocity for the local route;
- same resulting interval displacement.

Fail if the two routes mix different clocks, different sign conventions, or different physical start states.

## Release sequence

1. identify all free-fall scaling claims;
2. verify `v ~ t`, `s ~ t^2`, and `t ~ sqrt(h)` relationships where applicable;
3. inspect every multi-drop timeline for distinct local elapsed times;
4. inspect every `last/between/final/spacing` problem for explicit interval boundaries;
5. verify no silent `u=0` reset appears mid-fall;
6. compare cumulative and local-stage routes when both are present;
7. render and inspect at normal student viewing size;
8. release only when all AD-51 through AD-55 findings are zero.
