# WP-04 — Full progress / handover / next-work contract

## Outcome

WP-04 makes progress and successor instructions source-derived rather than human-report mirrors.

```text
PROGRESS.yaml
  -> Objective
  -> Phase
  -> Work Package
  -> EP
  -> Implementation Step
  -> Acceptance Criterion

semantic EP.next_work.steps[]
  -> ordered action
  -> targets / inputs
  -> tests / benchmarks
  -> acceptance
  -> expected result
  -> stop/reconciliation conditions

source authority objects
  -> report_projection.py
  -> render_status.py / render_handover.py / render_report_projection.py
```

Generated output is projection only; it never becomes a competing source of truth.

## Delivered

- `PROGRESS.yaml` now carries `implementation_steps` and `acceptance_criteria` in addition to roadmap/EP buckets.
- `validate_progress.py` requires complete roadmap coverage and current ACTIVE EP/step/acceptance coverage.
- acceptance progress rows carry status and durable basis.
- `REPO_STATE.progress` values are compatibility mirrors; validator requires overall/phase/EP mirrors and basis revision to match authoritative progress.
- `progress_projection.py` derives the complete roadmap/task hierarchy.
- every semantic EP now requires structured `next_work.steps[]`.
- next-work validation checks ordered contiguous steps and current input/test/benchmark/acceptance IDs.
- `report_projection.py` creates a structured derived report with source digests for repository state, roadmap, progress, issue graph, EP and checkpoint.
- `validate_report_projection.py` is part of aggregate conformance.
- `render_report_projection.py` emits the derived report as YAML.
- status/handover renderers consume the derived projection rather than REPO_STATE percentage mirrors.
- handover renders Objective -> Phase -> WP -> Step -> AC with percentages/status/basis and exact ordered next work.
- parallel lane, join and replan custody detail remains visible.
- bootstrap now creates complete zero-weight roadmap progress rows without inventing executable work.
- parallel join reconciliation creates the integration EP progress/step/acceptance rows before cold start.
- `templates/REPORT.md` explicitly states that report prose is generated projection, not authority.

## Key invariants

```text
REPO_STATE phase/EP mirror != PROGRESS source
    -> conformance FAIL

roadmap/current EP object absent from PROGRESS
    -> conformance FAIL

ACTIVE EP missing structured next_work
    -> conformance FAIL

next_work references stale/unknown input/test/benchmark/AC
    -> conformance FAIL

generated report source object changes
    -> report digest/projection changes on regeneration
```

## Synthetic acceptance

`tests/stress/test_progress_handover.py` proves:

1. stale phase/EP mirrors fail while rendering remains source-derived;
2. missing roadmap progress rows fail;
3. handover exposes objective, phase, WP, step, AC and detailed next work;
4. stale next-work references fail;
5. next-work order must be contiguous;
6. report projection changes with source progress and cannot retain stale generated truth.

Existing bootstrap, parallel convergence and renderer fixtures were strengthened to exercise the new hierarchy while preserving custody semantics.

## Validation evidence

Pre-checkpoint aligned head:

```text
fabcb280167fbc1a8d95d120d4e88d242e1cd211
```

Workflow:

```text
35104423581
```

Result:

```text
compile                         PASS
root unit tests                 PASS
dedicated synthetic stress     PASS
```

The dedicated stress discovery currently executes 105 repository-neutral tests.

## Remaining ownership

WP-04 does not implement GitHub orchestration, procedural quality reviews, Owner-language translation, Owner change intake or release-level recursive relay certification. Those remain WP-05 onward.
