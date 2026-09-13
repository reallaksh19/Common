# M-UPGRADE-2 handoff — Mathematics learner-product maturity

This directory is the continuation handoff for issue **#358**
(`[M-UPGRADE-2] Mathematics learner-product maturity`). It is a **sibling of the #345
handoff**, not a new lineage:

```text
Grade 9/V2/Mathematics/StressTestArtifacts/
├── PR323/          <- draft PR #345, the seven-topic stress-test handoff. READ IT FIRST.
│                      (branch `pr323-stress-test-artifacts-ready4`, based on #323)
└── M-UPGRADE-2/    <- this directory: what #358 turned those findings into, in code
```

`PR323/` is not present on this branch because #345 is based directly on #323 while this
work is stacked on #351. Nothing here supersedes it: `PR323/README.md`, `STATUS.json`,
`CONSOLIDATED_REBUILD_PLAN.md`, `ARTIFACT_SHA256.txt` and `BINARY_ARTIFACT_BUNDLE.md`
remain the authority for the **topic-by-topic artifact state**, the NCERT source
authorities, and the binary bundle. This directory is the authority for the **contract and
falsifier state**.

A new agent should read, in order:

1. `PR323/README.md` and `PR323/STATUS.json` from draft PR #345 — topic status, artifact
   inventory, hashes, and the continuation order for the remaining topics;
2. PR #323 comment `5646045040` (consolidated superseding review) and comment
   `5647300608` (RCA) — still the normative sources;
3. `STATUS.json` in this directory — what #358 built, what it deliberately did not build,
   and what is open;
4. `FALSIFIER_INDEX.json` — every gate now in code, with the phase that raises it and the
   stress-test finding it came from;
5. `CONTINUATION_ORDER.md` — the exact next steps.

## What changed since #345 was written

#345 was written against PR #323. Two things have moved since:

- **#351** added Core1A/Core2A and then, during this work, a full `LearnerProduct/`
  execution contract: an 18-stage ordered pipeline (LP-00..LP-17), a two-lane Core2A
  (`SOURCE_CORE2` / `GENERATED_CHALLENGE`), per-question inline citation, a competitive
  archetype registry, and a central `math-learner-language-policy.json`.
- **#358** (this work) added the semantic layers that contract sequences but does not
  itself define.

The division of responsibility that resulted is worth preserving, because it was not
obvious from either side alone:

```text
#351 LearnerProduct  ->  WHICH stages run, in WHAT ORDER, under WHICH policies
#358 (this work)     ->  WHAT COUNTS as valid content inside those stages
```

For example, `LP-13 AUTHOR_FULL_WORKING` says full working must be authored at that point
in the sequence. It does not say that "Compute S1, compute S2" is not full working. That
is `MATH_OPERATION_NAMED_BUT_NOT_DEMONSTRATED` in `LearnerRealization`.

## What this work added, as phases

| Phase | Issue item | What it makes falsifiable |
| --- | --- | --- |
| `MathTypesetting/` | 1 | mathematics is a structured AST and is typeset, never ASCII-flattened |
| `LearnerRealization/` | 2, 5, 8, 9 | a step shows a real state transition; transformations carry invariant witnesses; every question has answer custody; internal labels never reach the page |
| `SourceLedger/` | 3 | completeness at question level **and** atomic-ask level, surviving to the rendered page |
| `RepresentationSemantics/` (additive) | 4 | figures declare their own semantics; givens are separated from what the learner must supply |
| `Core1Reconstruction/` | 6 | the teaching chain is realized, not labelled; Core2 reasoning resolves to Core1 evidence |
| `LayoutSafety/` | 7 | readable size per semantic role, sibling collision, measured pagination |

Each phase follows the repository's existing shape
(`contracts/ engine/ registry/ policies/ fixtures/ tests/`), uses deterministic digests,
fails closed, and is exercised by falsifier-driven tests that mutate one correct artifact at
a time.

## Semantic decisions worth preserving

These are the decisions discovered through failure during this work. They cost more to
rediscover than to read.

