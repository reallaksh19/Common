# Mathematics V2 — Adaptive Learning Blueprint

This layer is the canonical orchestration authority above the existing Core1/Core1A/Core2/Core2A production kits.

It exists to enforce one governing distinction:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.
```

Core1 and Core2 are independent interpretations of original evidence. Either may execute first depending on the evidence available. Neither becomes ground truth merely because it executed first.

## Increment 1 — blueprint foundation

The first implemented increment freezes only the root contracts required before adaptive routing is added:

```text
Original evidence
      ↓
GroundTruthManifest
      ↓
MathLearningRunBlueprint
      ↓
GT_READY
```

The foundation deliberately does **not** choose Core1-first or Core2-first yet. Routing belongs to Increment 2 and must be based on evidence strength rather than hard-coded stage order.

## Original evidence is authority

`GroundTruthManifest` records the original evidence available to the run:

- question corpus;
- syllabus;
- authoritative source/textbook;
- answer key;
- solution set;
- figure set.

Evidence availability is explicit:

```text
PRESENT
ABSENT
PARTIAL
UNRESOLVED
CONFLICTED
```

`ABSENT` means evidence is absent. It must never be converted into claims such as low importance, low difficulty, out-of-scope, or learner weakness.

Only these authority classes are legal inside the ground-truth manifest:

```text
ORIGINAL_EVIDENCE
AUTHORITATIVE_SOURCE
```

Derived claims, external benchmarks, model conclusions and owner overrides do not become ground truth.

## Root run blueprint

Every downstream packet must belong to one `MathLearningRunBlueprint`.

The run blueprint binds:

- exact ground-truth manifest reference and digest;
- learner prior and learning purpose, when known;
- owner override references without mutating evidence;
- run state;
- handoff bundles;
- downstream packet references;
- final publication/audit references.

The run state machine is fixed at the root level:

```text
GT_READY
ROUTED
FIRST_CORE_COMPLETE
SECOND_CORE_COMPLETE
CROSS_VALIDATED
JOIN_READY
ASSIMILATION_COMPILED
CORE1A_REALIZED
EXPOSURE_RECORDED
CORE2A_ELIGIBLE
CORE2A_REALIZED
FINAL_AUDIT_PASS

BLOCKED_EVIDENCE
BLOCKED_CONFLICT
BLOCKED_PREREQUISITE
BLOCKED_REPRESENTATION
BLOCKED_EXPOSURE
BLOCKED_OWNER_REVIEW
```

Increment 1 may initialize only `GT_READY`. Later increments will own legal transitions.

## Handoff bundles

The root schema already encodes the transport constraint:

```text
1 <= subtopics per bundle <= 3
```

This is a relay-size constraint only. It does not constrain the number of learning atoms, equations, representations, misconceptions, inference edges or teaching steps inside a subtopic.

## Files

```text
contracts/math-ground-truth-build-spec.schema.json
contracts/math-ground-truth-manifest.schema.json
contracts/math-learning-run-blueprint.schema.json
policies/math-evidence-state-policy.json
engine/blueprint_common.py
engine/build_ground_truth_manifest.py
engine/init_math_learning_run.py
tests/test_blueprint_foundation.py
```

## Next increment

Increment 2 adds the adaptive Relay/EvidenceRouter:

```text
GroundTruthManifest
      ↓
subtopic evidence profile
      ↓
HandoffBundle <= 3
      ↓
CORE1_FIRST | CORE2_FIRST | BLOCK
```

No first-role decision is legal until that evidence router exists and passes its golden fixtures.
