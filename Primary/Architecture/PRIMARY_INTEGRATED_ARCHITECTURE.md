# Primary Grades 4–5 Integrated Educational Architecture

**Status:** v1 architecture candidate  
**Canonical authority:** `reallaksh19/Common`  
**Tracking:** Common #162  
**Programme roadmap:** Study-Hub #40  
**Backend/provider roadmap:** Study-Hub #39

## 1. Purpose

This architecture defines the educational semantics shared by Grade 4–5 Math and English learning experiences across Study-Hub, print/PDF, Kani Game App, and future renderers.

The conceptual centre is not a publishing pipeline. It is the teacher/learner loop:

```text
CHILD ACTION
    ↓
OBSERVE
    ↓
INTERPRET / DIAGNOSE
    ↓
DECIDE
    ↓
TEACHER MOVE
    ↓
CHILD ACTION
    ↓
NEW EVIDENCE
    ↺
```

Core 1/Core 2 research and publication architecture remains useful implementation infrastructure, but Primary learning decisions are governed by the runtime above.

## 2. Canonical ownership boundary

```text
COMMON
  defines educational meaning
        ↓
STUDY-HUB
  instantiates / orchestrates / publishes
        ↓
KANI
  renders game experiences / records observations
```

Common owns the semantics of:

- `LearningObject` and prerequisite relationships;
- `TeachingTarget`;
- `LearningCell` relationship to learner-facing `LearningEpisode`;
- `ChildLearningProfile`, `SkillState`, and `CurrentLearningState`;
- `Observation`, `ResponseDiagnosis`, `TeacherDecision`, and `TeacherMove`;
- conceptual support vs access/load adjustments;
- representation evidence roles;
- multidimensional longitudinal learning evidence;
- source-model boundary and ambiguity states;
- Grade 4–5 Math/English pedagogical rules;
- curriculum mapping semantics and future stretch/competition seams.

Study-Hub owns app-facing orchestration and transport. Kani owns game runtime, stable learner identity, immutable attempts, and deterministic recent-evidence summaries.

Neither Study-Hub nor Kani may redefine durable learning judgement or pedagogical next action.

## 3. Six-plane Primary model

### 3.1 Knowledge plane

Defines what may be learned.

Typical objects:

```text
LearningObject
PrerequisiteEdge
LearningCell
Representation
Strategy
Misconception
QuestionFamily
Text / LanguageFeature
```

Math and English extend this plane differently. They do not share a forced ontology.

### 3.2 Expectation plane

Defines what an external programme expects without cloning canonical knowledge.

```text
CurriculumProfile
GradeScope
SchoolScope
SourceScope
AssessmentDemandProfile
```

IB PYP, NCF-SE/NCERT, school textbooks, and later competition profiles are overlays over canonical learning objects.

### 3.3 Child plane

Stores long-lived, evidence-backed information about the learner.

```text
ChildLearningProfile
SkillState
LearningHistory
StablePreferenceEvidence
```

A single session must not silently create a durable child trait.

### 3.4 Session plane

Stores temporary context for the present encounter.

```text
CurrentLearningState
TeachingTarget
EffortLoadProfile
LearningEpisode
```

Hesitation, repeated questions, recent errors, rushing, fatigue reports, or a successful streak belong here first unless repeated evidence justifies promotion.

### 3.5 Teaching plane

Represents teacher reasoning and action.

```text
Observation
    ↓
ResponseDiagnosis
    ↓
TeacherDecision
    ↓
TeacherMove
```

A diagnosis is a hypothesis with confidence and evidence, not a permanent label.

### 3.6 Experience and evidence plane

Represents what the child actually encounters and what observable evidence results.

```text
Study-Hub / Print / Kani / Oral / other renderer
              ↓
Attempt / response / representation use
              ↓
Observable evidence
              ↓
Teacher Runtime interpretation
```

## 4. Evidence is not judgement

Freeze this dependency:

```text
RAW OBSERVATION / ATTEMPT
        ↓
RECENT DETERMINISTIC EVIDENCE SUMMARY
        ↓
PRIMARY TEACHER RUNTIME
        ↓
LEARNING JUDGEMENT
        ↓
TEACHER DECISION / NEXT ACTION
```

A renderer may state what happened. It may not silently infer durable mastery.

Examples of observations:

