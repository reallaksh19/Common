# Motion Source Coverage Map

## Authority and ordering

Primary authority: supplied **Motion in straight line questions** source bank, 68 questions.

Use **question number** as the stable source identifier. The printed/scanned page sequence around Q41-Q68 is not reliable.

This file proves Source -> Concept coverage for the Motion Concept Book. It does not silently correct source wording.

## Legend

- `CB1` Position, Distance and Displacement
- `CB2` Speed, Velocity and Average Motion
- `CB3` Acceleration meaning
- `CB4` `v = u + at`
- `CB5` displacement under constant acceleration
- `CB6` `v^2 = u^2 + 2as`
- `CB7` special patterns / nth second / stopping / repeated resistance
- `CB8` delayed and multi-stage motion
- `CB9` free fall / gravity as acceleration
- `CB10` vertical projection
- `CB11` two-body / release / relative motion
- `CB12` graphs

## Q1-Q10 — Distance/displacement; speed/velocity

| Q | Concept destination | Core source idea | SEE -> REALIZE -> UNDERSTAND focus |
|---:|---|---|---|
| 1 | CB1 | Zero displacement can coexist with non-zero distance | Return-to-start walk -> path vs change in position -> `distance >= |displacement|` |
| 2 | CB1 | Ratio of displacement magnitude to distance | Straight arrow vs travelled path -> displacement cannot exceed path -> bound the ratio |
| 3 | CB1 | Half-circle path versus diameter displacement | Semicircle sketch -> arc is distance, chord/diameter is displacement -> compute ratio |
| 4 | CB1 | Closed triangular path | Triangle walk -> same final point gives zero displacement -> closed-path reasoning |
| 5 | CB1 | Circular motion after more than one revolution | Circle/clock sketch -> complete turns do not alone determine displacement -> final position controls chord |
| 6 | CB2 | Distance, displacement, average speed and average velocity together | Out-and-back timeline -> two totals differ -> apply correct average definition |
| 7 | CB2 | Direct speed-distance-time relation | Light crossing known distance -> speed is distance per unit time -> unit/scale check |
| 8 | CB2 | Average speed for equal time intervals | Equal-width time boxes -> equal times weight speeds equally -> arithmetic average works here |
| 9 | CB2 | Average speed for equal distances | Equal road lengths -> slower leg takes longer -> total distance/total time, not arithmetic mean |
| 10 | CB2 | Repeated forward/backward motion | 5-forward/3-back cycle -> net progress differs from distance walked -> cycles plus final partial cycle |

## Q11-Q20 — Acceleration and special uniform-acceleration patterns

| Q | Concept destination | Core source idea | SEE -> REALIZE -> UNDERSTAND focus |
|---:|---|---|---|
| 11 | CB3, CB4 | Uniform deceleration to rest | Velocity countdown -> `stops` means `v=0` -> solve with signed acceleration |
| 12 | CB3 | Rest to 72 km/h in 20 s | Start/end speed table -> acceleration is velocity change per second -> convert units and divide by time |
| 13 | CB5, CB7 | First 2 s versus next 2 s from rest | 0-2 and 2-4 time boxes -> equal time does not mean equal distance -> cumulative subtraction / `t^2` scaling |
| 14 | CB3 | Rest to 36 km/h in 10 s | Start/end comparison -> same acceleration meaning -> `a=(v-u)/t` |
| 15 | CB6, CB7 | Stopping-distance ratio for speeds `U` and `4U` | Two cars, same braking -> speed factor is squared in stopping distance -> `s_stop proportional to u^2` |
| 16 | CB7 | Distance in the 11th second | Highlight only 10-11 s -> nth second is an interval -> `S(11)-S(10)` then shortcut |
| 17 | CB7 | Successive equal-time distances from rest | Total distances 1,4,9... -> differences 1,3,5... -> first differences of a quadratic |
| 18 | CB6, CB7 | Bullet through identical planks | Equal-width slabs -> constant retardation over equal distances changes `v^2` equally -> use `v^2-u^2` relation |
| 19 | CB8 | Same acceleration with delayed start | Two offset timelines -> first object has extra acceleration time -> common clock plus `s proportional to t^2` from rest |
| 20 | CB5, CB7 | Distance in one interval versus next interval | Cumulative timeline -> interval distance is difference of totals -> subtraction before shortcut |

## Q21-Q34 — Equation construction, intervals, direction and acceleration

