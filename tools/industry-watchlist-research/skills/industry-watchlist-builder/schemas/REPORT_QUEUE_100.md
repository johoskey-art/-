# v0.4 private report queue schema

`report_queue` is an object `{ "target_unique_body_reviewed": 100, "checkpoint_reference": "private Drive URL, only after verified write/readback", "items": [...] }`.

Each report:
```
{
  "id": "a_stable_source_id", "title": "Original title", "issuer": "Original issuer",
  "report_date": "2026-09-14", "source_uri": "authenticated-or-public-real-url",
  "document_type": "PDF_REPORT", "origin": "UNIVERSITY_RESEARCH",
  "content_sha256": "optional actual sha256 of original PDF, not invented",
  "dedupe_key": "optional stable provider original-report edition ID",
  "status": "BODY_REVIEWED", "priority": 1,
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
