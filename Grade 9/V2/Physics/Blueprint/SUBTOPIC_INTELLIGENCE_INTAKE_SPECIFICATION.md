# Physics V2 — Subtopic Intelligence Library (SIL) Intake Specification

> **CANONICAL SUBORDINATE MODULE**: Part of the Physics V2 Canonical Architecture.
> **Governing Root**: [`CANONICAL_ARCHITECTURE.md`](CANONICAL_ARCHITECTURE.md)
> **Subject**: `PHYSICS` only.
> **Scope**: Grades 9, 10, and 11 across CBSE Board, NSEP Olympiad, JEE Main, and JEE Advanced.

---

## 1. Pedagogical Scope & Objectives

The Subtopic Intelligence Library (SIL) establishes the micro-level canonical knowledge architecture for Physics across Grades 9–11. Every subtopic in Physics must satisfy the highest standard of physical rigor:
1. Physical models must specify coordinate reference frames and conservation validity boundaries before equations are introduced.
2. Learner misconceptions must be proactively surfaced and repaired using cognitive contrast pairs (Flawed Action vs. Correct Diagnostic Cue).
3. Active student reconstruction must be enforced via Reconstructable Technical Task Units (TTUs) featuring bounded viewports (`clip_to_viewport = true`).
4. Competitive exam discrimination must be achieved without altering frozen source questions.

---

## 2. Four-Layer Subtopic Intelligence Packet Architecture

Every subtopic admitted to the library is structured as a typed 4-layer intelligence packet:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: PHYSICAL CORE & NON-NEGOTIABLE PRECONDITIONS                  │
│ • Coordinate frame declarations • Validity conditions (e.g. W_nc = 0)  │
│ • Mandatory invariant equations • Vector/scalar dimensional integrity │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ feeds
┌───────────────────────────────────▼────────────────────────────────────┐
│ LAYER 2: COGNITIVE TRANSFORMATIONS & LEARNING ATOM DAG                 │
│ • Atomic concepts (CONCEPT, RELATION, INVARIANT, PROCEDURE, STRATEGY)   │
│ • Symbol bridges (formal vector notation ↔ intuitive physical meaning) │
│ • Misconception repair contrasts (flawed logic ↔ correct diagnostic cue)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ concretizes
┌───────────────────────────────────▼────────────────────────────────────┐
│ LAYER 3: RECONSTRUCTABLE TTU LIBRARY (TECHNICAL TASK UNITS)            │
│ • Incomplete free-body diagrams with missing vector components         │
│ • Energy accounting bar skeletons with dissipation terms               │
│ • Bounded viewports (clip_to_viewport = true)                          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ exercises
┌───────────────────────────────────▼────────────────────────────────────┐
│ LAYER 4: PROBLEM FAMILIES & TRANSFER DISCRIMINATION                    │
│ • Canonical worked exemplars (Core1A) • Faded self-tutors (Core1B)    │
│ • Expert solution anatomy (Core2A)   • Open transfer challenges (Core2B)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Concrete Exemplar Packet: Work, Energy, Power & Mechanical Energy Conservation (`PHY-WORK-ENERGY-POWER`)

Below is the canonical reference implementation of a Subtopic Intelligence Packet for **Work, Energy, Power & Mechanical Energy Conservation** across Grades 9–11.

### 3.1 Layer 1: Physical Core & Non-Negotiable Invariants

- **Canonical Subtopic ID**: `PHY-WORK-ENERGY-POWER`
- **Engineering Gate Binding**: `PHY-WORK-ENERGY-POWER` (Digest-bound closure receipt)
- **Learner Title**: Work, Energy, Power & Conditions for Mechanical Energy Conservation
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 11 (Standard/Advanced Mechanics)
- **Non-Negotiable Preconditions**:
  1. **Work-Energy Theorem Generality Invariant**: The net work done on a particle by *all* acting forces (conservative, non-conservative, and external) strictly equals the change in kinetic energy: $W_{\text{net}} = W_{\text{c}} + W_{\text{nc}} + W_{\text{ext}} = \Delta K = \frac{1}{2}m v_f^2 - \frac{1}{2}m v_i^2$. This holds in any inertial frame regardless of force nature.
  2. **Mechanical Energy Conservation Condition Invariant**: Mechanical energy $E_{\text{mech}} = K + U$ is conserved ($\Delta E_{\text{mech}} = 0$) **if and only if** the net work done by all non-conservative and non-potential forces vanishes: $W_{\text{nc}} + W_{\text{ext}} = 0$. Stating $K_i + U_i = K_f + U_f$ in the presence of unmodeled friction or inelastic deformation is a fatal physical error.
  3. **Potential Energy Definition Invariant**: Potential energy is defined exclusively for conservative forces via the line integral: $\Delta U = - W_{\text{c}} = -\int_{\vec{r}_i}^{\vec{r}_f} \vec{F}_{\text{c}} \cdot d\vec{r}$. Potential energy cannot be assigned to dissipative or non-conservative interactions (e.g. kinetic friction).

### 3.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-WEP-01` (`CONCEPT`): Work as a scalar path integral of force along displacement: $W = \int \vec{F} \cdot d\vec{r} = \int (F_x dx + F_y dy + F_z dz)$. For constant force, $W = \vec{F} \cdot \vec{d} = F d \cos\theta$.
- `ATOM-WEP-02` (`RELATION`): Conservative force as the negative gradient of potential energy: $\vec{F} = -\vec{\nabla} U = -\left(\frac{\partial U}{\partial x}\hat{i} + \frac{\partial U}{\partial y}\hat{j} + \frac{\partial U}{\partial z}\hat{k}\right)$.
- `ATOM-WEP-03` (`INVARIANT`): Conservation of Mechanical Energy condition: $W_{\text{nc}} = 0 \implies \Delta (K + U) = 0$. In general: $K_i + U_i + W_{\text{nc}} + W_{\text{ext}} = K_f + U_f$.
- `ATOM-WEP-04` (`PROCEDURE`): Energy accounting workflow: (1) Define isolated system boundary, (2) Identify conservative forces and associate potential energy functions ($mgh, \frac{1}{2}kx^2$), (3) Calculate line work of non-conservative forces along actual path, (4) Formulate work-energy equation.
- `ATOM-WEP-05` (`STRATEGY`): Discrimination between instantaneous power $P = \vec{F} \cdot \vec{v}$ and average power $P_{\text{avg}} = \frac{\Delta W}{\Delta t}$ in variable velocity systems.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Work is force times distance"* | $W = \int_{r_1}^{r_2} \vec{F} \cdot d\vec{r}$ | Path integral of the directional scalar product, not naive scalar multiplication. |
| *"Energy is always conserved"* | $W_{\text{nc}} = 0 \iff \Delta (K + U) = 0$ | Total mass-energy is universally conserved, but *mechanical* energy requires vanishing non-conservative work. |
| *"Potential energy of a body"* | $U_{\text{system}} = -\int \vec{F}_{\text{int,c}} \cdot d\vec{r}$ | Potential energy is a shared configuration property of a system, never of an isolated particle alone. |

#### C. Misconception Contrasts
1. **Misconception: Unconditional Mechanical Energy Conservation**:
   - *Flawed Action*: Writing $mgh = \frac{1}{2}mv^2$ for a block sliding down a rough ramp with friction coefficient $\mu > 0$.
   - *Correct Diagnostic Cue*: Kinetic friction is non-conservative ($W_f = -\mu mg \cos\theta \cdot d \neq 0$). The correct statement is $K_i + U_i + W_f = K_f + U_f \implies mgh - \mu mg \cos\theta \cdot d = \frac{1}{2}mv^2$.
2. **Misconception: Normal Force Never Does Work**:
   - *Flawed Action*: Assuming normal force work $W_N = 0$ in an accelerating elevator or on a movable wedge.
   - *Correct Diagnostic Cue*: $W = \int \vec{F} \cdot d\vec{r}_{\text{point of contact}}$. If the contact surface itself moves along the normal vector (e.g. a rising elevator floor), $W_N = N \Delta y > 0$.
3. **Misconception: Centripetal Force Does Work**:
   - *Flawed Action*: Calculating work done by tension in circular motion as $T \times 2\pi r$.
   - *Correct Diagnostic Cue*: At every instant, tension is perpendicular to instantaneous velocity ($\vec{T} \cdot \vec{v} = 0 \implies \vec{T} \cdot d\vec{r} = 0$). Therefore, work done by pure centripetal force is strictly zero.

---

### 3.3 Layer 3: Reconstructable TTU Library

#### TTU-WEP-01: Incomplete Energy Accounting Bar Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A 2 kg mass is released from rest at height h = 5 m on a ramp. At the bottom, its speed is 8 m/s.
Take g = 9.8 m/s². Determine the work done by friction W_nc.

Step 1: Calculate initial mechanical energy E_i = K_i + U_i:
        K_i = [ ___ ] J,  U_i = mgh = 2 · 9.8 · 5 = [ ___ ] J  =>  E_i = [ ___ ] J
Step 2: Calculate final mechanical energy E_f = K_f + U_f:
        K_f = 1/2 · m · v_f² = 1/2 · 2 · (8)² = [ ___ ] J,  U_f = [ ___ ] J  =>  E_f = [ ___ ] J
Step 3: State the governing non-conservative work relation:
        W_nc = E_f - E_i = [ ___ ] J - [ ___ ] J = [ ___ ] J
