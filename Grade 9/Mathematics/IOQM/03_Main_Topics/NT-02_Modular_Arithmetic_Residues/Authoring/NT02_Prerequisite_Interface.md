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
6. simultaneous congruences at Grade-9 depth;
7. collision criterion through congruent residues.

## Retrieval cues
- remainder/comparison -> congruence;
- huge powers -> cycle;
- final decimal digits -> choose 10/100/...;
- cancellation -> invertibility check;
- two congruences -> compatibility then combined period;
- distinct residues -> prevent divisibility of pairwise differences.

## First-move rules
- `a congruent b (mod m)` -> `m|(a-b)` when proof/check needed;
- huge power -> reduce base and list cycle;
- `cx congruent d` -> check gcd(c,m)=1 before inverse/cancellation;
- simultaneous constraints -> parameterize one residue class and test the other.

## Decision boundaries
- equality vs congruence;
- divisibility vs congruence;
- brute powers vs cycles;
- legal vs illegal cancellation;
- mod10 vs mod100;
- compatible vs incompatible simultaneous congruences.

## Misconception traps
- treating congruence as equality;
- dividing residues as ordinary fractions;
- reducing an exponent by an unproved period;
- ignoring zero/non-coprime base cases;
- assuming every pair of congruences has a solution.

## Reusable identities
- congruent quantities may be added/subtracted/multiplied and raised to positive integer powers;
- cancellation mod m is valid for a factor coprime to m;
- same residue iff modulus divides difference;
- decimal last k digits are residue mod `10^k`.

## Downstream assumptions
NT-05 may retrieve modular reduction/power cycles for digit/place-value applications. COMB-04 may retrieve residue classes as invariant states. Neither should reteach the NT-02 canon.

`SOURCE_ANCHORS_CHECKED: PASS (25,31,42)`
`DEPENDENCY_INVERSION: NONE`
`DOWNSTREAM_STATUS: READY_FOR_RETRIEVAL`
