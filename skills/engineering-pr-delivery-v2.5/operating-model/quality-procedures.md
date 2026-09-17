# Quality procedures and QRV evidence

## Purpose

Quality is an engineering procedure/evidence system, not a synonym for execution blocking. An Execution Package routes only the procedures relevant to the current slice; a `QRV-*` Quality Review records what those procedures actually established on the exact execution basis.

## Applicability routing

Every executable EP partitions the complete built-in blueprint library exactly once:

```text
quality.applicable[]
quality.not_applicable[]
```

An applicable entry requires a concrete reason and review focus. A not-applicable entry requires a concrete reason. Silent omission is invalid, but an inapplicable procedure is not run ceremonially.

The built-in library currently covers software design, coding, testing, code review, UI/UX, accessibility, performance, migration, engineering numerics, and GitHub delivery. Each blueprint defines when it applies, required inputs, procedure, checklist, anti-patterns, artifacts, verification, finding classification, true hard-stop conditions, Owner report, and successor handover.

## QRV-* Quality Review

Before checkpoint publication for executable work, applicable quality procedures are evidenced in a `QRV-*` object under `agents/relay/quality/`.

QRV is bound to:

- the exact EP contract digest;
- current roadmap revision;
- execution material ref;
- the exact quality-router snapshot.

Procedure results are:

```text
CLEAR
FINDINGS
NOT_RUN
```

`NOT_RUN` is evidence/quality truth. It can make quality `NEEDS_ATTENTION`, but it is not automatically an execution stop.

## Quality findings

Findings use stable `QF-*` IDs and preserve classification, severity, evidence, disposition, and successor transfer when unresolved.

Severity and blocker language are deliberately separate. A finding may set `blocks_execution: true` only when it maps to one of the existing hard-stop categories and carries durable basis proving that stop condition. Maintainability, design preference, incomplete optional evidence, or ordinary quality debt cannot manufacture material-write authority changes.

The quality plane remains:

```text
CLEAR
NEEDS_ATTENTION
OWNER_REVIEW_REQUIRED
```

The evidence plane separately records what ran or did not run, and the stop plane separately records genuine hard stops.

## Checkpoint and handover custody

A checkpoint references its QRV by id/path/digest. An executable successor cannot be published while the bound QRV contains a true blocking finding.

Deferred or unresolved findings transfer exactly through successor handover. They may be resolved only with durable resolution evidence; they cannot disappear because a new EP or agent takes custody.

Generated report, technical status, and Owner status project quality evidence downstream. They never override QRV, checkpoint, EP, or roadmap authority.

## Enforcement

Primary validators:

```text
validate_blueprints.py
validate_quality_router.py
validate_quality_review.py
validate_checkpoint_linkage.py
validate_relay_conformance.py
```

Repository-neutral stress tests prove complete routing, exact QRV coverage, `NOT_RUN` semantics, non-blocking high-severity findings, valid hard-stop mapping, and unresolved-finding transfer.

Historical implementation evidence remains in `wp-06-quality-procedures.md`; this file is the stable operating model.
