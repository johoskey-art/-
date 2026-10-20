# Role-based discovery & mandatory coverage audit (v0.2)

The objective is not a small elegant list of widely covered leaders, nor a mechanically large watchlist. A product role is *not researched* until comparable public companies and meaningful challengers have been searched for at multiple sizes and geographies. Missing coverage is a research HOLD, not evidence that no firms exist.

## Discovery sequence

1. Load previous industry HOME/MASTER, explicit inclusion/exclusion, previous candidate and exclusion logs. Preserve stable groups.
2. Read recent domestic **and foreign** industry research, industry-body publications, and global leader IR / annual reports. Use report graphs and product comparisons to form focused questions. No sell-side coverage is required for a company to qualify.
3. Build an initial **product and economic-role** map: upstream inputs, equipment/enablers, finished equipment, integration/installation, distribution/customer; include substitutes and branches. Do not treat themes/technologies/regions as same-level HOME products.
4. For **each material existing and discovered product HOME**, execute and document four discovery tracks:
   - `GLOBAL_LEADERS`: global leaders / pure plays / directly competing incumbents; official filings and product catalogs.
   - `DOMESTIC_SMALL_MID`: smaller and mid-cap domestic specialists, recent contract winners, niche manufacturers, suppliers and relevant listed subsidiaries. **Do not use high capitalization or analyst coverage as an inclusion precondition.**
   - `FOREIGN_SPECIALISTS`: small and mid-cap overseas names, Taiwan/Japan/China/U.S. niche peers, second-tier challengers, global competitors and substitutes.
   - `INCUMBENT_CROSS_PRODUCT`: for **every discovered company**, review its *other important sellable product lines*, subsidiaries, channel/sales/distribution/supply contracts, and recheck whether it belongs in an additional HOME. A company's original HOME does not forbid other credible positions.
5. Search each track with role-led product keywords, local naming variants, competitor/customer IR, distributor/installation networks, project award announcements, technical catalogs and filings. Repeat only when a meaningful role is unrepresented or a new source changes the underlying economics. Keep query/method, date, evidence refs, candidates and disposition.
6. For product exposures distinguish `MANUFACTURER`, `SUPPLIER`, `DISTRIBUTOR`, `INTEGRATOR`, `INSTALLER`, `SERVICE`, `OTHER`. A listed channel entity with a disclosed supply contract may have meaningful earnings exposure *without owning production*. Do not incorrectly label it a manufacturing peer. A group may include a differentiated distributor/supplier where useful, with role annotated.
7. Investigate every candidate's product, direct customer/end market, commercial stage, economics and listing. Distinguish primary company revenue from a small product option; verified existence is not proof of high EPS sensitivity. Record inclusion, hold, exclusion with source and reason.
8. Close each role audit only after major material roles, global and local rivals, domestic small/mid, foreign specialists, subsidiary/channel connections and alternatives have been considered. The outcome may be `NO_MATCH_FOUND` (documented search) or `NOT_APPLICABLE` (reasoned), never silent omission. If new searches add no economically differentiated names, stop. No arbitrary company-count target.

## Mandatory coverage output

Produce `coverage_audits[]` per HOME with four research tracks, status `CLOSED` or `OPEN`, and research provenance. Produce `candidates[]` including excluded/held candidates (do not silently drop). Every newly discovered product of an incumbent must appear as a company×product claim and HOME membership **or** as a recorded hold/exclusion with why.

## Two-way audit

- **Role → Company**: who builds/sells/distributes/installs/maintains this product? What mid/small public competitor is missing? Who benefits from an unexpected project/order/spec shift?
- **Company → Role**: what does each company *actually* sell through subsidiaries, contracts, service/channel roles, and optional businesses? Which second/third HOME would matter economically?

Sample failure mode: a cable maker is already on the list, but its subsidiary is a contractual busway supply/channel participant. A one-HOME-only search may miss that. Review the agreement, contracting entity, manufacturing entity and revenue attribution, then keep cable as primary HOME and add busway exposure only with adequate evidence, marking it as `SUPPLIER` rather than producer.

## Signal and beta-aware candidate review

High *stock beta* is **not** the same as high earnings sensitivity to the industry event. When measurable, capture: market capitalization/float and liquidity (date/source), segment exposure, backlog/order change, incremental sales-to-operating-profit leverage, margin, pricing power, and customer concentration. Mark speculative or unmeasurable values `UNVERIFIED`; never invent quantitative ranks or EPS sensitivities. Micro/small-cap stocks can be CORE, STRUCTURAL, OPTION or SIGNAL based on actual **company×product** evidence.
