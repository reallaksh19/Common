# Mathematics V2 — Publication

This directory now holds **two** lineages. Read this before touching anything in it.

## LIVE: Core product realization (M-L, #319)

```text
MathCore1StudyPlan  (M-H)   ─┐
MathCore2TransferPlan (M-I)  ├─→ realize_math_core_products.py ─→ core1_study_guide.pdf
MathCoverageClosure  (M-J)   │                                 └─→ core2_transfer_book.pdf
Math PCK candidates  (M-G)   │        + publication_structure.json
Math teaching primitives     ─┘       + physical_page_map.json
                                      + publication_audit.json
                                      + publication_manifest.json
```

Entry points:

| File | Role |
| --- | --- |
| `engine/realize_math_core_products.py` | consumes real M-chain JSON, paginates, records placement evidence, binds the exact PDF sha256 |
| `engine/math_primitive_adapter.py` | the stable figure seam: `render_primitive(kind, params, canvas, bbox)` |
| `contracts/math-core-product-*.schema.json` | page map, manifest and realization contracts |
| `tests/test_math_core_product_renderer.py` | falsifier suite |

```bash
python 'Grade 9/V2/Mathematics/Publication/tests/test_math_core_product_renderer.py'
```

### Figures are real vector graphics, driven by real data

Every canonical primitive in
`RepresentationSemantics/registry/math-teaching-primitive-registry.json` has a
real realization; a registry entry with no realization fails the render with
`TEACHING_PRIMITIVE_LABEL_ONLY_NOT_REALIZED`. Coordinate frames, slope
triangles, transversal/angle figures, combinatorial slot models and
equivalence-balance views are drawn from the item's **declared** data —
`assert_grounded` refuses to draw any numeric literal that does not appear
verbatim in the declared source text (`MATH_VISUAL_UNGROUNDED_VALUE`). Where an
item declares no numeric instance, the frame is drawn symbolically and the
placement is recorded as `data_grounding: DECLARED_SYMBOLIC` rather than being
padded with invented values.

### Shared visual library seam

Drawing is delegated to the subject-agnostic package vendored at
`Grade 9/V2/Shared/MasterTemplates/primitives/` (from PR #310). That package is
treated as a **read-only dependency**: this subject renderer adapts Mathematics
semantics onto it and never edits it. `_LIBRARY_BINDINGS` in
`math_primitive_adapter.py` is the single table that says which library object
realizes which teaching primitive, so swapping to #310's published package later
is a change to that table, not to any call site.

### What a green render does and does not mean

`PUBLICATION_ENGINEERING = PASS` only. `SUBJECT_CORRECTNESS`,
`PEDAGOGICAL_DESIGN`, `ASSESSMENT_DESIGN` and `VISUAL_USABILITY` are emitted as
`PENDING` and can only be decided by M-L from authorized human review receipts
bound to the exact artifact-set digest. While the bound PCK is provisional
(`pck_expert_review_state = PENDING`), `release_legal` is `false` and claiming
otherwise raises `PROVISIONAL_PRODUCT_CLAIMED_RELEASE_LEGAL`.

## LEGACY / REFERENCE ONLY: MATH-V2-05 publication realization

`engine/realize_math_publication.py`, `engine/build_semantic_product.py`,
`validator/`, `fixtures/`, `METHODOLOGY.md`, `TRANSFER_PLAN.md` and the
`math-publication-*` / `math-physical-page-map` / `math-learner-semantic-product`
contracts belong to the **MATH-V2-01..07** lineage (issue #212, PRs #160/#161/#202).
That lineage consumes `MathLearningDesignPlan` from
`Grade 9/V2/Mathematics/LearningDesign/`, which is itself legacy (see its
`LEGACY.md`), and is not connected to the M-A→M-L chain.

Its engineering was **adopted rather than rebuilt**, per #174 §7: material
custody, `PublicationStructure`, `PhysicalPageMap`, ReportLab placement
instrumentation and exact PDF hash binding all reappear in
`realize_math_core_products.py`, rewritten around M-chain ownership.

Do not extend the legacy engine, and do not treat its `candidate.pdf` or its
`publication_manifest.json` as release evidence for the M-chain.

Tracking: #319 (live), #212 (legacy).
