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


## 2026-10-19 후속검산 REV5/하위STACK V4 — 현재 최신 파일
- 국내 시총 기준: **2,000억원** (기존 3,000억원 판본은 히스토리 보존).
- [HTS 국내외 1차 핵심 REV5](watchlists/HTS_STAGE1_CORE_20GROUPS_20261019_REV5_2000EOK.csv): 국내 82 + 해외 46 = **128기업, 193 공정배치**.
- [HTS 2차 검토 REV4](watchlists/HTS_STAGE2_VERIFY_20261019_REV4_2000EOK.csv): **116 공정배치**, 전체 309 보존.
- [국내 시총 99사 전수표 REV4](watchlists/KR_2000EOK_MARKETCAP_GATE_20261019_REV4.csv): 시총확인 41사(충족24/미달17), 미확인 58사(현재 핵심 선편입분).
- [20공정/87개 제품기능/309배치 최신 하위STACK V4](data/SEMI_SUBSTACK_309ROWS_20261019_REVIEW_V4_2000EOK.csv).
- [하위기능 재현 규칙 V3](data/SEMI_SUBSTACK_RULEBOOK_20261019_V3_OFFICIAL.tsv).
- [6관심그룹 하위소제목 V4 미리보기](watchlists/SEMI_SUBSTACK_6GROUP_PREVIEW_20261019_V4_2000EOK.txt).
- [31건 공정/매출 게이트 보류](audit/SEMI_SUBSTACK_REVIEW_QUEUE_20261019_V4.csv).
- [이번 후속검산 및 공식 제품 출처/재분류 로그](audit/SEMI_STACK_CAP_AND_SUBSTACK_AUDIT_20261019_V4.md).
- **주의:** 모든 309배치 품목 매출비중 및 Secondary X%는 아직 검증/확정되지 않았으므로 위 193배치는 HTS 우선후보지 최종 승인 등록 대상이 아님. 삼성 POP `.sbt` 새 파일은 아직 제작/검증되지 않음.


## 2026-10-19 추가 검산 — POP SBT 제작 및 심사 고정
- 실제 데이터 구조 검산을 거친 삼성 POP CP949·CRLF SBT(기존 11그룹 보존 통합17 / SEMI 독립6)가 **현재 대화 다운로드 파일**로 제공됨. 바이너리 `.sbt`는 이 GitHub 저장소에 아직 업로드되지 않았으므로 **이 문서 링크를 SBT 다운로드 링크로 오해하지 말 것**.
- 기준 stage1은 128기업, 193 기업-공정배치; Technoprobe(이탈리아 POP 지원 미확인) 1건과 ISC F08·F10, 한미 B04·B08, 원익IPS F05 5건의 매출/제품 게이트 보류를 제외하고 **187개 배치를 SBT 검토용으로 수록**. 개별 POP 종목코드 실제 인식은 테스트 미완료.
- [31건 공정 심사 결과](audit/SEMI_SUBSTACK_31CASE_DECISIONS_20261019.csv): KEEP/REMAP/DROP/HOLD 개별 근거 및 URL 완료. 이 판정은 제품 존재 확인과 수익비중 승격을 명확히 분리.
- [2천억 미만 국내 17사 예외 심사](audit/KR_UNDER_2000EOK_EXCEPTIONS_17_DECISIONS_20261019.csv): 잠정 제외1·조건부 전문기업15·공정 증빙 보류1. 15사는 유동성 floor 미확인으로 별도 보조 후보, 정식 SBT 편입 미실시.
- [2천억 시총 검산 REV5](watchlists/KR_2000EOK_MARKETCAP_GATE_20261019_REV5_PARTIAL_VERIFIED.csv): 99기업 중 확인47(충족30·미달17), **미확인 52**. 마지막 52는 이미 HTS stage1에 있는 기업이라 이 미확인이 POP 관심그룹 파일 작성을 지연시키는 사유가 되어서는 안 됨. 하지만 공식 시총 전수검증 완료 주장 금지.
- 기능 교정: 케이씨텍 F08 300mm 웨이퍼 Wet Clean, NAURA F08 12인치 세정·F06 이온주입·B05 하이브리드 본딩, Nikon F09 인라인 검사, TES F04 Gas Phase Etch & Clean, 코미코 F10 장비부품 정밀세정.
- 309개 전 공정 배치의 공시직접 세부 매출비중 및 Secondary X% 게이트는 별도 미확인·미합의. 특정 제품 존재를 곧바로 Secondary 승격으로 자동 판정하지 말 것.