Step 4: Explain the sign of W_nc:
        Friction does [ positive / negative ] work because displacement is [ opposite / parallel ] to friction.

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: K_i = 0 J, U_i = 98.0 J, E_i = 98.0 J
Step 2: K_f = 64.0 J, U_f = 0 J, E_f = 64.0 J
Step 3: W_nc = 64.0 J - 98.0 J = -34.0 J
Step 4: Friction does negative work because displacement is opposite to friction.
```

#### TTU-WEP-02: Reconstructable FBD & Variable Force Integral (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A force F(x) = (3x² - 2x) N acts on a particle of mass m = 0.5 kg moving from x = 1 m to x = 3 m.
If the particle starts with v(1) = 2 m/s, find its velocity at x = 3 m.

Step 1: Set up work integral: W = ∫[1 to 3] ( [ ___ ] ) dx
Step 2: Evaluate antiderivative: [ ___ - ___ ] evaluated between 1 and 3
        At x = 3: (3)³ - (3)² = [ ___ ]
        At x = 1: (1)³ - (1)² = [ ___ ]
        W = [ ___ ] J
Step 3: Apply Work-Energy Theorem: W = 1/2 · m · (v_f² - v_i²)
        [ ___ ] = 1/2 · (0.5) · (v_f² - [ ___ ])
Step 4: Solve for v_f:
        v_f = [ ___ ] m/s

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: W = ∫[1 to 3] (3x² - 2x) dx
Step 2: [x³ - x²] from 1 to 3. At 3: 27 - 9 = 18. At 1: 1 - 1 = 0. W = 18 J.
Step 3: 18 = 1/2 · 0.5 · (v_f² - 4) => 18 = 0.25 · (v_f² - 4) => 72 = v_f² - 4
Step 4: v_f² = 76 => v_f = √76 ≈ 8.72 m/s
```

---

### 3.4 Layer 4: Problem Families & Transfer Discrimination

#### FAMILY-WEP-01 (CBSE_BOARD): Constant Force on Inclined Plane
- **Canonical Setup**: Mass sliding down plane with constant friction coefficient $\mu$.
- **Cognitive Target**: Scalar decomposition of work; distinguishing work done by gravity ($mgh$) from friction ($-\mu mg d \cos\theta$).
- **Fading Progression**: Fully worked example in Core1A $\to$ Faded TTU-WEP-01 in Core1B.

#### FAMILY-WEP-02 (JEE_MAIN): Compressed Spring & Loop-the-Loop
- **Canonical Setup**: Mass released from compressed spring entering vertical circular track of radius $R$.
- **Cognitive Target**: Multi-stage potential energy transfer; critical speed condition at top of loop ($v_{\text{top}} \ge \sqrt{gR} \implies N \ge 0$).
- **Fading Progression**: Solution anatomy in Core2A $\to$ Open transfer with varying track friction in Core2B.

---

## 4. Foundation Packet: Newton's Laws of Motion & Free Body Diagrams (`PHY-NLM-FIRST-LAW`)

### 4.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-FIRST-LAW`
- **Learner Title**: Newton's Laws of Motion, Inertial Frames & Free Body Diagrams
- **Grade Span**: Grade 9 (Foundation) &bull; Grade 11 (Standard/Advanced)
- **Non-Negotiable Preconditions**:
  1. **Inertial Reference Frame Precondition**: Newton's First and Second Laws ($\sum \vec{F} = m\vec{a}$) are valid **if and only if** evaluated in an inertial reference frame. In a frame accelerating with acceleration $\vec{a}_0$, an observer must introduce fictitious pseudo forces $\vec{F}_{\text{pseudo}} = -m\vec{a}_0$.
  2. **Action-Reaction Pair Invariant**: Newton's Third Law forces $\vec{F}_{AB} = -\vec{F}_{BA}$ act on **two different interacting bodies**, never on the same body. They never cancel in a single-body free body diagram.

### 4.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-NLM-01` (`CONCEPT`): Inertia as the intrinsic resistance of mass to changes in its velocity vector ($\vec{v} = \text{const} \iff \sum \vec{F} = 0$).
- `ATOM-NLM-02` (`RELATION`): Newton's Second Law as rate of change of momentum: $\vec{F}_{\text{net}} = \frac{d\vec{p}}{dt} = m\vec{a} + \vec{v}\frac{dm}{dt}$. For constant mass, $\vec{F}_{\text{net}} = m\vec{a}$.
- `ATOM-NLM-03` (`INVARIANT`): Momentum conservation of isolated system: $\sum \vec{F}_{\text{ext}} = 0 \implies \vec{P}_{\text{total}} = \text{const}$.
- `ATOM-NLM-04` (`PROCEDURE`): Systematic FBD isolation: (1) Choose boundary of interest, (2) Draw coordinate axes along expected acceleration, (3) Enumerate all contact forces (normal, friction, tension) and long-range forces (gravity), (4) Project along axes: $\sum F_x = m a_x, \sum F_y = m a_y$.
- `ATOM-NLM-05` (`STRATEGY`): Selection of non-inertial reference frame with pseudo force vs. inertial laboratory frame.

#### Misconception Contrasts
1. **Misconception: Normal Force Always Equals $mg$**:
   - *Flawed Action*: Assuming $N = mg$ on an incline or when an external angled force acts.
   - *Correct Diagnostic Cue*: Normal force is a contact constraint determined by dynamic balance: $\sum F_{\perp} = 0 \implies N = mg \cos\theta \pm F_{\text{ext}}\sin\phi$.
2. **Misconception: Action and Reaction Cancel Out**:
   - *Flawed Action*: Arguing a horse cannot pull a cart because the cart pulls back on the horse with equal and opposite force.
   - *Correct Diagnostic Cue*: The forward force on the cart is exerted by the horse; the backward force on the horse is exerted by the cart. Since they act on different bodies, each body accelerates according to the net force acting on *it*.

### 4.3 Layer 3: Reconstructable TTU Library
#### TTU-NLM-01: Incomplete Free-Body Vector Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A 5 kg block rests on a rough ramp inclined at 30° to the horizontal. A horizontal pushing force F = 20 N acts on the block.
Draw and resolve the forces along the ramp (x-axis, pointing up) and perpendicular to the ramp (y-axis, pointing away).

Step 1: Resolve gravity mg (5 · 9.8 = 49 N):
        Component down ramp: mg · [ sin / cos ](30°) = 49 · [ ___ ] = [ ___ ] N
        Component perpendicular to ramp: mg · [ sin / cos ](30°) = 49 · [ ___ ] = [ ___ ] N
Step 2: Resolve horizontal force F = 20 N:
        Component up ramp: F · [ sin / cos ](30°) = 20 · [ ___ ] = [ ___ ] N
        Component into ramp: F · [ sin / cos ](30°) = 20 · [ ___ ] = [ ___ ] N
Step 3: Formulate normal force N from perpendicular equilibrium:
        N = mg_perp + F_perp = [ ___ ] N + [ ___ ] N = [ ___ ] N

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: mg_down = mg·sin(30°) = 49·0.5 = 24.5 N; mg_perp = mg·cos(30°) = 49·0.866 = 42.44 N
Step 2: F_up = F·cos(30°) = 20·0.866 = 17.32 N; F_perp = F·sin(30°) = 20·0.5 = 10.0 N
Step 3: N = 42.44 N + 10.0 N = 52.44 N
```

#### TTU-NLM-02: Connected Bodies & String Tension TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Two masses m1 = 3 kg and m2 = 2 kg are connected by a massless string over a frictionless pulley (Atwood machine).
Find acceleration a and tension T.

Step 1: Write equation for m1 (moving down): m1·g - T = m1·a  =>  [ ___ ] - T = 3a
Step 2: Write equation for m2 (moving up):   T - m2·g = m2·a  =>  T - [ ___ ] = 2a
Step 3: Add both equations: (m1 - m2)·g = (m1 + m2)·a  =>  [ ___ ] = 5a  =>  a = [ ___ ] m/s²
Step 4: Substitute to find T: T = m2·(g + a) = 2 · ([ ___ ]) = [ ___ ] N

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 29.4 - T = 3a
Step 2: T - 19.6 = 2a
Step 3: 9.8 = 5a => a = 1.96 m/s²
Step 4: T = 2 · (9.8 + 1.96) = 2 · 11.76 = 23.52 N
```

### 4.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLM-01` (`CBSE_BOARD`): Newton's second law on single body with friction on horizontal and inclined surfaces.
- `FAMILY-NLM-02` (`JEE_MAIN`): Multi-body connected systems with massless strings, pulleys, and normal reaction constraints.

---

## 5. Foundation Packet: Ray Optics, Reflection & Refraction (`PHY-OPTICS-REFLECTION-MIRRORS`)

### 5.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-OPTICS-REFLECTION-MIRRORS`
- **Learner Title**: Geometric Optics: Laws of Reflection, Spherical Mirrors & Sign Conventions
- **Grade Span**: Grade 10 (Board) &bull; Grade 12 (Wave/Ray Wavefronts)
- **Non-Negotiable Preconditions**:
  1. **Cartesian Sign Convention Precondition**: All distances are measured from the optical pole/center. Distances measured in the direction of incident light are positive; opposite to incident light are negative. Heights upward from principal axis are positive; downward are negative.
  2. **Paraxial Ray Approximation**: Spherical mirror formula $\frac{1}{v} + \frac{1}{u} = \frac{1}{f}$ and lens formula $\frac{1}{v} - \frac{1}{u} = \frac{1}{f}$ hold strictly for rays close to and making small angles with the principal axis ($\sin\theta \approx \tan\theta \approx \theta$).

