# ALG-03 - First-Step Reference

## One topic-wide router

```text
REQUEST
  -> individual roots?          FACTOR / SOLVE
  -> symmetric root target?     VIETA
  -> root count/real behavior?  DISCRIMINANT
  -> shifted/transformed roots? TRANSFORM INPUT
  -> remainder/factor?          EVALUATE / DIVIDE
  -> high power modulo relation? REDUCE
  -> common root?               ELIMINATE
  -> CHECK
```

## Recognition atlas

| Target clue | First question |
|---|---|
| `alpha+beta`, `alpha beta`, symmetric powers | do coefficients already determine it? |
| number of real roots / repeated root | what is `Delta`? |
| roots shifted by `c` | should polynomial be `P(x-c)`? |
| divisor `x-a` | evaluate `P(a)`? |
| huge exponent + polynomial relation | what low-degree remainder class repeats? |
| two equations share root | can subtraction/combination lower degree? |

## Four mandatory contrasts

- solve roots vs use symmetric invariants;
- discriminant/root-count vs vertex/minimum;
- transformed roots vs shifted input;
- calculate high power vs reduce modulo a polynomial.
