---
name: industry-watchlist-builder
description: Build or update evidence-verified cross-border equity watchlists as industry value-chain maps with HOME peer groups, EPS-linked EVENT transmission, and broker-ready exports when formats are known. Use for industrial watchlist research, global peer discovery, missing-role audits, classification verification, and Samsung Securities/Korea Investment Securities watchlist preparation.
---

# Industry Watchlist Builder

Produce a usable **industry and company comparison watchlist**, not a long research report. The watchlist is the final product. Do not re-create a previously validated map unless the evidence materially requires it.

## Operating modes

- **NEW**: no usable MASTER; discover the industry from scratch.
- **UPDATE**: load the latest MASTER, evidence register, scope, and change log; investigate only changed or uncertain claims.
- **AUDIT**: independently verify an existing map and produce a change set; preserve valid block order.
- **EXPORT**: generate broker-specific files from a verified MASTER, but only if the broker's exact accepted file syntax and instrument support were verified.

When files or broker templates are not accessible, issue an explicit `UNVERIFIED` record and produce a broker-neutral preview instead. Never invent an import format or claim an account was updated.

## ChatGPT tool orchestration

- Use the user-connected Google Drive connector for private report discovery and reads; public web research for global primary/company/industry sources. A skill never grants access itself.
- If the user requests GitHub persistence and the connector is connected with write rights, preserve source provenance and write only after verifying the destination repository; do not put private report full text or personal holdings into a public repository without clear authorization.
- For a phone-first conversation, prioritize in-chat HOME/EVENT summaries and link to verified generated files; do not pretend the mobile host can execute bundled Python scripts.
- If broker formats or connected broker account actions are unavailable, use broker-neutral text and hold broker-specific imports, rather than fabricating success.

## Mandatory execution sequence

1. **Load & scope-lock**. Read existing MASTER and latest confirmed watchlist, prior decisions, test cases, and user-specified included/excluded products. Freeze scope for the run. Respect user exclusion rules regardless of report coverage.
2. **Discover industry roles**. Begin with recent domestic and international industry reports, authoritative sector studies, and lead-company annual reports/IR. Extract products, who buys from whom, alternatives, pricing, capacity, bottlenecks, and physical installation/use context. Distinguish FACT, ESTIMATE, OUTLOOK, and HYPOTHESIS. Read `references/discovery.md`.
3. **Coverage audit & global discovery**. Draw a provisional product/role value chain before finalizing companies. Detect missing economically material roles. Search for companies by **role/product/customer problem**, not merely by an existing stock list. For each missing role, seek global leaders, pure-plays, integrators, alternatives, and relevant Korean firms. Verify candidate business with company annual reports, filings, products, and customer sources. Do not assume the absence of brokerage coverage means a company is unimportant.
4. **Verify company × product × role**. Collect sources for each important claim: actual product, segment revenue if available, sales to whom, actual stage (pilot/qualification/ramp/revenue), profitability driver, public listing/security. Verify recent divestitures and ticker/status changes independently. Read `references/evidence.md`.
5. **Build HOME and nearest-peer blocks**. Group chiefly by WHERE+WHAT, then compare SAME MONEY DRIVER. Prefer genuine same-product competitors. A global leader can anchor a block, while partial/expanding businesses should be differentiated. Multiple meaningful product HOME locations are allowed with a recorded reason. Preserve earlier stable block IDs and order unless evidence demands edits. Read `references/peer-and-order.md`.
6. **Construct selective EVENT transmission**. For each meaningful current event, explain the route to Q/P/MIX/SHARE/UTIL/COST/YIELD, then margin/EPS/FCF; include direct/indirect/competitive/alternative effects, stage, next indicator, and contradictory evidence. Only high-sensitivity companies go into EVENT display. Read `references/events.md`.
7. **Independent quality gate**. Apply all gates in `references/verification.md`. Check scope contamination, outdated businesses, listing/ticker, peer proximity, overclaimed customer names, segment-vs-group utilization, recency conflicts, economic causality, and exceptions. Re-open **only affected** steps. When a Python execution environment is available, run `python scripts/validate_master.py validate <master.json>` and repair errors. In mobile chat without a local execution tool, perform the same structural checks from `references/verification.md` by inspection and report `NOT_EXECUTED` for automated validator tests; never claim they passed. Warnings need a decision or explicit HOLD.
8. **Render and export**. When an execution environment is available, run `python scripts/validate_master.py render <master.json>`; otherwise construct the same company-first preview from the validated MASTER. Preserve companies-first visual rhythm (generally 2–6 firms then short label and at most one line explanation); HOME value-chain sequence and EVENT causal sequence are separately ordered. Render all unknown broker capabilities as HOLD. Produce diff/change log and audit report. Read `references/export.md`.

## Core decisions and stopping conditions

- No new group merely for an interesting material, process, theme, or customer; create a distinct economic block only when product/customer, ASP, margin, scarcity, qualification, or earnings sensitivity differ meaningfully.
- A **structurally important** company with weak direct EPS exposure can still be an essential industry-map or signal reference; distinguish CORE / STRUCTURAL / OPTION / SIGNAL at **company-product** level.
- A missing role is material if excluding it hides a major buying decision, integrator, substitute, bottleneck, or causal link. Search until such gaps have defensible representatives and additional candidates add little incremental understanding; log unresolved gaps.
- Prefer company/filing/IR for *what a firm actually sells*, independently triangulate for *market share, technical superiority, rival position and supply-chain relationships*. Newer verified operating data override older outlook, without erasing useful older mechanism/history.
- Never infer exact buyer–supplier relationships from a value-chain arrow without supporting evidence.
- Stop when the essential product roles, nearest peers, economic differences, main event/negative case, and required listing identifiers are resolved **or explicitly held**; do not continue broad searches for the sake of coverage.
- Output must distinguish `VERIFIED`, `ESTIMATED`, `OPTION`, and `HOLD`. Do not silently upgrade unsupported statements.

## Final deliverables

1. `MASTER` with company × product assignments, peers, evidence and status.
2. `HOME` and `EVENT` company-first watchlist preview.
3. `CHANGELOG` showing additions, removals, group moves, source and cause.
4. `QA` report with blockers/holds, and broker-specific export **only after actual import format confirmation**.

The skill orchestrates available access/tools; it does not grant new Google Drive, securities account, or exchange entitlements. When a source or tool is unavailable, continue with admissible evidence and document the gap.
