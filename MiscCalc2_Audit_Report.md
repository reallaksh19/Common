# Misc Calc Audit Report 

## Scope
Audited the uploaded patch against the agreed requirements:
- formula correctness / removal of mock logic
- source-data structures for pending tables
- parsed → linelist → manual mapping integrity
- unit conversion and UI consistency
- benchmark coverage
- SVG / console wiring

Requirements baseline came from the uploaded prompt, especially:
- no silent placeholder formulas
- structured source/master tables
- parsed → linelist → manual precedence
- explicit unit normalization and display
- benchmarkable results with zero unexplained mismatches. 

## Overall verdict
**Status: PARTIAL / NOT APPROVED FOR COMPLETION CLAIM**

The patch makes useful progress on **source-data table structure** and **in-app editing UI**, but it does **not** close the core technical items yet:

- PSV Open still contains placeholder force equations.
- Bursting Disc Liquid and Blast still use non-workbook placeholder formulas.
- Flange Check still uses placeholder allowables for force/moment and simplified fallback logic.
- Benchmark cases are stored, but the benchmark engine does not execute benchmark inputs.
- Unit conversion exists, but the UI still presents hardcoded input labels/units and does not fully adapt to mode changes.
- “Save to public” does not actually target `../public/...` as requested.

---

## 1. Structural audit

### PASS
- Added a new `viewer/calc/source-data-manager.js`.
- Added source-data editor config and Source data panes in `viewer/tabs/misc-calc-tab.js`.
- Added default JSON-shaped structures for:
  - PSV Open
  - Bursting Disc Liquid
  - Blast
  - Flange Check

### PARTIAL
- The uploaded zip is an **incremental patch**, not a self-contained runnable package. The tab imports many modules outside the uploaded delta:
  - `../core/state.js`
  - `../calc/core/calc-registry.js`
  - multiple formula/svg modules
  - etc.
- That is acceptable as a delta patch, but it means the upload itself cannot be validated standalone.

---

## 2. Source-data structure audit

## 2.1 What is good
`source-data-manager.js` creates table skeletons for all requested pending areas:

- `mc-psvopen`
  - `orificeTable`
  - `kRoTable`
  - `benchmarkCases`
- `mc-bdliquid`
  - `deviceSize`
  - `coefficients`
  - `correctionFactors`
  - `benchmarkCases`
- `mc-blast`
  - `caseFactors`
  - `pressureCoefficients`
  - `dragFactors`
  - `benchmarkCases`
- `mc-flange-check`
  - `runtimeAllowables`
  - `forceAllowables`
  - `momentAllowables`
  - `benchmarkCases`

This satisfies the “create the structure of missing tables” requirement.

## 2.2 Major defect
`saveSourceDataToPublic()` does **not** write to `../public/...` or to a selected `public/...` path.

Current behavior:
- prompts user to pick a directory
- then creates / writes to:
  - `misc-calc-source-data/<filename>.json`

But it ignores the `public/` segment of the configured save target.

So:
- configured target says `public/misc-calc-source-data/...`
- actual write code uses only `misc-calc-source-data/...`

That is a direct mismatch with the requested save behavior.

## 2.3 Secondary defect
If File System Access API is unavailable, save falls back to runtime/localStorage only.  
That is acceptable as fallback behavior, but it is **not** equivalent to “save as json in ../public/... folder”.

**Audit result:** Source-data structures are present, but save-to-public is only **partially implemented**.

---

## 3. Formula audit

## 3.1 PSV Open
### Finding
The calculator now reads source data and benchmark tables, but the core formulas are still placeholders:

- `pressureAtTip = W / tailpipeTipArea`
- `F1 = W * 0.1`
- `F3 = W * 0.05`
- `F4 = W * 0.02`

Then:
- `totalVerticalForceAtElbow = (F1 + F3 + F4) * impactFactor`

This is still explicit placeholder logic, not workbook-derived PSV Open logic.

### Result
**Status: MOCK-RISK**

The source-data structures are useful, but the core formula is still not technically valid enough for closure.

## 3.2 Bursting Disc Liquid
### Finding
The calculator now reads source data and computes:

- `deltaP = burstPressure - downstreamPressure`
- gets the first configured `burstArea_mm2`
- `resultantLoad = deltaP * configuredArea * 1e-3`

This is still a generic placeholder screening relation, not workbook logic.
It also does not use:
- coefficient tables
- correction factors
- device-specific discharge logic

### Result
**Status: BLOCKED / PLACEHOLDER**

## 3.3 Blast
### Finding
The calculator currently computes:

- `resultantLoad = blastPressure * exposedArea * coefficient * 1e-6`

This is still a generic shell formula, not workbook-driven blast logic.
The source data tables exist, but the formula does not actually consume them meaningfully beyond count reporting.

### Result
**Status: BLOCKED / PLACEHOLDER**

## 3.4 Flange Check
### Finding
This is the strongest of the four, but still incomplete.

What improved:
- uses source data via resolver
- supports runtime pressure allowables
- supports force/moment allowable placeholders via Source data

What is still pending:
- NC path still falls back to:
  - `20 ksi` pressure allowable placeholder
  - `1000 N` axial allowable placeholder
  - `5000 N-mm` moment allowable placeholder
- UG44 path still uses simplified synthetic allowables:
  - `p_allow = 25 * Fm`
  - `f_allow = 1200 * Gm`
  - `m_allow = 6000 * Gm`

Those are not yet demonstrated as workbook-true or code-true.

### Result
**Status: PARTIAL / PENDING_ACCESS_PARITY**

---

## 4. Mapping audit

