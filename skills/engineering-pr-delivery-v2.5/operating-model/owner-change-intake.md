# Owner Change Intake

## Purpose

A material Owner change must be legible before and after application without creating a second authority source. The Owner Decision Record (ODR) remains intent authority; the roadmap revision remains structural-change authority; generated change reports are projections only.

## Authority chain

```text
Owner message / durable Owner source
    ↓
ODR-* decision + change_intake semantic summary
    ↓
OWNER_INTENT_MUTATION roadmap revision
    ↓
roadmap / progress / issue / active-EP reconciliation
    ↓
owner_change_projection.py
    ↓
OWNER_CHANGE.md
```

`OWNER_CHANGE.md` never overrides either ODR or roadmap transaction state.

## ODR change_intake

For an Owner intent mutation that needs an Owner-facing change report, the ODR records:

```yaml
change_intake:
  previous_concept: "..."
  requested_concept: "..."
  retained_behavior:
    - "..."
  invalidated_behavior:
    - "..."
  new_scope:
    - "..."
```

This is semantic Owner-intent context. It does not replace `affected`, `required_reconciliation`, or the roadmap revision's actual topology/progress/frontier effects.

## Applied change requirements

When the current roadmap revision is `OWNER_INTENT_MUTATION`:

1. The revision references exactly one APPLIED `ODR-*` with `decision.kind: INTENT_MUTATION`.
2. The ODR contains a concrete `change_intake`.
3. The revision classifies active work explicitly as changed, removed, unaffected, or invalidated.
4. `progress_basis_change.new_basis` equals the current authoritative Progress Basis.
5. `frontier_after` equals the frontier computed from the resulting roadmap.
6. Issue impact is visible; if affected issues are named, `issue_graph_reconciled` must be true.
7. The generated projection states whether the decision is merely captured or has actually been applied to the current roadmap.

## Current-EP disposition

The change report derives one of:

```text
NO_ACTIVE_EP
PENDING_OWNER_CHANGE
INVALIDATED
RECONCILE_REQUIRED
CONTINUE_UNCHANGED
```

`UNCLASSIFIED` is diagnostic-only and fails validation for a current applied Owner mutation. Silence is never evidence that the active EP survived an Owner change.

## Owner-facing report

`render_owner_change.py` reports:

- previous concept;
- requested/new concept;
- retained behavior;
- invalidated behavior;
- new scope;
- roadmap revision effects;
- Progress Basis and denominator effects;
- issue impact and reconciliation state;
- current EP disposition;
- resulting frontier;
- required reconciliation;
- applied/not-applied status.

The report intentionally uses plain language and ends by stating that it is derived, not authoritative.

## Pending decisions

A CAPTURED ODR may be rendered directly with `--odr`. In that case the semantic requested change is visible, but `new_frontier` is not invented and the report states that the decision is not yet applied. Material repository truth changes only through an APPLIED ODR plus a valid roadmap transaction.

## Commands

```bash
python scripts/validate_owner_change_intake.py <repo-root>
python scripts/owner_change_projection.py <repo-root> [--odr agents/relay/roadmap/owner-decisions/ODR-xxxx.yaml]
python scripts/render_owner_change.py <repo-root> [--odr ...] [--output agents/relay/generated/OWNER_CHANGE.md]
```

`validate_owner_change_intake.py` is part of aggregate relay conformance.
