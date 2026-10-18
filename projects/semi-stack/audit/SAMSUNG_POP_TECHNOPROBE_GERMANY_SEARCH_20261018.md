# Technoprobe 독일 POP 검색 대안 (2026-10-18)

## 삼성 POP에서 순서대로 입력
1. 독일 `A3DES7` — 독일 증권 식별번호(WKN).
2. 독일 `IT0005482333` — 국제증권식별번호(ISIN). **이탈리아 원주 ISIN이어도 독일 교차거래 동일 종목**.
3. 독일 `TECHNOPROBE` 또는 `TECHNOPROBE SPA`.
4. 독일 `K8B` — 독일 거래소 주식 기호.
5. `GERDEUK8B` — 사용자 SBT에서 확인한 `GERDEU` 접두 + K8B 결합. **형식 후보이며 삼성종목 DB 존재 검증 안 됨**.

## 경로
- 삼성 POP HTS **[3421] 해외주식주문**에서 시장구분: 독일 선택 → 종목명/종목코드 검색 → 검색 결과에서 이탈리아 원주 ISIN `IT0005482333` 매칭 확인.
- **[0517] 관심종목**에서 Insert로 검색·추가도 시도하되, 일반 관심종목 검색이 모든 해외시장 종목을 보여준다고 가정하지 않음.
- [3421 공식 도움말](https://www.samsungpop.com/contents/poptrading/help/3421.html): 시장구분/종목명·코드 선택.
- [0517 공식 도움말](https://samsungpop.com/contents/poptrading/help/0517.html): Insert 키로 종목검색·등록.

## 공식 상장 확인
- [Börse Stuttgart 종목정보](https://www.boerse-stuttgart.de/en/products/equities/stuttgart/a3des7-technoprobe-s-p-a/): `WKN A3DES7`, `ISIN IT0005482333`, `Symbol K8B`, 시장 `Freiverkehr`(장외/비규제 거래 세그먼트).
- [Deutsche Börse](https://live.deutsche-boerse.com/equity/technoprobe-s-p-a): 동일 식별.
- [Tradegate](https://www.tradegatebsx.com/orderbuch.php?isin=IT0005482333): K8B 거래 표시.
- **주의**: 회사는 독일 기업이 아닌 이탈리아 발행사로, 독일에서 교차거래됨. 삼성은 독일 온라인 거래 지원을 공지하지만 독일의 모든 시장/종목을 검색 지원한다고는 공지하지 않음.
- 삼성 독일 시장 온라인 가능: https://www.samsungpop.com/ux/kor/trading/overseasStock/overseasStockMarketGuide/westEurope.do
- 삼성 14개 온라인시장 및 전화주문: https://samsungpop.com/mbw/trading/foreignStock/tradingGuide.pop
- 삼성은 이탈리아를 **일부 전화주문 가능 외국 시장**으로 별도 안내하므로 '이탈리아 전체 지원 안 함'과 'POP 온라인 검색 목록에 이탈리아가 없음'은 구분할 필요 있음: https://www.samsungpop.com/ux/kor/customer/guide/workproductguide/overseasStockTab2.do

## 실패 진단
- 3421 독일시장에서도 WKN·ISIN·회사명·K8B 모두 안 뜬다면, 회사가 독일 거래소 Freiverkehr에만 유통되는 한편 **삼성 온라인 지원 종목 DB에 등재되지 않았을 가능성**이 높다. 사용자 앱 단에서는 공식적으로 확인할 방법 없음.
- 삼성 해외주식 데스크 `1599-5899`에 **IT0005482333 (WKN A3DES7), Frankfurt/Stuttgart/Tradegate K8B**를 지원하는지 및 POP 관심종목 검색 등록 가능 여부를 구체적으로 문의.
- SBT 자체에는 승인되지 않은 `GERDEUK8B`를 임의로 끼워 넣지 않음. 공식 POP에서 종목 조회가 되거나 내보내기로 실제 내부코드를 회수했을 때 반영.
- 사용자가 미국 OTC THNBY 검색 실패를 확인했으므로 미국 대안 재시도 권유하지 않음.

## 결론
주식 식별 자체는 공식 확인됨. 삼성 POP 검색·지원 여부와 Xetra 대비 Freiverkehr 세그먼트 차이는 미확인. 이 둘을 분리 기록.