```text
correct / incorrect
partial credit
response time
hints used
self-corrected
response mode
representation used
representation role
access adjustment used
conceptual support used
```

Examples of Teacher Runtime interpretation:

```text
possible misconception
possible prerequisite gap
possible language bottleneck
possible performance lapse
support dependency
ready for independent retry
schedule delayed retrieval
```

## 5. Learning evidence is multidimensional

`ACQUIRE → INDEPENDENT → RETAIN → TRANSFER → optional STRETCH` is a teaching progression, not one exclusive learner-state enum.

Preferred learner evidence shape:

```yaml
learning_evidence:
  acquisition: SECURE
  independent_use: SECURE
  delayed_retention: NOT_YET_TESTED
  transfer: DEVELOPING
  stretch: NOT_YET_TESTED
```

Evidence in one dimension must not imply evidence in another.

Immediate game accuracy can contribute to acquisition or independent-use evidence only when the task conditions support that interpretation. It cannot by itself establish delayed retention or transfer.

## 6. Support has two independent dimensions

### 6.1 Conceptual support

Support that changes the intellectual assistance provided to solve the target learning problem.

Examples:

```text
PROMPT
HINT
MODEL
THINK_ALOUD
WORKED_EXAMPLE
```

### 6.2 Access/load adjustments

Changes that reduce incidental burden without supplying the target concept.

Examples:

```text
REDUCED_LANGUAGE
ONE_STEP_AT_A_TIME
ORAL_RESPONSE_ALLOWED
REDUCED_WRITING
READ_ALOUD
EXTRA_VISUAL_SPACING
```

A learner who succeeds after a reading-load adjustment has not necessarily required a mathematical hint.

## 7. Representation evidence includes role

Where observable, represent at least:

```text
PROVIDED
CHILD_SELECTED
CHILD_PRODUCED
```

Being shown a number line is weaker independence evidence than selecting or constructing the number line unaided.

## 8. LearningCell vs LearningEpisode

A `LearningCell` is reusable pedagogical knowledge.

A `LearningEpisode` is one learner-facing encounter shaped by target, learner evidence, current state, and teacher decisions.

```text
LearningCell
 + TeachingTarget
 + SkillState
 + CurrentLearningState
        ↓
TeacherDecision
        ↓
LearningEpisode
```

An episode may contain teaching, guided practice, representation shifts, independent checks, reflection, transfer, and delayed retrieval obligations.

The semantic definition of `LearningEpisode` belongs to Common. Study-Hub may instantiate and serialize a particular episode into an ExperienceManifest.

## 9. Teacher Runtime invariants

### 9.1 Same-route failure

```text
IF the same target has produced two unsuccessful attempts
AND the teaching route has remained substantially the same
THEN the next teacher move must vary a meaningful dimension.
```

Meaningful variation may include representation, language complexity, concrete context, task size, response mode, problem structure, or prerequisite probe.

The runtime must not simply repeat a longer version of the same explanation.

### 9.2 Child action between teaching chunks

In tutor mode, substantial teaching should be followed by an observable child action unless the user explicitly requests reference material rather than tutoring.

### 9.3 Independent retry after repair

Repair is incomplete until the child receives an isomorphic or appropriately varied independent attempt.

### 9.4 Support fading

When evidence permits, the system should reduce conceptual support and/or access scaffolds rather than preserve maximum support indefinitely.

### 9.5 Stop rule

The system must be able to stop a learning episode when continued work would add little educational value, when the target evidence has been obtained, or when session state indicates that continuation is inappropriate. Stopping is a teacher move, not failure.

## 10. Source-model boundary

Primary sources often teach simplified models. The platform must distinguish:

```text
SOURCE MODEL
        ≠
FULLER CANONICAL MODEL
```

When a source example does not fit the simplified taxonomy, do not invent a child-facing category and pretend it was taught by the source.

Required internal statuses include:

```text
SOURCE_BOUNDARY
AMBIGUOUS
TEACHER_JUDGMENT
SOURCE_NOT_PROVIDED
```

Child-facing explanations should preserve the taught model and explain the boundary in age-appropriate language.

### 10.1 Grammar regression example

If a workbook teaches:

```text
number → opinion → size → age → shape → colour → origin → material → purpose
```

and a word such as `heavy`, `broken`, or `handmade` does not map cleanly into that simplified taxonomy, the tutor must not silently add `quality`, `condition`, or another invented category as though it were part of the workbook rule.

