# Local PR Delivery v1.1 — Common Reviewer Protocol integration

Local v1.1 uses `skills/common-reviewer-protocol-v1.0/` as the reusable generic engineering-review floor.

The Coordinator-created project review / acceptance protocol remains the authority for project-specific correctness and specialist acceptance.

```text
COMMON REVIEWER PROTOCOL v1.0
+
PINNED PROJECT REVIEW / ACCEPTANCE PROTOCOL
+
REPOSITORY REQUIRED CHECKS
=
EFFECTIVE REVIEW PROFILE
```

## Coordinator bootstrap requirement

Before the first Production Responsibility is released, Coordinator bootstrap must pin:

- exact Common Reviewer Protocol ref + digest;
- exact project review / acceptance protocol ref + digest;
- Reviewer-required project method IDs;
- Super-Reviewer-required project method IDs;
- specialist / external / release methods where applicable;
- criterion applicability and any authority-bearing waivers.

The Common floor does not permit a Coordinator to postpone project review design until after the implementation candidate is visible.

## Reviewer role

Reviewer executes:

```text
Common CR-01..CR-10 applicable Reviewer floor
+
reviewer_check_required project methods
```

Coder self-review evidence may be consumed as context but is not inherited Reviewer approval.

## Coordinator / Super Reviewer role

Super Review executes:

```text
Common CR-01..CR-10 applicable Super-Review floor
+
super_review_required project methods
+
independent project harness/oracle/integration gates
```

Reviewer evidence cannot be renamed into Super-Reviewer evidence.

## Independence

Local role/principal truth remains explicit. When Owner authorizes same-principal role collapse, the fresh role attempt still records the lack of distinct-principal independence and must execute the role's required methods anew. A context reset is not principal independence.

## Finding / repair behavior

Use the Common taxonomy:

```text
BLOCKING_DEFECT
BOUNDED_PRODUCT_FIX
MATERIAL_SCOPE_CHANGE
ACCEPTANCE_SURFACE_DEFECT
EXTERNAL_DEPENDENCY
ADVISORY
```

Only bounded product fixes remain inside the role repair envelope. Material scope change becomes governed split/continuation. Acceptance-surface defects require proposal/adoption/new acceptance epoch where affected. Required external dependencies remain truthful NOT_RUN/BLOCKED.

## Version evolution

Every active Local role pins the Common Reviewer Protocol ref/digest through its effective review profile. A newer Common Reviewer Protocol must trigger a revision/integration notice; no active responsibility silently migrates.
