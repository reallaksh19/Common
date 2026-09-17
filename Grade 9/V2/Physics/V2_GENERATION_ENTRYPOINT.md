# Physics V2 — generation entrypoint (cold start)

Read this file and `GENERATION_AUTHORITY_MANIFEST.json` for P-A…P-K generation. For P-L mature-release work, also read `ExactProduct/RELEASE_AUTHORITY_MANIFEST.json`. Together these repository artifacts are sufficient: **no chat history, no issue history and no manually pre-computed intermediate is required or permitted.** If an implementation needs one, the repository architecture is incomplete and must remain blocked.

## P-K generation command

```bash
python "Grade 9/V2/Physics/ColdStart/engine/physics_cold_start_runner.py" \
  --out-dir /tmp/physics-v2-cold-start
```

The runner executes the same assessment twice, once without an `AttemptSet` and once with learner-attempt evidence. Each run emits exactly two learner PDFs:

```text
physics-core-study-guide.pdf
physics-transfer-solution-book.pdf
```

plus the run report and governed intermediate artifacts. `<out>/comparison.json` verifies the two-run invariants.

Validate a run independently with:

```bash
python "Grade 9/V2/Physics/ColdStart/engine/physics_cold_start_validator.py" \
  --report /tmp/physics-v2-cold-start/with-attempts/run_report.json
```

## Authority chain

| phase | directory | produces / authorizes |
|---|---|---|
| P-A | `AssessmentIntake` | QuestionSet, DeclaredTopicScope, AttemptSet (optional) |
| P-B | `AssessmentReview` | source/item validity and diagnostic-use review |
| P-C | `AssessmentScope` | exact assessment scope, capability/prerequisite closure |
| P-C.5 | `ColdStart` + `Shared/EngineeringGate` | Engineering Readiness for the exact P-C scope; `PROBLEM_SEMANTICS` permission |
| P-D | `ProblemSemantics` | problem families, reasoning routes, verification routes, consuming the exact gated P-C bundle |
| P-E | `LearnerEvidence` | LearnerStateSnapshot |
| P-F | `StudySynthesis` | LearnerStudyScope + LearnerStudyModel + longitudinal init |
| P-G | `CoreAuthoring` | promoted PCK + Core1 study plan + Appendices A/B/C |
| P-H | `Representation` | teaching-primitives, representation bundle, PhysicalPageMap |
| P-I | `Core2Transfer` | transfer pages, H1/H2/H3 hint ladder, First-Step Reference |
| P-J | `CoverageClosure` | coverage matrices, longitudinal update, publication closure |
| P-K | `ColdStart` | code-generated two-product learner package |
| P-L | `ExactProduct` | exact-byte quality gates, governed human-review intake, final comparator guard and mature-release decision |

### P-C.5 is mandatory authority, not a Blueprint exception

Cold start derives P-C from the repository inputs, then submits that exact `scope_model_digest` and the governed Physics capability-to-Engineering binding registry to `Grade 9/V2/Shared/EngineeringGate`. Only after the global envelope allows the manifest-declared `PROBLEM_SEMANTICS` consumer may P-D execute.

```text
P-C exact scope
  ↓
governed capability → authority routes
  ↓
subject technical closure + provider-owned external prerequisites
  ↓
Shared Engineering Gate readiness envelope
  ↓ require PROBLEM_SEMANTICS
P-D consumes that exact P-C bundle
```

No topic name, case ID, prior fixture or model memory may substitute for a binding. If a future capability is routed to a real Engineering gate, the same runtime automatically applies recursive technical closure and cross-domain receipt enforcement. If authority is absent, consumption is held rather than inferred.

A scope may legitimately have `technical_gate_requirement_state = NOT_REQUIRED_FOR_THIS_SCOPE` only when every required capability has an explicit governed authority route and none maps to a dedicated active technical gate. That state is still evaluated and receipted by the global Engineering Gate; it is not a bypass.

## Two products, never three

```text
CORE_STUDY_GUIDE          main teaching + Appendix A practice + Appendix B solutions
                          + Appendix C printable handout
TRANSFER_SOLUTION_BOOK    transfer questions + hint ladders + full solutions
```

Appendix C is a section of the Core Study Guide. A separate third PDF is a topology failure.

## Two-run invariant

The assessment determines what must be teachable; learner evidence may change only order, depth, bridge, treatment and support. The question set, declared scope, scope authority, **P-C scope digest, Engineering binding-registry digest, Engineering readiness digest/status/gate-requirement state**, external corpus, problem semantics, study scope, required capability/item sets, problem-family truth, physical-model truth, law truth, external eligibility and two-product topology must remain identical across the two runs.

The study model, Core1 plan and lesson-mode distribution may differ because those are evidence-adaptive. Engineering readiness may not differ because it is upstream of learner evidence.

## P-L governed release

P-K readiness is not mature-product approval. The real P-L path is:

```text
exact two PDFs
  ↓
machine publication engineering
  ↓
AI pre-review — advisory only
  ↓
exact two-PDF HumanReview binding
  ↓
Shared V2 HumanReview REAL_RELEASE projection
  SUBJECT / PEDAGOGY / ASSESSMENT / VISUAL
  ↓
all four authorized human gates PASS
  ↓
final reference-comparison eligibility
  ↓
frozen PR #156 comparison
  ↓
governed mature-release decision
```

`ExactProduct/RELEASE_AUTHORITY_MANIFEST.json` is the cold-start authority map for this P-L path. `ExactProduct/engine/evaluate_physics_governed_release.py` is the canonical real-release authority. The older `evaluate_physics_exact_product.py` remains the machine/state-projection primitive and synthetic state-machine test surface; arbitrary inline attestations from that helper are not real release authority.

## Boundaries

- PR #156 is never a P-A…P-K producer input. The reference eligibility guard is required to return **before reading any comparator bytes** until governed real human review is complete.
- `Publication/` and `LearningDesign/` are legacy pre-assessment-gate layers and must not be wired into this P-A…P-L chain.
- A manually supplied Engineering Readiness result is forbidden. P-C.5 must be recomputed from exact current P-C authority and governed Engineering bindings on every cold start.
- Human review cannot be generated by repository code. The four real reviewer authorization lists are currently empty, and there are no real review submissions.
- TEST_ONLY reviewer identities and submissions are falsifier fixtures only and can never become release evidence.
- Learning effectiveness remains independent of rendering/product polish.

## Current honest state

The repository can regenerate and validate the two learner PDFs from repository inputs alone. The cold-start production path now structurally invokes Engineering Readiness before Problem Semantics and persists exact readiness custody in each run report.

Machine publication engineering passes. The architecture for real human intake and the final comparator boundary is present and CI-enforced, but the real product remains:

```text
SUBJECT_CORRECTNESS       PENDING
PEDAGOGICAL_DESIGN        PENDING
ASSESSMENT_DESIGN         PENDING
VISUAL_USABILITY          PENDING
REFERENCE_COMPARABILITY   NOT_RUN
MATURE_DESIGN_QUALITY     PENDING
release                   BLOCKED_PENDING_AUTHORIZED_REVIEW_OR_EXACT_ARTIFACT
```

This is an external-evidence block, not missing machine architecture: authorized humans must be explicitly registered and submit reviews bound to the exact PDF hashes before the comparator can legally run.
