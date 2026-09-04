# Compression/Loss Preservation + Concept Assimilation Addendum v1

**Purpose:** prevent a compact student edition from becoming a revision-card stack that silently drops the mechanism, variants, transfer edges, or visuals required by the frozen corpus.

This addendum is mandatory whenever a study guide is condensed, repackaged, or regenerated from an earlier self-sufficient build, especially for large corpora.

The core rule is:

```text
compress pages, not support routes
```

A shorter book is acceptable only when the omitted material is either duplicated, reviewer-only, or deliberately supplied by a companion practice artifact. Compression must not remove information that makes a target question executable.

---

## 1. Packaging mode must be explicit

Choose one before student-book generation:

### SELF_CONTAINED_EDITION

The learner artifact contains the teaching core and the target practice stems required for self-contained use.

### REFERENCE_PLUS_PRACTICE_BOOK

The learner reference may omit frozen question stems if a clearly identified companion practice book/corpus is part of the package.

Required behavior:

- the reference preserves readable skill -> question routing;
- every target question still has a complete support route in the package;
- the reference states that the companion practice book is required;
- do not describe the reference alone as self-contained.

Gate:

```text
PACKAGING_MODE_DECLARED = PASS
PACKAGE_SELF_SUFFICIENCY = PASS_n_OF_n
```

---

## 2. Compression/Loss Ledger Contract

Before replacing a richer build with a compact build, produce a loss ledger.

For every stable skill and every target question, classify removed information:

```text
SAFE_TO_DROP
REFERENCE_DETAIL
ASSIMILATION_CRITICAL
TRANSFER_CRITICAL
VISUAL_CRITICAL
PRACTICE_ONLY
```

Definitions:

- `SAFE_TO_DROP`: duplicate prose, build metadata, reviewer machinery, or layout repetition.
- `REFERENCE_DETAIL`: useful enrichment that may be shortened without breaking execution.
- `ASSIMILATION_CRITICAL`: definition, mechanism, concrete example, legality, or contrast needed to understand the skill.
- `TRANSFER_CRITICAL`: an extra representation or bridge needed by at least one target question.
- `VISUAL_CRITICAL`: a structural visual whose removal increases the number of mental steps or obscures the representation.
- `PRACTICE_ONLY`: question stem/answer material intentionally kept in the companion practice artifact.

A compact edition fails if any `ASSIMILATION_CRITICAL`, `TRANSFER_CRITICAL`, or `VISUAL_CRITICAL` item disappears without an explicit replacement route.

Required gates:

```text
COMPRESSION_LOSS_LEDGER = COMPLETE
ASSIMILATION_CRITICAL_LOSSES_UNRESOLVED = 0
TRANSFER_CRITICAL_LOSSES_UNRESOLVED = 0
VISUAL_CRITICAL_LOSSES_UNRESOLVED = 0
```

---

## 3. Concept Assimilation Contract

A stable-skill page is not complete merely because it has a theorem name, a FIRST MOVE box, and practice IDs.

For an unfamiliar or non-routine concept, the learner should normally receive enough of the following roles to construct a usable mental model:

```text
WHAT IS THIS?
plain definition / object / relation

TINY EXAMPLE
small concrete instance before abstraction

THE EXAM / OLYMPIAD LINK
what surface wording should trigger this skill

WHY IT WORKS
mechanism, representation, or short proof idea

WORKED EXAMPLE
one complete non-identical example when execution is non-routine

FIRST MOVE
a concrete legal opening, preferably with actual numbers/symbols

VARIANTS AND CLOSE CONTRASTS
important nearby forms and decision boundaries

WATCH OUT
a real failure mode or counterexample

CHECK
an executed verification, not merely the word "check"

GUIDED PRACTICE
one scaffolded bridge toward independent execution

PRACTISE NEXT
readable skill -> question IDs / ladder rungs
```

These are **semantic roles, not mandatory equal-weight boxes**. The page should read like a strong teacher developing an idea, not like a form generated from a schema.

Direct/familiar skills may use fewer roles. Transfer-heavy skills require more depth.

---

## 4. Depth Class Contract

Do not give every skill the same page budget.

A useful default:

```text
A - DIRECT / FAMILIAR
short definition + example + first move + watch-out + practice

B - CORE STRATEGIC
mechanism + worked example + first move + contrast + check

C - TRANSFER-HEAVY
full assimilation + variants + guided practice + transfer routing

D - MULTI-TRANSFER
full assimilation + multiple named transfer labs/variants as required by corpus evidence
```

Depth class comes from prerequisite novelty, execution complexity, transfer-gap count, legality risk, and visual burden - not from a desired page count.

---

## 5. FIRST MOVE must be concrete

A generic directive such as:

> Compute the gcd first.

is weaker than a retrieval object such as:

```text
84x + 126y = 30

gcd(84,126) = 42
42 does not divide 30
STOP: no integer solutions.
```

When practical, FIRST MOVE should contain an actual miniature instance showing what the student writes or draws.

Gate:

```text
FIRST_MOVE_CONCRETE_INSTANCE = PASS_n_OF_n
```

---

## 6. WATCH OUT and CHECK must demonstrate, not label

For subtle skills:

- `WATCH OUT` should use a counterexample, illegal step, or nearby wrong route with concrete mathematics when possible.
- `CHECK` should execute a verification on an actual candidate, parameter family, domain condition, endpoint, residue class, equality case, or combinatorial count.

