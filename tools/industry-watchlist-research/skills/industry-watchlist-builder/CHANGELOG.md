## v0.3.0 (2026-10-21) — event-led historical research
- Catalogue historical/current broker reports by sector and adjacent-sector before concluding event coverage.
- Two-pass retrieval (metadata -> novel claims/charts) and resumable corpus evidence; identify duplicates and analyst disagreements.
- Canonical policy event IDs, original regulatory text priority, implementation conditions and source hierarchy. Explicit EO 14421 vs EO 14420 anti-regression case.
- Economic impact graph includes conditional and negative exposures, product/geography/ownership/US production distinctions, BBU vs BESS vs critical UPS.
- v0.3 structural event-coverage QA and offline regression tests.
- Preserve v0.2 small-cap, cross-product and role-coverage safeguards.

# Industry Watchlist Builder changelog

## 0.2.0 — coverage and evidence QA

- Preserved one industry-independent skill with `NEW`, `UPDATE`, `AUDIT`, `EXPORT` modes.
- Implemented four role-by-role discovery tracks for global peers, domestic small/mid-cap, foreign specialists and existing-firm cross-product/supply-channel audits.
- Added manufacturer / supplier / distributor / installer distinctions and supporting company×product business-stage evidence.
- Added evidence-backed inclusion/exclusion/HOLD candidate register; requires explanation rather than silently pruning smaller specialists.
- Replaced misleading `0 holds` acceptance for v0.1 MASTER; visibly distinguishes offline syntax/structure checks from actual market verification.
- Added `audit` JSON summary and `--strict` for blocking export-ready status when holds remain.
- Added synthetic supplier-with-second-HOME fixture and regression suite.
- The historical power-equipment MASTER remains **unmodified** by this skill update; it must be re-researched and migrated to schema v0.2 to satisfy new completion gates.

## 0.1.1 — initial personal ChatGPT plugin

- Industry report-led discovery, HOME and EVENT schema, initial structural validator and broker format holds.
