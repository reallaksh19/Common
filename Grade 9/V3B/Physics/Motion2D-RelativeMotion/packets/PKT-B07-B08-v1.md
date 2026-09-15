# PKT-B07-B08-v1 — meeting, collision and frame-transfer applications

**Buckets:** B07–B08. **State:** reviewable self-review packet; cold independent restart NOT_RUN.

Immutable dependencies: frozen corpus `SYN-M2D-20260915-V1` SHA-256 `6aac1841445e051244c3ad41f2d1ccab0d21e486b92efd0da68a87298bb29648`; source inventory/coverage/equation register; V3B PR #364 `6be71db1a321c449131a26ee3084b6b9c0edca28`. Current PR #350 is a separate straight-line Motion workstream; see `../qa/live-authority-reconciliation.md`.

## Source/data obligations

Q07: x-coordinate equality occurs at 5 s while y equality occurs at 0 s, so there is no meeting. Q08: paths cross at (6,0), but A arrives at 3 s and B at 2 s; no collision. Closest-approach enrichment has `d²=8(t-2.5)²+2`, so minimum separation is `sqrt(2)` at 2.5 s. Q09: boat/water (0,3) m/s plus water/ground (4,0) m/s gives ground (4,3), speed 5; 60 m crossing takes 20 s, drift 80 m, path 100 m. Q10: rain relative to observer (-8,-6) m/s, magnitude 10 m/s. Q12 lacks direction information; retain the underdetermination hold and conditional examples rather than inventing one answer.

## Model obligations

Meeting means same x and y at the same time; path intersection alone is insufficient. Boat/current and rain/observer use explicit frame chains and vector addition/subtraction. Closest approach is enrichment only and must use table/algebra/completing-square reasoning, not calculus. Keep Grade-9 no-trig/no-calculus boundary.

## Representations

Canonical assets: `collision-pair.svg`, `boat-current.svg`, `rain-observer.svg`, `time-labelled-path.svg`, `relative-subtraction.svg`. Check event-time labels, observer/frame names and component directions.

Core2A positive meeting control: t=4 s at (8,4). Core2B positive meeting control: t=3 s at (3,6). Preserve the 2A/2B exact 6-entry/4-standard/2-stretch distributions and Core2B 8 fresh-transfer/4 registered-revisit split.

**Next action:** read B07–B08 atom/coverage rows, Q07–Q12 frozen blocks and visual assets; rerun source-fidelity, arithmetic/model and transfer checks before accepting changes. Q12 hold is mandatory.
