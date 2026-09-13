# Grade 4 English — Adjective Boundary and Phrase Placement Contract (DRAFT)

**Status:** DRAFT — companion contract for `Grade4EnglishChildFacingV2_DRAFT.md`  
**Scope:** adjective classification and ordering only  
**Purpose:** prevent source-boundary words from creating invented school categories while still allowing a complete phrase when placement has an explicit authority.

---

## 1. Core invariant

The implementation must keep these two questions separate:

```text
What box does the school model give this word?

is NOT the same question as

Where does this word go in the completed English phrase?
```

Therefore:

```text
school category != phrase position
```

A word may have no school category and still have a supported phrase position.

---

## 2. Freeze the school model before analysing examples

Every adjective-order lesson must bind to exactly one `school_model` before any example is classified.

```yaml
school_model:
  model_id: ...
  source_ref: ...
  authority: ...
  verification_status: VERIFIED_PRIMARY_SOURCE | OWNER_CONFIRMED_PENDING_PRIMARY_SOURCE | DERIVED_ONLY | UNRESOLVED
  categories: []
  order: []
  immutable_for_episode: true
```

### Required invariants

1. `categories` and `order` are fixed for the episode.
2. Encountering a difficult word must not append a category.
3. A category absent from `categories` cannot be assigned to an adjective item.
4. General-English analysis must not silently mutate the school model.
5. If the primary workbook has not been verified, that uncertainty remains visible in internal metadata.

A learner example is never evidence that a new box exists.

---

## 3. Two-layer adjective record

Each adjective item must keep school classification separate from phrase placement.

```yaml
adjective_item:
  word: heavy

  school_analysis:
    category: null
    status: SOURCE_MODEL_BOUNDARY
    recognition_question: null
    child_message: "Heavy is a describing word, but it does not have a box in our book."

  phrase_placement:
    position_index: 1
    authority: OUTSIDE_CANONICAL_KNOWLEDGE
    evidence_ref: null
    child_message: "In this phrase, heavy comes after large."
```

For a word that is inside the school model:

```yaml
adjective_item:
  word: brown

  school_analysis:
    category: COLOUR
    status: CLASSIFIED
    recognition_question: "What colour?"
    child_message: "Brown tells the colour."

  phrase_placement:
    position_index: 2
    authority: EXPLICIT_SOURCE_RULE
    evidence_ref: ...
```

### Hard rule

`phrase_placement` must never be converted into a school category merely to make the data look complete.

---

## 4. Boundary-word contract

If a word does not fit the frozen school taxonomy:

```yaml
school_analysis:
  category: null
  status: SOURCE_MODEL_BOUNDARY
```

Do **not** create labels such as:

```text
QUALITY
PHYSICAL_QUALITY
CONDITION
TYPE
GENERAL_DESCRIPTION
OTHER_ADJECTIVE
```

unless that exact label is established by the bound school model.

Boundary words are still describing words. The boundary means only:

> this school model has no taught box for the word.

It does not mean the word is invalid, ungrammatical, or ignorable.

---

## 5. Phrase-placement authority

A completed phrase containing a boundary word may be asserted only when that word's placement has an explicit authority.

Use the strongest available authority in this order:

```text
1. EXPLICIT_SOURCE_RULE
2. EXPLICIT_SOURCE_EXAMPLE
3. OWNER_OR_TEACHER_SUPPLIED_RULE
4. DERIVED_STUDY_MATERIAL_ASSERTION
5. OUTSIDE_CANONICAL_KNOWLEDGE
6. SOURCE_UNRESOLVED
```

### Rules

- `EXPLICIT_SOURCE_RULE` and `EXPLICIT_SOURCE_EXAMPLE` may support both school classification and placement when the bound source actually establishes them.
- `OWNER_OR_TEACHER_SUPPLIED_RULE` may define the active school model, but should retain a verification status if the primary workbook has not yet been checked.
- `OUTSIDE_CANONICAL_KNOWLEDGE` may support phrase placement, but it must not create or rename a school category.
- `SOURCE_UNRESOLVED` cannot support a claimed final placement. If placement is unresolved, state that the source does not establish the answer.

---

## 6. Stable child procedure

Every ordering lesson should use the same visible sequence:

```text
1  Find the noun
        ↓
2  Find the describing words
        ↓
3  Put book words into their boxes
        ↓
4  Mark words that do not fit a box with ★
        ↓
5  Put the book boxes in book order
        ↓
6  Place ★ words only when we have a rule or example for them
        ↓
7  Read the whole phrase
```

The ★ means:

> still a describing word; no new school box.

Do not render `SOURCE_MODEL_BOUNDARY`, authority enums, provenance labels, or validation terminology on `CHILD_SURFACE`.

---

## 7. Model-dependent classification

The same word may receive different school-analysis results under different frozen models.

Example:

```text
Model A contains PURPOSE  -> classroom may be PURPOSE.
Model B has no PURPOSE    -> classroom must not become PURPOSE merely because normal English can analyse it that way.
```

This is expected. The validator must evaluate the item against the model bound to that case, not against a global adjective taxonomy.

---

## 8. Required regression cases

The following cases are mandatory fixtures for this contract:

```text
large heavy brown leather suitcase
colourful handmade Afghan woollen blanket
cheerful new bright classroom posters
broken old metal cooking pot
```

Minimum assertions:

- `heavy` is never promoted to `SIZE`, `QUALITY`, or `PHYSICAL_QUALITY` unless a bound source explicitly creates such a category.
- `handmade` is never promoted to `QUALITY`, `TYPE`, or `CONDITION` unless present in the bound model.
- `broken` is never promoted to `CONDITION`, `QUALITY`, or `TYPE` unless present in the bound model.
- `classroom -> PURPOSE` is legal only when the bound model contains `PURPOSE`.
- `cooking -> PURPOSE` is legal only when the bound model contains `PURPOSE`.
- Every boundary word in a claimed completed phrase has non-unresolved placement authority.
- Child-facing messages contain no internal labels.

---

## 9. Validation failures

Validation must fail when any of the following occurs:

```text
CATEGORY_NOT_IN_FROZEN_MODEL
MODEL_MUTATED_BY_EXAMPLE
BOUNDARY_WORD_ASSIGNED_INVENTED_CATEGORY
BOUNDARY_WORD_MISSING_PLACEMENT_AUTHORITY
UNRESOLVED_PLACEMENT_USED_IN_FINAL_PHRASE
PURPOSE_ASSIGNED_WITHOUT_PURPOSE_MODEL
INTERNAL_LABEL_LEAKED_TO_CHILD_SURFACE
EXPECTED_PHRASE_MISMATCH
```

These are internal diagnostics only.

---

## 10. Adoption rule

This contract remains draft while the primary workbook taxonomy/order is unresolved.

It may be used immediately for:

- regression fixtures;
- extraction checks;
- renderer prototypes;
- supervised learner trials.

It must not silently change `skills/grade4-english/SKILL.md` or the canonical `Grade4EnglishSchema.md` until primary-source verification and learner-facing review are complete.
