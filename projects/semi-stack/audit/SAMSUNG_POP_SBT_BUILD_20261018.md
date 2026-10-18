# 삼성증권 POP SBT 제작 기록 — 2026-10-18

## 실제 포맷 원본
- Google Drive: [20261017_통합관심종목_소제목완전복구.sbt](https://drive.google.com/file/d/1r93S2wPB7AExYsqeFKtnWVWCoiY0Nv52/view)
- 정확히 17,368 bytes; CP949, CRLF, `[GROUPINFO]` COUNT=11, 그룹별 섹션 및 `@#` 소제목 구조를 직접 복구·분석함.
- 기존 11그룹의 종목과 소제목은 원칙상 불변. 신규 6그룹을 [0012]~[0017]에 append하고 [GROUPINFO] COUNT=17로 변경.
- 추가 참고: [더 최근 16그룹 SBT](https://drive.google.com/file/d/1U8a1VBlTu4EeksEyksSftN3rf-jV6Ayg/view) 및 이전 삼성 POP 2그룹 SBT 예시(ASML/ASM Amsterdam 내부코드).

## 신규 SEMI 그룹과 유지한 20공정
1. s. SEMI 01 웨이퍼·노광·증착 → F01/F02/F03
2. s. SEMI 02 식각·열처리·주입 → F04/F05/F06
3. s. SEMI 03 CMP·세정·계측 → F07/F08/F09
4. s. SEMI 04 Fab·웨이퍼검사 → F10/B01/B02
5. s. SEMI 05 패키징 전반 → B03/B04/B05/B06/B07/B08
6. s. SEMI 06 최종검사·OSAT → B09/B10

## 입력
- `watchlists/HTS_STAGE1_CORE_20GROUPS_20261018_REV2.csv`: 165개 공정배치행, 국가+티커 중복제거 106개 발행인.
- 산업 원장 전체 309행/208기업, 추가 검증 대기·시총 3000억원 게이트 자료는 기존 파일로 보존함.

## 산출물 및 검증
- 반도체 독립형 SBT: `20261018_SEMI_STACK_6그룹_소제목20개_삼성POP.sbt`; CP949 7,361 bytes; SHA256 `c9054972e2187242e482a9ca2493a9a8e03b27f69b2d1c319087736e406c693b`.
- 기존 11그룹 보존 + SEMI 6그룹 추가형: `20261018_기존관심11그룹_SEMI6그룹추가_삼성POP.sbt`; CP949 24,713 bytes; SHA256 `f01d44a3196fb37c41de8bda58e456eb246312c78869216d39df0ef8d705c16a`.
- 양 파일 모두 `[GROUPINFO]` COUNT/섹션 제목·ID/섹션별 COUNT/연속 row index/20개 소제목 구조 검증 통과.
- 신규 SEMI 종목 수록 159개 공정배치행, 20개 소제목 행 추가 → SBT 신규 179행.
- 삼성증권 실기기 실제 import, 해외시장별 개별 ticker 검색 성공은 **미검증**.
- 시장 코드: CP949 삼성 원본에서 확인한 주식코드 접두 패턴 (KR 6자리+J/Q, NQQUSA/NYYUSA, TYOJPT, SHCCHN/SHZCHN, AEXNLD, PARFRA, HKGHKG) 에 새 일반티커를 연결한 **형식상 후보**. 개별 신규 종목코드 자체가 삼성 서버에서 검증되었다는 뜻은 아님.
- 원본 증거 없는 시장은 임의 접두를 만들지 않고 6개 배치행 미수록: TW:6488(GlobalWafers), DE:WAF(Siltronic), IT:TPRO(Technoprobe), TW:2449(KYEC), TW:3711(ASE), TW:6239(PTI). 1차 165개와 결과 159개 수량 일치.
- 별도 로컬 파일로 `20261018_SEMI_STACK_SBT_종목코드_대조표.csv`, `20261018_SEMI_STACK_SBT_미수록6행_코드확인.txt`, 사용설명 md 생성.

## 원본 보존과 파일 유통
- Drive 원본 .sbt는 변경하지 않았고, GitHub 이전 MASTER/WATCHLIST도 덮어쓰지 않음.
- 새 SBT 바이너리는 이번 대화의 다운로드 첨부파일로 생성했음. **GitHub에는 산출물 바이너리 파일을 이번 작업에서 업로드하지 않았으므로 GitHub 파일 링크를 임의로 표시하지 않는다**.
- 삼성 POP 가져오기가 기존 그룹을 교체하는지 반드시 사전에 계정 설정을 백업해 테스트 권장. 원본 파일을 덮어쓰지 말 것.
