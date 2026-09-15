---
name: grade9-physics-publication
description: Band-aware Physics publication engine for Grade 9-11. Render learner-band PDFs (30/50/90 percent prior knowledge) from a declarative publication JSON, with a fixed block schema, reserved figure placeholders, badge and callout vocabulary, source-obligation citation ledgers, internal linkage closure, page-density and glyph gates, and a deterministic pre-release audit. Use whenever producing, re-rendering, auditing or fixing a Physics study guide, concept book, transfer book, practice set or PYQ book as a PDF, and whenever a physics PDF must be checked for band drift, missing citations, blank pages, preview leakage or notation defects before release.
---

# Grade 9 Physics Publication

Render banded Physics learning products from structured data. The PDF is an output; the publication JSON is the source of truth. Never edit the PDF and never let layout convenience change pedagogy.

## 0. Which publisher is this?

The repository has three publication engines and they are not interchangeable.

| Engine | Source of truth | Use when |
|---|---|---|
| `grade9-publication` | An existing source PDF or book | Reconstructing and reconciling supplied material |
| `grade9-textbook-publisher` | Validated canonical master data | Rendering a generic linked textbook or bank |
| **`grade9-physics-publication`** | **A banded physics publication JSON** | **Publishing physics teaching material where the learner band determines the page** |

The distinctive claim is the band. The same two subtopics produce two structurally different books at B30 and B90 — different block types, different module order, different hint visibility, different density. A publisher that ignores the band produces one book that serves the middle and fails both ends.

This engine consumes `grade9-physics` for correctness, band policy, conventions and gates. It may not redefine any of them.

## 1. Pipeline

```
physics authority (band, conventions, gates)
      → publication JSON  (schema §2)
      → render_physics_book.py      → PDF
      → check_physics_publication.py → audit report
      → rasterise + look at every page
      → drift register entry
      → release
```

Nothing is released on the audit alone. The audit catches what is countable; rasterise the pages and look at them, because glyph placement, visual rhythm and whether a page reads as a coherent spread are not countable properties.

## 2. Publication schema

```jsonc
{
  "publication": {
    "publication_id": "PHY-MOT-B30-v1",
    "series": "Grade 9 Physics · Motion",
    "title": "...", "subtitle": "...",
    "band": "B30",                    // B30 | B50 | B80 | B90
    "band_label": "building the foundation",
    "grade": 9,
    "build_contract_ref": "PHY-MOTION-2026-01",   // links to the frozen contract
    "frame": "Motion to the right is positive...",
    "sign_convention": "right positive · left negative",
    "symbol_table": { "s": "displacement (never distance)" },
    "source_ledger_id": "SRC-MOTION-v1",
    "hint_policy_badge": "HINTS PRE-LOADED",
    "audience": "...",                // who this is for, in plain words
    "placement_note": "P1 ✗ P2 ✗ → B30",
    "band_rationale": "...",          // why the book is shaped this way
    "how_to_use": [["do this", "because"]]
  },
  "subtopics": [{
    "subtopic_id": "M-01",
    "concept_id": "PHY-MOT-C01",
    "title": "...",
    "blocks": [ /* §3 */ ]
  }],
  "audit": { "checkpoints": { "GATE NAME": "PASS — evidence" } }
}
```

Every block carries `source_obligation_ids`. An empty array means VALUE_ADD and is legal; a **missing key is a citation failure and blocks release**. There is no third state, because "we forgot" and "this is ours" must not look the same in the ledger.

### Placement percentages map to bands

`< 40` → B30 · `40-75` → B50 · `> 75` → B90. Between 75 and 85, publish as **B80**: B90 architecture with derivation bridges retained rather than assumed. A learner at 80% typically holds a derivation without owning it, and removing it entirely is the one way to break an otherwise strong student.

## 3. Block vocabulary

Blocks are band-gated. The auditor rejects a block type that does not belong to the declared band.

| Block | B30 | B50 | B80/B90 | Purpose |
|---|:-:|:-:|:-:|---|
| `prereq_check` | ● required | ● | | Named ask + named destination on failure |
| `purpose_anchor` | ● required | ● | | One situation, opened with and returned to |
| `worked` | ● | ● | ✗ | Complete solution, nothing elided |
| `name_card` | ● | ● | ✗ | The rule, arriving after it has been computed |
| `fade_ladder` | ● | | ✗ | One support removed per stage |
| `notice` | ● | ● | | First recognition task |
| `exit_check` | ● | ● | | Return to anchor, no numbers |
| `compression_card` | | | ● required | Cue / first move / check / trap on one page |
| `discrimination` | | ● | ● required | Pairs differing in exactly one feature |
| `stress_set` | | | ● | Unlabelled, mixed, timed |
| `boundary_set` | | ● | ● | Limits, sign reversals, degenerate cases |
| `preview` | ✗ | ✗ | ● | Grade-11 preview, unscored, formalism unnamed |
| `misconception` | ● | ● | ● | Wrong model + why attractive + probe + repair |
| `gap_map` | ● | ● | ● | Wrong answer → gap → destination |
| `practice` | ● | ● | ● | Mix per the band contract |
| `figure` | ● | ● | ● | Reserved placeholder, §4 |
| `callout`, `prose`, `equation`, `heading` | ● | ● | ● | General |

`worked`, `name_card`, `fade_ladder` and `purpose_anchor` re-teach. Their presence in a B80/B90 book is band drift and blocks release — a near-complete learner does not need the concept explained, and explaining it reads as condescension.

## 4. Figure placeholders

A book is publishable before its artwork exists. A placeholder is a first-class object, not a gap.

