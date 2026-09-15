# Core 1A — Detailed declarative teaching

**Learner job:** build understanding through explicit explanations, worked examples, diagrams, misconception repair and answered checkpoints. The K50 fixture does not reduce intrinsic bucket depth.

## Two bridges before the hard reasoning

**Right-triangle bridge.** Perpendicular horizontal and vertical changes are the legs of a right triangle. Their resultant magnitude is `√(a²+b²)`; no trigonometry is needed.

**Two-equation bridge.** In a plane a location has x and y coordinates. A collision is one physical event, so both coordinate equalities must use the same elapsed time. Solve one equality, then test that same time in the other.

<a id="b01-observer-frame-axes-origin-and-common-clock"></a>
## B01 — Observer, frame, axes, origin and common clock

**Intrinsic difficulty:** Easy. **Primary scope label:** CBSE_OPTIONAL_ADVANCED.

### Why a frame is part of the measurement
A bare statement such as “the bag moves at 8 m/s” is incomplete until a reference frame is named. A passenger can see the bag at rest in the bus frame while a person on the pavement sees it move east in the ground frame. The object is the same; the coordinate description changes.

A usable setup names four things: **frame/observer**, **origin**, **axis signs**, and **clock origin**. Simultaneous comparisons require one shared `t=0`.

![Frame setup](diagrams/frames-axes-clock.svg)

### Worked example
A bus moves east at 10 m/s relative to ground. A notebook stays fixed on a seat. In the ground frame its velocity is `+10 m/s`; in the bus frame it is `0 m/s`. If west were chosen positive, the same ground motion would be `−10 m/s`. The sign changed because the axis changed, not because the motion changed.

### Misconception repair
**Wrong:** “Zero velocity means stationary everywhere.” **Repair:** zero velocity is frame-relative. It can be zero relative to the bus and nonzero relative to ground.

