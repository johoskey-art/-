# SEMI STACK | 2026-10-16

기존 20개 반도체 소부장 공정(F01~F10/B01~B10)을 유지하며, 기업별 공정 배치와 검증 근거를 관리하는 프로젝트.

## 현재 GitHub 백업
- `watchlists/SEMI_STACK_WATCHLIST_20261016.txt`: 20개 공정별 관심종목 후보, 총 279개 배치행
- `watchlists/SEMI_STACK_WATCHLIST_20261016.csv`: 동일 명단의 기계 판독용 정규화 CSV
- `audit/C_VALIDATION_20261017.md`: C등급 우선 검산 진행과 근거

## 반드시 구분할 사항
- 279개는 공정 배치 **행**이며, 중복 제거 시 약 208개 상장기업 후보임.
- C등급은 80개 공정 배치행(74개 기업)이었으며 **미검증 또는 과거 근거만 존재**한다는 뜻. 투자 등급이 아님.
- 최종 XLSX 원본 `SEMI_STACK_MASTER_20261016.xlsx`는 이 GitHub 백업과 **별개의 보관물**이다. 바이너리 파일 업로드 여부는 별도로 확인해야 한다.
- 본 목록의 주식 코드는 일반 상장 티커이며 삼성증권 POP/mPOP 전용 등록 코드를 검증한 파일이 아니다.
- 별도 사업(일반 PCB·기판, 팹리스·IDM), 비상장법인 및 중복 경제적 노출은 MASTER에서 분리해서 관리한다.

## 운영 규칙
새 공정/PLAY를 만들지 않고 기존 기업의 공시·IR·공식 제품 자료를 기준으로 실제 오류만 교정한다. 변경 시 출처 URL과 검산 날짜, 수정 전후 배치를 남긴다.

## 2026-10-17 추가 백업
- [`data/SEMI_STACK_MASTER_20261016.csv`](data/SEMI_STACK_MASTER_20261016.csv): 367개 기업/법인 항목, 검증 등급과 근거 URL, 기존 원장 출처 포함
- [`audit/CORRECTIONS_20261016.csv`](audit/CORRECTIONS_20261016.csv): 기존 교정·검토 기록 44건
- `.xlsx` 파일 자체는 아직 GitHub에 저장되지 않았다. GitHub CSV는 엑셀의 기업 MASTER 시트를 재구성한 텍스트 백업이다.
- C등급 추가 조사 결과(Piotech, Aehr, Teradyne, Chroma)는 `audit/C_VALIDATION_20261017.md`에 기록했으며, **2026-10-16 CSV와 별도 델타**로 관리한다.


## 2026-10-18 검토용 증분 — 원본과 구분
- [SESSION_20261018.md](audit/SESSION_20261018.md): 이번 세션 GitHub 복구·공식 출처·결정·후속 대기 로그
- [C_VALIDATION_DELTA_20261018.csv](audit/C_VALIDATION_DELTA_20261018.csv): C등급 기업 15개 사례 기록, 검증상태 및 출처
- [SEMI_STACK_MASTER_20261018_REVIEW.csv](data/SEMI_STACK_MASTER_20261018_REVIEW.csv): 367행 기존 MASTER CSV 기반 복원·교정 초안. 기존 20261016 원본 불변.
- [SEMI_STACK_WATCHLIST_20261018_REVIEW.csv](watchlists/SEMI_STACK_WATCHLIST_20261018_REVIEW.csv): 기존 279행에 공식 제품 근거 신규 공정 9행을 합친 **288행 검토본**, 고유기업 208개.
- [SEMI_STACK_POP_MANUAL_20GROUPS_20261018.txt](watchlists/SEMI_STACK_POP_MANUAL_20GROUPS_20261018.txt): POP HTS 20개 그룹별 **수동 검색·등록 보조용** 명단. 삼성 공식 import 파일 아님.
- 이번 공식 제품 대조 12개사, 나머지 C기업 전수 검증 및 HTS 실제 종목 검색 테스트 미완료. 최신 원장을 FINAL로 잘못 표기하지 않을 것.