```jsonc
{ "type": "figure",
  "figure_id": "FIG-M02-01",
  "status": "RESERVED",           // RESERVED | DRAFTED | FINAL
  "reserve_mm": 52,               // exact bounds, fixed now
  "semantic_spec": [              // enough for someone else to draw it
    "Velocity–time axes, v 0–12, t 0–7, gridlines every 1",
    "Grid must be countable — this figure exists to be counted, not admired",
    "One square outlined in bold, labelled '1 m/s × 1 s = 1 m'"],
  "caption": "...",
  "source_obligation_ids": ["SRC-MOTION-v1/§3.4"] }
```

Reserving exact bounds now means inserting the real artwork later cannot reflow the page. The semantic spec must be sufficient for a different person to draw it without asking questions — axes, ranges, gridlines, labels, what is shaded, and what must *not* appear. For discrimination figures, the spec must also forbid the caption revealing the answer.

Never invent a figure because a page looks empty. Fix the emptiness with content.

## 5. Badges

Badges carry state onto the student page without cluttering it. Full state lives in the appendix ledger.

| Badge | Meaning |
|---|---|
| `BAND` | Which learner this page is built for |
| `SOURCE` | Traces to a source obligation |
| `VALUE_ADD` | Ours, deliberately, not an omission |
| `MODEL` | A simplification is in use here |
| `NOT_SCORED` | Never enters assessment or a coverage denominator |
| `HINT` | Hint policy in force — pre-loaded, earned, or none |
| `PREREQ` | A prerequisite gate sits here |
| `GAP` | Error routing attached |
| `PREVIEW` | Grade-11 forward material |
| `PLACEHOLDER` | Artwork pending |

`NOT_SCORED` on every preview block is enforced. Preview material inside a coverage denominator corrupts every downstream audit and silently redefines the grade level of the book.

## 6. Linkage and citation

Two identities are kept for everything: the immutable source ID, and the generated publication label. Page numbers are derived after layout and are never authoritative.

Every book ends with an appendix ledger that is generated, not written: block → source obligation, figure → status and reserved bounds, and the audit checkpoints that were cleared at render time. Required closure at release:

```
blocks_with_source_key   = blocks_total
broken_references        = 0
orphan_targets           = 0
duplicate_publication_ids = 0
```

## 7. Audit gates

`check_physics_publication.py book.json book.pdf` — exits non-zero on any BLOCK row.

| Gate | Blocks release when |
|---|---|
| `SRU-23 BAND_DECLARED` | No band, or an unknown band |
| `D1 BAND_FIDELITY` | A block type illegal for the declared band |
| `D1 NO_RETEACH_AT_HIGH_BAND` | A re-teaching block appears at B80/B90 |
| `CITATION_CLOSURE` | Any block has no source key at all |
| `PREVIEW_FENCED` | Preview at B30/B50, or preview without `NOT_SCORED` |
| `SRU-19 GAP_MAP_COVERAGE` | A subtopic has answerable blocks and no gap map |
| `SRU-26 PREREQUISITE_ROUTED` | A gap row names no destination |
| `B30_PREREQ_REQUIRED` | A B30 book with no prerequisite check |
| `FIGURE_PLACEHOLDER_SPEC` | A placeholder without bounds or semantic spec |
| `GLYPH_INTEGRITY` | Replacement or box glyphs anywhere |
| `NO_BLANK_PAGES` | Any empty page |
| `PAGE_DENSITY_70_85` | Warning only — see §8 |

Density is a warning rather than a blocker because the honest response to a thin page is usually to add the content the band contract already required, not to compress what is there. Treat every warning as a content question first.

## 8. Measuring density honestly

Occupancy is the union of vertical bands containing text or rules inside the content frame, divided by frame height. Three rules make the number mean something:

- **Exclude running head and footer.** Counting chrome as content is how a density gate reports over 100% and passes a half-empty page.
- **Exclude the cover and the appendix.** They are not ordinary learning pages, and including them hides real voids elsewhere.
- **Merge bands with a small tolerance.** Ordinary line leading is not a void; a 200-point gap is.

Ruled working space counts as meaningful occupancy. A B30 page that is 40% work zone is doing its job.

## 9. Typography

Register DejaVu, or another font with complete coverage, before rendering anything. ReportLab's built-in fonts have no subscript, superscript, Greek or arrow glyphs and render them as solid black boxes — which passes a text-extraction check and fails a reader.

Publish true notation: `v₁`, `m s⁻²`, `√(t₁t₂)`, `−5 m/s`, `Δv`. Keep the raw source string in the audit model. Never infer index-versus-exponent semantics from typography alone; resolve it from the source relation.

## 10. Reserve → draw → advance

Every component declares its bounds, wraps its content, reserves vertical space, draws, then advances. Never continue from a guessed y-coordinate after a fixed-height component; that is the mechanism behind every overlap and clipped equation.

Use a conditional break, not an unconditional one, when starting a subtopic on a fresh page. An unconditional break emitted against an already-fresh frame produces a blank sheet.

## 11. Render-first QA

Deterministic checks pass on files that read badly. After every render:

1. save the artifact;
2. rasterise **every** page at 100 dpi or better;
3. look at each one — equations, clipping, badge alignment, page rhythm, voids, whether the page reads as a coherent spread rather than a stack of cards;
4. run the audit;
5. record the result in the drift register, including clean runs;
6. re-render and repeat after any fix. Never patch the PDF.

## 12. Completion gates

Do not release until: zero blocking audit rows · every page visually inspected after the final render · every density warning either resolved or recorded with a reason · the appendix ledger regenerated from the final source · the drift register updated.

## Scripts

- `scripts/render_physics_book.py book.json out.pdf`
- `scripts/check_physics_publication.py book.json out.pdf`
