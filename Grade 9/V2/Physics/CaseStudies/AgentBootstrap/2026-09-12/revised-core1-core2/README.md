# Motion in a Plane - Revised Core 1 and Core 2

This folder is the current handoff target for the Motion in 2D / Motion in a Plane case study.

## Frozen learner format

### Revised Core 1

Each concept page follows this learner grammar:

`physical picture -> What is happening? -> Key idea -> How it works -> Worked example -> Watch out -> Quick check + answer`

The chapter contains 22 concept families and an explicit Q1-Q59 review map. The concept surface covers the supplied theory plus the demands exposed by the complete numbered challenge bank.

### Revised Core 2 attempt pages

`question -> physics picture -> Hint 1 -> Hint 2 -> Hint 3 -> exactly two writing lines`

The hint system is now a **paired prompt + reveal contract**. Every hint must remain understandable even when revealed by itself.

For each hint rung:

1. **PROMPT** - an open-ended learner question that requires a cognitive action.
2. **REVEAL** - a directly matched concept clarification, representation, equation, state diagram, or small figure that answers only that prompt.
3. The reveal must not jump ahead to a later rung or resolve the final requested result.

The three rungs are:

- **Hint 1 - What is the key physics?** Ask about the decisive event, invariant, state, frame, direction, or physical condition. Reveal the physical interpretation/state only.
- **Hint 2 - How would you represent it?** Ask for the diagram, components, axes, frame, graph, geometry, or mathematical representation. Reveal that representation and its governing relation/figure only.
- **Hint 3 - What would you write first?** Ask for the first executable equation/constraint. Reveal that starting equation or construction only; do not solve it.

Robustness rule: `hint_prompt_i` and `hint_reveal_i` are authored as one semantic pair and validated together. A reveal that does not answer its own prompt is a publication failure. Later-rung information appearing in an earlier reveal is also a failure.

Attempt workspace is exactly two writing lines. Hint blocks are content-height; there are no large blank hint cards.

### Revised Core 2 worked pages

`question recap -> picture / known state -> reasoning ladder -> Answer -> Quick check -> Check it another way -> Watch out -> Review this idea`

The full reasoning ladder is frozen as:

1. UNDERSTAND
2. REPRESENT
3. CONNECT
4. CALCULATE
5. INTERPRET

Every rung must contain the actual physics of the item. The solution is **step-complete**: no algebraic, geometric, state-transition, substitution, or unit-bearing step needed by a Grade 9 learner may be silently skipped. Compactness comes from tighter layout and typography, not from deleting reasoning steps.

### Solution layout rules

- Smaller title/header footprint than earlier prototypes.
- Larger body mathematics and improved line spacing.
- Row height is content-driven; no fixed empty ladder rows.
- Representation figure and known-state panel must agree with the question.
- `CALCULATE` may use multiple lines and intermediate equations when the problem needs them.
- Answer block follows immediately after the ladder.
- Quick check and `Check it another way` must test the actual result; they are not substitutes for the answer.

## Answer requirement

All 59 numbered questions must have an explicit answer mapping. Quick checks and verification do not substitute for an answer.

## Source boundary

The rebuild uses the supplied `Motion in 2d(2).pdf` / `Motion in 2d.pdf`. The source scan is not redistributed in this handoff. Q49 and Q51 remain source-ambiguous because the supplied scan clips part of those items; missing wording must not be invented.

## Current implementation target

The next Core 2 revision must implement the paired prompt/reveal hint model across all 59 attempts and a step-complete solution ladder across all 59 solutions. The earlier Revised Core 2 PDF remains a regression fixture, not the final target.

Expected revised output filename:

- `physics-motion-2d-revised-core2-v2.pdf`

The generator and QA audit must travel with the PDF so a future agent can reproduce and validate the build.
