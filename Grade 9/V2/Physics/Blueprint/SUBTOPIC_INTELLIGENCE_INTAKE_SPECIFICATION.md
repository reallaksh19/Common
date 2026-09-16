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

## 15. Foundation Packet: Scalars, Vectors, Magnitude, and Direction (`PHY-VEC-BASICS`)

### 15.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-VEC-BASICS`
- **Learner Title**: Scalars, Vectors, Magnitude, and Direction
- **Chapter / Domain**: Vectors / Motion in a Plane &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **PRECOND-2**:  *Boundary constraint*: Physical model breaks down.

#### Mandatory Physical Invariants
- **Equation `EQ-VEC-MAG-NONNEG`**: $$ — 


### 15.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-VECBAS-01` (`CONCEPT`): A scalar is a physical quantity completely specified by a single real number representing magnitude with appropriate units, obeying ordinary algebra.
- `ATOM-VECBAS-02` (`RELATION`): A vector is a physical quantity possessing both a non-negative magnitude and an intrinsic spatial direction that transforms according to vector algebra.
- `ATOM-VECBAS-03` (`INVARIANT`): Vectors are denoted by an arrow over a symbol or boldface; magnitude is denoted by |A| or A, with |A| >= 0.
- `ATOM-VECBAS-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-VECBAS-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-VEC-CURRENT**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: MISC-VEC-NEG-MAG**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.

---

### 15.3 Layer 3: Reconstructable TTU Library

#### TTU-VECBAS-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Scalars, Vectors, Magnitude, and Direction.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-VECBAS-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Scalars, Vectors, Magnitude, and Direction.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 15.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-VECBAS-01` (`CBSE_BOARD`): Scalars, Vectors, Magnitude, and Direction Standard Core — Standard textbook problem setup.
- `FAMILY-VECBAS-02` (`JEE_MAIN`): Scalars, Vectors, Magnitude, and Direction Multi-Step Synthesis — Competitive transfer challenge.

---
## 16. Foundation Packet: Resolution of Vectors into Orthogonal Components (`PHY-VEC-COMPONENTS`)

### 16.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-VEC-COMPONENTS`
- **Learner Title**: Resolution of Vectors into Orthogonal Components
- **Chapter / Domain**: Vectors / Motion in a Plane &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-VEC-COMP-X`**: $$ — 
- **Equation `EQ-VEC-COMP-Y`**: $$ — 
- **Equation `EQ-VEC-RECON-MAG`**: $$ — 


### 16.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-VECCOMP-01` (`CONCEPT`): Any vector in a 2D plane can be uniquely decomposed into two perpendicular projections along orthogonal axes: A = A_x i + A_y j.
- `ATOM-VECCOMP-02` (`RELATION`): Dimensionless vectors of unit magnitude (i, j, k) specifying spatial axis directions.
- `ATOM-VECCOMP-03` (`INVARIANT`): Scalar components A_x and A_y are signed real numbers depending on alignment with declared positive axes.
- `ATOM-VECCOMP-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-VECCOMP-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-VEC-COS-ALWAYS-X**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Resolution of Vectors into Orthogonal Components**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 16.3 Layer 3: Reconstructable TTU Library

#### TTU-VECCOMP-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Resolution of Vectors into Orthogonal Components.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-VECCOMP-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Resolution of Vectors into Orthogonal Components.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 16.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-VECCOMP-01` (`CBSE_BOARD`): Resolution of Vectors into Orthogonal Components Standard Core — Standard textbook problem setup.
- `FAMILY-VECCOMP-02` (`JEE_MAIN`): Resolution of Vectors into Orthogonal Components Advanced Transfer — Competitive entrance examination problem.

---
## 17. Foundation Packet: Force as an Interaction between Bodies (`PHY-NLM-INTERACTION`)

### 17.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-INTERACTION`
- **Learner Title**: Force as an Interaction between Bodies
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-FNET`**: $$ — 


### 17.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMINT-01` (`CONCEPT`): A force is a vector push or pull exerted by one identifiable physical body on another body as a result of an interaction.
- `ATOM-NLMINT-02` (`RELATION`): Every genuine force requires an explicit agent (causer) and receiver (object acted on): F_{on Receiver by Agent}.
- `ATOM-NLMINT-03` (`INVARIANT`): Forces are strictly contact forces (requiring physical contact) or field forces (action at a distance).
- `ATOM-NLMINT-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMINT-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-FORCE-OF-MOTION**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Force as an Interaction between Bodies**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 17.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMINT-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Force as an Interaction between Bodies.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMINT-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Force as an Interaction between Bodies.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 17.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMINT-01` (`CBSE_BOARD`): Force as an Interaction between Bodies Standard Core — Standard textbook problem setup.
- `FAMILY-NLMINT-02` (`JEE_MAIN`): Force as an Interaction between Bodies Multi-Step Synthesis — Competitive transfer challenge.

---
## 18. Foundation Packet: Free-Body Diagrams and System Isolation (`PHY-NLM-FBD`)

### 18.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-FBD`
- **Learner Title**: Free-Body Diagrams and System Isolation
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-FBD-SUM`**: $$ — 


### 18.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMFBD-01` (`CONCEPT`): A system is isolated by defining an imaginary closed boundary around the body of interest, severing all external connections.
- `ATOM-NLMFBD-02` (`RELATION`): An FBD represents the isolated body showing ALL external forces acting ON that body as directed vectors.
- `ATOM-NLMFBD-03` (`INVARIANT`): An FBD must contain ONLY forces exerted ON the isolated body BY external agents. Forces exerted BY the body are strictly prohibited.
- `ATOM-NLMFBD-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMFBD-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-FBD-MA-FORCE**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: MISC-NLM-FBD-PAIR-ON-ONE**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.

---

### 18.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMFBD-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Free-Body Diagrams and System Isolation.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMFBD-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Free-Body Diagrams and System Isolation.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 18.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMFBD-01` (`CBSE_BOARD`): Free-Body Diagrams and System Isolation Standard Core — Standard textbook problem setup.
- `FAMILY-NLMFBD-02` (`JEE_MAIN`): Free-Body Diagrams and System Isolation Multi-Step Synthesis — Competitive transfer challenge.

---
## 19. Foundation Packet: Newton's Second Law of Motion (`PHY-NLM-SECOND-LAW`)

