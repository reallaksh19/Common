# Newton's Laws of Motion - Revised Core 1 and Core 2

This topic is the third completed pair in the topic-by-topic Physics learner-product rebuild.

## Revised Core 1

- 25 pages.
- 11 competency families.
- Teaching contract: choose body/system -> interaction/state representation -> governing law -> complete execution -> physical check.
- Every competency includes a concept-native figure, worked example, guided try, faded try, watch-out/anti-trigger, quick check, and explicit answer.
- Key families: motion vs force; body selection; FBD/net force; Newton II scaling; stopping-force chains; signed momentum; impulse; Newton III; system-boundary conservation; recoil/rocket exchange; v-t slope to friction force.

## Revised Core 2

- 42 pages.
- 20 source-demand-aligned challenges corresponding to the 20 direct Unit 9 demands in the existing NLM source reconciliation ledger.
- Q10 is retained as an ambiguity-aware item rather than silently inventing a rolling mechanism for the source's smooth-floor wording.
- Each attempt uses an exact problem representation, H1/H2/H3 paired prompt/reveal hints, and exactly two work lines.
- H1 asks for decisive physics, H2 asks for the representation, H3 asks for the first executable constraint only.
- Every solution uses the complete UNDERSTAND -> REPRESENT -> CONNECT -> CALCULATE -> INTERPRET ladder, followed by explicit answer, quick check, alternate check, watch-out and Core 1 review link.

## Representation requirements

Core 2 problem figures are state-specific rather than generic. Examples include:

- rightward speed increase represented with velocity and acceleration arrows rather than unrelated force magnitudes;
- frictionless constant-velocity puck with vertical N and mg and no invented horizontal force;
- braking vehicle figures distinguished from accelerating-train figures;
- mass-ranking and force/mass-scaling figures separated;
- ball-only momentum-conservation test shown with gravity crossing the system boundary;
- horse/cart balance shown with the actual 500 N forward force and unknown backward resistance.

## Layout / typography

- DejaVu Sans family used for consistent Greek/superscript/subscript support.
- Dynamic title sizing prevents long NLM headings from clipping.
- Figures are constrained to their semantic panes.
- Content-height reasoning rows; no fixed empty solution boxes.
- Core 2 attempt workspace is exactly two writing lines.

## QA

See `physics-nlm-revised-core1-core2-audit.json`.

Final automated scan:
- zero out-of-bounds text blocks in Core 1 and Core 2;
- zero severe overlap flags in Core 1 and Core 2;
- zero hint-pair validation failures;
- 20/20 direct Unit 9 demands represented in Core 2;
- both PDFs re-rendered after the final figure/hint/layout corrections.

Expected workbench artifacts:

- `physics-nlm-revised-core1.pdf`
- `physics-nlm-revised-core2.pdf`
- `physics-nlm-revised-core1-core2-audit.json`
- `build_nlm_revised_core1_core2.py`
- `NLM_REVISED_README.md`
- `nlm-revised-topic-handoff-2026-09-12.zip`
