# IOQM Grade 9 - ALG-07 Floor, Ceiling & Discrete Functions

Status: `WAVE0_ARCHITECTURE_FROZEN`

## Learner entry model

Assume the learner can order real numbers and solve routine linear/quadratic equations, and may have seen the greatest-integer symbol informally. The unstable links are endpoint control, negative inputs, floor/ceiling as interval encoders, and the switch from a real interval to an integer solution set.

## Governing router

Before calculating, ask:

1. What integer value is the floor/ceiling expression claiming?
2. What **half-open interval** does that integer encode?
3. Which endpoint is included and which is excluded?
4. After solving the real interval, is the target real or integer?
5. Does a negative input make truncation intuition unsafe?
6. Is a shift/reflection identity cheaper than recomputing cases?

Compressed learner rule:

`DISCRETE VALUE -> HALF-OPEN INTERVAL -> CONTINUOUS CONDITION -> INTEGER FILTER -> ENDPOINT CHECK`

## Knowledge dependency map

| Node | Adaptation tag | Disposition |
|---|---|---|
| order on real numbers | `G9_CORE` | prerequisite retrieval |
| linear inequalities | `G9_CORE` | prerequisite retrieval |
| simple quadratic inequalities/factor sign where needed | `IOQM_BRIDGE` | minimal local bridge only |
| floor definition by inequalities | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| ceiling definition by inequalities | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| half-open interval endpoints | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| negative floor/ceiling behavior | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| integer translations and reflection | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| fractional part | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| floor/ceiling equations and inequalities | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| integer filtering/counting from real intervals | `IOQM_BRIDGE` | ALG-07 canonical teaching |
| general inequality optimization/equality doctrine | `DEFERRED` | canonical owner ALG-02 |

## Canonical ownership

ALG-07 owns:
- `floor(x)=n <=> n<=x<n+1`;
- `ceil(x)=n <=> n-1<x<=n`;
- endpoint discipline and negative inputs;
- integer shifts and `ceil(x)=-floor(-x)`;
- fractional part `{x}=x-floor(x)`;
- interval translation of floor/ceiling equations/inequalities;
- integer filtering/counting after interval solving.

ALG-02 remains canonical owner of general inequality methods, optimization, equality cases and attainment doctrine. ALG-07 uses only the minimum inequality manipulation needed to decode a discrete function.

## Method-selection map

| Similar surface | Route A | Route B | Discriminating question | First useful line |
|---|---|---|---|---|
| positive decimal | truncation happens to match floor | floor definition | Is the input negative or is a proof needed? | `n<=x<n+1` |
| negative decimal | truncation toward zero | floor toward `-infinity` | Which integer is the greatest one `<=x`? | locate x between consecutive integers |
| floor vs ceiling | left-closed/right-open | left-open/right-closed | Is the integer below or above the real number? | write the correct half-open interval |
| floor equation vs ordinary equation | interval family | single equality | Is the symbol preserving all decimals or collapsing a unit interval? | `floor(f(x))=n -> n<=f(x)<n+1` |
| real interval vs integer solutions | continuum | finite filter | Does the question ask for real x or integer x? | solve real interval, then intersect `Z` |
| endpoint included vs excluded | `<=` endpoint | `<` endpoint | Which side of the floor/ceiling definition is strict? | mark brackets before algebra |
| shifted input | case-by-case recomputation | integer translation identity | Is the shift an integer? | `floor(x+k)=floor(x)+k` |
| fractional part vs decimal digits | decimal-looking heuristic | `x-floor(x)` | Is x negative or nonterminating? | `{x}=x-floor(x)` |
| floor inequality | ordinary-looking inequality | integer threshold decoding | Is the comparison value an integer? | translate using the defining interval/order |

## Transfer map

- T2 representation: floor symbol -> half-open interval.
- T2 representation: fractional part -> integer part plus remainder in `[0,1)`.
- T3 context: integer timestamps/seat labels/levels counted inside a real interval.
- T3 context: digit constraints intersect a narrow floor-generated integer interval.
- T3 changed target: same floor equation, but integer-only solutions after real solving.
- T4 bridge: NT/COMB may use ALG-07 as a final discrete filter; they must not reteach floor theory.

## Required contrast set

1. floor vs truncation;
2. floor vs ceiling;
3. real interval vs integer solution set;
4. floor equation vs ordinary algebraic equation;
5. endpoint included vs endpoint excluded;
6. negative floor vs dropping the decimal part;
7. integer translation vs re-solving from scratch;
8. fractional part vs decimal part intuition;
9. floor-generated interval vs general inequality optimization.

## Exit belief

> "A floor or ceiling symbol does not destroy information randomly. It tells me exactly which half-open interval the input belongs to. I decode that interval first, then solve and filter."
