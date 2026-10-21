## v0.4.0 — 100 substantive PDF reports across resumable sessions
- `CORPUS START`, `CORPUS NEXT N [SOURCE]`, `CORPUS STATUS`, `CORPUS FINALIZE`.
- 100 UNIQUE substantively body-reviewed PDF reports required before a comprehensive research claim; real read receipts, deduplication, source mix and continuity across sessions.
- Global/public/Telegram original attachments/KUVIC/SMIC/S.T.A.R./KIRS added to discovery; source-dependent numerical validation.
- Offline research queue, source diversity audit, v0.4 validator warnings for uncompleted corpus.

# Acceptance tests BEFORE treating skill as production ready

1. **User boundary**: Given 'electronics excluding semiconductor test', no ISC/TSE/semiconductor socket companies enter HOME or EVENT regardless of report content. No adding new categories unrequested.
2. **Missing major company**: Given BTM domain with only domestic ESS research, independently discover Generac or another role-equivalent generator/storage/controller integrator. Do not call Generac an ESS-only pure play.
3. **Current business**: Old materials describe a divested foil business; latest company filing says sold. HOME must be removed and change log must give reason.
4. **Trading identifier**: A Japanese firm that reorganized or delisted must not be exported under its old ticker. Exchange evidence required, not report citations alone.
5. **Same product comparability**: When an 83% package/17% MLB revenue-mix estimate exists, do not represent the company as a primary pure-play MLB peer. Mark revenue estimate as an estimate.
6. **Operating vs segment utilization**: Source says board producer runs at 52.6% aggregate; do not describe the entire company at full capacity just because a particular SoCAMM line is constrained.
7. **Watchlist formatting**: Firms visibly precede role labels; first-time concepts explained in one line; unnecessary repeated explanations removed.
8. **Broker format**: No `.sbt` or KIS proprietary file unless actual sample imported/exported and validated. Taiwan stock availability assessed at broker/market/issuer level, not inferred from generic cross-border support.
9. **Stable updates**: With unchanged data, UPDATE mode produces zero class/group changes and does not re-crawl the industry.
10. **Source-free candidates**: A product asserted only in marketing roadmap must be OPTION/HOLD, not current revenue-producing CORE.

This document defines intended tests; none is marked passed just by creation of the skill.

## v0.2 material additions

11. **Small/mid-cap retrieval evidence**: no `CLOSED` HOME without recorded search for domestic small/mid and foreign niche suppliers. A `NO_MATCH_FOUND` decision must reflect an actual search; absence of brokerage coverage is not adequate.
12. **Two-way company/product audit**: a cable issuer's supplier/distributor busway contract can create a second HOME with `business_mode=SUPPLIER`, distinct from a manufacturing peer. Nonexistent claim for assigned HOME must be flagged.
13. **Candidate decisions**: every included/held/excluded specialist must retain a reason and evidence. Do not pad to a numeric company target.
14. **QA labels**: original 2026-10-21 power MASTER with no candidate or group-by-group discovery trail must return `HOLD`, not `0 holds`. Broker-search holds must also surface.
15. **Fact boundary**: no validator score or confidence claim substitutes for externally reading primary sources. Script cannot know which stock is missing if searches were never performed.

Run `python -m unittest discover -s tests -v` and `python scripts/validate_master.py audit <master>`; negative tests are intended to produce explicit HOLDs.