### 19.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-SECOND-LAW`
- **Learner Title**: Newton's Second Law of Motion
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-NEWTON2-COMP-X`**: $$ — 
- **Equation `EQ-NLM-NEWTON2-COMP-Y`**: $$ — 


### 19.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMTWO-01` (`CONCEPT`): The net external force on a body equals the time rate of change of its linear momentum: F_net = dp/dt.
- `ATOM-NLMTWO-02` (`RELATION`): For constant mass, sum F = m*a. Acceleration is directly proportional to net force and points strictly in net force direction.
- `ATOM-NLMTWO-03` (`INVARIANT`): Vector sum F = m*a decouples into independent equations: sum F_x = m*a_x and sum F_y = m*a_y.
- `ATOM-NLMTWO-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMTWO-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-A-DIR-VEL**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: MISC-NLM-SCALAR-FMA**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.

---

### 19.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMTWO-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Newton's Second Law of Motion.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMTWO-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Newton's Second Law of Motion.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 19.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMTWO-01` (`CBSE_BOARD`): Newton's Second Law of Motion Standard Core — Standard textbook problem setup.
- `FAMILY-NLMTWO-02` (`JEE_MAIN`): Newton's Second Law of Motion Multi-Step Synthesis — Competitive transfer challenge.

---
## 20. Foundation Packet: Newton's Third Law of Motion (`PHY-NLM-THIRD-LAW`)

### 20.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-THIRD-LAW`
- **Learner Title**: Newton's Third Law of Motion
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-NEWTON3-PAIR`**: $$ — 


### 20.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMTHREE-01` (`CONCEPT`): To every action there is always an equal and opposite reaction: F_AB = -F_BA.
- `ATOM-NLMTHREE-02` (`RELATION`): Action and reaction forces act strictly on two different bodies; they NEVER act on the same body.
- `ATOM-NLMTHREE-03` (`INVARIANT`): An action-reaction pair consists of forces of the exact same physical nature (both gravitational, both normal, etc.).
- `ATOM-NLMTHREE-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMTHREE-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-NORMAL-WEIGHT-PAIR**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: MISC-NLM-HORSE-CART**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.

---

### 20.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMTHREE-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Newton's Third Law of Motion.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMTHREE-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Newton's Third Law of Motion.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 20.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMTHREE-01` (`CBSE_BOARD`): Newton's Third Law of Motion Standard Core — Standard textbook problem setup.
- `FAMILY-NLMTHREE-02` (`JEE_MAIN`): Newton's Third Law of Motion Multi-Step Synthesis — Competitive transfer challenge.

---
## 21. Foundation Packet: Normal Contact Force and Surface Constraints (`PHY-NLM-NORMAL`)

### 21.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-NORMAL`
- **Learner Title**: Normal Contact Force and Surface Constraints
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-NORMAL-SOLVE`**: $$ — 


### 21.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMNOR-01` (`CONCEPT`): The normal force N is a contact force exerted by a compressed solid surface on a body, directed perpendicular to the surface.
- `ATOM-NLMNOR-02` (`RELATION`): The normal force is a constraint force self-adjusting to enforce the kinematic condition a_perp = 0.
- `ATOM-NLMNOR-03` (`INVARIANT`): N = mg holds ONLY for solitary body at rest on flat horizontal surface. Under any other conditions, N != mg.
- `ATOM-NLMNOR-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMNOR-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-N-EQUALS-MG**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Normal Contact Force and Surface Constraints**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 21.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMNOR-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Normal Contact Force and Surface Constraints.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMNOR-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Normal Contact Force and Surface Constraints.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 21.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMNOR-01` (`CBSE_BOARD`): Normal Contact Force and Surface Constraints Standard Core — Standard textbook problem setup.
- `FAMILY-NLMNOR-02` (`JEE_MAIN`): Normal Contact Force and Surface Constraints Multi-Step Synthesis — Competitive transfer challenge.

---
## 22. Foundation Packet: Tension in Light Strings and Pulley Systems (`PHY-NLM-TENSION`)

### 22.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-TENSION`
- **Learner Title**: Tension in Light Strings and Pulley Systems
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-ATWOOD-ACCEL`**: $$ — 
- **Equation `EQ-NLM-ATWOOD-TENSION`**: $$ — 


### 22.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMTEN-01` (`CONCEPT`): A flexible string can only pull, never push (T >= 0); tension points away from the body along string line.
- `ATOM-NLMTEN-02` (`RELATION`): An ideal string is massless and inextensible; tension is strictly uniform along its continuous length.
- `ATOM-NLMTEN-03` (`INVARIANT`): Because string is inextensible, connected bodies share acceleration magnitude along constraint path: a1 = a2 = a.
- `ATOM-NLMTEN-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMTEN-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-TENSION-EQUALS-WEIGHT**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Tension in Light Strings and Pulley Systems**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 22.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMTEN-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Tension in Light Strings and Pulley Systems.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMTEN-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Tension in Light Strings and Pulley Systems.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 22.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMTEN-01` (`CBSE_BOARD`): Tension in Light Strings and Pulley Systems Standard Core — Standard textbook problem setup.
- `FAMILY-NLMTEN-02` (`JEE_MAIN`): Tension in Light Strings and Pulley Systems Multi-Step Synthesis — Competitive transfer challenge.

---
## 23. Foundation Packet: Static and Kinetic Friction (`PHY-NLM-FRICTION`)

### 23.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-FRICTION`
- **Learner Title**: Static and Kinetic Friction
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-STATIC-INEQUALITY`**: $$ — 
- **Equation `EQ-NLM-KINETIC`**: $$ — 


### 23.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMFRIC-01` (`CONCEPT`): Static friction prevents relative sliding and is self-adjusting: 0 <= f_s <= f_{s,max} = mu_s * N.
- `ATOM-NLMFRIC-02` (`RELATION`): During active relative sliding, kinetic friction is f_k = mu_k * N, where mu_k <= mu_s.
- `ATOM-NLMFRIC-03` (`INVARIANT`): Friction opposes relative motion between contact surfaces, NOT motion relative to ground.
- `ATOM-NLMFRIC-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMFRIC-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-FRICTION-ALWAYS-MU-N**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: MISC-NLM-FRICTION-OPPOSES-MOTION**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.

---

### 23.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMFRIC-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Static and Kinetic Friction.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMFRIC-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Static and Kinetic Friction.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 23.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMFRIC-01` (`CBSE_BOARD`): Static and Kinetic Friction Standard Core — Standard textbook problem setup.
- `FAMILY-NLMFRIC-02` (`JEE_MAIN`): Static and Kinetic Friction Multi-Step Synthesis — Competitive transfer challenge.

