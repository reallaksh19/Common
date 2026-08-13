# Grade 4 English — Skill, Text, Question-Bank & Textbook Production Schema

**Status:** Grade 4 production standard  
**Primary use cases:** textbook-quality English chapters, reading-comprehension banks, vocabulary and grammar learning, writing instruction, adaptive tutoring, source-grounded study material, teacher/student editions, and language-skill analytics.  
**Design principle:** Grade 4 English should not be forced into a mathematics-shaped schema. Its central objects are **text/language feature + skill + evidence/reasoning + response**, supported by prerequisite language knowledge, task variation, diagnostics, writing rubrics, mastery, and transfer.

---

## 1. Purpose

This schema defines how to turn a Grade 4 English source — textbook pages, stories, poems, grammar lessons, worksheets, school papers, teacher notes, or language-competition material — into a structured learning system.

A complete Grade 4 English production should contain:

1. a **source-faithful text and task layer**;
2. a **unit/text reverse-engineering layer**;
3. a **language-skill map**;
4. a **prerequisite/dependency graph**;
5. a **text profile** describing linguistic and comprehension demands;
6. **learning cells** for reading, vocabulary, grammar, and writing;
7. controlled **task archetypes**;
8. a **language-learning fingerprint** for each question/task;
9. a multidimensional **difficulty profile**;
10. an **evidence/response model** for comprehension;
11. **helpers and progressive hints** appropriate to the English domain;
12. **misconception/error diagnostics** and repair paths;
13. **practice sequencing** from recognition to independent use;
14. a **mastery model** based on multiple kinds of evidence;
15. a **transfer ladder** across passages, genres, contexts, and writing tasks;
16. provenance, editorial QC, and textbook-rendering QA.

The architecture is:

```text
SOURCE
  ↓
UNIT / TEXT REVERSE-ENGINEERING
  ↓
LANGUAGE-SKILL MAP
  ↓
PREREQUISITE GRAPH
  ↓
TEXT + LANGUAGE PROFILE
  ↓
LEARNING CELLS
  ↓
TASK ARCHETYPES
  ↓
QUESTION / TASK INSTANCES + LANGUAGE FINGERPRINTS
  ↓
DIFFICULTY PROFILE
  ↓
EVIDENCE / RESPONSE MODEL
  ↓
PEDAGOGICAL ENRICHMENT
  ↓
DIAGNOSTICS + REPAIR
  ↓
PRACTICE SEQUENCING
  ↓
MASTERY
  ↓
TRANSFER
  ↓
TEXTBOOK PRODUCTION + QA
```

---

# 2. Non-negotiable principles

## 2.1 Source fidelity first

Do not silently rewrite, simplify, modernize, correct, or replace a source passage or task.

Preserve when relevant:

```text
passage wording
paragraph boundaries
poem line breaks
capitalization
punctuation
dialogue formatting
illustrations
captions
headings
question wording
options
underlining/bold emphasis
answer key
```

Each extracted item must have one of:

- `VERIFIED_TRANSCRIPTION`
- `RECONSTRUCTED`
- `QC_ALERT`
- `SOURCE_UNRESOLVED`

If a source contains a grammar, spelling, punctuation, or factual defect, retain the original in provenance and mark the issue rather than silently correcting it.

## 2.2 English is not one skill

The top-level instructional domains are distinct:

```text
READING
VOCABULARY
GRAMMAR / LANGUAGE CONVENTIONS
WRITING
```

They share infrastructure but not identical pedagogy.

A reading-inference question, a subject–verb agreement item, and a paragraph-writing task need different fingerprints, hint ladders, diagnostics, and mastery evidence.

## 2.3 Evidence is central to reading comprehension

A child may select the correct option by guessing, background knowledge, or partial comprehension.

Therefore the system should distinguish:

```text
Correct answer
```

from:

```text
Correct answer supported by relevant textual evidence and reasoning
```

Whenever appropriate, comprehension records must preserve:

- the expected answer;
- the supporting evidence location;
- the reasoning link between evidence and answer.

## 2.4 Language production is different from answer selection

Writing does not usually have one correct answer.

Use a rubric and process model for writing tasks rather than forcing them into an MCQ-style correctness schema.

## 2.5 Difficulty is linguistic and cognitive

Do not treat text length as the main difficulty variable.

Difficulty may arise from:

- vocabulary;
- sentence structure;
- pronoun/reference chains;
- location of evidence;
- number of clues that must be integrated;
- inference distance;
- distractor subtlety;
- grammar-rule knowledge;
- required response length;
- organization and language production.

## 2.6 Diagnostics must identify the language process that broke

Do not label a child simply as `weak in comprehension`.

A wrong answer may come from:

- unknown vocabulary;
- inability to locate the relevant sentence;
- pronoun confusion;
- literal misunderstanding;
- weak inference;
- unsupported guessing;
- misunderstanding the question stem.

Diagnose the stage before prescribing repair.

## 2.7 Transfer is across language situations

For English, transfer may involve:

- a new passage;
- a longer passage;
- a different genre;
- less obvious evidence;
- multiple clues;
- moving from recognition to production;
- applying a grammar rule in authentic writing.

---

# 3. Core entity hierarchy

The Grade 4 English system uses:

```text
UNIT / TEXT SET
  ↓
DOMAIN
  ↓
SKILL / SUBSKILL / LEARNING CELL
  ↓
QUESTION OR WRITING TASK
```

Learner data is separate.

```text
Content question/task     ≠     StudentAttempt
Learning cell             ≠     StudentSkillState
Writing prompt            ≠     StudentWritingSubmission
```

---

# 4. Stage A — Source ingestion and editorial extraction

