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

## 실측 처리 능력과 Work 분업 필드 (v0.8, optional)

`execution_log`는 실행별 관측값을 저장하며, 숫자는 실제 완료한 영수증 수만 기록한다. `planned_count`를 `completed_count`로 복사하지 않는다.

```json
{
  "execution_log": [
    {"run_id":"example-1", "environment":"CHAT", "attempted_count":5, "completed_count":3, "completed_ids":["Q1","Q2","Q3"], "readback_ok":true, "failed_count":2, "blockers":["PDF_ACCESS"], "measured_at":"2026-10-21"}
  ],
  "capacity_gate": {"route":"PILOT_NEEDED", "basis":"실측값 없거나 최초 시도", "next_scope":"고정보다 실제 소화량에 맞춤"},
  "work_handoff": {"status":"NOT_PREPARED", "artifact_uri":null, "work_result_verified":false}
}
```

`handoff.status`는 `HANDOFF_PREPARED`, `WORK_STARTED`, `WORK_COMPLETED_UNVERIFIED`, `WORK_RESULT_ACCEPTED` 중 하나를 사용하며, Work가 실행되었는지 사용자가 확인하거나 결과 증거가 있을 때만 갱신한다. 사용자 계정의 Work 접근 상태를 모르면 자동 사용 가능하다고 단정하지 않는다.
