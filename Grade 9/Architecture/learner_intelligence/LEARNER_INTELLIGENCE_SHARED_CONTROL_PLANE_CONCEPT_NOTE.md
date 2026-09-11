# Concept Note — Learner Intelligence as a Shared Control Plane

**Status:** Draft for architecture review  
**Scope:** Grade 9–11 learning-production architecture  
**Primary decision:** Learner Intelligence is a shared control plane for both research/study synthesis and learning publication; it is not merely a downstream publisher input  
**Related work:** PR #160, PR #161, PR #166–#170  
**Review intent:** Revisit the two-core architecture before further schema migration or production integration

---

## 1. Executive decision

The current architecture is too linear.

The working model established by PR #160 and PR #161 is approximately:

```text
Canonical Registry
  → Project ScopeGraph
  → Core (1) Research
  → ResearchBundle
  + LearnerProfile / Bxx
  → Core (2) Publisher
  → learner product
```

That model correctly separates canonical subject truth from learner adaptation, but it makes a deeper assumption that no longer holds after examining real learner evidence across Mathematics, Physics and Chemistry:

> learner state is treated primarily as a downstream adaptation input after research has already been completed.

That is insufficient.

Learner Intelligence must influence **two different downstream decisions**:

1. **Research / Study Synthesis:** what knowledge must be expanded, reused, bridged, contrasted, represented or newly researched for this learner and goal;
2. **Publication / Learning Design:** how that selected knowledge should be scaffolded through explanation, worked reasoning, hint ladders, fading, practice, retrieval and transfer.

The revised architecture is therefore:

```text
                    CANONICAL SUBJECT AUTHORITY
                              │
                              ▼
                       CANONICAL RESEARCH
                              │
                    CanonicalResearchBundle
                              │
                              │
       ┌──────────────────────┴──────────────────────┐
       │                                             │
       │          LEARNER INTELLIGENCE PLANE         │
       │                                             │
       │ Evidence → Observation → Diagnosis          │
       │        → Capability State → RCA             │
       │                                             │
       └─────────────┬─────────────────┬─────────────┘
                     │                 │
          ResearchLearnerView   PublicationLearnerView
                     │                 │
                     ▼                 │
              STUDY SYNTHESIS          │
                     │                 │
              LearnerStudyModel        │
                     │                 │
                     └────────┬────────┘
                              ▼
                       LEARNING DESIGN
                              │
                 hints / learning ladder
                 fading / practice / transfer
                              │
                              ▼
                          PUBLICATION
                              │
                              ▼
                         learner work
                              │
                              ▼
                         new evidence
                              │
                              └──────────────→ Learner Intelligence
```

This note proposes that architecture for review before modifying the frozen contracts.

---

## 2. Why the current architecture is insufficient

### 2.1 The current separation is necessary but incomplete

PR #160 made an important and correct decision:

```text
learner state must not change canonical mathematical/scientific truth
learner state must not become part of ResearchBundle identity merely because the learner changes
```

That invariant should remain.

However, the stronger statement implied by the current flow — that research can be completed independently and learner adaptation can happen primarily in Core (2) — is too broad.

There are at least three different activities currently being conflated under the word "research":

```text
A. Canonical truth/evidence research
B. learner-conditioned research prioritization / gap closure
C. learner-conditioned study synthesis
```

Only A must be learner-independent.

B and C require Learner Intelligence.

### 2.2 Generic research can be pedagogically wrong even when factually perfect

A learner may already understand one part of a topic while failing on a hidden prerequisite or cross-subject dependency.

For example, a learner can demonstrate:

```text
coordinate-geometry modelling         demonstrated
use of distance relationships          demonstrated
binomial expansion                     unstable
verification                           weak
```

A generic low chapter baseline might cause the system to research and explain coordinate geometry from the beginning.

That is inefficient and misaligned.

The correct study research problem is:

```text
What canonical knowledge must be selected, expanded or newly bridged so that this learner can progress from demonstrated geometry modelling through the algebraic bottleneck to independent verification?
```

That question cannot be answered from the target syllabus alone.

It needs Learner Intelligence.

### 2.3 Core (2) cannot repair an upstream semantic miss through layout and hints

