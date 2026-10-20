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
