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
    page_title="LEGACY: 주가위치 연구 데모 (SMA240 고정배율)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일링
st.markdown("""
<style>
    .metric-card {
        background: #181b24;
        border: 1px solid #2e3444;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .stage-badge {
        font-size: 1.15rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        display: inline-block;
    }
    .badge-ultra   { background-color: #880e4f; color: #f8bbd0; }
    .badge-grand   { background-color: #b71c1c; color: #ffcdd2; }
    .badge-top     { background-color: #d32f2f; color: #ffebee; }
    .badge-shldr   { background-color: #1b5e20; color: #c8e6c9; }
    .badge-waist   { background-color: #37474f; color: #eceff1; border: 1px solid #78909c; }
    .badge-thigh   { background-color: #e65100; color: #ffe0b2; }
    .badge-knee    { background-color: #0d47a1; color: #bbdefb; }
    .badge-ankle   { background-color: #006064; color: #b2ebf2; }
    .badge-gaksul  { background-color: #4a148c; color: #e1bee7; }
    .badge-trap    { background-color: #212121; color: #ffeb3b; border: 2px solid #ffeb3b; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 사이드바 설정
# -------------------------------------------------------------
with st.sidebar:
    st.title("📈 LEGACY 주가위치 데모")
    st.caption("SMA240×임의 고정배율 예전 데모 · 로그 5/7 연구 공식과 별개")
    st.divider()

    PRESET_STOCKS = {
        "삼천당제약 (000250) - 상투 수직낙하 사례": "000250",
        "성호전자 (043260) - 울트라상투 광기 사례": "043260",
        "SK하이닉스 (000660) - 실적 주도주 시세국면": "000660",
        "로보티즈 (108490) - 상투 후 2차 시도": "108490",
        "에코프로 (086520) - 2차 상투(각설이) 사례": "086520",
        "삼성전자 (005930)": "005930",
        "한미반도체 (042700)": "042700",
        "알테오젠 (196170)": "196170",
        "엔비디아 (NVDA)": "NVDA",
        "테슬라 (TSLA)": "TSLA",
        "[직접 입력]": "CUSTOM"
    }

    selected_preset = st.selectbox("🎯 주도주 케이스 빠른 선택", list(PRESET_STOCKS.keys()), index=0)
    
    if selected_preset == "[직접 입력]":
        ticker_input = st.text_input("종목 코드 입력 (예: 000660, NVDA)", value="000250").strip().upper()
    else:
        ticker_input = PRESET_STOCKS[selected_preset]

    period_years = st.select_slider(
        "📅 분석 기간 (최근 N년)",
        options=[2, 3, 5, 7, 10],
        value=5
    )
    
    use_log_scale = st.checkbox("로그 스케일 (Log Scale) 차트 적용", value=True)
    show_sub_ma = st.checkbox("보조 이평선(40/50/60/120선) 표시", value=True)
    
    st.divider()
    st.markdown("""
    **📋 LEGACY 가정 11개 라인 체계 (원작 공식 검증 아님)**
    * 🚨 **울트라상투 (8.88배)**: 임의 데모 기준 (상투 보장 불가)
    * ⚡ **대상투 (6.18배)**: 광기의 시작
    * ⚠️ **상투 (4.25배)**: 과거 임의 데모 기준
    * 🔔 **어깨 (2.85배)**: 1차 70% 분할 매도
    * ⭐ **허리 (2.12배)**: 시세 국면 지지축
    * 🚀 **허벅지 (1.46배)**: 시세 분출 / 진입 마지노선
    * 🔥 **무릎 (1.00배 - 240선)**: 유일한 정석 매수 타점!
    * 🌱 **턴어라운드1 (0.82배)**
    * 👣 **발목 (0.68배)**
    * 🌱 **턴어라운드2 (0.58배)**
    * ❄️ **각설이패턴 (0.51배)**
    """)

# -------------------------------------------------------------
# 데이터 로드
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
        return df if not df.empty else None
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

st.warning("LEGACY 연구 데모: 표시되는 무릎·상투와 행동 문구는 SMA240×임의 고정배율로 계산되며, 38개 수정종가 로그 5·7등분 연구의 검증된 매매 신호나 원작 공식이 아닙니다. 차트의 로그축 체크박스는 표시 방식만 변경합니다.")
with st.spinner(f"[{ticker_input}] 주가 데이터 로딩 중..."):
    raw_df = load_data(ticker_input, period_years)

if raw_df is None or len(raw_df) < 100:
    st.error("충분한 주가 데이터를 가져오지 못했습니다. 종목코드나 기간을 확인해 주세요.")
    st.stop()

df = calculate_position_levels(raw_df)

# 보조 이평선 추가
df["MA40"] = df["Close"].rolling(40).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["MA60"] = df["Close"].rolling(60).mean()
df["MA120"] = df["Close"].rolling(120).mean()

# 최근 데이터 분석
latest = df.iloc[-1]
close_p = latest["Close"]
knee_p = latest["Knee"]
ultra_p = latest["UltraTop"]
grand_p = latest["GrandTop"]
top_p = latest["Top"]
shldr_p = latest["Shoulder"]
waist_p = latest["Waist"]
thigh_p = latest["Thigh"]
ankle_p = latest["Ankle"]
gaksul_p = latest["Gaksul"]

# 1차 상투 발생 이력 및 기준선 전이 착시 감지
recent_120 = df.tail(120)
had_recent_top = (recent_120["High"] >= recent_120["Top"]).any()
is_transition_trap = had_recent_top and (close_p < shldr_p)

# 단계 및 행동 매뉴얼 판별
if close_p >= ultra_p:
    stage_name = "🚨 울트라상투 (100% 임계점)"
    stage_cls = "badge-ultra"
    action_text = "미련 없이 100% 전량 매도! 시장 에너지가 물리적으로 더 이상 팽창할 수 없는 절대 고점입니다."
    stage_idx = 7
elif close_p >= grand_p:
    stage_name = "⚡ 대상투 (광기의 영역)"
    stage_cls = "badge-grand"
    action_text = "전량 매도 권고! 극소수(0.1%) 종목만 진입하는 광기 구간으로 언제든 급락할 수 있습니다."
    stage_idx = 7
elif close_p >= top_p:
    stage_name = "⚠️ 상투 (현실적 최종 천정)"
    stage_cls = "badge-top"
    action_text = "전량 매도 원칙! 대다수 주도주의 현실적 최종 고점입니다. 삼천당제약처럼 수직 낙하하기 전에 전량 탈출하세요."
    stage_idx = 6
elif close_p >= shldr_p:
    stage_name = "🔔 어깨 (1차 분할 매도권)"
    stage_cls = "badge-shldr"
    action_text = "보유 물량의 70%를 1차 분할 매도하세요! 잔여 30%만 상투선 도달 여부를 지켜봅니다."
    stage_idx = 5
elif is_transition_trap:
    stage_name = "⛔ 기준선 전이 착시 주의구간"
    stage_cls = "badge-trap"
    action_text = "신규 매수 절대 금지! 1차 상투 후 이평선이 따라 올라와 주가가 낮아 보이는 '치명적인 착시' 구간입니다."
    stage_idx = 4
elif close_p >= waist_p:
    stage_name = "⭐ 허리 (시세 국면 지지축)"
    stage_cls = "badge-waist"
    action_text = "추세 홀딩 구간. 허리선 지지 여부를 관찰하며, 이탈 시 주의해야 합니다."
    stage_idx = 4
elif close_p >= thigh_p:
    stage_name = "🚀 허벅지 (시세 본격 분출)"
    stage_cls = "badge-thigh"
    action_text = "시세 분출 추세를 즐기며 홀딩하세요. 신규 매수는 허벅지 통과 전까지만 유효하므로 진입은 마감되었습니다."
    stage_idx = 3
elif close_p >= knee_p:
    stage_name = "🔥 무릎 (유일한 정석 매수 타점!)"
    stage_cls = "badge-knee"
    action_text = "🔴 무릎통과신호 발생! 240선 중심축을 뚫어낸 가장 안전하고 손익비가 높은 최적의 매수 기회입니다."
    stage_idx = 2
elif close_p >= ankle_p:
    stage_name = "🌱 발목 (턴어라운드 모색)"
    stage_cls = "badge-ankle"
    action_text = "매수 금지! 바닥과 발목에서는 사지 않는 것이 원칙입니다. 무릎선을 뚫고 올라올 때까지 관망하세요."
    stage_idx = 1
else:
    stage_name = "❄️ 각설이패턴 (바닥권 수렴)"
    stage_cls = "badge-gaksul"
    action_text = "매수 금지! 바닥 아래에 지하실이 더 있을 수 있습니다. 무릎 돌파를 확인할 때까지 절대 진입하지 마세요."
    stage_idx = 0

ratio_to_knee = ((close_p - knee_p) / knee_p) * 100
gain_to_shldr = ((shldr_p - close_p) / close_p) * 100
gain_to_top   = ((top_p - close_p) / close_p) * 100

# -------------------------------------------------------------
# 메인 헤더 & 스코어보드
# -------------------------------------------------------------
st.title(f"📊 [{ticker_input}] 주가위치 진단 리포트")
st.markdown(f"**현재 주가 위치:** <span class='stage-badge {stage_cls}'>{stage_name}</span>", unsafe_allow_html=True)

if is_transition_trap:
    st.error(f"⚠️ **[경고] {action_text}**")
elif "무릎" in stage_name:
    st.success(f"📌 **[행동 매뉴얼] {action_text}**")
elif "어깨" in stage_name or "상투" in stage_name:
    st.warning(f"📌 **[행동 매뉴얼] {action_text}**")
else:
    st.info(f"📌 **[행동 매뉴얼] {action_text}**")

# 핵심 지표 카드
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("현재 종가", f"{close_p:,.0f} 원")
with m2:
    st.metric("무릎선 (240선 기준축)", f"{knee_p:,.0f} 원", f"{ratio_to_knee:+.2f}%")
with m3:
    st.metric("어깨선 (1차 70% 익절)", f"{shldr_p:,.0f} 원", f"{gain_to_shldr:+.1f}%")
with m4:
    st.metric("상투선 (현실적 최종 천정)", f"{top_p:,.0f} 원", f"{gain_to_top:+.1f}%")
with m5:
    st.metric("울트라상투 (100% 임계점)", f"{ultra_p:,.0f} 원")

# 진행도 바
st.markdown("#### 🎯 주가 위치 진행 단계")
prog = min(max((stage_idx + 1) / 8.0, 0.05), 1.0)
st.progress(prog)
c_labels = ["1.각설이", "2.발목", "3.무릎(매수)", "4.허벅지", "5.허리", "6.어깨(70%매도)", "7.상투(전량매도)", "8.울트라상투"]
cols = st.columns(8)
for i, c in enumerate(cols):
    if i == stage_idx:
        c.markdown(f"**👉 `{c_labels[i]}`**")
    else:
        c.caption(c_labels[i])

st.divider()

# -------------------------------------------------------------
# 탭 구성: 차트 / 백테스트 / HTS 수식 / 매매 매뉴얼
# -------------------------------------------------------------
tab_chart, tab_backtest, tab_manual, tab_code = st.tabs([
    "📈 11개 라인 인터랙티브 차트", 
    "🧪 매매 매뉴얼 백테스팅", 
    "📖 댕기왕자 공식 매매 매뉴얼", 
    "💻 키움 영웅문 & 트레이딩뷰 수식"
])

# 탭 1: 인터랙티브 차트
with tab_chart:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.82, 0.18])

    # 캔들스틱
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name="캔들스틱", increasing_line_color="#FF1744", decreasing_line_color="#2979FF"
    ), row=1, col=1)

    # 11개 라인 플롯 (차트 이미지와 100% 동일한 색상)
    fig.add_trace(go.Scatter(x=df.index, y=df["UltraTop"], line=dict(color="#FF007F", width=2), name="울트라상투 (8.88배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["GrandTop"], line=dict(color="#D50000", width=2), name="대상투 (6.18배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Top"], line=dict(color="#E0E0E0", width=2, dash="dash"), name="상투 (4.25배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Shoulder"], line=dict(color="#00C853", width=2), name="어깨 (2.85배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Waist"], line=dict(color="#FFFFFF", width=2.5), name="허리 (2.12배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Thigh"], line=dict(color="#FF6D00", width=2), name="허벅지 (1.46배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Knee"], line=dict(color="#2962FF", width=3.5), name="무릎 (1.00배 - 240선)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Turn1"], line=dict(color="#BA68C8", width=1), name="턴어라운드1 (0.82배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Ankle"], line=dict(color="#FF4081", width=1.5), name="발목 (0.68배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Turn2"], line=dict(color="#CE93D8", width=1), name="턴어라운드2 (0.58배)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Gaksul"], line=dict(color="#7B1FA2", width=1.5), name="각설이패턴 (0.51배)"), row=1, col=1)

    # 보조 이평선
    if show_sub_ma:
        fig.add_trace(go.Scatter(x=df.index, y=df["MA40"], line=dict(color="#F48FB1", width=1), name="단순 40"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["MA60"], line=dict(color="#FFE082", width=1), name="단순 60"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["MA120"], line=dict(color="#B0BEC5", width=1.2), name="단순 120"), row=1, col=1)

    # 거래량
    v_colors = ['#FF1744' if c >= o else '#2979FF' for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], marker_color=v_colors, name="거래량", opacity=0.7), row=2, col=1)

    y_axis_type = "log" if use_log_scale else "linear"
    fig.update_layout(
        template="plotly_dark",
        height=720,
        margin=dict(l=30, r=30, t=30, b=30),
        xaxis_rangeslider_visible=False,
        yaxis=dict(type=y_axis_type, title="가격 (원)"),
        yaxis2=dict(title="거래량"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, width='stretch')

# 탭 2: 백테스팅 시뮬레이션
with tab_backtest:
    st.subheader(f"🧪 [{ticker_input}] 댕기왕자 공식 매매 매뉴얼 백테스팅")
    st.markdown("""
    * **매수**: 바닥/발목 매수 금지! 240 무릎선 상향 돌파 시 매수 (허벅지 통과 전까지만 유효)
    * **1차 매도**: 어깨선(2.85배) 도달 시 물량의 **70% 1차 분할 익절**
    * **2차 매도**: 상투선(4.25배) 도달 시 잔여 **30% 전량 익절** (수직낙하 방지)
    * **손익 보전**: 어깨 도달 후 조정 시 허벅지선 이탈 시 전량 매도
    * **착시 필터**: 최근 120일 내 상투를 친 적이 있으면 기준선 전이 착시로 간주하여 신규 매수 금지
    """)
    
    if st.button("🚀 백테스트 실행하기", key="btn_run_bt"):
        with st.spinner("시뮬레이션 실행 중..."):
            res = run_backtest(df)
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("누적 수익률", f"{res['total_return_pct']:+.2f} %")
            c2.metric("최대 낙폭 (MDD)", f"{res['max_drawdown_pct']:.2f} %")
            c3.metric("최종 자산", f"{res['final_equity']:,.0f} 원")
            c4.metric("매매 승률 (Win Rate)", f"{res['win_rate']:.1f} %")

            fig_eq = go.Figure()
            fig_eq.add_trace(go.Scatter(x=res["equity"].index, y=res["equity"]["Equity"], line=dict(color="#00E676", width=2.5), name="계좌 평가액"))
            fig_eq.update_layout(template="plotly_dark", height=380, title="누적 자산 성장 곡선 (Equity Curve)", yaxis_title="평가액 (원)")
            st.plotly_chart(fig_eq, width='stretch')

            if not res["trades"].empty:
                st.markdown("#### 📋 상세 매매 기록")
                st.dataframe(res["trades"], width='stretch')

# 탭 3: 댕기왕자 공식 매매 매뉴얼
with tab_manual:
    st.subheader("📖 댕기왕자의 투자이야기 - 주가위치분석 공식 매뉴얼")
    st.markdown("""
    ### 1. 매수 매뉴얼
    1. **바닥과 발목에서는 절대 사지 않는다.** 무릎선을 통과할 때(또는 통과 후 지지 확인 시) 매수한다.
       * *cf) 빨간색 화살표(무릎통과신호)가 나올 때 매수한다.*
    2. 그 종목만 무릎을 통과한 게 아니라 같은 섹터 친구들까지 함께 무릎을 통과했는지 확인한다.
    3. 핵심 섹터의 주도주를 매수한다 (실적 주도주, 수급 주도주, 차트 주도주 중 실적 주도주가 가장 안정적).
    4. **늦어도 최대 허벅지를 통과하기 전까지만 매수 구간으로 본다.** (허벅지 통과 후는 신규 매수 금지)
    5. **어깨 이상까지 우직하게 보유한다.**

    ---

    ### 2. 매도 매뉴얼
    * **표준 매도 전략**:
      1. **1차 상투(어깨)에서 70% 매도** 후, 1차 상투에서 바로 어깨 위 상투까지 도달하면 **잔여 30% 전량 매도**한다.
         * *cf) 매도 신호(파란색 아래 화살표)가 나오지 않았다면 좀 더 기다려 본다.*
      2. 70% 어깨 도달 후 매도했고, 어깨에서 조정이 나오는데 **허벅지 라인을 이탈 시 전량 매도**한다.
      3. 이탈하지 않고 각설이 패턴이 나오면서 2차 상투를 만들면 그때 전량 매도한다.
    * **보수적 매도 전략**:
      * 1차 상투(어깨)에서 미련 없이 전량 매도한다.

    ---

    ### 3. 각설이 패턴(2차 상투)과 상투 이후의 운명
    * **재상투(각설이 패턴)의 확률은 전체 주도주의 10% 미만이다.** 나머지 90%는 상투 치면 재상승하지 못하고 다 하락한다.
    * 재상투를 노리는 투자는 상당한 난이도를 요구하며, **쉽게 가려면 각설이 패턴을 먹으려고 하지 않으면 된다.**
    * **기준선 전이 착시 경고**: 1차 상투 이후 이평선이 따라 올라와 주가 위치가 낮아 보이는 구간은 기회가 아니라 리스크 관리 영역이다.
    * **성호전자 vs 삼천당제약**:
      * 실체가 약한 종목(삼천당제약)은 상투 치고 즉시 수직 낙하(-68%)하여 폐허가 된다.
      * 실체가 강한 종목(성호전자)이라도 울트라상투에 들어오면 수학적으로 100% 상투이므로 전량 탈출해야 한다.
    """)

# 탭 4: HTS 및 트레이딩뷰 수식
with tab_code:
    st.subheader("💻 실전 HTS / 트레이딩뷰 수식 코드")
    sub1, sub2 = st.tabs(["키움증권 (영웅문4 수식관리자)", "트레이딩뷰 (TradingView Pine Script)"])
    
    with sub1:
        st.markdown("**영웅문4 수식관리자 입력용 (지표 2개 + 신호검색 3개)**")
        k_path = os.path.join(os.path.dirname(__file__), "kiwoom_formulas.txt")
        if os.path.exists(k_path):
            with open(k_path, "r", encoding="utf-8") as f:
                st.code(f.read(), language="text")
                
    with sub2:
        st.markdown("**트레이딩뷰 Pine Script v5 코드**")
        p_path = os.path.join(os.path.dirname(__file__), "stock_position_system.pine")
        if os.path.exists(p_path):
            with open(p_path, "r", encoding="utf-8") as f:
                st.code(f.read(), language="pine")