Examples:

```text
WATCH OUT
6x = 6 (mod 15) cannot be divided by 6 while keeping modulus 15.

CHECK
Test x = 1, 6, 11; all satisfy the original congruence, confirming one class modulo 5.
```

Gate:

```text
SUBTLE_WATCH_OUTS_WITH_CONCRETE_FAILURE = PASS_n_OF_n
CORE_CHECKS_WITH_EXECUTED_VERIFICATION = PASS_n_OF_n
```

---

## 7. Variant Contract

A learner must be taught important nearby variants when they change representation, first move, legality, or closure.

Typical variant triggers:

- same theorem under different admissibility conditions;
- direct cycle vs Euler vs multiplicative order;
- congruence-only digit sum vs exact carry accounting;
- unrestricted integer solutions vs positivity/range-constrained Diophantine solutions;
- ordinary last digits vs idempotents / least terminal exponent / last nonzero digits;
- direct floor interval vs nested/boundary-jump floors.

Do not create a Variant section merely to add volume. A variant must teach a real decision boundary or transfer edge.

Gate:

```text
SUBTLE_SKILLS_WITH_VARIANT_OR_CLOSE_CONTRAST = PASS_n_OF_n
```

---

## 8. Transfer Lab Contract

A transfer lab is the student-facing form of a real transfer-gap bridge.

Use it when the core skill is understood but a target family still needs an extra idea.

Student-facing transfer navigation should be:

```text
Question ID
-> readable transfer name
-> readable core concepts to review first
```

Internal IDs such as `NT-A17` may remain in secondary type or in the build dossier, but should not be the primary learner navigation language.

A transfer lab should normally contain:

- recognition cue;
- concrete first move;
- concise core route with enough execution to imitate;
- legality / wrong route;
- guided transfer prompt.

Transfer labs need not be collected into a detached "advanced chapter". They may be embedded beside the relevant skill or grouped in a clearly labelled transfer section, whichever improves learner navigation.

Gates:

```text
TRANSFER_EDGE_MANIFEST = PASS_n_OF_n
TRANSFER_MAP_READABLE_NAME_FIRST = PASS
RAW_TRANSFER_IDS_AS_PRIMARY_NAVIGATION = 0
HARD_TRANSFER_GAPS_WITHOUT_LAB = 0
```

---

## 9. Practice Map Contract

`Practice Map` has a specific learner-facing meaning:

```text
READABLE SKILL NAME -> TARGET QUESTION IDs
```

It is not:

- a reviewer question-to-method matrix;
- a concept graph export;
- Appendix B;
- a transfer-gap ledger.

For large corpora, a useful extension is:

```text
CORE PRACTICE: Q...
TRANSFER PRACTICE: Q... -> readable transfer name
```

Keep internal IDs secondary.

---

## 10. Navigation tables are UI, not data dumps

Any learner-facing table must be tested as an interface.

Reject:

- raw graph/matrix exports;
- dense internal-ID columns;
- text that runs off the page;
- tables so small that a student must zoom significantly;
- rows whose terminology only makes sense to the authoring system.

Prefer readable names, fewer columns, and multi-page tables over one compressed reviewer-style table.

---

## 11. Student-Surface Prototype Gate

Before generating a long book, render and inspect at least:

1. one concept-assimilation page from a transfer-heavy skill;
2. one navigation/router page;
3. one practice/transfer-map page.

When the domain relies on diagrams, include a prototype with a required visual.

Do not proceed to bulk generation until the prototype passes:

```text
CONCEPT_PROTOTYPE = PASS
NAVIGATION_PROTOTYPE = PASS
PRACTICE_PAGE_PROTOTYPE = PASS
VISUAL_PROTOTYPE = PASS_IF_REQUIRED
```

This gate exists to catch card-reader layouts, poor contrast, tiny tables, badge dominance, and raw-ID leakage before they are multiplied across dozens of pages.

---

## 12. Final-size legibility gates

The rendered PDF, not source code, is authoritative.

Reject any student page with:

```text
LOW_CONTRAST_HEADING
BROKEN_HEADING_COLOR
RAW_ID_DOMINANCE
TINY_NAVIGATION_TABLE
OFF_PAGE_TABLE_OR_TEXT
UNREADABLE_BADGE
CARD_STACK_WITHOUT_TEACHING_FLOW
BROKEN_GLYPH_OR_MATH
```

Required gates:

```text
LOW_CONTRAST_HEADINGS = 0
BROKEN_HEADING_COLORS = 0
RAW_SKILL_ID_PRIMARY_NAVIGATION = 0
TINY_NAVIGATION_TABLES = 0
OFF_PAGE_TABLES = 0
CARD_READER_PAGE_FAILURES = 0
```

---

## 13. Preservation audit after generation

After the student PDF is generated, re-run the question-level support matrix against the actual artifact/package.

For every target question verify:

```text
core skill exists
+ required transfer lab/variant exists
+ required visual exists
+ practice route is findable
+ legality/check remains taught
```

A successful compact build may have far fewer pages than the source build while still returning:

```text
QUESTION_SUPPORT_PACKAGE = PASS_n_OF_n
```

Page count is never the acceptance metric.

---

## Final rule

The compact book should feel simpler because its **interface** is simpler, not because the mathematics needed for transfer was deleted.
