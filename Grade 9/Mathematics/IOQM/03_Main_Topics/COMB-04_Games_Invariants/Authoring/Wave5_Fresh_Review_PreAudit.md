# COMB-04 Wave-5 Fresh-Review Pre-Audit

Status: `PASS_SECOND_PASS__FORMAL_WAVE5_GATE_BLOCKED_FRESH_REVIEWER_REQUIRED`

Scope: rigorous second-pass mathematics/source/pedagogy review performed after Wave 4, before render/PDF work.

## Reviewer-separation truth

The main-topic production authority requires **a fresh reviewer independently** to check every promoted answer and condition/source claim before `WAVE5_INDEPENDENT_QA_PASS` may be asserted.

The current custodian authored/materialized Waves 0–4. Therefore this record does **not** claim fresh-reviewer independence and does **not** set authored `answer_verified_independently=true`.

This pre-audit exists to expose defects early and give a fresh reviewer a complete, repository-local verification index. A future reviewer must recompute rather than merely copy the conclusions below.

Formal gate state: `G11_BLOCKED_FRESH_REVIEWER_REQUIRED`.

## Live reconciliation before review

- branch: `ioqm-g9-comb04-games`;
- production base: `grade9-ioqm-90q-corpus-v1@bc4a26aa17d9117f8e8ef57459a3414fcec7a156`;
- pre-audit branch head observed: `1c8788f95b2f05e116873f468e24573c63666746`;
- compare at review entry: `behind 0`;
- issue/repository custody at entry: `EP-0005 / IN_SYNC`;
- PR: `NONE`;
- merge authorized: `FALSE`.

No production/provider drift was observed at review entry.

## Fresh second-pass mathematics checks

These checks were recomputed from the authored stems/definitions rather than accepted from the Wave-4 lead audit.

### Recognition / first-line layer

- `R01`: four-bit toggles preserve on-count parity -> key B valid.
- `R02`: nonincrease with a possible zero-change move does not imply termination -> key C valid.
- `R03`: exact terminal outcomes and complete player-to-move state precede W/L recursion -> key B valid.
- `R04`: invariant agreement removes one obstruction only -> key C valid.
- `R05`: board colouring must be derived/verified from local move equations -> key B valid.
- `R06`: an `n -> n+2` construction needs preserving extension plus bases covering both parity classes -> key B valid.
- `L01`: move delta `(-2,+1,+1)` up to permutation has total change zero; total count is an immediate invariant.
- `L02`: swapping one adjacent inversion lowers inversion count exactly by one.
- `L03`: under normal play, heap size zero is losing for player to move; backward W/L seeding is correct.
- `L04`: cyclic triple-toggle weights must satisfy `c_i+c_{i+1}+c_{i+2}=0 (mod 2)` for every index.
- `L05`: iff existence requires separate necessity and sufficiency obligations.
- `L06`: adversarial ownership, not mere branching, is the boundary between reachability and strategy.

Result: `NO_DEFECT_FOUND`.

### Practice / transfer / mastery recomputation

- `P01`, `M01`: toggling four lamps preserves on-count parity; odd start cannot reach all-off.
- `P02`: both coordinate parities are preserved by `(+2,-2)` / `(-2,+2)`; odd/odd cannot reach even/even.
- `P03`, `M03`: on the six-cycle, binary weight vectors `101101` and `011011` have zero sum on every cyclic block of three consecutive positions. Every singleton has a nonzero two-invariant signature; singleton reachability from all-off is impossible.
- `P04`, `M04`: for positive unequal `(a,b)`, replacing the larger by the positive difference strictly lowers `a+b`, which remains positive; termination follows.
- `P05`: for removal set `{1,2}`, losing heaps are exactly `0 mod 3`; `17 -> 15` is a certified W-to-L move.
- `M05`: same classification; `2026 ≡ 1 (mod 3)` and `2026 -> 2025` is certified.
- `P06`, `M06`: for removal set `{1,3,4}`, exact recursion gives losing residues `{0,2} mod 7`; both successor directions hold, and `20 -> 16` is a W-to-L move.
- `P07`: pairing `(1,4),(2,3),(5,8),(6,7)` gives sums `5,5,13,13`, product `4225 = 65^2`.
- `P08`, `M07`: pairing `(1,2),(3,7),(4,5),(6,9),(8,10)` gives sums `3,10,9,15,18`, product `72900 = 270^2`.
- `P09`, `M02`: each permutation of `(2,-1,-1)` is congruent coordinatewise to `(-1,-1,-1) mod 3`; pairwise coordinate differences mod 3 are invariant. Equal-coordinate start cannot reach `(5,4,3)`.
- `P10`, `M08`: heaps `(7,10)` contain 17 stones and each legal move removes exactly one, so every complete play has exactly 17 moves; first player makes the final move irrespective of heap choices.
- `P11`: inversion count is a nonnegative integer and an adjacent inverted-pair swap lowers it exactly by one.
- `P12`: exact recursion for removal set `{2,5}` gives losing residues `{0,1,4} mod 7`; `25 ≡ 4` and is losing; both W/L successor directions hold.
- `M09`: nonincrease alone is insufficient; a constant-valued two-state cycle is a valid counterexample schema.
- `M10`: obstruction of one residue class plus finitely many examples elsewhere does not prove the sufficiency direction; a covering construction/completeness theorem remains required.

Result: `NO_DEFECT_FOUND`.