### 5.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-OPT-01` (`CONCEPT`): Specular reflection: incident ray, reflected ray, and surface normal lie in the same plane; angle of incidence equals angle of reflection ($\theta_i = \theta_r$).
- `ATOM-OPT-02` (`RELATION`): Spherical mirror focal length relation: $f = R/2$; mirror formula: $\frac{1}{f} = \frac{1}{v} + \frac{1}{u}$.
- `ATOM-OPT-03` (`INVARIANT`): Transverse magnification: $m = -\frac{v}{u} = \frac{h_i}{h_o}$. Real inverted images have $m < 0$; virtual erect images have $m > 0$.
- `ATOM-OPT-04` (`PROCEDURE`): Principal ray tracing algorithm: (1) Ray parallel to axis reflects through focus, (2) Ray through focus reflects parallel to axis, (3) Ray through center of curvature retraces path.
- `ATOM-OPT-05` (`STRATEGY`): Identifying virtual objects where converging incident rays strike an optical element before meeting.

#### Misconception Contrasts
1. **Misconception: Virtual Images Cannot Be Photographed**:
   - *Flawed Action*: Claiming a camera cannot record an image in a plane mirror because the image is virtual.
   - *Correct Diagnostic Cue*: A virtual image acts as a real divergence source for the camera's converging lens, which projects a real image onto the camera sensor.
2. **Misconception: Covering Half of a Mirror Cuts the Image in Half**:
   - *Flawed Action*: Believing that covering the top half of a concave mirror makes only the bottom half of the object visible.
   - *Correct Diagnostic Cue*: Every point of the object sends infinite rays to the entire mirror surface. Covering half the mirror reduces image brightness by 50% without altering the complete field of view.

### 5.3 Layer 3: Reconstructable TTU Library
#### TTU-OPT-01: Incomplete Ray Trace & Sign Convention Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
An object of height 3 cm is placed 20 cm in front of a concave mirror of radius of curvature R = 30 cm.
Find the image position v, height h_i, and nature.

Step 1: Identify given parameters with Cartesian signs:
        u = [ ___ ] cm,  R = [ ___ ] cm,  f = R/2 = [ ___ ] cm
Step 2: Apply mirror equation: 1/v + 1/u = 1/f
        1/v + 1/([ ___ ]) = 1/([ ___ ])
        1/v = 1/(-15) - 1/(-20) = -1/15 + 1/20 = (-4 + 3)/60 = [ ___ ]
        v = [ ___ ] cm
Step 3: Calculate magnification m:
        m = - v / u = - ([ ___ ]) / ([ ___ ]) = [ ___ ]
Step 4: Image characteristics:
        Nature: [ Real / Virtual ], Orientation: [ Inverted / Erect ], Height h_i = m · h_o = [ ___ ] cm

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: u = -20 cm, R = -30 cm, f = -15 cm
Step 2: 1/v + 1/(-20) = 1/(-15) => 1/v = -1/60 => v = -60 cm
Step 3: m = -(-60)/(-20) = -(3) = -3
Step 4: Nature: Real, Orientation: Inverted, Height h_i = -3 · 3 = -9 cm
```

#### TTU-OPT-02: Snell's Law & Apparent Depth TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A ray passes from water (n1 = 4/3) into glass (n2 = 3/2) at an angle of incidence θ1 = 30°.
Find the angle of refraction θ2 and the critical angle for total internal reflection at glass-water interface.

Step 1: Apply Snell's Law: n1 · sin(θ1) = n2 · sin(θ2)
        (4/3) · sin(30°) = (3/2) · sin(θ2)
        (4/3) · (0.5) = (3/2) · sin(θ2)  =>  sin(θ2) = [ ___ ]
        θ2 = arcsin([ ___ ])
Step 2: Calculate critical angle θ_c for ray going from glass to water:
        sin(θ_c) = n_rarer / n_denser = (4/3) / (3/2) = [ ___ ]
        θ_c = arcsin([ ___ ])

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: (4/6) = (3/2)·sin(θ2) => sin(θ2) = 4/9 ≈ 0.444 => θ2 = arcsin(4/9) ≈ 26.39°
Step 2: sin(θ_c) = (4/3) / (3/2) = 8/9 ≈ 0.889 => θ_c = arcsin(8/9) ≈ 62.73°
```

### 5.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-OPT-01` (`CBSE_BOARD`): Mirror and thin lens formula, linear magnification, refraction through rectangular slab.
- `FAMILY-OPT-02` (`JEE_MAIN`): Combination of lenses and mirrors, silvered lens surfaces, critical angle and total internal reflection.

---

## 6. Foundation Packet: Fluid Statics & Dynamics, Archimedes & Bernoulli (`PHY-FLUID-BERNOULLI-EQUATION`)

### 6.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-FLUID-BERNOULLI-EQUATION`
- **Learner Title**: Fluid Dynamics: Continuity Equation, Bernoulli's Principle & Torricelli's Law
- **Grade Span**: Grade 9 (Archimedes/Buoyancy) &bull; Grade 11 (Continuity & Bernoulli)
- **Non-Negotiable Preconditions**:
  1. **Incompressible & Non-Viscous Fluid Invariant**: Bernoulli's equation $P + \frac{1}{2}\rho v^2 + \rho g h = \text{const}$ strictly applies **along a streamline** for an ideal fluid (incompressible, non-viscous, irrotational, steady flow).
  2. **Archimedes Principle Buoyant Force Invariant**: Buoyant force equals the weight of the *displaced* fluid volume: $F_b = \rho_{\text{fluid}} V_{\text{submerged}} g$. It acts through the center of buoyancy (centroid of displaced volume).

### 6.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-FLU-01` (`CONCEPT`): Hydrostatic pressure variation with depth: $P = P_0 + \rho g h$. Pascal's principle: pressure applied to enclosed fluid is transmitted undiminished.
- `ATOM-FLU-02` (`RELATION`): Equation of continuity for incompressible flow: $A_1 v_1 = A_2 v_2 = Q = \text{const}$.
- `ATOM-FLU-03` (`INVARIANT`): Bernoulli's conservation of energy per unit volume along a streamline: $P_1 + \frac{1}{2}\rho v_1^2 + \rho g y_1 = P_2 + \frac{1}{2}\rho v_2^2 + \rho g y_2$.
- `ATOM-FLU-04` (`PROCEDURE`): Torricelli efflux analysis: (1) Apply continuity between tank surface and small orifice, (2) Neglect surface descent speed ($v_1 \approx 0$), (3) Equate surface pressure to orifice pressure ($P_0$), (4) Deduce $v = \sqrt{2gh}$.
- `ATOM-FLU-05` (`STRATEGY`): Venturi meter pressure differential analysis: $\Delta P = \frac{1}{2}\rho (v_2^2 - v_1^2) = \rho_{\text{manometer}} g \Delta h$.

#### Misconception Contrasts
1. **Misconception: High Speed Means High Pressure**:
   - *Flawed Action*: Assuming that water rushing fast out of a nozzle has high internal static pressure.
   - *Correct Diagnostic Cue*: By Bernoulli's principle, an increase in fluid velocity along a horizontal streamline occurs alongside a *drop* in static pressure.
2. **Misconception: Buoyancy Depends on Object Mass**:
   - *Flawed Action*: Claiming a 1 kg lead sphere and a 1 kg aluminum sphere experience the same buoyant force in water.
   - *Correct Diagnostic Cue*: Buoyant force depends strictly on *displaced fluid volume*, not object mass. Since lead is denser, its volume is smaller, so it experiences less buoyant force than aluminum.

### 6.3 Layer 3: Reconstructable TTU Library
#### TTU-FLU-01: Incomplete Venturi Flow Rate Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Water (ρ = 1000 kg/m³) flows through a horizontal pipe. At section 1, area A1 = 10 cm², speed v1 = 2 m/s.
At section 2 (throat), area A2 = 5 cm². Find v2 and pressure difference P1 - P2.

Step 1: Apply equation of continuity: A1·v1 = A2·v2
        (10 · 10⁻⁴) · 2 = (5 · 10⁻⁴) · v2  =>  v2 = [ ___ ] m/s
Step 2: Apply horizontal Bernoulli equation: P1 + 1/2·ρ·v1² = P2 + 1/2·ρ·v2²
        P1 - P2 = 1/2 · ρ · (v2² - v1²)
        P1 - P2 = 1/2 · (1000) · ( [ ___ ]² - [ ___ ]² )
Step 3: Evaluate numeric pressure difference:
        P1 - P2 = 500 · ( [ ___ ] - [ ___ ] ) = 500 · [ ___ ] = [ ___ ] Pa

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: v2 = (10·2)/5 = 4 m/s
Step 2: P1 - P2 = 1/2·1000·(4² - 2²)
Step 3: P1 - P2 = 500·(16 - 4) = 500·12 = 6000 Pa
```

#### TTU-FLU-02: Torricelli Efflux & Range TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A large tank filled with water to height H has a small hole at depth h below the water surface.
Find the horizontal range R of the exiting water jet on the ground.

Step 1: Efflux speed from Torricelli's theorem: v = [ ___ ]
Step 2: Time of flight from height (H - h) to ground: t = √( 2 · [ ___ ] / g )
Step 3: Horizontal range R = v · t:
        R = √(2gh) · √( 2(H - h)/g ) = 2 · √( [ ___ ] )
Step 4: At what depth h is range maximized?
        h = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: v = √(2gh)
Step 2: t = √(2(H - h)/g)
Step 3: R = 2·√(h(H - h))
Step 4: By differentiating h(H - h) or AM-GM, maximum occurs at h = H/2
```

