# Core 1B — Conceptual self-tutor

**Learner job:** predict, draw, explain and reconstruct before reveal. Each bucket closes with expected reasoning, plausible wrong-response feedback and a retry. The K50 fixture does not reduce intrinsic depth.

<a id="b01-observer-frame-axes-origin-and-common-clock"></a>
## B01 — Observer, frame, axes, origin and common clock

**Intrinsic difficulty:** Easy. **Primary scope label:** CBSE_OPTIONAL_ADVANCED.

**Question record — ID:** `C1B-B01-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Observer · **Linked:** prediction, reconstruction · **Bucket:** B01 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** entry (3/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b01-p1-reasoning](#c1b-b01-p1-reasoning)

### Predict / draw / explain
A notebook lies on a table inside a bus moving steadily east. Predict whether it is moving or at rest, but attach a frame to every statement. Then name the origin/axis/clock choices needed to compare it with a cyclist outside.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Observer, frame, axes, origin and common clock](diagrams/frames-axes-clock.svg)

<a id="c1b-b01-p1-reasoning"></a>
**Expected reasoning.** It can be at rest relative to the bus and moving east relative to ground. A comparison needs one common frame, an origin, a positive direction and a shared t=0.

### Feedback for plausible wrong responses
- “It must be either moving or at rest.” → the observer is missing.
- “Mix the bus and ground velocities directly.” → first express compared velocities in one compatible frame.

**Question record — ID:** `C1B-B01-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B01 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** entry (0/10) · **Support:** targeted feedback available · **Answer:** [c1b-b01-r1-answer](#c1b-b01-r1-answer)

### Retry
Two runners are side by side at t=0 and both move east at 4 m/s. Relative to B what is A doing? Relative to ground?

<a id="c1b-b01-r1-answer"></a>
**Retry closure.** Relative to B, A has zero velocity; relative to ground A moves east at 4 m/s.

### What to carry forward
Always attach motion to a named frame and keep axes/clock explicit.

<a id="b02-path-distance-displacement-and-average-quantities"></a>
## B02 — Path, distance, displacement and average quantities

**Intrinsic difficulty:** Medium. **Primary scope label:** CBSE_STANDARD.

**Question record — ID:** `C1B-B02-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Path · **Linked:** prediction, reconstruction · **Bucket:** B02 · **Syllabus:** CBSE_STANDARD · **Demand:** standard (5/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b02-p1-reasoning](#c1b-b02-p1-reasoning)

### Predict / draw / explain
Before calculating, predict which is larger for a 6 m east then 8 m north walk: distance or displacement magnitude. Draw both.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Path, distance, displacement and average quantities](diagrams/path-displacement.svg)

<a id="c1b-b02-p1-reasoning"></a>
**Expected reasoning.** Distance is 14 m; displacement is the diagonal, 10 m. The bend makes path length larger.

### Feedback for plausible wrong responses
- “Displacement is 14 m.” → that is path length.
- “Displacement is 8−6=2 m.” → perpendicular legs are not collinear lengths.

**Question record — ID:** `C1B-B02-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B02 · **Syllabus:** CBSE_STANDARD · **Demand:** entry (1/10) · **Support:** targeted feedback available · **Answer:** [c1b-b02-r1-answer](#c1b-b02-r1-answer)

### Retry
Walk 5 m east then 12 m north. Find distance and displacement magnitude.

<a id="c1b-b02-r1-answer"></a>
**Retry closure.** Distance 17 m; displacement magnitude 13 m.

### What to carry forward
Distance follows route; displacement follows endpoint change.

<a id="b03-coordinates-components-and-reconstructing-a-vector-visually"></a>
## B03 — Coordinates, components and reconstructing a vector visually

**Intrinsic difficulty:** Hard. **Primary scope label:** CBSE_OPTIONAL_ADVANCED.

**Question record — ID:** `C1B-B03-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Coordinates · **Linked:** prediction, reconstruction · **Bucket:** B03 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** stretch (7/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b03-p1-reasoning](#c1b-b03-p1-reasoning)

### Predict / draw / explain
Move from (2,5) to (20,−19). Predict the signs of Δx and Δy before arithmetic; then reconstruct the displacement triangle.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Coordinates, components and reconstructing a vector visually](diagrams/component-triangle.svg)

<a id="c1b-b03-p1-reasoning"></a>
**Expected reasoning.** x increases so Δx positive; y decreases so Δy negative. Components `(18,−24) m`; magnitude 30 m.

### Feedback for plausible wrong responses
- “Δy must be +24 because distance is positive.” → components are signed.
- “Use initial minus final only for y.” → subtraction order is final minus initial on every axis.

**Question record — ID:** `C1B-B03-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B03 · **Syllabus:** CBSE_OPTIONAL_ADVANCED · **Demand:** entry (2/10) · **Support:** targeted feedback available · **Answer:** [c1b-b03-r1-answer](#c1b-b03-r1-answer)

### Retry
From (−3,2) to (1,−1), find components and magnitude.

<a id="c1b-b03-r1-answer"></a>
**Retry closure.** Δx=+4 m, Δy=−3 m; magnitude 5 m.

### What to carry forward
Components are signed; magnitude is reconstructed from perpendicular legs.

<a id="b04-constant-motion-in-two-coordinates-tables-and-graphs"></a>
## B04 — Constant motion in two coordinates; tables and graphs

**Intrinsic difficulty:** Medium. **Primary scope label:** REQUESTED_ENRICHMENT.

**Question record — ID:** `C1B-B04-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Constant motion in two coordinates; tables and graphs · **Linked:** prediction, reconstruction · **Bucket:** B04 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (5/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b04-p1-reasoning](#c1b-b04-p1-reasoning)

### Predict / draw / explain
A point begins at (1,2) m with velocity (2,−1) m/s. Build a t=0,1,2,3 table and predict x(t),y(t) slope signs.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Constant motion in two coordinates; tables and graphs](diagrams/xy-time-graphs.svg)

<a id="c1b-b04-p1-reasoning"></a>
**Expected reasoning.** Positions `(1,2),(3,1),(5,0),(7,−1)`. x slope +2; y slope −1; each row uses the same t.

### Feedback for plausible wrong responses
- “Use different times because rates differ.” → one physical state shares the clock.
- “Negative slope means negative speed.” → it is a signed component.

**Question record — ID:** `C1B-B04-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B04 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** entry (1/10) · **Support:** targeted feedback available · **Answer:** [c1b-b04-r1-answer](#c1b-b04-r1-answer)

### Retry
At t=4 s, what single ordered pair describes the point, and why not mix x at 4 s with y at 3 s?

<a id="c1b-b04-r1-answer"></a>
**Retry closure.** At 4 s, `(9,−2) m`; mixing times makes a state the object never occupied.

### What to carry forward
Component calculations are separate but the event clock is shared.

<a id="b05-one-dimensional-relative-motion-units-and-signs"></a>
## B05 — One-dimensional relative motion, units and signs

**Intrinsic difficulty:** Medium. **Primary scope label:** REQUESTED_ENRICHMENT.

**Question record — ID:** `C1B-B05-P1` · **Source:** Agent-authored tutor prompt · **Primary:** One-dimensional relative motion · **Linked:** prediction, reconstruction · **Bucket:** B05 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** standard (5/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b05-p1-reasoning](#c1b-b05-p1-reasoning)

### Predict / draw / explain
East is positive. A moves east at 8 m/s, B east at 5 m/s. Predict A’s direction as seen by B and whether the relative speed is above or below 8 before subtracting.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![One-dimensional relative motion, units and signs](diagrams/relative-1d-signline.svg)

<a id="c1b-b05-p1-reasoning"></a>
**Expected reasoning.** A appears eastward to B at 3 m/s: target minus observer `8−5`.

### Feedback for plausible wrong responses
- “Add because both are speeds.” → use signed velocities.
- “B/A is also +3.” → reversing observer reverses the relative vector.

**Question record — ID:** `C1B-B05-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B05 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** entry (1/10) · **Support:** targeted feedback available · **Answer:** [c1b-b05-r1-answer](#c1b-b05-r1-answer)

### Retry
A and B both move east at 5 m/s but B begins 20 m ahead. Predict separation after 10 s.

<a id="c1b-b05-r1-answer"></a>
**Retry closure.** Still 20 m because relative velocity is zero; zero relative velocity does not imply zero gap.

### What to carry forward
Use target-minus-observer after units/signs; equal velocity preserves separation.

<a id="b06-relative-velocity-in-two-dimensions-and-observer-reversal"></a>
## B06 — Relative velocity in two dimensions and observer reversal

**Intrinsic difficulty:** Hard. **Primary scope label:** REQUESTED_ENRICHMENT.

**Question record — ID:** `C1B-B06-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Relative velocity in two dimensions and observer reversal · **Linked:** prediction, reconstruction · **Bucket:** B06 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (7/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b06-p1-reasoning](#c1b-b06-p1-reasoning)

### Predict / draw / explain
A moves east at 3 m/s; B north at 4. Stand mentally on B. Predict which horizontal and vertical directions A appears to move, then construct components.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Relative velocity in two dimensions and observer reversal](diagrams/relative-subtraction.svg)

<a id="c1b-b06-p1-reasoning"></a>
**Expected reasoning.** A gains east (+3) while B’s north motion makes A appear south (−4), so A/B=(3,−4) m/s, magnitude 5.

### Feedback for plausible wrong responses
- “A/B=(3,+4).” → observer’s +4 is subtracted.
- “Reversal changes magnitude.” → vector negation preserves length.

**Question record — ID:** `C1B-B06-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B06 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** entry (2/10) · **Support:** targeted feedback available · **Answer:** [c1b-b06-r1-answer](#c1b-b06-r1-answer)

### Retry
Write B/A and state what changes and what stays invariant.

<a id="c1b-b06-r1-answer"></a>
**Retry closure.** B/A=(−3,+4); direction/components reverse, magnitude remains 5 m/s.

### What to carry forward
Subtract matching components; observer reversal negates the whole relative vector.

<a id="b07-meeting-requires-the-same-position-at-the-same-time"></a>
## B07 — Meeting requires the same position at the same time

**Intrinsic difficulty:** Hard. **Primary scope label:** REQUESTED_ENRICHMENT.

**Question record — ID:** `C1B-B07-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Meeting requires the same position at the same time · **Linked:** prediction, reconstruction · **Bucket:** B07 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (7/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b07-p1-reasoning](#c1b-b07-p1-reasoning)

### Predict / draw / explain
A starts (0,0) with (2,1); B starts (10,0) with (0,2). Predict whether matching x alone proves meeting, then solve both coordinate conditions.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Meeting requires the same position at the same time](diagrams/collision-pair.svg)

<a id="c1b-b07-p1-reasoning"></a>
**Expected reasoning.** x gives 5 s; y gives 0 s. Different times mean no meeting.

### Feedback for plausible wrong responses
- “Meet at x match t=5.” → y coordinates differ then.
- “Any path crossing is collision.” → timing must also match.

**Question record — ID:** `C1B-B07-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B07 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** entry (2/10) · **Support:** targeted feedback available · **Answer:** [c1b-b07-r1-answer](#c1b-b07-r1-answer)

### Retry
A: (0,0)+(2,1)t. B is fixed at (6,3). Test both coordinates.

<a id="c1b-b07-r1-answer"></a>
**Retry closure.** Both give t=3 s, so meeting at (6,3) m.

### What to carry forward
Meeting requires both coordinate equalities at one same time.

<a id="b08-boatcurrent-and-rainobserver-model-transfer-ambiguity"></a>
## B08 — Boat/current and rain/observer model transfer; ambiguity

**Intrinsic difficulty:** Hard. **Primary scope label:** REQUESTED_ENRICHMENT.

**Question record — ID:** `C1B-B08-P1` · **Source:** Agent-authored tutor prompt · **Primary:** Boat/current and rain/observer model transfer; ambiguity · **Linked:** prediction, reconstruction · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (7/10) · **Support:** attempt first; reveal after attempt · **Answer:** [c1b-b08-p1-reasoning](#c1b-b08-p1-reasoning)

### Predict / draw / explain
A 60 m river flows east at 4 m/s; a boat is steered north at 3 m/s relative to water. Predict whether crossing time uses 3,4 or 5 m/s and name every frame.

**Do not reveal yet.** Write or sketch your first model before continuing.

### Reveal the representation
![Boat/current and rain/observer model transfer; ambiguity](diagrams/boat-current.svg)

<a id="c1b-b08-p1-reasoning"></a>
**Expected reasoning.** The north component 3 m/s controls width crossing. Boat/ground=(4,3), speed 5; time 20 s; drift 80 m.

### Feedback for plausible wrong responses
- “Use 5 m/s for crossing.” → resultant is not entirely across the river.
- “Current changes boat/water velocity.” → it changes boat/ground velocity.

**Question record — ID:** `C1B-B08-R1` · **Source:** Agent-authored retry · **Primary:** repair and transfer · **Linked:** same bucket; changed action · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** entry (2/10) · **Support:** targeted feedback available · **Answer:** [c1b-b08-r1-answer](#c1b-b08-r1-answer)

### Retry
Rain/ground=(0,−6), observer/ground=(8,0). Predict horizontal sign of rain/observer, then compute.

<a id="c1b-b08-r1-answer"></a>
**Retry closure.** Negative/westward: rain/observer=(−8,−6) m/s, magnitude 10.

### What to carry forward
Name every frame in a velocity chain and refuse to invent missing directions.

## Final synthesis

**Question record — ID:** `C1B-SYN-01` · **Source:** Agent-authored final synthesis · **Primary:** choose the correct motion model · **Linked:** frames, components, relative velocity, meeting, transfer · **Bucket:** B08 · **Syllabus:** REQUESTED_ENRICHMENT · **Demand:** stretch (9/10) · **Support:** no full model until attempt · **Answer:** [c1b-syn-01-answer](#c1b-syn-01-answer)

For each situation name the **first model/check**, not the full arithmetic:

1. Two walkers start 30 m apart on one signed east-west line.
2. Two drones have initial coordinate pairs and constant velocity pairs; decide collision.
3. Boat velocity is relative to water and current relative to ground.
4. A and B have speeds 5 m/s and 3 m/s but no directions.

Attempt before reading the closure.

<a id="c1b-syn-01-answer"></a>
**Synthesis closure.** (1) Choose a sign axis and use relative velocity or 1D position equations while retaining the initial gap. (2) Write x(t),y(t) for both and require both equalities at one time. (3) Use boat/ground = boat/water + water/ground and the across component for crossing time. (4) Diagnose underdetermination; directions/frame relation are missing.

Decision order: **name frame → set axes/units/clock → write components/positions → choose subtraction or meeting conditions → verify direction, units and a limiting case.**