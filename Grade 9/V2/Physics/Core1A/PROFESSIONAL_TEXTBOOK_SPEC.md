# Core (1A) professional textbook publication spec

This file controls the publication layer after the SBA teaching plan is complete. It must not be used to simplify away pedagogy.

## 1. Lossless professionalisation

Professionalisation may change composition, typography, page rhythm, callout placement, figure size and page count. It may not remove an instructional function that exists in the authorised SBA profile or transfer routine.

Before replacing an older learner build, make a function map from the old build/profile to the new one. Every required function must have a destination, including:

- foundation diagnostic / prerequisite route;
- model contract and validity;
- staged concept figures;
- misconception evidence and rebuild;
- worked example reasoning;
- Complete One / faded practice when required;
- independent practice before hints;
- H1/H2/H3 support;
- readiness gate;
- exact Core (2) transfer / hold state.

If an instructional function has no destination, fail with `CORE1A_PROFESSIONALISATION_CONTENT_LOSS`.

## 2. Heading hierarchy

Large headings are reserved for bucket openers only. Ordinary page headings must not look like cover titles.

Recommended / maximum sizes:

- bucket opener: 22-26 pt;
- ordinary page section heading: 14-16 pt;
- long page heading: 13-14.5 pt;
- subsection heading: 10-12 pt;
- small kicker / atom label: 7.5-9 pt.

A heading such as `Velocity components at a stated instant` is an ordinary page heading, not a bucket opener. It must use the ordinary/long page-heading tier. Oversized page headings fail with `CORE1A_PAGE_HEADING_TOO_LARGE`.

## 3. Textbook composition

Prefer:

- running heads instead of repeated production banners;
- normal explanatory prose plus one dominant teaching figure;
- fewer, more meaningful callout boxes;
- `Why this step | Working` for worked examples;
- two-page or multi-page concept rhythm when the idea is difficult;
- intentional white space and larger figures instead of dense card stacks.

Do not expose production phrases such as `novice build`, `20% knowledge path`, schema names or internal teaching-home identifiers on every learner page. The learner should experience the support, not the production machinery.

## 4. Figures

Hard concept = larger figure area and fewer inferential jumps.

- Use staged local viewports and semantic labels.
- Keep figure labels clear of axes, curves, captions and panel boundaries.
- Prefer a figure occupying 35-55% of meaningful page area when it carries the central concept.
- Re-render and inspect all figures; a collision or unreadable label is a build failure.

## 5. Practice and transfer

Professional layout must preserve the SBA transfer grammar:

`WATCH ONE -> COMPLETE ONE -> INDEPENDENT PRACTICE -> H1/H2/H3 -> READINESS -> CORE (2)`

Do not merge Complete One and Independent Practice merely to reduce page count when that removes the fading-support step.

## 6. Reference builds

- SBA-03 professional-lossless v2 establishes the lossless rebuild principle.
- SBA-06 professional-lossless v1 establishes the restrained heading scale for D3 pages and two-family trajectory transfer.

Use these as design references, not fixed templates.
