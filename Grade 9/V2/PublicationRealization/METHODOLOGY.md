# Publication Realization Methodology

## 1. Freeze upstream semantics

Input semantic payload and LearningDesign refs are immutable for this layer. `PublicationStructure` references content IDs and realization primitives; it does not duplicate or rewrite educational meaning.

## 2. Account for every material item

For each `MATERIAL` item:

```text
semantic item
→ exactly one structure placement intent
→ one or more renderer placement fragments with preserved content_ref
→ exact candidate artifact
```

A material item may be explicitly omitted only by an upstream-approved disposition. V2-06 synthetic proof permits no material omissions.

## 3. Teaching primitives are rendering mechanisms

Shared primitives:

- `TEXT_BLOCK`
- `ANNOTATED_REPRESENTATION`
- `PREDICT_BOX`
- `RECONSTRUCTION_LADDER`
- `WORKED_REASONING_STACK`
- `MINIMAL_CONTRAST_PANEL`
- `GUIDED_WORKSPACE`
- `SELF_CHECK_STRIP`
- `TRANSFER_CHALLENGE`

A primitive cannot satisfy an obligation merely by existing. Its content refs must bind to frozen semantic/LearningDesign objects.

## 4. Physical evidence comes from rendering

The renderer emits placement evidence at the same moment it emits the corresponding PDF drawing/text operation. Planned page numbers are not accepted as physical evidence.

## 5. Seal after physical checks

Order:

```text
structure
→ PDF bytes + placement events
→ PDF SHA256
→ PhysicalPageMap
→ independent custody audit
→ PublicationAudit
→ PublicationManifest
→ deterministic package digest
```

The package digest hashes artifact descriptors and never includes itself or the manifest bytes.

## 6. Engineering quality is not educational quality

Producer output records:

```text
publication_engineering = PASS | FAIL
subject_correctness = PENDING | PASS | FAIL
pedagogy_usability = PENDING | PASS | FAIL
visual_usability = PENDING | PASS | FAIL
benchmark_comparative_validation = NOT_RUN | PASS | FAIL
```

V2-06 producer may set only the engineering state. Downstream quality authorities must supply separate evidence.
