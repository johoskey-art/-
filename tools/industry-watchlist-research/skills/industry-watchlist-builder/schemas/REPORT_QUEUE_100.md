# v0.5 private report queue schema — prioritized reading

`report_queue` is an object `{ "target_unique_body_reviewed": 100, "selection_policy":"INFORMATION_VALUE_FIRST", "checkpoint_reference": "private Drive URL verified on readback", "items": [...], "selection_audit": {...}, "research_decision": {...} }`. The 100 is an optional breadth aspiration, not the definition of completion.

Each report:
```
{
  "id": "a_stable_source_id", "title": "Original title", "issuer": "Original issuer",
  "report_date": "2026-09-14", "source_uri": "authenticated-or-public-real-url",
  "document_type": "PDF_REPORT", "origin": "UNIVERSITY_RESEARCH",
  "content_sha256": "optional actual sha256 of original PDF, not invented",
  "dedupe_key": "optional stable provider original-report edition ID",
  "status": "BODY_REVIEWED", "priority": 1,
  "coverage_tags":["PRODUCT:PCS","EVENT:US_POWER_SECURITY"],
  "priority_reason":"Potential unique product economics / evidence; preliminary",
  "priority_signals":{"role_or_event_gap":4,"expected_new_mechanism":4,"primary_evidence_potential":3,"earnings_bridge":4,"contradictory_view":1,"time_sensitive_update":2,"topic_relevance":5,"redundancy_risk":0},
  "read_log": {
    "reader": "assistant", "reviewed_at": "2026-10-21",
    "sections_reviewed": ["ESS system structure", "Policy-driven cell suppliers"],
    "locators": ["original PDF p. 12 §ESS system", "original PDF p. 28 table 7"],
    "findings": ["Concrete role/policy observation with attribution", "Another material independent finding / counterargument"],
    "full_text_read": false,
    "claims": [{"type":"HYPOTHESIS","topic":"ESS","needs_independent_verification":true}],
    "event_ids": ["US_GRID_SECURITY_EXAMPLE"]
  }
}
```

If only filename/summary/Telegram excerpt read, use `CATALOGUED` and **omit `read_log`**. `BODY_REVIEWED` means source body sections genuinely read, not every page. `DEEP_READ` means the complete substantive report was analyzed; do not mislabel. Original PDF forwarded many times counts once; prefer content hash, else normalized original title+publisher+date. A regulator webpage/Telegram message is not `PDF_REPORT`.

`source_search_audit` contains seven `{family,status,query_or_method,as_of,notes}` records: DRIVE_ARCHIVE, PUBLIC_WEB, GLOBAL_IR, TELEGRAM_COLLECTOR, UNIVERSITY_RESEARCH, KIRS, PUBLIC_REGULATOR. The `source_search_audit` is separate from PDF quota and the preexisting `report_corpus_audit` axes.

`report_queue.py` is only a deterministic metadata counter and next-candidate selector; it cannot read PDFs or verify truth. Access to Drive/web and persistence must be performed by the authorized host execution environment. `NEXT` **must fetch/read original PDF before marking receipt**. Verified private storage is required for cross-session continuation.

To record actual progress using the local helper:

```
python scripts/report_queue.py init /private/industry-report-queue.json --target 100
python scripts/report_queue.py import /private/industry-report-queue.json --input candidate_reports.json
python scripts/report_queue.py next /private/industry-report-queue.json --count 20
# only after actually reading each report body and writing a fully grounded receipt file:
python scripts/report_queue.py mark /private/industry-report-queue.json --input read_receipt.json
python scripts/report_queue.py status /private/industry-report-queue.json
```

This file should remain in private storage. `import` never marks documents read; `mark` rejects missing actual reading evidence, although it still cannot independently attest that the assistant actually read the report. The user-facing ChatGPT command uses the same state transitions by available connector actions, not a promise that local Python executes on Android.

## Priority and stop audit
`selection_audit.dimensions[]` should cover ROLE_PRODUCT, EVENT_POLICY, HISTORIC_CURRENT, COMPANY_EPS, CONTRADICTION, GEOGRAPHY, SOURCE_DIVERSITY with `status:REVIEWED` and provenance/notes or a reasoned `JUSTIFIED_NOT_APPLICABLE`. Track `critical_gaps` explicitly.

`research_decision` must contain `decision: CONTINUE|SATURATED|COVERAGE_CONFIRMED|BLOCKED`, `reason`, `as_of`, `last_batches` (per-batch number of new material event nodes, firms/products, independent confirmations and contradictions), `high_value_unread_review` (titles and why they do or do not change decisions), and `unresolved_critical_gaps`. A declaration without real source investigation is not proof of completeness. The numeric count can be below/above 100 while the quality gate remains independently open/closed.

Ranking fields of *unread* documents are speculative title/abstract judgments only. Never upgrade them to fact evidence until actual body read. The queue selects using these factors and possible coverage tags.
