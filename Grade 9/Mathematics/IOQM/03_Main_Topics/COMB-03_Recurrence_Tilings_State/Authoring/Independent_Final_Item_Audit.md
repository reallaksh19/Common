# COMB-03 Independent Final-Item Audit

Status: `PASS_STATIC_MATH_AFTER_CORRECTION`

The final learner wording was recomputed independently of the Teacher Key before PDF custody. One pre-custody mismatch was found and corrected: Mixed Mastery item 1 is `55`, not `89`, because a length-9 strip tiled by pieces of lengths 1 and 2 has sequence value `a_9=55` when `a_0=a_1=1`.

## Recurrence sequences

- length-1/2 tilings: `1,1,2,3,5,8,13,21,34,55,89`; practice targets `13,8,21,34` and mastery target `55` agree.
- length-1/3 tilings: `1,1,1,2,3,4,6,9,13,19,28`; targets `9` and `28` agree.
- `2 x n` domino-plus-square recurrence `v_n=v_{n-1}+2v_{n-2}`: `1,1,3,5,11,21,43`; targets `21` and `43` agree.
- compositions with parts 1/2 and no consecutive 2s: targets sum 8=`19` and sum 9=`28` agree with an independent two-state DP.

## Finite-state strings

- binary strings with no three equal consecutive bits: length 6=`26` by exhaustive finite-state check;
- binary strings with no consecutive 1s and even one-count: length 6=`11`, length 7=`17`, length 8=`27`; exhaustive enumeration and four-state DP agree;
- `{A,B,C}` length 6 with adjacent letters different and even A-count: `52`; direct enumeration and compressed state DP agree.

## Search items

Breadth-first search independently confirms:
- `1 -> 31` under `+1,*2`: minimum `8`;
- `1 -> 100` under `+1,*2`: minimum `8`;
- `2 -> 29` under `+3,*2`: minimum `5`;
- `1 -> 63` under `+1,*2`: minimum `10`.

## Representation counts

- partitions of 8 into distinct parts: `6`;
- partitions of 10 into distinct parts: `10`;
- 10 as powers of 2 with multiplicity at most 2: `5`;
- 18 as powers of 2 with multiplicity at most 2: `7`;
- four E and three N with no adjacent N: `C(5,3)=10`.

No promoted author-created numerical answer depends on an unverified historical key. After the mastery-item correction, all final learner items, Teacher Key answers and metadata answers agree.