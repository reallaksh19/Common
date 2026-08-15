# Motion Generated Artifact Manifest

The Markdown/YAML specifications in this folder are the reproducible authoring authority. Generated PDFs are publication artifacts and must remain traceable to the specification and source map.

## Current generated artifacts

| Artifact | Purpose | SHA-256 |
|---|---|---|
| `Motion_Concept_Book_Grade9_Revised.pdf` | Grade 9 concept/reference book using SEE -> REALIZE -> UNDERSTAND | `21b3a8fc7c74274172f18fd052519b1b71ff2485aec769ceee4742428391317b` |
| `Motion_Concept_Book_Source_Coverage_and_QA_Map.pdf` | Human-readable source coverage / authoring QA map | `204ab84ffe533e19a842d3e18212fad197112002fa2ae0dc815acb7e43c19c47` |
| `Motion_First_Step_Reference_Book.pdf` | Companion first-step/problem-recognition reference | `f00c28c9e6d3b3888d14e715596ef17212a915565f7ca9075896a9476c95f54b` |

## Publication authority

A PDF is considered current only if it is consistent with:

1. `Motion_Concept_Book_Spec.md`;
2. `Motion_Source_Coverage_Map.md`;
3. `motion_source_map.yaml`;
4. `../../skills/grade9-physics/references/concept-book-see-realize-understand.md`.

## Required PDF QA

Before publishing a regenerated PDF:

- confirm source coverage remains 68/68;
- confirm every major equation has SEE, REALIZE and UNDERSTAND treatment;
- confirm Grade 9 depth rather than elementary-only exposition;
- confirm source QA flags are preserved;
- inspect fonts and mathematical glyphs after final rendering;
- reject missing glyphs, substituted symbols, clipped superscripts/subscripts, or inconsistent fallback fonts;
- visually inspect representative derivation, graph, gravity, and equation-heavy pages.

## Binary storage note

The authoring authority is intentionally kept in text form so it is reviewable and diffable. Binary publication artifacts may be added to the chapter folder or a release when the repository workflow supports direct binary artifact upload; checksums above identify the current generated builds.
