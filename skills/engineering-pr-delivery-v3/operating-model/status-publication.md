# Event / change-budget status publication

Engineering Relay V3 does not require a time-based heartbeat.

Status publication is child/task-local and is driven by **semantic change** or **material change debt**.

## Policy

Repository-specific policy lives at:

```
relay/CONFIG/status-publication.yaml
```

If that file is absent, the evaluator uses the skill default for preview/evaluation. `relay.can` only enforces publication when the repository-specific policy exists and is enabled.

The default policy combines:

- hard semantic triggers;
- fallback material-volume thresholds;
- a weighted status-debt threshold.

Default volume triggers are 300 changed material lines, 5 touched material files, 3 created material files, or 3 commits since the previous publication cursor.

Generated/vendor/build/lock-file paths are excluded by policy.

## Child-local cursor

Publication baseline is coordination metadata stored per EP:

```
relay/PUBLICATION/<EP-ID>.status.yaml
```

Sibling agents never share a cursor.

The cursor records the last published material/task projection, not accepted engineering truth.

## Evaluate

```bash
python skills/engineering-pr-delivery-v3/scripts/status_publication.py <repo-root>
```

A due result exits non-zero and explains the exact triggers and score.

Optional explicit semantic signals:

```yaml
schema_version: relay-v3-status-publication-signals
public_contract_changed: true
roadmap_reconciliation_requested: false
```

Use:

```bash
python .../status_publication.py <repo-root> --signals signals.yaml
```

## Record after publishing

After actually publishing the child status to the Owner/handover surface:

```bash
python .../status_publication.py <repo-root> --apply \
  --note "Published parent/task checklist and current pending items."
```

This advances only that EP's publication cursor.

## Before lifecycle actions

Policies may require a fresh publication before checkpoint, handover, PR-ready, or task exit.

Evaluate/record with the matching action:

```bash
python .../status_publication.py <repo-root> --action CHECKPOINT
python .../status_publication.py <repo-root> --action CHECKPOINT --apply --note "Pre-checkpoint status published."
```

The preparation is bound to the current HEAD. A later material commit requires a new pre-action publication.

## MATERIAL_WRITE enforcement

If `relay/CONFIG/status-publication.yaml` exists and is enabled, `relay.can(MATERIAL_WRITE)` checks the child-local publication debt.

When due it denies with:

```
STATUS_PUBLICATION_DUE
```

This creates a deterministic publication boundary without a clock.

## UI

Open:

```
skills/engineering-pr-delivery-v3/ui/status-publication-policy.html
```

The page edits thresholds, weights, hard triggers and exclusions, provides a live score simulator, and exports repository YAML.

The page is only a policy editor. The checked-in repository YAML remains the policy source of truth.
