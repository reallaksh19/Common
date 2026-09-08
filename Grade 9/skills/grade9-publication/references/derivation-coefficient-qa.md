# Derivation and Coefficient-Reading QA

Use this checkpoint set whenever a student-facing batch contains an algebraic derivation whose intermediate transformations are part of the teaching, or a standard-form coefficient map such as motion equations.

## AD-33 DERIVATION-CHAIN INTEGRITY

A derivation is core instructional data, not merely a way to obtain the final formula. Preserve the complete reasoning chain in the same logical order supported by the source.

Check that:

- every source-supported starting relation remains visible;
- substitutions are shown before the expression they create;
- algebraic identities used by the source remain explicit where they carry teaching value;
- no intermediate transformation is silently skipped merely to save space;
- the final equation is not presented as if it were a new independent law when the source explicitly rebuilds it from earlier ideas;
- each displayed line is complete and legible at normal view;
- arrows/connectors or numbering make the order of transformations unambiguous;
- duplicated extraction artifacts are not mistaken for separate source obligations, but genuine repeated instructional statements are preserved.

For a derivation such as the time-free motion relation, the semantic chain should be auditable as:

```text
v = u + at
-> t = (v-u)/a
s = ((u+v)/2)t
-> substitute t
-> multiply (u+v)(v-u)
-> difference of squares v^2-u^2
-> 2as = v^2-u^2
-> v^2 = u^2 + 2as
```

Fail if the publication shows only the starting and final formula while dropping source-supported intermediate reasoning.

## AD-34 COEFFICIENT-MAP INTEGRITY

When students read physical quantities from a standard-form equation, the coefficient-to-meaning map must be exact.

For the constant-acceleration position form:

```text
x(t) = x0 + ut + 1/2 at^2
```

verify that the student-facing mapping preserves:

- constant term -> initial position x0;
- coefficient of t -> initial velocity u;
- coefficient of t^2 -> a/2, so acceleration is twice the t^2 coefficient;
- sign of u and a as directional information under the chosen axis;
- the condition that the shortcut applies to the quadratic constant-acceleration form, not to arbitrary polynomials;
- the anti-trigger that a t^3 or other non-quadratic term requires a different model;
- any follow-on use of v = u + at occurs only after u and a have been correctly read.

Fail if the page visually suggests `coefficient of t^2 = a`, omits the factor 1/2, or lets a generic polynomial be treated as constant acceleration without the source-supported model gate.

## AD-35 DERIVATION / MAP DENSITY AND FLOW

Do not scatter a short derivation or coefficient map across large isolated cards with accidental empty lower-page space. Use the page to show the cognitive route.

Pass when:

- the eye can follow the derivation in one continuous scan;
- the standard-form equation is visually dominant on a coefficient-reading page;
- meaning labels sit close to the corresponding mathematical terms;
- explanatory notes support the equation rather than visually overpowering it;
- unused space is purposeful, such as a learner work zone, not an artifact of fixed-height layout.

## Required review sequence

1. Freeze the ordered derivation or coefficient semantic manifest before layout.
2. Render the page at normal viewing size and at 100%.
3. Read every equation line in order; verify no skipped or clipped transformation.
4. For coefficient maps, point to each visible coefficient and state the physical quantity it maps to; compare with the source manifest.
5. Run the normal overlap, bounds, formula-completeness and math-typography checks.
6. Record `derivation_chain_findings = 0` and `coefficient_map_findings = 0` before release.