1. **A rendered superscript cannot be checked by text extraction.** A genuinely typeset
   script is a smaller glyph on a raised baseline, so PDF extraction returns `x2`, not `x²`.
   Rendered-page evidence for a real script is therefore *geometric* (a reduced-size span at
   the declared ratio); extracted text is what proves no ASCII flattening survived. Every
   post-render gate in this work respects that split.

2. **Astral-plane glyphs cannot be gated after rendering.** `𝕎` (U+1D54E) is present in
   DejaVu but does not round-trip through PDF text extraction. `WHOLES` therefore binds to
   the NCERT-conventional `W`. A glyph that cannot be read back cannot be gated.

3. **Teaching evidence must be derived, not declared.** If a Core1 chain can *state* the
   reasoning it teaches, it will eventually state more than it contains. The evidence tokens
   are computed from the chain's own realized derivations, and trivial steps are excluded —
   a `CLASSIFY` step that restates the givens is not evidence for a Core2 `TRANSFORM`.

4. **Cross-core linkage must be state-level, not lesson-level.** A row pointing a `SETUP`
   state at `MATH-C1L-FACTOR-THEOREM` rather than `MATH-C1L-FACTOR-THEOREM#SETUP` passes a
   lesson-reference check and proves nothing.

5. **Completeness is two-dimensional and the second dimension is not derivable from the
   first.** The probe corpus has 4 top-level rows and 12 atomic asks. Losing one subpart
   leaves the row count perfect.

6. **Occlusion is invisible to both a JSON equality check and a page-bounds check.** The
   occlusion test asserts this directly: after the mutation, the covered option text is
   *still present in the extracted page text*, and the gate still fails.

7. **Whitespace alone is not a layout failure.** Neither is slightly small type on a full
   page. The failure is the conjunction, which is why
   `MICROTYPE_USED_WHILE_EXPANDABLE_SPACE_EXISTS` takes both.

8. **Containment is not collision.** Sibling-pair checking needs an explicit `container_id`;
   without it every child overlapping its own panel reads as a collision, and the check gets
   disabled.

9. **A converse must genuinely swap the implication.** A "converse" whose condition is not
   the forward conclusion is a re-typed forward statement, and Core2 proof routes that need
   the reverse direction will silently have no teaching behind them.

10. **Do not build a second ban-list.** #351's `math-learner-language-policy.json` is the
    learner-language authority. What was missing was an engine to enforce it and the role
    labels it did not cover; both were added to *that* file and a shared detector, not to a
    parallel registry.

## Release meaning — unchanged

Everything in this work is `PUBLICATION_ENGINEERING` only.

- No PCK moves beyond `PROVISIONAL_PROMOTED`.
- Expert review stays `PENDING`.
- Subject, pedagogy, assessment and visual-usability review stay `PENDING`.
- No human or expert review is asserted anywhere, and no gate in this work can assert one.

A green audit bundle means the learner-product **objects** are strong enough that the
renderer is publishing already-mature mathematics. It does not mean the mathematics has
been reviewed.

## Honest statement of what is NOT done

See `STATUS.json` for the machine-readable version. In prose:

- The new gates run against **reference fixtures**, not against the full seven-topic
  corpus. Number Systems, Polynomials, Coordinate Geometry and Linear Equations have
  realized instances; Euclid's Geometry, Lines & Angles and Surface Areas & Volumes appear
  only as *shapes* in the source-ledger probe, not as realized learner mathematics.
- Nothing here is yet wired into `LearnerProduct`'s `STAGE_RUNNERS`, which remains empty by
  design. These phases are callable libraries plus gates; the ordered pipeline does not yet
  invoke them.
- `Core1A`'s textbook engine consumes the shared learner-copy detector, but its worked
  examples are not yet emitted through `MathTypesetting`; Core1A output still goes through
  its own `safe_text()` path.
- `Publication/engine/realize_math_core_products.py` still contains the original
  `ascii_safe()` flattening function. It is no longer the only path available, but it has
  **not** been removed, and the #323 renderer still uses it.
- No end-to-end learner PDF has been produced through the whole new stack. The rendered
  evidence in this work comes from two purpose-built probes (an attempt-page probe and a
  layout probe), which is enough to falsify the gates but is not a product.
