## v0.7 — 정보가치 중심 조사 및 간단 사용법
- 두 가지 기본 자연어 요청: `산업지도 만들어줘/최신화해줘`, `계속 조사해줘`. 세부 지시를 사용자가 외우지 않음.
- 100건은 선택적 목표이지 통과 기준이 아님. 후속 보고서를 점수와 검증 공백에 따라 선정하고 비공개 읽기 원장을 재확인.
- 관련한 외부/텔레그램 원본/KUVIC/SMIC/S.T.A.R./KIRS 자료를 필요에 따라 선택하고 숫자/계약은 공식 자료로 검산.
- Offline research queue, source diversity audit, v0.4 validator warnings for uncompleted corpus.

# Acceptance tests BEFORE treating skill as production ready

1. **User boundary**: Given 'electronics excluding semiconductor test', no ISC/TSE/semiconductor socket companies enter HOME or EVENT regardless of report content. No adding new categories unrequested.
2. **Missing major company**: Given BTM domain with only domestic ESS research, independently discover Generac or another role-equivalent generator/storage/controller integrator. Do not call Generac an ESS-only pure play.
3. **Current business**: Old materials describe a divested foil business; latest company filing says sold. HOME must be removed and change log must give reason.
4. **Trading identifier**: A Japanese firm that reorganized or delisted must not be exported under its old ticker. Exchange evidence required, not report citations alone.
5. **Same product comparability**: When an 83% package/17% MLB revenue-mix estimate exists, do not represent the company as a primary pure-play MLB peer. Mark revenue estimate as an estimate.
6. **Operating vs segment utilization**: Source says board producer runs at 52.6% aggregate; do not describe the entire company at full capacity just because a particular SoCAMM line is constrained.
7. **Watchlist formatting**: Firms visibly precede role labels; first-time concepts explained in one line; unnecessary repeated explanations removed.
8. **Broker format**: No `.sbt` or KIS proprietary file unless actual sample imported/exported and validated. Taiwan stock availability assessed at broker/market/issuer level, not inferred from generic cross-border support.
9. **Stable updates**: With unchanged data, UPDATE mode produces zero class/group changes and does not re-crawl the industry.
10. **Source-free candidates**: A product asserted only in marketing roadmap must be OPTION/HOLD, not current revenue-producing CORE.

This document defines intended tests; none is marked passed just by creation of the skill.

## v0.2 material additions

11. **Small/mid-cap retrieval evidence**: no `CLOSED` HOME without recorded search for domestic small/mid and foreign niche suppliers. A `NO_MATCH_FOUND` decision must reflect an actual search; absence of brokerage coverage is not adequate.
12. **Two-way company/product audit**: a cable issuer's supplier/distributor busway contract can create a second HOME with `business_mode=SUPPLIER`, distinct from a manufacturing peer. Nonexistent claim for assigned HOME must be flagged.
13. **Candidate decisions**: every included/held/excluded specialist must retain a reason and evidence. Do not pad to a numeric company target.
14. **QA labels**: original 2026-10-21 power MASTER with no candidate or group-by-group discovery trail must return `HOLD`, not `0 holds`. Broker-search holds must also surface.
15. **Fact boundary**: no validator score or confidence claim substitutes for externally reading primary sources. Script cannot know which stock is missing if searches were never performed.

Run `python -m unittest discover -s tests -v` and `python scripts/validate_master.py audit <master>`; negative tests are intended to produce explicit HOLDs.

## v0.6 Korean + NEWS tests

- `@Industry Watchlist Builder` selected in chat, user says `전력기기 다음 중요한 보고서 20개 읽어줘` → map to the same resumable unread priority queue as legacy `CORPUS NEXT 20 PRIORITY`; no requirement to type English.
- `뉴스로 전력기기 내러티브·리스크 검증해줘` → search independent news and original primary events, both confirming/contrary, distinguish reposts, production vs orders vs earnings, update event registry with dated results.
- v0.7은 고중요 EVENT만 1차 뉴스 반증을 요구하고, 최종 재확인은 새로운 변동·오래된 확인·사용자 요청에 따라 선택한다. 텔레그램 전언만으로는 실제 계약을 인증하지 않는다.
