import sys
import os
import math
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Windows 콘솔 인코딩 호환성
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import FinanceDataReader as fdr
import yfinance as yf
from backtest import calculate_position_levels, run_backtest

# 페이지 설정
st.set_page_config(
    page_title="주가위치분석시스템 (Stock Position System)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일링
st.markdown("""
<style>
    .metric-card {
        background: #1e222d;
        border: 1px solid #2e3444;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .stage-badge {
        font-size: 1.15rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        display: inline-block;
    }
    .badge-gaksul { background-color: #4a148c; color: #e1bee7; }
    .badge-ankle  { background-color: #006064; color: #b2ebf2; }
    .badge-knee   { background-color: #0d47a1; color: #bbdefb; }
    .badge-thigh  { background-color: #1b5e20; color: #c8e6c9; }
    .badge-waist  { background-color: #f57f17; color: #fff9c4; }
    .badge-shldr  { background-color: #e65100; color: #ffe0b2; }
    .badge-top    { background-color: #b71c1c; color: #ffcdd2; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 사이드바 설정
# -------------------------------------------------------------
with st.sidebar:
    st.title("📈 주가위치분석시스템")
    st.caption("과거 5대 주도주 20선 실측 통계 기반 로그-피보나치 7단계 모델")
    st.divider()

    # 인기 종목 사전 프리셋
    PRESET_STOCKS = {
        "SK하이닉스 (000660)": "000660",
        "삼성전자 (005930)": "005930",
        "한미반도체 (042700)": "042700",
        "기아 (000270)": "000270",
        "현대차 (005380)": "005380",
        "알테오젠 (196170)": "196170",
        "삼양식품 (003230)": "003230",
        "HD현대일렉트릭 (267260)": "267260",
        "엔비디아 (NVDA)": "NVDA",
        "테슬라 (TSLA)": "TSLA",
        "애플 (AAPL)": "AAPL",
        "[직접 입력]": "CUSTOM"
    }

    selected_preset = st.selectbox("🎯 주도주 빠른 선택", list(PRESET_STOCKS.keys()), index=0)
    
    if selected_preset == "[직접 입력]":
        ticker_input = st.text_input("종목 코드 입력 (예: 000660, NVDA)", value="000660").strip().upper()
    else:
        ticker_input = PRESET_STOCKS[selected_preset]

    period_years = st.select_slider(
        "📅 분석 기간 (최근 N년)",
        options=[2, 3, 5, 7, 10, 15],
        value=5
    )
    
    use_log_scale = st.checkbox("로그 스케일 (Log Scale) 차트 적용", value=True)
    show_sub_ma = st.checkbox("보조 이평선(40/50/60/120선) 표시", value=True)
    
    st.divider()
    st.markdown("""
    **💡 7단계 주가위치 구조**
    1. ❄️ **각설이 (바닥권)**: 무릎 ÷ 2.246
    2. 🌱 **발목 (턴어라운드)**: 무릎 ÷ 1.531
    3. 🔥 **무릎 (추세돌파)**: 300일 초장기선
    4. 🚀 **허벅지 (시세분출)**: 무릎 × 1.581
    5. ⭐ **허리 (중간지지)**: 허벅지 × 1.618
    6. ⚠️ **어깨 (분할매도)**: 허리 × 1.406
    7. 🚨 **상투 (최종과열)**: 무릎 × 5.911 (13.3배)
    """)

# -------------------------------------------------------------
# 데이터 로드 함수
# -------------------------------------------------------------
@st.cache_data(ttl=600)
def load_data(ticker: str, years: int):
    start_date = (pd.Timestamp.now() - pd.DateOffset(years=years)).strftime("%Y-%m-%d")
    try:
        if ticker.isdigit():
            df = fdr.DataReader(ticker, start_date)
        else:
            df = yf.download(ticker, start=start_date, progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
        
        df = df.dropna()
        if df.empty:
            return None
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

# 데이터 다운로드 및 7단계 계산
with st.spinner(f"[{ticker_input}] 최근 {period_years}년 주가 데이터 로딩 중..."):
    raw_df = load_data(ticker_input, period_years)

if raw_df is None or len(raw_df) < 100:
    st.error("충분한 주가 데이터를 가져오지 못했습니다. 종목코드나 기간을 다시 확인해 주세요.")
    st.stop()

df = calculate_position_levels(raw_df)

# 보조 이평선 추가 계산
df["MA40"] = df["Close"].rolling(40).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["MA60"] = df["Close"].rolling(60).mean()
df["MA120"] = df["Close"].rolling(120).mean()

# 최근 행 데이터
latest = df.iloc[-1]
close_price = latest["Close"]
knee_price = latest["Knee"]
top_price = latest["Top"]
shoulder_price = latest["Shoulder"]
waist_price = latest["Waist"]
thigh_price = latest["Thigh"]
ankle_price = latest["Ankle"]
gaksul_price = latest["Gaksul"]

# 단계 판별
if close_price >= top_price:
    stage_name = "🚨 7. 상투 (최종 고점 과열권)"
    stage_cls = "badge-top"
    stage_score = 7
    guide_text = "전체 주도주 통계상 평균 고점(13.3배)에 도달한 과열권입니다. 신규 매수 금지 및 전량 분할 익절을 권고합니다."
elif close_price >= shoulder_price:
    stage_name = "⚠️ 6. 어깨 (분할 매도 구간)"
    stage_cls = "badge-shldr"
    stage_score = 6
    guide_text = "시세가 충분히 분출된 상단 구간입니다. 욕심을 줄이고 물량의 40~50%를 1차 분할 익절하는 전략이 안전합니다."
elif close_price >= waist_price:
    stage_name = "⭐ 5. 허리 (중간 눌림 및 지지)"
    stage_cls = "badge-waist"
    stage_score = 5
    guide_text = "상승 파동의 허리(황금비 지점)입니다. 허리선 지지 시 추가 매수(불타기)가 가능하며, 이탈 시 주의가 필요합니다."
elif close_price >= thigh_price:
    stage_name = "🚀 4. 허벅지 (본격 시세 분출)"
    stage_cls = "badge-thigh"
    stage_score = 4
    guide_text = "무릎을 뚫고 본격적인 주도주 랠리가 시작되는 구간입니다. 추세를 끝까지 즐기며 홀딩하는 단계입니다."
elif close_price >= knee_price:
    stage_name = "🔥 3. 무릎 (추세 돌파 완료 - 핵심 매수)"
    stage_cls = "badge-knee"
    stage_score = 3
    guide_text = "300일 초장기 이평선을 강하게 뚫어낸 가장 안전하고 손익비가 뛰어난 '핵심 매수 타점'입니다!"
elif close_price >= ankle_price:
    stage_name = "🌱 2. 발목 (1차 턴어라운드)"
    stage_cls = "badge-ankle"
    stage_score = 2
    guide_text = "바닥을 딛고 턴어라운드를 모색하는 단계입니다. 정찰조 분할 매수나 300선 돌파 대기가 유효합니다."
else:
    stage_name = "❄️ 1. 각설이 (바닥권 수렴)"
    stage_cls = "badge-gaksul"
    stage_score = 1
    guide_text = "주가가 역사적 바닥권에 위치해 있습니다. 거래량 수반 및 발목선 돌파 여부를 먼저 확인해야 합니다."

ratio_knee = ((close_price - knee_price) / knee_price) * 100
gain_to_top = ((top_price - close_price) / close_price) * 100

# -------------------------------------------------------------
# 메인 헤더 & 스코어보드
# -------------------------------------------------------------
st.title(f"📊 [{ticker_input}] 주가위치 진단 리포트")
st.markdown(f"**현재 주가 위치:** <span class='stage-badge {stage_cls}'>{stage_name}</span>", unsafe_allow_html=True)
st.info(f"📌 **행동 전략 가이드:** {guide_text}")

# 주요 지표 카드
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("현재 종가", f"{close_price:,.0f} 원")
with m2:
    st.metric("기준 무릎선 (300선)", f"{knee_price:,.0f} 원", f"{ratio_knee:+.2f}%")
with m3:
    st.metric("상투 목표가 (13.3배)", f"{top_price:,.0f} 원")
with m4:
    st.metric("상투까지 잔여 여력", f"{gain_to_top:+.1f}%")
with m5:
    st.metric("어깨 1차 매도가", f"{shoulder_price:,.0f} 원")

# 7단계 게이지 바
st.markdown("#### 🎯 7단계 위치 진행도")
progress_val = min(max(stage_score / 7.0, 0.05), 1.0)
st.progress(progress_val)
cols_stages = st.columns(7)
stages_lbls = ["1.각설이", "2.발목", "3.무릎(돌파)", "4.허벅지", "5.허리", "6.어깨(익절)", "7.상투(고점)"]
for idx, c in enumerate(cols_stages):
    if idx + 1 == stage_score:
        c.markdown(f"**👉 `{stages_lbls[idx]}`**")
    else:
        c.caption(stages_lbls[idx])

st.divider()

# -------------------------------------------------------------
# 탭 구성: 차트 / 백테스트 / 실측 데이터 / HTS 수식
# -------------------------------------------------------------
tab_chart, tab_backtest, tab_data, tab_code = st.tabs([
    "📈 7단계 인터랙티브 차트", 
    "🧪 백테스팅 시뮬레이션", 
    "📂 역대 주도주 20선 실측표", 
    "💻 HTS 및 트레이딩뷰 수식"
])

# 탭 1: 인터랙티브 차트
with tab_chart:
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.04, 
        row_heights=[0.8, 0.2]
    )

    # 캔들스틱 차트
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="캔들스틱",
            increasing_line_color="#FF334B",
            decreasing_line_color="#0066FF"
        ),
        row=1, col=1
    )

    # 7단계 라인 플롯
    fig.add_trace(go.Scatter(x=df.index, y=df["Top"], line=dict(color="#FF1744", width=2.5, dash="dash"), name="7. 상투선 (13.3배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Shoulder"], line=dict(color="#FF9100", width=2), name="6. 어깨선 (8.06배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Waist"], line=dict(color="#FFD600", width=2), name="5. 허리선 (5.73배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Thigh"], line=dict(color="#00E676", width=2), name="4. 허벅지선 (3.55배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Knee"], line=dict(color="#2979FF", width=3.5), name="3. 무릎선 (300선 기준축)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Ankle"], line=dict(color="#00E5FF", width=1.8), name="2. 발목선 (1.47배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Gaksul"], line=dict(color="#7C4DFF", width=1.8), name="1. 각설이선 (1.0배)"), row=1, col=1)

    # 보조 이평선
    if show_sub_ma:
        fig.add_trace(go.Scatter(x=df.index, y=df["MA40"], line=dict(color="#F06292", width=1), name="MA 40"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["MA60"], line=dict(color="#FFB74D", width=1), name="MA 60"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["MA120"], line=dict(color="#90A4AE", width=1.2), name="MA 120"), row=1, col=1)

    # 거래량
    colors = ['#FF334B' if c >= o else '#0066FF' for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(
        go.Bar(x=df.index, y=df["Volume"], marker_color=colors, name="거래량", opacity=0.7),
        row=2, col=1
    )

    y_type = "log" if use_log_scale else "linear"
    fig.update_layout(
        template="plotly_dark",
        height=720,
        margin=dict(l=30, r=30, t=30, b=30),
        xaxis_rangeslider_visible=False,
        yaxis=dict(type=y_type, title="가격 (원)"),
        yaxis2=dict(title="거래량"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# 탭 2: 백테스팅 시뮬레이션
with tab_backtest:
    st.subheader(f"🧪 [{ticker_input}] 무릎 돌파 매수 & 분할 익절 백테스트")
    st.markdown("""
    * **매수 조건**: 주가가 무릎선(300일 초장기선)을 상향 돌파할 때 매수
    * **익절 조건**: 허리선 도달(30%), 어깨선 도달(50%), 상투선 도달(잔여 전량)
    * **손절 조건**: 매수가 대비 -8% 또는 무릎선 -5% 이탈 시 전량 손절
    """)
    
    if st.button("🚀 백테스트 실행하기", key="btn_run_bt"):
        with st.spinner("전략 시뮬레이션 계산 중..."):
            res = run_backtest(df)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("누적 수익률", f"{res['total_return_pct']:+.2f} %")
            c2.metric("최대 낙폭 (MDD)", f"{res['max_drawdown_pct']:.2f} %")
            c3.metric("최종 자산", f"{res['final_equity']:,.0f} 원")
            c4.metric("매매 승률 (Win Rate)", f"{res['win_rate']:.1f} %")

            # 자산 곡선 차트
            fig_eq = go.Figure()
            fig_eq.add_trace(go.Scatter(x=res["equity"].index, y=res["equity"]["Equity"], line=dict(color="#00E676", width=2.5), name="계좌 평가액"))
            fig_eq.update_layout(template="plotly_dark", height=380, title="누적 자산 성장 곡선 (Equity Curve)", yaxis_title="평가액 (원)")
            st.plotly_chart(fig_eq, use_container_width=True)

            if not res["trades"].empty:
                st.markdown("#### 📋 상세 거래 내역")
                st.dataframe(res["trades"], use_container_width=True)

# 탭 3: 역대 주도주 20선 실측표
with tab_data:
    st.subheader("📂 1990~2020년대 5대 산업 사이클 역대 주도주 실측 데이터")
    csv_path = os.path.join(os.path.dirname(__file__), "data", "leading_stocks_data.csv")
    if os.path.exists(csv_path):
        data_df = pd.read_csv(csv_path)
        st.dataframe(data_df, use_container_width=True)
    else:
        st.warning("데이터 파일을 찾을 수 없습니다.")

# 탭 4: HTS 및 트레이딩뷰 수식
with tab_code:
    st.subheader("💻 실전 차트 적용 수식 코드")
    subtab1, subtab2 = st.tabs(["트레이딩뷰 (TradingView Pine Script)", "키움증권 (영웅문4 수식관리자)"])
    
    with subtab1:
        st.markdown("**트레이딩뷰 Pine Script v5 코드** (하단 Pine 에디터에 붙여넣기)")
        pine_path = os.path.join(os.path.dirname(__file__), "stock_position_system.pine")
        if os.path.exists(pine_path):
            with open(pine_path, "r", encoding="utf-8") as f:
                st.code(f.read(), language="pine")
                
    with subtab2:
        st.markdown("**키움증권 영웅문4 수식관리자 입력용 수식**")
        kiwoom_path = os.path.join(os.path.dirname(__file__), "kiwoom_formulas.txt")
        if os.path.exists(kiwoom_path):
            with open(kiwoom_path, "r", encoding="utf-8") as f:
                st.code(f.read(), language="text")
