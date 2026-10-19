# SEMI STACK Primary 추정 191건 — 실제 매출 검산 실행 요약
기준일: 2026-10-19. 저장소: johoskey-art/- / projects/semi-stack/

## GitHub 직접 저장·재조회에 성공한 자료
- `audit/SEMI_PRIMARY_191_REVENUE_AUDIT_20261019_BATCH02_V5.csv`: 191건 전수 식별·감사표. 그중 54건에 공식 공시·IR 또는 기존 검산 자료 근거, 기간, 범위, confidence, 판정 기입. 나머지 137건은 명확히 "이번 차수 미검증"으로 보존.
- `data/SEMI_STACK_309_ROLE_AUDIT_20261019_V8_PRIMARY_REVENUE_CHECK.csv`: 위 54건 교정이 반영된 전체 309행 원장. 기존 208기업·20공정 유지.
- `watchlists/SEMI_HTS_PRIMARY_CANDIDATES_20261019_V10_REVENUE_REVIEW.csv`: 후보 141기업(국내 96·해외 45) 그대로 보존하면서 근거를 연동. 기존 SBT 파일 자체는 변경 안 함.
- `audit/SEMI_TECHWING_PRIMARY_MIX_CHECK_20261019.md`: 이후 공식 KIND 공시 추가 검증 1건. **원장 V8과 191건 V5에 아직 미병합**, 별도 감사 이력으로 보존.

## 판정현황 — 감사표 V5 안에 반영된 54건
- Primary 정량확인 14 / 정성확인 3 / 사업부 최대매출 확인-하위공정 보류 12 / Primary 매출근거·매핑 보류 11 / 전사 Primary 취소 14 / **아직 공식검산 진행하지 않은 137건**. 합계 191.
- **독립 보강 1건:** 테크윙은 2025FY COK 매출이 Test Handler 등 장비보다 크고, 2026Q1에는 장비매출이 COK보다 큼. B09.TEST_HANDLER 단독의 최대매출은 입증되지 않았으므로 별도 메모에서 `Primary 매출 검증보류`로 판정. 단독 보강을 합산한 **실제 조사 진행은 55건, 미조사 136건**. 연결 CSV의 정식 상태는 여전히 54/137이며 병합 실패 사실 공개.
- 숫자는 제품/보고부문 매출의 **공식 공시 구분과 기간을 따른 값**이다. 부문 전체 매출을 하위 SKU 공정 매출로 쓰지 않았으며 X% 게이트는 미합의로 유지.

## 전사 Primary 취소 14건(재검증 포함)
Coherent SiC F01, Wolfspeed SiC F01, Nikon 노광 F02, Canon 노광 F02, Fujifilm 포토소재 F02, DNP 포토마스크 F02, HOYA 마스크 F02, Merck KGaA 반도체 화학 F02, Resonac CMP F07, Entegris CMP F07, LINTEC 다이싱필름 B03, Kulicke & Soffa HBM TCB B05, Air Liquide 반도체가스 F10, 한화비전 반도체장비 B05(이전 배치 판정 재반영). **기업 자체를 반도체 공급망에서 제거한 뜻이 아님.** 관련 제품 존재와 연결 최대 매출은 독립된 판단이다.
- 회사 연결 Primary가 아닌 제품은 정식 주력에서 승격검토·PLAY 후보로 이동; Secondary 매출 임계값 X%는 정하지 않고 보류.
- 기존 141기업 HTS 후보표에서 **HOYA·Entegris**는 전사 Primary 아님으로 재편입 검토 플래그. 나머지 취소 회사 대부분 기존 HTS 141후보 밖. SBT 실물 변경 없음.
- K&S 2025 Ball Bonding Equipment 매출 44.8% vs Advanced Solutions 11.1%: HBM TCB는 후자 일부. Resonac Front-end Semiconductor Materials 83.6십억 엔(그 안에 CMP) < Back-end Materials 245십억 엔.
- AIXTRON: 2025 증착장비 매출 444.6백만 유로/전사 556.6백만 유로=79.9%, Primary 제품군 정량 확인. GaN/SiC 관련 57%는 **장비매출의 비중**이며 전사 비중이 아님.

## 이번 배치 대표적인 신규 Primary 정량 검증
- Photronics: IC photomasks $615.1m vs display $234.2m (FY2025)
- Axcelis: 이온주입 장비·서비스 $824.098m / $839.048m (FY2025)
- ASE: 2025 packaging NT$308,343m > EMS NT$257,193m > testing NT$71,900m
- Eugene Technology: FY2025 LPCVD/Plasma ALD 증착 장비 제품군 81.0%
- Leeno Industrial: FY2025 테스트 소켓 제품군 65.48%
- HPSP: FY2025 고압 어닐링 장비 제품군 89.1%
- ASML, KLA, Advantest, Teradyne, FormFactor 등은 감사표에 원문 링크·기간 포함.

## 현재 중요한 미해결 사항 (보류 ≠ 조사)
1. **136건은 이번 차수 공시 매출 대조 자체를 완료하지 못함.** "근거가 없다"고 단정하지 말고 미조사로 표기. 감사표 V5는 137건 미검증(테크윙 1건이 별도 메모로 조사됨).
2. **11건은 자료를 봤으나 SKU 매출분리/사업별 출처·시점 등으로 확정 불가.** 기존 세그먼트 매출과 개별 공정 SKU의 구분 계속 필요.
3. SBT 141기업·SEMI6·기존11그룹 파일은 이번 회차 편집하지 않았음. POP 실기기 가져오기 미검증.
4. `SEMI_PRIMARY_191_REVENUE_AUDIT_20261019_BATCH02_V6.csv` 와 이에 대응하는 원장·후보표 추가 쓰기 요청은 플랫폼 안전검사에서 차단되어 **커밋되지 않았음**. 테크윙 보정 단독 메모는 별도 커밋 완료.
5. 다음 완료 조건: 아직 미조사 136건 공시 매출 원문 교차검산 + 11건 매출 분리 가능성 검토 + 별도 Techwing 1건 메인 원장 동기화 + 최종 141기업 HTS 실파일 교정.
