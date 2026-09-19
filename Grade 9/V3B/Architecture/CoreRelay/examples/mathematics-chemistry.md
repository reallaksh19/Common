# Mathematics and Chemistry transfer checks

Status: ILLUSTRATIVE DESIGN WALKTHROUGHS. All questions here are newly authored. No official examination provenance, agent execution, independent expert acceptance or learner result is claimed.

## Mathematics: roots and factors

### Scope, semantic spine and demand

ST-M-ROOT-FACTOR concerns a quadratic over the real numbers that is known to have real roots. Let a != 0 and f(x) = ax² + bx + c. If r is a root, f(r) = 0, and the factor theorem justifies x-r as a factor. For roots r and s, including a repeated root, f(x) = a(x-r)(x-s).

Core1 must retain the hypotheses and justification, rather than presenting root → sign change as a trick. Expansion yields:

a(x-r)(x-s) = a[x² - (r+s)x + rs].

Comparing coefficients gives r+s = -b/a and rs = c/a, where division is valid because a != 0. A quadratic without real roots needs a different real-domain account or an explicit extension to complex numbers; do not imply every real quadratic factors into two real linear factors.

Q-M-01: A monic quadratic has roots 2 and -3. Construct it and verify both roots.

D-M-01 preserves:
- Cue: roots supplied, polynomial requested.
- First useful move: make each factor zero at its stated root.
- Wrong chain: write (x+2)(x-3) by copying root signs.
- Dependency: substitution, zero product and distributive expansion.
- Correct route: (x-2)(x+3) = x² + x - 6, then substitute 2 and -3.
- Alternative: use sum=-1 and product=-6 to infer the coefficients, if those relations have been justified.
- SAFE: different known real roots.
- CONDITIONAL: nonmonic construction requires the leading coefficient; repeated roots require multiplicity interpretation.
- FORBIDDEN in current scope: claiming two specified roots uniquely determine a polynomial without degree/leading-coefficient constraints.

### Core1A assimilation

CT-M-01: move from seeing a root as a number to seeing it as an input making the whole expression zero.

Use a value table and two factor boxes as complementary representations. For x = 2, the factor x-2 equals zero; zero multiplied by any value gives zero. For x = -3, x+3 equals zero. This explains each sign without memorizing sign reversal.

| Input x | x-2 | x+3 | Product |
|---|---:|---:|---:|
| 2 | 0 | 5 | 0 |
| -3 | -5 | 0 | 0 |
| 0 | -2 | 3 | -6 |

Then expand in justified steps:
(x-2)(x+3) = x(x+3) - 2(x+3)  
= x² + 3x - 2x - 6  
= x² + x - 6.

The first two lines use distributivity; the last combines like terms. If distributivity is unprovided, it needs a bridge. A signed algebra-tile picture may help some learners, but a naive positive-area rectangle cannot faithfully represent all these negative terms. RR/RC/RD must record that risk rather than requiring a geometric illustration by default.

Recompose: each factor identifies an input that kills the product, and expansion expresses the same polynomial in coefficient form. A graph could show zero crossings after graph-reading prerequisites are provided; it is not needed to justify the factor theorem here.

Candidate T locators are the factor explanation, value table, expansion and justification above. They describe draft content only.

### Owner-directed Core2A

Elementary request despite high reported knowledge:
- Which expression becomes zero at x = 4: x-4 or x+4? Answer: x-4.
- If one factor in a product is zero, what is the product? Answer: zero.

Challenge request with appropriate bridges:
- A quadratic has roots 1 and 3 and value -6 at x = 2. Find it.
- Solution: f(x) = a(x-1)(x-3). At x = 2, -a = -6, so a = 6. Thus f(x) = 6x² - 24x + 18.
- Required new demand: infer a scale factor from an extra condition. This is conditional until the leading-coefficient role and substitution are supported.

Failure injection: an upstream packet says divide (x-2)(x+3)=0 by x-2 to obtain only x=-3. Fresh review must reject the loss of x=2: the divisor can be zero precisely at a solution. This is a domain/solution-preservation issue that a packet-count test would miss.

## Chemistry: coefficients, subscripts and conservation

### Scope, semantic spine and demand

ST-C-COEFF-SUBSCRIPT concerns interpreting a balanced equation using a simple particle model:

