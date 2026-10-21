# On-demand quality contract v0.9

## Purpose
Each user invocation must independently generate a **fresh, bounded, cited and decision-usable** industry/EVENT research snapshot, even with no earlier MASTER, queue, saved library, or automation. The user should not need to prime the agent with a policy headline. Report-led discovery is the primary generation method; the six lanes below audit missed categories. Persistence and completion of an editable broker MASTER are **orthogonal** concerns, not preconditions for quality.

## Delivery contract (read before output)

The first visible result must use **A. Industry chain and child-level explanation / B. named global peers with segmented revenue, product/role and earnings differences / C. independently discovered thematic event→earnings transmission**, consistent with `output-contract.md`. Log relevant sector-native-language and discovered analyst/Telegram channels per `source-scout.md`. Generic HOME/EVENT metadata without firm-by-firm economic comparability is not a completed map. Lack of segment financial disclosure is shown as unavailable, never fabricated.

## Discovery-first quality gate (read before any theme output)

- Did the run search **industry/theme research reports and high-depth company news first**, across both current and historical materials, rather than only recent top headlines or existing MASTER events?
- Did at least one material candidate theme have an accessible `origin_source` with actual report body/technology/customer/industrial narrative **or** an independently verified new primary breaking source? A report title alone is a *lead*, not a read. When none is accessible, state `REPORT_LED_SOURCE_LIMITED` and present only source-calibrated hypotheses.
- Did the run explicitly extract the report thesis, economic mechanism, affected product roles, adoption maturity, contrary drivers, and verify candidate firms in **appropriate country filings and independent company/customer IR** before promoting to confirmed? Did it avoid treating a sell-side target price/estimate as a company fact?
- Did the run supply at least one alternative report/news view and update judgments where contradictory evidence actually mattered? If not available label the missing risk rather than invent it.
- Does the final deliverable show actual HOME/EVENT with named companies and documented causes rather than just what to research next? The user must not need to seed the theme or issue a second command to obtain the first useful result.

## Mandatory coverage lattice (secondary gap check, not the discovery engine)

After generating theme hypotheses from reports, use a per-industry role grid (product/installation/customer/earnings drivers) with historical-to-current event scan across these lanes:
1. `POLICY_TRADE` (national origin, tax/incentive/security, China/non-China, regulation and implementation).
2. `DEMAND_CUSTOMER` (CAPEX, procurement, customer contracts, qualifications, shipment, timing).
3. `SUPPLY_PRICE` (capacity, scarcity, material price, utilization, lead time, competing capacity).
4. `TECH_SPEC` (technical specifications, qualification, substitutions, packaging, redesign).
5. `CAPACITY_EQUIPMENT` (capex/ramp, machine and consumables orders, yield, competing build-outs).
6. `COMPETITION_RISKS` (entrant/substitute, demand cancellations, legal exemptions, project delays, EPS counterexamples).

Each lane records one of `SEARCHED`, `NOT_MATERIAL` (with scope-specific reason), `UNAVAILABLE` (with access limitation). **Coverage search is not equivalent to finding an event.** Expand bilingual/sector-adjacent search terms when a critical lane is blank. Event scan should not depend solely on previous companies or user keywords. Date of event vs date of report vs date of verification must stay distinct.

## Evidence hierarchy and report selection

- Actual laws/regulations, filings, customer and supplier contracts/IR, technical specs and actual production/orders anchor hard facts. A reported contract or regulatory scope from analyst/student press is a *lead*, not verified until primary checked.
- Multiple broker/industry/KIRS/university reports reveal different causal mechanisms and counterarguments; same government release repeated across 5 houses is not 5 independent facts. University analyses are strong for value chain maps, weaker for unverified numbers and valuations.
- Telegram collector is discovery index; retrieve original PDF/statement when possible. News is for implementation, timing, industry behavioral change and falsification, not unconditional future earnings.
- Prioritize next source by filling a high-sensitivity missing event/product/company/EPS link or credible contradiction per unit effort. 100 total reads, 30/read capacity or a fixed mix are not quality thresholds. Reading receipts must reflect actual body read, not title.

## Output quality floor by request type

**INDUSTRY_MAP:** present nonempty product-role HOME and actual company peers *and* autonomously discovered material EVENT candidates with company impact, including negative cases. If no supported major event is located after independent search, explicitly state that; do not synthesize events to fill space. The industry watchlist must be usable without viewing a separate research log.

**EVENT_SCAN:** present dated, cited event candidates ranked for significance, product/firm mapping, and for each supported event a causal earnings bridge, confirmation level, credible contrary case and next indicator. Missing MASTER only reduces ability to claim prior-vs-new delta; it doesn't prohibit finding current events. 'New' means new to this verified run or newly observed versus a **verified accessible** prior registry; do not falsely claim never-before-seen.

At minimum report: (1) freshness/as-of with original event dates, (2) source/provenance IDs/links, (3) actual search axes and limitations, (4) product and company economic roles, (5) one real contrary/risk path for material claims (or explicit not independently verified), (6) factual vs analyst forecast vs inference, (7) output delivered in this run even if checkpoint failed.

If tooling/data accessibility prevents a robust industry view, **lower the certainty label**, do not relax evidence checks or claim identical accuracy. A precise lower-coverage report is better than a fabricated comprehensive one. Do not request user permission for routine authorized reads/research, and do not create automated scheduled tasks without explicit request.

## Evaluation to calibrate repeatability

Maintain **fixed benchmark prompts** on three different industries, e.g. power equipment, electronic substrates, ESS. For each prompt run from new empty chat as well as with existing MASTER, at two different times/contexts where feasible. Compare independent coverage of product roles, independently found major EVENTS, trustworthy primary-source tracing, firm×product economics, contradictory views, and visible uncertainty. Do not assume skill instructions alone guarantee invariant output; actual repeated executions are the required test.

## Optional local structural checker

`python scripts/validate_snapshot.py snapshot.json` checks a compact verifiable **delivery record**: source identities/verified recency, search coverage, company+product link, key EVENT fields, independent narrative check, and immediate output. It cannot fetch new facts or guarantee recall of every firm/event. If Python cannot be used, perform the same checklist manually and say so.