Core (2) can adapt sequencing and support, but it should not be responsible for discovering that the learner's real bottleneck is an upstream prerequisite that the ResearchBundle never represented sufficiently.

If research supplies only:

```text
concept
formula
worked example
practice
```

while the learner actually needs:

```text
missing prerequisite bridge
representation contrast
wrong-model discriminator
state-continuity model
cross-subject symbolic repair
```

then stronger hinting cannot fully compensate.

A publisher can scaffold the content it receives. It should not be required to invent missing subject semantics.

---

## 3. Revised authority model

The revised architecture separates four authorities.

### 3.1 Canonical Subject Authority

Owns learner-independent subject truth and stable semantics:

```text
concept identity
prerequisites
laws / theorems / definitions
validity conditions
representations
question mechanisms
misconception definitions
error signatures
canonical diagnostic probes
exam-demand evidence
source provenance
```

This authority can evolve only through subject/canonical review.

### 3.2 Learner Intelligence Authority

Owns evidence-backed state about the learner:

```text
attempt evidence
reasoning observations
diagnostic hypotheses
capability states
assistance history
transfer evidence
retention evidence
cross-subject bottleneck candidates
diagnostic uncertainty
```

Learner Intelligence does **not** own subject truth and does not invent canonical misconceptions.

### 3.3 Study Synthesis Authority

Owns the learner-conditioned semantic study representation:

```text
what is already demonstrated
what must be repaired
what can be compressed
what must be reconstructed
what bridge is required
which representation sequence should be used
which misconceptions/contrasts are relevant
what independent evidence will count as completion
```

Its primary artifact is the proposed `LearnerStudyModel`.

### 3.4 Learning Design / Publisher Authority

Owns the instructional delivery mechanism:

```text
learning ladder
hint ladder
support states
worked → guided → independent progression
fading
practice sequence
retrieval
transfer challenge
feedback
workspace
publication structure
physical rendering
publication QA
```

This is the natural home of Core (2).

---

## 4. Learner Intelligence is horizontal, not a third sequential core

This proposal does **not** recommend a simple three-stage line:

```text
Research → Learner Intelligence → Publisher
```

That still places Learner Intelligence too late.

Instead, Learner Intelligence is a persistent horizontal subsystem with at least two consumers:

```text
Learner Intelligence
      │
      ├── ResearchLearnerView
      │
      └── PublicationLearnerView
```

The same evidence-backed state is projected differently according to consumer need.

The Research consumer should not need all private interaction history.

The Publisher should not receive unrestricted raw evidence if a scoped learner-state view is sufficient.

This preserves privacy, reproducibility and authority boundaries.

---

## 5. Proposed canonical runtime flow

### 5.1 Platform foundation

Before any learner-specific run, the platform needs reusable canonical structures:

```text
canonical concept/prerequisite registry
subject reasoning contracts
canonical capability definitions
misconception definitions
error signatures
diagnostic probes
question families / mechanisms
source/evidence authority
```

These are not regenerated per learner.

### 5.2 Existing learner evidence

A learner may arrive with evidence from:

```text
T1, T2, T3 ... Tx assessments
practice attempts
retrieval checks
transfer tasks
teacher observations
digital interactions
```

That produces:

```text
LearnerEvidenceLedger
        ↓
ReasoningObservations
        ↓
DiagnosticCases
        ↓
LearnerStateSnapshot
```

### 5.3 Goal formation and learner-conditioned research planning

For a new learning goal:

```text
LearningGoal
+ canonical target scope
+ ResearchLearnerView
        ↓
Research / reuse / gap plan
```

The plan may decide:

```text
REUSE_VERIFIED_FRESH
REUSE_WITH_REVALIDATION
EXTEND_EXISTING
RESEARCH_MISSING
DIAGNOSTIC_GAP_BEFORE_RESEARCH
```

Learner Intelligence changes **research priority and required depth**, not truth.

### 5.4 Canonical research output

Any newly researched knowledge must remain canonical/reusable:

```text
learner exposes missing bridge
        ↓
Core1 researches bridge
        ↓
bridge is represented as canonical/reusable knowledge
        ↓
ResearchBundle version may change
```

