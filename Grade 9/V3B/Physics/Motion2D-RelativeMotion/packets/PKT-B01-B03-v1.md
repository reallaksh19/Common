# PKT-B01-B03-v1 — frames, path/displacement, components

**Buckets:** B01–B03. **Receiver:** Core/self-study maintainer. **State:** reviewable self-review packet; cold independent restart NOT_RUN.

Immutable dependencies: `source-corpus.md` source `SYN-M2D-20260915-V1` SHA-256 `6aac1841445e051244c3ad41f2d1ccab0d21e486b92efd0da68a87298bb29648`; `source-inventory.json` 159 atoms; `coverage.csv`; `equation-register.json`; V3B PR #364 `6be71db1a321c449131a26ee3084b6b9c0edca28`. Historical vector/shared-clock provenance is bounded as recorded in `../qa/live-authority-reconciliation.md`.

## Source/data obligations

Relevant frozen questions include Q01 (6 m east then 8 m north in 14 s), Q02 (`t,x,y`: 0,0,0; 2,6,8; 4,12,16; 6,12,16), and Q03 (start (2,5), constant velocity (3,-4) m/s for 6 s). Q04/Q06/Q10 supply sign/observer examples that depend on B01/B03 conventions. Never paraphrase frozen Core2 blocks when claiming source fidelity.

## Equation/semantic obligations

Use final-minus-initial signed components; displacement magnitude from a right triangle/Pythagoras; average velocity is displacement/time and average speed is distance/time. Every vector statement declares frame/axes/sign. One common time coordinate is required when two component equations describe the same event. No trig or `atan2` is assumed.

## Representations

Canonical assets: `frames-axes-clock.svg`, `path-displacement.svg`, `component-triangle.svg`, `time-labelled-path.svg`. Verify labels, arrow direction, units, and equation/figure agreement after edits.

## Core realization expectation

Core1 = concise map/check; Core1A = worked declarative teaching; Core1B = attempt-first reconstruction; Core2 = frozen source/hints/solutions; Core2A = supported application; Core2B = transfer/model choice. Preserve intrinsic badges B01 Easy, B02 Medium, B03 Hard; support must not be used to relabel intrinsic demand.

**Exact next action after receipt:** read B01–B03 atoms in inventory/coverage, open the four SVGs and linked Core anchors, then rerun source-fidelity/coverage checks before accepting any edit. Missing dependency => stop rather than infer.
