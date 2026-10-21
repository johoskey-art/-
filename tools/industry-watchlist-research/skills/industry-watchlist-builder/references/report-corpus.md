# REPORT CORPUS RESEARCH v0.4 — ≥100 distinct substantive PDF reports

## Outcome standard
An **industry-comprehensive audit** targets **at least 100 unique on-topic PDF reports with substantive body-review evidence**, not 100 Drive search hits, 100 abstracts, repeated PDFs, or 100 references in Telegram. There is **no fixed upper limit**, and the 100 threshold is a research-fidelity floor, not proof that every meaningful event or company has been found. The user may request a preliminary map before the 100 are reached; mark PROVISIONAL and show actual `N/100`.

## Catalog widely BEFORE reading
Search dated and historical reports and adjacent sectors, across Drive, public brokers, international sell-side/industry bodies, corporate IR, Telegram collector originals, KUVIC/SMIC/S.T.A.R. and KIRS. Build an indexed prioritized queue, title and paper date, issuer, subtype, source URL/file ID, estimated relevance, digest/hash if available, event hypotheses, and current read status. Don't stop search merely because a Drive query returns 35 results; page and broaden into folder and topic/date combinations.

## Resume as a user-facing workflow
Commands supported in natural language after `@Industry Watchlist Builder` selection:

- `CORPUS START 전력기기 TARGET 100` — create/update the industry's persistent queue without clearing existing confirmed report reads; broaden source discovery.
- `CORPUS NEXT 10` or `CORPUS NEXT 20` — read the next **unique unread** PDF reports. N is a *request*, not a guarantee; the execution stops after actual work capacity, preserving exact remaining items. Do not repeat completed documents. Prefer varied sources and new/contradictory theses. If a PDF is long, use fewer reports per batch and accurately log status.
- `CORPUS NEXT 10 UNIVERSITY` — prioritize student reports. `CORPUS NEXT 10 TELEGRAM` — prioritize saved collector **original** PDF attachments, not forwards. `CORPUS NEXT 10 GLOBAL` — prioritize external international research. `CORPUS NEXT 10 KIRS` — prioritize Korea IR Council reports.
- `CORPUS STATUS` — return catalog size, eligible unique PDF report reads, incomplete receipts, duplicate forwarding count, read mix by source, unread highest priority titles, and `100-N` remaining.
- `CORPUS EVENT AUDIT` — form canonical EVENT registry from already read docs, flag coverage gaps and negative cases. It does **not** imply that target=100 was met.
- `CORPUS FINALIZE` — produce comprehensive assessment **only** if 100 distinct verified read receipts and other evidence gates pass. Otherwise output interim HOME/EVENT with explicit research HOLD and next commands. No auto-magic background ingestion.

## What counts as a PDF read
A PDF report is counted only if a read receipt documents:
1. Original or authenticated PDF was **actually opened and inspected**. Stable source/document ID, report date, issuer, public/Drive URL, and dedupe hash or normalized bibliographic identity.
2. `document_type: PDF_REPORT`, `status: BODY_REVIEWED` (targeted actual report-body review) or `DEEP_READ` (broad full document analysis), `read_log.reviewed_at`, `read_log.reader`.
3. At least **two different substantive body sections** (e.g., product/spec & company competition, regulation & earnings model, tables & counterarguments) and at least two **concrete findings of ≥18 characters each**.
4. Two or more identifiable report page numbers/chart/table/section locators. Model-generated guesses about page numbers do not count. If the PDF has no reliable page numbers, use original headings or quoted section labels and mark locator type.
5. Each finding classified and linked to an EVENT/ROLE/COMPANY or rejection; numbers originating in student reports require a factual verification ticket.

Opening only title/TOC/abstract, inferring content from filename, reading a Telegram message or copied summary, using an unread legacy report-corpus audit count, or reading duplicated copies must **not** increment the counter. Log inaccessible scans `UNAVAILABLE` with details. Do not label target-only reading as full-text if not all material body reviewed.

## Batch selection
Sort by novelty/role gaps/event contradiction, then source diversity, document length and publication time. A batch of 5–10 may be comfortable for lengthy reports, but this is **never the total research threshold**. The user may ask NEXT 15/20/30; honor as many as can actually be substantively read, checkpoint progress, and state completed count. If a batch request exceeds execution capacity, mark remaining still queued rather than silently misrepresenting completion. Do not force the user to guess the right number or repeatedly pick files manually.

## Durable storage
Persist a private `REPORT_QUEUE_<industry>.json` containing items/read receipts; record every batch's completed IDs, next unread IDs, source-coverage audit and event registry delta. Prefer connected private Google Drive and **verify write/read-back** each batch. If writing is unavailable, provide generated checkpoint JSON (and current status) and tell the user to reattach it to continue. Never claim cross-session continuity from a mere chat summary. Do not upload private collector exports, licensed complete PDF bodies or personal holdings to public GitHub. Public GitHub can hold the generic reader/validator scripts and synthetic fixtures.

## Deduplication & idempotence
Prefer content SHA256 of the original PDF, otherwise known source report ID / canonical issuer+date+normalized original title. Same pdf in Telegram, Drive and original site = one unique read. A new dated/materially revised report version can count separately only with explicit delta and version identifier. Imported claims from a document don't become independent evidence when repeated by several later reviews.

## Source-specific rules
Consult `references/source-diversity.md`. Student/KUVIC/SMIC/S.T.A.R. and Korea IR Council reports have high discovery value for obscure firms and the physical value chain but their valuation targets, market-share estimates, sales forecasts and obscure named customer assertions require primary-source check. Telegram text is a discovery/search surface; save source-channel/time/file URL and open the original PDF before counting.

## Event temporal lineage
Across corpus searches preserve each canonical event's first report, later issuer-specific thesis changes, policy primary source and formal effective/enforcement dates, alternative explanations, and current status. Several analyst reports repeating one EO are not independent official confirmations. Revisit only reports where the legal status changed or meaningful missing product exposure is found.

## Stop condition
If fewer than 100 relevant unique accessible PDF reports exist even after cross-source discovery, report accessible counts, held/out-of-scope reasons and the search methods. Never fabricate 100 reads. Give interim assessment, not bogus `COMPREHENSIVE_RESEARCH_COMPLETE`. A separate source-diversity/open-event legal check remains mandatory after hitting 100.
