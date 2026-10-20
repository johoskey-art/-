# 엔진 데이터 계약 v0 — 차트선·주도주성·반례 분리

## 왜 세 테이블로 분리하는가

원작 위치선이 그려진 화면은 **모델 출력의 관측값**이고, EPS·밸류·실적은 **입력 조건**, 최종 주도주/비주도주 판정은 **결과 레이블**이다. 이 셋을 한 열이나 한 점수로 섞으면 사후 고점·선택편향이 다시 들어온다.

```text
원작 차트선                 EPS·밸류·섹터·수급             미래의 실제 경로
→ PositionBandObservation   → LeaderGateFeature            → OutcomeLabel
           \                         |                          /
            \___________________ 검증 시 결합 _________________/
```

## 1. `chart_band_observations.csv` — 위치선의 정답 라벨

차트당 한 행이 아니라, **한 화면 × 한 x시점 × 한 밴드**가 한 행이다.

| 필드 | 설명 |
|---|---|
| image_id / ticker / chart_asof | 원본 화면 식별 |
| x_chart_date | 화면 내부의 실제 거래일. 화면 캡처일과 분리 |
| band | knee, thigh, waist, shoulder, top, grand_top 등 |
| y_px / price_low / price_high | 픽셀 관측과 가격축 역변환 범위 |
| price_axis | LOG / LINEAR / UNKNOWN |
| observation_quality | tooltip / direct line / occluded / inferred |
| original_indicator_confirmed | 원작 지표 여부 |

툴팁 없는 JPEG는 `price_low~price_high` 범위로 보관한다. 점 추정 가격을 사실처럼 고정하지 않는다.

## 2. `leader_gate_features.csv` — 위치선을 신뢰할지 판단하는 입력

모든 값은 해당 거래일 당시 알 수 있던 것만 쓴다.

| 범주 | 초기 변수 |
|---|---|
| 가격구조 | 박스권 지속일, 전고점/박스 돌파, 돌파 후 지지, 변동성 |
| 수급 | 거래대금 백분위, 거래량 확장, 상대강도, 섹터 동행률 |
| 실적 | 매출·영업이익·EPS 컨센서스의 방향과 가속도 |
| 밸류 | 12개월 선행 PER, 목표 PER 변화, ROE, 밸류의 실적 반영 정도 |
| 분류 | 실적형/테마형/혼합, 산업, 시대, 기업규모 |
| 배제 | 최근 1차 상투·급락·기준선 전이 후 재반등 여부 |

PER의 절대값만으로 탈락시키지 않는다. 실적 가속도·컨센서스 변화와 함께 해석한다.

## 3. `cycle_outcomes.csv` — 사후 검증용 결과

| 필드 | 설명 |
|---|---|
| cycle_id / gate_date | 무릎 통과 후보일과 확정·후보 상태 |
| L / H / adjust_method | 수정가격 저점·고점. H는 학습/평가에서만 사용 |
| max_stage_reached | 허벅지/허리/어깨/상투 미도달도 포함 |
| terminal_type | 추세 지속, 중간 종료, 상투 후 붕괴, 우측 검열 |
| leader_outcome | 주도주/비주도주/보류와 근거 |

## 첫 모델의 출력 계약

```json
{
  "ticker": "000000",
  "asof": "YYYY-MM-DD",
  "leader_gate": "confirmed | candidate | rejected | unknown",
  "leader_confidence": "0-100",
  "position": "below_knee | knee_to_thigh | thigh_to_waist | waist_to_shoulder | above_shoulder | post_top",
  "bands": {
    "knee": {"low": null, "high": null, "quality": "unverified"},
    "thigh": {"low": null, "high": null, "quality": "inferred"},
    "waist": {"low": null, "high": null, "quality": "inferred"},
    "shoulder": {"low": null, "high": null, "quality": "inferred"},
    "top": {"low": null, "high": null, "quality": "insufficient_evidence"}
  },
  "warnings": ["no_future_peak_input", "original_formula_not_identified"]
}
```

범위·신뢰도·근거가 없는 단일 목표가는 출력하지 않는다.

## 다음 구현 순서

1. PF013~PF041처럼 차트와 EPS/밸류 표가 짝지어진 종목부터 시점 정합 원장을 만든다.
2. SK하이닉스·SK텔레콤·두산·두산에너빌리티는 긴 시계열의 밴드 관측·상태전이 표본으로 쓴다.
3. BGF리테일·하나기술 등은 주도주성 반례인지 확인한 뒤 대조군으로 확정한다.
4. `LeaderGate`와 `PositionBands`를 같은 점수로 합치지 않고 각각 검증한다.
