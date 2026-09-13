# Grade 4 English — Child-Facing Production Schema V2 (DRAFT)

**Status:** DRAFT — non-authoritative, not yet wired into `skills/grade4-english/SKILL.md`  
**Extends:** `Grade4EnglishSchema.md` and the Primary Teacher Runtime  
**Purpose:** close the structural gap between source-faithful English semantics and genuinely child-facing Grade 4 learning materials.

---

## 1. Why this draft exists

The current Grade 4 English schema is strong on source fidelity, skills, diagnostics, evidence, and transfer. It does not yet constrain the **learner-facing instructional surface** strongly enough. A technically correct study guide can therefore still become dense, teacher-like, or over-expose internal labels.

This draft adds explicit rules for:

- source-authority separation;
- taught-category vs encountered-word separation;
- child-facing vs teacher/internal surfaces;
- short teach–act–check learning episodes;
- visible mental models;
- guided practice and scaffold fading;
- fresh independent retry;
- delayed retrieval;
- page/segment cognitive-load limits;
- source-boundary handling without inventing categories.

The target child-facing spine is:

```text
NOTICE
  -> UNDERSTAND
  -> WATCH ONE
  -> TRY ONE
  -> CHECK
  -> HINT / REPAIR IF NEEDED
  -> FRESH RETRY
  -> APPLY / TRANSFER
  -> DELAYED RETRIEVAL
```

This replaces weak publication structures such as:

```text
RULE DUMP -> MULTIPLE EXAMPLES -> LARGE PRACTICE SET -> ANSWER KEY
```

when the deliverable is intended for independent Grade 4 learning.

---

# 2. Source-authority model

Every extracted rule, category, order, example, question, and answer must carry an authority class.

```text
EXPLICIT_SOURCE_RULE
EXPLICIT_SOURCE_EXAMPLE
SOURCE_DERIVED_PATTERN
DERIVED_STUDY_MATERIAL_ASSERTION
OUTSIDE_CANONICAL_KNOWLEDGE
SOURCE_MODEL_BOUNDARY
SOURCE_UNRESOLVED
```

## 2.1 Taught category is not the same as encountered word

A word may appear in a source sentence without proving that the source teaches a new grammar category.

```text
encountered lexical item != taught category
example in sentence        != source taxonomy extension
```

If a simplified workbook teaches only seven adjective families, an unclassifiable word must not cause an eighth family to be invented.

## 2.2 Taxonomy provenance

For simplified grammar models, store:

```yaml
taxonomy:
  name: ...
  source_status: EXPLICIT_SOURCE_RULE | SOURCE_DERIVED_PATTERN | DERIVED_STUDY_MATERIAL_ASSERTION
  categories: []
  excluded_or_unresolved_examples: []
```

A broader canonical English taxonomy may be recorded separately, but must never be silently merged into the school model.

---

# 3. Audience surfaces

Each content object must declare where it belongs.

```text
CHILD_SURFACE
TEACHER_SURFACE
PARENT_SURFACE
INTERNAL_METADATA
```

## 3.1 Child surface

Use concrete Grade 4 language. Prefer recognition questions and actions.

Good:

```text
Where is it from?
What is it made of?
This word does not fit our seven boxes yet. Keep it aside.
```

Avoid exposing internal architecture terms such as:

```text
SOURCE_MODEL_BOUNDARY
provenance class
error signature
mastery state
```

unless the user explicitly requests a technical learner-facing explanation.

## 3.2 Teacher/internal surface

May retain exact diagnostic and provenance labels, including `SOURCE_MODEL_BOUNDARY`, error signatures, confidence, and source authority.

## 3.3 Dual-language boundary rule

A boundary may have two representations:

```yaml
boundary:
  internal_label: SOURCE_MODEL_BOUNDARY
  child_message: "This word does not fit our seven boxes yet. Keep it aside for now."
```

---

# 4. Child-facing Learning Episode contract

A learner-facing episode is smaller than a Learning Cell. A Learning Cell may generate several episodes.

```yaml
learning_episode:
  objective: ...
  child_goal: ...
  notice: ...
  mental_model: ...
  worked_example: ...
  immediate_check: ...
  guided_try: ...
  hint_ladder: []
  repair_probe: ...
  fresh_retry: ...
  transfer: ...
  delayed_retrieval: ...
```

