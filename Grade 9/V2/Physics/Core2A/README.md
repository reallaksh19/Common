# Physics V2 — Core (2A): taught-state-gated transfer compiler + Worked Transfer Atlas

Core (2) remains the complete source-transfer authority. Core (2A) is a downstream learner-product compiler. It selects and realizes transfer practice for a stated learner purpose, but it may not change Physics truth, Core (2) source identity, Core (1A) teaching authority or learner-evidence history.

At the learner surface, Core2A is now explicitly a **self-guided declarative worked problem atlas**:

> **Show me how an expert recognizes, represents and solves this problem family.**

The canonical learner-product grammar is defined in `LEARNER_PRODUCT_SPEC_v1.md`.

## Frozen-source rule

Core2 source questions are frozen. Core2A must not rewrite a source question to make it easier.

Difficulty adaptation changes:

- support density;
- item ordering;
- prerequisite explanation;
- completion level;
- visual support;
- clearly-labelled `GENERATED_ORIGINAL` variants.

The worked-atlas grammar is:

```text
QUESTION
-> difficulty + required knowledge
-> WHAT SHOULD I NOTICE?
-> representation
-> WHY THIS MODEL?
-> FIRST MOVE
-> full working
-> physical/dimensional/limiting check
-> common wrong route
-> why the question is hard
-> what changes in a variation
```

## Semantic contract

```text
Core1 semantic boundary
∩ Core1A T-* TEACHING_COMPLETE receipts
∩ Core2 transfer envelope
∩ learner-product purpose
∩ owner policy
        ↓
      Core2A
```

A publication receipt proves that the learner product taught a capability. It does **not** prove that the learner mastered it. `learner_evidence_state = UNKNOWN` is therefore legal and expected.

## Purpose is mandatory

Exactly one purpose is required:

```text
FIRST_STUDY
PRACTICE
REVISION
COMPETITIVE_EXAM
```

Purpose changes source-question selection, generated challenge mix and support density. Purpose never expands legal Physics scope.

## Two lanes

### SOURCE_CORE2

The complete Core (2) corpus remains immutable authority. Core (2A) may select a purpose-dependent subset for a learner product, but it never deletes an unselected source question from Core (2).

A source item is learner-releasable only when every required capability has a matching `T-PHY-*` receipt with:

```text
publication_state = TEACHING_COMPLETE
learner_profile_ref = requested learner profile
purpose_ref = requested purpose
```

Otherwise the source question remains in corpus custody with `HELD_UNTIL_TEACHING_COMPLETE`.

### GENERATED_ORIGINAL

Fresh questions may be realized only when:

- the anchor Core (2) question is itself releasable and its problem-family/bucket binding agrees;
- every required capability has a matching teaching-complete receipt;
- the Physics validator type is supported and independently recomputes the governed relation;
- declared SI units are valid and the recomputed result matches the learner-facing canonical answer;
- the generated prompt passes near-copy checking against all source stems;
- staged help does not disclose the answer or duplicate full-working steps;
- provenance explicitly says `GENERATED_ORIGINAL` and does not claim false official-question provenance.

Unsupported Physics validators fail closed. They are not free-written.

## Physics validation

The v1 executable validator registry authorizes:

```text
CONSTANT_ACCELERATION_VELOCITY
CONSTANT_ACCELERATION_INITIAL_VELOCITY
CONSTANT_ACCELERATION_EVENT_TIME
VECTOR_DOT_PERPENDICULAR
SPEED_FROM_COMPONENTS
```

Additional problem families require an explicit validator before generated challenges from those families are production-legal.

## Release boundary

Core2A activates the semantic/executable legality model and the declarative learner-product grammar. A worked Core2A solution does not prove learner transfer; that evidence belongs to Core2B.
