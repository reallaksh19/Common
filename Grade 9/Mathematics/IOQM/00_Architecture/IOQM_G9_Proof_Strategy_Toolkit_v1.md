# IOQM Grade 9 — Proof Strategy Toolkit v1

Status: `V1_CROSS_TOPIC_BRIDGE`
Issue: `#132`

This is a **cross-topic bridge**, not a 23rd main topic and not a fifth IOQM domain. It exists so that proof habits are taught once, named consistently, and then retrieved inside Number Theory, Algebra, Geometry and Combinatorics.

The toolkit does not claim that IOQM has a separate official “proof theory” syllabus. It operationalizes the preparation requirement for basic proofs / proof strategies within the existing 22-topic architecture.

## Learner proof router

Use this seven-step card before writing a long argument:

1. **State the claim precisely.** What exactly must be shown or disproved?
2. **List the hypotheses.** Include domain, positivity, integrality, distinctness, coprimality, geometric incidence and selection rules.
3. **Choose a proof mode.** Use the cheapest mode that fits the logical shape.
4. **Write the decisive first line.** Translate the condition into the representation that preserves the needed structure.
5. **Preserve legality.** Track implication vs equivalence, reversible vs one-way moves, and theorem hypotheses.
6. **Close every required case.** Include equality cases, boundary cases, or a completeness argument when casework is used.
7. **Return to the original claim.** Verify the constructed object/candidate satisfies the original conditions.

## Canonical proof modes

### P1 — Direct implication
Start from the hypotheses and derive the target through valid implications.

Typical surfaces:
- divisibility rewritten as an integer equation;
- angle/ratio facts chained from proved geometry;
- algebraic identities transformed toward the requested expression.

### P2 — Equivalence discipline
Use `⇔` only when both directions are justified. If a step is only one-way, use `⇒` and validate candidates against the original condition.

Typical risks:
- squaring;
- multiplying/dividing by an expression of unknown sign or possible zero;
- clearing denominators;
- taking roots/logarithms;
- replacing a geometric condition by a necessary but not sufficient equation.

### P3 — Contradiction
Assume the negation of the target and derive an impossibility with a hypothesis, invariant, bound or established fact.

Use when the negation creates a stronger structural handle than the target itself.

### P4 — Contrapositive
To prove `A ⇒ B`, prove `not B ⇒ not A` when that direction exposes divisibility, parity, order or feasibility more cleanly.

Do not force contraposition when a direct proof is shorter.

### P5 — Counterexample to disprove
A universal claim is disproved by one legal counterexample. The example must satisfy every hypothesis and violate the conclusion.

“Several examples work” is not a proof of a universal claim.

### P6 — Finite exhaustive cases
Reduce to a finite list using structure first, then show the list is complete and check each remaining case.

A computer-like list without a completeness argument is not an olympiad proof.

### P7 — Extremal choice
Choose a largest, smallest, nearest, farthest, first or last object so that the extremal property forces a contradiction or a rigid relation.

This is retrieved heavily by COMB-05 and occasionally by NT/GEO problems.

### P8 — Invariant / monovariant
- **Invariant:** a quantity/state class does not change under legal moves.
- **Monovariant:** a quantity changes strictly in one direction and is bounded, forcing termination or excluding cycles.

This is retrieved heavily by COMB-04 and state-process problems.

### P9 — Construction vs obstruction
- **Existence:** exhibit a legal object/strategy and verify it.
- **Impossibility:** prove every legal object would violate a necessary condition.

Do not confuse “I found none” with an impossibility proof.

### P10 — Equality-condition closure
In inequalities/optimization, prove both the bound and that equality is attainable under the original constraints.

A numerical bound without an attainable equality case is not a completed maximum/minimum proof.

## “Example suggests” vs “proof establishes”

Examples are useful during DISCOVER, but they do not establish a universal theorem. The learner should be able to label a line as one of:

- observation/example;
- conjecture;
- proved implication;
- proved equivalence;
- counterexample;
- completed proof.

## First-line recognition table

| Surface clue | Proof question | Typical first line |
|---|---|---|
| `p | ab`, `p` prime | can divisibility be split across factors? | invoke/prove Euclid’s Lemma after checking primality |
| huge power modulo `n` | cycle or theorem? | reduce base; check coprimality before Euler/Fermat |
| “for every” / “always” | direct, contradiction, or invariant? | write the exact universal claim and hypotheses |
| “there exists” | construction or finite reconstruction? | state the object to build and all legality conditions |
| “impossible” | obstruction/invariant/contradiction? | state the necessary property that every legal state must preserve |
| maximize/minimize | bound + equality? | derive the bound, then identify the equality condition |
| finitely many integer cases | why is the list complete? | derive the bound/factorization/filter before enumerating |
| square/root/log transformation | reversible? | record domain/sign conditions before transforming |
| geometry diagram looks special | proved or visual? | state the missing theorem hypothesis/proof target |

## Topic retrieval contract

Main-topic packages should **retrieve** this toolkit rather than recreate a second proof chapter.

- Recognition/First-Line labs may ask for the proof mode or legality check where natural.
- Practice and mastery should require a short justification when the result is not self-validating.
- Teacher diagnostics may use the failure codes below.
- A topic may teach a specialized proof method only when it owns that mathematics.

## Diagnostic codes

- `HYPOTHESIS_DROPPED`
- `EXAMPLE_USED_AS_PROOF`
- `IMPLICATION_REVERSED`
- `ONE_WAY_STEP_TREATED_AS_EQUIVALENCE`
- `CASE_LIST_NOT_PROVED_COMPLETE`
- `COUNTEREXAMPLE_NOT_LEGAL`
- `THEOREM_HYPOTHESIS_UNCHECKED`
- `EQUALITY_NOT_SHOWN_ATTAINABLE`
- `VISUAL_PROPERTY_ASSUMED`
- `CONSTRUCTION_NOT_VERIFIED`
- `INVARIANT_NOT_SHOWN_PRESERVED`

## Scope boundary

This toolkit is not a formal logic course. It does not require symbolic logic notation, induction, advanced set theory, or abstract proof taxonomy unless a main topic/source genuinely needs them.

Classroom timing/readability, retention, psychometric calibration, qualification/pass-mark calibration and publication approval are evidence-dependent and remain `NOT_RUN` until separately measured.