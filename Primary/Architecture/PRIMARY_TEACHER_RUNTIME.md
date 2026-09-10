# Primary Teacher Runtime v1

**Status:** canonical semantic candidate  
**Authority:** Common  
**Tracking:** Common #162

## 1. Goal

The Primary Teacher Runtime defines how evidence about a Grade 4–5 learner becomes a bounded pedagogical next move.

It does not define UI, backend storage, game mechanics, or curriculum content. It defines the educational reasoning contract.

Central loop:

```text
OBSERVATION
    ↓
RESPONSE DIAGNOSIS
    ↓
TEACHER DECISION
    ↓
TEACHER MOVE
    ↓
CHILD ACTION
    ↓
NEW EVIDENCE
    ↺
```

## 2. Core records

### 2.1 TeachingTarget

Represents the purpose of the current encounter.

Minimum semantics:

```yaml
teaching_target:
  learning_object_ids: []
  purpose: ACQUIRE | REPAIR | INDEPENDENT | RETAIN | TRANSFER | STRETCH
  desired_evidence: []
  source_scope_ref: optional
  completion_condition: {}
```

The target is not the same as a publication format or game mission.

### 2.2 ChildLearningProfile

Long-lived evidence-backed learner information.

It may contain:

- repeatedly observed learning strengths/needs;
- stable or repeated modality/access evidence;
- subject/language history;
- prior mastery-dimension evidence;
- timestamps and confidence.

It must not contain unsupported personality, ability, medical, or intelligence labels.

### 2.3 SkillState

A learning-object-specific longitudinal state.

Preferred dimensions:

```yaml
skill_state:
  learning_object_id: MATH-FRAC-EQUIVALENCE
  acquisition: DEVELOPING
  independent_use: NOT_YET_TESTED
  delayed_retention: NOT_YET_TESTED
  transfer: NOT_YET_TESTED
  stretch: NOT_APPLICABLE
  evidence_refs: []
  confidence: MEDIUM
```

No single field should collapse these dimensions into durable `mastery`.

### 2.4 CurrentLearningState

Session-scoped state inferred from recent evidence and, where relevant, learner report.

Examples:

```text
recent unsuccessful attempts
recent successful attempts
current conceptual support
current access adjustments
repeated confirmation requests
current representation route
rushing candidate
fatigue reported by child
frustration signal
```

Rules:

- default lifetime is the current session;
- every inference carries evidence and confidence;
- promotion into a long-lived profile requires repeated evidence;
- transient state must not become a durable learner label automatically.

### 2.5 Observation

A factual or directly captured event.

Examples:

```text
selected option B
wrote 6
self-corrected after prompt
requested hint
chose a bar model
produced a number line
asked "Large?"
completed mission
returned to independent task
```

Observations should preserve provenance and renderer context.

### 2.6 ResponseDiagnosis

A bounded hypothesis explaining an observation.

Candidate classifications:

```text
CONCEPTUAL_MISCONCEPTION
PREREQUISITE_GAP
PROCEDURAL_ERROR
LANGUAGE_COMPREHENSION_ERROR
REPRESENTATION_ERROR
TASK_INTERPRETATION_ERROR
MEMORY_RETRIEVAL_FAILURE
PERFORMANCE_LAPSE
ATTENTION_OR_RUSHING_CANDIDATE
RESPONSE_FORM_ERROR
SOURCE_MODEL_BOUNDARY
INSUFFICIENT_EVIDENCE
```

A diagnosis must include:

```yaml
hypothesis:
  code: ...
  confidence: LOW | MEDIUM | HIGH
  evidence_refs: []
  competing_hypotheses: []
  information_needed: []
```

Diagnosis is not a permanent child trait.

### 2.7 TeacherDecision

Represents the pedagogical choice made from available evidence.

Typical decisions:

```text
DIAGNOSE_BEFORE_RETEACH
REPAIR_PREREQUISITE
REDUCE_ACCESS_LOAD
CHANGE_REPRESENTATION
MODEL_ONE_STEP
ASK_FOR_EXPLANATION
GIVE_INDEPENDENT_RETRY
FADE_SUPPORT
EXTEND_TO_TRANSFER
SCHEDULE_RETRIEVAL
END_EPISODE
```

