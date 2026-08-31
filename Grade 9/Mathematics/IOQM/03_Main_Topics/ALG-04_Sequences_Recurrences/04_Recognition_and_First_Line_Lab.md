# ALG-04 — Recognition and First-Line Lab

First attempt is H0. Write only the recognition statement or first useful mathematical line; do not finish the whole problem unless needed to justify the first move.

## Core recognition

1. `S_n=2n^2+3n`; asked for `a_n`.
2. `5,9,13,17,...`.
3. `3,12,48,192,...`.
4. `2,5,10,17,26,...`.
5. `a_n=4n^2-1`; asked for `a_100`.
6. `a_{n+1}=a_n+2n+1`, `a_1=1`; asked what information defines the sequence.
7. 5-term moving sums are strictly increasing.
8. 7-term moving averages are strictly decreasing.
9. `a_{n+2}=5a_{n+1}-4a_n`; look for a recurrence for first differences.
10. `sum 1/[k(k+1)]`.
11. `sum 1/(k^2+1)`.
12. `b_{n+2}=-4b_{n+1}-7b_n`; target contains `b_n^2-b_{n-1}b_{n+1}`.

## Close contrasts

13. A: `2,6,10,14,...`  
    B: `2,6,18,54,...`  
    State the local invariant that separates them.

14. A: `a_n=3n+1`  
    B: `a_{n+1}=a_n+3`, `a_1=4`  
    Which is explicit and which is recursive?

15. A: all 4-term sums are equal.  
    B: `S_n` is known explicitly.  
    Which nearby subtraction should be written in each case?

16. A: `1/[k(k+1)]`.  
    B: `1/(k^2+1)`.  
    Which one has an immediate neighboring-factor telescope?

17. A recurrence is supplied algebraically with two initial values.  
    A recurrence is claimed to count tilings.  
    What must be justified in the second problem that is not needed in the first?

18. A deterministic process has fixed transitions.  
    A two-player game has strategic choices.  
    Which neighboring topic owns the second structure?

## Verification recognition

19. A proposed formula matches the first five terms of a recurrence. What is still missing for verification?
20. A second-order recurrence is written with no initial values. What information is missing before it defines a unique sequence?
