# WP-07 — Human Communication implementation report

## Outcome

WP-07 separates technical and Owner-facing communication without creating another source of truth.

```text
repository authority objects
  -> report_projection.py
  -> communication_projection.py
      -> render_technical_status.py
      -> render_owner_status.py
```

`TECHNICAL_STATUS.md` and `OWNER_STATUS.md` are disposable generated projections. They never override roadmap, EP/plan, checkpoint, progress, quality, issue, state-plane, or Owner-decision authority.

## Delivered behavior

- `report_projection.py` now carries current contract purpose/scope, Owner-decision summaries, known problems/non-goals, checkpoint limitations/remaining work, QRV state and roadmap reconciliation with source digests.
- `communication_projection.py` derives one shared communication object from the report projection.
- `render_technical_status.py` preserves protocol precision and source-basis identifiers for engineering operators.
- `render_owner_status.py` translates the same truth into plain language: current capability, purpose, protected/non-change scope, evidence gaps, quality risks/limitations, roadmap progress/reconciliation, genuine Owner decisions, next work and active stops.
- `validate_human_communication.py` is part of aggregate relay conformance and verifies that Owner communication cannot hide hard stops, missing evidence, unresolved quality risk, protected scope, genuine decisions, or exact next work.
- The Owner view distinguishes an Owner-reserved domain from an Owner decision actually required now.
- A non-blocking quality concern remains visible as a risk and is not promoted into fake execution-stop language.
- Owner-facing source text is checked for internal relay jargon where ordinary language is required.
- `operating-model/human-communication.md` and the scripts README document the generated-view contract.

## Repository-neutral regressions

`tests/stress/test_human_communication.py` covers:

1. Owner and technical views derive from one report projection.
2. A current `OWNER_DECISION_REQUIRED` stop is visible in plain language.
3. Missing/NOT_RUN evidence cannot be hidden.
4. A non-blocking quality finding is visible without becoming a fake stop.
5. Owner-reserved scope does not fabricate a decision request.
6. Next-work source mutation is reflected in Owner communication.
7. Internal relay jargon in Owner-facing source text is rejected.

## Failure found during implementation

The first documentation-aligned run exposed a renderer-only `TypeError`: `_text()` compared a list value against a set containing a list literal. The source/communication invariants were not weakened; `_text()` was corrected to handle scalar/list values safely and the full suite was rerun.

## Validation evidence

Repaired implementation head:

```text
0b5c38f008d670ab9db24cf7b3fe4fccba07893b
workflow 35166010334 — PASS
```

Documentation-aligned pre-checkpoint head:

```text
49d0e52ee81e34ddf4152927456a4f4e4bdef665
workflow 35176089341 — PASS
```

The aligned run passed compile, 7 root unit tests and the dedicated 125-test repository-neutral synthetic stress surface.

## Deliberately not performed

- Owner change-intake transaction UX/payload; owned by WP-08.
- Full Agent A -> B -> C zero-chat release certification; owned by WP-09.
- Whole-surface schema/template/validator/renderer/docs consistency audit; owned by WP-10.
- Ready-for-review transition or merge; owned by WP-11/Owner authority.
- Downstream repository adoption or modification.
- Any change to engineering-pr-delivery-v2.
