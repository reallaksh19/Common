# Mathematics Core1B — Static Consolidation Compiler

Core1B is a **build-time learner-product compiler** downstream of Core1A. It does not interact with the learner while the artifact is being used.

## Governing question

> Given Core1A-governed mathematics and the already-authorized learner treatment, what fixed consolidation workbook should be published?

## Owns

- method-comparison composition;
- correct/wrong contrast composition;
- controlled one-feature-at-a-time variation;
- completion examples;
- fixed worked-example fading;
- close independent consolidation;
- learner-facing answer/check placement;
- static workbook quality audit.

## Does not own

- Core1A mathematical authority, PCK, representations, learner diagnosis or treatment;
- learner attempts or post-publication evidence;
- live diagnosis, branching, hints, repair routing or state transitions;
- Core2/Core2A legality or transfer scope.

## Required product shape

A full Core1B consolidation plan must contain:

1. at least one `METHOD_COMPARISON` or `ERROR_CONTRAST` block;
2. at least one `COMPLETION` or `FADED` block;
3. at least one `CLOSE_INDEPENDENT` block;
4. an `ANSWER_CHECK` block.

`CONTROLLED_VARIATION` is strongly preferred and required by the two current goldens.

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

The compiled output declares `delivery_mode = STATIC`.

## Validation families

- `MATH-EQUIDISTANT-POINT-ON-AXIS`
- `MATH-LINEAR-SYSTEM-SOLVE`

Both use the same compiler while supplying different mathematics and different worked-example structures.

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