---
## 24. Foundation Packet: Connected Systems and Acceleration Constraints (`PHY-NLM-CONNECTED`)

### 24.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-NLM-CONNECTED`
- **Learner Title**: Connected Systems and Acceleration Constraints
- **Chapter / Domain**: Laws of Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-NLM-WHOLE-SYSTEM`**: $$ — 
- **Equation `EQ-NLM-PULLEY-CONSTRAINT`**: $$ — 


### 24.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-NLMCON-01` (`CONCEPT`): A composite system of multiple bodies can be treated as a single mass M_tot = sum(m_i) accelerated by external forces.
- `ATOM-NLMCON-02` (`RELATION`): Internal forces cancel in pairs by Newton III and do not appear in whole-system equation.
- `ATOM-NLMCON-03` (`INVARIANT`): String length constraint f(x_1, ..., x_n) = L differentiated twice yields acceleration relations.
- `ATOM-NLMCON-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-NLMCON-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-NLM-PULLEY-EQUAL-A**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Connected Systems and Acceleration Constraints**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 24.3 Layer 3: Reconstructable TTU Library

#### TTU-NLMCON-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Connected Systems and Acceleration Constraints.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-NLMCON-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Connected Systems and Acceleration Constraints.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 24.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-NLMCON-01` (`CBSE_BOARD`): Connected Systems and Acceleration Constraints Standard Core — Standard textbook problem setup.
- `FAMILY-NLMCON-02` (`JEE_MAIN`): Connected Systems and Acceleration Constraints Multi-Step Synthesis — Competitive transfer challenge.

---
## 25. Foundation Packet: Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement) (`PHY-KIN-MOTION-GRAPHS`)

### 25.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-KIN-MOTION-GRAPHS`
- **Learner Title**: Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement)
- **Chapter / Domain**: Motion &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-VT-AREA-DISPLACEMENT`**: $$ — 


### 25.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-KINGRAPH-01` (`CONCEPT`): Slope of position-time graph dx/dt equals instantaneous velocity; area under velocity-time graph equals displacement.
- `ATOM-KINGRAPH-02` (`RELATION`): Governing relation.
- `ATOM-KINGRAPH-03` (`INVARIANT`): System invariant.
- `ATOM-KINGRAPH-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-KINGRAPH-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-GRAPH-NEGATIVE-AREA**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement)**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 25.3 Layer 3: Reconstructable TTU Library

#### TTU-KINGRAPH-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement).
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-KINGRAPH-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement).
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 25.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-KINGRAPH-01` (`CBSE_BOARD`): Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement) Standard Core — Standard textbook problem setup.
- `FAMILY-KINGRAPH-02` (`JEE_MAIN`): Motion Graphs: x-t Slope (Velocity) & v-t Area (Displacement) Multi-Step Synthesis — Competitive transfer challenge.

---
## 26. Foundation Packet: Uniform Circular Motion: Centripetal Acceleration & Radial Direction (`PHY-KIN-CIRCULAR-UNIFORM`)

### 26.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-KIN-CIRCULAR-UNIFORM`
- **Learner Title**: Uniform Circular Motion: Centripetal Acceleration & Radial Direction
- **Chapter / Domain**: Motion &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-CENTRIPETAL-ACCEL`**: $$ — 


### 26.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-KINUCM-01` (`CONCEPT`): In uniform circular motion, speed is constant but velocity continuously changes direction, requiring radial inward centripetal acceleration a_c = v^2/r.
- `ATOM-KINUCM-02` (`RELATION`): Governing relation.
- `ATOM-KINUCM-03` (`INVARIANT`): System invariant.
- `ATOM-KINUCM-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-KINUCM-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-CIRCULAR-ZERO-ACCEL**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Uniform Circular Motion: Centripetal Acceleration & Radial Direction**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 26.3 Layer 3: Reconstructable TTU Library

#### TTU-KINUCM-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Uniform Circular Motion: Centripetal Acceleration & Radial Direction.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-KINUCM-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Uniform Circular Motion: Centripetal Acceleration & Radial Direction.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 26.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-KINUCM-01` (`CBSE_BOARD`): Uniform Circular Motion: Centripetal Acceleration & Radial Direction Standard Core — Standard textbook problem setup.
- `FAMILY-KINUCM-02` (`JEE_MAIN`): Uniform Circular Motion: Centripetal Acceleration & Radial Direction Multi-Step Synthesis — Competitive transfer challenge.

---
## 27. Foundation Packet: Newton's Three Laws: Inertia, F=ma & Action-Reaction (`PHY-FORCE-NEWTON-LAWS`)

### 27.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-FORCE-NEWTON-LAWS`
- **Learner Title**: Newton's Three Laws: Inertia, F=ma & Action-Reaction
- **Chapter / Domain**: Force and Laws of Motion &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-NEWTON-SECOND`**: $$ — 


### 27.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-FORCENL-01` (`CONCEPT`): First law defines inertia; Second law F_net = ma equates net external force to rate of change of momentum; Third law states mutual forces between bodies are equal and opposite.
- `ATOM-FORCENL-02` (`RELATION`): Governing relation.
- `ATOM-FORCENL-03` (`INVARIANT`): System invariant.
- `ATOM-FORCENL-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-FORCENL-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-FORCE-OF-MOTION**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Newton's Three Laws: Inertia, F=ma & Action-Reaction**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 27.3 Layer 3: Reconstructable TTU Library

#### TTU-FORCENL-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Newton's Three Laws: Inertia, F=ma & Action-Reaction.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-FORCENL-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Newton's Three Laws: Inertia, F=ma & Action-Reaction.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 27.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-FORCENL-01` (`CBSE_BOARD`): Newton's Three Laws: Inertia, F=ma & Action-Reaction Standard Core — Standard textbook problem setup.
- `FAMILY-FORCENL-02` (`JEE_MAIN`): Newton's Three Laws: Inertia, F=ma & Action-Reaction Multi-Step Synthesis — Competitive transfer challenge.

---
## 28. Foundation Packet: Momentum, Impulse & Conservation of Linear Momentum (`PHY-FORCE-MOMENTUM-IMPULSE`)