| Q | Concept destination | Core source idea | SEE -> REALIZE -> UNDERSTAND focus |
|---:|---|---|---|
| 21 | CB6, CB7 | Penetration after losing half speed | Mark first penetration length -> half velocity does not imply half distance -> `v^2` varies linearly with distance for constant `a` |
| 22 | CB4, CB8 | Velocity several seconds before a known event | Timeline with point A -> translate "4 s before" into an earlier time -> linear `v(t)` |
| 23 | CB5 | Average velocity from final velocity and acceleration | Velocity endpoints -> uniform acceleration gives midpoint average -> use `u=v-at`, then `(u+v)/2` |
| 24 | CB5 | Acceleration from displacement function | Compare `S=10t+5t^2` term-by-term -> coefficient of `t^2` encodes `a/2` -> identify acceleration |
| 25 | CB6, CB8 | Two approaching cars both brake to rest | Two stopping sketches -> solve each stopping distance before comparing separation -> spatial bookkeeping |
| 26 | CB5 | Initial velocity from displacement function | Compare polynomial with kinematics form -> coefficient of `t` is `u` -> model identification |
| 27 | CB7 | Consecutive equal-interval distances 30 m and 50 m | Adjacent time boxes -> interval-distance difference encodes acceleration -> derive rather than pattern-match |
| 28 | CB3, CB12 | Velocity law `v=4t` | Table/straight line -> coefficient is change in velocity per second -> slope of `v-t` is acceleration |
| 29 | CB3, CB4 | Returns to start with same speed along same line | `+v` arrow becomes `-v` arrow -> same speed is not same velocity -> `Delta v=-2v`; constant-`a` assumption is a source QA flag |
| 30 | CB3 | Constant speed on semicircle but non-zero average acceleration | Velocity arrows at opposite ends -> direction change changes velocity -> average acceleration from vector change |
| 31 | CB3 | Average acceleration from measured speeds | 4.1 to 6.9 m/s -> acceleration is rate of velocity change -> direct calculation |
| 32 | CB7 | Successive equal-duration distances from rest | Square-number totals -> odd-number interval distances -> nth-second structure |
| 33 | CB5, CB8 | Given velocity change, acceleration, average velocity | Velocity interval -> first obtain time from `Delta v/a` -> displacement from average velocity times time |
| 34 | CB7 | nth-second distance versus total distance in n seconds | One highlighted interval inside 0-n -> interval and cumulative quantities differ -> derive ratio from formulas |

## Q35-Q44 — Gravity and free fall

| Q | Concept destination | Core source idea | SEE -> REALIZE -> UNDERSTAND focus |
|---:|---|---|---|
| 35 | CB9 | Same window crossed from different release heights | Falling from higher point gives greater entry speed -> crossing time changes -> stage motion under gravity |
| 36 | CB10 | Same maximum height on Earth/Moon | Same height under different `g` -> smaller gravity needs smaller launch speed -> `H=u^2/(2g)` scaling |
| 37 | CB10 | Same height reached at times `t1`, `t2` | Up/down branches crossing same height line -> one position can occur twice -> quadratic roots / symmetry |
| 38 | CB10 | Highest-point misconception | Throw chalk upward -> velocity is momentarily zero while gravity persists -> `v=0`, `a=-g` |
| 39 | CB11 | One body dropped, one projected downward | Two side-by-side bodies -> both gain same gravitational velocity change -> relative acceleration cancels |
| 40 | CB9, CB5 | Average velocity during free fall | Velocity ramp 0 to `gt` -> uniform change gives midpoint average -> `v_avg=gt/2` |
| 41 | CB9, CB11 | Two masses dropped with resistance proportional to mass | Compare force per mass -> mass can cancel in acceleration contribution -> reason from `F/m`, not force magnitude alone |
| 42 | CB9 | Acquired velocity numerically equals displacement | Build `v(t)` and `s(t)` together -> linear vs quadratic time dependence -> solve simultaneous relation |
| 43 | CB9 | Tower height from 4 s free fall | Four time blocks -> distance grows as `t^2` -> `h=1/2 gt^2` |
| 44 | CB9, CB7 | Last 6 m takes 0.2 s | Highlight final 0.2 s only -> last-distance is an interval -> `S(T)-S(T-0.2)` |

## Q45-Q56 — Vertical projection, towers, scaling and release