## 4.1 Source record

```json
{
  "source_id": "SRC-ENG-001",
  "type": "TEXTBOOK",
  "title": "...",
  "publisher": "...",
  "grade": 4,
  "edition": "...",
  "pages": "...",
  "url": "...",
  "verified": true,
  "verification_date": "YYYY-MM-DD"
}
```

## 4.2 Extract the unit before extracting isolated questions

Capture:

```text
unit title
anchor text / story / poem / article
genre
learning objectives
reading skill focus
vocabulary focus
grammar/language focus
writing focus
visuals/captions
teacher modelling
worked examples
practice sections
review sections
assessment
```

## 4.3 Text record

```json
{
  "text_id": "TXT-001",
  "source_id": "SRC-ENG-001",
  "title": "...",
  "genre": "NARRATIVE",
  "raw_text": "...",
  "paragraphs": [],
  "assets": [],
  "transcription_status": "VERIFIED_TRANSCRIPTION",
  "editorial_notes": "..."
}
```

## 4.4 Question/task extraction

```json
{
  "seed_id": "ENG-U3-Q08",
  "text_id": "TXT-001",
  "source_page": 84,
  "source_question_number": 8,
  "provenance_class": "USER_UPLOADED_ANCHOR",
  "transcription_status": "VERIFIED_TRANSCRIPTION",
  "raw_question": "...",
  "options": [],
  "source_answer": "...",
  "editorial_notes": "..."
}
```

## 4.5 Grade 4 English editorial QC

Check:

- punctuation and capitalization fidelity;
- poem line breaks/stanzas;
- quotation marks/dialogue formatting;
- missing headings/captions;
- whether a question requires a picture not captured;
- whether multiple options are defensible;
- whether the passage actually supports the answer;
- whether a “main idea” option is too broad/narrow;
- whether inference questions have enough evidence;
- whether vocabulary questions use the intended contextual sense;
- whether grammar items accidentally have multiple correct answers;
- whether writing directions specify audience/purpose/form when needed.

---

# 5. Stage B — Unit / text reverse-engineering

Before creating a bank, determine what the source is teaching.

For each unit/text set answer:

```text
1. What is the central text or language experience?
2. What genre/text type is used?
3. Which reading skills are taught explicitly?
4. Which vocabulary strategies are taught?
5. Which grammar/language features are taught?
6. Which writing outcome is expected?
7. How does teacher modelling move into independent work?
8. Does the unit move literal → inferential → analytical?
9. Does grammar move identify → choose → correct → apply?
10. Does writing move model → plan → draft → revise → edit?
11. What misconceptions/errors are anticipated?
12. What would mastery look like beyond the source text?
```

---

# 6. Stage C — Language-skill map

Use four main domains.

## 6.1 Reading

```text
READING
│
├── Literal comprehension
│   ├── Locate explicit detail
│   ├── Who / what / where / when
│   └── Follow directions/information
│
├── Text structure
│   ├── Sequence
│   ├── Cause and effect
│   ├── Compare and contrast
│   ├── Problem and solution
│   └── Description
│
├── Main ideas
│   ├── Main idea
│   ├── Supporting details
│   ├── Topic
│   └── Summary
│
├── Narrative understanding
│   ├── Character
│   ├── Setting
│   ├── Events
│   ├── Character traits
│   ├── Character motivation
│   ├── Problem / conflict
│   └── Theme / lesson at Grade-appropriate level
│
├── Inferential comprehension
│   ├── Inference from one clue
│   ├── Inference from multiple clues
│   ├── Prediction
│   ├── Cause not directly stated
│   └── Character feeling/motivation inference
│
├── Author / perspective
│   ├── Author purpose
│   ├── Point of view
│   ├── Fact and opinion
│   └── Word choice / tone at Grade-appropriate level
│
└── Evidence
    ├── Find supporting sentence
    ├── Select best evidence
    ├── Match claim to evidence
    └── Explain answer using evidence
```

## 6.2 Vocabulary

```text
VOCABULARY
│
├── Word meaning
├── Meaning in context
├── Synonym
├── Antonym
├── Multiple-meaning words
├── Homophones / homographs as appropriate
├── Prefixes
├── Suffixes
├── Root/base words
├── Compound words
├── Context clues
│   ├── definition clue
│   ├── example clue
│   ├── contrast clue
│   └── general sense
├── Idioms / common figurative expressions
├── Figurative language at Grade-appropriate level
└── Precise word choice
```

## 6.3 Grammar / language conventions

```text
GRAMMAR
│
├── Nouns
├── Pronouns
├── Verbs
├── Verb tense
├── Subject–verb agreement
├── Adjectives
├── Adverbs
├── Articles / determiners
├── Prepositions
├── Conjunctions
├── Sentence types
├── Subjects and predicates where curriculum-appropriate
├── Complete sentences / fragments
├── Word order
├── Capitalization
├── Punctuation
├── Apostrophes / contractions / possessives where appropriate
└── Editing / sentence correction
```

## 6.4 Writing

```text
WRITING
│
├── Idea generation
├── Planning
├── Audience and purpose
├── Organization
├── Topic sentence
├── Supporting details
├── Sequence / transitions
├── Paragraphing
├── Vocabulary / precise word choice
├── Sentence construction
├── Sentence variety at Grade-appropriate level
├── Revision
├── Editing
├── Narrative writing
├── Descriptive writing
├── Opinion writing
├── Informative/explanatory writing
├── Summary writing
└── Response to text
```

---

# 7. Stage D — Prerequisite graph

Prerequisites are dependencies, not tags.

Example: inference from multiple clues