### 6.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-FLU-01` (`CBSE_BOARD`): Archimedes principle, relative density, pressure variation in static columns.
- `FAMILY-FLU-02` (`JEE_MAIN`): Venturi tube, siphon flow, Magnus effect, dynamic lift on aerofoils.

---

## 7. Foundation Packet: 1D & 2D Kinematics & Projectile Motion (`PHY-KIN-1D-MOTION`)

### 7.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-KIN-1D-MOTION`
- **Learner Title**: Kinematics: 1D Rectilinear Motion, Graph Analysis & 2D Projectile Motion
- **Grade Span**: Grade 9 (1D Motion & Graphs) &bull; Grade 11 (2D Projectiles & Relative Velocity)
- **Non-Negotiable Preconditions**:
  1. **Constant Acceleration Constraint**: The kinematic equations ($v = u + at$, $s = ut + \frac{1}{2}at^2$, $v^2 = u^2 + 2as$) hold **if and only if** acceleration is strictly constant ($\vec{a} = \text{const}$). For time-varying or position-dependent acceleration, calculus definitions $v = \frac{ds}{dt}$ and $a = v\frac{dv}{ds}$ must be integrated.
  2. **Independence of Orthogonal Motions**: In 2D projectile motion, the horizontal ($x$) and vertical ($y$) components are completely independent and coupled only by time parameter $t$.

### 7.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-KIN-01` (`CONCEPT`): Distinction between distance (scalar path length) and displacement (vector $\Delta \vec{r} = \vec{r}_f - \vec{r}_i$).
- `ATOM-KIN-02` (`RELATION`): Graph calculus correspondences: slope of $s\text{-}t$ is $v(t)$; slope of $v\text{-}t$ is $a(t)$; area under $v\text{-}t$ is displacement $\Delta s$.
- `ATOM-KIN-03` (`INVARIANT`): Projectile trajectory equation in vacuum: $y = x\tan\theta - \frac{g x^2}{2 u^2 \cos^2\theta} = x\tan\theta\left(1 - \frac{x}{R}\right)$.
- `ATOM-KIN-04` (`PROCEDURE`): Derivation of projectile parameters: $T = \frac{2u\sin\theta}{g}$, $H = \frac{u^2\sin^2\theta}{2g}$, $R = \frac{u^2\sin 2\theta}{g}$.
- `ATOM-KIN-05` (`STRATEGY`): Resolving relative motion in 2D: $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$ (rain-umbrella, river-swimmer problems).

#### Misconception Contrasts
1. **Misconception: Zero Velocity Means Zero Acceleration**:
   - *Flawed Action*: Saying a ball thrown vertically upward has $a = 0$ at its highest point because $v = 0$.
   - *Correct Diagnostic Cue*: At the peak, velocity is instantaneously zero ($v = 0$), but acceleration is constant and non-zero ($a = -g = -9.8\text{ m/s}^2$).
2. **Misconception: Speed and Average Speed Equivalence**:
   - *Flawed Action*: Calculating average speed for round trip at speeds $v_1$ and $v_2$ as arithmetic mean $\frac{v_1+v_2}{2}$.
   - *Correct Diagnostic Cue*: Average speed is total distance over total time: $v_{\text{avg}} = \frac{2d}{d/v_1 + d/v_2} = \frac{2v_1 v_2}{v_1 + v_2}$ (harmonic mean).

### 7.3 Layer 3: Reconstructable TTU Library
#### TTU-KIN-01: Incomplete Motion Graph Analysis Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A v-t graph starts at (0, 0), rises linearly to (4 s, 12 m/s), stays constant until 10 s, then decelerates to rest at 14 s.
Find total distance travelled and acceleration in each phase.

Phase 1 (0 to 4 s):   a1 = (12 - 0)/(4 - 0) = [ ___ ] m/s²;   Area1 (triangle) = 1/2 · 4 · 12 = [ ___ ] m
Phase 2 (4 to 10 s):  a2 = [ ___ ] m/s²;                      Area2 (rectangle) = (10 - 4) · 12 = [ ___ ] m
Phase 3 (10 to 14 s): a3 = (0 - 12)/(14 - 10) = [ ___ ] m/s²; Area3 (triangle) = 1/2 · (14 - 10) · 12 = [ ___ ] m
Total distance = Area1 + Area2 + Area3 = [ ___ ] + [ ___ ] + [ ___ ] = [ ___ ] m

[COMPLETION KEY - VERIFICATION ONLY]
Phase 1: a1 = 3 m/s², Area1 = 24 m
Phase 2: a2 = 0 m/s², Area2 = 72 m
Phase 3: a3 = -3 m/s², Area3 = 24 m
Total distance = 24 + 72 + 24 = 120 m
```

#### TTU-KIN-02: Projectile Motion Decomposition TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A projectile is fired with u = 50 m/s at θ = 37° to horizontal (cos 37° = 0.8, sin 37° = 0.6, g = 10 m/s²).
Find its velocity vector at t = 2 s and time of flight T.

Step 1: Initial velocity components: u_x = 50 · 0.8 = [ ___ ] m/s,  u_y = 50 · 0.6 = [ ___ ] m/s
Step 2: Velocity components at t = 2 s:
        v_x(2) = u_x = [ ___ ] m/s
        v_y(2) = u_y - g·t = 30 - (10)·(2) = [ ___ ] m/s
Step 3: Magnitude and angle of velocity at t = 2 s:
        |v(2)| = √( [ ___ ]² + [ ___ ]² ) = √( [ ___ ] ) m/s
Step 4: Time of flight T = (2 · u_y) / g = (2 · [ ___ ]) / 10 = [ ___ ] s

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: u_x = 40 m/s, u_y = 30 m/s
Step 2: v_x(2) = 40 m/s, v_y(2) = 10 m/s
Step 3: |v(2)| = √(40² + 10²) = √(1600 + 100) = √1700 ≈ 41.23 m/s
Step 4: T = (2 · 30) / 10 = 6.0 s
```

### 7.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-KIN-01` (`CBSE_BOARD`): Equations of motion derivation via graphical method, vertical free fall under gravity.
- `FAMILY-KIN-02` (`JEE_MAIN`): Projectile motion from height, projectile on inclined plane, collision of projectiles in mid-air.

---

## 8. Foundation Packet: Gravitation, Free Fall & Planetary Orbits (`PHY-GRAV-UNIVERSAL-LAW`)

### 8.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-GRAV-UNIVERSAL-LAW`
- **Learner Title**: Universal Gravitation: Inverse-Square Law, Gravitational Potential & Kepler's Laws
- **Grade Span**: Grade 9 (Universal Law & Free Fall) &bull; Grade 11 (Kepler, Orbits, Escape Speed)
- **Non-Negotiable Preconditions**:
  1. **Point Mass & Spherically Symmetric Body Constraint**: Newton's Law $F = \frac{G m_1 m_2}{r^2}$ applies strictly between point masses or spherically symmetric mass distributions (Newton's Shell Theorem).
  2. **Areal Velocity & Angular Momentum Conservation**: Kepler's Second Law ($\frac{dA}{dt} = \frac{L}{2m} = \text{const}$) holds for any central force because torque about the sun is identically zero ($\vec{\tau} = \vec{r} \times \vec{F} = 0$).

### 8.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-GRAV-01` (`CONCEPT`): Universal Gravitation Law: $F = \frac{G M m}{r^2}$ with $G \approx 6.674 \times 10^{-11}\text{ N}\cdot\text{m}^2/\text{kg}^2$.
- `ATOM-GRAV-02` (`RELATION`): Acceleration due to gravity: $g(h) = \frac{GM}{(R+h)^2} \approx g_0\left(1 - \frac{2h}{R}\right)$ for $h \ll R$; $g(d) = g_0\left(1 - \frac{d}{R}\right)$ at depth $d$.
- `ATOM-GRAV-03` (`INVARIANT`): Gravitational potential energy of two-mass system: $U(r) = -\frac{G M m}{r}$ (reference zero at $r \to \infty$).
- `ATOM-GRAV-04` (`PROCEDURE`): Orbital mechanics derivations:
  - Orbital speed: $v_o = \sqrt{\frac{GM}{r}}$.
  - Escape speed from surface: $v_e = \sqrt{\frac{2GM}{R}} = \sqrt{2gR} = \sqrt{2}v_o$.
- `ATOM-GRAV-05` (`STRATEGY`): Kepler's Third Law application: $T^2 = \left(\frac{4\pi^2}{GM}\right) a^3$ for elliptical/circular orbits.

#### Misconception Contrasts
1. **Misconception: Zero Gravity in Orbit**:
   - *Flawed Action*: Explaining astronaut weightlessness on the ISS as absence of gravity ($g = 0$).
   - *Correct Diagnostic Cue*: At 400 km altitude, $g \approx 8.7\text{ m/s}^2$ (about 89% of surface gravity). Astronauts experience apparent weightlessness because they and the station are in continuous free fall together.
2. **Misconception: Heavier Bodies Fall Faster in Vacuum**:
   - *Flawed Action*: Assuming a 10 kg bowling ball accelerates twice as fast as a 5 kg ball in free fall.
   - *Correct Diagnostic Cue*: Inertial mass equals gravitational mass ($m_i a = \frac{GM m_g}{r^2} \implies a = \frac{GM}{r^2}$). Acceleration is completely independent of the falling object's mass.

### 8.3 Layer 3: Reconstructable TTU Library
#### TTU-GRAV-01: Incomplete Escape Velocity Derivation Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Derive the escape speed v_e from the surface of Earth (mass M, radius R) using energy conservation.

