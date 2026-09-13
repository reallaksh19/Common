# Mathematics V2 — Adaptive Learning Blueprint

This layer is the canonical orchestration authority above the existing Core1/Core1A/Core2/Core2A production kits.

Its governing invariant is:

```text
EXECUTION ORDER MAY VARY.
AUTHORITY ORDER MAY NOT.
```

Core1 and Core2 reconstruct different kinds of intelligence from the original evidence. Either may execute first when the evidence justifies it. Neither becomes ground truth because it executed first.

## Implemented state

```text
Original evidence
      ↓
GroundTruthManifest
      ↓
MathLearningRunBlueprint
      ↓
GT_READY
      ↓
Adaptive Evidence Router
      ↓
CORE1_FIRST | CORE2_FIRST | BLOCK
      ↓
ROUTED / BLOCKED_*
```

Increment 1 established immutable evidence binding and the root run state. Increment 2 adds evidence-adaptive first-role routing, owner routing overrides, deterministic max-three handoff bundling and routing goldens.

## Ground truth

`GroundTruthManifest` records original question corpus, syllabus, authoritative source/textbook, answer key, solution set and figure set.

Evidence availability is explicit:

```text
PRESENT
ABSENT
PARTIAL
UNRESOLVED
CONFLICTED
```

`ABSENT` means evidence is absent. It cannot be translated into low importance, low difficulty, out-of-scope status, learner weakness or a claim that the topic is not assessed.

Only `ORIGINAL_EVIDENCE` and `AUTHORITATIVE_SOURCE` are legal ground-truth authority classes. Derived claims, benchmarks, agent conclusions and owner overrides remain outside ground truth.

## Root run blueprint

Every downstream artifact belongs to one `MathLearningRunBlueprint`. The run identity is assigned once and remains stable across state transitions; `run_digest` changes as state evolves.

The root binds exact ground-truth ref/digest, learner prior, learning purpose, product mode, owner override refs, routing, handoff bundles and later Core1/Core2/Join/Assimilation/Core1A/Core2A/publication refs.

The handoff transport constraint is:

```text
1 <= subtopics per bundle <= 3
```

This does not limit learning atoms, equations, inference edges, representations or teaching steps.

## Increment 2 — Adaptive Relay / EvidenceRouter

Routing consumes a `math-routing-build-spec` containing candidate subtopics and six evidence dimensions:

```text
SA  scope authority
SS  semantic source strength
QE  question evidence
QR  question resolution
UA  uncertainty
CI  conflict index
```

All dimensions use the governed 0–4 rubric in `policies/math-evidence-routing-policy.json`; every non-zero evidential strength must point back to GroundTruth evidence. Numbers are not free-form confidence scores.

Derived strengths are:

```text
semantic_strength   = max(SA, SS)
assessment_strength = min(QE, QR)
```

The deterministic routing rules are:

```text
material conflict
→ BLOCK_CONFLICT

semantic_strength <= 1 and assessment_strength <= 1
→ BLOCK_EVIDENCE

strong semantic authority
→ CORE1_FIRST

otherwise rich + resolved question evidence
→ CORE2_FIRST

otherwise
→ BLOCK_OWNER_REVIEW
```

If both Core1 and Core2 are evidence-admissible, normal system routing starts with Core1 because semantic authority is already strong; Core2 must still independently re-ground later. Missing/coarse semantic authority with rich resolved questions routes Core2 first.

A GroundTruth item marked `CONFLICTED` blocks ordinary routing when used by the subtopic profile. Conflict is preserved, not silently reconciled.

## Owner override semantics

Routing computes `system_action` first and never overwrites it.

A routing decision stores separately:

```text
SYSTEM ACTION
OWNER OVERRIDE
FINAL ACTION
```

`HARD` may change the operational first role even when the system recommended a block; the conflict/insufficiency remains recorded.

`SOFT` may choose only a role already present in `eligible_roles`. It cannot manufacture evidence admissibility.

Owner overrides never mutate GroundTruth.

## Handoff bundle synthesis

Routed subtopics are grouped by:

```text
final first role + coherence group
```

then ordered by declared subtopic sequence and chunked deterministically into bundles of at most three. Overflow creates another bundle; it never deletes or merges subtopics invisibly.

## Executable command

After initializing GroundTruth and a `GT_READY` run:

```bash
python 'Grade 9/V2/Mathematics/LearningBlueprint/engine/route_math_learning_run.py' \
  --ground-truth /tmp/ground_truth_manifest.json \
  --run /tmp/math_learning_run.json \
  --routing-spec /tmp/routing_spec.json \
  --out-plan /tmp/routing_plan.json \
  --out-run /tmp/math_learning_run_routed.json
```

Optional owner routing control is supplied with `--override-ledger`.

## Routing goldens

Three goldens prove the architecture's central routing behavior:

1. strong detailed syllabus/source + rich questions → `CORE1_FIRST`;
2. absent/coarse syllabus + rich resolved questions → `CORE2_FIRST`;
3. sparse/conflicted evidence → `BLOCK_CONFLICT` rather than forced consensus.

The goldens validate routing behavior, not topic-specific mathematics.

## Files

```text
contracts/math-ground-truth-build-spec.schema.json
contracts/math-ground-truth-manifest.schema.json
contracts/math-learning-run-blueprint.schema.json
contracts/math-routing-build-spec.schema.json
contracts/math-routing-plan.schema.json
contracts/math-owner-override-ledger.schema.json

policies/math-evidence-state-policy.json
policies/math-evidence-routing-policy.json

engine/blueprint_common.py
engine/build_ground_truth_manifest.py
engine/init_math_learning_run.py
engine/route_math_learning_run.py

golden/routing/01-core1-first.json
golden/routing/02-core2-first.json
golden/routing/03-block-conflict.json

tests/test_blueprint_foundation.py
tests/test_adaptive_router.py
```

## Completion boundary

Increment 2 decides only **which intelligence role should run first** and creates safe handoff bundles. It does not yet claim that Core1/Core2 independent re-grounding is solved.

## Next increment

Increment 3 implements the dual-intelligence runtime and independence firewall:

```text
routed bundle
      ↓
fresh first-role Core instance
      ↓
first package sealed
      ↓
fresh second-role instance
      ↓
PASS A: original ground truth only
      ↓
independent findings sealed
      ↓
PASS B: expose first-role package
      ↓
claim-level validation
CONFIRMED / REFINED / MISSING / UNSUPPORTED /
CONTRADICTED / OUT_OF_SCOPE / UNKNOWN
```

The runtime must prove the second role completed its ground-truth-only pass before it could see the first role's claims. Fresh instance IDs alone are not sufficient evidence of independence.