### 28.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-FORCE-MOMENTUM-IMPULSE`
- **Learner Title**: Momentum, Impulse & Conservation of Linear Momentum
- **Chapter / Domain**: Force and Laws of Motion &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-MOMENTUM-CONSERVE`**: $$ — 


### 28.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-FORCEMOM-01` (`CONCEPT`): Total linear momentum of an isolated system is conserved: Sigma p_initial = Sigma p_final when F_ext_net = 0; Impulse J = integral F dt = Delta p.
- `ATOM-FORCEMOM-02` (`RELATION`): Governing relation.
- `ATOM-FORCEMOM-03` (`INVARIANT`): System invariant.
- `ATOM-FORCEMOM-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-FORCEMOM-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-SCALAR-MOMENTUM**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Momentum, Impulse & Conservation of Linear Momentum**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 28.3 Layer 3: Reconstructable TTU Library

#### TTU-FORCEMOM-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Momentum, Impulse & Conservation of Linear Momentum.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-FORCEMOM-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Momentum, Impulse & Conservation of Linear Momentum.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 28.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-FORCEMOM-01` (`CBSE_BOARD`): Momentum, Impulse & Conservation of Linear Momentum Standard Core — Standard textbook problem setup.
- `FAMILY-FORCEMOM-02` (`JEE_MAIN`): Momentum, Impulse & Conservation of Linear Momentum Multi-Step Synthesis — Competitive transfer challenge.

---
## 29. Foundation Packet: Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight (`PHY-GRAV-FREE-FALL`)

### 29.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-GRAV-FREE-FALL`
- **Learner Title**: Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight
- **Chapter / Domain**: Gravitation &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-FREE-FALL-HEIGHT`**: $$ — 


### 29.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-GRAVFF-01` (`CONCEPT`): Under gravity alone (no air resistance), vertical throw has acceleration -g throughout; ascent time equals descent time, and velocity at return equals -u.
- `ATOM-GRAVFF-02` (`RELATION`): Governing relation.
- `ATOM-GRAVFF-03` (`INVARIANT`): System invariant.
- `ATOM-GRAVFF-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-GRAVFF-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-ZERO-ACCEL-APEX**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 29.3 Layer 3: Reconstructable TTU Library

#### TTU-GRAVFF-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-GRAVFF-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 29.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-GRAVFF-01` (`CBSE_BOARD`): Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight Standard Core — Standard textbook problem setup.
- `FAMILY-GRAVFF-02` (`JEE_MAIN`): Free Fall: Trajectory Symmetry, Maximum Height & Time of Flight Multi-Step Synthesis — Competitive transfer challenge.

---
## 30. Foundation Packet: Buoyancy, Archimedes' Principle & Floatation Equilibrium (`PHY-FLUID-BUOYANCY-ARCHIMEDES`)

### 30.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-FLUID-BUOYANCY-ARCHIMEDES`
- **Learner Title**: Buoyancy, Archimedes' Principle & Floatation Equilibrium
- **Chapter / Domain**: Gravitation &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-ARCHIMEDES-BUOYANCY`**: $$ — 


### 30.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-FLUIDBUOY-01` (`CONCEPT`): Upward buoyant force equals weight of displaced fluid: F_b = rho_fluid * V_submerged * g; body floats in equilibrium when F_b = W_body.
- `ATOM-FLUIDBUOY-02` (`RELATION`): Governing relation.
- `ATOM-FLUIDBUOY-03` (`INVARIANT`): System invariant.
- `ATOM-FLUIDBUOY-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-FLUIDBUOY-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-BUOYANCY-BODY-DENSITY**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Buoyancy, Archimedes' Principle & Floatation Equilibrium**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 30.3 Layer 3: Reconstructable TTU Library

#### TTU-FLUIDBUOY-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Buoyancy, Archimedes' Principle & Floatation Equilibrium.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-FLUIDBUOY-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Buoyancy, Archimedes' Principle & Floatation Equilibrium.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 30.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-FLUIDBUOY-01` (`CBSE_BOARD`): Buoyancy, Archimedes' Principle & Floatation Equilibrium Standard Core — Standard textbook problem setup.
- `FAMILY-FLUIDBUOY-02` (`JEE_MAIN`): Buoyancy, Archimedes' Principle & Floatation Equilibrium Multi-Step Synthesis — Competitive transfer challenge.

---
## 31. Foundation Packet: Conservation of Mechanical Energy & Rate of Work (Power) (`PHY-ENERGY-CONSERVATION-LAW`)

### 31.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-ENERGY-CONSERVATION-LAW`
- **Learner Title**: Conservation of Mechanical Energy & Rate of Work (Power)
- **Chapter / Domain**: Work and Energy &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-ENERGY-CONSERVATION`**: $$ — 


### 31.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-ENERGCONS-01` (`CONCEPT`): In conservative force fields (gravity, springs), total mechanical energy E = KE + PE is constant; Power P = dW/dt = F * v measures energy transfer rate.
- `ATOM-ENERGCONS-02` (`RELATION`): Governing relation.
- `ATOM-ENERGCONS-03` (`INVARIANT`): System invariant.
- `ATOM-ENERGCONS-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-ENERGCONS-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-ENERGY-FRICTION-CONSERVE**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Conservation of Mechanical Energy & Rate of Work (Power)**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 31.3 Layer 3: Reconstructable TTU Library

#### TTU-ENERGCONS-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Conservation of Mechanical Energy & Rate of Work (Power).
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-ENERGCONS-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Conservation of Mechanical Energy & Rate of Work (Power).
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 31.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-ENERGCONS-01` (`CBSE_BOARD`): Conservation of Mechanical Energy & Rate of Work (Power) Standard Core — Standard textbook problem setup.
- `FAMILY-ENERGCONS-02` (`JEE_MAIN`): Conservation of Mechanical Energy & Rate of Work (Power) Multi-Step Synthesis — Competitive transfer challenge.

---
## 32. Foundation Packet: Sound: Longitudinal Compression Waves, Speed & Echo (`PHY-SOUND-LONGITUDINAL-WAVES`)