**Question record — ID:** `C1A-Q01` · **Source:** Agent-authored checkpoint · **Primary:** frame and shared clock · **Linked:** axes, origin · **Bucket:** B01 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** entry (2/10) · **Support:** worked teaching available · **Answer:** [c1a-q01-answer](#c1a-q01-answer)

### Checkpoint
A suitcase is fixed in a train moving past a platform. Give two compatible frame-dependent velocity statements.

<a id="c1a-q01-answer"></a>
**Worked answer.** It can have zero velocity relative to the train and nonzero train velocity relative to the ground.

<a id="b02-path-distance-displacement-and-average-quantities"></a>
## B02 — Path, distance, displacement and average quantities

**Intrinsic difficulty:** Medium. **Primary scope label:** CBSE_STANDARD.

### Path and endpoint change answer different questions
**Distance** is accumulated path length. **Displacement** is the single start-to-finish change. Standard Science explicitly distinguishes distance/displacement and speed/velocity; the right-angled two-dimensional example here is an extension of that foundation.

![Path versus displacement](diagrams/path-displacement.svg)

### Worked example: 6 east then 8 north in 14 s
Distance `=6+8=14 m`. Displacement components are `(6,8) m`; Pythagoras gives magnitude `10 m`. Average speed `=14/14=1.00 m/s`. Average-velocity components are `(6/14,8/14)=(3/7,4/7) m/s`, magnitude `10/14=5/7≈0.714 m/s`.

Average speed is larger because it remembers the bent route; average velocity remembers only the net endpoint change.

### Misconception repair
**Wrong:** “Displacement is distance with a direction.” **Repair:** their magnitudes can differ because distance uses the entire path while displacement uses only endpoints.

**Question record — ID:** `C1A-Q02` · **Source:** Agent-authored checkpoint · **Primary:** distance/displacement averages · **Linked:** Pythagoras · **Bucket:** B02 · **Syllabus:** CBSE_STANDARD · **Demand:** standard (5/10) · **Support:** worked teaching available · **Answer:** [c1a-q02-answer](#c1a-q02-answer)

### Checkpoint
Walk 5 m east then 12 m north in 17 s. Find distance, displacement magnitude, average speed and average-velocity magnitude.

<a id="c1a-q02-answer"></a>
**Worked answer.** Distance 17 m; displacement 13 m; average speed 1 m/s; average-velocity magnitude 13/17≈0.765 m/s.

<a id="b03-coordinates-components-and-reconstructing-a-vector-visually"></a>
## B03 — Coordinates, components and reconstructing a vector visually

**Intrinsic difficulty:** Hard. **Primary scope label:** CBSE_OPTIONAL_ADVANCED.

### Coordinates become signed changes
For a move from `(x_i,y_i)` to `(x_f,y_f)`, always use final minus initial: `Δx=x_f−x_i`, `Δy=y_f−y_i`. A negative component says the change points opposite the positive axis; speed does not become negative.

![Component reconstruction](diagrams/component-triangle.svg)

### Worked example
From `(2,5) m` to `(20,−19) m`: `Δx=+18 m`, `Δy=−24 m`. These are perpendicular component legs, so displacement magnitude is `√(18²+24²)=30 m`.

Now give the object constant velocity `(3,−4) m/s` for 6 s from `(2,5) m`. The component changes are `(18,−24) m`, final point `(20,−19) m`; speed is `√(3²+4²)=5 m/s`; straight-line distance in 6 s is 30 m.

### Representation check
The ordered pair `(18,−24)` and the diagonal arrow are two representations of the same displacement. The negative y sign records direction; the triangle uses leg **lengths** 18 and 24.

### Misconception repair
**Wrong:** “−4 m/s is a negative speed.” **Repair:** it is a signed y-component; the speed is the nonnegative magnitude 5 m/s.

**Question record — ID:** `C1A-Q03` · **Source:** Agent-authored checkpoint · **Primary:** coordinate changes · **Linked:** negative components, magnitude · **Bucket:** B03 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** standard (5/10) · **Support:** worked teaching available · **Answer:** [c1a-q03-answer](#c1a-q03-answer)

### Checkpoint
Move from (−1,4) m to (5,−4) m. Find displacement components and magnitude.

<a id="c1a-q03-answer"></a>
**Worked answer.** Δx=+6 m, Δy=−8 m, magnitude 10 m.

<a id="b04-constant-motion-in-two-coordinates-tables-and-graphs"></a>
## B04 — Constant motion in two coordinates; tables and graphs

**Intrinsic difficulty:** Medium. **Primary scope label:** REQUESTED_ENRICHMENT.

### Separate component equations, one event clock
For constant planar velocity, `x=x0+v_x t` and `y=y0+v_y t`. The equations can be calculated separately, but a physical state uses one common time.

![Time-labelled path](diagrams/time-labelled-path.svg)

For Q02, the first four seconds change by `(12,16) m`, giving `(v_x,v_y)=(3,4) m/s`. From 4 to 6 s neither coordinate changes, so velocity is `(0,0)`.

![Shared coordinate-time graphs](diagrams/xy-time-graphs.svg)

Both graphs put time on the horizontal axis. Their slopes are +3 and +4 m/s until 4 s, then both are flat. A straight geometric path does not imply the object kept moving for all six seconds.

### Worked table
For start `(1,−2) m` and velocity `(2,1) m/s`, positions at 0,2,4 s are `(1,−2)`, `(5,0)`, `(9,2)`. Both coordinates used the same row time.

### Misconception repair
**Wrong:** “x and y have different rates, so use different times.” **Repair:** rates differ, but coordinates of one event share a clock.

**Question record — ID:** `C1A-Q04` · **Source:** Agent-authored checkpoint · **Primary:** constant planar equations · **Linked:** graphs, shared time · **Bucket:** B04 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (5/10) · **Support:** worked teaching available · **Answer:** [c1a-q04-answer](#c1a-q04-answer)

### Checkpoint
Start at (−2,3) m with velocity (4,−1) m/s. Give position at 5 s and graph slopes.

<a id="c1a-q04-answer"></a>
**Worked answer.** Position `(18,−2) m`; x slope +4 m/s, y slope −1 m/s.

<a id="b05-one-dimensional-relative-motion-units-and-signs"></a>
## B05 — One-dimensional relative motion, units and signs

**Intrinsic difficulty:** Medium. **Primary scope label:** REQUESTED_ENRICHMENT.

### Relative velocity in one dimension
Choose a positive axis, write signed velocities in one frame, reconcile units, then use `v_A/B=v_A/G−v_B/G`: **target minus observer**.

![Relative sign line](diagrams/relative-1d-signline.svg)

### Worked catch-up
A starts at 0 m at `+8 m/s`; B starts 30 m ahead at `+5 m/s`. `v_A/B=+3 m/s`, so the 30 m gap closes in `30/3=10 s`. A is then at 80 m; B is also at `30+5×10=80 m`. Reversing observer gives `v_B/A=−3 m/s`.

### Unit bridge
`36 km/h = 36×1000/3600 = 10 m/s`. Only after conversion can a walker at 2 m/s be subtracted, giving 8 m/s relative speed in the same direction.

### Equal-velocity case
If A and B both move east at 5 m/s, `v_A/B=0`. If B starts 20 m ahead, the 20 m separation remains. Zero relative velocity means no **change** in relative position, not zero relative position.

### Misconception repair
**Wrong:** “Relative speed always adds.” **Repair:** signed direction controls whether the subtraction produces a difference or a sum in magnitude.

**Question record — ID:** `C1A-Q05` · **Source:** Agent-authored checkpoint · **Primary:** 1D relative velocity · **Linked:** unit conversion · **Bucket:** B05 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (5/10) · **Support:** worked teaching available · **Answer:** [c1a-q05-answer](#c1a-q05-answer)

### Checkpoint
A scooter moves east at 18 km/h and walker east at 1 m/s. Find scooter/walker.

<a id="c1a-q05-answer"></a>
**Worked answer.** 18 km/h=5 m/s; relative velocity=+4 m/s east.

<a id="b06-relative-velocity-in-two-dimensions-and-observer-reversal"></a>
## B06 — Relative velocity in two dimensions and observer reversal

**Intrinsic difficulty:** Hard. **Primary scope label:** REQUESTED_ENRICHMENT.

### Two-dimensional subtraction is still target minus observer
Write both ground velocities in the same axes, then subtract corresponding components: `v_A/B=(v_Ax−v_Bx, v_Ay−v_By)`.

A east at 3 m/s has `(3,0)`; B north at 4 m/s has `(0,4)`. Thus `v_A/B=(3,−4) m/s`, magnitude 5 m/s.

![Relative subtraction](diagrams/relative-subtraction.svg)

### Observer reversal
`v_B/A=(−3,+4) m/s = −v_A/B`. Both components reverse; magnitude remains 5 m/s.

### Relative position uses the same order
`r_A/B=r_A/G−r_B/G`. If A and B start together, after 10 s their positions are `(30,0)` and `(0,40)`, so A from B is `(30,−40)` and separation is 50 m. If they start apart, keep the initial relative position; a shared `t=0` does not erase the gap.

### Misconception repair
**Wrong:** “Reverse observer, change only the verbal direction.” **Repair:** the entire vector is negated component by component.

**Question record — ID:** `C1A-Q06` · **Source:** Agent-authored checkpoint · **Primary:** observer reversal in 2D · **Linked:** relative position · **Bucket:** B06 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (6/10) · **Support:** worked teaching available · **Answer:** [c1a-q06-answer](#c1a-q06-answer)

### Checkpoint
A has (−2,3) m/s and B (1,−1) m/s. Find A/B and B/A and compare magnitudes.

<a id="c1a-q06-answer"></a>
**Worked answer.** A/B=(−3,4), B/A=(3,−4) m/s; both magnitudes 5 m/s.

<a id="b07-meeting-requires-the-same-position-at-the-same-time"></a>
## B07 — Meeting requires the same position at the same time

**Intrinsic difficulty:** Hard. **Primary scope label:** REQUESTED_ENRICHMENT.

### Meeting is a same-time position equality
For point objects, require `x_A(t)=x_B(t)` **and** `y_A(t)=y_B(t)` for one same admissible `t`.

![Collision versus path crossing](diagrams/collision-pair.svg)

### Worked non-meeting case
A: `(0,0)+(2,1)t`; B: `(10,0)+(0,2)t`. The x equation gives `t=5 s`; the y equation gives `t=0 s`. Because the candidate times differ, there is no meeting. At 5 s their positions are `(10,5)` and `(10,10)`.

### Positive control
A: `(0,0)+(2,1)t`; B fixed at `(6,3)`. x gives `t=3 s`; y also gives `t=3 s`; both are at `(6,3) m`. The method can therefore correctly say **yes** when both constraints close.

### Path intersection is not enough
A path records places visited; it does not automatically record arrival times. If A reaches a crossing at 3 s and B at 2 s, no collision occurs.

### Misconception repair
**Wrong:** “The lines cross, so collision.” **Repair:** collision is a spacetime event: same position and same time.

**Question record — ID:** `C1A-Q07` · **Source:** Agent-authored checkpoint · **Primary:** 2D meeting test · **Linked:** same time · **Bucket:** B07 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (7/10) · **Support:** worked teaching available · **Answer:** [c1a-q07-answer](#c1a-q07-answer)

### Checkpoint
A starts (0,0) with (1,2); B starts (6,3) with (−1,1) m/s. Do they meet?

<a id="c1a-q07-answer"></a>
**Worked answer.** x: t=6−t gives 3 s; y: 2t=3+t also 3 s. Meet at (3,6) m.

<a id="b08-boatcurrent-and-rainobserver-model-transfer-ambiguity"></a>
## B08 — Boat/current and rain/observer model transfer; ambiguity

**Intrinsic difficulty:** Hard. **Primary scope label:** REQUESTED_ENRICHMENT.

### Boat/current: name every frame
`v_B/G=v_B/W+v_W/G`. For boat/water `(0,3) m/s` north and water/ground `(4,0) m/s` east, boat/ground is `(4,3) m/s`, speed 5 m/s.

![Boat/current](diagrams/boat-current.svg)

For a 60 m width, crossing time is `60/3=20 s` because only the north component reduces the remaining width. East drift is `4×20=80 m`; ground path is `5×20=100 m`.

### Rain/observer is the same frame logic
Rain/ground `(0,−6)`, observer/ground `(8,0)`: `v_R/O=(−8,−6) m/s`, magnitude 10 m/s.

![Rain/observer](diagrams/rain-observer.svg)

The apparent westward component comes from subtracting the observer's eastward motion.

### Scientific ambiguity
“A moves at 5 m/s and B at 3 m/s” gives only speeds. If both east, A/B is +2 m/s; if A east and B west, it is +8 m/s. Without directions there is no unique relative velocity.

### Labelled enrichment: closest approach without calculus
For Q08, A from B has relative position `(2t−6,4−2t)`. Then `d²=(2t−6)²+(4−2t)²=8(t−2.5)²+2`. The square is smallest at `t=2.5 s`, so closest separation is `√2≈1.41 m`. A table at 2.0,2.5,3.0 s gives 2.00,1.41,2.00 m and confirms the minimum.

### Misconception repair
**Wrong:** “Familiar speeds guarantee one familiar relative speed.” **Repair:** relative velocity is a vector; direction and frame information are essential.

**Question record — ID:** `C1A-Q08` · **Source:** Agent-authored checkpoint · **Primary:** frame-chain transfer · **Linked:** crossing component, ambiguity · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (8/10) · **Support:** worked teaching available · **Answer:** [c1a-q08-answer](#c1a-q08-answer)

### Checkpoint
A 40 m river: boat/water 4 m/s north, water/ground 3 m/s east. Find crossing time, drift, ground speed.

<a id="c1a-q08-answer"></a>
**Worked answer.** Ground velocity (3,4), speed 5 m/s; time 10 s; drift 30 m.

## Teaching-source notes

- CBSE Standard Science 2026–27 Motion p.14 supports the straight-line distance/displacement, speed/velocity and graph foundation.
- CBSE Optional Advanced Science Ch 2 §§2.1–2.4 supports reference frames and graphical vector work.
- OpenStax University Physics §§4.1 and 4.5 informed coordinate/component and relative-motion representation choices.
- OpenStax Physics §2.3 informed coordinate-time graph conventions.
- NIST SI definitions support metre/second unit discipline.

These sources improve scientific explanation; they do not convert requested enrichment into Standard examination scope.