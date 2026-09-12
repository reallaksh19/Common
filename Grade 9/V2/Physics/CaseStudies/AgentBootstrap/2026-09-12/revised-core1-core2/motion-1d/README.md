# Motion in 1D - Revised Core 1 and Core 2

This is the second topic in the topic-by-topic Physics learner-product rebuild. It supersedes the earlier Motion-in-1D exploratory/recovery artifacts as the current case-study implementation target.

## Revised Core 1

Core 1 is a teaching product, not a formula summary. Eleven competency families are taught through:

`physical event -> axis / clock -> state -> representation -> relation construction / validity -> worked example -> guided -> faded -> rebuild -> watch out -> quick check + answer`

The competency surface is:

1. distance vs displacement
2. average speed vs average velocity
3. equal-time vs equal-distance weighting
4. velocity sign, acceleration sign and reversal
5. UVATS/state-table model and equation selection
6. reconstruction of the constant-acceleration equation family
7. multiphase motion and delayed starts
8. vertical motion / free fall
9. position-time graphs
10. velocity-time / acceleration-time graphs
11. interval motion, nth-second reasoning and graph consistency

## Revised Core 2

Fourteen transfer items stress those competencies. Attempt pages use the frozen hint contract:

- H1 asks an open-ended question about the decisive physics and reveals only that concept/state.
- H2 asks how to represent the situation and reveals the matching diagram/state table/graph/clock.
- H3 asks what to write first and reveals one executable starting relation only.
- Every hint is self-contained when revealed.
- Exactly two writing lines follow the ladder.

Worked pages use the complete ladder:

`UNDERSTAND -> REPRESENT -> CONNECT -> CALCULATE -> INTERPRET`

Every necessary state transition, substitution, sign choice and unit-bearing step is shown. Quick check and alternate check are supplemental; they never substitute for the explicit answer.

## Representation rules

Problem-state figures must match the actual question. Generic phase figures are not acceptable when the concrete state is known. The rebuild includes dedicated representations for reversal, round-trip averages, sign states, UVATS, x-t and v-t graphs, multiphase motion, free-fall comparisons, relative acceleration, equal-distance weighting, later-interval displacement, delayed-start catch-up and x-t graph consistency.

## Layout / typography

- DejaVu Sans embedded throughout.
- Core 1 and Core 2 use content-height cards; no fixed empty teaching boxes.
- Long practice headers are shortened instead of spilling beyond the page.
- Solution figures use problem-specific compact variants rather than squeezing full-width figures.
- Base learner text remains above the practical font floor; smaller extracted sizes are limited to sub/superscript rendering.
- No raw authoring labels such as `phase 1 -> boundary state -> phase 2` remain when physical events can be named directly.

## QA

See `physics-motion-1d-revised-core1-core2-audit.json`. Final PDFs were rendered at 180 dpi after the last build and visually inspected. Automated checks report zero out-of-bounds text and zero severe overlap flags in both products.

## Files

- `physics-motion-1d-revised-core1.pdf`
- `physics-motion-1d-revised-core2.pdf`
- `physics-motion-1d-revised-core1-core2-audit.json`
- `build_motion1d_revised_core1_core2.py`
