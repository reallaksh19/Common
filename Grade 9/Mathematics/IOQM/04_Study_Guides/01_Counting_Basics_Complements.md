# 1. Counting basics: stages, cases and complements

## The central idea

Before reaching for a formula, decide what one completed object looks like. Then ask whether you are building it in stages, splitting it into cases, or counting everything except a simpler forbidden class.

## 1.1 The multiplication principle

If a construction is made in successive stages and every completed object is obtained by making one choice at each stage, multiply the number of choices.

If a code has 3 choices for the first symbol and then 5 choices for the second, there are

\[
3\cdot5=15
\]

codes.

The important phrase is **successive stages**. Multiplication is not a formula to use automatically whenever two numbers appear.

### Teacher check

Ask yourself: after I choose at stage 1, have I counted the legal stage-2 choices correctly for that choice? If the second-stage count changes, either split into cases or sum the stage-dependent counts.

## 1.2 The addition principle

If valid objects split into non-overlapping cases, add the case counts.

For example, suppose a two-digit number must begin with 2 **or** 7. These cases cannot occur together, so count each case and add.

Before adding, ask:

> Can one valid object belong to two of my cases?

If yes, simple addition will overcount.

## 1.3 Complement counting

When the condition says

- at least one,
- not all,
- not none,
- at least one forbidden event occurs,

the complement is often shorter.

The pattern is

\[
\#(\text{wanted})=\#(\text{all})-\#(\text{unwanted complement}).
\]

### Teacher example

How many subsets of a 7-element set contain at least one of two distinguished elements \(a,b\)?

All subsets: \(2^7\).

Subsets containing neither \(a\) nor \(b\): choose freely from the other 5 elements, so \(2^5\).

Therefore the required count is

\[
2^7-2^5.
\]

Notice that the empty set is automatically included in the complement. There is no special correction.

## 1.4 Independent category choices

If a selection is made separately from independent categories, multiply the allowed counts for the categories.

Suppose there are 4 history books and 5 science books and we want at least one from each category. We have

\[
(2^4-1)(2^5-1)
\]

choices.

This is usually cleaner than applying inclusion–exclusion to the entire collection.

## 1.5 Inclusion–exclusion for two simple restrictions

If \(A\) is the set of objects violating one rule and \(B\) violates another, then

\[
|A\cup B|=|A|+|B|-|A\cap B|.
\]

So

\[
\#(\text{valid})=\#(\text{all})-|A|-|B|+|A\cap B|.
\]

This is especially useful for forbidden first/last positions or two overlapping membership restrictions.

## What should I notice?

- “at least one” → test the complement;
- “choose from each category” → count each category separately, then multiply;
- “first position / last position” → handle that restricted position early;
- “or” → check overlap before adding;
- two forbidden conditions → inclusion–exclusion may be shorter than casework.

## Common mistakes

1. Adding overlapping cases.
2. Forgetting the empty set when counting subsets.
3. Treating a leading digit like an ordinary digit.
4. Multiplying stage counts without checking whether later choices depend on earlier ones.
5. Subtracting two bad sets but forgetting to add their intersection back.

## Appendix A practice

Questions **Q3, Q4, Q24, Q28, Q54, Q56**.
