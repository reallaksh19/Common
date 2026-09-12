# Primary Math V2 Concept Model

**Authority:** #328, consuming Common #163/#171/#172/#185/#182/#164.

## 1. Concept identity

A canonical concept is independent of grade label, page number, worksheet section and renderer.

Use stable IDs for reusable mathematical meaning. Grade/curriculum expectations attach as overlays.

## 2. Core entities

```text
ConceptNode
  id
  title
  description
  learning_object_refs[]
  capability_refs[]
  prerequisite_refs[]
  representation_refs[]
  representation_translation_refs[]
  problem_family_refs[]
  invariant_refs[]
  reasoning_route_refs[]
  error_signature_refs[]
  transfer_dimension_refs[]
```

Related entities:

```text
Capability
MicroSkill
PrerequisiteEdge
RepresentationRole
RepresentationTranslation
ProblemFamily
QuantityStructure
Invariant
ReasoningRoute
ErrorSignature
DiagnosticFeature
TransferDimension
```

## 3. Grade and curriculum overlays

Per #163:

```text
CANONICAL CONCEPT
   ├─ generic Grade 4 expectation overlay
   ├─ generic Grade 5 expectation overlay
   ├─ NCERT / NCF overlay
   ├─ Common Core overlay
   ├─ school/source overlay
   └─ stretch / assessment-demand overlay
```

Do not clone the canonical concept because a grade or curriculum labels it differently.

## 4. ConceptMode

`ConceptMode` describes the current learning-design purpose, not the concept itself.

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

A concept may occur in multiple modes in one learner journey.

### Constraints

- `REPAIR` requires bounded evidence or an explicit source-driven repair objective.
- `PROBE` requires hypotheses and an information-gain purpose per #185.
- `PRACTISE` is not evidence that reteaching is needed.
- `VERIFY` should be preferred over full reteach when prior evidence is strong enough.
- `REFERENCE` is not independent evidence.

## 5. Representation semantics

Representation roles include:

```text
CONCRETE
PICTORIAL
STRUCTURAL
SYMBOLIC
STRATEGIC
PROCEDURAL
ABSTRACT_REASONING
```

Evidence roles from #164 remain separate:

```text
PROVIDED
CHILD_SELECTED
CHILD_PRODUCED
```

A representation can therefore have both a mathematical role and an evidence role.

## 6. Quantity structure

For word problems, grouped units, money, rates and conversion, use #171's quantity-structure discipline:

```text
QUANTITY
→ UNIT
→ ROLE
→ RELATIONSHIP
→ UNKNOWN
→ OPERATION(S)
```

Keywords are clues, never operation rules.

## 7. Error signatures

Error signatures are bounded evidence patterns, not learner traits.

Examples:

```text
DIV_QUOTIENT_ZERO_PLACE_VALUE
UNIT_CHAIN_STEP_DROPPED
MULT_PARTIAL_PRODUCT_PLACE_MISALIGNMENT
FRACTION_EQUAL_PARTITION_CONFUSION
```

They may activate `PROBE` or `REPAIR`, but require provenance and confidence.

## 8. Transfer dimensions

Transfer must be explicitly parameterized rather than represented by number substitution alone.

Possible dimensions:

```text
CONTEXT_CHANGE
REPRESENTATION_CHANGE
UNKNOWN_POSITION_CHANGE
SURFACE_LANGUAGE_CHANGE
MULTI_STEP_COMPOSITION
METHOD_CHOICE
DISTRACTOR_STRUCTURE
UNIT_CHANGE
SCALE_CHANGE
```

## 9. Anti-drift invariants

Fail architecture review if:

```text
GRADE5_CLONED_AS_SEPARATE_CANONICAL_ONTOLOGY
QUESTION_INSTANCE_USED_AS_CONCEPT_ID
PAGE_NUMBER_USED_AS_CONCEPT_ID
ERROR_SIGNATURE_PROMOTED_TO_DURABLE_TRAIT
KEYWORD_OPERATION_RULE_OVERRIDES_QUANTITY_STRUCTURE
REPRESENTATION_ROLE_COLLAPSED_WITH_EVIDENCE_ROLE
```