The new knowledge is not labelled "true for learner A".

The learner merely revealed that the existing reusable research package was insufficient for a legitimate learning path.

### 5.5 Learner Study Model generation

Once canonical research is sufficient:

```text
CanonicalResearchBundle
+ ResearchLearnerView
+ LearningGoal
+ StudySynthesisPolicy
        ↓
LearnerStudyModel
```

This artifact is learner-specific.

### 5.6 Learning Design and publication

Then:

```text
LearnerStudyModel
+ PublicationLearnerView
+ PublicationTarget
+ LearningDesignPolicy
        ↓
LearningDesignPlan
        ↓
learner semantic product
        ↓
PublicationStructure
        ↓
physical product
```

### 5.7 Feedback loop

Learner interaction produces new evidence:

```text
published learning experience
        ↓
new attempts / hints / retries / transfer
        ↓
LearnerEvidenceLedger
        ↓
new LearnerStateSnapshot
```

The ResearchBundle does **not** rerun automatically on every state update.

Research reruns only when state exposes a genuine research or representation gap.

---

## 6. ResearchLearnerView

`ResearchLearnerView` should be a scoped projection of Learner Intelligence for research and study synthesis.

It should answer:

> What learner evidence materially changes what knowledge should be reused, researched, bridged, contrasted or emphasized for this goal?

Illustrative shape:

```yaml
research_learner_view:
  view_id: RLV-...
  learner_state_snapshot_ref: LSS-...
  target_scope_ref: ...

  demonstrated_capabilities:
    - capability_ref: PHY-KIN-SELECT-EQUATION
      state: READY
      confidence: HIGH

  repair_priorities:
    - capability_ref: PHY-KIN-PROPAGATE-STATE
      state: REPAIR_REQUIRED
      evidence_strength: STRONG
      prerequisite_reach: HIGH

  developing_capabilities:
    - capability_ref: SHARED-SIGNED-NUMBER-EXECUTION

  unresolved_cases:
    - diagnostic_case_ref: DC-...
      action: DIAGNOSTIC_PROBE_REQUIRED

  relevant_cross_subject_dependencies:
    - upstream_capability_ref: SHARED-SYMBOLIC-PRESERVE-MEANING
      affects:
        - MATH-ALG-...
        - PHY-KIN-...

  research_priority_directives:
    - EXPAND_PREREQUISITE_BRIDGE
    - INCLUDE_CONTRAST
    - INCLUDE_STATE_TRANSITION_REPRESENTATION
```

It should not expose unnecessary learner identity or full raw histories.

---

## 7. PublicationLearnerView

`PublicationLearnerView` serves a different purpose.

It should answer:

> Given the learner's current state and the Study Model, what amount and type of support should be provided now?

It therefore requires state that research does not necessarily need:

```text
hint usage history
guided vs independent success
retry patterns
fading stage
recent retrieval evidence
transfer evidence
delayed retention evidence
support dependency
```

Illustrative shape:

```yaml
publication_learner_view:
  view_id: PLV-...
  learner_state_snapshot_ref: LSS-...

  capability_support_state:
    - capability_ref: PHY-KIN-PROPAGATE-STATE
      state: DEVELOPING
      independent_success: 0
      guided_success: 2
      hint_history:
        H1: success
        H2: success
      next_support_ceiling: H1

  transfer_state:
    - capability_ref: SHARED-PROPORTIONAL-REASONING
      near_transfer: DEMONSTRATED
      far_transfer: NOT_YET_EVIDENCED
```

The Publisher then chooses instructional choreography from this state.

---

## 8. The missing central artifact: LearnerStudyModel

The largest missing semantic object in the current architecture is a learner-conditioned study model between canonical research and publication.

The proposed invariant is:

```text
CanonicalResearchBundle
× ResearchLearnerView
× LearningGoal
→ LearnerStudyModel
```

The Study Model represents **what this learner should study and how the knowledge should be semantically organized**, before page layout or concrete hint wording.

Illustrative structure:

```yaml
learner_study_model:
  study_model_id: LSM-...
  learner_state_snapshot_ref: LSS-...
  research_bundle_ref: RB-...
  research_bundle_digest: ...
  learning_goal_ref: ...
  synthesis_policy_version: ...

  units:
    - unit_id: ...
      target_capabilities: [...]

      demonstrated:
        - capability_ref: ...
          treatment: COMPRESS | VERIFY_ONLY | USE_AS_ENTRY_POINT

      prerequisite_decisions:
        - capability_ref: ...
          decision: READY | REPAIR_BEFORE_UNIT | REPAIR_IN_UNIT | PROBE_FIRST

      conceptual_bridges: [...]
      reconstruction_targets: [...]
      representation_sequence: [...]
      misconception_contrasts: [...]
      worked_reasoning_requirements: [...]
      validity_and_verification_requirements: [...]
      transfer_requirements: [...]
      completion_evidence_required: [...]
```

Notably absent from the Study Model:

```text
font choice
page geometry
physical page placement
final H1/H2/H3 prose
worksheet layout
PDF-specific structure
```

Those belong to publication.

---

## 9. Research adaptation: what Learner Intelligence may change

Learner Intelligence may legitimately affect:

```text
research priority
bridge depth
prerequisite expansion
which known misconception discriminators are required
which representation needs stronger treatment
which alternative method/model needs contrast
which transfer boundary needs examples
which research gaps block the learner path
```

It may **not** change:

```text
canonical theorem/law/definition
validity conditions
source authority
correct equation/reaction semantics
truth of a misconception definition
exam fact
canonical concept identity
```

### 9.1 Research prioritization versus canonical scope

A critical distinction is needed between:

```text
CanonicalTargetScope
```

and:

```text
LearnerStudyScope
```

The canonical scope records what the curriculum/exam/topic requires.

The learner study scope records what should receive active study attention.

A learner being strong in one capability does not remove that capability from the canonical scope; it may change its treatment to:

```text
VERIFY_ONLY
COMPRESS
USE_AS_ENTRY_POINT
```

This prevents the architecture from confusing personalization with curriculum deletion.

---

## 10. Publication adaptation: learning ladder and hint ladder

Core (2) should treat hints as learner-conditioned support, not static question metadata.

The general function is:

```text
HintLadder = f(
  reasoning contract,
  LearnerStudyModel,
  PublicationLearnerView,
  current attempt state
)
```

For a Physics multi-phase kinematics problem, a learner who already knows the equations but fails state propagation should not receive as the first hint:

```text
Use v = u + at.
```

That support solves the wrong problem.

An appropriate ladder might be:

```text
H0: no hint
H1: Which quantity at the end of phase 1 becomes an initial condition for phase 2?
H2: Find the velocity at the phase boundary.
H3: Use that velocity as u for the second interval.
H4: Show the complete state-transition setup.
```

For another learner who cannot select the governing equation, the ladder should be different.

Therefore hint semantics are not simply a property of the question.

They are a property of:

```text
question reasoning contract
+ learner state
+ current support history
```

---

## 11. Subject-specific reasoning remains essential

Learner Intelligence is shared, but subject reasoning semantics must remain discipline-specific.

### 11.1 Mathematics

Math reasoning should emphasize:

```text
object
representation
structure
method/theorem selection
transformation
equivalence/invariant preservation
conditions/domain
verification
```

Learner-conditioned research may decide that a learner needs an algebraic bridge while preserving already-demonstrated geometric modelling.

### 11.2 Physics

Physics reasoning should emphasize:

```text
system
frame
state variables
model/law
representation
qualitative prediction
mathematical execution
state transition
sign/direction interpretation
physical validation
```

Learner-conditioned research may need to foreground state continuity even when formula knowledge is already strong.

### 11.3 Chemistry

Chemistry reasoning should emphasize:

```text
macroscopic observation
particle/entity model
symbolic representation
quantitative relationship
conservation
conditions
experimental evidence
representation translation
```

Learner-conditioned research may retain advanced gas-law treatment while inserting a cross-subject proportionality bridge.

The shared engine should detect cross-subject recurrence without flattening these disciplinary distinctions.

---

## 12. Bxx is a projection, not the control object

The current architecture gives Bxx too much conceptual importance.

Bxx remains useful for:

```text
cold start
compact adaptation summaries
legacy compatibility
coarse publication profile selection
```

But the mature flow should be:

```text
Learner Evidence
      ↓
Capability State
      ↓
Subtopic / scope aggregation
      ↓
Bxx projection
```

not:

```text
test score
      ↓
Bxx
      ↓
research and teaching decisions
```

A learner may have the same Bxx as another learner for completely different causal reasons.

Example:

```text
Learner A: modelling strong, algebra weak
Learner B: modelling weak, algebra strong
```

A shared B45 does not justify the same research or hint ladder.

---

## 13. Determinism and artifact identity

The revised architecture should preserve reproducibility across every authority boundary.

### 13.1 CanonicalResearchBundle identity

Depends only on canonical project research inputs, evidence and scope.

It does **not** change merely because learner state changes.

### 13.2 LearnerStateSnapshot identity

Derived from:

```text
LearnerEvidenceLedger digest
+ canonical registry version
+ diagnostic policy version
```

### 13.3 ResearchLearnerView identity

Derived from:

```text
LearnerStateSnapshot digest
+ target scope
+ research-view projection policy
```

### 13.4 LearnerStudyModel identity

Derived from:

```text
CanonicalResearchBundle digest
+ ResearchLearnerView digest
+ LearningGoal / canonical target scope
+ StudySynthesisPolicy version
```

### 13.5 PublicationLearnerView identity

Derived from:

```text
LearnerStateSnapshot digest
+ publication scope
+ publication-view projection policy
```

### 13.6 LearningDesign identity

Derived from:

```text
LearnerStudyModel digest
+ PublicationLearnerView digest
+ PublicationTarget
+ LearningDesignPolicy version
```

This gives deterministic replay without making learner state part of canonical research identity.

---

## 14. Three separate gap protocols are required

The architecture should no longer use one generic gap concept for all failures.

### 14.1 Diagnostic gap

Learner evidence is insufficient to distinguish competing explanations.

```yaml
status: DIAGNOSTIC_GAP
capability_ref: ...
action: TARGETED_PROBE_REQUIRED
```

### 14.2 Research gap

The canonical research package lacks required knowledge or representation needed for a valid learner path.

```yaml
status: CORE1_RESEARCH_GAP
gap_type: PREREQUISITE | BRIDGE | REPRESENTATION | MISCONCEPTION | PROBE | QUESTION_FAMILY | EXAM_DEMAND
blocking: true
```

### 14.3 Learning-design/publication gap

The Study Model is sufficient, but instructional or rendering primitives cannot realize it.

```yaml
status: CORE2_DESIGN_GAP
gap_type: HINT_LADDER | FADING | PRACTICE | REPRESENTATION_REALIZATION | PAGE_COMPOSITION | FEEDBACK
```

This separation prevents Core2 deficiencies from being mistaken for research deficiencies and vice versa.

---

## 15. Validation against the cross-subject learner fixture

The architecture should be rejected if it cannot reproduce the following distinctions from structured evidence.

### 15.1 Mathematics — coordinate geometry / algebra

Observed pattern:

```text
geometric model                     success
distance relation                   success
binomial expansion                  failure
```

Research adaptation should:

```text
retain coordinate-geometry level
avoid full reteaching of basic coordinate representation
expand/reuse algebra bridge
include transformation verification
```

Publication adaptation should:

```text
use short legal-transformation hints
fade algebra scaffolding
require independent verification
```

### 15.2 Mathematics — word model / compound expression

Observed pattern:

```text
word → equation                     success
compound expression meaning         failure
```

Research adaptation should target expression semantics, not generic word-problem modelling.

Publication hints should ask the learner to preserve the meaning of `x+y`, rather than restating the word problem.

### 15.3 Physics — multi-stage kinematics

Observed pattern:

```text
law selection                       success
phase-1 calculation                 success
state continuity                    failure
```

Research adaptation should foreground:

```text
terminal state
phase boundary
continuity
state transition diagrams
```

Publication should build a hint ladder around state propagation rather than formula recall.

### 15.4 Physics — projectile motion

Observed pattern:

```text
component decomposition             success
symbolic elimination                success
diagram/state interpretation         ambiguous
```