| Q | Concept destination | Core source idea | SEE -> REALIZE -> UNDERSTAND focus |
|---:|---|---|---|
| 45 | CB10 | Time to highest point | Upward velocity countdown under gravity -> gravity removes `g` m/s each second -> set `v=0` in `v=u-gt` |
| 46 | CB10, CB11 | Same speed launched upward/downward from tower | Opposite initial arrows -> path/time differ but `u^2` is same in final-speed relation -> compare final speed magnitudes |
| 47 | CB10, CB11 | Time gap for upward/downward launches | Two timelines -> upward case spends extra up-and-return time -> extra `2u/g` |
| 48 | CB10 | Flight time proportional to initial velocity | Symmetric same-level trajectory -> up time `u/g`, total `2u/g` -> direct proportionality |
| 49 | CB10 | Same launch speed on Earth/Moon | Two gravity strengths -> smaller `g` gives larger height -> `H proportional to 1/g`; source must supply/establish gravity ratio |
| 50 | CB10 | Doubling launch speed and maximum height | Height bars for `u` and `2u` -> speed enters squared -> height becomes four times |
| 51 | CB11 | Dropped body and upward-projected body meet | Two-body sketch -> both share gravity -> relative motion can simplify meeting condition |
| 52 | CB11 | Stone released from accelerating balloon | Balloon + release arrow -> released object inherits carrier velocity -> source numeric stem requires scan verification |
| 53 | CB9 | Fall-time ratio from heights `a` and `b` | Two towers -> `t=sqrt(2h/g)` -> time scales with square root of height |
| 54 | CB10, CB11 | One ball initially upward, one downward from same building | Equal `|u|`, same height -> final-speed relation contains `u^2` -> same final speed magnitude under ideal model |
| 55 | CB10 | Required launch speed for double height | Compare `h` and `2h` -> invert `H proportional to u^2` -> speed scales as square root of height |
| 56 | CB9 | Impact velocity after 5 s free fall | Five time boxes -> gravity adds velocity uniformly -> `v=gt` from rest |

## Q57-Q68 — Vertical-motion reasoning and graphs

| Q | Concept destination | Core source idea | SEE -> REALIZE -> UNDERSTAND focus |
|---:|---|---|---|
| 57 | CB10 | Height remaining when speed is `u/2` | Mark trajectory and current speed -> speed fraction does not map linearly to height fraction -> use squared-velocity relation |
| 58 | CB10 | Double launch speed with different mass | Cross out mass; compare velocity arrows -> ideal vertical height independent of mass -> `H proportional to u^2` |
| 59 | CB9, CB7 | Successive free-fall distances | 1st/2nd/3rd second boxes -> gravity is constant acceleration from rest -> `1:3:5:...` reappears |
| 60 | CB9 | Height from 3 s fall | Three time blocks -> same free-fall displacement law -> `h=1/2 gt^2` |
| 61 | CB10 | Upward throw from bridge ending below start | Coordinate axis through bridge -> upward `u` and negative displacement can coexist -> signed `y=ut-1/2 gt^2` |
| 62 | CB11 | Bombs released from ascending balloons at `v,2v,3v` | Three balloons with inherited upward arrows -> "dropped" from moving carrier does not mean ground-frame `u=0` -> release velocity matters |
| 63 | CB12 | Meaning of slopes and areas | Draw `x-t` and `v-t` together -> graph geometry maps to physical quantities -> slope/area relationships |
| 64 | CB12, CB10 | `v-t` graph for vertical projection | Upward throw + velocity line falling through zero -> `v=u-gt` is linear with slope `-g` |
| 65 | CB12, CB6 | Velocity-displacement relation in free fall | Plot data from `v^2=2gs` -> velocity is not linear in displacement -> teach invariant relation before curve-name claim |
| 66 | CB12, CB10 | Displacement-time graph for vertical projection | Position rises, flattens, falls -> constant acceleration gives quadratic position -> parabola |
| 67 | CB12 | Curve impossible for 1-D motion vs time | Vertical-line test -> one particle cannot occupy several positions at same time -> single-valuedness |
| 68 | CB12 | Impossible `v-t` graph | Candidate graphs -> one particle cannot have several velocities at one instant -> physical/function consistency |

## Coverage status

- Source questions mapped: **68 / 68**
- Orphan source questions: **0**
- Concept blocks represented: **CB1-CB12**, with CB0 as an enabling pre-unit

## Preserved source QA flags

1. **Q29** — expected solution appears to require constant/uniform acceleration; do not silently insert that into a quoted source stem.
2. **Q49** — Earth/Moon gravity ratio must be supplied or established for a self-contained result.
3. **Q52** — part of the scan is obscured; exact numeric reproduction requires verification.
4. **Q65** — graph curve naming depends on axis assignment; teach `v^2 proportional to s` first.
5. Printed/scanned page order around Q41-Q68 is not used as authority; question number is authoritative.

## Publication gate

A regenerated Concept Book must fail QA if any source question loses its destination or if a major equation is present without a SEE -> REALIZE -> UNDERSTAND explanation.