```json
{
  "skill_id": "READ-INF-02",
  "dependencies": [
    {
      "skill_id": "READ-LITERAL-DETAIL",
      "strength": "CRITICAL"
    },
    {
      "skill_id": "VOCAB-CONTEXT",
      "strength": "CRITICAL"
    },
    {
      "skill_id": "READ-CAUSE-EFFECT",
      "strength": "STRONG"
    },
    {
      "skill_id": "BACKGROUND-KNOWLEDGE",
      "strength": "SUPPORTING"
    }
  ]
}
```

Example: subject–verb agreement

```text
Identify subject            CRITICAL
Identify verb               CRITICAL
Singular/plural concept     CRITICAL
Present-tense forms         STRONG
Pronoun reference           SUPPORTING
```

Allowed strengths:

```text
CRITICAL
STRONG
SUPPORTING
```

---

# 8. Stage E — Text profile

Text profile is a first-class object because English difficulty depends on the linguistic environment.

```json
{
  "text_profile": {
    "genre": "NARRATIVE",
    "text_type": "SHORT_STORY",
    "word_count": 520,
    "paragraph_count": 8,
    "average_sentence_complexity": "MODERATE",
    "vocabulary_load": 4,
    "dialogue_load": 3,
    "pronoun_reference_load": 4,
    "figurative_language_load": 2,
    "inference_density": 5,
    "information_density": 3,
    "chronology_complexity": 2,
    "background_knowledge_demand": 2,
    "illustration_dependency": false,
    "caption_dependency": false,
    "table_or_diagram_dependency": false
  }
}
```

The numeric values are internal calibration aids, not student-facing labels.

---

# 9. Stage F — Learning Cells

English uses domain-specific Learning Cells.

## 9.1 Reading Learning Cell

```yaml
learning_cell_id: READ-INF-02
title: Make an inference from two clues
domain: Reading
skill: Inference

learning_objective: >
  Combine two relevant details from a Grade 4 passage to infer information that
  is not directly stated and justify the inference with text evidence.

child_friendly_meaning: >
  The author may not tell me everything directly. I can put clues together to
  work out what is probably true.

prerequisites:
  - understand the sentences
  - locate important details
  - know key vocabulary

skill_invariant: >
  A valid inference must fit the text and be supported by clues.

recognition_cues:
  - answer not directly stated
  - question asks what is probably true / why / how a character feels
  - multiple details point to one conclusion

worked_examples: []
guided_practice: []
independent_practice: []
misconceptions: []
diagnostics: []
mastery_evidence: []
transfer_links: []
```

## 9.2 Vocabulary Learning Cell

Required sections:

```text
Target strategy / word knowledge
Child-friendly meaning
Prerequisites
Model sentence
Context clue type
Think-aloud
Worked examples
Guided practice
Word-choice contrast
Misconceptions
Diagnostic probe
Independent use
Transfer to new sentence/text
```

## 9.3 Grammar Learning Cell

Required sections:

```text
Target rule/feature
Meaning/function
Recognition pattern
Examples
Non-examples
Rule discovery / noticing
Worked example
Guided identification
Selection/completion
Correction
Transformation
Application in own sentence
Editing in authentic paragraph
Misconceptions
Diagnostic probes
Transfer into writing
```

## 9.4 Writing Learning Cell

Required sections:

```text
Writing purpose
Audience
Form/genre
Success criteria
Mentor/model example
Notice the craft/structure
Plan
Shared/guided composition
Independent draft
Revision target
Editing target
Rubric
Feedback prompts
Transfer prompt
```

---

# 10. Stage G — Task archetype space

Task archetypes are domain-specific.

## 10.1 Reading archetypes

```text
LOCATE_DETAIL
SELECT_DETAIL
SEQUENCE
MATCH_CAUSE_EFFECT
COMPARE
IDENTIFY_MAIN_IDEA
SELECT_SUPPORTING_DETAIL
SUMMARIZE
IDENTIFY_CHARACTER_TRAIT
INFER
PREDICT
IDENTIFY_AUTHOR_PURPOSE
IDENTIFY_POINT_OF_VIEW
FIND_EVIDENCE
SELECT_BEST_EVIDENCE
JUSTIFY_WITH_EVIDENCE
CROSS_TEXT_COMPARE
```

## 10.2 Vocabulary archetypes

```text
DEFINE
CONTEXT_MEANING
MATCH_MEANING
SYNONYM
ANTONYM
MULTIPLE_MEANING
WORD_PART_ANALYSIS
CONTEXT_CLUE_TYPE
REPLACE_WORD
CHOOSE_PRECISE_WORD
USE_IN_SENTENCE
```

## 10.3 Grammar archetypes

```text
IDENTIFY
CLASSIFY
MATCH
COMPLETE
CHOOSE
CORRECT
TRANSFORM
COMBINE
PUNCTUATE
CAPITALIZE
EDIT_SENTENCE
EDIT_PARAGRAPH
APPLY_IN_OWN_SENTENCE
APPLY_IN_WRITING
```

## 10.4 Writing archetypes

```text
BRAINSTORM
PLAN
ORDER_IDEAS
WRITE_TOPIC_SENTENCE
ADD_SUPPORTING_DETAIL
EXPAND_SENTENCE
WRITE_PARAGRAPH
SUMMARIZE
RESPOND_TO_TEXT
DRAFT_NARRATIVE
DRAFT_DESCRIPTION
DRAFT_OPINION
DRAFT_INFORMATIONAL
REVISE_FOR_IDEAS
REVISE_FOR_ORGANIZATION
REVISE_FOR_WORD_CHOICE
EDIT_FOR_GRAMMAR
EDIT_FOR_PUNCTUATION
```

