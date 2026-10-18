# 삼성증권 SBT 대만/독일 예시 대조 및 SEMI 관심종목 재생성 (2026-10-18)

## 근거 파일
- 사용자 신규 SBT 원본 `대만ㅇㄹㅇㄹ.sbt`: 1개 그룹, 29개 레코드, 1,330 bytes, CP949/CRLF.
- 원본에서 관찰한 실제 코드 예: `TAITWN2330` (TSMC), `TAITWN6515` (WinWay), `TAITWN3501`, `TAITWN9941A`, `GERDEUNOT`, `GERDEU0ZC`.
- 기존 POP SBT 예시: [20261017_통합관심종목_소제목완전복구.sbt](https://drive.google.com/file/d/1r93S2wPB7AExYsqeFKtnWVWCoiY0Nv52/view) 11그룹.
- 종목 모집단: `watchlists/HTS_STAGE1_CORE_20GROUPS_20261018_REV2.csv` = 20개 공정 165개 배치행 / 106개 고유 기업.
- 2026-10-18 기존 생성물 6그룹 독립형과 기존11+SEMI6 병합본을 **CP949 그대로 유지해 패치**. 과거 11개 그룹의 레코드를 보존.

## 추가된 종목 5개
| 공정 | 국가 | 일반티커 | 새 SBT 코드 후보 | 근거 |
|---|---|---|---|---|
| F01 | TW | 6488 | `TAITWN6488` | 실제 사용자 SBT의 TAITWN 접두 |
| F01 | DE | WAF | `GERDEUWAF` | 실제 사용자 SBT의 GERDEU 접두, [Siltronic IR에서 WAF 확인](https://www.siltronic.com/en/investors/information-on-the-share.html) |
| B10 | TW | 2449 | `TAITWN2449` | 실제 사용자 SBT의 TAITWN 접두 |
| B10 | TW | 3711 | `TAITWN3711` | 실제 사용자 SBT의 TAITWN 접두 |
| B10 | TW | 6239 | `TAITWN6239` | 실제 사용자 SBT의 TAITWN 접두 |

**구별**: 사용자가 제공한 실제 SBT에서 *시장 접두부의 존재*는 확인됐지만 위 **각 신규 결합코드가 삼성 서버에서 인식되는지까지는 검증되지 않았다**. POP 실기기 가져오기 성공을 주장하지 않는다.

## 미수록 보류
- `B02 IT:TPRO` Technoprobe: 제공된 모든 SBT에서 이탈리아 종목 식별코드의 실제 사례가 발견되지 않음. 삼성증권 [해외주식 온라인거래 시장 목록](https://www.samsungpop.com/mbw/trading/foreignStock/tradingGuide.pop)에도 이탈리아는 직접 열거되지 않아 임의 `MILITA` 등 생성하지 않음.
- 투자·상장 제외가 아니라 POP 내부코드·온라인 관심등록 지원 확인 대기.

## 제작과 검증
- 반도체 단독형: `20261018_SEMI_STACK_6그룹_대만독일5종목보완.sbt` 6개 그룹, **20개의 F01~B10 소제목**, **164개의 종목배치**, SBT 종목+소제목 총 184행, 7,612 bytes.
- 기존11 + SEMI6 통합형: `20261018_기존11그룹_SEMI6그룹_대만독일보완.sbt`, 총17그룹, 기존 11그룹 401행 변경 없음, SEMI 184행 포함, 전체 585행, 24,964 bytes.
- 파일 인코딩 CP949, 개행 CRLF; GROUPINFO COUNT, 각 그룹 COUNT/행 번호, 소제목 `@#` one-based 인덱스 전부 재검산.
- **20공정 × SBT 실제코드 다중집합과 165행 종목코드 매핑표 대조**: 포함 164행이 모두 해당 공정에 정확히 일치하고, 누락은 IT:TPRO 1행뿐.
- 원래 2026-10-17 관심 11그룹의 그룹명·순서·원본 각 행이 완전히 동일함을 구조·내용 검증.
- 바이너리 SHA256 단독형 `dc8e5483e4d04fd9298bc4589784a25821f5f1592464ab5ef5dad19e1462e899`, 통합형 `a30ae3685b0082763dca585e7616e349cb94f44c0b6f2aa67867c9ffcef4b4b5`.
- 두 SBT는 이 대화의 **파일 첨부로 전달**. 이번 GitHub 기록은 제조 근거/검사이력을 보존하며, **SBT 바이너리 자체는 이번에 GitHub 업로드하지 않았음**.
- 향후 HTS 실제 적용 전 현재 사용 중인 그룹을 별도 백업. 이 통합본은 10월 17일 11그룹을 기준으로 하므로 그 이후 추가된 관심그룹은 보존하지 못할 수 있음.

## 다음 실제 테스트
1. 기존 관심종목 백업 → 17그룹 통합형 시험 가져오기.
2. 그룹12(F01): GlobalWafers, Siltronic 인식 확인.
3. 그룹17(B10): KYEC, ASE, PTI 인식 확인.
4. 그룹/소제목 COUNT 및 국내·해외 관심종목 표시 확인.
5. TPRO의 거래소 코드와 삼성 POP 지원이 확인되면 B02에 수동 등록 또는 SBT 증분.
