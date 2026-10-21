# NEWS NARRATIVE STRESS TEST — EVENT 중간 검증 (v0.6)

## 가장 중요한 위치

**리포트/과거 근거로 EVENT 후보와 공식 원문을 확인한 후, 기업별 수혜/EPS 경로를 확정하기 전** 뉴스로 해당 내러티브가 실제 세계에서 어떻게 나타나는지 점검한다. 이후 **최종 HOME/EVENT 출력 직전** 주요 변경점과 위험신호를 다시 확인한다. 뉴스만으로 처음부터 투자 테마를 만들어 결론 내리면 안 된다.

1. **선행 스캔 (optional discovery)**: 최신·과거의 뉴스/텔레그램 텍스트로 잠재 EVENT, 뜻밖의 계약·프로젝트 지연, 규제 집행, 경쟁자 등장 발견 → 독립 원문 추적. 이 단계 뉴스는 아직 증거가 아닌 단서.
2. **PRE_BENEFICIARY (mandatory on ACTIVE/WATCH major EVENT)**: 증권사 다중 보고서에서 만든 전망을 대상으로 최근 뉴스가 *어디를 확증하거나 반박하는지* 검사하고 기업 매핑을 바꾼다.
3. **PRE_RELEASE (mandatory on ACTIVE/WATCH major EVENT)**: 최종 답변/MASTER 배포 직전에 지난 검사 이후 새로운 원문·계약·지연·정책 해석이 나왔는지 검색. 변동 없음도 검색범위·검증일을 기록한다.

## 조사 절차

- 정책: 공식 정부 원문/시행 규칙/집행기관 발표를 먼저 체크. 2차 뉴스 헤드라인의 `전면 퇴출`, `즉시 발효` 등은 대상·조건·예외·집행일 검증 전에는 사실로 채택하지 않는다.
- 기업: 공시·수주계약·고객사 채택·공장 가동·가격·납기·발주 지연·취소·재고·현지 생산·인증을 확인. **소식 → 물량 → 매출인식 → 영업이익** 간 시차를 강제로 분리한다.
- 반론: 비수혜/피해/수혜 지연 시나리오, 대체 공급부족, 가격 경쟁, 수요 중단, 내수/수출/원산지 예외를 적극 검색한다. 비판 기사가 없더라도 원문 기반 risk case를 만들어 '아직 관측 못 함'으로 표시한다.
- 독립성: 기사가 10개여도 통신사 원문 1건을 재전재하면 **독립 사건 1개**다. 게시일과 실제 사건 발생일을 별도 기록; 구 뉴스가 최근 재유통됐다는 이유로 신규 EVENT를 만들지 않는다. 텔레그램은 원문 위치를 찾는 탐색기, 팩트 검증은 원문·독립 확인으로 한다.
- 보고서와 비교: `REPORT_THESIS → NEWS_OBSERVATION → PRIMARY_VERIFICATION → BENEFICIARY_RECLASSIFICATION`. 명백한 확인·반증·혼재·추가 관측 없음 중 하나로 판정. 새로운 중요 기사/상충 주장이 있으면 기존 `EVENT_REGISTRY`를 수정하고 관련 제품·기업만 재검산한다.
- 실적 전이: 규제 제품 여부, 경쟁사 퇴출/지연의 실제 적용, 현지 적격 생산·납기·물량, 계약기업·제조기업 구분, 높은 관련 사업 매출 비중을 확인하기 전에는 강한 EPS 수혜 선언 금지.

## news_audits[] 기록 형식

각 중요 EVENT의 필수 확인 지점마다 한 행:

```json
{
 "event_id":"CANONICAL_EVENT_ID",
 "stage":"PRE_BENEFICIARY",
 "status":"CHECKED",
 "checked_at":"2026-10-21",
 "time_window":"last 45 days plus origin date, justified per event",
 "query_or_method":"official agency + named company + opposing industry news search",
 "source_ids":["NEWS_SOURCE_OR_PRIMARY_SOURCE_ID"],
 "independent_origin_ids":["ORIGINAL_STORY_ID_OR_AGENCY"],
 "positive_signal":"confirmed order / no confirmed order observed",
 "negative_signal":"project deferrals or missing export qualification / not found despite search",
 "narrative_verdict":"MIXED",
 "narrative_delta":"A regulatory headline exists, but replacement order timing uncertain",
 "primary_verification":"VERIFIED",
 "next_indicator":"next agency guidance or quarterly order disclosure"
}
```

`status`: `CHECKED` / `OPEN` / `NOT_APPLICABLE` (reason required). `narrative_verdict`: `CONFIRMING` / `CONTRADICTING` / `MIXED` / `NO_OBSERVABLE_CHANGE`. `primary_verification`: `VERIFIED` / `PARTIAL` / `HOLD`. `PARTIAL`/`HOLD` mark unresolved claims and prevent confirmed-beneficiary language. If original news cannot be opened, status `OPEN` and `NEWS_AUDIT_HOLD` — do not fabricate findings. No fixed minimum news count; quality and contrary-source search matter.

## Output

Per EVENT give a compact, decision-relevant delta rather than headline dump: `원래 주장 / 새로 관측한 것 / 반대 근거 / 기업 영향(+·0·−·?) / EPS 반영 시점 / 다음 확인`. State dates and independent original sources. Prioritized news must be fresh enough to address the event's turning point, not necessarily within a universal 24h limit; explicitly report source age.
