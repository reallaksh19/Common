# Source, Benchmark, and Common-Document Indexing

## Purpose

The next agent must not rediscover the governing engineering material from chat or repository archaeology.

Every endpoint therefore lists six inventories:

```text
INPUTS
BENCHMARKS
COMMON / GOVERNING DOCUMENTS
AUTHORITATIVE SOURCES
PRODUCTION PATHS
VALIDATION / TEST PATHS
```

## Minimum record

For each important item record as applicable:

```text
name / role:
repository:
path or external controlled locator:
commit / blob / hash / version:
page / section / equation / table / figure:
authority class:
why needed for next leg:
qualification state:
```

Use `null`, `NONE`, or `UNRESOLVED` explicitly where the field cannot legitimately be supplied.

## Inputs

List actual engineering/task inputs needed to reproduce or continue the work, for example:

- model/source input files;
- canonical fixtures;
- load cases;
- material/section/geometry definitions;
- configuration profiles;
- retained source transcriptions;
- controlled generated evidence when it is itself an input to the next leg.

Do not list broad directories when only one or two files are actually authoritative.

## Benchmarks

List every benchmark that materially constrains the next contribution:

- analytical hand calculations;
- published examples;
- independent reference datasets;
- cross-solver cases;
- frozen regression fixtures with qualified provenance;
- experimental measurements where applicable.

Distinguish:

```text
INDEPENDENT
IMPLEMENTATION_COUPLED
REFERENCE_ONLY
UNQUALIFIED
```

Do not silently promote a regression fixture to an independent engineering oracle.

## Common / governing documents

Include process and methodology documents needed by the next agent, such as:

- this Skill version;
- repository `AGENTS.md`;
- repository coding rules;
- promotion/release plans;
- project method definitions;
- shared `Common` references.

Where possible pin the exact commit/version that governed the current leg.

## Authoritative sources

List engineering authority separately from process documentation.

Examples:

- standard/code source;
- WRC bulletin;
- manufacturer source data;
- controlled primary engineering document;
- source-qualified table/equation dataset.

State the authority boundary. A document being present does not prove every semantic interpretation is qualified.

## Production paths

List the actual code/data boundaries expected to be inspected or changed by the next leg.

Prefer exact files/functions/modules over broad path prefixes where known.

## Validation / test paths

List the scripts/tests/evidence needed to falsify or validate the next contribution.

Include independent evidence separately from implementation-coupled tests.

## Pinning discipline

Prefer stable locators:

```text
repository + commit + path
blob SHA
semantic hash
source revision/date
page/section/table/equation
```

For mutable URLs or branches, record the observed commit/version when practical.

## Missing material

Never hide absence.

Examples:

```text
BENCHMARKS:
NONE — no independent benchmark exists yet; next leg must establish one before production promotion.
```

```text
AUTHORITATIVE SOURCES:
UNRESOLVED — physical shell-thickness basis is not yet qualified from the primary WRC source.
```

Missing authority is an engineering state, not a documentation inconvenience.

## Avoid endpoint bloat

`agentchain.md` should point to detailed source ledgers or evidence rather than reproducing them.

Good:

```text
BENCHMARK:
validation/lafea/lafea3-t6-benchmark-v1.json
semantic hash: ...
authority: INDEPENDENT_ANALYTICAL
```

Bad: paste the entire benchmark dataset into the endpoint.