## 4.1 One dominant move at a time

A page or screen should normally have one dominant instructional purpose:

```text
explain
model
classify
order
repair
apply
review
```

Do not stack several unrelated instructional purposes merely to reduce page count.

## 4.2 Child action after teaching

After a short teaching/model chunk, require observable child thinking before the next substantial explanation.

Preferred rhythm:

```text
teach  -> child acts
model  -> child tries
repair -> child retries
```

## 4.3 Worked-example limit

For a new grammar idea, default to **one fully worked example**, then an immediate check-for-understanding. Additional examples should be contrasts, not a passive block of four or five solved items.

---

# 5. Persistent visual mental models

For concepts that depend on classification, ordering, structure, evidence, or writing plans, define one persistent visual organizer.

Examples:

```text
Adjective Family Cards
Adjective Order Train
Noun Phrase Builder
Answer–Clue–Connection
Stanza Meaning Map
Species–Threat–Action table
```

The same model should recur across model, guided practice, hint, and retry where useful. Decorative graphics do not count as a mental model.

---

# 6. Grammar classification and ordering contract

For source-grounded adjective work, use this sequence:

```text
FIND NOUN
  -> FIND DESCRIBING WORDS
  -> CLASSIFY USING SOURCE QUESTIONS
  -> MARK UNRESOLVED WORDS
  -> ORDER ONLY SOURCE-SUPPORTED CATEGORIES
  -> READ ALOUD
  -> FRESH CHECK
```

## 6.1 Classification record

```yaml
adjective_item:
  surface_word: "Swedish"
  modifies: "object"
  source_category: ORIGIN
  recognition_question: "Where from?"
  authority: DERIVED_STUDY_MATERIAL_ASSERTION
  child_explanation: "Swedish tells where it is from."
```

## 6.2 Boundary record

```yaml
adjective_item:
  surface_word: "traditional"
  modifies: "..."
  source_category: null
  authority: SOURCE_MODEL_BOUNDARY
  child_explanation: "This word does not fit our seven boxes yet."
  canonical_analysis: null
```

Do not invent `quality`, `condition`, `type`, or another source category to force a fit.

## 6.3 Ordering rule record

```yaml
ordering_model:
  categories: []
  authority: ...
  evidence_ref: ...
  learner_display: ...
```

If `number`, `purpose`, or another category appears in a sentence but is not established by the supplied source model, do not promote it to the workbook taxonomy without evidence.

---

# 7. Practice progression

For a Grade 4 grammar concept, prefer:

```text
RECOGNISE
-> CLASSIFY
-> CONTRAST
-> ORDER / APPLY
-> CORRECT
-> FRESH INDEPENDENT RETRY
-> OWN SENTENCE / AUTHENTIC WRITING
-> DELAYED RETRIEVAL
```

A long list of near-identical classification items is not equivalent to this progression.

## 7.1 Contrast items

Use contrast pairs when two categories are easy to confuse.

Examples:

```text
wide vs round     -> SIZE vs SHAPE
Swedish vs wooden -> ORIGIN vs MATERIAL
old vs grey       -> AGE vs COLOUR
```

## 7.2 Fresh retry

The retry must change the lexical surface enough that success cannot come from remembering the worked example.

---

# 8. Hint and repair contract

Hints are progressive and must not reveal the answer too early.

For grammar classification:

```text
H1 FIND THE NOUN
H2 ASK THE SOURCE QUESTION
H3 NAME THE FAMILY
H4 TEST THE ORDER
H5 REREAD
```

A diagnostic probe should identify the broken step before more explanation is given.

Example:

```text
Observed: child places "large" under colour.
Probe: "Does large tell what colour, or how big?"
Likely diagnosis: GRAMMAR_RULE_ERROR / APPLICATION_ERROR
Repair: compare "large" with "red" using the recognition questions.
Retry: classify "tiny" without help.
```

After two unsuccessful attempts through substantially the same route, materially vary the representation, wording, response mode, or prerequisite probe.

---

# 9. Writing/application contract

Do not equate "more adjectives" with better writing.

When a source requires several adjectives across a paragraph:

- spread them naturally across sentences;
- preserve a clear noun;
- use strong nouns and verbs too;
- avoid adjective piles;
- distinguish grammar accuracy from writing quality.

A writing application should normally include a planner or response frame before independent composition.

