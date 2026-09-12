# Chemistry V2 C-L — Exact Product Quality Gate

This gate is the publication-quality firewall after C-K cold-start generation.

It binds machine evidence, exact PDF byte hashes, semantic custody, human reviews and final mature-design comparison without allowing any one class of evidence to impersonate another.

## Release sequence

```text
C-K frozen semantic candidate
-> exact Core1/Core2 PDF bytes + page/render evidence
-> machine exact-product gate
-> AI pre-review (advisory only)
-> authorized Chemistry subject review
-> authorized pedagogy review
-> authorized assessment review
-> authorized visual/usability review
-> frozen PR #157 mature-design comparison
-> V2_MATURE_INSTRUCTIONAL_PRODUCT
```

PR #157 is permitted only in the final comparison stage. It remains forbidden producer input.

## Quality states

Tracked independently:

- `PUBLICATION_ENGINEERING`
- `SUBJECT_CORRECTNESS`
- `PEDAGOGICAL_DESIGN`
- `ASSESSMENT_DESIGN`
- `VISUAL_USABILITY`
- `MATURE_DESIGN_QUALITY`
- `REFERENCE_COMPARABILITY`

Learning effectiveness is separate and defaults to `STUDY_REQUIRED`; a polished or human-approved PDF is not evidence of validated learning efficacy.

## Blocking semantics

The command-line evaluator uses:

```text
0 = exact product and all required release gates PASS
1 = technical/validation FAIL
2 = BLOCKED because exact artifacts or authorized manual gates are incomplete
```

Machine-green with missing authorized human review must return `2`, never `0`.

## Required topology

Exactly two learner-facing PDFs are supported:

1. Core Study Guide, containing main teaching plus Appendix A Core Practice, Appendix B Core Solutions and Appendix C Printable Handout.
2. ExamSIDE Solution & Transfer Book.

Appendix C is not emitted as a third required PDF.

## Current C-L boundary

The repository now defines and tests the machine quality firewall and exact-review custody semantics. Production mature status remains blocked until exact rendered Chemistry PDFs and authorized review attestations bound to those exact PDF hashes exist.

## Realized teaching primitives (issue #321)

The renderer previously called only `drawString`/`setFont`, so every C-H
teaching primitive reached the learner as prose. It now draws real vector
graphics through one stable interface:

```python
render_primitive(kind, params, canvas, bbox)   # chemistry_visual_primitives
primitive_height(kind, params, width)
```

- **Selection stays C-H authority.** `chemistry-page-intent-profile.json`
  chooses which primitive a capability gets (`renderer_selection_forbidden`);
  the renderer only decides where it lands on the page.
- **Every value is source-authorized.** Coefficients, subscripts, charges,
  particle counts, atom ledgers and oxidation-state values are parsed by
  `chemistry_notation.py` out of the item's own notation tokens. The renderer
  invents no chemistry: when source data cannot support a primitive honestly,
  nothing is drawn and the kind is recorded in
  `machine_evidence.teaching_primitives_label_only`.
- **Generic, not topic-specific.** Reaction type and species role are data
  flowing through one parser and one primitive set. Redox is one instance of
  the generic contract, never its own schema.
- **Fail-closed before drawing.** Each call runs the shared
  `VisualSemanticValidator` (vendored from PR #310), so an ungrounded species,
  a broken atom ledger or an inverted agent role raises
  `UngroundedEntityError` / `ConservationError` / `RolePolarityError` instead
  of reaching the page.

### Relationship to the shared MasterTemplates library

`Grade 9/V2/Shared/MasterTemplates/primitives/` is vendored verbatim from
PR #310 (commit `88d3a719`) and is **read-only** here. Chemistry consumes its
`Palette`, card/pill/arrow helpers, `OxidationLaneDiagram` and
`VisualSemanticValidator`. Two upstream engines cannot be used yet because
they still draw their prototype example regardless of arguments; they are
listed in `chemistry_visual_primitives.UPSTREAM_HARDCODED_ENGINES` for upstream
repair rather than patched locally, and Chemistry draws those two primitives
from real data in the meantime through the same interface.

## Learner-surface firewall

`learner_surface_guard.py` rejects any internal-identifier-shaped token in
rendered learner-facing text. Shapes are derived from the identifier spellings
the Chemistry registries actually use (`CAP-...`, `CORE1-CAP-...`,
`CHEM-CONCEPT-...`, `CHECK_SPECIES_IDENTITY`, `OBLIGATION_REP:FORMULA`, `CQ12`,
`EXT05`, ...). The guard runs three times: while drawing (aborting the render),
in the AI pre-review over extracted page text, and in the independent custody
validator.

## Physical placement custody

`physical_page_map()` emits a placement fragment at the moment each block is
drawn - `START` on the first page, `CONTINUATION` after a break - and binds the
map to the exact PDF SHA256. `validator/validate_chemistry_custody.py`
recomputes all of it from the bytes on disk: hash binding, page-intent
reconciliation, physical bounds, orphan continuations and primitive validation
provenance. Custody model adapted from PR #161 / PR #196.

## Durable frozen candidate

`candidates/CHEM-C-L-EXACT-CANDIDATE-A/` holds the exact reviewed bytes plus a
`FROZEN_MANIFEST.json` of per-file SHA256 and a non-self-referential package
digest, so the candidate survives GitHub Actions artifact retention. CI
verifies that copy on every run and can publish the same bundle as a Release
asset on manual dispatch.

## What none of this establishes

Everything above is **publication engineering**. The AI pre-review is an
`AI_PRE_REVIEW` and records `production_claim: false`; it is not, and may not
be presented as, expert review. `SUBJECT_CORRECTNESS`, `PEDAGOGICAL_DESIGN`,
`ASSESSMENT_DESIGN`, `VISUAL_USABILITY` and `MATURE_DESIGN_QUALITY` remain
`PENDING` until real authorized human reviewers attest against these exact
artifact hashes.