Step 1: Total mechanical energy at launch from surface:
        E_i = 1/2 · m · v_e² + U(R) = 1/2 · m · v_e² - [ ___ ]
Step 2: Total mechanical energy at r -> infinity with minimum escape speed:
        E_f = K_inf + U_inf = 0 + [ ___ ] = [ ___ ]
Step 3: Equate E_i = E_f:
        1/2 · m · v_e² - G·M·m/R = 0  =>  1/2 · v_e² = [ ___ ]
Step 4: Express in terms of surface gravity g = G·M/R²:
        v_e = √( 2 · [ ___ ] / R ) = √( 2 · [ ___ ] · R )

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: U(R) = -G·M·m/R
Step 2: U_inf = 0, E_f = 0
Step 3: 1/2 · v_e² = G·M/R
Step 4: v_e = √(2GM/R) = √(2gR)
```

#### TTU-GRAV-02: Orbital Period & Energy Balance TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A satellite of mass m orbits Earth at altitude h = R (so r = 2R).
Find its kinetic energy K, potential energy U, and total mechanical energy E.

Step 1: Express orbital speed: v_o = √( G·M / [ ___ ] )
Step 2: Kinetic energy: K = 1/2 · m · v_o² = 1/2 · m · ( G·M / (2R) ) = [ ___ ] · (G·M·m / R)
Step 3: Potential energy: U = - G·M·m / (2R) = - [ ___ ] · (G·M·m / R)
Step 4: Total energy: E = K + U = ( [ ___ ] - [ ___ ] ) · (G·M·m / R) = - [ ___ ] · (G·M·m / R)
Verify virial theorem: E = -K = U/2: [ Confirmed / Violated ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: v_o = √(GM/(2R))
Step 2: K = 1/4 · (GMm/R) = 0.25 (GMm/R)
Step 3: U = -1/2 · (GMm/R) = -0.5 (GMm/R)
Step 4: E = (0.25 - 0.5)(GMm/R) = -0.25 (GMm/R). Confirmed: E = -K = U/2.
```

### 8.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-GRAV-01` (`CBSE_BOARD`): Universal gravitation calculations, variation of g with altitude and depth, mass vs weight.
- `FAMILY-GRAV-02` (`JEE_MAIN`): Geostationary satellite orbit radius, binding energy of satellites, binary star systems.

---

## 9. Foundation Packet: Current Electricity, Ohm's Law & Circuit Analysis (`PHY-ELEC-CURRENT-OHM`)

### 9.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-ELEC-CURRENT-OHM`
- **Learner Title**: Current Electricity: Ohm's Law, Resistivity & Kirchhoff's Laws
- **Grade Span**: Grade 10 (Ohm's Law, Series/Parallel) &bull; Grade 12 (Kirchhoff, Potentiometer)
- **Non-Negotiable Preconditions**:
  1. **Ohmic Material Precondition**: Ohm's Law ($V = IR$) holds strictly at constant temperature for materials with linear $I\text{-}V$ characteristics. For semiconductor diodes or incandescent filaments, resistance is non-linear and dynamic ($r_d = \frac{dV}{dI}$).
  2. **Charge & Energy Conservation Invariant**: Kirchhoff's Current Law ($\sum I = 0$ at a junction) represents local charge conservation. Kirchhoff's Voltage Law ($\sum \Delta V = 0$ around a closed loop) represents electrostatic energy conservation ($\oint \vec{E} \cdot d\vec{l} = 0$).

### 9.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-ELEC-01` (`CONCEPT`): Electric current as drift of charge carriers: $I = n e A v_d$; current density $\vec{J} = \sigma \vec{E}$.
- `ATOM-ELEC-02` (`RELATION`): Resistance and resistivity: $R = \rho \frac{L}{A}$; temperature dependence: $R(T) = R_0 (1 + \alpha \Delta T)$.
- `ATOM-ELEC-03` (`INVARIANT`): Series and parallel combinations:
  - Series: $R_{\text{eq}} = R_1 + R_2 + \dots$ (same current).
  - Parallel: $\frac{1}{R_{\text{eq}}} = \frac{1}{R_1} + \frac{1}{R_2} + \dots$ (same potential difference).
- `ATOM-ELEC-04` (`PROCEDURE`): Joule heating and electrical power calculations: $P = V I = I^2 R = \frac{V^2}{R}$.
- `ATOM-ELEC-05` (`STRATEGY`): Loop analysis via Kirchhoff's rules with declared sign conventions across batteries and resistors.

#### Misconception Contrasts
1. **Misconception: Current is Consumed by Resistors**:
   - *Flawed Action*: Thinking current leaving a resistor is less than the current entering it.
   - *Correct Diagnostic Cue*: Current is rate of flow of charge. Charge is strictly conserved; the current entering and leaving any resistor in series is identical. What is dropped is electrical potential energy ($V$), not charge.
2. **Misconception: Electrons Travel Near Speed of Light**:
   - *Flawed Action*: Assuming electrons race from the switch to the lightbulb at the speed of light.
   - *Correct Diagnostic Cue*: The drift speed $v_d$ of conduction electrons in copper is typically $\sim 10^{-4}\text{ m/s}$ (sub-millimeter per second). The electromagnetic wave that drives them propagates near $c$.

### 9.3 Layer 3: Reconstructable TTU Library
#### TTU-ELEC-01: Incomplete Equivalent Resistance & Circuit Reduction Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A 12 V battery is connected to a circuit: R1 = 4 Ω in series with a parallel combination of R2 = 6 Ω and R3 = 3 Ω.
Find the total equivalent resistance, battery current I, and voltage drop across R2.

Step 1: Calculate parallel combination of R2 and R3:
        1/R_p = 1/6 + 1/3 = (1 + 2)/6 = 3/6  =>  R_p = [ ___ ] Ω
Step 2: Total circuit resistance R_total:
        R_total = R1 + R_p = 4 + [ ___ ] = [ ___ ] Ω
Step 3: Total battery current I:
        I = V / R_total = 12 / [ ___ ] = [ ___ ] A
Step 4: Voltage drop across R1 and R_p:
        V1 = I · R1 = [ ___ ] · 4 = [ ___ ] V
        V_p = V - V1 = 12 - [ ___ ] = [ ___ ] V

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: R_p = 6/3 = 2 Ω
Step 2: R_total = 4 + 2 = 6 Ω
Step 3: I = 12 / 6 = 2 A
Step 4: V1 = 2 · 4 = 8 V; V_p = 12 - 8 = 4 V
```

#### TTU-ELEC-02: Kirchhoff Loop Equations TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A two-mesh circuit has battery E1 = 10 V in branch 1 with r1 = 1 Ω, battery E2 = 4 V in branch 2 with r2 = 2 Ω,
connected across central load resistor R = 5 Ω.
Set up Kirchhoff mesh currents I1 (clockwise) and I2 (counterclockwise).

Step 1: Mesh 1 loop equation: E1 - I1·r1 - (I1 + I2)·R = 0
        10 - 1·I1 - 5·(I1 + I2) = 0  =>  [ ___ ]·I1 + [ ___ ]·I2 = 10
Step 2: Mesh 2 loop equation: E2 - I2·r2 - (I1 + I2)·R = 0
        4 - 2·I2 - 5·(I1 + I2) = 0   =>  [ ___ ]·I1 + [ ___ ]·I2 = 4
Step 3: Solve linear system for I1 and I2:
        I1 = [ ___ ] A,  I2 = [ ___ ] A

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: 6·I1 + 5·I2 = 10
Step 2: 5·I1 + 7·I2 = 4
Step 3: From (1)*7 - (2)*5: 42·I1 - 25·I1 = 70 - 20 => 17·I1 = 50 => I1 = 50/17 ≈ 2.94 A.
        Then 5*(50/17) + 7·I2 = 4 => 7·I2 = 4 - 250/17 = -182/17 => I2 = -26/17 ≈ -1.53 A.
```

### 9.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-ELEC-01` (`CBSE_BOARD`): Series and parallel resistance networks, electrical power rating and bill estimation.
- `FAMILY-ELEC-02` (`JEE_MAIN`): Multi-loop circuits with Kirchhoff rules, Wheatstone bridge sensitivity, internal resistance of cells.

---

## 10. Foundation Packet: Magnetism, Lorentz Force & Electromagnetic Induction (`PHY-MAG-FIELD-LORENTZ`)

### 10.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-MAG-FIELD-LORENTZ`
- **Learner Title**: Magnetic Fields: Lorentz Force, Biot-Savart Law & Faraday Induction
- **Grade Span**: Grade 10 (Magnetic Effects of Current) &bull; Grade 12 (Lorentz Force & Induction)
- **Non-Negotiable Preconditions**:
  1. **Magnetic Force Velocity Perpendicularity Invariant**: Magnetic force $\vec{F}_B = q(\vec{v} \times \vec{B})$ is strictly perpendicular to instantaneous velocity $\vec{v}$. Consequently, the magnetic force does zero work ($W_B = \int \vec{F}_B \cdot \vec{v} dt = 0$) and cannot alter a particle's speed or kinetic energy in a pure magnetic field.
  2. **Lenz's Law Energy Conservation Invariant**: Induced electromotive force $\mathcal{E} = -\frac{d\Phi_B}{dt}$ opposes the change in magnetic flux that creates it. A positive sign would violate conservation of energy by creating self-amplifying currents without mechanical work.

### 10.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-MAG-01` (`CONCEPT`): Magnetic flux as surface integral: $\Phi_B = \int \vec{B} \cdot d\vec{A} = B A \cos\theta$.
- `ATOM-MAG-02` (`RELATION`): Helical motion in uniform magnetic field: radius $r = \frac{m v_\perp}{q B}$; cyclotron frequency $f = \frac{q B}{2\pi m}$ (independent of velocity).
- `ATOM-MAG-03` (`INVARIANT`): Lorentz force law: $\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})$.
- `ATOM-MAG-04` (`PROCEDURE`): Determining direction of magnetic force and induced currents via Right Hand Rule and Lenz's Law.
- `ATOM-MAG-05` (`STRATEGY`): Motional EMF analysis across a moving conductor: $\mathcal{E} = B l v$.

