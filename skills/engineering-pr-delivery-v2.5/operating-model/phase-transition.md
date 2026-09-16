# Phase transitions and Q1-Q5

A phase transition occurs when recomputed frontier moves into another phase. It requires a fresh incoming-phase question set derived from the new EP:
```text
Q1 Production path
Q2 Incoming engineering problem
Q3 Boundaries and invariants
Q4 Verification
Q5 First safe implementation slice
```
Questions reference incoming roadmap IDs, AC IDs, TEST IDs, INPUT IDs, production domains and Owner decisions. Reject packs that primarily test the previous phase. Same-phase progression does not require new Q1-Q5 unless technical/authority boundary materially changes.