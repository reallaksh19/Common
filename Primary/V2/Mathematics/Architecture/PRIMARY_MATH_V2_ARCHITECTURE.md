# Primary Mathematics V2 Architecture

**Status:** architecture candidate  
**Tracking:** #328  
**Implementation child:** #324  
**Independent acceptance:** #325 / PR #326

## Normative Common PR stack

Primary Math V2 consumes the merged Primary stack; it does not redefine it.

| Authority | Applies to |
| --- | --- |
| Common #163 | canonical Primary Grades 4–5 semantics, scope provenance, curriculum overlays, shared Grade 4/5 ontology, repository ownership |
| Common #171 | MathematicalWorkEvidence, WorkStep, QuantityStructure, child/teacher provenance, ambiguity preservation |
| Common #172 | evidence before diagnosis; bounded teaching decision; independent retry |
| Common #185 | ContrastSet, CompetingHypothesis, DiagnosticProbe, smallest discriminating probe |
| Common #182 | visual-first learner publishing, H1/H2/H3 support, fresh independent retry, page-image child usability |
| Common #164 | support vs access adjustment, representation roles, route change, acquisition/independence/retention/transfer |

Grade 9 PRs are non-normative. They may inform engineering regressions only.

## 1. Purpose

Primary Math V2 turns grounded Grade 4–5 scope and optional learner evidence into explicit concept/skill models, learning-design plans, validated representations, linked Core 1/Core 2 products, and independently judged candidate artifacts.

The architecture is:

```text
question_set REQUIRED
student_workout OPTIONAL
 topic_hints OPTIONAL
        ↓
PrimaryMathInput
        ↓
SCOPE RESOLUTION
        ↓
PrimaryMathSkillModel
        ↓
EVIDENCE / DIAGNOSTIC REASONING when available
        ↓
PrimaryMathCore1StudyPlan
PrimaryMathCore2CompanionPlan
RepresentationPlan
        ↓
Visual Semantic Validation
        ↓
Visual / Notebook Publisher
        ↓
PhysicalPageMap + exact artifacts
        ↓
Neutral Candidate Export
        ↓
Independent Benchmark (#325)
        ↓
Human review
```

Raw questions must never be rendered directly into the learner product.

## 2. Authority separation

Freeze six authorities:

```text
SCOPE AUTHORITY
CONCEPT AUTHORITY
EVIDENCE / DIAGNOSTIC AUTHORITY
LEARNING-DESIGN AUTHORITY
REPRESENTATION / PUBLICATION AUTHORITY
BENCHMARK / RELEASE AUTHORITY
```

Invariant:

```text
MATHEMATICAL TRUTH
!= REPRESENTATION CHOICE
!= PAGE LAYOUT
!= LEARNER DIAGNOSIS
!= RELEASE APPROVAL
```

A downstream layer may consume upstream meaning but may not silently rewrite it.

## 3. Scope provenance

Every activated capability declares one of:

```text
CURRICULUM_CONFIRMED
QUESTION_SET_OBSERVED
SCHOOL_CLASSWORK_OBSERVED
COMMON_G4_5_CAPABILITY
CURRICULUM_OVERLAY
EXTENSION
STRETCH
MAPPING_PENDING
SOURCE_NOT_PROVIDED
```

`CURRICULUM_CONFIRMED` requires an authority reference where one is available.

Question-derived or school-work-derived scope may not become a universal grade claim.

## 4. Canonical concept layer

A concept is not a page, question or worksheet section. The canonical layer contains reusable objects such as:

```text
LearningObject
ConceptNode
Capability
MicroSkill
PrerequisiteEdge
RepresentationRole
RepresentationTranslation
ProblemFamily
ReasoningRoute
QuantityStructure
Invariant
ErrorSignature
DiagnosticFeature
TransferDimension
```

Grade 4 and Grade 5 reuse one canonical object where the mathematics is the same. Curriculum/grade expectations are overlays.

## 5. ConceptMode

Every learner-facing use of a concept declares why it appears now:

```text
INTRODUCE
CONNECT
REPAIR
PROBE
PRACTISE
RETRIEVE
TRANSFER
VERIFY
REFERENCE
```

`PROBE` is governed by #185 and is not ordinary practice. `REPAIR` requires bounded evidence; it is not inferred from one wrong final answer. `VERIFY` prevents unnecessary reteaching of already-demonstrated knowledge.

## 6. Work evidence and diagnosis

When `student_workout` is present, reuse #171/#172/#185 semantics.

Preserve observable work before diagnosis:

```text
operation choice
ordered work steps
successful substeps
incorrect substeps
quantity/unit roles
representations
child-created strategy supports
self-corrections
teacher annotations with separate provenance
transcription certainty
```

Required distinctions:

```text
child work != teacher correction
child-produced != child-initiated != independent
ambiguous handwriting != inferred answer
successful substep != correct final answer
error signature != durable learner trait
```

Diagnostic reasoning follows:

```text
observable evidence
→ structural features
→ ContrastSet
→ 2–3 bounded CompetingHypotheses
→ smallest DiagnosticProbe
→ observed result
→ confidence update
→ teaching decision
→ fresh independent retry
```

## 7. Learning-design products

Before publication, produce:

```text
PrimaryMathCore1StudyPlan
PrimaryMathCore2CompanionPlan
RepresentationPlan
```

Each planned module binds:

```text
concept_ref
concept_mode
learning objective
prerequisite refs
representation roles / sequence
worked-example obligations
learner action
support / fade plan
independent-check obligation
practice / retrieval / transfer refs
Core1/Core2 semantic links
source / evidence provenance
```

## 8. Core 1

Canonical learner product:

```text
PrimaryMathCore1StudyGuide
```

Governed by #182. Page intents include:

```text
DISCOVER
NOTICE
CONNECT
WORKED
TRY_TOGETHER
TRY
COMPARE
CHECK
RETRIEVE
```

Typical choreography:

```text
SEE / EXPERIENCE
→ NOTICE
→ MAKE / DRAW / MOVE
→ CONNECT REPRESENTATIONS
→ WATCH ONE WORKED EXAMPLE
→ TRY WITH LIMITED SUPPORT
→ FRESH INDEPENDENT TRY
→ CHECK / EXPLAIN
```

Pages are visual-first, child-readable and action-oriented. Content that does not fit must split across pages rather than shrink readability or workspace.

## 9. Core 2

Canonical companion product:

```text
PrimaryMathCore2Companion
```

It contains:

```text
Appendix A — Practice Batches
Appendix B — Hint Ladder + Solutions
Appendix C — Visual Quick Reference
```

Practice batch semantics:

```text
RECONNECT
BUILD
CHOOSE
MIX
TRANSFER
RETRIEVE
```

Primary quick-support projection:

```text
H0 TRY
H1 NOTICE
H2 REMEMBER
H3 REPRESENT
→ fresh H0 independent retry
```

Supported success is not independent evidence.

## 10. Representation architecture

Representations carry mathematical meaning. Support progression such as:

```text
CONCRETE / OBJECT
→ PICTORIAL
→ STRUCTURAL
→ SYMBOLIC
→ STRATEGIC
→ PROCEDURAL
→ ABSTRACT / REASONING
```

Not every concept uses every level. Representation translation is itself a learning target where appropriate.

## 11. Visual publisher

The publisher is downstream of semantic planning:

```text
RepresentationPlan
→ PrimitiveSpec
→ VisualSemanticValidator
→ VectorRenderBackend
→ PageComposer
→ PhysicalPageMap
→ exact PDF + page-image review bundle
```

The publisher may decide placement, size, hierarchy, wrapping and pagination. It may not invent math values, equations, diagram relationships, scope, diagnosis, solution steps or learner work.

```text
renderer_invention_allowed = false
```

The render seam is backend-neutral:

```python
validate_primitive(kind, semantic_source, params) -> ValidationResult
primitive_height(kind, params, width) -> height
render_primitive(kind, params, surface, bbox) -> PlacementEvidence
```

## 12. Visual validation

Every data-bearing structural primitive validates before draw. Validator families must cover at least cardinality, arrays, equal groups, bars, number-line scale, place value, partial products, division identity/work steps, remainders, fraction partition/value, decimals, units, measurement scale, clocks, perimeter, area, volume, angle geometry and chart data/scale.

For written division, internal/trailing positional zeros required after quotient construction begins must be preserved; leading quotient zeros must not be invented.

## 13. Notebook publisher

Notebook rendering is semantic, not prose set in a handwriting font.

Provenance modes:

```text
ORIGINAL_SOURCE_IMAGE
FAITHFUL_TRANSCRIPTION
STRUCTURED_REPLAY
AUTHORED_NOTEBOOK_EXAMPLE
```

Support place-value work, regrouping, partial products, vertical multiplication, partial quotients, short/long division, quotient-zero place, fraction work, aligned decimals, units and child/self/teacher annotations.

Natural cosmetic variation must never disturb mathematical alignment.

## 14. Stable semantic links

Stable IDs survive pagination and backend changes:

```text
concept_ref
capability_ref
representation_ref
problem_family_ref
core1_module_ref
hint_ref
practice_batch_ref
```

Physical page number is never canonical identity. Core2 links to Core1 by semantic reference and resolves the final page only after pagination.

## 15. Runtime behaviour

Reuse #164/#172:

```text
conceptual support != access/load adjustment
provided representation != child-selected != child-produced
supported success != independent success
same-session success != delayed retention
acquisition != independent use != delayed retention != transfer
```

After two substantially same-route failures, change a meaningful teaching route instead of repeating the same explanation at greater length.

## 16. Benchmark / release boundary

#324 owns production. #325 owns independent acceptance.

```text
#324 producer
→ neutral candidate export
→ #325 frozen oracle / negative corpus
→ human subject/pedagogy/assessment/visual/child-usability review
```

The producer may not rewrite benchmark expected values to make itself pass. The benchmark may not import producer rendering internals.

Machine-green publication engineering does not establish mature educational quality.

## 17. Definition of architectural conformance

A conforming implementation:

1. preserves the Common PR stack as authority;
2. resolves scope provenance explicitly;
3. creates `PrimaryMathSkillModel` before publication;
4. uses one canonical Grade 4/5 ontology plus overlays;
5. records `ConceptMode` separately from concept identity;
6. preserves optional learner work without invented steps;
7. uses bounded diagnostic reasoning where evidence supports it;
8. produces explicit Core1/Core2/Representation plans;
9. validates mathematical visuals before draw;
10. keeps rendering/backend/layout downstream of semantic truth;
11. preserves stable semantic links across pagination;
12. exports exact candidate evidence for independent #325 judgment;
13. separates machine gates from human review.
