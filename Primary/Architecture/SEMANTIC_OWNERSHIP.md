# Primary semantic ownership

**Authority:** Common  
**Tracking:** Common #162

This document prevents the same educational concept from acquiring different meanings in Common, Study-Hub, and Kani.

## Ownership matrix

| Concern | Canonical owner | Other repositories may |
|---|---|---|
| LearningObject meaning | Common | reference IDs, render, map to curriculum |
| LearningCell meaning | Common | instantiate/use |
| TeachingTarget meaning | Common | serialize/route |
| LearningEpisode meaning | Common | instantiate and orchestrate specific episodes |
| ChildLearningProfile semantics | Common | persist/profile through authorized runtime |
| SkillState semantics | Common | display or persist derived state |
| CurrentLearningState semantics | Common | maintain session instance |
| Observation semantics | Common | emit/store observations |
| ResponseDiagnosis semantics | Common | run/reference Teacher Runtime |
| TeacherDecision / TeacherMove | Common | execute/render decisions |
| Conceptual support semantics | Common | record/apply support |
| Access-adjustment semantics | Common | record/apply adjustments |
| Representation role semantics | Common | emit observations |
| Longitudinal evidence dimensions | Common | persist/display derived state |
| Source-model boundary | Common | surface source-specific boundary |
| Curriculum mapping model | Common | consume mappings |
| `kani-content-v1` transport | Study-Hub | consume through locked adapter |
| `kani-catalog-v1` transport | Study-Hub | consume through locked adapter |
| `kani-activity-v1` transport | Study-Hub | emit/consume lifecycle messages |
| `kani-attempt-v1` transport | Study-Hub | emit/store validated attempts |
| ExperienceManifest instance serialization | Study-Hub | consume |
| QR / mission routing | Study-Hub | resolve/launch |
| Stable game learner identity | Kani | reference authorized ID |
| Immutable game attempts | Kani runtime | consume as evidence |
| Game mechanics/stars/streaks | Kani | display as game metrics only |
| Recent deterministic evidence summaries | Kani/shared implementation | consume as non-authoritative evidence summaries |
| Durable learning judgement | Common semantics / Primary Teacher Runtime | persist/display result |
| Next pedagogical action | Common semantics / Primary Teacher Runtime | execute/render |
| SQLite/Firebase provider profile | Study-Hub #39 / app infrastructure | must preserve semantics |

## Semantic vs transport contract

A semantic contract answers:

```text
What does this educational object mean?
What evidence may support it?
What inferences are forbidden?
```

A transport contract answers:

```text
How is a particular object serialized?
How is it versioned between applications?
How is identity bound at runtime?
```

Therefore:

```text
Common LearningEpisode semantics
        ↓ adapter
Study-Hub ExperienceManifest / KaniMission transport
        ↓
Kani renderer
```

Study-Hub may not change `INDEPENDENT_CHECK` to mean "game completed". Kani may not change `delayedRetention` to mean "high recent accuracy".

## Instance ownership

Canonical meaning and runtime instance ownership are different.

Example:

```text
Common owns:
  what LearningEpisode means

Study-Hub may own:
  EP-G4-FRAC-007 instance and renderer sequence

Kani may own:
  the immutable attempts produced during mission KM-FRAC-007
```

## Question/content rule

Do not introduce a second canonical question truth for Primary.

Existing Study-Hub `kani-content-v1` remains the app-facing question/content contract family. Common may define semantic metadata that a question references, such as learning object, question family, evidence goal, source boundary, and representation requirement.

## Backend rule

For identical canonical inputs:

```text
SQLite semantics = Firebase semantics = future-provider semantics
```

Storage or sync implementation may change latency/availability but not educational meaning.

## Change-control rule

A change belongs in Common when it changes the meaning of learning, teaching, learner state, support, evidence, diagnosis, source boundaries, or curriculum mapping.

A change belongs in Study-Hub when it changes cross-app serialization, publication/orchestration, QR routing, renderer sequencing, or version-lock mechanics without changing educational meaning.

A change belongs in Kani when it changes game execution, local learner runtime, mechanics, or observation capture without redefining educational meaning.