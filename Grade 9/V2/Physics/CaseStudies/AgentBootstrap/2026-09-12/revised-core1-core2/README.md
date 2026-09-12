# Motion in a Plane - Revised Core 1 and Core 2

This folder is the current handoff target for the Motion in 2D / Motion in a Plane case study.

## Frozen learner format

### Revised Core 1

Each concept page follows this learner grammar:

`physical picture -> What is happening? -> Key idea -> How it works -> Worked example -> Watch out -> Quick check + answer`

The chapter contains 22 concept families and an explicit Q1-Q59 review map. The concept surface covers the supplied theory plus the demands exposed by the complete numbered challenge bank.

### Revised Core 2 attempt pages

`question -> physics picture -> Hint 1: Spot the key idea -> Hint 2: Set it up -> Hint 3: First step -> exactly two writing lines`

Hints are content-height, not fixed-height filler. H3 performs one executable first move only and must not resolve the requested answer.

### Revised Core 2 worked pages

`question recap -> picture / known state -> reasoning ladder -> Answer -> Quick check -> Check it another way -> Watch out -> Review this idea`

The full reasoning ladder is frozen as:

1. UNDERSTAND
2. REPRESENT
3. CONNECT
4. CALCULATE
5. INTERPRET

Every rung must contain the actual physics of the item. Generic filler such as "identify the clue" or "choose a relation" is not sufficient.

## Answer requirement

All 59 numbered questions must have an explicit answer mapping. Quick checks and verification do not substitute for an answer.

## Source boundary

The rebuild uses the supplied `Motion in 2d(2).pdf` / `Motion in 2d.pdf`. The source scan is not redistributed in this handoff. Q49 and Q51 remain source-ambiguous because the supplied scan clips part of those items; missing wording must not be invented.

## Current verified output

- Revised Core 1: 27 pages, 22 concept pages, Q1-Q59 all mapped.
- Revised Core 2: 122 pages, 59 protected attempts, 59 worked solutions, 59 answers.
- Attempt workspace: exactly 2 lines per question.
- Full solution ladder: UNDERSTAND -> REPRESENT -> CONNECT -> CALCULATE -> INTERPRET.
- Automated bbox audit: zero out-of-bounds text; zero severe text-overlap flags.
- Both PDFs were rendered after the final build for visual verification.

Expected output filenames:

- `physics-motion-2d-revised-core1.pdf`
- `physics-motion-2d-revised-core2.pdf`
- `physics-motion-2d-revised-core1-core2-audit.json`

The current build script is `build_motion2d_revised_core1_core2.py`; it also carries the source-question crop coordinates so the source crops can be regenerated when the original scan is available.