2H₂ + O₂ → 2H₂O.

The equation states stoichiometric proportions for the represented reaction. It does not by itself describe the sequence of elementary molecular events, reaction rate, energy changes, or practical experimental conditions.

Core1 distinguishes:
- H₂ denotes a molecule containing two hydrogen atoms.
- The coefficient 2 counts two such molecules in this particle interpretation, or a corresponding amount ratio at the macroscopic level.
- The subscript belongs to the species' composition.
- Balancing changes amounts/coefficient ratios while preserving the specified species identities.
- Atom counts here are four hydrogen and two oxygen atoms on each side.

Q-C-01: Why cannot we balance this equation by changing H₂O to H₂O₂?

D-C-01 preserves:
- First useful distinction: number of particles versus composition of each particle.
- Wrong chain: adjust any visible number until totals match.
- Correct response: changing the subscript changes water into hydrogen peroxide, a different chemical species; balancing must retain the intended species.
- Required representations: symbol parsing and a conserved-atom count.
- SAFE: scale all coefficients together and interpret counts.
- CONDITIONAL: limiting-reagent tasks require leftover-particle reasoning; ionic equations need charge/species conventions.
- FORBIDDEN in this slice: infer a collision mechanism directly from the balanced equation.

### Core1A assimilation

Start with a familiar grouping analogy: two packets containing two counters each contain four counters. Map packets to molecules and counters to atoms only for the counting distinction. A molecule is not literally a bag of freely interchangeable counters; chemical bonding and identity are outside that analogy.

Use a particle inventory with explicit legend before translating to symbols:

| Side | Represented particles | Hydrogen atoms | Oxygen atoms |
|---|---|---:|---:|
| Before | Two H-H groups and one O-O group | 4 | 2 |
| After | Two H-O-H groups | 4 | 2 |

The grouping notation is a schematic composition aid, not a claim about bond angles, relative atomic size or the reaction mechanism.

Now explain 2H₂: the coefficient says two molecules, each subscript says two H atoms, so total H atoms = 2 × 2 = 4. In 2H₂O, each of two molecules contains two H atoms and one O atom; totals are four H and two O.

Contrast H₂O with H₂O₂ explicitly. The extra oxygen inside each molecule changes its composition and identity. Balancing the amounts of specified substances cannot be done by replacing one of those substances without changing the stated reaction.

Core1A should bridge macro observations, particle models and symbols where the concept requires it. This example supplies particle/symbol counting, not a laboratory demonstration. Do not invent observed water formation or claim the drawing shows what an individual reaction event actually does.

### Owner-directed Core2A

Elementary request:
- How many H atoms are represented by one H₂ molecule? Answer: two.
- How many H atoms are represented by 3H₂ in the molecule-count interpretation? Answer: six.
- Does changing the coefficient in front of H₂O change each molecule's composition? Answer: no.

Conditional extension:
- In an ideal complete-reaction particle-count model, begin with four H₂ molecules and three O₂ molecules. How many H₂O molecules can form, and what remains?
- Each represented stoichiometric set consumes two H₂ and one O₂ to form two H₂O. Four H₂ permit two sets, consuming two O₂ and forming four H₂O. One O₂ remains.
- This is a stoichiometric accounting model under the explicit complete-reaction assumption, not a mechanistic description or an experiment recommendation.

Before that extension becomes ordinary supported practice, add and review the idea of a limiting amount and leftovers. If absent from T, Core2A must request that bridge or use the owner's explicit diagnostic/stretch mode. A harder-looking question alone does not justify the extension.

### Chemistry-specific failure injection

A draft visual draws all reactant molecules simultaneously colliding and labels that picture how the reaction happens. V should reject the mechanistic claim: the balanced equation and atom conservation do not establish that pathway. Correct the caption/drawing to represent accounting, retain the original rejected claim, and invalidate any explanation relying on it.

## What generalizes

Reuse provenance, exact bindings, owner control, 1–3-subtopic relay, claim-level validation and dependency-aware recovery across subjects. Keep subject reasoning distinct: physical models and frames; mathematical domains and equivalence; chemical species, conservation and representational levels.

A shared schema should permit these differences rather than forcing all three subjects into a Physics derivation vocabulary.