#### Misconception Contrasts
1. **Misconception: Magnetic Field Lines Have Ends**:
   - *Flawed Action*: Drawing magnetic field lines starting from North and terminating at South inside a magnet.
   - *Correct Diagnostic Cue*: Magnetic field lines form continuous closed loops ($\vec{\nabla} \cdot \vec{B} = 0$, Gauss's law for magnetism). Inside the magnet, lines point from South to North.
2. **Misconception: Magnetic Force Speeds Up Charged Particles**:
   - *Flawed Action*: Calculating kinetic energy gain of an electron traveling through a uniform magnetic field.
   - *Correct Diagnostic Cue*: $\vec{F}_B \perp \vec{v} \implies P = \vec{F}_B \cdot \vec{v} = 0$. Pure magnetic fields change only the *direction* of velocity, never its magnitude.

### 10.3 Layer 3: Reconstructable TTU Library
#### TTU-MAG-01: Incomplete Cyclotron Orbit Radius Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A proton (m = 1.67 · 10⁻²⁷ kg, q = 1.6 · 10⁻¹⁹ C) enters a uniform B = 0.5 T field perpendicular to velocity at v = 2 · 10⁶ m/s.
Derive and calculate the orbital radius r and time period T.

Step 1: Equate centripetal force to magnetic Lorentz force:
        m · v² / r = q · v · B  =>  r = ( m · [ ___ ] ) / ( [ ___ ] · B )
Step 2: Calculate numeric radius:
        r = (1.67 · 10⁻²⁷ · 2 · 10⁶) / (1.6 · 10⁻¹⁹ · 0.5) = (3.34 · 10⁻²¹) / (0.8 · 10⁻¹⁹) = [ ___ ] m
Step 3: Express time period T:
        T = 2πr / v = (2π · m) / ( [ ___ ] · B )
Step 4: Does T depend on speed v? [ Yes / No ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: r = (m · v) / (q · B)
Step 2: r = 3.34e-21 / 0.8e-19 = 0.04175 m = 4.18 cm
Step 3: T = (2π · m) / (q · B)
Step 4: No (cyclotron resonance principle)
```

#### TTU-MAG-02: Motional EMF & Braking Force TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A conducting rod of length l = 0.5 m, mass m = 0.1 kg, resistance R = 2 Ω slides down frictionless rails at speed v = 4 m/s
in a perpendicular magnetic field B = 1.2 T.
Find the induced EMF, current, magnetic braking force, and power dissipation.

Step 1: Induced motional EMF: E = B · l · v = 1.2 · 0.5 · 4 = [ ___ ] V
Step 2: Induced current: I = E / R = [ ___ ] / 2 = [ ___ ] A
Step 3: Magnetic braking force: F_mag = I · l · B = [ ___ ] · 0.5 · 1.2 = [ ___ ] N
Step 4: Mechanical power converted to heat: P = F_mag · v = I² · R = [ ___ ] W

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: E = 2.4 V
Step 2: I = 2.4 / 2 = 1.2 A
Step 3: F_mag = 1.2 · 0.5 · 1.2 = 0.72 N
Step 4: P = 0.72 · 4 = 2.88 W (checks with I²R = 1.2² · 2 = 1.44 · 2 = 2.88 W)
```

### 10.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-MAG-01` (`CBSE_BOARD`): Magnetic field around straight conductor, solenoid, Fleming's left hand and right hand rules.
- `FAMILY-MAG-02` (`JEE_MAIN`): Cyclotron orbit, velocity selector with crossed E and B fields, motional EMF on rotating conducting rods.

---

## 11. Foundation Packet: Vector Mechanics & Resolving Components (`PHY-VEC-ADD-SUB`)

### 11.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-VEC-ADD-SUB`
- **Learner Title**: Vector Algebra: Addition, Subtraction, Resolution & Scalar/Vector Products
- **Grade Span**: Grade 11 (Foundational Engineering Mechanics)
- **Non-Negotiable Preconditions**:
  1. **Vector Addition Commutativity & Parallelogram Law**: Vectors add geometrically ($\vec{A} + \vec{B} = \vec{B} + \vec{A}$). The magnitude of resultant is $R = \sqrt{A^2 + B^2 + 2AB\cos\theta}$. Scalars and vectors cannot be added together.
  2. **Coordinate Invariance of Dot and Cross Products**: The dot product $\vec{A} \cdot \vec{B} = A B \cos\theta$ is a coordinate-invariant scalar. The cross product $\vec{A} \times \vec{B} = A B \sin\theta\,\hat{n}$ is an axial vector perpendicular to both $\vec{A}$ and $\vec{B}$.

### 11.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-VEC-01` (`CONCEPT`): Vector representation: magnitude and direction; unit vector $\hat{a} = \frac{\vec{A}}{|\vec{A}|}$.
- `ATOM-VEC-02` (`RELATION`): Cartesian decomposition: $\vec{A} = A_x\hat{i} + A_y\hat{j} + A_z\hat{k}$ where $A_x = A\cos\alpha, A_y = A\cos\beta, A_z = A\cos\gamma$.
- `ATOM-VEC-03` (`INVARIANT`): Direction cosines identity: $\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1$.
- `ATOM-VEC-04` (`PROCEDURE`): Evaluating cross product via determinant: $\vec{A} \times \vec{B} = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ A_x & A_y & A_z \\ B_x & B_y & B_z \end{vmatrix}$.
- `ATOM-VEC-05` (`STRATEGY`): Choosing rotated coordinate axes aligned with constraints (such as ramp inclination) to decouple equations of motion.

#### Misconception Contrasts
1. **Misconception: Cross Product Commutativity**:
   - *Flawed Action*: Writing $\vec{A} \times \vec{B} = \vec{B} \times \vec{A}$.
   - *Correct Diagnostic Cue*: Cross product is anti-commutative: $\vec{A} \times \vec{B} = -(\vec{B} \times \vec{A})$. Reversing operand order flips the normal vector direction.
2. **Misconception: Division by Vectors**:
   - *Flawed Action*: Attempting to compute $\frac{\vec{A}}{\vec{B}}$ to find a vector.
   - *Correct Diagnostic Cue*: Division by a vector is undefined because multiple vectors can produce the same dot or cross product result.

### 11.3 Layer 3: Reconstructable TTU Library
#### TTU-VEC-01: Incomplete Vector Resolution & Resultant Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Vector A has magnitude 10 at 30° above positive x-axis. Vector B has magnitude 6 along positive y-axis.
Find resultant vector R = A + B in component and magnitude-direction form.

Step 1: Resolve vector A:
        A_x = 10 · cos(30°) = 10 · [ ___ ] = [ ___ ]
        A_y = 10 · sin(30°) = 10 · [ ___ ] = [ ___ ]
Step 2: Resolve vector B:
        B_x = [ ___ ],  B_y = [ ___ ]
Step 3: Add components:
        R_x = A_x + B_x = [ ___ ] + [ ___ ] = [ ___ ]
        R_y = A_y + B_y = [ ___ ] + [ ___ ] = [ ___ ]
Step 4: Magnitude: |R| = √( R_x² + R_y² ) = √( [ ___ ]² + [ ___ ]² ) = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: A_x = 10 · 0.866 = 8.66; A_y = 10 · 0.5 = 5.0
Step 2: B_x = 0; B_y = 6.0
Step 3: R_x = 8.66 + 0 = 8.66; R_y = 5.0 + 6.0 = 11.0
Step 4: |R| = √(8.66² + 11²) = √(75 + 121) = √196 = 14.0
```

#### TTU-VEC-02: Cross Product & Torque Vector TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A force F = (2i + 3j - k) N acts at position r = (4i - j + 2k) m.
Find torque vector τ = r × F and angle between r and F.

Step 1: Set up determinant:
        τ = i( (-1)(-1) - (2)(3) ) - j( (4)(-1) - (2)(2) ) + k( (4)(3) - (-1)(2) )
Step 2: Evaluate components:
        τ_x = 1 - 6 = [ ___ ]
        τ_y = - (-4 - 4) = [ ___ ]
        τ_z = 12 - (-2) = [ ___ ]
        τ = [ ___ ]i + [ ___ ]j + [ ___ ]k N·m
Step 3: Calculate dot product r · F:
        r · F = (4)(2) + (-1)(3) + (2)(-1) = 8 - 3 - 2 = [ ___ ] J

[COMPLETION KEY - VERIFICATION ONLY]
Step 2: τ_x = -5, τ_y = 8, τ_z = 14; τ = -5i + 8j + 14k N·m
Step 3: r · F = 3 J
```

### 11.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-VEC-01` (`CBSE_BOARD`): Parallelogram law of vector addition, resolving force on inclined plane.
- `FAMILY-VEC-02` (`JEE_MAIN`): Torque and angular momentum vector cross products, unit normal vector to planes.

---

## 12. Foundation Packet: Rotational Dynamics & Angular Momentum Conservation (`PHY-ROT-RIGID-BODY`)

### 12.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-ROT-RIGID-BODY`
- **Learner Title**: Rotational Dynamics: Moment of Inertia, Torque & Angular Momentum Conservation
- **Grade Span**: Grade 11 (Rigid Body Mechanics & Rolling Motion)
- **Non-Negotiable Preconditions**:
  1. **Angular Momentum Origin Precondition**: Angular momentum $\vec{L} = \vec{r} \times \vec{p}$ and torque $\vec{\tau} = \vec{r} \times \vec{F}$ **must always be defined with respect to the same specified origin point**. Shifting the origin changes both torque and angular momentum.
  2. **Rolling Without Slipping Condition**: Pure rolling on a stationary surface requires the contact point instantaneous velocity to be zero: $v_{\text{cm}} = \omega R$. Static friction performs zero net work during pure rolling.

### 12.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-ROT-01` (`CONCEPT`): Moment of inertia as rotational inertia: $I = \int r^2 dm$; parallel axis theorem $I = I_{\text{cm}} + M d^2$; perpendicular axis theorem $I_z = I_x + I_y$ for laminar bodies.
- `ATOM-ROT-02` (`RELATION`): Rotational analogue of Newton's second law: $\vec{\tau}_{\text{ext}} = I\vec{\alpha} = \frac{d\vec{L}}{dt}$.
- `ATOM-ROT-03` (`INVARIANT`): Conservation of angular momentum: $\sum \vec{\tau}_{\text{ext}} = 0 \implies \vec{L}_{\text{total}} = \text{const} \implies I_1 \omega_1 = I_2 \omega_2$.
- `ATOM-ROT-04` (`PROCEDURE`): Total kinetic energy of rolling body: $K_{\text{total}} = K_{\text{trans}} + K_{\text{rot}} = \frac{1}{2}M v_{\text{cm}}^2 + \frac{1}{2}I_{\text{cm}}\omega^2 = \frac{1}{2}M v_{\text{cm}}^2\left(1 + \frac{k^2}{R^2}\right)$.
- `ATOM-ROT-05` (`STRATEGY`): Analyzing acceleration down an incline: $a_{\text{cm}} = \frac{g\sin\theta}{1 + I_{\text{cm}}/(MR^2)}$.

#### Misconception Contrasts
1. **Misconception: Friction Always Opposes Rolling Motion**:
   - *Flawed Action*: Assuming friction always points backward on a rolling cylinder or bicycle wheel.
   - *Correct Diagnostic Cue*: Static friction opposes relative slippage between surfaces. On the rear driven wheel of a bicycle, friction points *forward*, propelling the bike forward.
2. **Misconception: Conservation of Angular Momentum About Any Point**:
   - *Flawed Action*: Applying $L_i = L_f$ about an origin where an external normal force exerts non-zero torque.
   - *Correct Diagnostic Cue*: Angular momentum is conserved only about an axis or point where the net external torque is zero ($\tau_{\text{ext}} = 0$).

### 12.3 Layer 3: Reconstructable TTU Library
#### TTU-ROT-01: Incomplete Rolling Incline Acceleration Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A solid cylinder (I_cm = 1/2·M·R²) rolls without slipping down an incline of angle θ.
Find its linear acceleration a_cm and compare it with a sliding frictionless block.

Step 1: Write dynamic equations:
        Along incline: M·g·sin(θ) - f_s = M·a_cm
        Torque about CM: f_s · R = I_cm · α = (1/2·M·R²) · (a_cm / R)
Step 2: Solve for friction force f_s:
        f_s = 1/2 · M · a_cm
Step 3: Substitute f_s into linear equation:
        M·g·sin(θ) - 1/2·M·a_cm = M·a_cm
        M·g·sin(θ) = [ ___ ] · M·a_cm
Step 4: Solve for a_cm:
        a_cm = [ ___ ] · g·sin(θ)
        Ratio of rolling cylinder acceleration to sliding block acceleration: [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 3: M·g·sin(θ) = (3/2)·M·a_cm
Step 4: a_cm = (2/3)·g·sin(θ); Ratio = (2/3) ≈ 0.67
```

#### TTU-ROT-02: Angular Momentum Conservation TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A turntable of moment of inertia I1 = 4 kg·m² rotates at ω1 = 30 rpm. A lump of clay of mass m = 1 kg
is dropped at distance r = 0.5 m from the axis of rotation and sticks.
Find the new rotational speed ω2 and the fraction of kinetic energy lost.

Step 1: Moment of inertia of clay: I_clay = m · r² = 1 · (0.5)² = [ ___ ] kg·m²
Step 2: Total final moment of inertia: I_total = I1 + I_clay = 4 + [ ___ ] = [ ___ ] kg·m²
Step 3: Apply angular momentum conservation:
        I1 · ω1 = I_total · ω2  =>  4 · 30 = [ ___ ] · ω2  =>  ω2 = [ ___ ] rpm
Step 4: Fractional kinetic energy loss (K_i - K_f) / K_i:
        K_f / K_i = I1 / I_total = 4 / [ ___ ] = [ ___ ]
        Fraction lost = 1 - [ ___ ] = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: I_clay = 0.25 kg·m²
Step 2: I_total = 4.25 kg·m²
Step 3: 120 = 4.25·ω2 => ω2 = 120/4.25 ≈ 28.24 rpm
Step 4: K_f / K_i = 4 / 4.25 = 16/17 ≈ 0.941; Fraction lost = 1/17 ≈ 5.88%
```

### 12.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-ROT-01` (`CBSE_BOARD`): Moment of inertia formulas for standard geometric shapes, parallel axis theorem.
- `FAMILY-ROT-02` (`JEE_MAIN`): Pure rolling dynamics on inclines, conservation of angular momentum in rotating platforms.

---

## 13. Foundation Packet: Thermodynamics & Heat Engines (`PHY-THERMO-FIRST-SECOND-LAW`)

### 13.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-THERMO-FIRST-SECOND-LAW`
- **Learner Title**: Thermodynamics: First Law, Thermodynamic Cycles & Carnot Efficiency
- **Grade Span**: Grade 11 (Thermal Physics & Heat Engines)
- **Non-Negotiable Preconditions**:
  1. **First Law Sign Convention Precondition**: First Law $\Delta U = Q - W$ where $W = \int P dV$ is work done **by** the system. (Alternatively, IUPAC $\Delta U = Q + W_{\text{on}}$). Consistency in sign convention must be preserved throughout an entire derivation.
  2. **Second Law & Carnot Efficiency Ceiling Invariant**: No heat engine operating between two thermal reservoirs at temperatures $T_H$ and $T_C$ can have an efficiency exceeding the reversible Carnot efficiency: $\eta \le \eta_{\text{Carnot}} = 1 - \frac{T_C}{T_H}$.

### 13.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-THE-01` (`CONCEPT`): Internal energy as state function: $U = \frac{f}{2} n R T$; $\Delta U$ depends only on initial and final states, not path.
- `ATOM-THE-02` (`RELATION`): Work in standard processes:
  - Isobaric: $W = P\Delta V = n R \Delta T$.
  - Isothermal: $W = n R T \ln\left(\frac{V_f}{V_i}\right)$ ($\Delta U = 0 \implies Q = W$).
  - Adiabatic: $P V^\gamma = \text{const}$, $W = \frac{P_i V_i - P_f V_f}{\gamma - 1} = -\Delta U$.
  - Isochoric: $W = 0 \implies Q = \Delta U = n C_v \Delta T$.
- `ATOM-THE-03` (`INVARIANT`): Cyclic process invariant: $\oint dU = 0 \implies Q_{\text{net}} = W_{\text{net}} = \text{Area inside } P\text{-}V \text{ loop}$.
- `ATOM-THE-04` (`PROCEDURE`): Calculating efficiency of cyclic engine: $\eta = \frac{W_{\text{net}}}{Q_{\text{in}}} = 1 - \frac{Q_{\text{out}}}{Q_{\text{in}}}$.
- `ATOM-THE-05` (`STRATEGY`): Identifying degrees of freedom $f$: monoatomic ($f=3, \gamma=5/3$), diatomic ($f=5, \gamma=7/5$).

#### Misconception Contrasts
1. **Misconception: Heat is Contained in a Body**:
   - *Flawed Action*: Saying a hot body "contains more heat" than a cold body.
   - *Correct Diagnostic Cue*: Heat ($Q$) is energy in transit across a boundary due to temperature difference. A body contains *internal energy* ($U$), never heat.
2. **Misconception: Adiabatic Expansion Means Constant Temperature**:
   - *Flawed Action*: Assuming temperature remains constant in adiabatic expansion because $Q = 0$.
   - *Correct Diagnostic Cue*: In adiabatic expansion, $W > 0$ and $Q = 0$. By First Law, $\Delta U = -W < 0 \implies n C_v \Delta T < 0$. Temperature strictly drops during adiabatic expansion.

### 13.3 Layer 3: Reconstructable TTU Library
#### TTU-THE-01: Incomplete P-V Cycle Work & Heat Table (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
1 mole of monoatomic gas (Cv = 3/2 R, Cp = 5/2 R) undergoes cycle:
A (P0, V0) --isobaric--> B (P0, 2V0) --isochoric--> C (P0/2, 2V0) --isothermal--> A (P0, V0).
Complete the thermodynamic table in terms of P0·V0.

Process A -> B (Isobaric):
  W_AB = P0 · (2V0 - V0) = [ ___ ] P0·V0
  ΔU_AB = n·Cv·ΔT = 3/2 · (P0·2V0 - P0·V0) = [ ___ ] P0·V0
  Q_AB = W_AB + ΔU_AB = [ ___ ] P0·V0
Process B -> C (Isochoric):
  W_BC = [ ___ ]
  ΔU_BC = n·Cv·ΔT = 3/2 · (P0/2·2V0 - P0·2V0) = 3/2 · ( -P0·V0 ) = [ ___ ] P0·V0
  Q_BC = ΔU_BC = [ ___ ] P0·V0

[COMPLETION KEY - VERIFICATION ONLY]
Process A -> B: W_AB = 1.0 P0·V0; ΔU_AB = 1.5 P0·V0; Q_AB = 2.5 P0·V0
Process B -> C: W_BC = 0.0; ΔU_BC = -1.5 P0·V0; Q_BC = -1.5 P0·V0
```

#### TTU-THE-02: Carnot Engine Efficiency & Refrigerator COP (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A Carnot heat engine operates between reservoirs at T_H = 500 K and T_C = 300 K, absorbing Q_in = 1000 J per cycle.
Find efficiency η, net work W_net, and coefficient of performance COP if operated as a refrigerator.

Step 1: Carnot efficiency: η = 1 - T_C / T_H = 1 - 300 / 500 = 1 - [ ___ ] = [ ___ ] (or [ ___ ] %)
Step 2: Net work output: W_net = η · Q_in = [ ___ ] · 1000 = [ ___ ] J
Step 3: Waste heat rejected: Q_out = Q_in - W_net = 1000 - [ ___ ] = [ ___ ] J
Step 4: Refrigerator COP: COP = T_C / (T_H - T_C) = 300 / (500 - 300) = 300 / [ ___ ] = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: η = 1 - 0.6 = 0.4 (or 40%)
Step 2: W_net = 0.4 · 1000 = 400 J
Step 3: Q_out = 1000 - 400 = 600 J
Step 4: COP = 300 / 200 = 1.5
```

### 13.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-THE-01` (`CBSE_BOARD`): First law of thermodynamics, molar heat capacities $C_p - C_v = R$, work in isothermal vs adiabatic expansion.
- `FAMILY-THE-02` (`JEE_MAIN`): Efficiency of complex thermodynamic cycles on P-V and T-S diagrams, Carnot theorem limits.

---

## 14. Foundation Packet: Oscillations, Simple Harmonic Motion & Waves (`PHY-OSC-SHM-WAVES`)

### 14.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-OSC-SHM-WAVES`
- **Learner Title**: Oscillations & Waves: Simple Harmonic Motion, Resonance & Wave Speed
- **Grade Span**: Grade 9 (Sound & Waves) &bull; Grade 11 (SHM & Superposition)
- **Non-Negotiable Preconditions**:
  1. **Linear Restoring Force Invariant**: Simple harmonic motion occurs **if and only if** the restoring force is directly proportional to displacement from stable equilibrium: $F = -k x \iff \frac{d^2x}{dt^2} + \omega^2 x = 0$. For a simple pendulum, this requires small angles ($\sin\theta \approx \theta$).
  2. **Wave Propagation Invariant**: Wave speed $v = f\lambda = \frac{\omega}{k}$ is determined solely by the mechanical properties of the medium ($v = \sqrt{T/\mu}$ for strings, $v = \sqrt{B/\rho}$ for fluids), independent of wave amplitude or frequency.

### 14.2 Layer 2: Cognitive Transformations & Learning Atom DAG
- `ATOM-OSC-01` (`CONCEPT`): Kinematics of SHM: $x(t) = A\cos(\omega t + \phi)$, $v(t) = -A\omega\sin(\omega t + \phi)$, $a(t) = -A\omega^2\cos(\omega t + \phi) = -\omega^2 x(t)$.
- `ATOM-OSC-02` (`RELATION`): Total energy in SHM: $E = K + U = \frac{1}{2}m v^2 + \frac{1}{2}k x^2 = \frac{1}{2}k A^2 = \text{const}$.
- `ATOM-OSC-03` (`INVARIANT`): Time period of harmonic oscillator:
  - Spring-mass: $T = 2\pi\sqrt{\frac{m}{k}}$.
  - Simple pendulum: $T = 2\pi\sqrt{\frac{L}{g}}$ (for $\theta \ll 1\text{ rad}$).
- `ATOM-OSC-04` (`PROCEDURE`): Energy oscillation frequency: potential and kinetic energy oscillate between 0 and $E$ at double the mechanical frequency ($f_E = 2f$).
- `ATOM-OSC-05` (`STRATEGY`): Doppler effect frequency shift calculation: $f' = f \left(\frac{v \pm v_o}{v \mp v_s}\right)$.

#### Misconception Contrasts
1. **Misconception: Pendulum Period Depends on Mass or Amplitude**:
   - *Flawed Action*: Thinking a heavier pendulum bob or pulling it back 10 cm instead of 5 cm changes the period.
   - *Correct Diagnostic Cue*: For small oscillations, $T = 2\pi\sqrt{L/g}$, which is completely independent of bob mass $m$ and amplitude $A$.
2. **Misconception: Sound Travels Faster in Air than in Steel**:
   - *Flawed Action*: Assuming sound moves slower in dense solid steel than in light airy gas.
   - *Correct Diagnostic Cue*: Wave speed depends on elasticity over density ($v = \sqrt{E/\rho}$). Although steel is denser than air, its Young's modulus is over 10,000 times higher, making sound travel $\approx 15$ times faster in steel ($\approx 5000\text{ m/s}$) than in air ($\approx 343\text{ m/s}$).

### 14.3 Layer 3: Reconstructable TTU Library
#### TTU-OSC-01: Incomplete SHM Energy & Phase Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A 0.2 kg mass on a spring (k = 80 N/m) oscillates with amplitude A = 0.1 m.
Find angular frequency ω, maximum speed v_max, and displacement x where kinetic energy equals potential energy.

Step 1: Angular frequency: ω = √( k / m ) = √( 80 / 0.2 ) = √( [ ___ ] ) = [ ___ ] rad/s
Step 2: Maximum speed: v_max = A · ω = 0.1 · [ ___ ] = [ ___ ] m/s
Step 3: Total mechanical energy: E = 1/2 · k · A² = 1/2 · 80 · (0.1)² = [ ___ ] J
Step 4: Find x where K = U:
        U = 1/2 · E  =>  1/2 · k · x² = 1/2 · (1/2 · k · A²)  =>  x² = A² / [ ___ ]
        x = ± A / √( [ ___ ] ) = ± 0.1 / [ ___ ] ≈ ± [ ___ ] m

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: ω = √400 = 20 rad/s
Step 2: v_max = 0.1 · 20 = 2.0 m/s
Step 3: E = 0.5 · 80 · 0.01 = 0.4 J
Step 4: x² = A²/2 => x = ± A/√2 = ± 0.1 / 1.414 ≈ ± 0.0707 m
```

#### TTU-OSC-02: Standing Waves in Strings TTU (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
A 1.2 m guitar string with linear density μ = 0.005 kg/m is under tension T = 180 N.
Find wave speed v, fundamental frequency f1, and frequency of the 3rd harmonic f3.

Step 1: Calculate wave speed: v = √( T / μ ) = √( 180 / 0.005 ) = √( [ ___ ] ) = [ ___ ] m/s
Step 2: Fundamental wavelength: λ1 = 2 · L = 2 · 1.2 = [ ___ ] m
Step 3: Fundamental frequency: f1 = v / λ1 = [ ___ ] / 2.4 = [ ___ ] Hz
Step 4: Third harmonic frequency (n = 3):
        f3 = 3 · f1 = 3 · [ ___ ] = [ ___ ] Hz

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: v = √36000 = 189.74 m/s (or exactly 60√10 m/s)
Step 2: λ1 = 2.4 m
Step 3: f1 = 189.74 / 2.4 ≈ 79.06 Hz
Step 4: f3 = 3 · 79.06 ≈ 237.17 Hz
```

### 14.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-OSC-01` (`CBSE_BOARD`): Longitudinal vs transverse waves, echo and reverberation, factors affecting speed of sound.
- `FAMILY-OSC-02` (`JEE_MAIN`): Superposition of perpendicular SHMs (Lissajous figures), resonance in closed and open organ pipes.

---

## 15. Intake Validation Checklist for Future Subtopics

To maintain unbroken architectural consistency, any prospective subtopic packet submitted for admission to the Subtopic Intelligence Library must pass the following 6-point verification gate before merging:

1. **Precondition Audit**: Layer 1 must declare explicit, non-empty coordinate reference frames, physical boundary conditions, and domain validity constraints.
2. **Atomic DAG Completeness**: Layer 2 must declare $\ge 4$ typed learning atoms (`CONCEPT`, `RELATION`, `INVARIANT`, `PROCEDURE`, `STRATEGY`).
3. **Misconception Contrast Pairs**: Layer 2 must document $\ge 2$ misconception pairs featuring explicit `Flawed Action` and `Correct Diagnostic Cue`.
4. **Reconstructable TTU Pairs**: Layer 3 must supply $\ge 2$ TTUs with explicit `[INCOMPLETE STATE` learner scaffolds and matching `[COMPLETION KEY` verification keys.
5. **Exam Family Mapping**: Layer 4 must map into $\ge 2$ recognized examination families (`CBSE_BOARD`, `JEE_MAIN`, `JEE_ADVANCED`, `NSEP_OLYMPIAD`).
6. **Zero Topic Hardcoding**: Runtime engine code must evaluate generic schema structures and contain zero hardcoded topic strings.
