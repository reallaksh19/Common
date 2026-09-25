# SCHEMA EXECUTION HANDSHAKE

PROTOCOL REVISION:
TPG-2P-2026-09-25-R1

GENERATOR MODE:
TWO_PASS_ONLY

SCHEMA FETCH STATUS:
LIVE_THIS_RUN

SCHEMA CONTENT SHA:
sha256-example

HANDSHAKE STATUS:
PASS

# SCHEMA BASIS

Canonical current-main two-pass schema fetched for this run.

## PASS 1 — INDEPENDENT SYSTEM BASELINE

You have inherited the Example application. Nobody has told you which ticket they want changed.

Inspect the live repository/application and explain how it actually works today from the user's point of view. Trace one important path from its source of truth through transformations to the result a user or downstream consumer sees. Work one representative real case end-to-end, vary one load-bearing condition to expose what should change and what must remain invariant, and verify the important conclusion by a genuinely independent route.

Return an INDEPENDENT_SYSTEM_BASELINE covering system/user outcome, current behaviour, the authority flow, the concrete witness, invariants/failure behaviour, independent verification, exact material/runtime basis, what is known, and what remains uncertain. End at understanding; do not recommend changes or choose future work.

## PASS 2 — IMPROVE, RECONCILE, PLAN

Use the actual Pass-1 baseline, then inspect the current assigned issue and live repository/provider state.

First step back and identify zero or more evidence-supported high-ROI improvements. Prefer no proposal to a speculative proposal and do not propose a rewrite merely because a cleaner architecture is imaginable. For each candidate, show an IMPROVEMENT PROPOSAL with observed gap, evidence, current→proposed state, quantitative before/after effect where measurable (UNKNOWN otherwise), estimated change size, impact/evidence/reuse/effort/risk scores, confidence, relative ROI, falsifier, and SCOPE RELATION.

Then reconcile the actual issue against live reality. State whether its responsibility should be preserved, amended, split, superseded, or is already satisfied. Keep adjacent improvements out of the issue unless separately approved as their own responsibility.

Show me a DRAFT IMPLEMENTATION_PLAN in chat with basis, understanding, issue disposition, proposals, owned outcome, STEP-* slices, surfaces, dependencies, falsifier, validation, preserved invariants, uncertainty, expected next observable, and consumer/handoff.

Finish your first response with APPROVAL REQUIRED. Do not publish a durable plan, create/bind EPs, or materially implement from this proposal response.

After I explicitly approve, refresh live reality. If the approval basis materially changed, show the delta and stop. Otherwise publish the approved IMPLEMENTATION_PLAN on the original issue including only approved Improvement Proposals, reuse/create EPs by bounded responsibility, refresh Task Snapshot/Handover for coordinator consumption, and execute only within the actions I approved.
