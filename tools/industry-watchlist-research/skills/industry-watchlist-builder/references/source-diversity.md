# Research source diversification — v0.4

## Discovery families (search even when Drive archive is large)

1. **DRIVE_ARCHIVE:** user's authenticated Google Drive historical and current PDF reports. Search filenames, subfolders, abbreviations, related sectors, release month/year, authors, and firm names. Deduplicate same PDF uploaded in several locations. Do not interpret last-modified as report date.
2. **PUBLIC_WEB:** publicly accessible Korean and overseas broker PDFs, industry deep dives, industry organizations, sector newsletters. Follow original/public download links when access permits, preserving publication date and source. Do not bypass authorization, paywalls or robots access rules; unavailable=HOLD.
3. **GLOBAL_IR:** annual/quarterly reports, investor days, presentations, earnings, catalogs, customers, suppliers, industry bodies. These documents may be PDFs and count towards the 100 if they meet the PDF report-review criteria, but record as primary corporate documents, not independent sell-side analyst confirmations.
4. **TELEGRAM_COLLECTOR:** use user's authorized saved collector exports where available, especially Drive folder `텔레그램 수집 자료` (located in the current user research history) / `날짜별 텍스트`, `외사 리포트`, `OCR 텍스트`, attachments JSON/HTML, and original saved report PDFs. First identify reposts and original source/report URLs, then **open the report body**. Telegram excerpts/forwards are discovery leads and cannot count as distinct PDF reports nor as independent corroboration. Never suggest direct Telegram access without a connected Telegram source; if private feed inaccessible, record a hold.
5. **UNIVERSITY_RESEARCH:** intentionally query the original published reports of **KUVIC (Korea University), SMIC (student research club; distinguish from Semiconductor Manufacturing International Corporation), Sungkyunkwan University S.T.A.R.**, and other relevant finance/investment research groups. Discover undercovered small caps, product-role diagrams, niche customers and policy-event hypotheses. Read the actual PDF, not just a forwarded abstract. Always treat novel company-product/customer claims as hypotheses until checked.
6. **KIRS:** Korea IR Council / 한국IR협의회 기업리서치센터 industry/technology/company PDFs and KRX reports. Good for overlooked small caps, industrial installation/process explanation and business history. Still distinguish estimates/management claims from audited facts and confirm current business status.
7. **PUBLIC_REGULATOR:** official law/regulation/order and enforcement agency primary texts (U.S. Federal Register, White House, DOE/FCC/FERC, EU official sites etc), trade agencies/standard bodies, and regulatory updates; these establish actual scope. A law webpage is not automatically a PDF report for the quota.

## Differential evidence weighting (by *claim type*, not prestige)

- Industrial taxonomy, physical equipment role, process illustration, installation position, optional substitutes: analyst, student club and KIRS detailed technical works are valuable **discovery and topology sources**; cross-check if contradictory.
- Precise segment revenue, margins, capex, backlog, raw EPS valuation, TAM/share, customer relationship or contract amount: independently verify via official audited filings, current IR, customer disclosure and primary contracts. No student valuation, price target or forecast should be promoted to FACT without verification.
- Government events: obtain exact original legal document and implementing documents; do not derive enforceable bans just by many papers repeating a thesis.
- Conflicting figures: keep both, state why assumptions/date/units differ, adjudicate or HOLD.

## Retrieval workflow and result accountability

For every family, document: query/site/folder, search execution date, matching PDF count, accessible original count, unique substantive reviewed count, unavailable count and open questions. Diversification is a **search completeness gate**, not a mandatory count per publisher.

If a source returns a massive text/collector file or hundreds of attachments, first index daily metadata/events and original PDF links, then read selected PDFs in the prioritized queue. Do not scan one huge export and call all embedded citations 'read'. A PDF report's `read_log` must carry 2+ inspected body sections and 2+ concrete source locators. This is not a claim that *every page* was read unless `DEEP_READ` is correctly recorded.

## Avoid circular or duplicate evidence

KUVIC student PDF forwarded in Telegram and separately backed up in Drive = ONE report. Multiple reports citing the same policy are independent analyses but not independent legal confirmations. A revised edition may count separately only with publication dates and material content changes. Prioritize truly dissimilar views (different house, product scope, forecast mechanism, negative thesis) in queue ordering, then broad full-coverage.
