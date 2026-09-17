# Inequalities, Bounds & Equality Conditions - First-Step Reference

## One-question router

> **What exactly must be solved or made extreme, over which domain, and in which direction?**

```text
REQUEST -> DOMAIN -> REPRESENTATION
        -> [INTERVAL / BOUND]
        -> CONDITIONS -> ATTAINMENT / INTEGER FILTER -> CHECK
```

## Recognition atlas

| Visible structure | First useful question |
|---|---|
| `|x-a|<d` or `|x-a|<=d` | what interval around `a` does the distance condition describe? |
| `|x-a|>d` or `|x-a|>=d` | what two outside rays remain? |
| nested `||x|-k|<d` | can I remove the **outer** absolute value first and then solve for `|x|`? |
| integer solutions of an absolute-value inequality | what is the real interval/union first, then which integers lie in it? |
| quadratic expression | complete square? |
| positive terms with fixed product | AM-GM for lower bound? |
| fixed positive sum, product target | upper bound at balance? |
| reciprocal sum + fixed sum | Engel/Cauchy justified? |
| integer domain | where is real optimum, then which nearby integers? |
| strict domain / excluded equality point | is the bound attained? |
| root-existence request | route to the polynomial/root-feasibility method? |

## Absolute value = distance

For `d>=0`:

- `|u|<d`  iff  `-d<u<d`;
- `|u|<=d` iff  `-d<=u<=d`;
- `|u|>d`  iff  `u<-d` or `u>d`;
- `|u|>=d` iff  `u<=-d` or `u>=d`.

If `d<0`, check feasibility before manipulating: `|u|<d` and `|u|<=d` have no solutions, while `|u|>d` and `|u|>=d` are automatically true for every real `u` when the comparison permits it.

### Nested absolute value

For

`||x|-k|<d`,

first write

`-d < |x|-k < d`,

so

`k-d < |x| < k+d`.

Now solve the condition on `|x|`.

Let `L=k-d` and `U=k+d`.

- If `U<=0`, there are no solutions because `|x|>=0`.
- If `L<=0<U`, the condition reduces to `|x|<U`, hence `-U<x<U`.
- If `0<L<U`, then `L<|x|<U`, hence `-U<x<-L` or `L<x<U`.

For non-strict inequalities, change endpoints carefully rather than memorizing a new rule.

### Integer counting discipline

Do **not** count integers until the real solution set is correct. Then count each interval/union component, checking whether `0` is included and whether endpoints are strict or closed.

Example:

`||x|-2020|<5`

becomes

`2015<|x|<2025`.

Thus `|x|` may be any integer from `2016` through `2024`: 9 positive magnitudes, each giving two values of `x`, so there are `18` integer solutions.

## Equality checklist for optimization

1. What equality condition does the inequality require?
2. Does that condition satisfy every original constraint?
3. Is the equality point in the requested domain?
4. If not, is there another equality case?
5. If no equality is attainable, state bound/infimum/supremum correctly rather than inventing a minimum/maximum.

## Mandatory contrasts

- absolute-value interval solving vs optimization;
- one interval vs two outside rays;
- real solution set vs integer counting;
- lower bound vs minimum;
- upper bound vs maximum;
- real optimum vs integer optimum;
- inequality optimization vs discriminant/root feasibility.
