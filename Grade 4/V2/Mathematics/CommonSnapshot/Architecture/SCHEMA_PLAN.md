# Primary Math V2 Schema Plan

## Contract family

```text
primary-math-input.schema.json
concept-node.schema.json
primary-math-skill-model.schema.json
learning-design-plan.schema.json
representation-plan.schema.json
architecture-manifest.schema.json
```

All contracts use JSON Schema Draft 2020-12 and declare:

```text
schema_version
authority
stable semantic IDs
compatibility assumptions
```

## 1. `PrimaryMathInput`

Required:

```text
question_set
```

Optional:

```text
student_workout
topic_hints
```

The schema must prove optional inputs are genuinely optional.

## 2. `ConceptNode`

Defines canonical reusable concept structure and supports one ontology plus grade/curriculum overlays.

Must include stable concept ID, title, capability/prerequisite refs and optional representation/problem-family/invariant/transfer refs.

## 3. `PrimaryMathSkillModel`

Mandatory semantic bridge between intake and publication.

Contains:

```text
scope resolutions
concept activations
capability refs
prerequisite edges
problem-family refs
representation requirements
quantity structures
reasoning obligations
practice / retrieval / transfer obligations
ambiguity/unresolved state
optional work evidence / diagnostic refs
```

## 4. `LearningDesignPlan`

A generic plan structure used for Core 1 and Core 2 modules.

Every module binds:

```text
module_id
concept_ref
concept_mode
objective
representation refs
learner action
support/fade state
independent-check obligation
semantic cross-links
```

The plan may not canonically depend on physical page number.

## 5. `RepresentationPlan`

Defines semantic visual requirements before layout:

```text
representation_id
concept_ref
role
primitive_kind
semantic_params
validator_refs
fade_modes
provenance
```

No renderer-generated mathematical values are allowed.

## 6. `ArchitectureManifest`

Binds one cold-start run across stages:

```text
input digest
skill-model digest
Core1 plan digest
Core2 plan digest
representation-plan digest
implementation version
candidate-export ref
artifact refs when present
benchmark ref when evaluated
human-review states
```

## 7. Compatibility policy

Additive optional fields may be backward-compatible within a major version. Changes to meaning, required identifiers, provenance semantics, ConceptMode meaning, or authority ownership require a version change and architecture review.

## 8. Required fixtures

Validate at least:

```text
question_set only
question_set + student_workout
question_set + topic_hints
question_set + student_workout + topic_hints
```

The first fixture is the minimum cold-start contract and must pass without fabricated learner evidence.
