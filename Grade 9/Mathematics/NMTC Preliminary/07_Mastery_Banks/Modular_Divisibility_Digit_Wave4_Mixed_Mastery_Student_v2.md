# Modular, Divisibility & Digit Structures — Wave 4 Mixed Mastery
## Student paper — Grade IX/X competitive foundation

This paper is deliberately **unlabelled by method**. Do not ask “which chapter is this from?” Ask:

> What information matters, and what smaller representation preserves it?

Do not use the answer/diagnostic key until the full paper is complete.

---

# A. Recognition only — 20 prompts

**Instruction:** do not solve. Write only the first useful representation, legality check, or structural move.

1. `N` leaves remainder 7 when divided by 12.
2. `2x≡2 (mod6)` and a learner wants to divide by 2.
3. Find the last digit of `7^318`.
4. A power cycle has length 4 and the exponent is divisible by 4.
5. One number leaves remainder 5 when divided by 12,18,30.
6. One divisor leaves the same remainder on 84,129,174.
7. Solve `x≡1 (mod4)`, `x≡3 (mod6)`.
8. Decide whether `x≡1 (mod4)`, `x≡2 (mod6)` can have a solution.
9. A number is divided by 5; then its quotient is divided by 6; then that quotient is divided by 7.
10. A two-digit number with digits `a,b` is compared with its reversal.
11. A six-digit number has the repeated form `ABCABC`.
12. Count numeral choices subject to divisibility by 9.
13. Test a four-digit number `abcd` for divisibility by 11.
14. Find integers making `(n+8)/(n+2)` integral.
15. Positive integers satisfy `k^2-n^2=120`.
16. Positive coprime integers have a product that is a perfect square.
17. Count consecutive blocks whose sums are divisible by `m`.
18. Process a long decimal numeral one digit at a time modulo 7.
19. An odd prime `p` divides `3^4+1`.
20. A historical remainder problem and its keyed answer cannot both be correct under the same interpretation.

---

# B. First useful line — 12 prompts

**Instruction:** write the first mathematical line only. Do not finish unless you need a line to make the representation unambiguous.

1. “`N` leaves remainder 4 when divided by 7.”
2. Solve `4x≡8 (mod12)`.
3. Find the last digit of `7^222`.
4. Find the least `N>100` leaving remainder 5 on division by 12 and 18.
5. Find the greatest divisor leaving equal remainders on 84,129,174.
6. Solve `x≡1 (mod4)`, `x≡3 (mod6)`.
7. A two-digit number has tens digit `a`, units digit `b`, and its reversal is 27 larger.
8. Explain the built-in divisibility of `ABCABC`.
9. Determine positive `n` for which `(n^2+5n+10)/(n+2)` is an integer.
10. Positive integers satisfy `k^2-n^2=120`.
11. For a sequence `a1,...,an`, test whether a consecutive block sum is divisible by `m` without enumerating all blocks.
12. Process the decimal digits of 314159 modulo 7 without long division.

---

# C. Mixed solve / transfer — 18 items

No family labels are supplied.

1. Solve `9x≡12 (mod15)` as residue classes modulo 15.
2. Find `5^123 mod13` without expanding the power.
3. Find the least integer greater than 1000 that leaves remainder 7 when divided by 18,24 and 30.
4. Find the greatest positive divisor that leaves the same remainder on 178,250 and 322. Also find the common remainder.
5. Solve `x≡3 (mod8)`, `x≡7 (mod12)` and state the complete class.
6. Decide without brute force whether `x≡2 (mod6)`, `x≡3 (mod9)` has a solution.
7. A two-digit number has digit sum 13 and its reversal exceeds it by 27. Find the number.
8. Using digits `{0,1,4,5}` without repetition, how many three-digit numbers are divisible by 3?
9. Find all positive integers `n` for which `(n^2+5n+10)/(n+2)` is an integer.
10. How many positive integer pairs `k>n` satisfy `k^2-n^2=120`?
11. How many ordered coprime positive pairs `(a,b)` satisfy `ab=900`?
12. For the sequence `3,1,4,1,5`, count the nonempty consecutive blocks whose sums are divisible by 4.
13. Process `271828` digit by digit and find its remainder modulo 11.
14. A game score is made only from 6-point and 10-point events. Can a total of 46 be formed using nonnegative numbers of events? If yes, exhibit one construction; if not, prove impossibility.
15. Find the least odd prime divisor of `3^4+1`, using the power-congruence structure before direct factor testing.
16. A machine has 12 states numbered `0,...,11`. Starting at state 4, each move advances 17 states cyclically. What state is reached after 100 moves?
17. Let `ABC` be any three-digit integer. Which of `7,11,13` must divide the repeated-block number `ABCABC`? Justify structurally.
18. You discover that a historical remainder stem, a repository summary, and the keyed answer cannot all describe the same mathematical problem. What must happen before that item is used as a canonical solved student anchor?

**Transfer classification note for teachers, not for solving:** items 8 and 12–18 intentionally change surface form rather than merely swap numbers from the teaching examples.

---

# D. WHY-NOT — 6 contrast items

For each, identify why the tempting move is invalid or inferior and state the safer first move.

1. Why not cancel 6 immediately from `6x≡9 (mod15)` while keeping modulus 15?
2. Why not reduce exponent 173 modulo 10 when finding `7^173 mod10`?
3. Why not use an LCM whenever the words “same remainder” appear?
4. Why not treat digits 0 and 9 as one choice merely because they are congruent modulo 9?
5. Why not count every positive factor pair of 120 after writing `(k-n)(k+n)=120`?
6. Why not rewrite `NMTC-BH-P-2024-Q20` into a clean CRT problem merely because that would fit a familiar method and one published answer?

---

# E. State / digit / high-ceiling check — 4 items

1. Digits are chosen from `{0,3,6,9}`, repetition allowed. How many three-digit numbers are divisible by 9?
2. Prefix residues modulo 4 are `0,1,3,1,0,3,1`. How many index pairs have equal residue?
3. Process the decimal digits of `314159` left-to-right using `r'≡10r+d (mod7)`. Find the final remainder.
4. Find the least odd prime divisor of `3^4+1`. Explain what the congruence `3^4≡-1 (mod p)` says about the return-to-1 cycle before testing the prime.

---

# F. Self-check

After the paper, mark each error by the **first failed decision**, not only the final answer:

- representation chosen;
- legality/admissibility checked;
- first move correct;
- arithmetic correct;
- original conditions rechecked;
- source custody respected.

`END OF STUDENT WAVE-4 PAPER`