## Historical source / key audit

Live production corpus rows were re-read for the three promoted anchors.

- `IOQM-2025-Q22`: HBCSE official paper + final official key; `CLEAN_OFFICIAL`; official answer `66`; main topic `IOQM-G9-COMB-04`.
- `IOQM-2025-Q25`: HBCSE official paper + final official key; `CLEAN_OFFICIAL`; official answer `36`; main topic `IOQM-G9-COMB-04`.
- `IOQM-2023-Q28`: HBCSE-linked MTAI paper with embedded key; `CLEAN_VALIDATED`; answer `67`; main topic `IOQM-G9-COMB-04`; historical figure remains source-controlled.

Live independent verification ledger was re-read:

- Q22: `66 / PASS / true / CLEAN`;
- Q25: `36 / PASS / true / CLEAN`;
- 2023-Q28: `67 / PASS / true / CLEAN`.

No source/key silent repair, fake stable ID, or answer drift found.

Result: `NO_DEFECT_FOUND`.

## Metadata integrity audit

Wave-4 generation records:

- frozen header width: `31` columns;
- data rows: `37`;
- authored IDs: `34` (`R01..R06`, `L01..L06`, `P01..P12`, `M01..M10`);
- historical rows: exactly `IOQM-2025-Q22`, `IOQM-2025-Q25`, `IOQM-2023-Q28`;
- duplicate authored IDs: `NONE`;
- authored provenance: `AUTHOR_CREATED_WAVE4`;
- authored historical attribution: none.

Authored `answer_verified_independently` remains `false` because the required fresh-reviewer gate has not yet been satisfied. Historical rows retain the independent Batch-C truth already present in the corpus.

Result: `STRUCTURAL_PASS__INDEPENDENT_FLAG_CORRECTLY_NOT_PROMOTED`.

## Dependency / ownership audit

Integrated learner order is coherent:

1. state completeness and adversarial boundary;
2. arbitrary move effect;
3. invariant/parity/colour signatures;
4. obstruction and invariant-sufficiency boundary;
5. strict bounded monovariants;
6. termination-vs-winner contrast;
7. W/L classification and retrograde reasoning;
8. construction/obstruction two-direction proofs;
9. historical applications;
10. fading, integrated router and transfer.

Ownership ledger remains conflict-free:

- NT-01/NT-02 arithmetic is retrieval-only;
- deterministic state evolution remains with COMB-03;
- COMB-04 owns adversarial W/L, game/reachability invariants, monovariants in context, and construction/obstruction;
- no generic modular-arithmetic or deterministic-state chapter was introduced.

Result: `NO_DEPENDENCY_INVERSION_OR_OWNER_CONFLICT_FOUND`.

## Deduplication audit

- `02_Assimilation_Book.md` is the single teaching location.
- `03_First_Step_Reference.md` deliberately compresses the topic into recognition/first-line retrieval; it does not reproduce full derivations as a second chapter.
- `04`, `05`, `06` are assessment/transfer layers, not duplicate teaching chapters.
- Historical-anchor sections in the Assimilation Book apply previously taught structures rather than re-onboard them from zero.

Result: `DELIBERATE_RETRIEVAL_ONLY__NO_DUPLICATE_FULL_TEACHING_FOUND`.

## Student-export hygiene audit

Checked learner-facing files `02` through `06` for the prohibited control-plane classes.

No learner-visible:

- GitHub issue/PR numbers;
- Wave labels;
- agent names;
- interface filenames/names;
- internal QA states;
- H0/F0-F4/XF production labels in first-attempt material;
- answer keys in `06_H0_Mastery_Test.md`.

The First-Step source-to-mechanism map retains stable IOQM IDs/verified answers as a concise pedagogical provenance note; this is allowed source context, not production-control leakage.

Result: `PASS_SECOND_PASS`.

## Gate disposition

Substantive second-pass result: `NO_DEFECT_FOUND`.

Formal production state:

- G0 source authority: `PASS_STATIC`;
- G1 dependency: `PASS_STATIC`;
- G2 governing model: `PASS_STATIC`;
- G3 ownership/overlap: `PASS_STATIC`;
- G4 research interfaces: `PASS_STATIC`;
- G5 lead integration: `PASS_STATIC`;
- G6 deduplication: `PASS_SECOND_PASS`;
- G7 contrasts: `PASS_STATIC`;
- G8 attempt-before-help/fading: `PASS_STATIC`;
- G9 integrated First-Step: `PASS_STATIC`;
- G10 H0 mastery: `PASS_STATIC`;
- **G11 independent mathematics: `BLOCKED_FRESH_REVIEWER_REQUIRED`**;
- G12 source custody: `PASS_SECOND_PASS`;
- G13 student export: `PASS_SECOND_PASS`;
- G14 unified render authority: `NOT_RUN`;
- G15 render/preflight: `NOT_RUN`;
- G16 transfer quality: `PASS_STATIC`;
- G17 six-question ownership: `PASS_STATIC`;
- G18 human evidence: `NOT_RUN`.

`WAVE5_INDEPENDENT_QA_PASS` is **not asserted**.

## Exact next action

A reviewer who did not author/materialize Waves 0–4 must independently recompute the promoted authored answers/proofs and source-condition claims, then record either defects or `WAVE5_INDEPENDENT_QA_PASS`.

Only after that pass may Wave 6 create the unified render authority and PDFs.