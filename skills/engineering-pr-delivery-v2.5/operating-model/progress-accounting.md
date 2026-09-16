# Progress accounting

Progress is calculated from durable acceptance, never guessed from elapsed effort or narrative confidence.

```text
Acceptance Criterion -> EP -> Work Package -> Phase -> Objective -> Overall Roadmap
```

When approved scope changes the denominator, create a new Progress Basis. Preserve completed work; do not rewrite history merely to keep the displayed percentage stable.

## Catch-up / completion basis

The V2.5 completion revamp defined in `catchup-completion-roadmap.md` uses a new explicit basis rather than inheriting a narrative percentage from the earlier control-plane build.

Suggested denominator weights are:

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

These numbers define the catch-up denominator only. Progress inside each WP must still be earned through weighted acceptance criteria and checkpoint evidence.

Future WPs may be fully defined without being executable. Serial execution means only the current frontier WP contributes active material execution. The initial revamp frontier is WP-00; WP-01 depends on WP-00 and WP-02 depends on WP-01.

A material Owner-approved change to this completion scope must create a new Progress Basis rather than silently editing the denominator.