Research should preserve advanced projectile competence.

Learner Intelligence should request a discriminating representation probe rather than downgrading the whole topic.

### 15.5 Chemistry — gas laws / proportionality

Observed pattern:

```text
ideal-gas relation                  success
density relation                    success
equality → proportionality          imprecise
```

Research adaptation should keep Chemistry conceptual level and add/reuse the shared mathematics bridge.

Publication should scaffold the proportional reasoning step, not reteach the gas law.

These cases are the architectural acceptance fixture.

---

## 16. Implications for PR #160

PR #160 should retain its strongest invariants:

```text
canonical truth is learner-independent
ResearchBundle has versioned evidence custody
learner state is not part of ResearchBundle identity
research assets should be reusable
```

But its learner-state relationship needs revision.

The current idea that LearnerProfile/Bxx is principally downstream should be replaced with:

```text
Learner Intelligence is visible to research through a scoped ResearchLearnerView
Learner Intelligence may prioritize/trigger research gaps
canonical research output remains learner-independent
learner-conditioned Study Synthesis follows canonical research
```

The phrase:

```text
Research once per evidence version → reuse many → publish many
```

can remain, but should be expanded conceptually to:

```text
Research canonical knowledge once per evidence version
→ reuse many
→ synthesize study models per learner/goal
→ publish many learner-specific learning experiences
```

---

## 17. Implications for PR #161

PR #161 correctly identifies LearningDesign as a first-class semantic stage and already contains capabilities, prerequisite decisions, misconceptions, support progression and transfer.

However, LearningDesign currently risks carrying two responsibilities:

```text
what this learner should study
and
how it should be taught
```

Those should be separated.

Proposed boundary:

```text
LearnerStudyModel
    owns semantic study selection/reconstruction

LearningDesignPlan
    owns instructional choreography
```

Core2 should consume both:

```text
LearnerStudyModel
+ PublicationLearnerView
+ PublicationTarget
→ LearningDesignPlan
```

This also gives #165 a cleaner diagnostic framework: poor learner product may arise from a weak Study Model, weak LearningDesign, weak rendering primitives, or combinations thereof.

---

## 18. Implications for PR #166–#170

### PR #166

The Evidence → Observation → DiagnosticCase → LearnerState separation remains valid.

No conceptual reversal is needed.

### PR #167

Subject reasoning contracts become even more important because both research adaptation and publication adaptation depend on the same disciplinary reasoning semantics.

### PR #168

The conservative inference policy remains valid and should feed both `ResearchLearnerView` and `PublicationLearnerView`.

### PR #169

The current Core1/Core2 hand-off concept is insufficient because it primarily defines learner state as a Core2 input.

It should be superseded or revised after this concept note is approved.

The corrected interface needs two projections plus a Study Model:

```text
Learner Intelligence
  ├ ResearchLearnerView → Study Synthesis
  └ PublicationLearnerView ───────────────┐
                                          ↓
LearnerStudyModel ───────────────→ LearningDesign
```

### PR #170

The deterministic state engine remains useful.

Its next evolution should produce scoped research and publication projections rather than directly treating one learner-state view as the sole integration object.

---

## 19. Proposed implementation sequence after approval

Do not immediately patch all existing schemas.

Recommended sequence:

```text
A. approve shared-control-plane concept
B. freeze authority boundaries
C. define ResearchLearnerView contract
D. define PublicationLearnerView contract
E. define LearnerStudyModel methodology before schema
F. add StudySynthesisPolicy
G. create end-to-end cross-subject replay
H. revise Core1 integration
I. revise Core2 LearningDesign input
J. only then migrate Bxx/legacy fixtures
```

The methodology for `LearnerStudyModel` should be designed before its JSON schema.

The schema should encode a validated educational model, not substitute for one.

---

## 20. Proposed release-blocking falsifiers

The architecture should fail review or implementation if any of the following is possible:

```text
1. learner weakness changes canonical scientific/mathematical truth
2. one wrong answer becomes a confirmed misconception
3. Bxx alone determines research or hint strategy when richer evidence exists
4. correct upstream reasoning is erased by a later wrong answer
5. Core1 always performs the same research depth regardless of demonstrated learner state
6. Core2 must invent a missing prerequisite bridge because Study Synthesis did not represent it
7. ResearchBundle identity changes only because the learner improved
8. learner strength causes canonical curriculum/exam scope to be deleted rather than compressed/verified
9. static question hints ignore the learner's actual failed reasoning stage
10. Math/Physics/Chemistry are forced into one generic reasoning sequence
11. shared algebra failure automatically becomes a Chemistry or Physics misconception
12. ambiguous evidence causes unsupported psychological diagnosis
13. a learner-state update unnecessarily triggers canonical research rebuild
14. a genuine missing learner bridge cannot trigger a research-gap workflow
15. two different learner profiles with the same Bxx are forced into the same Study Model
```

---

## 21. Review questions requiring explicit decision

Architecture review should explicitly decide:

1. Is Learner Intelligence approved as a horizontal shared control plane for both research/study synthesis and publication?
2. Should `LearnerStudyModel` become a first-class semantic artifact between ResearchBundle and LearningDesign?
3. Should research consume a scoped `ResearchLearnerView` rather than only optional Bxx?
4. Should publication consume a separate `PublicationLearnerView` containing assistance/fading/transfer state?
5. Should canonical target scope and learner study scope be separate objects?
6. Should learner-triggered research gaps produce reusable canonical knowledge rather than learner-specific truth objects?
7. Should `LearningDesignPlan` be narrowed to instructional choreography rather than also deciding core study content?
8. Should PR #169 be superseded after this design is accepted?
9. Should Bxx remain only a projection/compatibility artifact in the mature path?
10. Should the Math/Physics/Chemistry answer-sheet fixture remain a permanent architecture falsifier?

---

## 22. Proposed architecture invariant set

If this note is approved, the following should become top-level invariants:

```text
I1. Canonical truth is learner-independent.

I2. Learner evidence, diagnosis, learner state, study synthesis and teaching decisions are separate authorities.

I3. Learner Intelligence is shared by research/study synthesis and publication.

I4. ResearchLearnerView may change research priority and expose gaps, but cannot change truth.

I5. Newly researched learner-triggered knowledge must be reusable/canonical when valid beyond the learner.

I6. LearnerStudyModel is learner-specific and binds canonical research to learner need.

I7. PublicationLearnerView governs support level, fading, hints, retrieval and transfer decisions.

I8. Bxx is a projection, not the canonical learner model.

I9. Core2 consumes diagnosis; it does not silently invent learner-state conclusions.

I10. A learner-state change does not imply a ResearchBundle rebuild unless it exposes a genuine canonical research gap.

I11. Subject-specific reasoning semantics remain first-class under shared evidence/inference infrastructure.

I12. Every learner-facing intervention must remain traceable both to canonical research and to the learner-state reason for its inclusion/support level.
```

---

## 23. Final proposed model

The resulting production model is:

```text
                           ┌──────────────────────────┐
                           │ CANONICAL SUBJECT AUTHORITY │
                           └─────────────┬────────────┘
                                         │
                                         ▼
                              Canonical Research
                                         │
                                  ResearchBundle
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 │                       │                       │
                 │                Learner Intelligence           │
                 │                       │                       │
                 │          ┌────────────┴────────────┐          │
                 │          ▼                         ▼          │
                 │  ResearchLearnerView      PublicationLearnerView
                 │          │                         │
                 │          ▼                         │
                 │     Study Synthesis                │
                 │          │                         │
                 │    LearnerStudyModel               │
                 │          └─────────────┬───────────┘
                 │                        ▼
                 │                 LearningDesign
                 │                        │
                 │             hints / ladder / fading
                 │                        │
                 │                   Publication
                 │                        │
                 └────────────────────────▼
                                      Learner
                                         │
                                         ▼
                                    New Evidence
                                         │
                                         └──────→ Learner Intelligence
```

The architecture is therefore no longer best described as:

```text
Research → learner adaptation → Publish
```

It is better described as:

```text
Canonical knowledge
+
continuous Learner Intelligence
→ learner-conditioned Study Synthesis
→ learner-conditioned Learning Design
→ evidence-producing learning loop
```

That is the proposed architecture for review.