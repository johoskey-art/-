# Reading priority: next best 10 reports, not any 100 (v0.5)

## Decision objective
Maximize **independent, decision-relevant knowledge gained per unit of reading effort**, while guaranteeing searches in undercovered material roles and dates. A verified 60-report collection containing primary sources, deep industrial diagrams, contradictions and earnings transmission may be more useful than 150 nearly identical sell-side company notes. Neither count automatically certifies completeness.

## Discovery order (two-pass)
1. Search a broad universe by product synonyms, adjacent end markets, time period, competitor IR, public international brokerage/industry analysis, Drive, Telegram collector original attachments, KIRS, KUVIC, SMIC, S.T.A.R., policies, and technical standards. Titles/dates/issuers are cheap to index.
2. Build a coverage matrix **(industry role × EVENT × geography × history/current × candidate/sensitivity)** and identify empty/weak cells. An important sector with no research must not be treated as no investable companies.
3. Preview a report's table of contents/executive summary and **which original evidence it cites** (do not count as a substantive report read). Assign preliminary score only with explicit brief rationale and `ESTIMATED` marker; unknown is not novelty. Deduplicate exact papers and same-primary-fact reiterations.
4. Choose the next small batch using greedy **incremental value**. Update scores immediately after each report's distinct findings and contradictions are recorded. Source/issuer diversity breaks ties; avoid arbitrary 20%-per-category quotas and fixed recency rules. An older first analysis of a policy change may outrank a repetitive newest report; a new implementation rule may outrank the old first analysis.

## Pre-read scores 0..5: not objective probabilities
All component ratings must be supported by report metadata/summary/known citations and record `priority_reason`. Weights rank **future reading candidates**, not investment prospects:

- `role_or_event_gap` ×5: fills missing role, overlooked smaller company, different geography or historical catalyst.
- `expected_new_mechanism` ×5: novel how/why of technical specification, delivery, bottleneck, pricing, capex, or customer selection.
- `primary_evidence_potential` ×4: official exhibits, cited contract/IR/procurement, independent numbers likely to be checkable.
- `earnings_bridge` ×4: links change to business-unit Q/P/MIX/SHARE/margin and timing, as opposed to thematic story.
- `contradictory_view` ×4: refutes prevailing view, highlights non-beneficiaries, changes old event judgment.
- `topic_relevance` ×3: scope fit with selected industry and its neighboring sectors.
- `time_sensitive_update` ×2: recent material change in applicable law, customer, pricing, share, EPS.
- `redundancy_risk` ×−5: same primary event/claims already read, not an independent interpretation.

Score **real report candidates** only after at least metadata/preview access; do not invent rankings for unseen files. Store `coverage_tags` such as `EVENT:US_POWER_SECURITY`, `PRODUCT:PCS`, `ROLE:INVERTER_MAGNETICS`, `REGION:US`, `EARNINGS:SANIL` to diversify selected reading. Metadata tags are a research hypothesis, not a verified claim. The deterministic script incorporates source/issuer diversity and new coverage tags; the analyst can manually override with an explicit reason when source quality or critical evidence justifies it.

## Source roles and reliability
- Official rules, product catalogs, audited filings and customer/contract confirmations: required for **legal scope / technical specs / actual company earnings facts**. Many aren't PDFs and must be used even though they don't increase PDF tally.
- Broker/foreign/industry reports: best for locating catalyst families, consensus, historical shifts and differing forward forecasts; several houses sharing the same underlying event are not independent proof of its legal details.
- KUVIC/SMIC/S.T.A.R.: often strong for obscure product breakdowns and causal diagrams; use for hypothesis generation. Independently verify claimed customers/volumes/EPS/market share.
- KIRS: valuable for Korean small-cap business anatomy; forecasts are still estimates, not filings.
- Telegram text: effective lead source and alert; read the original linked report/official document whenever possible, never count forwards as separate PDF evidence.

## Batch review receipt and remaining work
For each chosen report: note the `reason_for_selection`, new factual evidence, newly proposed but unverified hypotheses, new firms/products/events, contradicting source, actual sections/page locator, and `incremental_value` (HIGH/MEDIUM/LOW). Log discarded candidates as `DEFERRED_LOW_VALUE` with reason, without lying that they were read. Show Top 10 next with specific expected contributions, plus discovered gaps for which *no candidate yet exists*.

## Stopping rule (no numeric shortcut)
After at least a range of relevant report families and histories has been searched, consider stopping **only** if:
- The HOME roles, non-Chinese sourcing/policy/industrial events, adjacent product chains, small companies and alternatives have credible coverage or explicit bounded exceptions.
- Critical policies are checked against official texts and dated implementations; contradictory broker claims and missed earnings bridges are resolved or held (not discarded).
- The unread highest-ranked candidates are assessed: none is likely to overturn a material beneficiary/non-beneficiary classification; if important unreads remain, continue.
- The last recorded batches add little material new evidence, **and** the analyst has documented a grounded `research_decision` (`SATURATED` or `COVERAGE_CONFIRMED`) with reason, batch delta, date, high-value unread audit, and remaining uncertainty.
- **100 unique reads with open critical gaps is NOT complete.** Fewer than 100 can be defended as *priority-research-complete* with transparent actual count and remaining limits. Stop is not proof no unknown firms exist.

## User commands
`CORPUS START 전력기기 PRIORITY` to build broad catalogue + coverage matrix; `CORPUS NEXT 20 PRIORITY` to read the next best documents; `CORPUS RERANK` to refresh priorities against current knowledge; `CORPUS STATUS` to show actual counts, next top candidates and coverage gaps; `CORPUS FINALIZE` to audit reasoning, sources, gaps and whether another batch is justified. Explicit `TARGET 100` records a desired exploration depth, not an automatic pass gate.
