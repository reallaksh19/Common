# Chemistry LearningBlueprint v7 — deterministic product assurance

v7 sits **after v6 realization planning and before publication**. Its job is to prove that the learner product is complete, differentiated, correctly routed and fully traceable before any PDF is accepted.

```text
v6 realization plan
    ↓
PAL — Product Assurance Layer
    ├─ G-COV coverage / omission
    ├─ G-DUP duplication / similarity
    ├─ G-DIF intrinsic difficulty or task-demand validation
    ├─ G-PUR Core-purpose validation
    ├─ G-FIT learner-fit validation [Core2A/Core2B only]
    ├─ G-QA question provenance + answer closure
    ├─ G-BDG badge discipline
    └─ G-PUB measured publication quality
    ↓
release candidate
```

## G-COV — canonical content bill of materials

The writer does not decide what to remember while authoring. The Canonical Domain Registry is first converted into a Core Content Bill of Materials (CCBOM).

Every authorized asset receives a disposition for all six products:

```text
MUST_REALIZE
MUST_REFERENCE
MUST_RECONSTRUCT
MUST_APPLY
MUST_SELECT_OR_RECONSTRUCT
OPTIONAL
NOT_APPLICABLE
FORBIDDEN
```

No blank disposition is legal. Every mandatory disposition requires an explicit realization reference to a block/page/TTU/question episode.

Release requires:

```text
mandatory_closed / mandatory_total = 1.00
unresolved_asset_ids = []
```

Asset classes include concepts, learning atoms, equations, derivations, data/constants, representations, examples, misconceptions, boundaries, verification rules, questions and answers.

Important equations are not closed by merely printing the equation. Their CCBOM realization must close the required equation anatomy from upstream authority: parent concept/law, conditions, symbol meaning, justification/derivation, representation binding, use, boundary/misuse and verification where mandated.

## G-DUP — semantic reuse versus pedagogical duplication

Exact reuse is expected and legal for frozen source wording, canonical equations, canonical facts and source figures retained under custody.

Generated learner-facing prose and pedagogical structure are different.

### Non-frozen prose

Initial deterministic thresholds:

```text
normalized verbatim 5-gram overlap <= 10%
identical contiguous prose > 35 words => FAIL
```

The exclusions above are removed before the overlap calculation.

### Generated-example fingerprint

```text
S_example =
  0.15 family
+ 0.15 givens
+ 0.10 values
+ 0.15 target
+ 0.15 representation
+ 0.15 model sequence
+ 0.05 special condition
+ 0.10 solution path
```

Each component is normalized `0..1`.

```text
< 0.70       PASS
0.70–<0.85   REVIEW / declared pedagogical reason required
>= 0.85      FAIL near-duplicate
```

Declared `FADING_ANCHOR` and `SOURCE_QUESTION_IDENTITY` relationships are exceptions, but remain auditable and do not count as transfer evidence merely because they are reused.

### A/B pedagogical similarity

```text
S_ped =
  0.30 example
+ 0.20 representation state
+ 0.25 learner action
+ 0.25 interaction sequence
```

```text
< 0.45      PASS
0.45–0.60   REVIEW
> 0.60      FAIL
```

Independent hard fail: example + representation + sequence + learner action are all unchanged and no legal fading/source exception is declared.

These numbers are **initial engineering thresholds**, not empirical learning-effect claims. They are versioned policy and must be calibrated from reviewer/learner evidence later.

## G-DIF — difficulty and task demand

The word `difficulty` is not allowed to mean two different things internally.

### Core1A/Core1B

Badge: `INTRINSIC_DIFFICULTY`.

Ten evidence dimensions are scored `0..3`:

```text
prerequisite depth
element interactivity
inferential jumps
representation translation
abstraction
model discrimination
condition sensitivity
misconception density
symbolic/quantitative coupling
synthesis
```

Machine-derived score bands:

```text
0–9    EASY
10–19  MEDIUM
20–30  HARD
```

If owner/source authority supplies the final badge, PAL preserves both the derived result and authorized badge. One-band disagreement requires a reason; a two-band disagreement requires explicit owner confirmation.

### Core2/Core2A/Core2B

Use `TASK_DEMAND`, not Core1 intrinsic difficulty. The task-demand vector remains question-bound and owned by Core2/LAU authority.

## G-PUR — Core-purpose contract

Purpose is validated through required learner actions and prohibited dominant modes, not by headings.

```text
Core1A: explain + represent + justify/derive + contrast + modeled example
Core1B: predict/retrieve + reconstruct + explain/justify + verify
Core2A: expert recognition + setup + full solution + why-steps + verify
Core2B: attempt + model/representation choice + first-move commitment + justify + verify
```

For Core1B/Core2B, at least 60% of major TTUs must require learner-generated output. A hard purpose violation cannot be rescued by a high aggregate score.

## G-FIT — learner fit for Core2A/Core2B

PAL independently recomputes the support band from the same declared inputs used by LAU.

```text
LearnerEvidence OR OwnerOverride
× TaskDemand
× Purpose
→ validator support band
```

The compiler band and validator band must match.

For learner-evidence mode, knowledge percentage is only the routing prior. Capability-specific focus dimensions may tighten support. A focus dimension below 50 forbids `CHALLENGE_MINIMAL`; below 35 forbids both `STANDARD` and `CHALLENGE_MINIMAL`.

For owner-override mode, knowledge percentage must remain null/absent and the explicit support band plus reason are authoritative operational inputs.

PAL validates consistency with the supplied learner evidence. It does **not** claim that the product is empirically optimal for the learner before observed use.

## G-QA — question custody and answer closure

Every question has a stable `question_id` and learner-visible source.

For `SOURCE_FROZEN` questions PAL requires:

```text
source title
source unit/chapter
source question number
source locator
source stem hash
stem_identity_status = EXACT
answer_status = CLOSED
answer_ref
canonical_solution_ref
verification_ref
```

If the original source says `Q15(c)`, learner-facing source display retains `Q15(c)`.

For `GENERATED_ORIGINAL` questions learner-visible source must say it is generated/original and provide grounding refs. Generated questions may never masquerade as source questions.

Question without source display, answer closure or verification fails publication.

## G-BDG — badge taxonomy

Learner-visible badge families:

```text
BUCKET
CONCEPT
INTRINSIC_DIFFICULTY [Core1 track]
TASK_DEMAND [Core2 track]
PURPOSE
LINKAGE
PROBLEM_FAMILY
REPRESENTATION_TTU
LEARNER_ACTION
TRANSFER
SOURCE
SUPPORT [Core2 only]
VERIFICATION
ANSWER_STATE
```

Do not normally show more than six badges on one learner page. Knowledge percentage is machine-only and must never be displayed as a learner badge.

Machine-only audit metadata includes authority status, source hash, answer-closure state, research level, difficulty evidence score, knowledge-conditioning mode, LAU decision, task-demand vector, TTU closure, similarity score, release state, owner override and confidence/provenance.

## Release doctrine

```text
Coverage is checked against the canonical inventory,
not against what the writer happened to produce.

Differentiation is checked against structured pedagogical fingerprints,
not against visual appearance or paraphrase.

Difficulty is evidence-backed.
Purpose is contract-backed.
Learner fit is independently recomputed.
Every question is source-visible and answer-closed.
```

v7 is a deterministic architecture/release gate. It does not prove learner efficacy, mastery, retention or optimal personalization.
