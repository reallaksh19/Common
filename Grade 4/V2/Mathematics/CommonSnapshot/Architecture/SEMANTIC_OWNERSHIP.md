# Primary Math V2 Semantic Ownership

**Tracking:** #328

## 1. Upstream Common ownership

Primary Math V2 consumes, rather than redefines, the following Common semantics:

```text
#163
  Primary ownership boundaries
  scope/source provenance
  curriculum overlays
  LearningObject / learning-state semantics

#171
  MathematicalWorkEvidence
  WorkStep
  QuantityStructure
  strategy support / teacher annotation provenance

#172
  evidence-before-diagnosis runtime consumption
  independent retry after teaching/repair

#185
  ContrastSet
  CompetingHypothesis
  DiagnosticProbe

#182
  visual-first learner publishing
  H1/H2/H3 projection
  student/adult separation
  page-image child-usability gate

#164
  support vs access adjustment
  representation evidence roles
  route change
  acquisition / independent / retention / transfer separation
```

## 2. Primary V2 owns

Primary V2 may canonically define:

```text
PrimaryMathInput
PrimaryMathSkillModel
ConceptNode specialization for Math
ConceptMode
PrimaryMathCore1StudyPlan
PrimaryMathCore2CompanionPlan
RepresentationPlan
PrimitiveSpec contract
PhysicalPageMap contract
ArchitectureManifest
neutral candidate-export seam to #325
```

These objects compose existing Primary semantics; they do not replace them.

## 3. #324 owns implementation, not meaning

#324 may implement:

```text
registries
validators
visual primitives
notebook renderer
page composer
PDF backend
artifact generation
```

It may not locally redefine:

```text
scope provenance
ConceptMode meaning
MathematicalWorkEvidence semantics
DiagnosticProbe meaning
H1/H2/H3 meaning
independent evidence
human review status
```

If implementation discovers a semantic gap, update the architecture authority first.

## 4. #325 owns independent acceptance

#325 may define:

```text
frozen benchmark cases
adversarial mutations
independent mathematical oracle
candidate-export validation
human review rubric
```

It must not become an alternate canonical concept ontology or an implementation dependency inside #324.

## 5. Study-Hub / Kani boundary

Study-Hub may serialize/orchestrate V2 products and references. Kani may render experiences and record observations it genuinely sees.

Neither becomes the canonical owner of Primary Math concept truth, diagnostic meaning or mastery state.

## 6. Renderer boundary

The renderer owns presentation operations:

```text
layout
placement
pagination
typography
vector drawing
```

It never owns:

```text
mathematical truth
curriculum activation
diagnosis
solution derivation
invented learner work
```

## 7. Human-review boundary

Machine systems may produce evidence for review but cannot self-authorize:

```text
SUBJECT_CORRECTNESS
PEDAGOGICAL_DESIGN
ASSESSMENT_DESIGN
VISUAL_USABILITY
CHILD_USABILITY
MATURE_DESIGN_QUALITY
```

Those states must remain explicit and independently recorded.
