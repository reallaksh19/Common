# COMB-03 - Source Coverage and PYQ Map

Status: `INTEGRATED_PRODUCTION_SOURCE_MAP_PASS`

Primary-count rule: use the frozen corpus primary owner. Secondary tags are bridge evidence only and do not inflate topic ownership.

| Stable ID | Year/Q | Verified answer | Primary mechanism | First structural move | Student use |
|---|---|---:|---|---|---|
| `IOQM-2024-Q14` | 2024 Q14 | `80` | deterministic sparse state evolution | work backward from the near-edge target; only one exceptional step can occur | source-linked transfer reference |
| `IOQM-2024-Q20` | 2024 Q20 | `10` | directed state graph / reverse search | invert `x->2x` and `x->x-3`; compare reverse branching | source-linked transfer reference |
| `IOQM-2023-Q08` | 2023 Q08 | `59` | tiling state decomposition | freeze the leftmost unresolved region and track special-square use | source-linked transfer reference |
| `IOQM-2023-Q21` | 2023 Q21 | `15` | residual/partition representation | compress the monotone function into a residual partition | source-linked representation contrast |
| `IOQM-2023-Q26` | 2023 Q26 | `19` | restricted binary representation / carry state | process binary digits with coefficient/carry memory | source-linked transfer reference |

All five are independently verified in the frozen answer-verification authority. No metadata-correction overlay event applies to these IDs.

## Source custody

- 2024 paper: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm-2024-english.pdf`
- 2024 key: `https://olympiads.hbcse.tifr.res.in/wp-content/uploads/2025/04/ioqm2024-answerkey.pdf`
- 2023 paper/key: `https://www.mtai.org.in/wp-content/uploads/2023/09/IOQM_Sep_2023_Question-paper-with-answer-key.pdf`

Historical stems/figures remain paper-controlled. The integrated learner book uses the stable IDs, mechanism fingerprints and verified answers; it does not silently rewrite a source stem.

## Mechanism fingerprints

### 2023 Q08 - tiling decomposition
A `2 x 7` tiling problem with dominoes and at most one `2 x 2` tile. The crucial move is leftmost decomposition plus enough state to remember whether the special tile has been used. Independent decomposition gives `21 + 38 = 59`.

### 2024 Q20 - reverse-state search
Starting from 11, the forward rules are doubling or subtracting 3. Reverse predecessors are halving when even and adding 3. Independent breadth/reverse search gives minimum distance `10`.

### 2024 Q14 - near-boundary sparse history
After 80 evolution steps, the target horizontal displacement is 79. The target itself implies exactly one non-right step; there are `80` positions for it. This is a canonical case where a huge state table is inferior to boundary compression.

### 2023 Q21 - representation before recurrence
A monotone integer function under a weighted constraint converts to a Ferrers/partition residual. Independent reduction gives a residual of 7 and `p(7)=15`. The point is to choose the smaller representation, not force recurrence.

### 2023 Q26 - carry state
Represent 100 using powers of 2 with at most two copies of each denomination. Coefficients `0,1,2` interact through local binary carry. Direct bounded-part DP and carry-state DP both give `19`.

## Coverage conclusion

The anchors cover five materially different decisions: first-step tiling recurrence, deterministic evolution, reverse search, recurrence-not-always-best representation, and carry/local-memory counting. The learner chapter therefore uses one state-first router rather than presenting COMB-03 as a Fibonacci-only topic.