### 32.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-SOUND-LONGITUDINAL-WAVES`
- **Learner Title**: Sound: Longitudinal Compression Waves, Speed & Echo
- **Chapter / Domain**: Sound &bull; Grade 9
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-WAVE-SPEED`**: $$ — 


### 32.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-SOUNDWAVE-01` (`CONCEPT`): Sound is a mechanical longitudinal wave requiring a material medium, propagating via alternating compressions (high pressure/density) and rarefactions; v = f * lambda; echo requires min distance 17.2m in air.
- `ATOM-SOUNDWAVE-02` (`RELATION`): Governing relation.
- `ATOM-SOUNDWAVE-03` (`INVARIANT`): System invariant.
- `ATOM-SOUNDWAVE-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-SOUNDWAVE-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-SOUND-VACUUM**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Sound: Longitudinal Compression Waves, Speed & Echo**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 32.3 Layer 3: Reconstructable TTU Library

#### TTU-SOUNDWAVE-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Sound: Longitudinal Compression Waves, Speed & Echo.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-SOUNDWAVE-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Sound: Longitudinal Compression Waves, Speed & Echo.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 32.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-SOUNDWAVE-01` (`CBSE_BOARD`): Sound: Longitudinal Compression Waves, Speed & Echo Standard Core — Standard textbook problem setup.
- `FAMILY-SOUNDWAVE-02` (`JEE_MAIN`): Sound: Longitudinal Compression Waves, Speed & Echo Multi-Step Synthesis — Competitive transfer challenge.

---
## 33. Foundation Packet: Light Refraction: Snell's Law, Lens Formula & Lens Power (`PHY-OPTICS-REFRACTION-LENSES`)

### 33.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-OPTICS-REFRACTION-LENSES`
- **Learner Title**: Light Refraction: Snell's Law, Lens Formula & Lens Power
- **Chapter / Domain**: Light - Reflection and Refraction &bull; Grade 10
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-LENS-FORMULA`**: $$ — 


### 33.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-OPTREFR-01` (`CONCEPT`): Snell's Law n1 sin(i) = n2 sin(r); Lens Formula 1/v - 1/u = 1/f; Power P = 1/f(meters) in Diopters; convex lens has positive f, concave negative.
- `ATOM-OPTREFR-02` (`RELATION`): Governing relation.
- `ATOM-OPTREFR-03` (`INVARIANT`): System invariant.
- `ATOM-OPTREFR-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-OPTREFR-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-LENS-FORMULA-SIGN**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Light Refraction: Snell's Law, Lens Formula & Lens Power**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 33.3 Layer 3: Reconstructable TTU Library

#### TTU-OPTREFR-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Light Refraction: Snell's Law, Lens Formula & Lens Power.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-OPTREFR-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Light Refraction: Snell's Law, Lens Formula & Lens Power.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 33.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-OPTREFR-01` (`CBSE_BOARD`): Light Refraction: Snell's Law, Lens Formula & Lens Power Standard Core — Standard textbook problem setup.
- `FAMILY-OPTREFR-02` (`JEE_MAIN`): Light Refraction: Snell's Law, Lens Formula & Lens Power Multi-Step Synthesis — Competitive transfer challenge.

---
## 34. Foundation Packet: Human Eye Optics, Accommodation & Vision Defect Corrections (`PHY-OPTICS-HUMAN-EYE`)

### 34.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-OPTICS-HUMAN-EYE`
- **Learner Title**: Human Eye Optics, Accommodation & Vision Defect Corrections
- **Chapter / Domain**: The Human Eye and the Colourful World &bull; Grade 10
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-CORRECTIVE-POWER`**: $$ — 


### 34.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-OPTEYE-01` (`CONCEPT`): Myopia (short-sightedness, image in front of retina) corrected by concave lens; Hypermetropia (far-sightedness, image behind retina) corrected by convex lens.
- `ATOM-OPTEYE-02` (`RELATION`): Governing relation.
- `ATOM-OPTEYE-03` (`INVARIANT`): System invariant.
- `ATOM-OPTEYE-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-OPTEYE-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-MYOPIA-CONVEX**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Human Eye Optics, Accommodation & Vision Defect Corrections**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 34.3 Layer 3: Reconstructable TTU Library

#### TTU-OPTEYE-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Human Eye Optics, Accommodation & Vision Defect Corrections.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-OPTEYE-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Human Eye Optics, Accommodation & Vision Defect Corrections.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 34.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-OPTEYE-01` (`CBSE_BOARD`): Human Eye Optics, Accommodation & Vision Defect Corrections Standard Core — Standard textbook problem setup.
- `FAMILY-OPTEYE-02` (`JEE_MAIN`): Human Eye Optics, Accommodation & Vision Defect Corrections Multi-Step Synthesis — Competitive transfer challenge.

---
## 35. Foundation Packet: Dispersion of Light, Prism Spectrum & Rayleigh Scattering (`PHY-OPTICS-DISPERSION-SCATTERING`)

### 35.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-OPTICS-DISPERSION-SCATTERING`
- **Learner Title**: Dispersion of Light, Prism Spectrum & Rayleigh Scattering
- **Chapter / Domain**: The Human Eye and the Colourful World &bull; Grade 10
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-RAYLEIGH-SCATTERING`**: $$ — 


### 35.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-OPTDISP-01` (`CONCEPT`): Prism decomposes white light into VIBGYOR because refractive index n varies inversely with wavelength lambda (violet bends most); Rayleigh scattering intensity is proportional to 1/lambda^4.
- `ATOM-OPTDISP-02` (`RELATION`): Governing relation.
- `ATOM-OPTDISP-03` (`INVARIANT`): System invariant.
- `ATOM-OPTDISP-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-OPTDISP-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-RED-BENDS-MORE**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Dispersion of Light, Prism Spectrum & Rayleigh Scattering**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 35.3 Layer 3: Reconstructable TTU Library

#### TTU-OPTDISP-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Dispersion of Light, Prism Spectrum & Rayleigh Scattering.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-OPTDISP-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Dispersion of Light, Prism Spectrum & Rayleigh Scattering.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 35.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-OPTDISP-01` (`CBSE_BOARD`): Dispersion of Light, Prism Spectrum & Rayleigh Scattering Standard Core — Standard textbook problem setup.
- `FAMILY-OPTDISP-02` (`JEE_MAIN`): Dispersion of Light, Prism Spectrum & Rayleigh Scattering Multi-Step Synthesis — Competitive transfer challenge.

---
## 36. Foundation Packet: Joule's Law of Heating, Electric Power & Circuit Safety (`PHY-ELEC-POWER-JOULE`)

