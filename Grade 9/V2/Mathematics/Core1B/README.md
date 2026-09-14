# Mathematics Core1B — Open-Ended Self-Tutoring Consolidation

Core1B is a **static, build-time learner-product compiler** downstream of Core1A. The artifact does not branch live, but its page grammar is deliberately open-ended so a learner can reconstruct the idea without a teacher beside them.

## Governing question

> Can the learner reconstruct and independently use what was taught?

Core1B therefore starts with learner production before explanation.

```text
OPEN QUESTION
→ TRY / PREDICT / SKETCH
→ MEANING HELP
→ REPRESENTATION HELP
→ CONCEPT HELP
→ FIRST-MOVE HELP
→ PROCEDURE HELP
→ ANSWER + EXPLANATORY VERIFICATION
```

The learner may stop at any earlier help level. Help restores the smallest missing bridge rather than immediately disclosing a full solution.

## Owns

- open-ended consolidation prompts;
- method-comparison composition;
- correct/wrong contrast composition;
- controlled one-feature-at-a-time variation;
- completion examples and fixed fading;
- close independent consolidation;
- concept-level self-guided help frames;
- visual/representation clues with a stated cognitive purpose;
- learner-facing explanatory answer/check placement;
- static workbook quality audit.

## Does not own

- Core1A mathematical authority, PCK, representations, learner diagnosis or treatment;
- new mathematics outside approved capability refs;
- learner attempts or post-publication evidence;
- live diagnosis, branching, hints, repair routing or state transitions;
- Core2/Core2A legality or transfer scope.

## Required product shape

A full Core1B consolidation plan must contain:

1. at least one `METHOD_COMPARISON` or `ERROR_CONTRAST` block;
2. at least one `COMPLETION` or `FADED` block;
3. at least one `CLOSE_INDEPENDENT` block;
4. an `ANSWER_CHECK` block;
5. an open-ended self-guided frame on each substantive task.

`CONTROLLED_VARIATION` is strongly preferred because Core1B should change one important feature at a time before asking for wider transfer.

## Cognitive turning points

Core1B should prompt explanation at consequential moments, not after every line. Typical prompts ask:

- What object are we describing?
- What information is fixed?
- What can vary?
- Draw or organise what you think is happening.
- Which relation governs the situation?
- Why is the shortcut or transformation legitimate?
- What would make it fail?
- Can you reconstruct the equation or method without looking?

## Visual contract

Every primary visual or representation must state:

1. why it is present;
2. what relation it must make visible;
3. how the visual maps to words/symbols/equations;
4. what it must not imply.

## Static invariant

The compiler rejects fields associated with live tutoring, including:

```text
attempts
learner_evidence
state_transition
next_task
repair_map
runtime_hint
adaptive_branch
```

The compiled output declares:

```text
delivery_mode = STATIC
pedagogy_mode = OPEN_ENDED
learner_role  = RECONSTRUCT_AND_CONSOLIDATE
```

This is a **paper tutor**, not a live tutor. Static help availability is allowed; post-answer inference is not.

## Validation families

- `MATH-EQUIDISTANT-POINT-ON-AXIS`
- `MATH-LINEAR-SYSTEM-SOLVE`

Both use the same compiler while supplying different mathematics and worked-example structures.

## Fail closed

```text
CORE1B_LIVE_RUNTIME_FIELD_FORBIDDEN
CORE1B_UPSTREAM_AUTHORITY_MISSING
CORE1B_UNAPPROVED_CAPABILITY_REF
CORE1B_NEW_MATH_NOT_ALLOWED
CORE1B_REQUIRED_COMPARISON_MISSING
CORE1B_FADING_OR_COMPLETION_MISSING
CORE1B_CLOSE_INDEPENDENT_MISSING
CORE1B_ANSWER_CHECK_MISSING
CORE1B_VARIATION_CHANGES_MULTIPLE_CRITICAL_FEATURES
CORE1B_INTERNAL_METADATA_LEAK
```
