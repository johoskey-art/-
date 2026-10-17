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
