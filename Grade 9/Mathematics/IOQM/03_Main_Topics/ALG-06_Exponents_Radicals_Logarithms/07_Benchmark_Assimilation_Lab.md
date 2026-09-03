# Benchmark Assimilation Lab — Exponents, Radicals and Logarithms

Use this after the Assimilation Book and before the final mastery test. It checks whether the topic has become usable, not merely familiar.

Learning loop:

`RECONNECT -> DIAGNOSE -> ADOPT -> TRANSFER`

## A. RECONNECT — no notes

Write only the first useful line unless a short answer is requested.

1. Simplify `sqrt(x^2)` over the reals.
2. For `sqrt(2x-1)=x-2`, what sign/domain facts must be written before squaring?
3. Which is the cheaper first route for `8^(x+1)=4^(2x-1)`: common base or logarithms?
4. What is the conjugate of `sqrt7-sqrt3`, and why is it useful?
5. State the real-domain conditions for `log_(x-1)(x+2)`.
6. In `sqrt(x-sqrt(x+a))`, which error would be made by writing `sqrt x-sqrt(x+a)`?
7. If `t=log_a b`, what is `log_b a` when both logs are defined?
8. If squaring an equation produces two candidates, what remains to be checked?

Diagnostic interpretation:

- misses 1-2 -> principal-root/sign bridge is weak;
- misses 3 -> representation choice is weak;
- misses 4 -> conjugate/difference-of-squares bridge is weak;
- misses 5 or 7 -> logarithm-domain/exponent bridge is weak;
- misses 6 -> nested-radical representation is weak;
- misses 8 -> equivalence/checking discipline is weak.

## B. Error laboratory

For each proposed solution, identify the **first invalid or inefficient move** and repair it.

### Error 1 — square-root sign loss

Claim: `sqrt((x-5)^2)=x-5`.

Repair target: state the correct expression and when the claimed simplification would become valid.

### Error 2 — automatic squaring

Claim: from `sqrt(x+3)=1-x`, immediately square to `x+3=(1-x)^2` and keep every quadratic root.

Repair target: record the missing sign condition before deciding whether squaring is reversible.

### Error 3 — flattening a nested radical

Claim: `sqrt(x-sqrt(x+a))=sqrt x-sqrt(x+a)`.

Repair target: explain why the outer radicand must be preserved as one object.

### Error 4 — logarithm before domain

Claim: solve `log_(x-2)(x+1)=2` by writing `(x-2)^2=x+1` first.

Repair target: write the three log-domain checks first.

### Error 5 — unnecessary logarithms

Claim: solve `9^x=27` by taking logarithms.

Repair target: choose the smaller representation.

### Error 6 — integer search too early

Claim: if an equation contains integer variables and radicals, start trying integer values before reducing the radical structure.

Repair target: state the correct order of operations.

## C. ADOPT — first move only

Do not solve fully. Write the first two useful lines.

1. `sqrt(3x+4)=x`.
2. `1/(sqrt13-sqrt5)`.
3. `sqrt(17+4sqrt15)`.
4. `log_(x-1) 27=3`.
5. `log_a b+2log_b a=3`, with `a,b>1`.
6. `16^(x-1)=8^(x+2)`.
7. `sqrt(x-sqrt(x+6))=2`.
8. A radical equation has already been squared once; one side before the second square is `x-4`. What must be checked?

## D. TRANSFER — changed surface

These are not number swaps of the earlier examples.

1. A quantity `u` is known to satisfy `u>=0` and `u^2=11-6sqrt2`. Decide whether a conjugate-style square recognition is useful before taking another square root.
2. Positive integers `a,b<=100` satisfy `log_a b+log_b a=5/2`. Turn the logarithm statement into a finite exponent/counting problem.
3. An equation contains `sqrt(P(x))=Q(x)` where `Q(x)` changes sign. Explain why solving the squared polynomial alone cannot be the final method.
4. A nested radical equation eventually gives `sqrt(N)=k+m sqrt a`, where `N,k,m,a` are integers and `a` is nonsquare. What invariant can separate rational and irrational parts?
5. A variable occurs only in exponents, but both sides are powers of 6 after factorization. Explain why logarithms are mathematically valid but strategically inferior.
6. Construct a simple equation where squaring is genuinely reversible because both sides are already known non-negative.

## E. Six-question assimilation test

Choose one problem from Section D and answer all six questions in words before completing algebra.

1. **What did you notice?** Name the visible structural clue.
2. **Why does the method work?** State the invariant or equivalence condition.
3. **What clue would make you think of it again?** Give a future recognition cue.
4. **What similar-looking situation needs a different method?** State one contrast pair.
5. **Can you write the first two useful lines without help?** Write them.
6. **Can you solve a disguised version?** Change the surface while preserving the same invariant, then outline the route.

## Readiness rule

You are not ready merely because you can reproduce a worked example. You are ready when you can protect the domain, choose the smallest representation, explain why a transformation is legal, reject a tempting near-miss, and start a disguised problem without a method label.