- [309행 31건 심사 병합본 V5](data/SEMI_SUBSTACK_309ROWS_20261019_V5_31_DECISIONS_MERGED.csv): 기존 309 기업-공정 연구배치를 유지하면서 31건 모든 개별판정을 원장에 직접 반영. 해당 공정 제외도 연구원장 삭제 대신 `DROP_THIS_PROCESS`로 기록함.
- 기존 주력 Primary와 부매출 중요도 미확인 Secondary를 분리. 현재 최종 이용 파일은 **대화 다운로드 `검산반영187건.sbt`**(6그룹 독립 및 기존11그룹 통합17), GitHub는 원장/감사기록 저장소 역할.


## 2026-10-19 국내 미검증 시총 52개 재검산 — 최우선 최신 기준
- [국내 99개 2천억 시총 검산 REV7](watchlists/KR_2000EOK_MARKETCAP_GATE_20261019_REV7_99SCREENED_1CONFLICT.csv): **78개 충족 / 20개 미달 / 1개 경계 출처 충돌**. 기존 미검증 52 중 51개 문턱 판정, 와이씨켐 112290만 보류.
- [HTS 1차 193배치의 시총 예외 표시 REV6](watchlists/HTS_STAGE1_CORE_20GROUPS_20261019_REV6_CAP_FLAGS.csv): 기존 128개/193배치 유지, 시총 미달 3개 기업 4배치 및 와이씨켐 1개 기업 2배치를 승격 보류로 표시. 시총 무쟁점은 124기업/187배치(구SBT 187배치와 다른 구성).
- [52개 추가 시총 검산 로그](audit/KR_99CAP_52MISSING_RECHECK_20261019_REV7.md): 직접/반올림 표기, 경계출처 충돌, 2천억 미달 전문기업 명단 기록.
- **이전 REV5 및 REV6의 시총 미검증 52개 또는 99개 모두 통과 표현은 낡은 내용이다.** 삼성 POP SBT 최종 확정이라고 표시하지 않는다.


## 2026-10-19 4단계 산출물 — 현재 최신 운영 검토본
- [4단계 통합 결과 및 미검증 경계](audit/SEMI_STACK_4STEPS_DELIVERY_20261019.md) — ①국내 99사: 시총통과78·공정전문성 예외19·비편입2, ②31건 검토이력, ③309건 정성 역할판정, ④POP SBT 제작·구조 QA.
- [국내 99사 HTS 판정](audit/KR_99_HTS_FINAL_POLICY_DECISIONS_20261019.csv) / [309건 주·부 STACK 판정·confidence](data/SEMI_STACK_309_ROLE_AUDIT_20261019.csv).
- [주력 후보 142사 고유종목표](watchlists/SEMI_HTS_ONE_FIRM_ONE_PRIMARY_CANDIDATE_20261019_142.csv): 한국97·해외45(이탈리아 Technoprobe 제외); 삼성 POP 6그룹/기존 11그룹 통합 SBT는 **현재 대화에 다운로드 파일로 제공**.
- **SBT는 구조 QA PASS이나 삼성 POP 실기기 import와 해외 내부코드 일부 미검증**. 309개 품목의 매출비중 실측 및 Secondary X%는 **미완료**이므로 142사는 '후보 주력'이지 주/부 영구 확정 아님. 기존 20261019 REV5/REV6 숫자와 혼용하지 않을 것.


