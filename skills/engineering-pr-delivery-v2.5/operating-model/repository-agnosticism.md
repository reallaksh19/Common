# Repository-agnostic core

V2.5 is reusable engineering-relay infrastructure. Downstream repositories are consumers and stress targets, not sources of hard-coded behavior.

## Rules

1. Common skill code, schemas, templates and validators must not depend on a downstream repository name, issue number, branch, file path, product name, engineering domain or formula.
2. Project-specific facts belong in that repository's `REPO_PROFILE.yaml`, `OVERALL_ROADMAP.yaml`, EPs, inputs, benchmarks and Owner Decision Records.
3. A real repository may be inspected to validate the protocol, but validation must be read-only unless the Owner separately authorizes migration/adoption in that repository.
4. If a real repository reveals a protocol defect, express the fix as a generic invariant or validator and add a synthetic regression fixture reproducing the condition.
5. Do not add `if repo == ...`, repository-specific allowlists, issue-specific exceptions or path-specific behavior to Common.
6. Stress fixtures use synthetic names and generic engineering/software conditions.
7. Repository adapters, if ever required, must be declarative project data, never hidden special cases in Common code.
8. A protocol change is acceptable only if it remains meaningful when all downstream names are replaced with arbitrary repositories and work domains.

## Validation use

Real projects should be treated as black-box stress environments for: large roadmaps, long histories, infrastructure `NOT_RUN`, owner concept changes, supersession, phase transitions, numerical authority, UI quality, and unexpected agent loss. Findings become generic tests; project data does not become protocol code.