---

# 10. Retrieval and evidence stages

Keep evidence separate by stage:

```text
ACQUISITION
INDEPENDENT_USE
DELAYED_RETENTION
TRANSFER
STRETCH (optional)
```

Same-session correctness does not establish delayed retention.

For a short study guide, include a small delayed check 3–7 days later where feasible.

---

# 11. Page/screen child-load constraints

These are defaults, not rigid typography laws.

A child-facing page should generally:

- have one clear goal;
- use short instructions;
- avoid exposing internal schema vocabulary;
- avoid more than one dense rule block;
- leave visible writing/thinking space;
- use one persistent organizer where structure matters;
- place a child action close to the teaching chunk it checks;
- avoid postponing all diagnostics and support to an answer-key section.

If a page reads primarily as notes for an adult, it is not child-facing merely because the font is large.

---

# 12. Extraction schema

Source-grounded extraction should create the following top-level object:

```yaml
source_extract:
  source:
    id: ...
    type: ...
    authority: ...
    transcription_status: ...
  source_model:
    explicit_rules: []
    derived_patterns: []
    unresolved_boundaries: []
  learning_cells: []
  learning_episodes: []
  visual_models: []
  tasks: []
  diagnostics: []
  transfer: []
  delayed_retrieval: []
  child_surface_policy: ...
  teacher_surface_notes: []
  provenance_notes: []
```

Each task should include, where applicable:

```yaml
- task_id: ...
  domain: GRAMMAR | READING | VOCABULARY | WRITING
  action: IDENTIFY | CLASSIFY | ORDER | CORRECT | EXPLAIN | WRITE | ...
  source_ref: ...
  source_authority: ...
  child_prompt: ...
  expected_response: ...
  mental_model_ref: ...
  hint_ladder: []
  diagnostic_probe: ...
  fresh_retry_ref: ...
  evidence_stage: ACQUISITION | INDEPENDENT_USE | DELAYED_RETENTION | TRANSFER
```

---

# 13. New quality gates

Add these gates to the existing Grade 4 English gates when producing learner-facing material:

```text
E-QG15 AUDIENCE_SURFACE_SEPARATION
E-QG16 TAUGHT_CATEGORY_PROVENANCE
E-QG17 CHILD_ACTION_DENSITY
E-QG18 TEACH_TRY_CHECK_SPINE
E-QG19 VISUAL_MENTAL_MODEL
E-QG20 SCAFFOLD_FADING_AND_FRESH_RETRY
E-QG21 PAGE_OR_SCREEN_CHILD_LOAD
E-QG22 DELAYED_RETRIEVAL_WHEN_APPLICABLE
```

### E-QG15 AUDIENCE_SURFACE_SEPARATION
Internal labels are not leaked into child-facing text without a pedagogical reason.

### E-QG16 TAUGHT_CATEGORY_PROVENANCE
Every taught category/order element is supported by the source authority claimed for it. Encountered words do not silently expand the taxonomy.

### E-QG17 CHILD_ACTION_DENSITY
Substantial teaching chunks are followed by observable child action rather than long passive reading.

### E-QG18 TEACH_TRY_CHECK_SPINE
The material visibly alternates explanation/model with try/check/repair.

### E-QG19 VISUAL_MENTAL_MODEL
A structural concept uses a reusable organizer rather than decorative layout alone.

### E-QG20 SCAFFOLD_FADING_AND_FRESH_RETRY
Guided support is followed by a genuinely fresh independent attempt.

### E-QG21 PAGE_OR_SCREEN_CHILD_LOAD
Page density, instruction length, terminology, and number of simultaneous moves are appropriate for Grade 4 independent use.

### E-QG22 DELAYED_RETRIEVAL_WHEN_APPLICABLE
Study/revision products include a later retrieval opportunity when the format permits it.

---

# 14. Draft migration rule

This file is intentionally **not canonical yet**.

Before adoption:

1. run at least one source-grounded adjective unit through the extraction schema;
2. compare the resulting child-facing plan against the current Grade 4 English schema;
3. inspect for source-boundary errors and accidental taxonomy expansion;
4. render and inspect at least one learner-facing PDF;
5. test with real or supervised Grade 4 learner evidence;
6. only then decide which clauses should migrate into `Grade4EnglishSchema.md` and `skills/grade4-english/SKILL.md`.