A decision should record why the selected move is preferred over plausible alternatives.

### 2.8 TeacherMove

The observable teaching action.

Canonical candidate vocabulary:

```text
MODEL
THINK_ALOUD
ASK_TO_NOTICE
ASK_TO_SHOW
ASK_TO_EXPLAIN
RETRIEVE_PRIOR_KNOWLEDGE
BREAK_INTO_STEPS
REDUCE_LANGUAGE
CHANGE_REPRESENTATION
PROMPT
HINT
COMPARE
GIVE_INDEPENDENT_TURN
FADE_SUPPORT
EXTEND
CHANGE_ACTIVITY
OFFER_BOUNDED_CHOICE
ASK_TO_REFLECT
ASK_CHILD_TO_CHOOSE_REPRESENTATION
ASK_CHILD_TO_CREATE_EXAMPLE
END_SESSION
SCHEDULE_RETRIEVAL
```

Subject schemas may specialize the details of a move without redefining its core meaning.

## 3. Academic error vs performance lapse

Wrong answers must not mechanically trigger reteaching.

The runtime should distinguish stable misunderstanding from transient performance where evidence permits.

Example:

```text
prior evidence strongly secure
7 × 8 answered as 54
child immediately corrects after "check that again"
```

This may be classified as `PERFORMANCE_LAPSE` rather than reopening the multiplication concept.

Conversely, repeated structurally similar errors with no self-correction may justify a stronger misconception/prerequisite hypothesis.

## 4. Diagnostic causality rule

The runtime must identify the likely broken stage before choosing a repair route when evidence is insufficient.

Pattern:

```text
OBSERVED RESPONSE
→ ERROR SIGNATURE
→ HYPOTHESIS
→ DIAGNOSTIC QUESTION
→ EVIDENCE
→ REPAIR
→ RETRY
```

A diagnostic question should be as small as possible while separating plausible hypotheses.

## 5. Same-route failure invariant

If the learner fails twice on the same target while the support route is substantially unchanged, the next teacher move must vary a meaningful dimension.

Allowed dimensions include:

```text
representation
language load
concrete context
problem size
response modality
problem structure
prerequisite probe
example/non-example contrast
```

The runtime must not respond with the same explanation rewritten at greater length.

## 6. Conceptual support vs access adjustment

These are independent evidence dimensions.

### Conceptual support

```yaml
conceptual_support:
  level: H0 | H1 | H2 | H3 | H4 | H5
  type: NONE | PROMPT | HINT | MODEL | THINK_ALOUD | WORKED_EXAMPLE
```

### Access adjustments

```text
REDUCED_LANGUAGE
ONE_STEP_AT_A_TIME
ORAL_RESPONSE_ALLOWED
REDUCED_WRITING
READ_ALOUD
EXTRA_VISUAL_SPACING
```

A learner who requires only an access adjustment should not be marked conceptually dependent on hints.

Subject-specific skills may define the meaning of H1–H5. For example, Grade 4 English may use Find Target → Remember Rule → Test Options → Reread → Apply, while Math may map levels to progressively stronger mathematical help.

## 7. Representation evidence

Representation is both a teaching route and a source of independence evidence.

Record:

```yaml
representation:
  type: BAR_MODEL
  role: PROVIDED | CHILD_SELECTED | CHILD_PRODUCED
```

Interpretation rule:

```text
PROVIDED < CHILD_SELECTED < CHILD_PRODUCED
```

is often an independence-strength ordering, but subject context determines the final judgement. It must not be treated as a universal score.

## 8. Child action invariant

In tutor mode, the child should do observable thinking between substantial teaching chunks.

Examples:

```text
classify one item
show a model
say the next step
explain why
choose between two representations
complete one line
solve a near-isomorphic retry
```

Reference/study-guide mode is exempt when the user explicitly requests passive material.

## 9. Bounded learner agency

Where it does not undermine the target, the runtime may offer controlled choice.

Examples:

```text
SHOW_PICTURE
SMALLER_EXAMPLE
LET_ME_TRY

SIMILAR_PROBLEM
PUZZLE
EXPLAIN_BACK
```

Agency must remain bounded by the TeachingTarget and completion evidence.

## 10. Feedback/teacher voice policy

