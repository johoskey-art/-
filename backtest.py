"""
LEGACY / 실험용: SMA240 고정배율 매매 백테스트 (원작 공식 검증되지 않음)
[주의: 기존 백테스트용 고정배율 가정; 38개 주도주 Adj_Close 로그 5/7 등분 연구와 분리]

[핵심 매매 매뉴얼]
1. 매수: 바닥/발목 매수 금지. 240일 무릎선 상향 돌파 시 매수 (허벅지 통과 전까지만 유효)
2. 매도:
   - 어깨선(2.85배) 도달 시 보유 물량 70% 1차 익절
   - 상투선(4.25배) 도달 시 잔여 30% 전량 익절 (수직 낙하 방지)
   - 어깨 터치 후 조정 시 허벅지선 이탈하면 전량 익절/손절
3. 기준선 전이 착시 필터:
   - 1차 상투 후 이평선이 따라 올라와 주가 위치가 낮아 보여도 재진입 금지
"""

import sys
import math
import argparse
import pandas as pd
import numpy as np

# Windows 콘솔 인코딩 호환성
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import FinanceDataReader as fdr
import yfinance as yf

def get_stock_data(ticker: str, start_date: str = "2020-01-01"):
    try:
        if ticker.isdigit():
            df = fdr.DataReader(ticker, start_date)
        else:
            df = yf.download(ticker, start=start_date, progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
        df = df.dropna()
        return df
    except Exception as e:
        print(f"데이터 다운로드 실패 ({ticker}): {e}")
        return None

def calculate_position_levels(df: pd.DataFrame, ma_period: int = 240):
    """
    댕기왕자 공식 모델 11개 라인 계산 (240선 중심축)
    """
    df = df.copy()
    df["Knee"] = df["Close"].rolling(ma_period).mean() # 파란색 무릎선
    
    # 상단 라인 (시세 국면 ~ 광기 영역)
    df["Thigh"]    = df["Knee"] * 1.46  # 허벅지 (시세 본격 분출)
    df["Waist"]    = df["Knee"] * 2.12  # 허리 (시세 지지축)
    df["Shoulder"] = df["Knee"] * 2.85  # 어깨 (1차 70% 분할 매도)
    df["Top"]      = df["Knee"] * 4.25  # 상투 (현실적 최종 천정, 전량 매도)
    df["GrandTop"] = df["Knee"] * 6.18  # 대상투 (광기의 시작)
    df["UltraTop"] = df["Knee"] * 8.88  # 울트라상투 (100% 임계점)
    
    # 하단 라인 (바닥 ~ 턴어라운드)
    df["Turn1"]    = df["Knee"] * 0.82  # 턴어라운드1
    df["Ankle"]    = df["Knee"] * 0.68  # 발목
    df["Turn2"]    = df["Knee"] * 0.58  # 턴어라운드2
    df["Gaksul"]   = df["Knee"] * 0.51  # 각설이패턴 (바닥)
    
    return df

def run_backtest(df: pd.DataFrame, initial_cash: float = 10_000_000):
    cash = initial_cash
    shares = 0
    trade_history = []
    equity_curve = []
    
    in_position = False
    entry_price = 0
    sold_shoulder = False
    last_top_index = -9999
    
    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        date = df.index[i]
        close = row["Close"]
        knee = row["Knee"]
        high = row["High"]
        
        if pd.isna(knee):
            equity_curve.append(cash)
            continue
            
        # 1차 상투 발생 여부 추적
        if high >= row["Top"]:
            last_top_index = i
            
        # 기준선 전이 착시 필터: 최근 120일 이내에 상투를 친 적이 있으면 신규 매수 금지!
        is_transition_trap = (i - last_top_index < 120)
        
        # 1. 매수 시그널: 바닥/발목 매수 금지! 240 무릎선 골든크로스 시 매수
        if not in_position and not is_transition_trap:
            if (prev_row["Close"] <= prev_row["Knee"]) and (close > knee):
                shares = int(cash // close)
                if shares > 0:
                    cost = shares * close
                    cash -= cost
                    entry_price = close
                    in_position = True
                    sold_shoulder = False
                    trade_history.append({
                        "date": date, "type": "BUY", "price": close, "shares": shares,
                        "reason": "🔴 무릎선 상향돌파 (정석 매수 타점)"
                    })
        
        # 2. 보유 중 매도 매뉴얼
        elif in_position:
            # A. 손절: 무릎선 대비 -7% 하회 시 즉시 손절 (원칙)
            if close < knee * 0.93:
                sell_val = shares * close
                cash += sell_val
                pnl = (close - entry_price) / entry_price * 100
                trade_history.append({
                    "date": date, "type": "STOP_LOSS", "price": close, "shares": shares,
                    "pnl_pct": pnl, "reason": "무릎선 -7% 이탈 손절"
                })
                shares = 0
                in_position = False
                
            # B. 1차 매도: 어깨선(2.85배) 도달 시 70% 분할 익절!
            elif not sold_shoulder and high >= row["Shoulder"]:
                sell_shares = int(shares * 0.7)
                if sell_shares > 0:
                    cash += sell_shares * close
                    shares -= sell_shares
                    sold_shoulder = True
                    pnl = (close - entry_price) / entry_price * 100
                    trade_history.append({
                        "date": date, "type": "PARTIAL_TP (70%)", "price": close, "shares": sell_shares,
                        "pnl_pct": pnl, "reason": "어깨선 도달 (1차 70% 분할 익절)"
                    })
                    
            # C. 2차 전량 매도: 상투선(4.25배) 도달 시 잔여 30% 전량 익절 (삼천당제약 수직낙하 방지!)
            elif high >= row["Top"]:
                cash += shares * close
                pnl = (close - entry_price) / entry_price * 100
                trade_history.append({
                    "date": date, "type": "FULL_TP (상투)", "price": close, "shares": shares,
                    "pnl_pct": pnl, "reason": "🔵 상투선 도달 (전량 익절 및 탈출)"
                })
                shares = 0
                in_position = False
                
            # D. 어깨 도달 후 조정 시 허벅지선 이탈하면 잔여 물량 전량 청산
            elif sold_shoulder and close < row["Thigh"]:
                cash += shares * close
                pnl = (close - entry_price) / entry_price * 100
                trade_history.append({
                    "date": date, "type": "TRAILING_STOP", "price": close, "shares": shares,
                    "pnl_pct": pnl, "reason": "어깨 도달 후 허벅지선 이탈 (수익 보전 전량 매도)"
                })
                shares = 0
                in_position = False
                
        current_equity = cash + (shares * close)
        equity_curve.append(current_equity)
        
    df_equity = pd.DataFrame({"Equity": equity_curve}, index=df.index[len(df) - len(equity_curve):])
    total_return = (df_equity["Equity"].iloc[-1] - initial_cash) / initial_cash * 100
    peak = df_equity["Equity"].cummax()
    drawdown = (df_equity["Equity"] - peak) / peak * 100
    mdd = drawdown.min()
    
    trades_df = pd.DataFrame(trade_history)
    exits = [t for t in trade_history if "pnl_pct" in t]
    win_exits = [t for t in exits if t["pnl_pct"] > 0]
    win_rate = (len(win_exits) / len(exits) * 100) if exits else 0
    
    return {
        "initial_cash": initial_cash,
        "final_equity": df_equity["Equity"].iloc[-1],
        "total_return_pct": total_return,
        "max_drawdown_pct": mdd,
        "total_trades": len(exits),
        "win_rate": win_rate,
        "trades": trades_df,
        "equity": df_equity
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="주가위치 댕기왕자 공식 백테스팅")
    parser.add_argument("--ticker", type=str, default="000250", help="종목 코드 (기본: 삼천당제약 000250)")
    parser.add_argument("--start", type=str, default="2022-01-01", help="시작 일자")
    args = parser.parse_args()
    
    print(f"📊 [{args.ticker}] 댕기왕자 주가위치 공식 매매 매뉴얼 백테스팅 실행 중...")
    df = get_stock_data(args.ticker, args.start)
    if df is not None and not df.empty:
        df = calculate_position_levels(df)
        res = run_backtest(df)
        print("=" * 65)
        print(f"📈 백테스트 결과: {args.ticker}")
        print("=" * 65)
        print(f"• 초기 자본금   : {res['initial_cash']:,} 원")
        print(f"• 최종 평가액   : {res['final_equity']:,.0f} 원")
        print(f"• 누적 수익률   : {res['total_return_pct']:+.2f} %")
        print(f"• 최대 낙폭(MDD): {res['max_drawdown_pct']:.2f} %")
        print(f"• 총 매도 횟수  : {res['total_trades']} 회")
        print(f"• 승률 (WinRate): {res['win_rate']:.1f} %")
        print("=" * 65)
        if not res["trades"].empty:
            print("\n[상세 매매 일지]")
            print(res["trades"].to_string(index=False))
