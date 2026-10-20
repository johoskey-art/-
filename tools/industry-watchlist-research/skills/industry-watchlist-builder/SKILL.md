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

## Mandatory execution sequence (v0.2)

1. **Load & scope-lock**. Read existing MASTER and latest confirmed watchlist, prior decisions, test cases, and user-specified included/excluded products. Freeze scope for the run. Respect user exclusion rules regardless of report coverage.
2. **Discover industry roles**. Begin with recent domestic and international industry reports, authoritative sector studies, and lead-company annual reports/IR. Extract products, who buys from whom, alternatives, pricing, capacity, bottlenecks, and physical installation/use context. Distinguish FACT, ESTIMATE, OUTLOOK, and HYPOTHESIS. Read `references/discovery.md`.
3. **Coverage audit & company discovery**. Draw a provisional product/role value chain before finalizing companies. For **every existing and new product HOME**, log four mandatory research tracks: (a) global leaders/direct peers, (b) domestic small/mid-cap specialists, (c) foreign smaller/niche specialists, (d) existing-company cross-product and subsidiary/sales/contract exposure. Search by function, installation point, local industry terminology, competitors, order announcements, customer/industry sources and official IR. Do **not** stop just because two or three famous firms explain a role. Do not rely on analyst coverage or market cap as a discovery gate. Record included, excluded and held candidates with reasoning and evidence in `coverage_audits` and `candidates`. Read `references/discovery.md`.
4. **Verify company × product × business mode**. Check each discovered firm's *other sellable products* and subsidiaries in reverse, not just the product used to find it. Distinguish manufacturer vs supplier/distributor/integrator, contracting entity vs producer, and sales agreement/framework amount vs recognized revenue. Multiple HOME entries are allowed **where an economically material documented role exists**; if not verified, log a candidate HOLD rather than assume exclusion. Capture product-specific `claim_specifics`, `business_mode`, `business_stage`, `profit_mechanism`, dated evidence and product-level role. Identify cap/liquidity/market beta separately from segment earnings sensitivity; never fabricate event-beta calculations. Read `references/evidence.md`.
5. **Build HOME and nearest-peer blocks**. Group chiefly by WHERE+WHAT and SAME MONEY DRIVER. Distinguish direct competitors from financially relevant suppliers/channels and label product role explicitly. Preserve stable HOME order and global reference positions; **do not limit stock coverage to 2–6 large firms** (that is a visual heuristic, not a discovery limit). Additional specialists with distinct earnings exposure are welcome with defensible evidence. Maintain all candidate decisions and new cross-product memberships. Read `references/peer-and-order.md`.
6. **Construct selective EVENT transmission**. For each meaningful current event, explain the route to Q/P/MIX/SHARE/UTIL/COST/YIELD, then margin/EPS/FCF; include direct/indirect/competitive/alternative effects, stage, next indicator, and contradictory evidence. Only high-sensitivity companies go into EVENT display. Read `references/events.md`.
7. **Independent quality gate**. Apply `references/verification.md` including **role-level coverage**, logged small/mid-cap and overseas search, incumbent cross-product audits, included/held/excluded candidate decisions, meaningful non-placeholder product evidence, order vs recognized revenue and all prior unresolved holds. A superficially neat map or script `0 errors` does **not** certify no omitted firms. The audit must explicitly list uncovered groups and unknown EPS sensitivity; a missing search is a HOLD, not a `NO_MATCH_FOUND`. With Python, run `python scripts/validate_master.py audit <master.json>` and `python scripts/validate_master.py validate <master.json> --strict` (strict nonzero is expected if holds remain). Without Python, manually run the equivalent gate and state `AUTOMATED_VALIDATOR_NOT_RUN`. Reopen only affected steps and maintain earlier errors as regression cases.
8. **Render and export**. When execution is available, run `python scripts/validate_master.py render <master.json>`; otherwise create the same company-first preview. HOME value-chain sequence and EVENT earnings transmission sequence are separate. Do not suppress high-sensitivity small companies simply to meet a 2–6-firm layout target. Print a compact **coverage/QA summary** including unperformed search tracks, held/excluded candidates, unsupported product modes and broker holds. Confirm exact broker import format before outputting broker-specific file. Read `references/export.md`.

## Core decisions and stopping conditions

- No new group merely for an interesting material, process, theme, or customer; create a distinct economic block only when product/customer, ASP, margin, scarcity, qualification, or earnings sensitivity differ meaningfully.
- A **structurally important** company with weak direct EPS exposure can still be an essential industry-map or signal reference; distinguish CORE / STRUCTURAL / OPTION / SIGNAL at **company-product** level.
- A missing role is material if excluding it hides a major buying decision, integrator, substitute, bottleneck, or causal link. Search until such gaps have defensible representatives and additional candidates add little incremental understanding; log unresolved gaps.
- Prefer company/filing/IR for *what a firm actually sells*, independently triangulate for *market share, technical superiority, rival position and supply-chain relationships*. Newer verified operating data override older outlook, without erasing useful older mechanism/history.
- Never infer exact buyer–supplier relationships from a value-chain arrow without supporting evidence.
- Stop when essential product roles, global leaders, domestic small/mid-cap peer search, overseas specialist search, cross-product business review, candidate decisions, economic differences and negative cases are **documented as checked or explicitly held**. No fixed target company count, but an unsearched category never satisfies the stop condition.
- Output must distinguish `VERIFIED`, `ESTIMATED`, `OPTION`, and `HOLD`. Do not silently upgrade unsupported statements.

## Final deliverables

1. `MASTER` v0.2 with company × product × business mode, product-level evidence, cross-HOME assignments, role-coverage research trails, candidate inclusion/hold/exclusion decisions and status.
2. `HOME` and `EVENT` company-first watchlist preview.
3. `CHANGELOG` showing additions, removals, group moves, source and cause.
4. `QA` report showing **both structural errors and missing discovery work** (including unanswered small/mid-cap, overseas, cross-product or broker checks); broker-specific export **only after actual import format confirmation**.

A bundled Python validator **checks data structure, not market facts or omitted firms**. A full discovery audit requires actual searches and independent source review. The skill orchestrates available access/tools; it does not grant new Google Drive, securities account, or exchange entitlements. When a source or tool is unavailable, continue with admissible evidence and document the gap.
