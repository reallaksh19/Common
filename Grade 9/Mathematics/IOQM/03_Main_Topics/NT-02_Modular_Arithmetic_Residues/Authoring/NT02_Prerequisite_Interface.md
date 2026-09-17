# NT-02 Stable Residue/Cycle Interface

main_topic_id: `IOQM-G9-NT-02`  
status: `FROZEN_V1_FOR_DOWNSTREAM_RETRIEVAL`  
canonical_teaching_owner: `IOQM-G9-NT-02`

## Prerequisites
- NT-01 divisibility meaning, `m|(a-b)`, gcd meaning/computation (retrieval only).
- G9 integer arithmetic and exponent basics.

## Concepts owned
1. congruence notation and same-residue meaning;
2. legal modular addition/subtraction/multiplication/powers;
3. inverses and cancellation legality;
4. power cycles and last-digit/last-two-digit reduction;
5. base-period + exponent-period coordination;
6. **Euler's theorem at bounded Grade-9 depth:** `gcd(a,n)=1 -> a^phi(n) congruent 1 (mod n)`, with minimal totient definition and mandatory coprimality check;
7. **Fermat's little theorem as a prime-modulus curriculum-design companion/corollary:** prime `p`, `p` not dividing `a` -> `a^(p-1) congruent 1 (mod p)`;
8. decision boundary between short visible cycles/order and theorem-based exponent reduction;
9. simultaneous congruences at Grade-9 depth;
10. collision criterion through congruent residues.

## Retrieval cues
- remainder/comparison -> congruence;
- huge powers -> reduce base and search for a short cycle first;
- coprime base/modulus with expensive cycle -> Euler may compress exponent;
- prime modulus with nonzero base -> Fermat may be the prime-modulus special case;
- final decimal digits -> choose 10/100/...;
- cancellation -> invertibility check;
- two congruences -> compatibility then combined period;
- distinct residues -> prevent divisibility of pairwise differences.

## First-move rules
- `a congruent b (mod m)` -> `m|(a-b)` when proof/check needed;
- huge power -> reduce base and list cycle before invoking a theorem;
- Euler -> explicitly verify `gcd(a,n)=1` before reducing exponent by `phi(n)`;
- Fermat -> verify prime modulus `p` and `p` not dividing the base;
- `cx congruent d` -> check gcd(c,m)=1 before inverse/cancellation;
- simultaneous constraints -> parameterize one residue class and test the other.

## Decision boundaries
- equality vs congruence;
- divisibility vs congruence;
- brute powers vs short cycles vs Euler/Fermat compression;
- coprime theorem case vs non-coprime base/modulus;
- legal vs illegal cancellation;
- mod10 vs mod100;
- compatible vs incompatible simultaneous congruences.

## Misconception traps
- treating congruence as equality;
- dividing residues as ordinary fractions;
- reducing an exponent by an unproved period;
- invoking Euler without `gcd(a,n)=1`;
- invoking Fermat when the modulus is not prime or the base is `0 mod p`;
- replacing an obvious short cycle with unnecessary theorem machinery;
- ignoring zero/non-coprime base cases;
- assuming every pair of congruences has a solution.

## Reusable identities / theorem bridge
- congruent quantities may be added/subtracted/multiplied and raised to positive integer powers;
- cancellation mod m is valid for a factor coprime to m;
- same residue iff modulus divides difference;
- decimal last k digits are residue mod `10^k`;
- `gcd(a,n)=1 -> a^phi(n) congruent 1 (mod n)`;
- prime `p`, `p` not dividing `a` -> `a^(p-1) congruent 1 (mod p)`.

## Downstream assumptions
NT-05 may retrieve modular reduction/power cycles and the bounded theorem bridge for digit/place-value applications where it is genuinely cheaper. COMB-04 may retrieve residue classes as invariant states. Neither should reteach the NT-02 canon.

`SOURCE_ANCHORS_CHECKED: PASS (25,31,42)`
`EULER_BRIDGE_STATIC_CHECK: PASS`
`FERMAT_COMPANION_STATIC_CHECK: PASS_DESIGN_ADDITION`
`DEPENDENCY_INVERSION: NONE`
`DOWNSTREAM_STATUS: READY_FOR_RETRIEVAL`
