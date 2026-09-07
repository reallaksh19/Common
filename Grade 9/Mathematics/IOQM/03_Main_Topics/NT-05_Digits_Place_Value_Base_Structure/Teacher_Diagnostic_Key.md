# Digits, Place Value & Base Structure - Teacher Diagnostic Key

## Historical anchor custody
- IOQM-2025-Q12: answer `33`; place value;divisibility;digit optimization; source status `CLEAN_OFFICIAL`.
- IOQM-2024-Q08: answer `49`; digit sums;carrying; source status `CLEAN_OFFICIAL`.
- IOQM-2024-Q18: answer `13`; concatenation;divisibility;gcd; source status `CLEAN_OFFICIAL`.
- IOQM-2023-Q19: answer `92`; digit product/sum;squarefree; source status `CLEAN_VALIDATED`.

## Practice bank
1. **100*a+10*b+c**
2. **a+b+c+d**
3. **d-c+b-a**
4. **3742**
5. **100*x+y**
6. **6**
7. **32**
8. **36**
9. **6**
10. **1**
11. **184**
12. **101101_2**
13. **b^2+1**
14. **(a+b) divisible by 9**
15. **yes**
16. **3**
17. **101*p**
18. **1001*x**
19. **2**
20. **no**
21. **no**
22. **73**
23. **2*a+2*b+c**
24. **basic counting**

## Mastery check
1. **23**
2. **14**
3. **10101**
4. **118**
5. **a+b+c+d divisible by9; -a+b-c+d divisible by11**
6. **no**
7. **1**
8. **b=a+c**
9. **100*123+y modulo(123+y)**
10. **5**
11. **9**
12. **1001**
13. **2a+2b+c divisible by9**
14. **1000_8**
15. **1,2,3,6,7 (but 6 excludes simultaneous2/3)**
16. **hand the 20-string counting to the counting method; do not rederive counting theory**

## Diagnostic routing
- Place-value error: write the numeral as a sum of digit coefficients times powers of the base before simplifying.
- Divisibility-by-9/11 error: reconstruct the rule from powers of 10 modulo 9 or 11; do not rely on a memorized pattern if the sign/order is unclear.
- Concatenation error: use the correct block power, for example concatenating a k-digit block y after x gives 10^k*x+y.
- Carry error: record how many trailing 9s are crossed; an increment changes digit sum by 1-9t when t trailing 9s reset.
- Digit-product error: translate the product into prime-exponent restrictions before enumerating digits.
- Counting boundary error: derive the arithmetic restriction here, then hand the admissible-string count to the counting method rather than rebuilding counting theory.
- Residue/cycle overreach: retrieve modular reduction when useful, but route generic modular-cycle work back to the modular-arithmetic topic.
When an answer is verbal/algebraic, require the stated restriction or representation, not merely an example numeral.
