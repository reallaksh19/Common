# Engineering Relay V3.2 — Common Reviewer integration

## Normative status

This is a normative V3.2 addendum for review design and standalone completion.

V3.2 uses the reusable Common Reviewer Protocol at:

```text
skills/common-reviewer-protocol-v1.0/
```

The Common protocol is the generic review floor. A Coordinator-created project review / acceptance protocol remains separately required for project-specific correctness, integration, performance, UX/accessibility, domain, hardware, numerical, browser, release, security or other specialized acceptance.

## Effective review basis

For every governed responsibility:

```text
COMMON_REVIEWER_PROTOCOL
+
PROJECT_REVIEW_PROTOCOL
+
REPOSITORY_REQUIRED_CHECKS
=
EFFECTIVE_REVIEW_PROFILE
```

Pin exact refs/digests for the Common and project protocols in durable review evidence.

A project protocol may strengthen/specialize the Common floor. It may not silently remove an applicable Common criterion. Inapplicability or waiver must be explicit and evidence/authority-bearing under `common-reviewer-protocol-v1.0`.

## Standalone activation

When V3.2 is invoked without Local PR Delivery:

```text
existing responsibility?
  YES -> resume its pinned review basis/stage
  NO  -> classify topology

R = 1 -> STANDALONE_SINGLE_RESPONSIBILITY_BOOTSTRAP
R >= 2 -> STANDALONE_PROGRAMME_COORDINATOR_BOOTSTRAP
```

Before material implementation, the bootstrap must establish:

- the responsibility/programme decomposition required by `PROGRAMME_DECOMPOSITION_PROGRESS.md`;
- a project review / acceptance protocol appropriate to the task;
- the Common Reviewer Protocol exact ref/digest;
- project review method IDs and specialist requirements;
- semantic implementation denominator;
- whether distinct-principal review is required by risk/project/Owner/repository policy.

For programme topology, no Coder responsibility is released until the Decomposition Quality Gate is `RELEASEABLE` and the project review basis is pinned.

## Mandatory minimum standalone self-review

A standalone agent MUST NOT move directly from implementation to `TASK_RESULT RESPONSIBILITY_COMPLETE=YES`.

At candidate boundary it must execute:

```text
TASK_EVIDENCE — SELF_REVIEW_START
        ↓
fresh review attempt over actual candidate
        ↓
Common CR-01..CR-10 applicability/results
        +
Coordinator-created project review methods
        ↓
findings frozen/classified
        ↓
bounded fixes if permitted
        ↓
affected review/verification replay on final candidate
        ↓
TASK_EVIDENCE — SELF_REVIEW_END
        ↓
completion decision
```

Required standalone evidence fields:

```text
REVIEW_MODE: SELF_REVIEW
PRINCIPAL_INDEPENDENCE: NONE
CONTEXT_RESET: FRESH_REVIEW_ATTEMPT
COMMON_REVIEW_PROTOCOL_REF + DIGEST
PROJECT_REVIEW_PROTOCOL_REF + DIGEST
COMMON_CRITERIA_RESULTS
PROJECT_METHOD_RESULTS
REVIEW_SCOPE / EXCLUSIONS
FINDINGS / DISPOSITIONS
FINAL_CANDIDATE
UNRESOLVED_REQUIRED_FINDINGS
```

The implementing agent must reconstruct from durable task/plan/protocol and actual files rather than certify from implementation memory.

`FRESH_REVIEW_ATTEMPT` is a context-discipline claim, not independence. Same-principal self-review MUST NOT satisfy a distinct Reviewer/Super-Reviewer requirement.

## Distinct review requirement

Set `DISTINCT_REVIEW_REQUIRED=true` when required by any applicable:

- Owner instruction;
- repository policy / CODEOWNERS / required review rule;
- Local lifecycle;
- project acceptance profile;
- material security/privacy/concurrency/safety/specialist risk classification;
- release/merge governance.

When true, standalone self-review is pre-review evidence only. It may improve the candidate but cannot authorize the distinct-review gate.

## Review findings and repair bounds

Use the Common finding taxonomy:

```text
BLOCKING_DEFECT
BOUNDED_PRODUCT_FIX
MATERIAL_SCOPE_CHANGE
ACCEPTANCE_SURFACE_DEFECT
EXTERNAL_DEPENDENCY
ADVISORY
```

Ordinary bounded fixes may occur inside self-review and must be reverified. Material scope growth invokes the responsibility split/continuation rules; an acceptance-surface defect invokes governed acceptance revision; an unavailable required external dependency remains truthful `NOT_RUN`/blocked.

## Progress relationship

Self-review does not manufacture Coder `P`.

If the Coordinator's delivery denominator includes review units, valid completed review methods may advance delivery/evidence progress only according to the declared denominator in `PROGRAMME_DECOMPOSITION_PROGRESS.md`.

Do not derive progress from number of review comments, findings, files inspected, tests executed or elapsed review time.

## Completion gate

`TASK_RESULT RESPONSIBILITY_COMPLETE=YES` in standalone mode requires all of:

```text
implementation semantic units complete
required Common review criteria complete on final candidate
required project review methods complete on final candidate
no unresolved BLOCKING_DEFECT / REQUIRED finding
required unavailable checks remain blocking rather than fabricated PASS
review independence stated truthfully
```

If distinct review is required but unavailable:

```text
RESPONSIBILITY_COMPLETE: NO
NEXT: DISTINCT_REVIEW_REQUIRED
```

## Local compatibility

When V3.2 evidence is nested under a Local lifecycle, the Common Reviewer Protocol may still be used as the generic quality floor, but Local owns role transition and distinct Reviewer/Super Reviewer semantics. V3.2 must not convert Coder self-review into Local Reviewer completion.

## Revision notice

The active task pins its Common Reviewer Protocol version/ref/digest.

A discovered newer Common Reviewer Protocol does not silently migrate active evidence. Surface a revision notice with integration impact, including whether:

```text
NEW_TASKS_RECOMMENDED
PROJECT_PROFILE_REVIEW_REQUIRED
LOCAL_ADAPTER_REVISION_REQUIRED
RELAY_ADAPTER_REVISION_REQUIRED
```

and keep active responsibility pins unchanged unless the governing authority explicitly migrates them.