### 36.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-ELEC-POWER-JOULE`
- **Learner Title**: Joule's Law of Heating, Electric Power & Circuit Safety
- **Chapter / Domain**: Electricity &bull; Grade 10
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-JOULE-HEATING`**: $$ — 


### 36.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-ELECPOW-01` (`CONCEPT`): Heat generated H = I^2 R t; Electrical Power P = V * I = I^2 R = V^2 / R; fuses protect circuits via low melting point Joule heating.
- `ATOM-ELECPOW-02` (`RELATION`): Governing relation.
- `ATOM-ELECPOW-03` (`INVARIANT`): System invariant.
- `ATOM-ELECPOW-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-ELECPOW-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-POWER-FORMULA-MISMATCH**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Joule's Law of Heating, Electric Power & Circuit Safety**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 36.3 Layer 3: Reconstructable TTU Library

#### TTU-ELECPOW-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Joule's Law of Heating, Electric Power & Circuit Safety.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-ELECPOW-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Joule's Law of Heating, Electric Power & Circuit Safety.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 36.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-ELECPOW-01` (`CBSE_BOARD`): Joule's Law of Heating, Electric Power & Circuit Safety Standard Core — Standard textbook problem setup.
- `FAMILY-ELECPOW-02` (`JEE_MAIN`): Joule's Law of Heating, Electric Power & Circuit Safety Multi-Step Synthesis — Competitive transfer challenge.

---
## 37. Foundation Packet: Electromagnetic Induction: Faraday's Laws & Lenz's Law (`PHY-MAG-INDUCTION-FARADAY`)

### 37.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-MAG-INDUCTION-FARADAY`
- **Learner Title**: Electromagnetic Induction: Faraday's Laws & Lenz's Law
- **Chapter / Domain**: Magnetic Effects of Electric Current &bull; Grade 10
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-FARADAYS-LAW`**: $$ — 


### 37.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-MAGIND-01` (`CONCEPT`): Induced EMF epsilon = -dPhi_B / dt is proportional to rate of change of magnetic flux; Lenz's law (negative sign) ensures induced current opposes the flux change (energy conservation).
- `ATOM-MAGIND-02` (`RELATION`): Governing relation.
- `ATOM-MAGIND-03` (`INVARIANT`): System invariant.
- `ATOM-MAGIND-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-MAGIND-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-STATIC-FLUX-INDUCTION**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Electromagnetic Induction: Faraday's Laws & Lenz's Law**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 37.3 Layer 3: Reconstructable TTU Library

#### TTU-MAGIND-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Electromagnetic Induction: Faraday's Laws & Lenz's Law.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-MAGIND-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Electromagnetic Induction: Faraday's Laws & Lenz's Law.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 37.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-MAGIND-01` (`CBSE_BOARD`): Electromagnetic Induction: Faraday's Laws & Lenz's Law Standard Core — Standard textbook problem setup.
- `FAMILY-MAGIND-02` (`JEE_MAIN`): Electromagnetic Induction: Faraday's Laws & Lenz's Law Multi-Step Synthesis — Competitive transfer challenge.

---
## 38. Foundation Packet: 2D Projectile Motion: Component Independence, Range & Trajectory (`PHY-KIN-2D-PROJECTILE`)

### 38.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-KIN-2D-PROJECTILE`
- **Learner Title**: 2D Projectile Motion: Component Independence, Range & Trajectory
- **Chapter / Domain**: Motion in a Plane &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-PROJECTILE-RANGE`**: $$ — 


### 38.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-KINPROJ-01` (`CONCEPT`): Horizontal motion (ax = 0, constant velocity ux) and vertical motion (ay = -g, free fall) are completely independent; Range R = u^2 sin(2 theta)/g.
- `ATOM-KINPROJ-02` (`RELATION`): Governing relation.
- `ATOM-KINPROJ-03` (`INVARIANT`): System invariant.
- `ATOM-KINPROJ-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-KINPROJ-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-PROJECTILE-GRAVITY-HORIZONTAL**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in 2D Projectile Motion: Component Independence, Range & Trajectory**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 38.3 Layer 3: Reconstructable TTU Library

#### TTU-KINPROJ-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for 2D Projectile Motion: Component Independence, Range & Trajectory.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-KINPROJ-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for 2D Projectile Motion: Component Independence, Range & Trajectory.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 38.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-KINPROJ-01` (`CBSE_BOARD`): 2D Projectile Motion: Component Independence, Range & Trajectory Standard Core — Standard textbook problem setup.
- `FAMILY-KINPROJ-02` (`JEE_MAIN`): 2D Projectile Motion: Component Independence, Range & Trajectory Multi-Step Synthesis — Competitive transfer challenge.

---
## 39. Foundation Packet: Circular Motion Dynamics: Centripetal Force & Banking of Roads (`PHY-KIN-CIRCULAR-DYNAMICS`)

### 39.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-KIN-CIRCULAR-DYNAMICS`
- **Learner Title**: Circular Motion Dynamics: Centripetal Force & Banking of Roads
- **Chapter / Domain**: Motion in a Plane &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-BANKING-ANGLE`**: $$ — 


### 39.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-KINCIRC-01` (`CONCEPT`): Centripetal force is provided by real physical forces (friction, normal component); optimum banking angle without friction is tan(theta) = v^2 / (r * g).
- `ATOM-KINCIRC-02` (`RELATION`): Governing relation.
- `ATOM-KINCIRC-03` (`INVARIANT`): System invariant.
- `ATOM-KINCIRC-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-KINCIRC-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-CENTRIFUGAL-INERTIAL**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Circular Motion Dynamics: Centripetal Force & Banking of Roads**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 39.3 Layer 3: Reconstructable TTU Library

#### TTU-KINCIRC-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Circular Motion Dynamics: Centripetal Force & Banking of Roads.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-KINCIRC-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Circular Motion Dynamics: Centripetal Force & Banking of Roads.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 39.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-KINCIRC-01` (`CBSE_BOARD`): Circular Motion Dynamics: Centripetal Force & Banking of Roads Standard Core — Standard textbook problem setup.
- `FAMILY-KINCIRC-02` (`JEE_MAIN`): Circular Motion Dynamics: Centripetal Force & Banking of Roads Multi-Step Synthesis — Competitive transfer challenge.

---
## 40. Foundation Packet: Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction (`PHY-KIN-RELATIVE-2D`)

### 40.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-KIN-RELATIVE-2D`
- **Learner Title**: Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction
- **Chapter / Domain**: Motion in a Plane &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-RELATIVE-VELOCITY`**: $$ — 


### 40.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-KINREL-01` (`CONCEPT`): Relative velocity of body A with respect to B is v_AB = v_A - v_B; river crossing time depends only on perpendicular velocity component.
- `ATOM-KINREL-02` (`RELATION`): Governing relation.
- `ATOM-KINREL-03` (`INVARIANT`): System invariant.
- `ATOM-KINREL-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-KINREL-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-RIVER-CROSSING-DRIFT**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 40.3 Layer 3: Reconstructable TTU Library

#### TTU-KINREL-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-KINREL-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 40.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-KINREL-01` (`CBSE_BOARD`): Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction Standard Core — Standard textbook problem setup.
- `FAMILY-KINREL-02` (`JEE_MAIN`): Relative Velocity in 2D: River-Boat, Rain-Man & Vector Subtraction Multi-Step Synthesis — Competitive transfer challenge.

