# Sequence & Series Generated Artifact Manifest

The Markdown/YAML specifications in this folder are the reproducible authoring authority. Generated PDFs are publication artifacts and must remain traceable to the specification and source map.

## Current generated artifacts

| Artifact | Purpose | SHA-256 |
|---|---|---|
| `Sequence_Series_Concept_Book_Grade9_v2.pdf` | Revised Mathematics Concept Book using SEE -> REALIZE -> UNDERSTAND -> ADOPT | `2741c9899dabeb8c1aabcf94e7346e64efd261e8fe007f9701710ea16340dc36` |
| `Sequence_Series_First_Step_Reference_Book_v2.pdf` | Recognition-first companion with 18-question JEE bridge | `b4eb6db80cbb981f2c87c0823162d69fc4c072f81c2fe1540c578c17d1872f54` |

## Publication authority

A PDF is considered current only if it is consistent with:

1. `Sequence_Series_Concept_Book_Spec.md`;
2. `Sequence_Series_First_Step_Reference_Spec.md`;
3. `Sequence_Series_Source_Coverage_Map.md`;
4. `sequence_series_source_map.yaml`;
5. `Sequence_Series_JEE_Bridge_Map.md`;
6. `../../skills/grade9-math/references/concept-book-see-realize-understand-adopt.md`.

## Required PDF QA

Before publishing a regenerated PDF:

- confirm handwritten/source coverage remains mapped;
- confirm external bridge material is visibly distinguished from source authority;
- confirm each major Concept Book idea passes applicable SEE/REALIZE/UNDERSTAND/ADOPT gates;
- confirm summation is introduced as repeated addition before sigma manipulation;
- confirm ADOPT contains independent first-move and transfer tasks;
- inspect fonts and mathematical glyphs after final rendering;
- reject missing sigma/radical/inequality glyphs, clipped superscripts/subscripts, broken fractions, or inconsistent fallback fonts;
- visually inspect representative AP/GP derivation, sigma, nested-sum, alternating-sum and JEE-bridge pages.

## Binary storage note

As with the Motion exemplar, the authoring authority is intentionally kept in text form so it is reviewable and diffable. Binary publication artifacts may be stored in the chapter folder or release workflow where appropriate; the checksums above identify the current generated builds.
