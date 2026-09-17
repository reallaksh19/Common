# ALG-04 - First-Step Reference

This is a compression layer. Use it after the Assimilation Book.

## Master router

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

## Recognition atlas

| Visible structure | Ask | First useful line |
|---|---|---|
| `S_n` given, `a_n` asked | accumulation or term? | `a_n=S_n-S_{n-1}` |
| constant local change | difference or ratio? | compute `a_{n+1}-a_n` |
| repeated multiplication | ratio constant? | compute `a_{n+1}/a_n` |
| `a_n=f(n)` | explicit? | substitute requested `n` |
| earlier terms on RHS | recurrent? | write initials + valid index range |
| moving sums/averages | overlapping windows? | subtract adjacent windows |
| high-index recurrence | can a transform simplify? | write nearby-index copies |
| `k(k+1)` / `(k-1)k` | exact telescope? | seek `F(k)-F(k+1)` |
| squares/products of neighboring recurrence terms | invariant candidate? | compare candidate at `n,n+1` |
| tilings/paths/states | where did recurrence come from? | route state derivation to the later combinatorics chapter |

## AP / GP card

AP:
`a_{n+1}-a_n=d`.

GP:
`a_{n+1}/a_n=r` for nonzero terms.

Do not decide from appearance. Test the invariant.

## Recurrence interface card

### Notation
`a_{n+2}=F(a_{n+1},a_n)` relates indexed terms.

### Semantics
A recurrence is valid on a stated index range.

### Initialization
An order-2 recurrence normally needs two starting values.

### Explicit versus recursive
- explicit: `a_n=f(n)`;
- recursive: `a_n` depends on earlier terms.

### Verification
1. check all initial values;
2. substitute the candidate into the recurrence;
3. prove the equality for every allowed index.

### Local cancellation
Before iterating:
- write the relation at neighboring indices;
- subtract/combine;
- test a transformed sequence.

## Window card

For

`W_i=a_i+...+a_{i+k-1}`,

`W_{i+1}-W_i=a_{i+k}-a_i`.

Fixed-size averages have the same ordering as their sums.

## Telescoping card

Target form:

`u_k=F(k)-F(k+1)`.

Then the sum collapses to boundary terms.

## Neighboring-term invariant card

For

`a_{n+2}=p a_{n+1}+q a_n`,

try

`D_n=a_n^2-a_{n-1}a_{n+1}`.

Then

`D_{n+1}=-qD_n`.

Use only after deriving/checking it for the given recurrence.

## Contrast strip

- term vs partial sum;
- AP vs GP;
- explicit vs recursive;
- local relation vs global formula;
- direct iteration vs shifted-relation subtraction;
- ordinary rational sum vs true telescoping sum;
- raw high-index terms vs invariant;
- algebraic recurrence vs counting-state recurrence;
- deterministic state evolution vs adversarial game;
- checking examples vs verifying a recurrence.

## Fast checks

Before finalizing:
- Did I preserve the correct index?
- Did I state enough initial values?
- Did I divide by a quantity that could be zero?
- Did I prove the telescope decomposition?
- Did I use the recurrence only where it is valid?
- If the recurrence counts objects, was the state decomposition justified elsewhere?
