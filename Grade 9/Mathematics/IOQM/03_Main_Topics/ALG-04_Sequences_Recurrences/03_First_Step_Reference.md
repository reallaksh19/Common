# ALG-04 — First-Step Reference

## Recognition atlas

| Visible clue | First move |
|---|---|
| partial sums `S_n`, asked for `a_n` | `a_n=S_n-S_{n-1}` |
| constant first difference | AP |
| constant nonzero ratio | GP |
| moving sums/averages | subtract adjacent windows |
| high-index recurrence | search transformed sequence/invariant |
| denominator `k(k+1)` or `(k-1)k` | partial fractions / telescope |
| tilings/paths/states | COMB-03 model, ALG-04 recurrence notation bridge |

## Quick router

```text
TERM or SUM?
  -> sum given, term asked -> difference adjacent sums

LOCAL pattern?
  -> constant difference -> AP
  -> constant ratio -> GP

WINDOW?
  -> subtract shifts

RECURRENCE?
  -> transform before brute force

SUM with neighboring factors?
  -> telescope
```

## First-step cards

### Partial sums
`a_n=S_n-S_{n-1}`.

### Window
`W_{i+1}-W_i = entering term - leaving term`.

### Recurrence
Write adjacent-index copies or transform to differences.

### Telescoping
Try to express each summand as `F(k)-F(k+1)`.

## Contrast strip

- AP vs GP;
- term vs sum;
- explicit formula vs recurrence;
- algebraic recurrence vs counting-state recurrence;
- compute-many-terms vs find-cancellation.
