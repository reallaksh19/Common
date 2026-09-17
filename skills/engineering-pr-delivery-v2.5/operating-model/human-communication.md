# Human communication

V2.5 exposes two generated human views over one derived communication projection:

```text
repository authority objects
  -> report_projection.py
  -> communication_projection.py
      -> TECHNICAL_STATUS.md
      -> OWNER_STATUS.md
```

Neither generated view is authority. Both are disposable projections and must be regenerated from current repository truth.

## Technical status

`TECHNICAL_STATUS.md` preserves protocol precision for engineering operators. It includes lifecycle, roadmap position, calculated progress, execution/material authority, evidence state, quality/QRV state, active stop, protected/prohibited scope, Owner decisions, ordered next work, readiness, and source-basis identifiers needed for diagnosis.

## Owner status

`OWNER_STATUS.md` translates the same source projection into plain language. It must answer:

- what can happen now;
- what the current work is intended to achieve;
- what will not change without authority;
- what evidence exists and what evidence is missing;
- what material quality risks or limitations remain;
- what changed in roadmap/progress at the last checkpoint;
- whether an Owner decision is genuinely required now;
- what happens next;
- what currently stops progress, if anything.

The Owner view must not invent urgency. A choice reserved to the Owner is not the same as an Owner decision required now. `OWNER_DECISION_REQUIRED` is shown only when current repository truth actually requires an Owner decision to proceed.

## Truth-preservation rules

The Owner view must never hide or soften away:

- active hard stops;
- `NOT_RUN` or otherwise missing evidence;
- unresolved/deferred quality findings;
- protected, prohibited, and deliberate non-goal scope;
- known limitations/problems;
- roadmap/progress reconciliation;
- exact ordered next work.

Quality severity alone does not become a hard stop in communication. A non-blocking quality risk remains visible as a risk, while execution-stop language is reserved for the STOP plane / valid hard-stop mapping.

## Plain-language boundary

The Owner view should avoid relay-internal object jargon where ordinary language carries the same meaning. It may name stable identifiers when they materially help traceability, but it must not require the Owner to understand internal terms such as EP, QRV, GHOP, or QSET in order to know capability, risk, evidence, decisions, and next work.

The technical view is intentionally allowed to retain protocol terms and object identifiers.

## Validation

`validate_human_communication.py` checks projection convergence and verifies that the Owner view cannot omit current stop/evidence/quality/scope/decision/next-work truth. Aggregate relay conformance invokes it.

Repository-neutral stress tests cover shared-source derivation, hard-stop visibility, missing evidence, non-blocking quality risk, Owner-reserved versus Owner-required decisions, next-work mutation, and internal-jargon rejection in Owner-facing source text.
