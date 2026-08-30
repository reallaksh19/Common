# IOQM Grade 9 — ALG-04 Sequences, Progressions & Recurrences

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Learner entry model

Assume the learner remembers AP/GP formulas and can generate terms, but may confuse:
- a term with a partial sum;
- an explicit formula with a recurrence;
- a recurrence with a command to compute many terms;
- an algebraic sequence problem with a counting-state recurrence.

## Governing idea

> A sequence problem becomes easier when you identify what changes locally: consecutive differences, consecutive ratios, shifted windows, or an invariant combination of nearby terms.

## Knowledge dependency map

```text
G9 arithmetic + algebra
      |
      +--> term notation / index meaning
      |      |
      |      +--> AP: constant first difference
      |      +--> GP: constant ratio
      |      +--> partial sum vs term
      |
      +--> recurrence reading
             |
             +--> subtract shifted recurrences
             +--> finite/window differences
             +--> telescoping
             +--> invariant combinations

stable ALG-04 interface
      |
      +--> COMB-03 recurrence notation bridge
```

## Method-selection router

1. **Given consecutive terms?** Check difference, ratio, then other structure.
2. **Given partial sums `S_n` but asked for a term?** Use `a_n=S_n-S_{n-1}`.
3. **Given recurrence and asked for a high index?** Look for a transform/invariant before computing dozens of terms.
4. **Given moving sums/averages?** Subtract adjacent windows; most terms cancel.
5. **Given a sum of rational terms with consecutive factors?** Test partial fractions/telescoping.
6. **Problem counts tilings/paths/states?** COMB-03 owns the counting model; ALG-04 supplies recurrence language only.

## Canonical ownership

ALG-04 owns:
- AP/GP recognition and meaning;
- term-vs-sum distinction;
- algebraic recurrences;
- shifted-recurrence subtraction;
- telescoping sums;
- window-difference simplification;
- sequence invariants.

COMB-03 owns recurrence derived from counting-state decomposition.

## Transfer map

```text
moving sum/average -> subtract adjacent windows -> distant term inequality
recurrence -> transform nearby terms -> invariant / lower-order pattern
rational summand -> partial fractions -> cancellation -> boundary terms
```

## Mandatory contrasts

- explicit formula vs recurrence;
- term vs partial sum;
- arithmetic progression vs geometric progression;
- compute many terms vs transform the recurrence;
- algebraic recurrence vs counting-state recurrence.

## Exit belief

> “Before generating terms, I ask what cancels when I compare neighboring indices.”