## 2026-10-19 공식 매출검산 배치 01 / SBT 141기업 교정
- **기존 142기업 검토용 SBT에서 확인된 오류:** 한화비전(489790)은 연결 시큐리티 매출이 최대, B05 TC본더는 한화세미텍 산하 사업이므로 연결기업 Primary 주장을 철회. 유니테스트(086390)는 B09 테스트 핸들러가 아니라 B09 메모리 테스터·번인.
- [5개 회사 10개 제품·공정 배치 2026/2025 실적 근거](audit/SEMI_REVENUE_EVIDENCE_BATCH01_20261019.csv): 유니테스트 2026H1 메모리 테스트장비군 89.56%, 오킨스전자 2026Q1 소켓 제조 외 91.9%·테스트 용역 6.7%, ISC 2026H1 Test Socket 등 제조 제품 83.7%, 한화비전 2026Q2 세미텍 사업부 전체 27.24%(TCB 단독 아님), 에프엔에스테크 2025 소재부품 묶음 47.22%(CMP 단독 아님). 직접 묶음수치와 개별 제품 비중 구분.
- [309행 원장 Batch01 증거 덧붙인 V2](data/SEMI_STACK_309_ROLE_AUDIT_20261019_V2_EVIDENCE.csv) / [142개 원형에 기업별 검증 메모 보강한 V2](watchlists/SEMI_HTS_142_PRIMARY_REVIEW_20261019_V2_EVIDENCE.csv).
- [171?가 아닌 **17개 회사에서 18개 공정쌍** 잠재 동일제품 중복](audit/SEMI_SUBSTACK_PRODUCT_ALIAS_18_PAIRS_20261019.csv): F04 식각 부품 vs F10 공통부품, F03 전구체 공급 vs F10 인프라, 마스크 검사 F02/F09 등의 동일 제품설명 중복. 서로 다른 SKU가 존재할 수 있으므로 **중복 가능성 경고일 뿐 회사/공정 자동 삭제 아님**.
- [**141기업 수정된 Primary 후보 시트**](watchlists/SEMI_HTS_PRIMARY_CANDIDATES_20261019_V3_141_NONPRIMARY_FILTER.csv): 국내 96·해외 45. 한화비전은 기업 원장 보존 및 Secondary/PLAY 검토 큐로 이동. 에프엔에스테크 F07은 CMP단독 비중 미공시이므로 주력 확정 아님.
- **새 삼성 POP SBT 통합17그룹/반도체 독립6그룹의 141기업 버전**은 이번 대화에 각각 다운로드 제공. 원래 11그룹 내용 바이트 보존, CP949/CRLF/COUNT/20공정·141종목 기계검산 PASS. 실제 POP import·해외 종목코드 및 309개 개별 매출 X%는 여전히 미검증.
- 과거 142기업 SBT는 유니테스트 소제목 오류 및 한화비전 주력 오분류로 **현재 기준 구판**이며 사용 전 141기업 교정본과 비교해야 함.


## 2026-10-19 추가 공식매출·중복 검산 — 최신 141기업 V2
- [동일제품 중복 의심 18쌍 전수 판정](audit/SEMI_SUBSTACK_PRODUCT_ALIAS_18_PAIRS_20261019_V2_VERDICTS.csv): 17사/18쌍, 공식 독립 제품(PSK SUPRA vs INTEGER)와 포괄 적용 태그를 분리. 유효한 별도 SKU/매출 미검증 종목은 `REVIEW` 유지.
- [공식 제품·매출 검산 Batch02 13행](audit/SEMI_REVENUE_EVIDENCE_BATCH02_20261019.csv): 메카로 히터블록 2026Q1 97.10%, 비씨엔씨 QD9·QD9+ 63.5%, 케이엔제이 2025 SiC 등 부품 98.25%, 월덱스 2026Q1 Si 69.4%, 원익QnC 세정·코팅 국내외 합산 12.0% 등. **제품군 매출비중을 특정 공정 매출비중으로 허위 전환하지 않음.**
- [309 연구행 기존 원장 보존 + 중복·정량근거 주석 V3](data/SEMI_STACK_309_ROLE_AUDIT_20261019_V3_ALIAS_REVIEW.csv): 208기업/309연구배치 원형 보존. 운영 공정은 별도 교정열을 사용.
- [HTS 주력후보 141개 공식매출 교정 V4](watchlists/SEMI_HTS_PRIMARY_CANDIDATES_20261019_V4_141_PRODUCT_CORRECTED.csv): 메카로 **F03 히터블록**, 비씨엔씨 **F04 식각 QD9**, 뉴파워프라즈마 **F10 RF 전원/RPG**로 정정, 한화비전 Primary 제외 유지.
- 해당 GitHub V4와 동일하게 수정된 삼성 POP `.sbt` **통합17그룹/SEMI6그룹 각각 141기업**은 대화 내 최신 ZIP `SEMI_STACK_POP_20261019_공식매출검산_141기업_V2.zip`에서 제공. 원본 11그룹 17,585바이트 prefix 동일, CP949/CRLF/그룹 COUNT/소제목 번호/20공정/141고유기업 자동 QA PASS. **바이너리 SBT는 아직 GitHub 미업로드, 실기기 POP import·해외 종목코드 미확인.**
- 구 142기업 SBT, 초기 141기업 SBT는 최신 하위기능과 불일치하므로 사용 권장하지 않음. Secondary X% 미확정 및 전사 최대 매출 공시 미분리 기업은 주력 **후보** 상태를 유지.