## 2026-10-18 C등급 74사 전수검산 결과 — 최신 읽을 파일
- [전수검산 감사보고서](audit/FULL_AUDIT_20261018.md): 74사 중 이전 검증 12사 + 잔여 62사 공식자료 전수 대조, 신규배치 30행과 공정 적합성 보류 사유.
- [잔여 62사 최종 검증표](audit/C_VALIDATION_REMAINING_62_20261018_FINAL_REVIEW.csv): **기업당 1행**, 확인 제품/상장·자료 수준/출처 URL/유지·추가·보류 판정.
- [최신 MASTER 교정 검토본](data/SEMI_STACK_MASTER_20261018_FINAL_REVIEW.csv): 367개 기업·법인 항목 중 STACK 208개/별도관리 159개. 최초 44개 교정 이력 보존.
- [최신 WATCHLIST 교정 검토본](watchlists/SEMI_STACK_WATCHLIST_20261018_FINAL_REVIEW.csv): 기존 279배치 + 10/18 공식 근거 신규 30배치 = **309배치**, 고유기업 208개, 공정 정확히 20개.
- [삼성 POP 수동검색용 20그룹](watchlists/SEMI_STACK_POP_MANUAL_20GROUPS_20261018_RECONCILED.txt): **309개 배치**, 삼성증권 내부종목코드/CSV import 규격 미확인. 파일 자체는 HTS 공식 업로드 형식 아님.
- **전수조사 완료 ≠ 최종 전부 PASS**. 잔여 62사 가운데 직접 제품/발행인사업 49사, 부분 공식자료 12사, 공정 매칭 보류 1사. Veeco/Axcelis 합병, 코세스 B05, 에프엔에스테크 F08 및 Samsung POP의 해외거래소 검색·등록 가능성은 별도 검증 중.
- 2026-10-16 원본 MASTER/44교정기록/279행 WATCHLIST와 2026-10-18 과정 파일들은 모두 히스토리로 유지하며 덮어쓰지 않음.

## 2026-10-18 삼성 POP HTS 압축명단 최신 REV2
- [20공정 핵심 TXT](watchlists/HTS_STAGE1_CORE_20GROUPS_20261018_REV2.txt): 106 고유 상장기업 / 165 공정배치행. 삼성 공식 파일 가져오기 규격이 아닌 수동 검색용.
- [1차 핵심 CSV](watchlists/HTS_STAGE1_CORE_20GROUPS_20261018_REV2.csv)
- [2차 시총/전문/보류](watchlists/HTS_STAGE2_VERIFY_20261018_REV2.csv): 144 배치행.
- [한국 99사 시총 검산표](watchlists/KR_3000EOK_MARKETCAP_GATE_20261018_REV2.csv): 7개 시총 확인, 잔여 미검증.
- [검산 출처](audit/HTS_MARKETCAP_CHECK_20261018.md), [선별정책](audit/HTS_SELECTION_POLICY_20261018.md).
- 연구용 전체 208사/309배치 원장 보존. 국내 3000억원 이상 후보 누락 여부 검사는 미완료.


## 2026-10-19 현재 운영 기준 — 국내 시총 2000억원 (최신)
- **국내 HTS 선정 시총 기준이 3000억 → 2000억원으로 변경됨.** 과거 REV2/3000억 목록은 이력용, 현재 운영본은 REV3.
- [SEMI HTS 핵심 1차 REV3](watchlists/HTS_STAGE1_CORE_20GROUPS_20261019_REV3_2000EOK.csv): 111개 기업(국내 65/해외 46), 공정배치 172건.
- [국내 99개 시총 판정 REV3](watchlists/KR_2000EOK_MARKETCAP_GATE_20261019_REV3.csv): 기존 검산 자료에서 7개만 확인, 92개 검증 대기.
- [SEMI HTS 2차 검증 REV3](watchlists/HTS_STAGE2_VERIFY_20261019_REV3_2000EOK.csv): 137개 공정 배치.
- [309배치 하위 STACK 88기능 V3](data/SEMI_SUBSTACK_309ROWS_20261019_REVIEW_V3_HTS2000EOK.csv) 및 [HTS 6그룹 하위 기능 프리뷰](watchlists/SEMI_SUBSTACK_6GROUP_PREVIEW_20261019_V3_2000EOK.txt).
- [2천억 변경 근거·검산 로그](audit/HTS_SELECTION_POLICY_2000EOK_20261019.md). 기존 208기업/309배치 연구용 원장은 변동 없음.
- **HTS 시총 게이트와 STACK 매출비중 Primary/Secondary 게이트는 독립**이며, 공정 검산 및 삼성 POP SBT 업데이트는 미완료.
