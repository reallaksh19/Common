# Mathematics V2 — Self-Teaching Pedagogy Contract

> **Consolidated Specification Notice**:
> This document is consolidated under the canonical subordinate module [`PEDAGOGY_AND_CALIBRATION.md`](PEDAGOGY_AND_CALIBRATION.md) as part of Mathematics V2 Specification Consolidation. It is preserved here for contract stability, historical references, and granular analysis.

This document governs learner-facing pedagogy for Core1A, Core1B, Core2A and Core2B. It does not change Core1/Core2 authority and it does not move learner-state inference into static products.

## Governing model

```text
Core1A  BUILD understanding                    (DECLARATIVE)
Core1B  RECONSTRUCT + CONSOLIDATE             (OPEN_ENDED)
Core2A  LEARN expert solution anatomy         (DECLARATIVE)
Core2B  SELECT + TRANSFER + DISCRIMINATE      (OPEN_ENDED)
```

```text
A = explanation-first / declarative self-teaching
B = elicitation-first / open-ended self-tutoring

Core1 series = build and reconstruct knowledge
Core2 series = apply, select and transfer knowledge
```

A separate generation-control distinction is mandatory:

```text
Core1A / Core1B depth
= SUBTOPIC DIFFICULTY BADGE
!= learner knowledge percentage

Core2A / Core2B calibration
= learner knowledge percentage
OR explicit owner waiver + owner-selected controls
```

See `GENERATION_CALIBRATION.md` for the executable rules.

## Core1A — build understanding

Core1A remains the mature declarative teaching layer. It explains meaning, representations, equations, inference bridges, misconceptions and initial guided practice. It is not forced into the open-ended tutor page grammar.

A learner should be able to answer:

- What mathematical object is being studied?
- What is fixed and what can vary?
- Why is each important relation legitimate?
- How does the visual/representation map to symbols?
- When does the method or shortcut fail?

Core1A closes the loop with worked examples, checks and verified answers, but explanation may precede difficult application.

Core1A is always authored **subtopic-wise as a bucket**. The bucket receives one `EASY / MEDIUM / HARD` difficulty badge based on mathematical/pedagogical complexity or owner designation, not on learner knowledge percentage. The badge governs minimum research obligation, decomposition, representation density and page ceiling. It does not forbid discovery.

## Core1B — reconstruct and consolidate

Core1B is an open-ended paper tutor. It starts with learner production before explanation.

> Can the learner reconstruct and independently use what was taught?

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

The learner does not need to consume every help step. Help restores only the smallest missing bridge. The final answer/check is always available because the product is self-taught.

Core1B prompts target cognitive turning points, not every line. Typical prompts ask:

- What object are we describing?
- What information is fixed?
- What can change?
- Draw what you think is happening.
- Why is this relation true?
- Which assumption allowed that step?
- What would make this shortcut fail?
- Can you reconstruct the equation without looking?

Core1B uses the **same subtopic bucket and difficulty badge as Core1A**. It may reorganize the mathematics into open-ended tutor moves, but it may not raise or lower knowledge depth because of learner knowledge percentage.

## Core1-series depth badges

Page budgets are **ceilings, not quotas**. Do not pad a bucket to reach a page count.

| Badge | Maximum pages per stage/bucket | Pedagogy web research | Decomposition | Representation expectation |
|---|---:|---|---|---|
| EASY | 10 | optional | subtopic only | visual + stepwise + dedicated diagrams where useful |
| MEDIUM | 20 | required, targeted | subtopic → sub-subtopic allowed | high visual density, stepwise reasoning, dedicated diagrams |
| HARD | 30 | required, deep | subtopic → sub-subtopic allowed | very high representation density, inference bridges, dedicated diagrams/graphs/tables |

Research permission and research obligation are intentionally separate. Web search may be used for any bucket when it improves representation, explanation, misconception repair or source understanding. `EASY` means that pedagogy research is not mandatory for promotion; it does **not** prohibit useful investigation. If optional research is used, its brief and evidence references must be fully bound. Half-bound research is invalid.

