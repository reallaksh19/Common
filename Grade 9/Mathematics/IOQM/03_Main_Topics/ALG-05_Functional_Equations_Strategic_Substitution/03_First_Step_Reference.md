# First-Step Reference: Functional Equations

## Read the domain first

Write one word at the top of your work:

`integers` or `reals`.

Every substitution must stay there.

## Input-choice router

### Product or mixed argument

If you see `xy`, `mn+1`, `(x-1)y`, or another product-like argument:

**First question:** can one variable be 0 or 1 so the argument becomes a known constant?

### Return partner

If you see `f(c-x)` together with `f(x)`:

**First line:** write the same equation with `x` replaced by `c-x`.

Check that applying the replacement twice returns to `x`.

### Two companion values

If the equations contain the same two unknown function values:

**First line:** name them temporarily, then add/subtract/eliminate.

### Integer domain

If the equation contains `m+n`, `m-n`, or a shift:

**First question:** what do `0`, `1`, and `-1` produce?

A unit-step relation may propagate all integer values.

### Equal outputs

If you need to show equal outputs force equal inputs (the property later called injective):

**First line:** assume `f(a)=f(b)` and use the given equation to see whether it forces `a=b`.

### Every target output

If you need to show every target value occurs (the property later called surjective):

**First line:** take an arbitrary target `t` and try to construct an input whose output is `t`.

## Three contrasts

- Random substitution asks “what happens at 2?” Strategic substitution asks “what removes the product/partner?”
- A recurrence generates indexed terms. A functional equation relates a function at transformed inputs.
- A table suggests a formula. The original equation proves it.

## Stop checks

Before accepting a solution:
- all substitutions legal?
- any hidden division by zero?
- partner equation really equivalent?
- enough equations for the unknown function values?
- candidate checked on the full stated domain?
