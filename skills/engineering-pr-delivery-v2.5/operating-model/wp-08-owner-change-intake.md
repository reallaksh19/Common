# WP-08 — Owner Change Intake implementation report

## Outcome

WP-08 adds an Owner-facing change-intake/report layer without introducing a competing authority source.

Authority remains:

```text
Owner source
  -> ODR-* intent authority
  -> OWNER_INTENT_MUTATION roadmap revision
  -> roadmap / progress / issue / active-EP reconciliation
  -> derived Owner change projection
  -> OWNER_CHANGE.md
```

## Delivered behavior

- `ODR.change_intake` records plain-language previous concept, requested concept, retained behavior, invalidated behavior and new scope for material Owner intent mutations.
- `owner_change_projection.py` combines that semantic intent with the linked roadmap revision, authoritative Progress Basis, issue graph, current execution state and computed frontier.
- `render_owner_change.py` produces a plain Owner-facing report with previous/new concept, retained/invalidated behavior, new scope, roadmap impact, progress-basis effect, issue impact, current-EP disposition, new frontier, required reconciliation and applied/not-applied state.
- `validate_owner_change_intake.py` is part of aggregate relay conformance.
- A CAPTURED ODR can be rendered without claiming the change has been applied.
- A current applied Owner mutation requires exact ODR/revision linkage, current Progress Basis, exact computed frontier, visible issue reconciliation and explicit active-work disposition.
- Generated `OWNER_CHANGE.md` is projection only; it cannot mutate or override the ODR or roadmap transaction.

## Active-EP disposition

Derived dispositions are:

```text
NO_ACTIVE_EP
PENDING_OWNER_CHANGE
INVALIDATED
RECONCILE_REQUIRED
CONTINUE_UNCHANGED
```

`UNCLASSIFIED` is diagnostic only and fails validation for a current applied Owner mutation.

## Artifacts

- `templates/ODR.yaml`
- `schemas/owner-change-projection.schema.yaml`
- `scripts/owner_change_projection.py`
- `scripts/render_owner_change.py`
- `scripts/validate_owner_change_intake.py`
- `operating-model/owner-change-intake.md`
- `tests/stress/test_owner_change_intake.py`
- aggregate wiring in `scripts/validate_relay_conformance.py`
- operator commands in `scripts/README.md`

## Repository-neutral regression matrix

The focused synthetic suite proves:

1. applied Owner changes project both semantic intent and structural effects;
2. a current Owner mutation without `change_intake` fails;
3. affected issues cannot be reported reconciled unless the revision says they were reconciled;
4. active work cannot silently survive a material Owner mutation without explicit disposition;
5. Progress Basis and frontier remain source-bound to the resulting roadmap transaction;
6. a CAPTURED decision is visible but cannot be presented as applied.

## Validation evidence

Documentation-aligned implementation head:

```text
fb5e0b15f25884793e38ba694505b748acaf84fd
workflow 35188301698 — PASS
```

The run passed compile, 7 root unit tests and 131 repository-neutral synthetic stress tests.

## Deliberately not done

- No new mutable Owner-change authority object.
- No downstream repository adoption or project-specific change model.
- No changes to V2.
- No WP-09 end-to-end zero-chat certification implementation.
- No WP-10 global self-consistency audit.
- No ready-for-review transition or merge.