For MEDIUM/HARD, a research brief plus credible web evidence is required before authoring. Source count is not used as a quality proxy. The research brief must record what the external research contributed to representation, explanation, misconception handling or decomposition.

Research is promoted claim-by-claim, not merely because a URL appears in a manifest. Every declared research-decision coverage category must have an explicit pedagogy claim. Every retained source relevant to that claim category is classified as `SUPPORTS` or `CONTRADICTS`; a promoted claim needs supporting evidence, and contradictory retained evidence needs an explicit resolution. Claims record `LOW / MODERATE / HIGH` confidence, while production promotion rejects `LOW` confidence. Sources actually used by promoted claims must remain in the bucket's bound research references. Discovery-only material may remain outside that promoted binding. None of these rules impose a universal minimum number of sources.

External research can improve pedagogy; it never becomes curriculum authority or expands legal mathematical scope. Source Integrity verification remains a separate path when original evidence is ambiguous, conflicted or damaged.

## Core2A — solution apprenticeship

Core2A remains governed by explicit learner purpose (`STARTER / PRACTICE / REVISION / COMPETITION`) and may use only legal/taught mathematics. Frozen Core2 source questions remain byte-faithful in identity and stem; difficulty adjustment occurs through selection, support density, ordering and generated variants with new provenance.

Core2A additionally requires **learner knowledge percentage** as a generation-calibration input. If that percentage is not known, generation is blocked unless the owner explicitly waives the requirement and supplies all replacement controls.

The percentage is a product-calibration input, not a mastery claim and not a replacement for `UNKNOWN / DEVELOPING / READY`.

The calibration must resolve:

```text
Core2A support profile
Core2A maximum generated-question demand level
Core2B maximum transfer demand level
```

> How does an expert recognize and solve this legal class of questions, and why does each non-obvious move work?

Each substantive Core2A solution should expose:

```text
question
→ structural cue / what matters
→ representation choice
→ first non-obvious move
→ step-by-step solution
→ why consequential moves are legitimate
→ alternative method where useful
→ common wrong chain / misconception
→ numeric / symbolic / graphical verification
→ nearby variant: what changes and what stays invariant?
```

Knowledge calibration may change generated-question demand, question selection within legal scope, support density, worked-step granularity, representation support and ordering. It may not rewrite frozen source questions or create curriculum authority.

## Core2B — transfer tutor

Core2B is an open-ended transfer tutor downstream of Core2A legality. It selects only from the legal pool and obeys the resolved Core2B transfer ceiling.

Core2B uses the same learner-calibration input as Core2A. If knowledge percentage is unknown, the owner waiver must explicitly state the support/demand controls; the system must not invent a pseudo-percentage.

> Can the learner recognize, select and transfer the mathematics when the surface changes and the method is not named?

```text
UNFAMILIAR / LESS-CUED QUESTION
→ ATTEMPT
→ RECOGNITION HELP
→ CONCEPT / STRUCTURE HELP
→ REPRESENTATION HELP
→ FIRST-MOVE HELP
→ METHOD HELP
→ ANSWER + EXPLANATORY VERIFICATION
```

When discrimination is being tested, family/method labels must not be visible before the attempt. Higher transfer may change representation, target direction, cue visibility, hidden constraints, method choice, family choice, multi-step synthesis or novelty, but cannot introduce illegal mathematics.

## Core2 knowledge-calibration gate

Core2A and Core2B must receive exactly one of these paths:

```text
A. learner_knowledge_percent = 0..100
   + knowledge source/reference
   + named calibration policy reference
   + resolved Core2A support profile
   + resolved Core2A maximum demand level
   + resolved Core2B maximum demand level

OR

B. owner waiver
   + owner identity/reference
   + reason percentage is unavailable
   + owner-selected Core2A support profile
   + owner-selected Core2A maximum demand level
   + owner-selected Core2B maximum demand level
```