## 4.1 What is good
- PSV Open resolver now reads lookup data from source-data tables instead of hardcoded constants.
- Flange resolver now injects source data into the normalized input path.

## 4.2 Missing / weak areas
- The requested precedence `Parsed → Linelist → Manual` is still not systematically enforced for these four calculators.
- In the audited files:
  - there is no robust per-calculator provenance structure returned for PSV / Blast / Bursting Disc / Flange
  - linelist fallback is not visibly implemented for these calculators in the changed formula/resolver files
  - manual entry still dominates most inputs
- Source-data tables are wired to formulas, but parsed and linelist mapping remains only partial.

### Result
**Status: PARTIAL**

---

## 5. Unit-system audit

## 5.1 What improved
A richer `UnitSystem` now exists with:
- length
- area
- force
- pressure
- stress
- moment
- density
- velocity
- mass flow
- temperature conversion support

Formulas now call:
- `UnitSystem.normalize(...)`
- `UnitSystem.format(...)`

This is a meaningful improvement.

## 5.2 What is still wrong
### UI/input mismatch
The top bar lets the user switch unit mode, but the form input labels remain hardcoded in many places.
That means the mode switch changes normalization assumptions, but the UI does not consistently tell the user which unit they are now expected to enter.

Example pattern:
- input field label remains e.g. `psi`, `mm`, `kg/m3`
- unit mode changes to SI or Imperial
- normalization changes, but label may not

This is still a technical integrity problem.

### Native-mode ambiguity
`UnitSystem.normalize()` infers the input unit from the selected mode defaults.  
This works only if the UI labels follow the same mode. They do not fully do that yet.

### Result rendering
Some result tables use `display` objects correctly, but others still compose rows manually and leave placeholder markers in the output.

### Result
**Status: PARTIAL**

---

## 6. Benchmark audit

## 6.1 What improved
There is now a shared `evaluateBenchmark()` helper and benchmark table structure per calculator.

## 6.2 Core defect
The benchmark system does **not** execute benchmark-case inputs.

It only:
- reads the current calculator outputs
- compares them with `expected` fields from enabled cases

So benchmark cases are not a true harness. They are only expected-value comparators against the current interactive run.

Missing:
- loop over benchmark case inputs
- execute calculator per case
- compare actual case outputs vs case expected outputs
- aggregate pass/fail per case run

### Additional issue
If no enabled cases exist, benchmark status stays `PENDING_SOURCE_EXTRACTION`, which is fine for pending calculators, but not enough for final closure.

### Result
**Status: PARTIAL / STRUCTURALLY INCOMPLETE**

---

## 7. Console / UI audit

## 7.1 Good
- Console shows:
  - metadata
  - inputs/input resolution
  - equation trace
  - intermediate values
  - outputs
  - benchmark block
  - source snapshot
  - warnings/errors

## 7.2 Defects
### PASS/FAIL display can be misleading
Console always renders:
- `[Result] PASS` if `session.pass`
- else `[Result] FAIL`

For calculators that are pending / blocked and do not set `session.pass`, this will appear as FAIL even if the calculation is only incomplete, not mathematically failed.

### Placeholder text still visible
PSV Open result table still labels:
- `F1`
- `F3`
- `F4`
as `(placeholder)`

That is technically honest, but it confirms the calculator is not closure-ready.

### Mock SVG bridge remains
`updateSvg()` still uses:
- `window._lastFlangeUr // mock up state bridge`

That is a lingering mock bridge and should be removed.

### Duplicate history appends
Some calculators still call `appendToHistory(envelope)` twice in the same click path.

### Result
**Status: PARTIAL**

---

## 8. Severity-ranked defect list

## High
1. PSV Open formula still placeholder
2. Bursting Disc Liquid formula still placeholder
3. Blast formula still placeholder
4. Flange force/moment allowables still placeholder
5. Benchmark harness does not execute benchmark inputs
6. Save-to-public path does not actually write to `public/...`

## Medium
7. Parsed → Linelist → Manual precedence not consistently implemented
8. Unit-mode switch does not fully update input labels / UI expectations
9. PASS/FAIL console state is misleading for pending calculators
10. Mock state bridge remains in flange SVG path

## Low
11. Source-data pane is useful but textarea-only; no schema validation beyond JSON parse
12. Some results show counts/status instead of engineering validity

---

## 9. Approval recommendation

## Not approved for “completed / zero-error benchmarked / technically closed”
Reason:
- core formulas are still pending for 3 of 4 target calculators
- flange still relies on placeholder allowables
- benchmark system is not yet a real case-runner
- save-to-public path is not faithful to the requested public-folder behavior

## Approved as “intermediate infrastructure phase”
Reason:
- source-data table structure exists
- source-data subtabs exist
- save/reset runtime flow exists
- unit helper improved
- benchmark scaffolding exists

---

## 10. Recommended next patch phases

### Phase A — close infrastructure defects
- fix `saveSourceDataToPublic()` path semantics to support selected `public/...`
- add schema validation per source-data section
- fix console result state for pending calculators
- remove mock SVG bridge
- remove duplicate history appends

### Phase B — close benchmark engine
- benchmark runner must execute each enabled case’s inputs
- compare case-specific outputs
- report per-case actual/expected/delta
- support SI and Imperial execution

### Phase C — close formula truth
- PSV Open workbook formula transcription
- Bursting Disc Liquid workbook formula transcription
- Blast workbook formula transcription
- Flange real allowable and interaction parity

### Phase D — close mapping and UI
- enforce Parsed → Linelist → Manual provenance
- update all input labels/live unit hints with mode switch
- ensure SVG labels follow unit mode too
