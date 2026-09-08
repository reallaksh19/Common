# Interval and Successive-Pattern QA

Use this checkpoint set whenever a student-facing batch contains nth-second questions, cumulative-to-interval subtraction, repeated equal-time intervals, or shortcut ratios such as 1:3:5:7.

## AD-36 INTERVAL-BOUNDARY INTEGRITY

Every interval phrase must resolve to explicit start and end times before a shortcut is applied.

Examples:

- `during the nth second` -> `(n-1) to n`;
- `during the 5th second` -> `4 to 5 s`;
- `between 3 s and 5 s` -> `S(5)-S(3)`;
- `during the next t seconds` after the first `t` seconds -> `S(2t)-S(t)`;
- a custom interval `2.5 to 4.0 s` -> `S(4.0)-S(2.5)`.

Fail if a student page silently replaces an interval with a cumulative total, for example using `S(5)` as the displacement during the fifth second.

For full-support and guided pages, make the interval boundary visible on a timeline or directly in the equation. For independent transfer, preserve intentional no-diagram instructions while giving task-specific workspace only.

## AD-37 SHORTCUT-DOMAIN INTEGRITY

A shortcut must never visually appear more universal than its source conditions.

For the nth-second shortcut

`sn = u + (a/2)(2n-1)`

verify:

- one constant-acceleration interval;
- the interval width is exactly one second;
- the result is displacement, not automatically total distance across a reversal.

For the pure odd-number pattern `1:3:5:7...`, verify all three conditions are stated or visually recoverable:

1. starts from rest (`u=0`);
2. constant acceleration;
3. successive equal-duration time blocks.

Fail if `constant acceleration` alone is shown as sufficient for `1:3:5:7`.

## AD-38 CUMULATIVE-vs-INTERVAL LINKAGE

Whenever a page teaches an interval shortcut or successive-distance pattern, preserve the parent cumulative model that justifies it.

Examples:

- `interval displacement = S(end)-S(start)` must remain the general helper;
- `sn = S(n)-S(n-1)` must appear before or alongside the compact nth-second formula in derivation/support pages;
- square cumulative totals `1,4,9,16` must be visibly connected to first differences `1,3,5,7`;
- equal-width intervals larger than 1 s must be justified from `S(kΔt) ∝ k²`, not by blindly relabelling one-second formulas.

Fail if the publication teaches the ratio/pattern as a disconnected mnemonic while omitting the cumulative displacement structure already present in the source.

## AD-39 ORDINAL / INDEX TYPOGRAPHY

Time-interval labels and indexed equations must be readable and semantically unambiguous.

- render `1st`, `2nd`, `3rd`, `4th` correctly rather than source-layout artifacts such as `1th`, `2th`, `3th`;
- render `sn`, `s(n+2)`, etc. with proper subscripts in student-facing equations where the font system supports them;
- avoid label collisions under narrow proportional bars; abbreviate the ordinal label (`1st`, `2nd`, etc.) rather than shrinking to unreadable type;
- keep the raw source token and any presentation normalization in the audit model.

This is a presentation normalization, not permission to change the mathematical relation.

## Required review sequence

1. Mark every interval start/end in the source obligation ledger.
2. Render each timeline/interval diagram and verify the highlighted span.
3. Compare every shortcut against its model conditions.
4. Check that cumulative and interval representations are explicitly linked.
5. Inspect ordinal/index labels at normal viewing size for collision or ambiguity.
6. Record `interval_boundary_findings = 0`, `shortcut_domain_findings = 0`, and `cumulative_interval_link_findings = 0` before release.