## 11. Subject specialization

### 11.1 Mathematics

`Grade4MathSchema.md` remains the Grade 4 Math subject specialization.

Primary Math learning objects may include:

```text
CONCEPT
MICROCONCEPT
MATHEMATICAL_RELATION
STRATEGY
PROCEDURE
REPRESENTATION
MATHEMATICAL_LANGUAGE
PROBLEM_STRUCTURE
INVARIANT
MISCONCEPTION
```

Math keeps its concrete/pictorial/structural/symbolic progression and concept-to-transfer pedagogy.

### 11.2 English

`Grade4EnglishSchema.md` remains the Grade 4 English subject specialization.

Primary English learning objects may include:

```text
TEXT
TEXT_FEATURE
GENRE_FEATURE
READING_SKILL
READING_STRATEGY
GRAMMAR_FEATURE
GRAMMAR_RULE
VOCABULARY_SENSE
MORPHOLOGY_FEATURE
ORTHOGRAPHY_FEATURE
WRITING_MOVE
WRITING_CRITERION
ORAL_LANGUAGE_SKILL
VISUAL_LANGUAGE_SKILL
```

English must preserve its own evidence model: literature interpretation may be textually supported without being a single binary truth; writing may be rubric-evaluated rather than answer-key evaluated.

## 12. Grade 4 → Grade 5 rule

Grade is a scope/depth overlay over shared canonical learning objects where the underlying concept is the same.

Do not create duplicate ontologies such as `GRADE4_FRACTIONS` and `GRADE5_FRACTIONS` unless the learning object is genuinely different.

Prefer:

```text
canonical LearningObject
      ├─ Grade 4 scope/depth profile
      └─ Grade 5 scope/depth profile
```

## 13. Curriculum overlays

Curriculum mappings are many-to-many overlays.

A canonical learning object may map to:

```text
IB PYP continuum / conceptual expectation
NCF-SE Preparatory Stage competency
NCERT textbook/unit
school workbook/source
later assessment-demand profile
```

Curriculum overlays may change sequencing emphasis or required evidence, but may not duplicate canonical truth.

PYP developmental phases must not be hard-coded as grade equivalents.

## 14. Kani boundary

Kani is a learning-experience renderer and attempt-evidence runtime.

It may own:

```text
stable learner identity
game mechanics
stars/streaks/scores
mission runtime
immutable attempts
recent deterministic evidence summaries
```

It may not independently own:

```text
canonical curriculum truth
durable mastery
misconception diagnosis as fact
TeacherDecision
NextLearningAction
```

Game completion means `ACTIVITY_COMPLETED`, not `SKILL_MASTERED`.

## 15. Study-Hub boundary

Study-Hub may own:

```text
ExperienceManifest instances
renderer sequencing
print/PDF publication
QR / mission routing
cross-app versioned transport contracts
contract registry / compatibility locks
```

Study-Hub must consume Common semantics instead of becoming their source of truth.

## 16. Backend/provider independence

Educational semantics are orthogonal to provider architecture:

```text
Primary semantics ⟂ SQLite / Firebase / future provider
```

Study-Hub #39 owns deployment/storage/provider concerns. The same canonical attempts must have the same educational interpretation regardless of backend.

## 17. Primary acceptance gates

The architecture fails review if it cannot demonstrate all of the following:

- one canonical authority for learning and teaching semantics;
- long-lived learner evidence separated from current-session state;
- evidence separated from judgement;
- conceptual support separated from access/load support;
- representation role distinguishable where observable;
- repeated same-route failure causes a meaningful teaching change;
- child receives an independent retry after repair;
- support can fade;
- immediate performance is not durable mastery;
- delayed retention and transfer are distinct evidence dimensions;
- source simplification/ambiguity is represented explicitly;
- same canonical learning object can survive multiple renderers;
- Grade 4 and Grade 5 can share canonical objects without duplicate ontology;
- provider/backend choice cannot change educational meaning.

## 18. Deferred scope

Do not build into v1:

- a single-number psychometric learner score;
- full autonomous AI tutoring;
- all IB/NCF curriculum mappings;
- all Grade 4/5 chapters;
- comprehensive game migration;
- IMO/IOM or Spell Bee competition engines.

Competition remains a later `STRETCH`/assessment-demand extension over shared canonical knowledge.