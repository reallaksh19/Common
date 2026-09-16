# Progress accounting

Progress is calculated from durable acceptance, never guessed from elapsed effort or narrative confidence.

```text
Acceptance Criterion
  -> Implementation Step
  -> EP
  -> Work Package
  -> Phase
  -> Objective
  -> Overall Roadmap
```

`PROGRESS.yaml` is the progress authority. It carries calculated buckets for objectives, phases, work packages, execution packages, implementation steps and acceptance criteria. Current acceptance rows also carry explicit status and durable basis.

`REPO_STATE.progress.overall_percent`, `phase_percent` and `ep_percent` are compatibility/location mirrors only. `validate_progress.py` requires them to agree with `PROGRESS.yaml`; generated status and handover output reads the source-derived projection rather than trusting those mirrors.

A roadmap/current-EP node missing from `PROGRESS.yaml` is invalid. This prevents a handover from silently omitting a work package, step or acceptance criterion.

Generated progress projection is produced by `scripts/progress_projection.py` and consumed by `report_projection.py`, `render_status.py` and `render_handover.py`.

When approved scope changes the denominator, create a new Progress Basis. Preserve completed work; do not rewrite history merely to keep the displayed percentage stable.

## Catch-up / completion basis

The V2.5 completion revamp defined in `catchup-completion-roadmap.md` uses an explicit 100-point denominator:

```text
WP-00 Kernel baseline / object matrix                 5
WP-01 Semantic Execution Package                    18
WP-02 Baton readiness + Takeover Certification      18
WP-03 Strong phase/boundary qualification           12
WP-04 Full progress / handover / next-work          12
WP-05 GitHub Program Projection operations           8
WP-06 Quality Procedure Library                     10
WP-07 Human Communication                            6
WP-08 Owner Change Intake                            3
WP-09 End-to-end Relay Certification Matrix          5
WP-10 Self-consistency Audit                         2
WP-11 PR Readiness                                    1
                                                    ---
                                                    100
```

These weights define the catch-up denominator only. Progress inside each WP remains acceptance/checkpoint-derived. A material Owner-approved scope change creates a new Progress Basis rather than silently editing the denominator.
