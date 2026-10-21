# Independent QA gates — v0.2

**This checklist applies to the final product, not just syntax.** Script checks are structural; they cannot verify sources independently or find an unknown stock without a fresh search.

- **G1 Scope & HOME:** no prohibited company×product role; preserve stable IDs and proper physical/economic ordering; no new folder for a theme alone.
- **G2 Role coverage:** per HOME inspect `coverage_audits`: global leaders, domestic small/mid, foreign specialists, and incumbent cross-product/supply-channel. If any track is undocumented, status must be OPEN/HOLD. One leading company or a 2–6-member aesthetically tidy block is **not** proof of sector coverage.
- **G3 Candidate accountability:** `candidates` records discovered, included, held and excluded names, evidence and selection reasons. No arbitrary minimum count, market-cap cutoff, domestic-only bias, or routine rejection because a stock has weak brokerage coverage. Review exclusions for unsupported small-cap penalties.
- **G4 Company×product×mode:** current products and subsidiaries/contracting entities matter. Manufacturer ≠ distributor/supplier; group memberships may overlap only where a product exposure or economic reason is supported. Every included company×HOME link needs its own evidence claim; a generic repeated text does not establish an actual product relationship.
- **G5 Financial significance:** label actual revenue, estimated revenue, order/contract, qualification and speculative roadmap. Reconcile total-company vs product revenue; a supply framework maximum ≠ booked revenue. High market beta ≠ event earnings beta; do not claim EPS leverage without calculations.
- **G6 Sources and listing:** prefer official annual reports/product catalogs/contract filings for company facts. Independently triangulate customer, competitive position and market shares. Check disposal and ticker changes; examine local exchange boards (e.g. TPEx) and both broker search capabilities separately.
- **G7 Events:** identify Q/P/MIX/SHARE/UTIL/COST/YIELD chain to earnings with next indicator and negative case; weak indirect thematic links do not make an EVENT core.
- **G8 Holds are real:** include outstanding `qa_holds`, per-company listing and broker holds, conditional claims, material coverage gaps and contradiction notes in report. Never say `0 holds` when only a syntax script happened to pass.
- **G9 Output and persistence:** keep companies first; HOME vs EVENT separate; one-line explanations once; diff against prior master, and retain evidence log. Do not create/import broker files from guessed formats.

## Regression cases — MUST recheck after changes

1. **Gaon busway (generic failure pattern)**: company is found under cables; an official supply/channel contract exposes it to busway. Verify actual legal entity and business mode; do not suppress second HOME just because it is not the manufacturer; avoid labelling all group members manufacturers. If evidence cannot be checked, explicit candidate HOLD.
2. **Niche firms**: each HOME documented small/mid-cap domestic search, foreign specialist search and candidate disposition. Other than a documented `NOT_APPLICABLE`, an empty track blocks research coverage completion.
3. **Inherited assumptions**: earlier MASTER classifications are starting hypotheses; meaningful recent primary evidence overrides inherited interpretation. Reopen only affected groups.
4. **Placeholder claim**: a repeated non-specific phrase cannot count as verified evidence.
5. **0 holds trap**: if broker registration is unverified, or role discovery is undocumented, QA must report outstanding work even if IDs and references are internally consistent.
6. **Others**: divested businesses, obsolete tickers, out-of-scope semiconductor tests, FC-BGA primary/entrant contrast, aggregate-vs-product utilization, export syntax not established.

`python scripts/validate_master.py audit <master.json>` prints a JSON structural coverage report. `validate <master.json> --strict` exits with code 3 on outstanding issues. A structural pass does **not** certify business facts, instrument trading status or live brokers.

## EVENT completeness gate (v0.3)
- `report_corpus_audit` must document HISTORICAL, CURRENT, MULTI_ISSUER and CROSS_SECTOR metadata/skim/deep-read work; an incomplete topic/year/sector window is OPEN/HOLD, not no-result.
- `event_registry` must list researched event roots, source lineage, confirmed vs analyst vs inferred claims, product/legal scope, status, first_seen, next indicator, contradictory case, affected companies and excluded/non-beneficiaries. A final EVENT does not automatically prove historical coverage.
- Legal identifiers must be matched to authoritative sources; do not silently inherit EO 14420 when controlling primary text is EO 14421. Multiple broker repeats of an erroneous identifier do not prove consensus.
- Distinguish BESS, critical-infrastructure UPS and rack-level BBU; specific regulation may not cover all three. `UNKNOWN_SCOPE` blocks automatic direct benefit labeling.
- Script audit can verify presence and internal consistency of these fields, but **cannot prove** that external reports were read or that beneficiaries truly capture profit.
