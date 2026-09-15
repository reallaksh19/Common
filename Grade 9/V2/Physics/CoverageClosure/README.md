# Physics V2 — P-J Coverage closure, evidence feedback and longitudinal update

P-J implements issue #258 under the #320 catch-up. It answers two separate questions and
keeps them separate:

1. **Is the publication complete?** Every assessment item and every eligible external
   candidate is either covered or carries an explicit disposition.
2. **What has the learner actually demonstrated?** Transfer evidence updates the
   longitudinal record without ever letting one current success close a future obligation.

```text
P-A question set + P-B item validity registry     (assessment denominator and exclusions)
+ P-G Core1 plan  (lessons + Appendix A practice)
+ P-H representation bundle (+ PhysicalPageMap)
+ P-I Core2 transfer plan + external classification
+ P-J transfer-evidence policy (+ optional evidence ledger)
→ SourceCoverageMatrix + ExternalCorpusCoverageMatrix
→ LongitudinalUpdate + LearnerStateUpdate
→ PublicationCoverageClosure
```

## Closure is fail-closed

`closure_state` is `CLOSED` only when there are **zero** gaps. Anything uncovered opens it:

| gap | falsifier if closure is claimed anyway |
|---|---|
| assessment item with no lesson, no practice item and no review exclusion | `SOURCE_ITEM_UNCOVERED_BUT_CLOSURE_CLAIMED` |
| eligible external candidate with no Core2 page | `EXTERNAL_CANDIDATE_UNCOVERED_BUT_CLOSURE_CLAIMED` |
| required capability with no representation | `CAPABILITY_WITHOUT_REPRESENTATION_COVERAGE` |
| no PhysicalPageMap, or a figure that drew nothing | `CLOSURE_CLAIMED_WITHOUT_PHYSICAL_REALIZATION` |

Closure requires **physical** realization, not a plan: the policy sets
`closure_requires_physical_realization`, and the closure binds the P-H page map and the
exact PDF SHA-256 it was computed from.

## One current success does not close a future obligation

This is the P-F invariant carried into feedback. Each of the nine longitudinal dimensions
declares, as data, the event classes that could close it plus a minimum success count,
minimum distinct instances and minimum delay:

```text
near_transfer        2 successes, 2 distinct instances, 0 days
far_transfer         2 successes, 2 distinct instances, 7 days
delayed_retention    2 successes, 2 distinct instances, 14 days
fluency / timed      3 successes, 3 distinct instances, 0 days
```

Dimensions listed in `never_closable_by_single_current_success` can never close on one
event regardless of the counts. On the current fixture a correct Core2 attempt leaves
`near_transfer` at `OPEN_WITH_PARTIAL_EVIDENCE` with
`blocked_reason: SINGLE_CURRENT_SUCCESS_MAY_NOT_CLOSE_THIS_DIMENSION`, and
`delayed_retention` stays `OPEN`. Forging either to `CLOSED` fails
`ONE_CURRENT_SUCCESS_CLOSES_DELAYED_RETRIEVAL` / `ONE_CURRENT_SUCCESS_CLOSES_FUTURE_EVIDENCE`.

## Evidence never shrinks assessment scope

Every capability in the P-F study scope appears in the learner-state update with
`remains_in_assessment_scope: true`. A capability with an incorrect transfer attempt is
marked `EVIDENCE_OF_DIFFICULTY` and **stays in scope**; removing one fails
`TRANSFER_EVIDENCE_SHRINKS_ASSESSMENT_SCOPE`.

## Evidence custody

Events are digest-bound and each carries a `source_trace_refs` list and an `instance_ref`.
The ledger declares `production_claim: false` — it is synthetic test evidence, not real
learner data, and claiming otherwise fails `SYNTHETIC_EVIDENCE_CLAIMED_AS_PRODUCTION`.

## Running

```bash
python "Grade 9/V2/Physics/CoverageClosure/contracts/validate_contracts.py"
python "Grade 9/V2/Physics/CoverageClosure/tests/test_physics_coverage_closure.py"
```

## Non-claims

A `CLOSED` coverage state means the publication accounts for every item; it is **not** a
quality, correctness or learning-effectiveness claim. Subject, pedagogy and assessment
expert review remain `PENDING` and are tracked at P-L.
