# 2. Restricted selections and committees

A committee or group is normally an **unordered selection**. Choosing \(A,B,C\) is the same committee as choosing \(C,A,B\).

That is why combinations appear:

\[
\binom nr=\frac{n!}{r!(n-r)!}.
\]

## 2.1 Paired restrictions

If objects come in pairs and the rule says “do not choose both,” first ask whether the problem actually forces exactly one from each pair.

If it does, each pair contributes 2 choices.

### Teacher example

There are four married couples. A team must contain exactly one person from each couple. The number of teams is

\[
2^4.
\]

No inclusion–exclusion is needed because the restriction has been built directly into the construction.

## 2.2 Conditional membership

Translate English conditions into logic before counting.

- “\(B\) serves only if \(C\) serves” means \(B\Rightarrow C\).
- “\(A\) refuses if \(B\) serves” means \(B\Rightarrow\neg A\).

A useful strategy is to split on the person who triggers the largest number of restrictions.

### Teacher example

A 3-person committee is chosen from \(A,B,C,D,E\), with \(A\) and \(B\) not allowed together.

Count all committees and subtract those containing both:

\[
\binom53-\binom31.
\]

The second term chooses the third member after \(A,B\) are already forced in.

## 2.3 Together or neither

A condition such as “\(A\) and \(B\) must either both be selected or both be omitted” creates two clean cases:

- both in;
- both out.

These cases are disjoint and exhaustive. Apply any other restrictions inside each case.

## 2.4 “At least”, “exactly” and “at most”

These phrases should immediately suggest different structures:

- **at least one** → often complement;
- **exactly one from each pair** → direct construction;
- **at most one from a pair** → choose neither or exactly one;
- **exactly \(k\) special objects** → choose those \(k\) first, then complete the group.

## 2.5 Restrictions inside categories

Suppose a committee must contain fixed numbers from two categories, such as 2 women and 3 men. Treat the category counts separately, but impose cross-category conditions in a careful case split if one person’s inclusion controls another person in the other category.

The safest order is:

1. choose the case-triggering person/status;
2. apply all consequences;
3. fill the remaining slots.

## What should I notice?

- committee/group/subset → order usually does not matter;
- paired objects → ask whether “one from each pair” is forced;
- “only if” → write the implication before counting;
- “together or neither” → two disjoint cases;
- fixed category totals → count within categories only after all logical restrictions are clear.

## Common mistakes

- treating “\(B\) only if \(C\)” as \(C\Rightarrow B\);
- using permutations for a committee;
- subtracting a forbidden pair without checking how many remaining members must still be chosen;
- counting “both in” and “at least one in” as disjoint cases;
- forgetting that exactly one from each of \(r\) independent pairs gives \(2^r\), not \(\binom{2r}{r}\).

## Appendix A practice

Questions **Q17, Q18, Q23**.
