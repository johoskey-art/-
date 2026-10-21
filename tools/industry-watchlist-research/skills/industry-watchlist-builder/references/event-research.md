# CANONICAL EVENT RESEARCH + TRANSMISSION v0.3

## Event-led discovery
Search for catalysts **before** deriving investor-facing EVENT names. The primary artifact is a canonical event register, not a story list. Sources are layered:
- L0: law/regulatory text, official implementing agencies, regulator guidance, filings/contracts, actual customer procurement.
- L1: dated independent corporate IR/product business evidence and major customer/supplier disclosures.
- L2: historical and current brokerage/industry analysis; keep each issuer's distinct *inference* with dates and distinguish shared original evidence.
- L3: news/secondary/commentary and model-derived conditional inferences. A quotation of L0 within an L2 paper is not itself a separate independent L0 source.

## Event ID and claim ledger
Canonical event ID examples: `US_EO_14421_20260826` and `US_FCC_INVERTER_COVERED_LIST_20260728` (these are **different** possible events; only include verified IDs and dates). Store aliases/misquotes for retrieval without accepting them as truth. Source claim tuple: (event ID, exact assertion, fact|analyst_interpretation|model_inference|contradiction, original source, issuer, report date, target product, geography, stage, confidence, claim status, cited section). Preserve first seen, last verified, and superseded claims.

## Policy adjudication — exact gating
For EACH regulation verify:
1. Official law/order identifier, issue date, current status (proposed vs signed vs effective vs enforcement).
2. The explicit physical system jurisdiction and item list (e.g., utility/grid-connected inverter vs rack BBU).
3. Prohibited transaction criteria: country-of-manufacture, covered party ownership/control, actual risk finding, import/installation/retrofit distinction, exceptions and geography.
4. Who enforces, implementation deadlines and whether secondary rulemaking/agency determinations are outstanding.
5. Which direct products and component supply chains are affected vs merely discussed by analysts.
6. Alternative interpretation, substitutes, project deferrals, US-made-but-foreign-controlled trade-offs, and contradictory cases.
Never convert `may prohibit certain transactions` into `all Chinese or foreign equipment banned immediately`. The 2026 US bulk-power grid EO is **14421** (not 14420 in some older derivative notes), and addresses identified bulk-power equipment; do not assume all behind-the-meter server BBUs automatically qualify. Check original text and current follow-through each run.

## Beneficiary / non-beneficiary matrix
For each candidate company×product create a conditional path:
`regulatory scope -> displaced incumbent or incremental customer need -> eligible replacement / actual supply contract -> supply availability & certification -> revenue timing & price/mix -> operating margin/EPS/FCF`.
Capture signs and tiers: DIRECT_CONFIRMED, CONDITIONAL_DIRECT, INDIRECT_UPSTREAM, INDIRECT_DOWNSTREAM, COMPETITOR_DISADVANTAGE, SUBSTITUTE_BENEFIT, NO_DOCUMENTED_EXPOSURE, UNCERTAIN. Separate actual observed contracts from investor/analyst narrative and explain why a headline winner might fail to capture profit. Distinguish regulatory scope from product availability. Evaluate small-caps and adjacent-sector names, not just existing HOME firms.

## Multi-analyst thesis clustering
Group reports by the *same underlying event*; group claims separately by agreement vs disagreement. Track 1) independent sources count, 2) analyst issuers count, 3) relevant date coverage, 4) incremental contribution of each report, 5) contrary evidence. Five brokers referencing one EO are NOT five independent confirmations of the legal text. An independent official correction outranks analyst repetition. A thesis becomes stronger when separate business facts (contract, capacity, product availability) verify the expected transmission, not just when more brokers repeat it.

## Release outputs
1. An EVENT inventory of `ACTIVE`, `WATCH`, `SUPERSEDED`, `REJECTED` plus short reasons; do not delete historical nodes.
2. Current HOME-relevant EVENT display and related cross-sector secondary paths, with confirmed/contradictory evidence and a next indicator.
3. A report-corpus audit showing which eras/neighbor sectors/broker theses were searched, which files were not readable, and what assumptions are still held.
4. A change log: what was known in the past, what newer reports changed, what official sources rejected, why inclusion/beneficiary tier changed.