---

# 11. Stage H — Language-learning fingerprint

## 11.1 Canonical fingerprint

```json
{
  "learning_fingerprint": {
    "language_domain": "...",
    "skill": "...",
    "subskill": "...",
    "task_action": "...",
    "text_type": "...",
    "target_language_feature": "...",
    "evidence_type": "...",
    "evidence_location": "...",
    "recognition_cues": [],
    "reasoning_moves": [],
    "language_knowledge": [],
    "distractor_logic": [],
    "response_form": "...",
    "expected_reasoning_path": [],
    "skill_invariant": "...",
    "transfer_invariant": "..."
  }
}
```

## 11.2 Reading reasoning moves

Suggested vocabulary:

```text
LOCATE_EXPLICIT_INFORMATION
IDENTIFY_REFERENT
TRACK_SEQUENCE
CONNECT_CAUSE_AND_EFFECT
COMPARE_DETAILS
DISTINGUISH_MAIN_IDEA_FROM_DETAIL
LOCATE_CHARACTER_ACTION
LOCATE_CHARACTER_DIALOGUE
COMBINE_TWO_CLUES
INFER_UNSTATED_MEANING
INFER_CHARACTER_FEELING
INFER_CHARACTER_MOTIVATION
ELIMINATE_UNSUPPORTED_OPTION
SELECT_TEXT_EVIDENCE
CONNECT_EVIDENCE_TO_CLAIM
SUMMARIZE_ESSENTIAL_INFORMATION
```

## 11.3 Vocabulary reasoning moves

```text
READ_SURROUNDING_SENTENCE
READ_BEFORE_AND_AFTER
IDENTIFY_DEFINITION_CLUE
IDENTIFY_EXAMPLE_CLUE
IDENTIFY_CONTRAST_CLUE
USE_PREFIX
USE_SUFFIX
USE_BASE_WORD
TEST_MEANING_IN_SENTENCE
COMPARE_CLOSE_MEANINGS
```

## 11.4 Grammar reasoning moves

```text
LOCATE_TARGET_WORD
IDENTIFY_WORD_FUNCTION
IDENTIFY_SUBJECT
IDENTIFY_VERB
CHECK_SINGULAR_PLURAL
CHECK_TENSE
CHECK_AGREEMENT
CHECK_SENTENCE_COMPLETENESS
CHECK_CAPITALIZATION
CHECK_PUNCTUATION
REPLACE_AND_REREAD
APPLY_RULE
```

## 11.5 Writing reasoning/process moves

```text
IDENTIFY_PURPOSE
IDENTIFY_AUDIENCE
GENERATE_IDEAS
SELECT_RELEVANT_IDEAS
ORGANIZE_SEQUENCE
WRITE_CLEAR_OPENING
ADD_SUPPORTING_DETAILS
USE_PRECISE_WORDS
CONNECT_SENTENCES
REVISE_MEANING
REVISE_ORGANIZATION
EDIT_GRAMMAR
EDIT_PUNCTUATION
CHECK_COMPLETENESS
```

---

# 12. Stage I — Difficulty profile

Use a profile appropriate to the English domain.

```json
{
  "difficulty": {
    "overall": 5.0,
    "decoding_demand": 2,
    "vocabulary_demand": 5,
    "sentence_comprehension_demand": 4,
    "text_location_demand": 5,
    "evidence_integration_demand": 6,
    "inference_demand": 6,
    "grammar_knowledge_demand": 0,
    "language_production_demand": 2,
    "writing_organization_demand": 0,
    "working_memory_demand": 4,
    "distractor_subtlety": 5,
    "response_demand": 3,
    "text_length_demand": 4,
    "transfer_distance": 2
  }
}
```

Not every field is relevant to every question. Irrelevant fields may be `0` or omitted according to implementation convention.

---

# 13. Stage J — Evidence / response architecture

This is central to English.

## 13.1 Reading comprehension answer object

```json
{
  "solution": {
    "answer": "...",
    "evidence": {
      "required": true,
      "type": "TEXTUAL",
      "supporting_locations": [
        {
          "paragraph": 3,
          "sentence": 2,
          "evidence_summary": "..."
        }
      ]
    },
    "reasoning": "...",
    "why_other_options_fail": []
  }
}
```

The system should distinguish:

```text
DIRECTLY_STATED
ONE_CLUE_INFERENCE
MULTI_CLUE_INFERENCE
WHOLE_TEXT_SYNTHESIS
```

## 13.2 Vocabulary answer object

Store:

```text
correct contextual meaning
relevant context clue
why competing meanings do not fit
example of correct usage where useful
```

## 13.3 Grammar answer object

Store:

```text
correct form
rule/function
target word(s)
minimal explanation
corrected sentence
```

## 13.4 Writing evaluation object

Do not use a single `correct_answer`.

```json
{
  "evaluation": {
    "type": "RUBRIC",
    "dimensions": [
      {
        "name": "CONTENT",
        "max_score": 4
      },
      {
        "name": "ORGANIZATION",
        "max_score": 4
      },
      {
        "name": "DETAILS_OR_EVIDENCE",
        "max_score": 4
      },
      {
        "name": "VOCABULARY",
        "max_score": 4
      },
      {
        "name": "SENTENCE_CONTROL",
        "max_score": 4
      },
      {
        "name": "GRAMMAR_AND_MECHANICS",
        "max_score": 4
      }
    ]
  }
}
```

Rubric descriptors should be Grade 4-specific and task-specific; do not rely only on numerical scores.

---

# 14. Stage K — “What should I notice?” taxonomy

English noticing should point to actual textual/language features.

Suggested types:

```text
QUESTION_WORD
KEY_DETAIL
CHARACTER_ACTION
CHARACTER_DIALOGUE
REPEATED_IDEA
SEQUENCE_SIGNAL
CAUSE_EFFECT_SIGNAL
CONTRAST
PRONOUN_REFERENCE
CONTEXT_CLUE
WORD_PART
GRAMMAR_SIGNAL
PUNCTUATION_SIGNAL
TEXT_STRUCTURE
EVIDENCE
WRITING_STRUCTURE
```

Example for inference:

```json
{
  "what_to_notice": [
    {
      "type": "CHARACTER_ACTION",
      "text": "Notice what Maya does after seeing the dark clouds."
    },
    {
      "type": "EVIDENCE",
      "text": "The text gives clues but does not directly state the weather outcome."
    }
  ]
}
```

Avoid empty advice such as `read carefully` or `look for clues` unless the clue type is specified.

---

# 15. Stage L — Skill trigger

Keep `recognition_cues` and `skill_trigger` separate.

Example:

```text
Recognition cues in this question:
“dark clouds”, “quickly brought clothes inside”

Skill trigger:
answer not directly stated + relevant clues → make an inference
```

Grammar example:

```text
Recognition cues:
subject = “She”; verb choices = “go/goes”

Skill trigger:
singular third-person subject + simple present → use matching singular verb form
```

---

# 16. Stage M — Helper architecture

Helpers are domain-sensitive teacher prompts.

## 16.1 Reading helper

```json
{
  "helper": {
    "understand_question": "What is the question asking you to find out?",
    "locate": "Which paragraph is most likely to contain useful information?",
    "notice": "Which words/actions seem important?",
    "connect": "What do these details suggest when you put them together?",
    "check_evidence": "Which sentence supports your answer?"
  }
}
```

## 16.2 Vocabulary helper

```text
Read the whole sentence.
What happens before and after the word?
Is there a definition/example/contrast clue?
Does a prefix/suffix/base word help?
Which meaning makes the sentence sensible?
```

## 16.3 Grammar helper

```text
What word/part of the sentence is the question testing?
What job does that word do?
Which rule applies?
Try the options in the full sentence.
Does the sentence sound and read correctly after the change?
```

## 16.4 Writing helper

```text
What is your purpose?
Who will read this?
What is your main idea?
Which details belong?
What order will be clearest?
What can you improve before editing spelling/punctuation?
```

---

# 17. Stage N — Progressive hint architecture

English should not use one hint ladder for every domain.

## 17.1 Reading hint ladder

```text
H1 — LOOK       10%
Where in the text should I focus?

H2 — REMEMBER   25%
What reading skill/rule should I activate?

H3 — FIND       45%
Which detail(s) provide evidence?

H4 — CONNECT    70%
How do the details answer the question?

H5 — RESPOND    90%
How should I state the answer/evidence?
```

Example — inference:

```text
H1 LOOK
Look again at what the character does after seeing the clouds.

H2 REMEMBER
An inference uses clues plus what you already understand.

H3 FIND
Find two details that point to the same idea.

H4 CONNECT
What conclusion explains both details?

H5 RESPOND
State the conclusion and support it with one relevant clue.
```

## 17.2 Vocabulary hint ladder

```text
H1 CONTEXT
H2 CLUE TYPE
H3 WORD PART
H4 TEST MEANING
H5 CHOOSE / USE
```

## 17.3 Grammar hint ladder

```text
H1 FIND THE TARGET
H2 REMEMBER THE RULE
H3 CHECK THE RELEVANT WORDS
H4 TEST THE OPTIONS / CORRECTION
H5 APPLY AND REREAD
```

## 17.4 Writing scaffold ladder

Writing uses scaffolds rather than “answer-reveal” hints:

```text
S1 IDEA
S2 ORGANIZE
S3 EXPAND
S4 REVISE
S5 EDIT
```

Writing support must not produce the child’s full composition unless the activity explicitly models a sample response.

---

# 18. Stage O — Misconception and error model

## 18.1 Error classes

```text
DECODING_ERROR
VOCABULARY_ERROR
PRONOUN_REFERENCE_ERROR
TEXT_LOCATION_ERROR
LITERAL_COMPREHENSION_ERROR
SEQUENCE_ERROR
CAUSE_EFFECT_ERROR
MAIN_IDEA_ERROR
INFERENCE_ERROR
EVIDENCE_ERROR
QUESTION_INTERPRETATION_ERROR
GRAMMAR_RULE_ERROR
GRAMMAR_APPLICATION_ERROR
RESPONSE_FORM_ERROR
WRITING_IDEA_ERROR
WRITING_RELEVANCE_ERROR
WRITING_ORGANIZATION_ERROR
SENTENCE_CONTROL_ERROR
EDITING_ERROR
```

## 18.2 Reading diagnostic example

Child gives a plausible but unsupported inference.

```json
{
  "error_signature": "plausible_answer_without_text_support",
  "error_stage": "EVIDENCE_ERROR",
  "possible_cause": "Student answered from imagination/background knowledge rather than the passage.",
  "diagnostic_probe": "Which words in the passage support your answer?",
  "evidence_expected": "Student identifies a relevant textual clue.",
  "repair": "Return to the relevant paragraph and distinguish text evidence from outside ideas.",
  "retry": "New inference item with one explicit supporting clue."
}
```

## 18.3 Vocabulary diagnostic example

```text
Observed:
child chooses a familiar dictionary meaning that does not fit the sentence

Hypothesis:
ignoring contextual sense

Probe:
read the sentence with the chosen meaning substituted

Repair:
compare two meanings and test each against the sentence
```

