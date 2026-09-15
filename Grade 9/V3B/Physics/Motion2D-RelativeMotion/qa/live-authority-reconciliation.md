# Live authority reconciliation — 2026-09-15

**Review mode:** same-instance repository reconciliation; not independent subject review.

## V3B authority

The V3B Physics execution contract remains PR #364 at `6be71db1a321c449131a26ee3084b6b9c0edca28`, with `CoreContracts.json` blob `dee9520c7dee3fa7da97b9276768fa323bec9268` (contract 1.1.0), `Engineering/CORE_CONTRACTS.md` `291d42c8999205c6c08660525f262fde0e5d34c1`, `Engineering/PACKET_CONTRACT.md` `e84c6e23bf2bba01426f2b5a95c9fa99084b7519`, and `Engineering/TOPIC_WORKFLOW.md` `b968c118cad27ca8e11b9ffe4608a00c539a98b9`.

## Physics PR #350 transition

The package was originally reconciled while PR #350 exposed a v3 Engineering Workbench. Historical provenance used these exact gate blobs: shared clock `af715733f1a28b52395f871a5ab5d78c136d3e2a`, vector components `aaf4c667056a44915a5a0a71d34a19f8a7ee37c5`, and vector add/sub `fa504ad7e9bc5c46c10ee0aad833489606bf9ea5`. Only their bounded invariants were adopted: declared frame/axes/signs, common event time, component subtraction, observer reversal, and Pythagorean reconstruction; trigonometric component resolution/atan2/projectile scope remained excluded.

On the final publication recheck, PR #350 had advanced to `2c4ece2833a8a6686607b5d038efe29674c5c6b6`. Its current `Grade 9/Physics/Motion` tree (`6ebb147be622dd7fd5f596215a2774916d4b6c50`) contains a straight-line Motion concept-book specification/source map and no longer contains the historical v3 gate registry. The current spec supports signed displacement, common timelines, graph/equation reasoning, and limited one-dimensional/common-acceleration relative-motion ideas, but it is not a replacement authority for this V3B two-dimensional relative-motion package.

## Compatibility conclusion

No learner Core is changed by this authority transition. The V3B contract remains the controlling six-Core architecture; the historical PR #350 gate SHAs are retained as provenance for the bounded vector/shared-clock semantics already embodied in the package. PR #350 current head is recorded as a live comparison authority with a different straight-line scope, not silently treated as an unchanged gate-bearing head.

No Mathematics or Chemistry path was modified. No owner approval, merge, release, or independent-review claim is implied by this reconciliation.
