# Functional Equations: Choose Inputs with a Purpose

A functional equation tells you something about the same function at several related inputs. The hard part is usually not algebra after the equations are written. The hard part is choosing the input that makes the structure collapse.

The central habit is:

> **Do not ask “which number should I try?” Ask “which input removes the most structure?”**

## 1. Start with the legal input set

Before substituting anything, read the domain.

If the equation is stated for all integers, then `0`, `1`, `-1`, and integer expressions are legal. If it is stated for all real numbers, a partner such as `3-x` is legal for every real `x`.

A substitution is invalid if it leaves the allowed input set.

## 2. Special values: make a complicated argument simple

Suppose an equation contains `mn+1`. One variable equal to 0 turns that argument into 1.

That is more useful than trying `m=2` merely because 2 is small.

### Example

For integers `m,n`, suppose

`F(m+n)=F(m)+n`

and `F(0)=4`.

Set `m=0`:

`F(n)=F(0)+n=n+4`.

One substitution determines the whole function on the stated integer domain.

The point is not that zero is magical. It is that zero collapses the structure.

## 3. Return-partner substitution

A transformation is especially useful when applying it twice returns to the original input.

For example,

`x -> 5-x -> 5-(5-x)=x`.

If an equation contains both `f(x)` and `f(5-x)`, write it once at `x` and once at `5-x`. This kind of self-reversing partner map is sometimes called an **involution**; the useful idea is the return, not the vocabulary.

### Example

For every real `x`,

`2f(x)+f(3-x)=x+9`.

Write the partner equation by replacing `x` with `3-x`:

`2f(3-x)+f(x)=12-x`.

Now the two unknowns are just `f(x)` and `f(3-x)`. Solve the 2x2 system:

`f(x)=x+2`.

The function was not guessed. It was forced by the pair.

## 4. Combine equations to eliminate a companion value

After you create a partner equation, the next move is ordinary algebra: add, subtract, or eliminate.

The algebra itself belongs to familiar equation solving. The new skill here is recognizing which second equation to manufacture.

### Example

Suppose

`f(x)+f(2-x)=10`

and

`f(2-x)-f(x)=2-2x`.

Add the equations:

`2f(2-x)=12-2x`.

Then `f(2-x)=6-x`, and substituting back gives

`f(x)=x+4`.

## 5. Integer-domain propagation: when a functional equation creates a step rule

On the integers, a substitution may create a recurrence-like step. That does not make the original problem a sequence problem.

### Example

For all integers `m,n`,

`f(m+n)=f(m)+f(n)+2mn`

and `f(1)=1`.

Set `m=0`:

`f(0)=0`.

Set `n=1`:

`f(m+1)=f(m)+1+2m`.

This step relation propagates through the integers. It suggests `f(m)=m^2`, and the original equation verifies it:

`(m+n)^2=m^2+n^2+2mn`.

The step relation is a consequence of the functional equation. The proof finishes in the original two-variable relation.

## 6. Functional equation vs recurrence

These two can look similar.

A recurrence such as

`a_(n+1)=a_n+2n+1`

defines or constrains an indexed sequence.

A functional equation such as

`f(m+n)=f(m)+f(n)+2mn`

constrains one function at many related inputs.

If the domain is integers, setting `n=1` can create a recurrence-like rule for `f(m)`. Use it, but remember where it came from and verify the final formula in the original equation.

## 7. A formula that fits values is only a conjecture

Suppose small calculations give

`f(0)=1, f(1)=2, f(2)=3, f(3)=4`.

The pattern `f(x)=x+1` is plausible. It is not proved.

A proof must show the rule holds for every allowed input, usually by:
1. deriving it directly from strategic substitutions, or
2. substituting a candidate into the original functional equation and proving it satisfies every condition.

Finite data cannot certify an all-input statement.

## 8. When equal outputs force equal inputs

First use the plain-language test: if `f(a)=f(b)`, can the equation force `a=b`? When this is true for all allowed inputs, the function is called **injective**.

Consider, for all real `x,y`,

`f(x+f(y))=f(x)+y`.

Suppose `f(a)=f(b)`. Then for any real `x`,

`x+f(a)=x+f(b)`,

so the left sides are equal. The equation gives

`f(x)+a=f(x)+b`,

hence `a=b`.

The equation itself proves the equal-output test; the word *injective* only names that result.

## 9. Constructing any requested output

Now ask a second plain-language question: given any real target `t`, can you build an input whose function value is `t`? If every target can be reached, the function is called **surjective**.

For the same equation,

`f(x+f(y))=f(x)+y`.

Set `x=0`:

`f(f(y))=f(0)+y`.

Given any target real number `t`, choose `y=t-f(0)`. Then

`f(f(y))=t`.

So every real target occurs as an output. The construction is the proof; the word *surjective* names the property afterward.

## 10. Domain checks matter in every method

Before each substitution ask:
- Is the chosen input allowed?
- If I cancel something, can it be zero?
- If I use the equal-output test, have I proved it?
- If I claim every target is hit, have I constructed an input?
- If I derived a formula from a few values, have I proved it for the whole domain?

## 11. Historical pattern: collapse first

In `IOQM-2025-Q14`, the equation is on the integers and contains `mn+1`. Setting one variable to zero makes the left side `f(1)`. The two asymmetric zero substitutions then determine the whole function immediately. Only after that does the finite sum matter.

The lesson is: **solve the function before summing its values.**

## 12. Historical pattern: pair the reflected input

In `IOQM-2024-Q16`, the equation relates `f(x)` and `f(3-x)`. Since the map `x -> 3-x` returns to `x` after two applications, the partner equation is automatic. Two equations, two companion values, then elimination.

The lesson is: **when the input transformation is self-reversing, write the partner equation before guessing the function.**

## 13. A compact router

When you meet a functional equation, ask in this order:

1. What inputs are legal?
2. Can 0, 1, or another simple value collapse an argument?
3. Is there a partner map such as `c-x` that returns to the original input?
4. Can I combine two equations to eliminate an unwanted function value?
5. On an integer domain, can one legal substitution create a unit-step rule?
6. Do I need to prove equal outputs force equal inputs, or construct an input for every target output?
7. If I see a pattern, what proves it for every allowed input?

Choose the input for structural payoff, not because it is numerically convenient.
