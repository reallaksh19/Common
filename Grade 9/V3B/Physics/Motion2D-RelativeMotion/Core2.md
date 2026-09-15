# Core 2 — Frozen source questions with ladder hints

**Source:** `SYN-M2D-20260915-V1` · `FROZEN_FOR_TEST`. Every source item is attributed “Author-created test fixture; not an official CBSE or past-exam question.” Source wording/data stay inside immutable blocks; derived support is outside.

<a id="source-conventions"></a>
## Source conventions

Ground frame unless stated otherwise; +x east and +y north. Positions are metres and times seconds unless stated otherwise. Velocities are constant over described intervals. Collision objects are points. Simultaneous start means shared t=0. Ordered pairs are x,y components.

<a id="help-map"></a>
## Hint ladder

H1 is conceptual; H2 sets representation; H3 is near-complete route; complete answers close the loop.

<a id="q01"></a>
## Q01

**Question record — ID:** `C2-Q01` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q01 · **Primary:** distance, displacement and averages · **Linked:** components · **Bucket:** B02 · **Syllabus:** CBSE_STANDARD · **Demand:** standard (5/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q01-answer](#q01-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q01 -->
A learner walks 6 m east and then 8 m north in a total of 14 s. (a) Draw the path and displacement. (b) Find distance and displacement magnitude. (c) Find average speed. (d) Give average velocity as east/north components and its magnitude. Explain why average speed and the magnitude of average velocity differ here.
<!-- FROZEN_SOURCE_END:Q01 -->

### H1 — conceptual cue
Separate path length from start-to-finish displacement.

### H2 — representation/setup
Sketch 6 east then 8 north; use one 14 s interval for averages.

### H3 — near-complete route
Distance 6+8; displacement √(6²+8²); average-velocity components 6/14 and 8/14.

<a id="q01-answer"></a>
### Complete answer and reasoning
(a) Path: 6 m east then 8 m north; displacement is the direct start-to-finish arrow. (b) Distance 14 m; displacement magnitude 10 m. (c) Average speed 1.00 m/s. (d) Average velocity `(3/7,4/7) m/s`; magnitude `5/7≈0.714 m/s`. Distance follows the whole route; displacement uses only endpoints.

<a id="q02"></a>
## Q02

**Question record — ID:** `C2-Q02` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q02 · **Primary:** constant planar motion from data · **Linked:** components, graphs, stationary interval · **Bucket:** B04 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (7/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q02-answer](#q02-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q02 -->
A tracked object has positions shown below. It moves along a straight line at constant velocity between successive recorded points. (a) Draw its path with time labels. (b) Find the velocity components in 0–4 s and in 4–6 s. (c) Find total distance, displacement components and average velocity over 0–6 s. (d) A student says, “The object moved at 5 m/s for all 6 s.” Diagnose the claim.

| t (s) | x (m) | y (m) |
|---:|---:|---:|
| 0 | 0 | 0 |
| 2 | 6 | 8 |
| 4 | 12 | 16 |
| 6 | 12 | 16 |
<!-- FROZEN_SOURCE_END:Q02 -->

### H1 — conceptual cue
Notice motion is at 5 m/s only through 4 s, then position is unchanged.

### H2 — representation/setup
Use Δx/Δt, Δy/Δt for 0–4 and 4–6; add segment lengths for distance.

### H3 — near-complete route
0–4: Δ=(12,16) over 4 s; first two 2-s segments are 6–8–10 triangles; last length is zero.

<a id="q02-answer"></a>
### Complete answer and reasoning
(a) `(0,0)` at 0 s, `(6,8)` at 2 s, `(12,16)` at 4 s, and the 6 s label stays at `(12,16)`. (b) 0–4 s velocity `(3,4) m/s`; 4–6 s `(0,0)`. (c) Total distance 20 m, displacement `(12,16) m`, average velocity `(2,8/3) m/s`, magnitude `10/3≈3.33 m/s`. (d) The 5 m/s claim is false for all 6 s: the object stops from 4–6 s.

<a id="q03"></a>
## Q03

**Question record — ID:** `C2-Q03` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q03 · **Primary:** coordinate components · **Linked:** constant velocity, negative component · **Bucket:** B03 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** standard (4/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q03-answer](#q03-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q03 -->
At t = 0 an object is at (2, 5) m. Its velocity is (3, −4) m/s. (a) Find its position at t = 6 s. (b) Find its displacement components and distance travelled in those 6 s. (c) Sketch the starting point, ending point and velocity direction. Explain the negative component without calling speed negative.
<!-- FROZEN_SOURCE_END:Q03 -->

### H1 — conceptual cue
Use separate constant-velocity x/y equations.

### H2 — representation/setup
In 6 s, Δx=18 and Δy=−24; add to the initial point.

### H3 — near-complete route
Speed is √(3²+4²)=5 m/s; distance in 6 s is 30 m.

<a id="q03-answer"></a>
### Complete answer and reasoning
(a) Final position `(20,−19) m`. (b) Displacement `(18,−24) m`; speed 5 m/s, so straight-line distance in 6 s is 30 m. (c) Arrow points +x and −y. The −4 m/s y-component indicates direction; speed is +5 m/s.

<a id="q04"></a>
## Q04

**Question record — ID:** `C2-Q04` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q04 · **Primary:** 1D relative catch-up · **Linked:** meeting, observer reversal · **Bucket:** B05 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (4/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q04-answer](#q04-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q04 -->
At t = 0, A is at x = 0 m and B is at x = 30 m on an east–west line. A travels east at 8 m/s and B travels east at 5 m/s. (a) Find A's velocity relative to B, stating the direction. (b) When and where does A catch B? (c) What is B's velocity relative to A?
<!-- FROZEN_SOURCE_END:Q04 -->

### H1 — conceptual cue
East positive; relative velocity is target minus observer.

### H2 — representation/setup
Use v_A/B=8−5 and x_A=8t, x_B=30+5t.

### H3 — near-complete route
Solve 8t=30+5t; reverse observer with 5−8.

<a id="q04-answer"></a>
### Complete answer and reasoning
(a) `v_A/B=+3 m/s` east. (b) `8t=30+5t` gives 10 s; meeting/catch position 80 m. (c) `v_B/A=−3 m/s`, meaning 3 m/s west relative to A.

<a id="q05"></a>
## Q05

**Question record — ID:** `C2-Q05` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q05 · **Primary:** opposite-direction relative motion · **Linked:** meeting, signs · **Bucket:** B05 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (4/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q05-answer](#q05-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q05 -->
At t = 0, A is at x = 0 m travelling east at 6 m/s and B is at x = 50 m travelling west at 4 m/s. (a) Find the time and position of meeting. (b) Give the velocity of A relative to B and the velocity of B relative to A. Explain each sign.
<!-- FROZEN_SOURCE_END:Q05 -->

### H1 — conceptual cue
With east positive, west is negative.

### H2 — representation/setup
Use v_A=+6, v_B=−4; positions 6t and 50−4t.

### H3 — near-complete route
Solve 6t=50−4t; relative velocities are 6−(−4) and −4−6.

<a id="q05-answer"></a>
### Complete answer and reasoning
East positive: `v_A=+6`, `v_B=−4`. Meeting `6t=50−4t` gives 5 s at x=30 m. `v_A/B=+10 m/s`; `v_B/A=−10 m/s`. Signs follow the east-positive axis.

<a id="q06"></a>
## Q06

**Question record — ID:** `C2-Q06` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q06 · **Primary:** 2D relative velocity · **Linked:** separation, observer reversal · **Bucket:** B06 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (6/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q06-answer](#q06-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q06 -->
A and B start from the same point at t = 0. A travels east at 3 m/s; B travels north at 4 m/s. (a) Find A's velocity relative to B as components and magnitude. (b) Find their separation after 10 s. (c) Reverse the observer and explain what changes and what remains the same.
<!-- FROZEN_SOURCE_END:Q06 -->

### H1 — conceptual cue
Subtract B components from A; since they start together, relative position after 10 s is v_rel×10.

### H2 — representation/setup
A/G=(3,0), B/G=(0,4), so A/B=(3,−4).

### H3 — near-complete route
Relative position at 10 s is (30,−40); use Pythagoras and negate vector for observer reversal.

<a id="q06-answer"></a>
### Complete answer and reasoning
`v_A/B=(3,−4) m/s`, magnitude 5 m/s. After 10 s relative position `(30,−40) m`, separation 50 m. Reversal gives `v_B/A=(−3,4) m/s`; direction changes, magnitude does not.

<a id="q07"></a>
## Q07

**Question record — ID:** `C2-Q07` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q07 · **Primary:** same-position same-time meeting · **Linked:** two coordinate equations · **Bucket:** B07 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (7/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q07-answer](#q07-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q07 -->
At t = 0, A is at (0, 0) m with velocity (2, 1) m/s. B is at (10, 0) m with velocity (0, 2) m/s. Do they meet? Show the x-coordinate and y-coordinate conditions using the same time. If they meet, give that time and position.
<!-- FROZEN_SOURCE_END:Q07 -->

### H1 — conceptual cue
A meeting needs both coordinate equalities at the same time.

### H2 — representation/setup
A=(2t,t), B=(10,2t); solve x and y separately.

### H3 — near-complete route
x gives 5 s; y gives 0 s. Compare candidate times.

<a id="q07-answer"></a>
### Complete answer and reasoning
A: `(2t,t)`; B: `(10,2t)`. x equality gives 5 s, y equality 0 s; no single time satisfies both, so they do not meet.

<a id="q08"></a>
## Q08

**Question record — ID:** `C2-Q08` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q08 · **Primary:** path crossing versus collision · **Linked:** closest approach enrichment · **Bucket:** B07 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (9/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q08-answer](#q08-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q08 -->
At t = 0, A is at (0, 0) m with velocity (2, 0) m/s. B is at (6, −4) m with velocity (0, 2) m/s. (a) Do they meet? Test both coordinates. (b) Explain why crossing paths need not mean collision. (c) As labelled enrichment, find their closest separation for t ≥ 0 using a table and/or completing a square, without calculus.
<!-- FROZEN_SOURCE_END:Q08 -->

### H1 — conceptual cue
First test same-time collision; closest approach is separate enrichment.

### H2 — representation/setup
A=(2t,0), B=(6,−4+2t). For closest approach use relative components (2t−6,4−2t).

### H3 — near-complete route
d²=(2t−6)²+(4−2t)²; complete the square or tabulate around the minimum.

<a id="q08-answer"></a>
### Complete answer and reasoning
(a) x equality gives 3 s; y equality gives 2 s, so no meeting. (b) Their paths cross at `(6,0)` but B arrives at 2 s and A at 3 s. (c) **Enrichment:** `d²=8(t−2.5)²+2`, so closest separation is `√2≈1.41 m` at 2.5 s; a 2.0/2.5/3.0 s table gives 2.00/1.41/2.00 m.

<a id="q09"></a>
## Q09

**Question record — ID:** `C2-Q09` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q09 · **Primary:** boat/current frame composition · **Linked:** crossing component, Pythagoras · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (8/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q09-answer](#q09-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q09 -->
A straight river is 60 m wide, with parallel banks running east–west. Water flows east at 4 m/s relative to the ground. A boat is steered north at 3 m/s relative to the water throughout its crossing. Starting at the south bank, (a) find the boat's ground-velocity components and speed; (b) find crossing time and eastward drift; (c) find the length of its ground path. Label which velocity belongs to which frame. Ignore changes in current and launch/landing time.
<!-- FROZEN_SOURCE_END:Q09 -->

### H1 — conceptual cue
Name frames before adding; crossing time uses the north component.

### H2 — representation/setup
Boat/ground=(4,3), speed is a 3–4–5 result; time=60/3.

### H3 — near-complete route
Then drift=4×20 and ground path=5×20.

<a id="q09-answer"></a>
### Complete answer and reasoning
`v_B/W=(0,3)`, `v_W/G=(4,0)`, so `v_B/G=(4,3) m/s`, speed 5 m/s. Crossing time 60/3=20 s; east drift 80 m; ground path length 100 m.

<a id="q10"></a>
## Q10

**Question record — ID:** `C2-Q10` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q10 · **Primary:** rain/observer relative velocity · **Linked:** component subtraction · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (6/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q10-answer](#q10-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q10 -->
Rain has ground-frame velocity (0, −6) m/s. An observer travels east with ground-frame velocity (8, 0) m/s. (a) Find the rain's velocity relative to the observer as components and magnitude. (b) Draw the ground and observer-frame arrows. (c) Explain which way the rain moves horizontally relative to the observer. An exact angle is not required.
<!-- FROZEN_SOURCE_END:Q10 -->

### H1 — conceptual cue
Rain/observer = rain/ground − observer/ground.

### H2 — representation/setup
(0,−6)−(8,0)=(−8,−6); draw arrows with common axes.

### H3 — near-complete route
Use 6–8–10 for magnitude; negative x means west relative to observer.

<a id="q10-answer"></a>
### Complete answer and reasoning
`v_R/O=(0,−6)−(8,0)=(−8,−6) m/s`, magnitude 10 m/s. Ground rain points downward; observer points east; observer-frame rain points west and downward. The horizontal relative motion is west.

<a id="q11"></a>
## Q11

**Question record — ID:** `C2-Q11` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q11 · **Primary:** unit conversion and relative velocity · **Linked:** separation · **Bucket:** B05 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** entry (3/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q11-answer](#q11-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q11 -->
A cyclist travels east at 36 km/h and a walker travels east at 2 m/s. They are at the same point at t = 0. (a) Convert the cyclist's speed to m/s. (b) Find the cyclist's velocity relative to the walker. (c) Find their separation after 20 s. Include units at each step.
<!-- FROZEN_SOURCE_END:Q11 -->

### H1 — conceptual cue
Make units consistent before subtraction.

### H2 — representation/setup
36 km/h = 10 m/s; cyclist/walker = 10−2.

### H3 — near-complete route
Starting together, separation after 20 s = relative speed×time.

<a id="q11-answer"></a>
### Complete answer and reasoning
36 km/h = 10 m/s. Cyclist/walker = 8 m/s east. Separation after 20 s = 160 m.

<a id="q12"></a>
## Q12

**Question record — ID:** `C2-Q12` · **Source:** SYN-M2D-20260915-V1 — Author-created test fixture; not an official CBSE or past-exam question. · **Original:** Q12 · **Primary:** underdetermined relative motion · **Linked:** missing directions · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (5/10) · **Support:** H1/H2/H3 ladder · **Answer:** [q12-answer](#q12-answer)

**Attribution:** Author-created test fixture; not an official CBSE or past-exam question.

<!-- FROZEN_SOURCE_START:Q12 -->
A moves at 5 m/s and B moves at 3 m/s. Find the velocity of A relative to B.
<!-- FROZEN_SOURCE_END:Q12 -->

### H1 — conceptual cue
Speeds alone do not determine a velocity difference.

### H2 — representation/setup
State the missing directions/frame relation, then give explicitly conditional cases.

### H3 — near-complete route
If both east: +5−(+3); if A east and B west: +5−(−3). These are conditions, not a unique source answer.

<a id="q12-answer"></a>
### Complete answer and reasoning
The item is **underdetermined**: speeds are given but directions/frame relation are not, so no unique relative velocity exists. Conditional cases: both east → +2 m/s east; A east and B west → +8 m/s east. No unique numerical answer is justified.

## Source-quality hold

Q12 remains `SOURCE_DEFECT_UNDERDETERMINED` while its explanatory conditional answer is complete. This held source-quality status blocks any claim that every frozen item is well-posed; it does not permit deletion or silent repair.