---
## 41. Foundation Packet: Work Done by Variable Forces, Conservative Fields & Potential Energy (`PHY-WEP-VARIABLE-FORCE`)

### 41.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-WEP-VARIABLE-FORCE`
- **Learner Title**: Work Done by Variable Forces, Conservative Fields & Potential Energy
- **Chapter / Domain**: Work, Energy and Power &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-SPRING-WORK`**: $$ — 


### 41.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-WEPVAR-01` (`CONCEPT`): Work done by variable force is line integral W = int F dx; for conservative forces F = -dU/dx, and mechanical energy is conserved Delta KE + Delta PE = 0.
- `ATOM-WEPVAR-02` (`RELATION`): Governing relation.
- `ATOM-WEPVAR-03` (`INVARIANT`): System invariant.
- `ATOM-WEPVAR-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-WEPVAR-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-SPRING-WORK-LINEAR**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Work Done by Variable Forces, Conservative Fields & Potential Energy**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 41.3 Layer 3: Reconstructable TTU Library

#### TTU-WEPVAR-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Work Done by Variable Forces, Conservative Fields & Potential Energy.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-WEPVAR-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Work Done by Variable Forces, Conservative Fields & Potential Energy.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 41.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-WEPVAR-01` (`CBSE_BOARD`): Work Done by Variable Forces, Conservative Fields & Potential Energy Standard Core — Standard textbook problem setup.
- `FAMILY-WEPVAR-02` (`JEE_MAIN`): Work Done by Variable Forces, Conservative Fields & Potential Energy Multi-Step Synthesis — Competitive transfer challenge.

---
## 42. Foundation Packet: Centre of Mass: Discrete & Continuous Systems, Motion of COM (`PHY-SYS-CENTRE-MASS`)

### 42.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-SYS-CENTRE-MASS`
- **Learner Title**: Centre of Mass: Discrete & Continuous Systems, Motion of COM
- **Chapter / Domain**: System of Particles and Rotational Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-COM-MOTION`**: $$ — 


### 42.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-SYSCM-01` (`CONCEPT`): Position r_cm = (Sigma m_i r_i) / M; internal forces cancel in pairs so total external force governs COM acceleration: F_ext = M a_cm.
- `ATOM-SYSCM-02` (`RELATION`): Governing relation.
- `ATOM-SYSCM-03` (`INVARIANT`): System invariant.
- `ATOM-SYSCM-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-SYSCM-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-COM-EXPLOSION-DEFLECTION**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Centre of Mass: Discrete & Continuous Systems, Motion of COM**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 42.3 Layer 3: Reconstructable TTU Library

#### TTU-SYSCM-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Centre of Mass: Discrete & Continuous Systems, Motion of COM.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-SYSCM-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Centre of Mass: Discrete & Continuous Systems, Motion of COM.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 42.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-SYSCM-01` (`CBSE_BOARD`): Centre of Mass: Discrete & Continuous Systems, Motion of COM Standard Core — Standard textbook problem setup.
- `FAMILY-SYSCM-02` (`JEE_MAIN`): Centre of Mass: Discrete & Continuous Systems, Motion of COM Multi-Step Synthesis — Competitive transfer challenge.

---
## 43. Foundation Packet: Angular Momentum Conservation & Pure Rolling Motion (`PHY-ROT-ANGULAR-MOMENTUM`)

### 43.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-ROT-ANGULAR-MOMENTUM`
- **Learner Title**: Angular Momentum Conservation & Pure Rolling Motion
- **Chapter / Domain**: System of Particles and Rotational Motion &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-PURE-ROLLING`**: $$ — 


### 43.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-ROTAM-01` (`CONCEPT`): Angular momentum L = I omega = r x p is conserved when net external torque tau_ext = 0; pure rolling requires v_cm = R * omega and point of contact at instantaneous rest.
- `ATOM-ROTAM-02` (`RELATION`): Governing relation.
- `ATOM-ROTAM-03` (`INVARIANT`): System invariant.
- `ATOM-ROTAM-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-ROTAM-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-ROLLING-WORK-FRICTION**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Angular Momentum Conservation & Pure Rolling Motion**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 43.3 Layer 3: Reconstructable TTU Library

#### TTU-ROTAM-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Angular Momentum Conservation & Pure Rolling Motion.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-ROTAM-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Angular Momentum Conservation & Pure Rolling Motion.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 43.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-ROTAM-01` (`CBSE_BOARD`): Angular Momentum Conservation & Pure Rolling Motion Standard Core — Standard textbook problem setup.
- `FAMILY-ROTAM-02` (`JEE_MAIN`): Angular Momentum Conservation & Pure Rolling Motion Multi-Step Synthesis — Competitive transfer challenge.

---
## 44. Foundation Packet: Kepler's Laws, Orbital Mechanics & Escape Velocity (`PHY-GRAV-PLANETARY-ORBITS`)

### 44.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-GRAV-PLANETARY-ORBITS`
- **Learner Title**: Kepler's Laws, Orbital Mechanics & Escape Velocity
- **Chapter / Domain**: Gravitation &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-ESCAPE-VELOCITY`**: $$ — 


### 44.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-GRAVORB-01` (`CONCEPT`): Kepler's 3 laws (ellipses, equal areas in equal time dA/dt = L/(2m) = const, T^2 proportional to a^3); orbital speed v_o = sqrt(GM/r); escape velocity v_e = sqrt(2GM/R) = sqrt(2) v_o.
- `ATOM-GRAVORB-02` (`RELATION`): Governing relation.
- `ATOM-GRAVORB-03` (`INVARIANT`): System invariant.
- `ATOM-GRAVORB-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-GRAVORB-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-ESCAPE-MASS-DEPENDENCE**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Kepler's Laws, Orbital Mechanics & Escape Velocity**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 44.3 Layer 3: Reconstructable TTU Library

#### TTU-GRAVORB-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Kepler's Laws, Orbital Mechanics & Escape Velocity.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-GRAVORB-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Kepler's Laws, Orbital Mechanics & Escape Velocity.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 44.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-GRAVORB-01` (`CBSE_BOARD`): Kepler's Laws, Orbital Mechanics & Escape Velocity Standard Core — Standard textbook problem setup.
- `FAMILY-GRAVORB-02` (`JEE_MAIN`): Kepler's Laws, Orbital Mechanics & Escape Velocity Multi-Step Synthesis — Competitive transfer challenge.

