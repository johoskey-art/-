# Persistent research state (v0.7)

**No new breaking master schema is required.** Keep existing fields `companies, groups, company_product_claims, event_registry, news_audits, sources, candidates, report_queue, coverage_audits, report_corpus_audit, change_log` whenever available. Write new work under `schema_version: "0.7"`; older datasets load in backward-compatible mode.

Recommended minimal `research_state`:

```json
{
  "industry": "전력기기",
  "as_of": "2026-10-21",
  "status": "IN_PROGRESS",
  "verified_checkpoint_uri": null,
  "last_readback_ok": false,
  "actual_unique_body_reviewed": 0,
  "top_unresolved_questions": [],
  "latest_home_event_delta": [],
  "last_checked_news_events": [],
  "next_high_value_reports": [],
  "persist_result": "STATE_NOT_PERSISTED"
}
```

When the user's storage connector can write, store only authorized private research metadata, no illicit copies of licensed reports, then READ BACK and set `last_readback_ok=true`. Otherwise provide a portable JSON attachment and mark state not persisted. On resume, never recreate the last-read index from a guess. `report_queue` includes stable source IDs, dedupe key, actual read receipts, time and specific findings. An optional PDF target should not be set unless user asks.
