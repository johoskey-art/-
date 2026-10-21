# REPORT CORPUS DISCOVERY v0.3 — Search broadly, read selectively

## Why this stage exists
A neat value-chain map can be materially wrong when an earlier POLICY / standards / supply-chain catalyst is omitted. A single Drive query using a sector name or the 3 newest PDFs cannot establish that historical coverage is complete. Retrieval window/batch limits are NOT evidence that nothing else exists.

## Two-pass + resumption algorithm
1. **Catalogue first (cheap):** search Drive folders and filenames, historical date ranges and adjacent sectors. Return a candidate manifest with Drive ID/URL, title, report_date, discovered_at, issuer, analyst, sector aliases, size/page count when available, file type and access status. Preserve pagination cursor. Do not read full PDF bodies yet. Expand synonyms in English/Korean (e.g. 전력기기, bulk-power, ESS/BESS, PCS, inverter, UPS/BBU, grid cyber, FEOC, transformer, AIDC). Use reported dates, not only upload timestamps.
2. **Classify before opening:** policy/event roots, company-specific exposures, technology spec, bottleneck, capacity, competitor/substitute, earnings revisions. Sort by likely thesis novelty and product relevance.
3. **Deduplicate:** exact duplicates by hash where available; otherwise same issuer/date/title/author with metadata confirmation. Cluster similar **claims**, not just similar titles. Mark `SAME_PRIMARY_FACT` if multiple reports cite one executive order; preserve distinct interpretations as separate claims. Multi-broker repetition is a research-coverage indicator, not independent verification of fact.
4. **Fast skim:** for each unique cluster, read introduction/summary and matching sections, charts/tables, conclusion. Extract canonical event candidates, source page/section, evidence type and contradiction. PDFs lacking searchable text require fallback page inspection when feasible, else `UNREADABLE_HOLD`.
5. **Escalate:** deep read selected reports if first-time catalyst, new covered product, updated enforcement, new earnings bridge, official/source disagreement, outlier estimate, or material counterargument. Defer verbatim repetitions.
6. **Merge into event registry:** Never overwrite first occurrence; add historical versions, new evidence, future triggers and explicit stale/overruled assertions. Link related events rather than collapsing different statutes into one.
7. **Stop gate:** Every material source/date/adjacent-sector cluster has a recorded reviewed/deferred/unavailable status; last few new unique clusters add no new event node/economic pathway, or unresolved gaps are explicitly OPEN. An arbitrary number of PDFs is not a completion criterion.

## Batch limits and persistence
Process in bounded batches (e.g., 5–10 unique high-relevance items at a time, tuned for context). After each batch **persist metadata, indexed snippets and progress** to a private Drive MASTER or authorized private repository; do not upload licensed full broker-report text to public GitHub. The next run loads cursor/index and continues. No promise of background reading; complete what the current run can actually execute and show remaining work. A metadata catalog can contain hundreds of reports without loading all PDFs simultaneously. Preserve both source timestamps and extracted-claim vintage.

## Four axes in corpus audit
- `HISTORICAL`: origin of current thesis, prior-cycle regulations/supply-chain precedents and changes across time.
- `CURRENT`: recent changes to law, customer wins, utilization, pricing, contracts, EPS.
- `MULTI_ISSUER`: at least contrasting analyst interpretations or explicitly explain coverage limits; never invent artificial minimum number of houses.
- `CROSS_SECTOR`: events whose legal/economic scope spans electrical equipment, ESS, solar, data centers, policy, batteries, software or power semiconductors.

Required audit fields per axis: status=SEARCHED|NOT_APPLICABLE|OPEN, query_or_method, range_or_scope, catalogued_count, unique_reviewed_count, deferred_count, as_of, source_ids, remaining_questions. An OPEN axis is a QA HOLD.
