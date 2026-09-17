# WP-10 — Self-consistency Audit

## Status

CONTENT ACCEPTANCE COMPLETE — checkpoint verification pending.

## Basis

- predecessor: CP-R010 / merged PR #396
- merged basis: `fb28a0817cab109a1120e3826ce11439b49586de`
- completion before WP-10: 97%
- scope: repository-neutral V2.5 skill only

## Audit objective

Prove that V2.5 has one coherent control model across schemas, templates, validators, renderers, operator documentation, tests, and `SKILL.md` before final PR-readiness cleanup.

## Deterministic audit

Added `scripts/self_consistency_audit.py` and made it a mandatory scoped-CI step before unit/stress execution. It checks:

- YAML schema/template parseability;
- required durable-object shape/producer/consumer/documentation surfaces;
- complete procedural blueprint structure;
- aggregate-validator reachability;
- focused-validator and renderer operator documentation;
- current authority/readiness vocabulary;
- stable object-authority mapping through CP-R010;
- generic repository-neutral runtime logic;
- explicit CI execution of self-consistency, root units, and dedicated stress discovery.

The workflow push scope now covers the V2.5 branch family rather than only the original implementation branch.

## Findings and disposition

| ID | Finding | Disposition | Resolution |
| --- | --- | --- | --- |
| SC-01 | `object-authority-matrix.md` was frozen at the CP-R002 architecture and still described later delivered objects as future work. | FIXED | Rewritten through CP-R010 with current authority classes, producers, consumers, derived predicates, projection boundaries, QRV, Owner views, and `ZERO_CONTEXT_RECONSTRUCTION`. |
| SC-02 | `relay-conformance.md` still described WP-03 and later layers as future completion work. | FIXED | Reconciled aggregate conformance through CP-R010, including qualification, progress/report, GitHub operations, QRV, human communication, Owner change, and A→B→C release proof. |
| SC-03 | `SKILL.md` retained future-tense WP-07 wording and did not expose zero-context certification as an operator entrypoint. | FIXED | Replaced with the current operator contract and added zero-context reconstruction/validation plus self-consistency commands. |
| SC-04 | `scripts/README.md` omitted zero-context commands and `render_roadmap.py`. | FIXED | Added release reconstruction, roadmap renderer, self-consistency command, and current aggregate-conformance scope. |
| SC-05 | QRV had a historical WP-06 implementation report but no stable non-WP operating-model document. | FIXED | Added `operating-model/quality-procedures.md`; historical WP-06 report remains implementation evidence. |
| SC-06 | The first portability check encoded a concrete downstream stress-repository name inside Common, contradicting repository-agnostic design. | FIXED | Replaced with a generic check rejecting hard-coded GitHub repository URLs in Python protocol logic. |
| SC-07 | Internal helper libraries were incorrectly flagged as undocumented operator commands. | FIXED | Classified `relaylib.py`, `qualitylib.py`, `takeoverlib.py`, and projection/reconstruction helpers as internal libraries; operator scripts remain documentation-checked. |
| SC-08 | Scoped CI did not run a cross-surface consistency gate and its push trigger targeted only the original implementation branch. | FIXED | Added mandatory self-consistency step and V2.5 branch-family push trigger while preserving path scoping. |
| SC-09 | No blocking schema/template parse failure, aggregate-validator orphan, blueprint structure gap, duplicate authority claim, lifecycle/write-authority contradiction, or downstream-specific runtime route remained after correction. | DOCUMENTED_INTENTIONAL | Verified by deterministic audit + existing semantic/stress validators. |
| SC-10 | Historical WP implementation reports and completion checkpoints contain historical status language by design. | DOCUMENTED_INTENTIONAL | They remain evidence/history; current normative surfaces are `SKILL.md`, stable operating-model docs, validators, templates/schemas, and current completion state. |

No `BLOCKING` finding remains. WP-11 owns final PR/readiness presentation cleanup rather than protocol redesign.

## Red-to-green evidence

Initial executable audit head:

```text
head: 8c7cbc7d7b03688e59de89dd380e83639d965391
workflow: 35197070033
result: FAIL at self-consistency audit
errors: 16
warnings: 3
unit/stress: not executed after audit failure
```

The red run exposed the stale authority/conformance/operator documentation and audit false positives listed above.

Corrected implementation head:

```text
head: 3beae3849550fb0cd28abe658c63d1d770d9d3fa
workflow: 35197671662
compile: PASS
self-consistency audit: PASS — 0 warnings
root units: 7 PASS
synthetic stress tests: 135 PASS
```

The green audit is an executable release guard, not a one-time prose review.

## Authority conclusions

The post-audit control model has one bounded source for each concern:

```text
Owner intent             ODR
planning/topology        OVERALL_ROADMAP + roadmap revision
current work             EP / approved parallel plan
candidate evidence       DISC / QUAL / TC
live write admission     runtime MATERIAL_WRITE_READY
quality evidence         QRV
execution history        CP
calculated progress      PROGRESS
issue coordination       ISSUE_GRAPH
external desired state   GHGEN / GHOP
external observed state  GITHUB_OBSERVATION
human/report surfaces    derived projections only
repository reconstruction ZERO_CONTEXT_RECONSTRUCTION derived only
chat                     non-authority
```

No generated view, GitHub UI state, persisted WRITE enum, or conversational context competes with those sources.

## Exit criteria

- deterministic self-consistency audit: PASS;
- retired/stale normative vocabulary: resolved;
- aggregate/operator reachability: PASS;
- durable object producer/consumer ownership: reconciled;
- multiple-source authority conflict: none found after correction;
- repository-neutral runtime logic: PASS;
- compile + root units + dedicated stress suite: PASS on corrected implementation head;
- CP-R011 exact-head verification: still required before formal WP-10 closure.

## Successor

After CP-R011 exact-head verification, WP-11 — PR Readiness is the only successor. WP-11 may perform portability/presentation/final-evidence cleanup but must not reopen architecture without a newly discovered correctness defect.
