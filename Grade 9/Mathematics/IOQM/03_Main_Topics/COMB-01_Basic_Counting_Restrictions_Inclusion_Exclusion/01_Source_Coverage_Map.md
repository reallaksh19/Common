# COMB-01 - Source Coverage Map

All historical items below retain the frozen corpus ID, paper/key custody and independently verified answer. They are source anchors, not a claim of official topic frequency.

| Stable ID | Verified answer | Canonical mechanism here | Independent reconstruction |
|---|---:|---|---|
| `IOQM-2025-Q05` | 45 | restricted digit counting | for hundreds digit `a=1,...,9`, allowed tens digits number `10-a`; sum `9+...+1=45` |
| `IOQM-2025-Q15` | 40 | restricted injection / inclusion-exclusion | three coupon-pairs have allowed envelope sets of size 4 and distinct envelope choices; direct restricted-injection or IE count gives 40 |
| `IOQM-2025-Q18` | 40 | multiset permutations + complement/relative order | choose positions of two 2s in `C(9,2)=36`; among the remaining 3 threes and 4 fours, required final symbol is 3 in `C(6,2)=15` ways; `N=540`, remainder 40 mod 100 |
| `IOQM-2024-Q02` | 12 | position restriction + permutation | units digit is 1 or 3, then arrange remaining three digits: `2*3!=12` |
| `IOQM-2023-Q07` | 48 | symmetry-normalized arrangements | fix opposite faces 1,2; six cyclic orders of 3,4,5,6 around the axis and `2^3` opposite-pair colour choices give 48 |
| `IOQM-2023-Q17` | 66 | unordered subsets + order-statistic symmetry | for a uniform 5-subset of `1,...,99`, the expected fourth order statistic is `4*100/6=200/3`; requested floor is 66 |
| `IOQM-2023-Q20` | 43 | finite-set cardinality/max constraints + binomial counts | factor the two cardinality/maximum equations; count feasible subsets containing prescribed maxima; repository verification gives `N=439`, requested `4+39=43` |

## Source custody

### 2025 Q05/Q15/Q18
Paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/en.M1.pdf`
Key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/10/final-key-7th-September.pdf`
Authority: `HBCSE_OFFICIAL`; key status: `FINAL_OFFICIAL`.

### 2024 Q02
Paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf`
Key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf`
Authority: `HBCSE_OFFICIAL`; key status: `OFFICIAL_HBCSE_KEY`.

### 2023 Q07/Q17/Q20
Paper/key: `https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf`
Authority: `HBCSE_LINKED_MTAI`; key status: `HBCSE_LINKED_MTAI_EMBEDDED_KEY`.

Independent verification authority: `01_Corpus/Verification/IOQM_Independent_Answer_Verification_Batch_A_Q01_Q10_v1.md` and `...Batch_B_Q11_Q20_v1.md`.