## 18.4 Grammar diagnostic example

```text
Observed:
“She go to school every day.” accepted as correct

Possible cause:
subject–verb agreement rule not activated

Probe:
What is the subject? Is it one person or more than one?

Repair:
contrast I/you/we/they go with he/she/it goes, then retry in a new sentence
```

## 18.5 Writing diagnostic model

Writing errors should map to stage:

```text
IDEA GENERATION
RELEVANCE
ORGANIZATION
DETAIL DEVELOPMENT
VOCABULARY
SENTENCE CONSTRUCTION
GRAMMAR
PUNCTUATION
SPELLING
REVISION
```

Do not collapse all writing feedback into grammar correction.

---

# 19. Stage P — Practice sequencing

Practice should progress by skill demand, not merely accumulate questions.

## 19.1 Reading sequence

```text
Teacher think-aloud
  ↓
Locate explicit detail
  ↓
Use one obvious clue
  ↓
Use two clues
  ↓
Select best answer
  ↓
Provide evidence
  ↓
Explain reasoning
  ↓
New passage
  ↓
New genre / farther transfer
```

## 19.2 Vocabulary sequence

```text
Recognize meaning
  ↓
Use context clue
  ↓
Compare possible meanings
  ↓
Select precise meaning
  ↓
Use word in new sentence
  ↓
Use word in writing
```

## 19.3 Grammar sequence

```text
NOTICE / IDENTIFY
  ↓
CLASSIFY
  ↓
CHOOSE / COMPLETE
  ↓
CORRECT
  ↓
TRANSFORM
  ↓
APPLY IN OWN SENTENCE
  ↓
EDIT IN PARAGRAPH
  ↓
USE IN AUTHENTIC WRITING
```

## 19.4 Writing sequence

```text
Read/analyse a model
  ↓
Notice structure/craft
  ↓
Plan
  ↓
Shared/guided composition
  ↓
Independent draft
  ↓
Revision for meaning/organization
  ↓
Editing for conventions
  ↓
Publish/share as appropriate
  ↓
Transfer to new prompt
```

---

# 20. Stage Q — Mastery model

Mastery differs by domain.

## 20.1 Reading mastery

Evidence should cover:

```text
literal understanding
text navigation / locating evidence
vocabulary in context
information integration
inference
main idea / summary as appropriate
justification with evidence
transfer to unfamiliar passage
transfer to different genre
```

## 20.2 Vocabulary mastery

```text
recognize meaning
infer meaning in context
distinguish close meanings
understand useful word parts
use word appropriately in a new sentence
apply in authentic reading/writing
```

## 20.3 Grammar mastery

```text
recognize feature
explain/use rule at Grade-appropriate level
select correct form
correct an error
apply in new sentence
edit in paragraph
use independently in writing
```

## 20.4 Writing mastery

```text
ideas/content
relevance to prompt
organization
supporting details/evidence
vocabulary
sentence control
grammar/mechanics
revision
editing
independence
transfer to new prompt
```

## 20.5 Mastery states

Suggested:

```text
NOT_STARTED
EMERGING
GUIDED
DEVELOPING
SECURE
TRANSFER_READY
```

Do not calculate mastery from raw accuracy alone.

---

# 21. Stage R — Transfer ladders

## 21.1 Reading transfer

```text
T0 — PREREQUISITE REPAIR
T1 — SAME SKILL / SAME PASSAGE
T2 — SAME SKILL / NEW SHORT PASSAGE
T3 — SAME SKILL / LONGER PASSAGE
T4 — SAME SKILL / NEW GENRE
T5 — MULTIPLE-CLUE INTEGRATION
T6 — COMBINED READING SKILLS
T7 — EVIDENCE JUSTIFICATION
T8 — CROSS-TEXT / ADVANCED TRANSFER
```

## 21.2 Vocabulary transfer

```text
T1 familiar sentence
T2 new sentence
T3 new paragraph
T4 same strategy with unfamiliar word
T5 distinguish close meanings
T6 use word independently
```

## 21.3 Grammar transfer

```text
T1 identify
T2 complete
T3 correct
T4 transform
T5 new sentence/context
T6 paragraph editing
T7 authentic writing use
```

## 21.4 Writing transfer

```text
T1 imitate model structure
T2 change details / same form
T3 new prompt / same purpose
T4 new audience/context
T5 independent composition
T6 response-to-text or cross-domain application
```

---

# 22. Similar-question / analogue system

Use arrays rather than fixed fields.

```json
{
  "analogues": [
    {
      "task_id": "...",
      "role": "NEW_PASSAGE_SAME_SKILL",
      "similarity": {
        "skill": 1.0,
        "reasoning": 0.95,
        "evidence_type": 0.9,
        "text_complexity": 0.8,
        "surface_topic": 0.3
      },
      "difference_summary": "Same inference structure in an informational passage."
    }
  ]
}
```

Suggested roles:

```text
PREREQUISITE_REPAIR
NEAR_TWIN
NEW_PASSAGE_SAME_SKILL
NEW_GENRE_SAME_SKILL
EVIDENCE_TRANSFER
TASK_ACTION_TRANSFER
GRAMMAR_APPLICATION_TRANSFER
WRITING_TRANSFER
ADVANCED_TRANSFER
```

Similarity should prioritize skill/reasoning/evidence structure over topic words.

---

# 23. Canonical Reading question record

