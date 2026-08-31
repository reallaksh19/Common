# IOQM Grade 9 — ALG-04 Sequences, Progressions & Recurrences

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Scope boundary

ALG-04 is the canonical teaching owner for:
- sequence notation and indexing;
- term versus partial sum;
- AP/GP recognition from invariants;
- explicit versus recursive definitions;
- recurrence semantics and initialization;
- recurrence transformation;
- local/window subtraction;
- telescoping;
- high-index cancellation;
- simple neighboring-term invariants.

ALG-04 does **not** own recurrence derivation from counting states. `COMB-03` owns state definition, first-step decomposition, tilings, path/state counting and deterministic state evolution. ALG-04 exports only the recurrence-language and recurrence-manipulation interface needed downstream.

## Learner entry model

### PRIOR_KNOWLEDGE
The learner can usually:
- compute several terms of a sequence;
- use familiar AP/GP formulas;
- manipulate simple algebra.

### LIKELY_HALF_KNOWLEDGE
The learner may:
- treat `a_n` and `S_n` as interchangeable;
- call a sequence AP/GP from appearance rather than checking the invariant;
- see a recurrence as a command to iterate;
- omit initial conditions;
- use a global formula when a local subtraction is cheaper.

### MISSING_BRIDGES
- accumulated information -> isolate one term;
- recurrence -> dependency plus initialization;
- nearby-index comparison -> cancellation;
- high index -> transformed quantity/invariant;
- summand decomposition -> telescoping;
- algebraic recurrence -> counting-state recurrence boundary.

## Governing learner router

```text
TERM OR SUM?
    |
EXPLICIT OR RECURRENT?
    |
LOCAL RELATION OR GLOBAL FORMULA?
    |
CAN NEARBY RELATIONS BE SUBTRACTED?
    |
CAN THE EXPRESSION TELESCOPE?
    |
ONLY THEN COMPUTE TERMS
```

This router is the canonical teaching spine. AP/GP are useful local invariants inside it, not the organizing principle of the whole unit.

## Knowledge dependency map

```text
G9_CORE arithmetic + algebra + indexing
        |
        +--> sequence notation a_n
        |      |
        |      +--> term a_n vs partial sum S_n
        |      |        |
        |      |        +--> a_n = S_n - S_{n-1}
        |      |
        |      +--> local invariants
        |               +--> AP: constant first difference
        |               +--> GP: constant nonzero ratio
        |
        +--> explicit definition vs recursive definition
               |
               +--> initialization + index range
               |
               +--> verify candidate recurrence/explicit form
               |
               +--> shifted/nearby relation subtraction
               |        |
               |        +--> first-difference transforms
               |        +--> moving-window cancellation
               |
               +--> telescoping as repeated local cancellation
               |
               +--> neighboring-term invariant
                        |
                        +--> high-index collapse

STABLE ALG-04 RECURRENCE INTERFACE
        |
        +--> COMB-03 may retrieve notation/semantics/verification
             but must define the combinatorial state before writing a recurrence
```

## Representation inventory

| Representation | What it exposes | First move | Main condition | Nearby wrong choice |
|---|---|---|---|---|
| list of terms | local change | mark differences/ratios | ratio only when denominator nonzero | force AP/GP by appearance |
| explicit `a_n=f(n)` | direct index access | substitute requested index | domain/index valid | compute previous terms |
| partial sum `S_n` | accumulated structure | write `a_n=S_n-S_{n-1}` | treat `a_1` separately if needed | set `a_n=S_n` |
| recurrence | dependency | record order, range, initials | enough initialization | iterate before seeking structure |
| moving window | shared overlap | subtract adjacent windows | fixed positive window size | expand all averages |
| rational summand | neighboring cancellation | seek `F(k)-F(k+1)` | decomposition exact | label any rational sum telescoping |
| neighboring-term invariant | high-index compression | compare invariant at `n,n+1` | recurrence applies on index range | compute raw high-index terms |

## Method-selection boundaries

| Similar surface | Route A | Route B | Discriminating question |
|---|---|---|---|
| `a_n` vs `S_n` | term | partial sum | Is this one contribution or an accumulation? |
| pattern list | AP | GP | Is difference constant, or nonzero ratio constant? |
| formula for `a_n` | explicit | recursive | Does it use only `n`, or earlier terms? |
| high index | global explicit formula | local recurrence transform | Which representation exposes the target with least work? |
| two moving averages | compare full values | subtract adjacent windows | Do the windows share almost all terms? |
| recurrence | iterate | subtract shifted relations | Can neighboring copies cancel? |
| rational sum | ordinary summation | telescope | Can each term be an exact neighbor difference? |
| recurrence invariant | raw terms | transformed `D_n` | Does a nearby-term combination scale simply? |
| same recurrence notation | algebraic sequence | counting-state recurrence | Was the recurrence given algebraically or derived by partitioning objects/states? |
| deterministic state process | COMB-03 | adversarial game COMB-04 | Is there an opponent choosing moves? |

## Core invariant family

The shared structural idea is:

> Compare neighboring indices so that most of the information cancels and the target becomes local.

Instances:
- `S_n-S_{n-1}=a_n`;
- `W_{i+1}-W_i=a_{i+k}-a_i`;
- shifted recurrences can create a simpler recurrence for differences;
- `F(k)-F(k+1)` telescopes over a sum;
- a neighboring-term determinant can scale by one constant under a second-order recurrence.

## Transfer map

```text
T2 representation change:
partial sum formula -> individual term
recurrence -> first-difference sequence
product denominator -> difference of reciprocals

T3 context change:
rolling total/average -> entering term minus leaving term
machine readings -> recurrence invariant audit quantity

T4 cross-domain bridge:
given algebraic recurrence -> ALG-04 manipulates it
counting problem -> COMB-03 must first DEFINE STATE -> PARTITION -> RECURRENCE
```

## H3 -> H0 mastery map

Each major mechanism has:
- H3: first algebraic relation supplied;
- H2: structure/representation named;
- H1: only the recognition clue;
- H0: changed-surface independent item.

Every supported problem is first presented as an H0 attempt; hints are optional. Across the practice sequence, the maximum available support fades `H3 -> H2 -> H1 -> H0`.

## Stable recurrence interface exported downstream

COMB-03 may assume the learner understands:

1. **Notation** — `a_n` is a term indexed by `n`; a recurrence relates indexed terms.
2. **Semantics** — a recurrence is a rule valid on a stated index range, not a complete sequence until enough initial values are supplied.
3. **Initialization** — an order-`r` recurrence normally needs `r` independent starting values.
4. **Explicit vs recursive** — explicit gives `a_n` directly from `n`; recursive gives `a_n` from earlier terms/states.
5. **Verification** — check initial values, then prove the proposed terms satisfy the recurrence for every allowed index.
6. **Local cancellation** — write nearby-index copies and subtract or combine them before iterating.
7. **Ownership boundary** — ALG-04 can manipulate a recurrence after it exists; COMB-03 must justify a counting recurrence from a defined state and a disjoint, exhaustive decomposition.

Detailed interface: `Authoring/ALG04_Recurrence_Interface_v1.md`.

## Exit belief

> “I first identify the object and representation. If neighboring indices overlap, I try subtraction or cancellation before I calculate many terms.”
