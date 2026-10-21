# REPORT CORPUS RESEARCH v0.5 — priority-ranked, not quota-driven

## Outcome standard
A high-quality industry audit does NOT require exactly 100 PDFs, and reading 100 does not establish completeness. The default **100 is a planning ambition**, not a pass threshold or excuse to read duplicated/irrelevant reports. First rank by expected marginal investment information, then review as many unique source bodies as needed to close meaningful role/event/EPS/contradiction gaps. Always report actual reads and major unsearched regions.

## Catalog widely BEFORE reading
Search dated and historical reports and adjacent sectors, across Drive, public brokers, international sell-side/industry bodies, corporate IR, Telegram collector originals, KUVIC/SMIC/S.T.A.R. and KIRS. Build an indexed prioritized queue, title and paper date, issuer, subtype, source URL/file ID, estimated relevance, digest/hash if available, event hypotheses, and current read status. Don't stop search merely because a Drive query returns 35 results; page and broaden into folder and topic/date combinations.

## Resume as a user-facing workflow
Commands supported in natural language after `@Industry Watchlist Builder` selection:

- `CORPUS START 전력기기 PRIORITY` (optionally `TARGET 100`) — create/update the industry's persistent queue without clearing existing confirmed report reads; broaden source discovery.
- `CORPUS NEXT 10 PRIORITY` or `CORPUS NEXT 20 PRIORITY` — read the next **unique unread** PDF reports. N is a *request*, not a guarantee; the execution stops after actual work capacity, preserving exact remaining items. Do not repeat completed documents. Prefer varied sources and new/contradictory theses. If a PDF is long, use fewer reports per batch and accurately log status.
- `CORPUS NEXT 10 UNIVERSITY` — prioritize student reports. `CORPUS NEXT 10 TELEGRAM` — prioritize saved collector **original** PDF attachments, not forwards. `CORPUS NEXT 10 GLOBAL` — prioritize external international research. `CORPUS NEXT 10 KIRS` — prioritize Korea IR Council reports.
- `CORPUS STATUS` — return catalog size, verified substantive reads, current ranked top 10 unread documents *with reasons*, major remaining coverage gaps, source balance, duplicate count, and progress toward optional 100 ambition.
- `CORPUS EVENT AUDIT` — form canonical EVENT registry from already read docs, flag coverage gaps and negative cases. It does **not** imply that target=100 was met.
- `CORPUS FINALIZE` — evaluate coverage, contradictions, information-value saturation, highest-impact unread candidates, and remaining blockers. Never use a pure numeric threshold as the sole success condition. Otherwise output interim HOME/EVENT with explicit research HOLD and next commands. No auto-magic background ingestion.

## What counts as a PDF read
A PDF report is counted only if a read receipt documents:
1. Original or authenticated PDF was **actually opened and inspected**. Stable source/document ID, report date, issuer, public/Drive URL, and dedupe hash or normalized bibliographic identity.
2. `document_type: PDF_REPORT`, `status: BODY_REVIEWED` (targeted actual report-body review) or `DEEP_READ` (broad full document analysis), `read_log.reviewed_at`, `read_log.reader`.
3. At least **two different substantive body sections** (e.g., product/spec & company competition, regulation & earnings model, tables & counterarguments) and at least two **concrete findings of ≥18 characters each**.
4. Two or more identifiable report page numbers/chart/table/section locators. Model-generated guesses about page numbers do not count. If the PDF has no reliable page numbers, use original headings or quoted section labels and mark locator type.
5. Each finding classified and linked to an EVENT/ROLE/COMPANY or rejection; numbers originating in student reports require a factual verification ticket.

Opening only title/TOC/abstract, inferring content from filename, reading a Telegram message or copied summary, using an unread legacy report-corpus audit count, or reading duplicated copies must **not** increment the counter. Log inaccessible scans `UNAVAILABLE` with details. Do not label target-only reading as full-text if not all material body reviewed.

## Batch selection
Sort by **expected information value**: urgent missing industrial role or material EVENT, thesis novelty, investment sensitivity path, independent evidence, contradictions, then source diversity and recency. Re-rank each NEXT batch after its findings are indexed; no rigid source quotas. A batch of 5–10 may be comfortable for lengthy reports, but this is **never the total research threshold**. The user may ask NEXT 15/20/30; honor as many as can actually be substantively read, checkpoint progress, and state completed count. If a batch request exceeds execution capacity, mark remaining still queued rather than silently misrepresenting completion. Do not force the user to guess the right number or repeatedly pick files manually.

## Durable storage
Persist a private `REPORT_QUEUE_<industry>.json` containing items/read receipts; record every batch's completed IDs, next unread IDs, source-coverage audit and event registry delta. Prefer connected private Google Drive and **verify write/read-back** each batch. If writing is unavailable, provide generated checkpoint JSON (and current status) and tell the user to reattach it to continue. Never claim cross-session continuity from a mere chat summary. Do not upload private collector exports, licensed complete PDF bodies or personal holdings to public GitHub. Public GitHub can hold the generic reader/validator scripts and synthetic fixtures.

## Deduplication & idempotence
Prefer content SHA256 of the original PDF, otherwise known source report ID / canonical issuer+date+normalized original title. Same pdf in Telegram, Drive and original site = one unique read. A new dated/materially revised report version can count separately only with explicit delta and version identifier. Imported claims from a document don't become independent evidence when repeated by several later reviews.

## Source-specific rules
Consult `references/source-diversity.md`. Student/KUVIC/SMIC/S.T.A.R. and Korea IR Council reports have high discovery value for obscure firms and the physical value chain but their valuation targets, market-share estimates, sales forecasts and obscure named customer assertions require primary-source check. Telegram text is a discovery/search surface; save source-channel/time/file URL and open the original PDF before counting.

## Event temporal lineage
Across corpus searches preserve each canonical event's first report, later issuer-specific thesis changes, policy primary source and formal effective/enforcement dates, alternative explanations, and current status. Several analyst reports repeating one EO are not independent official confirmations. Revisit only reports where the legal status changed or meaningful missing product exposure is found.

## Stop condition
If fewer than 100 genuinely informative distinct reports exist, do not read weak duplicates merely to fill the quota. A smaller corpus may support a conditional completion after coverage and evidence-saturation audit; show its true size and remaining uncertainties. If over 100 are needed to close important gaps, continue. Never fabricate read receipts. Official legal and financial verification are mandatory regardless of report count.

## Priority evaluation
Read `reading-priority.md` for the two-pass selection rubric, deterministic queue signals, coverage-matrix reassessment and conditional research completion gate. `priority_reason` must explain why opening this PDF can alter HOME, EVENT, company EPS driver, negative case, or verification. A low-value title doesn't become more valuable just because the count is below 100.
