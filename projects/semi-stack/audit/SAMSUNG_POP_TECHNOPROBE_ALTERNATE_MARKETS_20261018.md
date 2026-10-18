# Technoprobe 대체 거래시장 확인 — 2026-10-18

## 결론
삼성 POP HTS 반도체 6그룹 B02에서 미등록 상태인 이탈리아 `TPRO`에 대한 **해외 동일 발행인·대체시장 확인**.

| 시장 | 종목코드 | 유형 | ISIN | 상태/근거 | 삼성 POP 확인 |
|---|---|---|---|---|---|
| 이탈리아 Euronext Milan | TPRO | 원주·기준 거래시장 | IT0005482333 | [Borsa Italiana](https://www.borsaitaliana.it/borsa/azioni/scheda/IT0005482333-MTAA.html) | 이탈리아 온라인거래 미지원 |
| **독일 Frankfurt/Tradegate** | **K8B** | 동일 원주 교차 거래 | **IT0005482333** | [Deutsche Börse](https://live.deutsche-boerse.com/equity/technoprobe-s-p-a), [Tradegate](https://www.tradegatebsx.com/orderbuch.php?isin=IT0005482333) | **삼성 개별종목 지원·실기기 SBT 등록 미확인** |
| **미국 OTC** | **THNBY** | Citibank **unsponsored ADR**, 원주 2주 : ADR 1주 | **US8789671083** | [Citi 예탁증서 공식 프로필](https://citiadr.factsetdigitalsolutions.com/stocks/profile.idms?cusip=878967108), [Citi Book Status OPEN](https://depositaryreceipts.citi.com/adr/guides/pgm_dispabook.aspx?cusip=878967108&pageId=15&subpageID=111) | 개별종목 검색·등록 미확인; OTC 거래 전화주문 |

## 삼성증권 거래 지원
- [삼성증권 해외주식 거래 안내](https://www.samsungpop.com/mbw/trading/foreignStock/tradingGuide.pop): 독일 온라인 주문 가능 시장 명시, 이탈리아는 온라인 지원 목록에 없음. **미국 OTC 주문은 해외주식 데스크 전화주문만 가능**하다고 안내.
- 신규 SBT 후보 식별자: `GERDEUK8B`은 사용자가 제공한 `대만ㅇㄹㅇㄹ.sbt`의 독일 접두부 `GERDEU` + 독일거래소 종목기호 `K8B`를 합친 **후보**이지 삼성 서버 조회가 성공한 확인코드는 아님.
- `THNBY`의 삼성 내부 코드도 검증되지 않았으며 `NQQUSATHNBY` 등 임의 접두 사용 금지 (미국 OTC는 나스닥 코드와 다를 수 있음).
- 독일 시세는 이탈리아 기준시장보다 거래량이 적을 수 있어 최종 모니터링 정확도를 비교할 것. ADR은 **2배 원주비율+USD/EUR 환율** 차이를 고려해야 함.
- 동일 기업이므로 원장 `IT:TPRO`을 중복기업으로 추가하거나 새 공정에 이중 배치하지 않음. B02에서 기존 본사 발행인 하나에 독일 대체시장/미국 ADR을 **Alias**로 저장할 것.

## 추후 실제 검증 체크
1. 삼성 POP 종목검색에서 국가 독일을 선택, `K8B` 또는 `IT0005482333` 검색.
2. 확인된다면 POP 관심종목 추가한 후 실제 SBT로 내보내기하여 **진짜 내부코드**를 추출.
3. 수동 등록·SBT에서 `GERDEUK8B`가 검증되기 전까지 기존 SBT의 TPRO 미수록은 유지.
4. 독일 개별 종목 지원이 안 되면 미국 OTC `THNBY` 관심종목 검색, 별도 거래는 해외주식 데스크 문의.