Primary feedback should:

- preserve the correct part of the learner's thinking;
- identify one useful next action;
- use specific rather than generic praise;
- avoid fixed-ability labels;
- keep mistakes safe to expose;
- avoid teacher-facing jargon unless the child has been taught it;
- avoid a long lecture immediately after an error;
- give a reproducible cue or method rather than only a conclusion.

Example:

```text
"Large tells us how big something is. Words that tell how big go in SIZE. Now try: where would tiny go?"
```

is preferable to:

```text
"Large → Size"
```

when the learner has already shown uncertainty about category mapping.

## 11. LearningEpisode runtime

A `LearningEpisode` is instantiated from:

```text
LearningCell
+ TeachingTarget
+ SkillState
+ CurrentLearningState
+ source/curriculum constraints
```

A typical episode may contain:

```text
CONNECT
DISCOVER / NOTICE
NAME
GUIDED ATTEMPT
CHILD TURN
EXPLANATION / REPAIR
SMALL SUCCESS
INDEPENDENT CHECK
OPTIONAL TRANSFER
EXIT REFLECTION
DELAYED RETRIEVAL
```

No fixed sequence is mandatory for every task; prerequisites and observed evidence control the route.

## 12. Independent retry requirement

When a repair move supplies meaningful conceptual help, the episode should include an independent retry on an isomorphic or appropriately varied item before claiming independent evidence.

Correctness on the worked example itself is not independent evidence.

## 13. Support fading

Evidence of success should normally trigger one of:

```text
reduce conceptual support
remove provided representation
ask child to select representation
ask child to produce representation
increase task variation
move to transfer
```

Support must not be removed merely to increase difficulty; fading should test whether the learning has become independently available.

## 14. Mastery/learning evidence dimensions

Use independent dimensions:

```text
ACQUISITION
INDEPENDENT_USE
DELAYED_RETENTION
TRANSFER
STRETCH
```

`STRETCH` is optional and is not required for ordinary curriculum mastery.

Competition preparation such as IMO/IOM or Spell Bee should attach primarily to stretch/assessment-demand profiles rather than redefine foundational mastery.

## 15. Retention

Delayed retention requires evidence after a meaningful delay. Same-session repeated correctness does not count as delayed retention.

The runtime may schedule retrieval, but backend task scheduling is outside this specification.

## 16. Transfer

Transfer requires a change in surface structure, context, representation, or task demand sufficient to test whether the child can apply the learning beyond the exact taught pattern.

Transfer evidence must record the nature of the variation.

## 17. Stop rules

A Teacher Runtime must be able to end or defer an episode when:

```text
target evidence obtained
learner demonstrates independent success
continued repetition adds little value
session signals suggest fatigue/frustration overload
a prerequisite gap requires a different episode
source ambiguity requires teacher/source clarification
```

`END_SESSION` or `CHANGE_ACTIVITY` is a valid pedagogical move.

## 18. Source-model boundary handling

When a source teaches a simplified grammar/math classification and an example lies outside it:

```text
preserve source model
→ detect mismatch
→ mark SOURCE_MODEL_BOUNDARY
→ explain boundary in child-friendly language
→ keep fuller canonical analysis separate
```

Never invent a new child-facing category to force-fit the example.

## 19. Renderer boundary

Renderers execute or display Teacher Runtime outputs but do not own their semantics.

### Study-Hub

May assemble/publish an episode and route steps across renderers.

### Kani

May execute a mission and record observations. Game completion is not learning mastery.

### Print/PDF

May contain guided/independent steps and QR mission references. Static products cannot infer session state unless evidence is returned through another channel.

## 20. Runtime falsifiers

A Primary Teacher Runtime v1 fails if any of these are true:

- wrong answer always triggers reteaching;
- two same-route failures can produce a third substantially identical explanation;
- current-session behaviour silently becomes a durable learner trait;
- access support is recorded as conceptual hint dependence;
- worked-example success is recorded as independent use;
- game completion is recorded as mastery;
- same-session accuracy is recorded as delayed retention;
- source-boundary cases are force-fit into invented source categories;
- no observable child action occurs between substantial tutor explanations;
- repair is not followed by an independent retry when one is appropriate;
- the runtime has no valid stop condition.