```json
{
  "id": "ENG-READ-INF-001",

  "question": {
    "stem": "...",
    "question_type": "MCQ",
    "options": [],
    "expected_answer": "..."
  },

  "provenance": {
    "source_id": "...",
    "text_id": "...",
    "source_page": null,
    "source_question_number": null,
    "provenance_class": "ORIGINAL_CALIBRATED",
    "verified": true
  },

  "classification": {
    "subject": "English",
    "grade": 4,
    "domain": "READING",
    "skill": "INFERENCE",
    "subskill": "CHARACTER_MOTIVATION",
    "task_archetype": "INFER"
  },

  "learning_fingerprint": {
    "language_domain": "READING",
    "skill": "INFERENCE",
    "subskill": "CHARACTER_MOTIVATION",
    "task_action": "INFER",
    "text_type": "NARRATIVE",
    "target_language_feature": null,
    "evidence_type": "MULTIPLE_TEXT_CLUES",
    "evidence_location": "TWO_SENTENCES_SAME_PARAGRAPH",
    "recognition_cues": [],
    "reasoning_moves": [],
    "language_knowledge": [],
    "distractor_logic": [],
    "response_form": "MCQ",
    "expected_reasoning_path": [],
    "skill_invariant": "valid inference is supported by text clues",
    "transfer_invariant": "combine evidence to infer unstated meaning"
  },

  "difficulty": {},
  "prerequisites": [],
  "what_to_notice": [],
  "skill_trigger": "",
  "helper": {},
  "hints": [],

  "solution": {
    "answer": "...",
    "evidence": {},
    "reasoning": "...",
    "why_other_options_fail": []
  },

  "diagnostics": [],
  "learning_takeaway": "...",
  "transfer_links": [],
  "analogues": []
}
```

---

# 24. Canonical Grammar question record

```json
{
  "id": "ENG-GRAM-SVA-001",
  "classification": {
    "subject": "English",
    "grade": 4,
    "domain": "GRAMMAR",
    "skill": "SUBJECT_VERB_AGREEMENT",
    "task_archetype": "COMPLETE"
  },
  "learning_fingerprint": {
    "target_language_feature": "PRESENT_TENSE_SINGULAR_VERB",
    "task_action": "CHOOSE",
    "recognition_cues": ["singular subject", "simple present"],
    "reasoning_moves": [
      "IDENTIFY_SUBJECT",
      "CHECK_SINGULAR_PLURAL",
      "IDENTIFY_VERB",
      "APPLY_RULE",
      "REREAD_SENTENCE"
    ],
    "response_form": "SINGLE_CHOICE",
    "skill_invariant": "subject and present-tense verb must agree in number/person"
  },
  "difficulty": {},
  "prerequisites": [],
  "what_to_notice": [],
  "skill_trigger": "",
  "helper": {},
  "hints": [],
  "solution": {},
  "diagnostics": [],
  "transfer_links": []
}
```

---

# 25. Canonical Writing task record

```json
{
  "id": "ENG-WR-NAR-001",

  "classification": {
    "subject": "English",
    "grade": 4,
    "domain": "WRITING",
    "skill": "NARRATIVE_WRITING",
    "task_archetype": "DRAFT_NARRATIVE"
  },

  "task": {
    "prompt": "...",
    "purpose": "ENTERTAIN",
    "audience": "CLASSROOM_READER",
    "form": "SHORT_NARRATIVE",
    "expected_length": "...",
    "source_text_id": null
  },

  "learning_fingerprint": {
    "task_action": "DRAFT",
    "reasoning_moves": [
      "GENERATE_IDEAS",
      "SELECT_RELEVANT_IDEAS",
      "ORGANIZE_SEQUENCE",
      "ADD_SUPPORTING_DETAILS",
      "WRITE_CLEAR_ENDING",
      "REVISE_MEANING",
      "EDIT_CONVENTIONS"
    ],
    "response_form": "EXTENDED_WRITING"
  },

  "success_criteria": [],
  "planning_scaffold": {},
  "writing_scaffolds": [],
  "evaluation": {
    "type": "RUBRIC",
    "dimensions": []
  },
  "diagnostics": [],
  "transfer_links": []
}
```

---

# 26. Student data — separate schema

Do not place learner state in immutable content records.

Reading/grammar attempt:

```json
{
  "student_attempt": {
    "student_id": "...",
    "task_id": "...",
    "attempt_number": 1,
    "answer": "...",
    "correct": false,
    "evidence_response": "...",
    "hints_used": [1, 2],
    "diagnostic_path": [],
    "timestamp": "..."
  }
}
```

Writing submission:

```json
{
  "student_writing_submission": {
    "student_id": "...",
    "task_id": "...",
    "draft": "...",
    "revision_history": [],
    "rubric_scores": {},
    "feedback": [],
    "timestamp": "..."
  }
}
```

Skill state:

```json
{
  "student_skill_state": {
    "student_id": "...",
    "skill_id": "READ-INF-02",
    "state": "DEVELOPING",
    "evidence": [],
    "known_gaps": [],
    "next_recommended_cells": []
  }
}
```

---

# 27. Unit/chapter assembly standard

A Grade 4 English unit may include:

```text
Unit opener / essential question
Vocabulary preview
Anchor text
First read / literal understanding
Skill modelling
Guided comprehension
Vocabulary strategy
Grammar/language lesson
Writing connection
Independent reading questions
Evidence-based response
Writing task
Revision/editing
Mixed review
Mastery check
Transfer text/task
Spiral review
```

Do not force all units into the same page structure. Preserve the source’s genre, skill sequence, and language purpose.

---

# 28. Source-grounded bank production

When building from supplied textbook/questions:

```text
SOURCE TEXT + ANCHOR TASKS
  ↓
classify each by domain + skill + archetype + fingerprint
  ↓
map evidence requirements
  ↓
check coverage across the language-skill map
  ↓
identify missing instructional forms
  ↓
generate/retrieve controlled variants
  ↓
rank by skill/reasoning/evidence similarity
  ↓
enrich with helpers/hints/solutions/diagnostics
  ↓
QA for passage support, level, repetition, and coverage
```

