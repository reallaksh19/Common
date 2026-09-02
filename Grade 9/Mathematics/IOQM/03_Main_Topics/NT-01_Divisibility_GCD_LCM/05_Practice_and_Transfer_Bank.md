# NT-01 - Practice and Transfer Bank

All items here are author-created. Historical IOQM IDs are not assigned to them.

## F0 - Foundation repair

1. State whether `18|234` and justify with an integer quotient.
2. If `d|48` and `d|30`, show directly that `d|18`.
3. Compute `gcd(84,126)` and `lcm(84,126)`.
4. If `8|24` and `24|120`, state two consequences about divisibility and gcd/lcm.

## F1 - Direct recognition

5. Find the greatest integer giving the same remainder on 155 and 239.
6. Find the least positive integer divisible by 16, 20 and 24.
7. Use Euclid to compute `gcd(2025,748)`.
8. Find the least `N>7` leaving remainder 7 on division by 12, 18 and 30.
9. If `gcd(a,b)=12` and `lcm(a,b)=420`, determine `ab`.

## F2 - Standard structural use

10. Find the greatest integer giving the same remainder on 437, 581 and 725.
11. Find all positive integers `d` such that 305, 473 and 641 leave the same remainder on division by `d`.
12. Find the least `N>9` leaving remainder 9 on division by 12, 15 and 20.
13. Positive integers `a,b` have gcd 12 and lcm 420. List the possible unordered pairs `(a,b)`.
14. Find all positive integers `x` satisfying `6|x` and `x|72`.

## F3 - Disguised structure

15. If `d` divides both `7x+5y` and `3x+2y`, prove that `d|x` and `d|y`. Hence show that no `d>1` is possible when `gcd(x,y)=1`.
16. Three machines reset every 18, 24 and 40 minutes. They reset together at 09:00. When do they next reset together?
17. Suppose `d|(4n+7)` and `d|(7n+13)`. Determine all positive values `d` that can occur for some integer `n`.
18. Positive integers `a,b` have gcd 15 and lcm 900. Write `a=15u`, `b=15v` and list the possible unordered pairs `(a,b)`.
19. A ruler has marks at 1001, 1457 and 1913 mm. What is the largest positive step size `d` for which all three positions have the same remainder when divided by `d`?

## F4 - Preliminary-style transfer

20. Find the greatest `d` such that 1001, 1457 and 1913 leave the same remainder upon division by `d`.
21. Find the least positive integer `N` such that `N+5` is divisible by 18, 24 and 30.
22. A positive integer `d` divides both `11n+8` and `7n+5`. Find the largest possible value of `d` over all integers `n`.
23. Positive integers `a,b,c<=50` satisfy
   `27(lcm(a,c)+lcm(b,c))=26c(a+b)`.
   Let `x=gcd(a,c)` and `y=gcd(b,c)`. Re-derive the key restriction on `x,y` before any enumeration. Do not use the historical answer as a starting assumption.
24. A number `N` leaves remainder 5 when divided by 12 and 18, but remainder 0 when divided by 5. Find the least `N>5` satisfying all three conditions, or prove none exists.

## Transfer prompts

25. **Representation change:** express "`a` and `b` leave the same remainder when divided by `d`" using only divisibility language, without congruence notation.
26. **Context change:** explain why a largest equal-spacing problem and a first-synchronization problem usually route to different operations.
27. **Changed target:** two numbers have gcd 18 and lcm 630. Explain why the product is determined but the ordered pair need not be unique.
28. **Downstream bridge:** state exactly which divisibility fact a later modular-arithmetic chapter may retrieve when it writes `a` and `b` as having the same residue modulo `d`.
29. **WHY-NOT:** Why is lcm the wrong first move for "greatest divisor giving the same remainder on 437, 581 and 725"?
30. **WHY-NOT:** Why do `gcd(a,b)=12`, `lcm(a,b)=420` not force only the pair `(12,420)`?
