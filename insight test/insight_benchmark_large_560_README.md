# Insight Large Synthetic Stress Benchmark

## Overview
A robust synthetic benchmark for validating Insight logic in NWv-7 / NWv-7-PG.

- **As-of time:** 2024-06-04T20:00:00+05:30
- **Total feed items:** 520
- **Expected parent stories:** 7
- **Duplicate groups:** 42
- **Noise items:** 160

## What it tests
- 4 snapshot windows: now / minus4h / minus12h / minus24h
- 7 expected parent stories, each with varied child insight angles
- heavy duplication across multiple sources
- noisy distractors from unrelated categories
- varied source groups
- messy `published_at_raw` formats
- ambiguous bridge stories challenging clustering boundaries
- date-parser edge cases

## Expected parent stories
1. NDA returns but BJP falls short of solo majority, allies turn crucial
2. Indian markets tumble and rupee weakens after surprise election outcome
3. Chennai supply crunch, desalination push and local outage advisories dominate city coverage
4. Oman weather watch brings port advisories, rainfall alerts and school warnings
5. AI chip export restrictions ripple through semiconductor names and cloud strategy
6. Airline flash sales collide with airport delays and summer travel congestion
7. OTT release controversy triggers censorship, legal and culture-war coverage

## Suggested checks
1. Top 7 parents should match the 7 expected canonical IDs.
2. Each parent should expose 5+ varied child insight groups.
3. No noise topic should rank as a top parent.
4. Same-angle duplicates should collapse under one group.
5. Snapshot presence should match slot assignments.
6. Edge date formats should not crash the pipeline.