Do not create variants solely by changing names or topics.

---

# 29. Provenance classes

Recommended:

```text
USER_UPLOADED_ANCHOR
OFFICIAL_SOURCE
PUBLISHED_REFERENCE
ORIGINAL_CALIBRATED
RECONSTRUCTED_FROM_SCAN
WEB_ANALOGUE_METADATA_ONLY
```

For copyrighted texts, store/use source material only according to applicable permissions and task context; newly authored passages are preferable for scalable original banks.

---

# 30. English verification / QA

Every scored task should pass the relevant checks.

## 30.1 Reading QA

```text
✓ answer supported by the passage
✓ evidence location identified
✓ distractors are clearly less supported
✓ inference does not require unsupported outside knowledge
✓ question wording matches the intended skill
✓ pronoun references are unambiguous
✓ text complexity matches intended Grade 4 level
✓ image/caption dependency is handled
✓ H1/H2 do not reveal the answer
```

## 30.2 Vocabulary QA

```text
✓ intended meaning fits context
✓ competing meanings do not also fit
✓ word-part clue is linguistically valid
✓ example sentence is natural
✓ distractors are plausible but distinguishable
```

## 30.3 Grammar QA

```text
✓ exactly one intended answer for scored objective items
✓ target rule is correct
✓ sentence remains natural after correction
✓ punctuation/capitalization examples are unambiguous
✓ no accidental dialect/register issue unless explicitly taught
```

## 30.4 Writing QA

```text
✓ purpose is clear
✓ audience is clear where relevant
✓ task form is clear
✓ success criteria match instruction
✓ rubric aligns to the prompt
✓ expected length is Grade-appropriate
✓ scaffolds support rather than write the answer for the child
```

---

# 31. Textbook-quality rendering standard

Use consistent editorial labels such as:

```text
READ
NOTICE
WORD WORK
GRAMMAR FOCUS
THINK ABOUT THE TEXT
FIND THE EVIDENCE
TRY IT
HELPER
HINT
CHECK YOUR ANSWER
WRITING WORKSHOP
REVISE
EDIT
MISCONCEPTION CLINIC
TAKEAWAY
CHALLENGE
```

Grade 4-specific requirements:

- readable line length and font size;
- generous white space;
- clear paragraph numbering when evidence location matters;
- strong separation between passage and questions;
- preserve poem/stanza formatting;
- do not overcrowd vocabulary/glossary boxes;
- clearly distinguish model answer from student response area;
- writing pages need sufficient working space;
- illustrations should support comprehension rather than create irrelevant clues;
- teacher-facing diagnostics should not appear accidentally in student editions.

Every final PDF should be rendered to images and visually inspected.

---

# 32. Prototype acceptance tests

Before declaring the English schema stable, build at least four complete prototypes.

## Prototype A — Reading

```text
Skill:
Inference from two textual clues
```

Must include:

```text
✓ source/text profile
✓ prerequisites
✓ teacher think-aloud
✓ what-to-notice prompts
✓ evidence model
✓ worked example
✓ guided practice
✓ new-passage practice
✓ five-level reading hints
✓ misconception/error signatures
✓ diagnostic probes
✓ mastery evidence
✓ genre transfer
```

## Prototype B — Vocabulary

```text
Skill:
Meaning from context clues
```

Must include context-clue types, distractor logic, diagnostic repair, and transfer to unfamiliar words.

## Prototype C — Grammar

```text
Skill:
Subject–verb agreement
```

Must include identify → complete → correct → paragraph edit → writing transfer.

## Prototype D — Writing

```text
Skill:
Grade 4 narrative paragraph / short composition
```

Must include model analysis, planning, drafting, revision, editing, rubric, feedback categories, and transfer prompt.

---

# 33. Final schema philosophy

The Grade 4 English engine should model different processes by domain.

## Reading

```text
UNDERSTAND THE QUESTION
  ↓
LOCATE RELEVANT TEXT
  ↓
NOTICE LANGUAGE / DETAILS
  ↓
CONNECT INFORMATION
  ↓
FORM ANSWER
  ↓
SUPPORT WITH EVIDENCE
  ↓
CHECK AGAINST THE TEXT
  ↓
TRANSFER TO A NEW TEXT
```

## Vocabulary

```text
NOTICE THE WORD
  ↓
READ THE CONTEXT
  ↓
USE CLUES / WORD PARTS
  ↓
TEST POSSIBLE MEANINGS
  ↓
CHOOSE / USE PRECISE MEANING
  ↓
TRANSFER TO NEW CONTEXT
```

## Grammar

```text
NOTICE THE TARGET FEATURE
  ↓
IDENTIFY ITS FUNCTION
  ↓
ACTIVATE THE RULE
  ↓
TEST / CORRECT
  ↓
REREAD
  ↓
APPLY IN NEW SENTENCE
  ↓
USE IN AUTHENTIC WRITING
```

## Writing

```text
UNDERSTAND PURPOSE + AUDIENCE
  ↓
GENERATE IDEAS
  ↓
ORGANIZE
  ↓
DRAFT
  ↓
DEVELOP
  ↓
REVISE
  ↓
EDIT
  ↓
TRANSFER TO NEW PROMPT
```

The goal is not merely to answer Grade 4 English questions. The goal is to model **how Grade 4 language understanding and production develop**, where comprehension or language use breaks, how it is diagnosed and repaired, and whether the skill transfers to unfamiliar texts and authentic writing.