---
## 45. Foundation Packet: Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus (`PHY-SOLID-ELASTICITY-HOOKE`)

### 45.1 Layer 1: Physical Core & Non-Negotiable Preconditions
- **Canonical Subtopic ID**: `PHY-SOLID-ELASTICITY-HOOKE`
- **Learner Title**: Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus
- **Chapter / Domain**: Mechanical Properties of Solids &bull; Grade 11
- **Non-Negotiable Preconditions**:
  1. **PRECOND-1**:  *Boundary constraint*: Physical model breaks down.
  2. **Coordinate Reference Frame & Boundary Invariant**: Physical state and vectors must be evaluated with an explicit inertial reference frame and sign convention before algebraic execution.

#### Mandatory Physical Invariants
- **Equation `EQ-PHYS-YOUNGS-MODULUS`**: $$ — 


### 45.2 Layer 2: Cognitive Transformations & Learning Atom DAG

#### A. Learning Atoms
- `ATOM-SOLHOOK-01` (`CONCEPT`): Stress = F/A, Strain = Delta L / L; Hooke's Law states Stress = Y * Strain within proportional limit; elastic potential energy per unit volume is (1/2) * stress * strain.
- `ATOM-SOLHOOK-02` (`RELATION`): Governing relation.
- `ATOM-SOLHOOK-03` (`INVARIANT`): System invariant.
- `ATOM-SOLHOOK-04` (`PROCEDURE`): Systematic problem-solving workflow: (1) Identify system boundary and declare coordinate axes, (2) Apply governing equations, (3) Verify dimensional consistency and limits.
- `ATOM-SOLHOOK-05` (`STRATEGY`): Diagnostic strategy for discriminating relevant parameters and checking asymptotic edge cases.

#### B. Symbol Bridges (Colloquial to Formal)
| Informal / Colloquial Phrase | Governed Symbolic Representation | Pedagogical Meaning |
|---|---|---|
| *"Everyday intuitive interpretation"* | Formal physical symbol | Strict operational definition under boundary constraints |
| *"Standard textbook heuristic"* | $\vec{F}, \vec{v}, \text{or constitutive parameter}$ | Vector quantity requiring magnitude and directional orientation |
| *"Formula result"* | Governing equation invariant | Conditioned identity holding only when preconditions are satisfied |

#### C. Misconception Contrasts
1. **Misconception: MISC-PHYS-MODULUS-WIRE-SIZE**:
   - *Flawed Action*: Ignoring boundary constraints or applying naive scalar intuition.
   - *Correct Diagnostic Cue*: Apply rigorous vector decomposition and conservation boundaries.
2. **Misconception: Intuitive Heuristic Failure in Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus**:
   - *Flawed Action*: Applying scalar formulas without verifying coordinate frame orientation.
   - *Correct Diagnostic Cue*: Establish standard Cartesian axes and project vector components independently.

---

### 45.3 Layer 3: Reconstructable TTU Library

#### TTU-SOLHOOK-01: Foundational Computational Scaffold (Core1A $\to$ Core1B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Standard problem scaffold for Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus.
Given system parameters: mass m = 2.0 kg, primary state parameter = 10.0 SI units.
Evaluate the primary governing physical response.

Step 1: State the governing equation:
        Primary relation: [ ___ ]
Step 2: Substitute system parameters:
        Value = [ ___ ] · [ ___ ] = [ ___ ] SI units
Step 3: Check directional sign convention:
        Vector component along declared axis is [ positive / negative ].

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Primary relation correctly stated.
Step 2: Evaluated exact numerical response: 20.0 SI units.
Step 3: Positive orientation along the primary positive axis.
```

#### TTU-SOLHOOK-02: Multi-Step Analytical Transfer Challenge (Core2A $\to$ Core2B)
```text
[INCOMPLETE STATE - LEARNER FACING]
Advanced competitive scenario for Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus.
A compound system experiences parametric variation under constrained boundary conditions.

Step 1: Set up system isolation and boundary balance:
        Sum of forces / balance relation: [ ___ ] = 0
Step 2: Express dependent variables in terms of independent parameters:
        Dependent parameter = [ ___ ]
Step 3: Solve for the critical threshold:
        Threshold value = [ ___ ]

[COMPLETION KEY - VERIFICATION ONLY]
Step 1: Balance relation correctly formulated with active constraints.
Step 2: Correct algebraic isolation of dependent parameter.
Step 3: Critical threshold matches exact analytical limit.
```

---

### 45.4 Layer 4: Problem Families & Transfer Discrimination
- `FAMILY-SOLHOOK-01` (`CBSE_BOARD`): Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus Standard Core — Standard textbook problem setup.
- `FAMILY-SOLHOOK-02` (`JEE_MAIN`): Elasticity: Stress-Strain Curve, Hooke's Law & Young's Modulus Multi-Step Synthesis — Competitive transfer challenge.

---
## 46. Intake Validation Checklist for Future Subtopics

To maintain unbroken architectural consistency, any prospective subtopic packet submitted for admission to the Subtopic Intelligence Library must pass the following 6-point verification gate before merging:

1. **Precondition Audit**: Layer 1 must declare explicit, non-empty coordinate reference frames, physical boundary conditions, and domain validity constraints.
2. **Atomic DAG Completeness**: Layer 2 must declare $\ge 4$ typed learning atoms (`CONCEPT`, `RELATION`, `INVARIANT`, `PROCEDURE`, `STRATEGY`).
3. **Misconception Contrast Pairs**: Layer 2 must document $\ge 2$ misconception pairs featuring explicit `Flawed Action` and `Correct Diagnostic Cue`.
4. **Reconstructable TTU Pairs**: Layer 3 must supply $\ge 2$ TTUs with explicit `[INCOMPLETE STATE` learner scaffolds and matching `[COMPLETION KEY` verification keys.
5. **Exam Family Mapping**: Layer 4 must map into $\ge 2$ recognized examination families (`CBSE_BOARD`, `JEE_MAIN`, `JEE_ADVANCED`, `NSEP_OLYMPIAD`).
6. **Zero Topic Hardcoding**: Runtime engine code must evaluate generic schema structures and contain zero hardcoded topic strings.
