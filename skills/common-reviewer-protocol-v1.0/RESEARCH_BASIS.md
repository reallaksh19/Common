# Common Reviewer Protocol v1.0 — research basis

This note records the external engineering-review sources used to design the generic Common review floor. The protocol text is adapted as a project-neutral synthesis; these sources remain external references rather than runtime dependencies.

## Google Engineering Practices — code review

Sources:

- https://google.github.io/eng-practices/review/
- https://google.github.io/eng-practices/review/reviewer/looking-for.html
- https://google.github.io/eng-practices/review/reviewer/standard.html
- https://google.github.io/eng-practices/review/reviewer/navigate.html
- https://google.github.io/eng-practices/review/developer/small-cls.html

General principles adapted into Common:

- review overall design/system fit before local polish;
- verify intended functionality and think about edge cases, users, concurrency and failure behavior;
- reject avoidable complexity/over-engineering;
- review tests themselves, including whether assertions are meaningful and tests would fail when behavior is broken;
- review naming, comments, style and durable documentation;
- inspect enough whole-file/system context to understand the change;
- cover every assigned human-written changed region unless review scope explicitly says otherwise;
- surface major design defects early;
- split changes that are too large to reason about effectively;
- judge technical facts and code-health impact rather than personal preference;
- aim for improving code health, not impossible perfection.

## OWASP — secure code review

Sources:

- https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
- https://owasp.org/projects/code-review-guide

General principles adapted into Common:

- understand architecture/business requirements before security-sensitive review;
- identify changed components, trust boundaries and critical assets;
- trace sources → transformations → sinks for material data flows;
- inspect input validation, authentication, authorization, sensitive-data handling, error handling, logging, configuration, dependency and integration risk where applicable;
- examine business-logic/state-transition/race/resource-limit failures that automation may miss;
- treat automated security tooling as evidence, not a replacement for contextual human reasoning.

The Common protocol intentionally marks security/privacy criteria applicability-based: not every code change crosses a material trust boundary, but omission is not allowed to masquerade as `NOT_APPLICABLE` without a basis.

## GitHub pull-request review guidance

Sources:

- https://docs.github.com/en/pull-requests/concepts/giving-reviews
- https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests
- https://docs.github.com/en/pull-requests/how-tos/review-pull-requests

General principles adapted into Common:

- reconstruct change purpose/context before reviewing files;
- preserve reviewer-visible testing/context in the PR/task surface;
- inspect changed files and relevant automated checks;
- review dependency/security impact when applicable;
- standardize the information authors provide so later reviewers/successors can reconstruct the change.

## Design consequence for standalone agents

Most conventional code-review guidance assumes a reviewer other than the author. A standalone engineering agent cannot truthfully reproduce that principal independence by merely changing personas.

Therefore Common v1.0 uses:

```text
SELF_REVIEW
PRINCIPAL_INDEPENDENCE: NONE
```

as a minimum quality gate, while preserving distinct Reviewer/Super-Reviewer requirements when the governing Local/project acceptance profile requires them.
