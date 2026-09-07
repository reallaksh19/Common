# Exponents, Radicals and Logarithms: Protect the Domain Before You Transform

Many exponent, radical and logarithm problems look as if they require a clever trick. Usually the real difficulty comes earlier: choosing a representation that keeps the equation equivalent and remembering which values are legal.

The central habit is:

> **Domain first. Normalize next. Transform only when you know whether the move is reversible.**

A useful working loop is:

`DOMAIN -> NORMALIZE -> REPRESENT -> TRANSFORM -> CHECK`

## 1. Exponents are a representation choice

Expressions such as

`8^x`, `4^(x+1)`, and `2^(3x)`

may look different, but they all use the same base after normalization:

`8^x=2^(3x)`,

`4^(x+1)=2^(2x+2)`.

If an equation can be written with one positive base different from `1`, equal powers give equal exponents.

### Example

Solve

`8^(x-1)=4^(x+2)`.

Write both sides in base 2:

`2^(3x-3)=2^(2x+4)`.

So

`3x-3=2x+4`,

hence `x=7`.

A logarithm would work, but it is more machinery than the problem needs.

## 2. Exponent rules have conditions

For nonzero `a`,

`a^m a^n=a^(m+n)`

and

`a^m/a^n=a^(m-n)`.

Also

`a^(-n)=1/a^n`,

so a negative exponent silently introduces the condition `a!=0`.

For rational exponents, it is safest in this course to normalize with a positive base unless the expression is already known to be real. Do not use a familiar exponent law in a domain where the expression itself may be undefined.

## 3. Principal square roots are non-negative

The symbol `sqrt(u)` means the non-negative square root of `u`, so over the real numbers:

- `u>=0` is required;
- `sqrt(u)>=0`;
- `sqrt(x^2)=|x|`, not automatically `x`.

This sign convention controls almost every radical equation.

### Example

`sqrt((x-3)^2)=5`

means

`|x-3|=5`,

so

`x=8` or `x=-2`.

Writing `sqrt((x-3)^2)=x-3` would lose one solution and would be false whenever `x<3`.

## 4. Simplify radicals only when the domain permits it

If `u,v>=0`, then

`sqrt(uv)=sqrt(u)sqrt(v)`.

For example,

`sqrt(72)=sqrt(36*2)=6sqrt2`.

But do not split a square root across subtraction:

`sqrt(u-v)` is not `sqrt(u)-sqrt(v)` in general.

For instance,

`sqrt(9-4)=sqrt5`,

while

`sqrt9-sqrt4=1`.

This distinction becomes crucial in nested radicals.

## 5. Conjugates remove a difference of squares

When a denominator or expression contains

`a+b sqrt(c)`

or

`sqrt(p)+sqrt(q)`,

the conjugate changes the mixed radical expression into a difference of squares.

### Example

Simplify

`1/(sqrt5-sqrt2)`.

Multiply numerator and denominator by `sqrt5+sqrt2`:

`(sqrt5+sqrt2)/(5-2)`

`=(sqrt5+sqrt2)/3`.

The conjugate is useful because the product has a predictable structure. It is not a ritual to apply to every radical.

## 6. Nested radicals: name the inside before squaring

A nested radical such as

`sqrt(x-sqrt(x+a))`

contains two layers of domain information:

`x+a>=0`

and

`x-sqrt(x+a)>=0`.

Squaring immediately can hide these conditions.

A better first question is:

> What simple quantity can represent the inner radical or the expression left after one justified square?

### A structural example

Suppose

`sqrt(5+2sqrt6)`

has the form

`sqrt m+sqrt n`.

Squaring the proposed form gives

`m+n+2sqrt(mn)`.

So we want

`m+n=5`, `mn=6`.

Thus `{m,n}={2,3}` and

`sqrt(5+2sqrt6)=sqrt2+sqrt3`.

We matched structure instead of repeatedly squaring an equation.

## 7. Squaring: equivalence or implication?

If

`A=B`,

then certainly

`A^2=B^2`.

But the reverse is not always true: `A^2=B^2` allows `A=B` or `A=-B`.

So in general,

`A=B  =>  A^2=B^2`.

Squaring becomes reversible when both sides are already known to be non-negative:

`A>=0, B>=0` and `A=B`

is equivalent to

`A^2=B^2`.

### Example: an implication-only square

Solve

`sqrt(x+2)=x`.

The left side is non-negative, so any solution must satisfy `x>=0` and `x+2>=0`.

Now both sides are non-negative, so squaring is reversible on this restricted domain:

`x+2=x^2`.

Thus

`x=2` or `x=-1`.

The domain condition `x>=0` rejects `-1`, leaving `x=2`.

The original equation is the final authority.

## 8. Do not cancel a sign condition

Suppose an equation is rearranged to

`sqrt(U)=V`.

Before squaring, write

`U>=0` and `V>=0`.

After squaring, solve

`U=V^2`

under those conditions.

This one habit prevents most extraneous-root errors.

## 9. Logarithms are exponents written backwards

For

`a>0`, `a!=1`, `b>0`,

`log_a b=t`

means exactly

`a^t=b`.

The logarithm is not a new kind of arithmetic object; it records an exponent.

### Example

`log_2 32=5`

because

`2^5=32`.

When a logarithm equation becomes simpler as an exponent relation, convert it.

## 10. The logarithm domain is part of the equation

For `log_a b` over the reals:

- base `a>0`;
- base `a!=1`;
- argument `b>0`.

These conditions must be written before algebraic manipulation if variables occur in the base or argument.

### Example

Solve

`log_(x-1) 8=3`.

The base conditions require

`x-1>0`, `x-1!=1`.

Convert to exponent form:

`(x-1)^3=8`.

So `x-1=2`, hence `x=3`.

But then the base is `2`, which is legal. Therefore `x=3` is valid.

## 11. Reciprocal logarithms

When both logarithms are defined and nonzero,

`log_a b * log_b a=1`.

A clean way to see this is to let

`t=log_a b`.

Then

`b=a^t`,

so

`a=b^(1/t)`,

and therefore

`log_b a=1/t`.

This substitution is often cheaper than applying several memorized logarithm identities.

## 12. Historical pattern: convert logs to an exponent relation

In `IOQM-2023-Q02`, set

`t=log_a b`.

Because the source has `a,b>=2`, both logs are legal and `t>0`. The relation becomes

`t+6/t=5`,

so

`t=2` or `t=3`.

Therefore

`b=a^2` or `b=a^3`.

The rest is an integer bound count. The logarithm disappears early because exponent form is the cheaper representation.

The lesson is:

> **When two reciprocal logarithms appear, compress them to one exponent variable.**

## 13. Historical pattern: a nested radical is not a difference of radicals

In `IOQM-2025-Q28`, the controlled equation contains

`sqrt(x-sqrt(x+a))`.

The inner radical is part of the radicand of the outer radical. It must not be flattened into

`sqrt(x)-sqrt(x+a)`.

The successful route is:

1. record the principal-root signs;
2. prove the integer `y` must be `0`;
3. square only after both sides are known non-negative;
4. reach `sqrt(x+a)=x-a`;
5. set the non-negative integer `t=x-a`;
6. obtain `a=t(t-1)/2`;
7. apply the bound and nonsquare condition.

The largest admissible value is `91`.

The lesson is:

> **Preserve the nesting, use the sign information, and turn the final radical into an integer parameter.**

## 14. Common base or logarithm?

Use a common base when both sides naturally become powers of the same positive base.

Use logarithms when:
- the variable is in an exponent and no convenient common base exists;
- a logarithm relation is already present;
- exponent comparison becomes simpler after taking logs and all positivity conditions are secure.

Do not introduce logarithms merely because an exponent appears.

## 15. A compact router

When you meet an exponent, radical or logarithm problem, ask:

1. What values are legal?
2. Is there a principal-root sign condition?
3. Can I normalize to a common base?
4. Is a conjugate exposing a difference of squares?
5. Is the radical nested? What should I name before squaring?
6. If I square, is the move `⇔` or only `⇒`?
7. Would exponent form be cheaper than logarithm form, or vice versa?
8. Are there integer restrictions to apply only after the main structure is solved?
9. Have I checked every candidate in the original condition?

The goal is not to perform more algebra. It is to keep every transformation legal and purposeful.