Invalid states:

```text
no percentage + no waiver          → BLOCK
percentage + waiver simultaneously → BLOCK
waiver without explicit controls   → BLOCK
inferred/default percentage        → FORBIDDEN
silent default support/ceilings    → FORBIDDEN
```

Learning purpose remains separate from knowledge calibration. `PRACTICE` is not a default and must never be inferred from knowledge percentage.

The architecture deliberately does **not** hard-code percentage bands such as `0–40 / 40–70 / 70+` without an owner-approved calibration policy. A named policy must resolve percentage to concrete controls, or the owner must directly supply those controls through the waiver path.

## Universal self-teaching closure

A self-taught learner must never reach a dead end. Every meaningful learning object has an answer/check path in some form.

All four stages provide:

- explanatory answer support;
- numeric or symbolic verification;
- graphical/representation verification when useful;
- misconception or wrong-path support where the learning objective needs it;
- provenance for source and generated questions;
- no false claim that a static page has measured mastery.

## Visual contract

A visual is a mathematical representation, not decoration. Every primary visual states:

1. cognitive purpose — why the visual exists;
2. what must become visible;
3. the bridge from picture/diagram/table/graph to words and symbols;
4. what the visual must not imply.

## Source-question integrity

```text
SOURCE QUESTION            = immutable
QUESTION INTERPRETATION    = derived
HINTS                      = derived
SOLUTION                   = independently verified
VISUAL                     = derived
GENERATED VARIANT          = new identity + new provenance
```

Core2/Core2A/Core2B may not silently rewrite a frozen source question to alter difficulty.

## Static-product epistemic boundary

```text
PLANNED PEDAGOGY
!= COMPILED STATIC PRODUCT
!= RENDERED ARTIFACT
!= LEARNER ATTEMPT
!= LEARNER PERFORMANCE EVIDENCE
```

The open-ended B grammar is a static self-tutoring design. It does not ingest responses, branch live, or declare new learner state. Any actual learner evidence enters later through the governed learner-intelligence boundary.

## Research basis and limits

The design is informed by evidence that worked examples support initial acquisition, especially when learners actively explain important steps; that well-designed visualization interventions have a positive overall effect in mathematics; and that excessive/redundant explanation can add unnecessary cognitive load. These findings support purposeful representations, modular decomposition and selective prompting — not page inflation.

Relevant research:

- Schoenherr, Strohmaier & Schukajlow (2024), *Educational Research Review*, visualization meta-analysis: https://doi.org/10.1016/j.edurev.2024.100639
- Renkl (2002), *Learning and Instruction*, worked examples + instructional/self explanations: https://doi.org/10.1016/S0959-4752(01)00030-5
- Chi et al. (1989), self-explanations and example-independent knowledge: https://doi.org/10.1016/0364-0213(89)90002-5
- Booth et al. (2024), explanation prompts in mathematics: https://doi.org/10.1016/j.jmathb.2024.101192
- Gerjets et al. (2006), modular worked examples and redundancy risk: https://doi.org/10.1016/j.learninstruc.2006.02.007

The `10 / 20 / 30` page ceilings and EASY/MEDIUM/HARD minimum research obligations are owner product-design rules, not empirical claims that those exact page counts are optimal.

## Publication gate

Deterministic Publication remains downstream. Before publication is frozen, the architecture must demonstrate:

- Core1A/Core1B bucket-depth behaviour for EASY, MEDIUM and HARD;
- optional research at EASY is either absent or fully bound;
- required research at MEDIUM/HARD is fully bound;
- promoted research decisions have complete claim coverage;
- retained category-relevant evidence is classified and contradictions are resolved;
- production promotion does not rely on LOW-confidence pedagogy claims;
- Core2A/Core2B generation with a real knowledge percentage;
- Core2A/Core2B generation with an explicit owner waiver;
- calibration of Core2A question demand as well as Core2B transfer demand;
- no drift in mathematical authority, source-question identity or answer verification.
