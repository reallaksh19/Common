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

When learner work contains meaningful intermediate reasoning, the evidence path expands before diagnosis:

```text
CHILD WORK / SOURCE ARTIFACT
        ↓
OBSERVABLE WORK EVIDENCE
  answer / operation / intermediate steps
  quantity-unit relationships
  representations / child-created strategies
  self-corrections / teacher annotations with provenance
        ↓
ERROR SIGNATURE / STRUCTURAL PATTERN
        ↓
BOUNDED DIAGNOSIS
        ↓
SMALLEST DISCRIMINATING PROBE
        ↓
TEACHER DECISION / MOVE
        ↓
INDEPENDENT RETRY
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
- Primary Math `MathematicalWorkEvidence`, `QuantityStructure`, strategy-support roles and error-signature semantics;
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
MathematicalRelation / QuantityStructure where subject-relevant
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
Study-Hub / Print / Kani / Oral / notebook / other renderer
              ↓
Attempt / response / work trace / representation use
              ↓
Observable evidence
              ↓
Teacher Runtime interpretation
```

For mathematics, the observable evidence layer may include ordered `WorkStep` records, quantity/unit structure, child-generated strategy supports and teacher annotations with separate provenance. See `PRIMARY_MATH_WORK_EVIDENCE.md`.

## 4. Evidence is not judgement

Freeze this dependency:

```text
RAW OBSERVATION / ATTEMPT / WORK TRACE
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
operation selected
intermediate mathematical steps
quantity/unit roles where observable
representation used
representation role
child-created strategy/support
access adjustment used
conceptual support used
teacher annotation with separate provenance
```

Examples of Teacher Runtime interpretation:

```text
possible misconception
possible prerequisite gap
possible procedural mechanism
possible language bottleneck
possible task/quantity-structure misunderstanding
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

### 6.3 Child-generated strategy support

A self-created mathematical support is not teacher-provided conceptual help.

Examples:

```text
child writes a multiplication/multiples table
child draws a bar model
child creates a place-value table
child chooses a number line
```

Where observable, record the support role as `PROVIDED`, `CHILD_SELECTED`, or `CHILD_PRODUCED`. A `CHILD_PRODUCED` support may be positive strategic independence evidence even when the final answer is incorrect.

## 7. Representation evidence includes role

Where observable, represent at least:

```text
PROVIDED
CHILD_SELECTED
CHILD_PRODUCED
```

Being shown a number line is weaker independence evidence than selecting or constructing the number line unaided.

The same role vocabulary may be used for subject-specific strategy supports when the distinction is educationally meaningful.

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

### 9.6 Work-trace preservation before diagnosis

When intermediate mathematical work exists, the runtime must preserve successful and unsuccessful substeps before forming a broad diagnosis.

A final incorrect answer must not erase evidence that the child selected the correct operation, generated useful facts, used a valid representation, or completed earlier place-value steps correctly.

### 9.7 Contrast before broad reteach

When structurally related attempts are available, the runtime should compare them before concluding that the whole concept is weak.

A repeated failure at one mechanism combined with stronger performance on a close contrast may justify a narrow error signature and a small diagnostic probe rather than whole-topic reteaching.

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
QUANTITY_STRUCTURE
INVARIANT
MISCONCEPTION
```

Math keeps its concrete/pictorial/structural/symbolic progression and concept-to-transfer pedagogy.

When learner work is available, `PRIMARY_MATH_WORK_EVIDENCE.md` defines how to preserve `MathematicalWorkEvidence`, ordered work steps, quantity/unit structure, strategy-support roles, teacher annotations, math error signatures and contrast-based diagnostic evidence.

For word problems with grouped units, rates, money or conversion, the preferred reasoning model is:

```text
QUANTITY
→ UNIT
→ ROLE
→ RELATIONSHIP
→ UNKNOWN
→ OPERATION / OPERATIONS
```

Keywords such as `each`, `shared`, `per` or `altogether` are clues, not operation rules.

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

Classroom evidence may refine a school/source scope overlay without silently widening universal Grade 4 scope. For example, repeated classwork using two-digit divisors may establish `OBSERVED_IN_SCHOOL_CLASSWORK` for that school scope while the generic Grade 4 schema remains source-dependent.

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
observable work steps that its UI genuinely captures
```

It may not independently own:

```text
canonical curriculum truth
durable mastery
misconception diagnosis as fact
TeacherDecision
NextLearningAction
reconstructed notebook work it did not observe
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
source/notebook ingestion transport
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
- child-generated strategy support distinguishable from teacher-provided conceptual help;
- intermediate mathematical work preserved when available;
- successful substeps preserved alongside an incorrect final answer;
- quantity/unit/relationship structure representable for relevant word problems;
- teacher annotations kept separate from child independent work;
- structurally contrasting attempts can inform a bounded diagnosis;
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

## 19. Notebook/classwork regression gate

Before the Primary Teacher Runtime v1 is considered validated for Math, run at least one notebook/classwork replay where final-answer correctness is insufficient to explain the learner's pattern.

The replay must prove that the runtime can preserve and use:

```text
operation selection
intermediate work steps
quantity/unit structure
child-generated strategy supports
successful contrasting items
teacher annotations with separate provenance
bounded error signatures
```

The canonical fixture is `contracts/v1/examples/division-notebook-work-replay.example.json`.

The replay fails if the runtime reduces the evidence to `weak in division`, reteaches the whole algorithm from final answers alone, ignores child-created strategy evidence, ignores a necessary unit conversion, or counts teacher correction as independent child success.
