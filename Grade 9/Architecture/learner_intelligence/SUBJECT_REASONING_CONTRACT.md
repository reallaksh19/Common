# Subject Reasoning Contract

**Status:** DRAFT / PHASE 2
**Depends on:** Phase 1 Learner Intelligence shared evidence/state contracts

## 1. Decision

Use one shared learner evidence/inference/state engine, but require subject-specific reasoning contracts.

```text
                         SHARED LEARNER INTELLIGENCE
                  evidence -> observation -> diagnosis -> state
                                      ^
                                      |
             +------------------------+------------------------+
             |                        |                        |
      MathReasoningContract    PhysicsReasoningContract ChemistryReasoningContract
```

A subject reasoning contract describes the expected cognitive/semantic checkpoints of a problem. It is canonical problem metadata, not learner state.

## 2. Shared envelope

Every reasoning contract carries:

```text
reasoning_contract_id
subject
question_family_ref
concept_refs
prerequisite_capability_refs
stages/checkpoints
required capability refs
known error-signature refs
validation checks
```

A learner attempt is compared with checkpoints to produce `ReasoningObservation` records from Phase 1.

## 3. Mathematics

Mathematics primarily reasons through mathematical objects and transformations while preserving invariants.

```text
UNDERSTAND OBJECT
-> SELECT REPRESENTATION
-> RECOGNIZE STRUCTURE
-> SELECT OPERATION/THEOREM
-> TRANSFORM
-> PRESERVE INVARIANT/EQUIVALENCE
-> CHECK CONDITIONS/DOMAIN
-> VERIFY RESULT
```

Math checkpoints may specify:

```text
input object/expression
operation or theorem
output object/expression
invariant to preserve
conditions
validation rule
```

Representative invariants include equality/equivalence, order, ratio, root set, area, congruence/similarity conditions and logical implication.

## 4. Physics

Physics requires first-class physical state and state transition semantics.

```text
PHYSICAL SITUATION
-> DEFINE SYSTEM
-> CHOOSE FRAME/AXES/SIGN
-> IDENTIFY STATE
-> SELECT MODEL/LAW
-> REPRESENT
-> PREDICT
-> EXECUTE MATHEMATICS
-> DERIVE NEW STATE
-> PHYSICAL CHECK/INTERPRETATION
```

Physics checkpoints may specify:

```text
system/entities/interactions
frame/sign convention
initial physical state
governing model/law
assumptions
representation
state transition
terminal physical state
units/dimensions
boundary/continuity/plausibility checks
```

A phase boundary does not reset physical state unless an explicit event/model says it does.

## 5. Chemistry

Chemistry requires explicit representation-level and entity/conservation semantics.

```text
MACROSCOPIC OBSERVATION
          <->
PARTICULATE / ENTITY MODEL
          <->
SYMBOLIC REPRESENTATION
          <->
QUANTITATIVE RELATION
```

Chemistry checkpoints may specify:

```text
representation level
entities/substances
process/transformation
governing relationship
fixed conditions
conserved quantities
source representation
target representation
experimental evidence/claim where relevant
```

A quantitative algebra failure MUST NOT automatically become a chemistry-concept failure when the chemical relationship and conditions were correctly selected.

## 6. Capability definitions

Capabilities are stable reusable definitions with subject/cross-subject identity. LearningDesign capabilities in Core (2) should eventually reference these definitions rather than inventing longitudinal learner identity.

A capability definition includes:

```text
capability_id
subject/shared domain
reasoning stage/class
description
prerequisite refs
success criteria
failure-signature refs
diagnostic-probe refs
```

## 7. Error signatures

An error signature is a reusable observable pattern, not a learner label.

Examples:

```text
MATH: x+y=24 -> x=24
PHYSICS: reuse original u at a continuous second phase
CHEMISTRY: delete a constant from an equality instead of deriving proportionality
```

An error signature MAY nominate several competing diagnostic hypotheses.

## 8. Diagnostic probes

A diagnostic probe is designed to discriminate competing explanations with minimal confounding.

A probe MUST state:

```text
target capability
candidate hypotheses distinguished
prompt intent
expected discriminating evidence
assistance policy
```

## 9. Cross-subject dependency

Subject capabilities may depend on shared capabilities. Example:

```text
MATH-SIMULTANEOUS-EQUATIONS
  -> SHARED-SIGNED-NUMBER-EXECUTION

PHY-KIN-MULTIPHASE-STATE
  -> PHY-KIN-VELOCITY-STATE
  -> SHARED-SIGNED-NUMBER-EXECUTION
  -> SHARED-SYMBOLIC-PRESERVE-MEANING

CHEM-GAS-DENSITY-PRESSURE
  -> CHEM-GAS-CONDITIONS
  -> SHARED-PROPORTIONAL-REASONING
```

This allows cross-topic root-cause analysis without making subject reasoning generic.

## 10. Phase 2 acceptance falsifiers

```text
MATH_CORRECT_MODEL_PLUS_BAD_ALGEBRA != MATH_CONCEPT_FAILURE
PHYSICS_FORMULA_KNOWN_PLUS_STATE_RESET = STATE_TRANSITION_OBSERVATION
CHEM_RELATION_CORRECT_PLUS_BAD_PROPORTIONAL_ALGEBRA != CHEM_CONCEPT_FAILURE
SUBJECT_REASONING_SEMANTICS_ARE_NOT_COLLAPSED = PASS
SHARED_CAPABILITY_DEPENDENCIES_ALLOWED = PASS
```
