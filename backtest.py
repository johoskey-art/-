"""
주가위치분석시스템 (Stock Position Analysis System) - 전략 백테스팅 모듈
역대 주도주 5대 사이클의 로그-피보나치 7단계 모델 기반 검증
"""

import math
import sys
import argparse
import pandas as pd
import numpy as np

# Windows 콘솔 인코딩 호환성 설정
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import FinanceDataReader as fdr
import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker: str, start_date: str = "2015-01-01"):
    """
    한국 주식(6자리 코드) 또는 해외 주식(알파벳 티커) 데이터를 가져옵니다.
    """
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

def calculate_position_levels(df: pd.DataFrame, ma_period: int = 300):
    """
    300일 이동평균선(무릎선)과 7단계 주가위치 라인을 계산합니다.
    """
    df = df.copy()
    
    # 300일 이중평활(TMA) 또는 단순이평(SMA)
    half = math.ceil(ma_period / 2)
    df["MA300"] = df["Close"].rolling(half).mean().rolling(ma_period - half + 1).mean()
    df["MA300"] = df["MA300"].fillna(df["Close"].rolling(ma_period).mean())
    
    # 7단계 배율
    df["Knee"]    = df["MA300"]                       # 3. 무릎 (2.25배 기준축)
    df["Gaksul"]  = df["Knee"] / 2.246                # 1. 각설이 (바닥권)
    df["Ankle"]   = df["Knee"] / 1.531                # 2. 발목 (1차 턴어라운드)
    df["Thigh"]   = df["Knee"] * 1.581                # 4. 허벅지 (본격 분출)
    df["Waist"]   = df["Thigh"] * 1.618               # 5. 허리 (중간 지지)
    df["Shoulder"]= df["Waist"] * 1.406               # 6. 어깨 (분할 매도)
    df["Top"]     = df["Knee"] * 5.911                # 7. 상투 (13.3배 과열권)
    
    return df

def run_backtest(df: pd.DataFrame, initial_cash: float = 10_000_000):
    """
    무릎선 돌파 매수 및 단계별 분할 익절 전략 백테스트
    - 매수: 주가가 무릎선(300선) 상향 돌파
    - 분할 익절: 허리(30%), 어깨(40%), 상투(잔여 전량)
    - 손절: 무릎선 대비 -8% 하회 시 전량 손절
    """
    cash = initial_cash
    shares = 0
    trade_history = []
    equity_curve = []
    
    in_position = False
    entry_price = 0
    stage_exits = {"waist": False, "shoulder": False}
    
    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        date = df.index[i]
        close = row["Close"]
        knee = row["Knee"]
        
        if pd.isna(knee):
            equity_curve.append(cash)
            continue
            
        # 1. 매수 시그널: 무릎선 골든크로스
        if not in_position and (prev_row["Close"] <= prev_row["Knee"]) and (close > knee):
            shares = int(cash // close)
            if shares > 0:
                cost = shares * close
                cash -= cost
                entry_price = close
                in_position = True
                stage_exits = {"waist": False, "shoulder": False}
                trade_history.append({
                    "date": date, "type": "BUY", "price": close, "shares": shares, "reason": "무릎선 상향돌파"
                })
        
        # 2. 포지션 보유 중 익절/손절 관리
        elif in_position:
            # 손절: 매수가 대비 -8% 또는 무릎선 -5% 이탈
            if close <= entry_price * 0.92 or close < knee * 0.95:
                sell_val = shares * close
                cash += sell_val
                pnl = (close - entry_price) / entry_price * 100
                trade_history.append({
                    "date": date, "type": "STOP_LOSS", "price": close, "shares": shares, "pnl_pct": pnl, "reason": "손절"
                })
                shares = 0
                in_position = False
                
            # 허리선 도달 1차 분할 익절 (30%)
            elif not stage_exits["waist"] and close >= row["Waist"]:
                sell_shares = int(shares * 0.3)
                if sell_shares > 0:
                    cash += sell_shares * close
                    shares -= sell_shares
                    stage_exits["waist"] = True
                    trade_history.append({
                        "date": date, "type": "PARTIAL_TP1", "price": close, "shares": sell_shares, 
                        "pnl_pct": (close - entry_price) / entry_price * 100, "reason": "허리선 도달 (30% 익절)"
                    })
                    
            # 어깨선 도달 2차 분할 익절 (보유량의 50%)
            elif not stage_exits["shoulder"] and close >= row["Shoulder"]:
                sell_shares = int(shares * 0.5)
                if sell_shares > 0:
                    cash += sell_shares * close
                    shares -= sell_shares
                    stage_exits["shoulder"] = True
                    trade_history.append({
                        "date": date, "type": "PARTIAL_TP2", "price": close, "shares": sell_shares, 
                        "pnl_pct": (close - entry_price) / entry_price * 100, "reason": "어깨선 도달 (분할 익절)"
                    })
                    
            # 상투선 도달 최종 익절 (전량)
            elif close >= row["Top"]:
                cash += shares * close
                trade_history.append({
                    "date": date, "type": "FULL_TP", "price": close, "shares": shares, 
                    "pnl_pct": (close - entry_price) / entry_price * 100, "reason": "상투선 도달 (전량 익절)"
                })
                shares = 0
                in_position = False
                
        current_equity = cash + (shares * close)
        equity_curve.append(current_equity)
        
    df_equity = pd.DataFrame({"Equity": equity_curve}, index=df.index[len(df) - len(equity_curve):])
    
    # 성과 지표 계산
    total_return = (df_equity["Equity"].iloc[-1] - initial_cash) / initial_cash * 100
    peak = df_equity["Equity"].cummax()
    drawdown = (df_equity["Equity"] - peak) / peak * 100
    mdd = drawdown.min()
    
    trades_df = pd.DataFrame(trade_history)
    win_trades = [t for t in trade_history if "pnl_pct" in t and t["pnl_pct"] > 0]
    all_exits = [t for t in trade_history if "pnl_pct" in t]
    win_rate = (len(win_trades) / len(all_exits) * 100) if all_exits else 0
    
    results = {
        "initial_cash": initial_cash,
        "final_equity": df_equity["Equity"].iloc[-1],
        "total_return_pct": total_return,
        "max_drawdown_pct": mdd,
        "total_trades": len(all_exits),
        "win_rate": win_rate,
        "trades": trades_df,
        "equity": df_equity
    }
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="주가위치 7단계 백테스팅")
    parser.add_argument("--ticker", type=str, default="000660", help="종목 코드 (기본: SK하이닉스 000660)")
    parser.add_argument("--start", type=str, default="2016-01-01", help="시작 일자 (YYYY-MM-DD)")
    args = parser.parse_args()
    
    print(f"📊 [{args.ticker}] 데이터 다운로드 및 7단계 백테스팅 실행 중...")
    df = get_stock_data(args.ticker, args.start)
    if df is not None and not df.empty:
        df = calculate_position_levels(df)
        res = run_backtest(df)
        print("=" * 60)
        print(f"📈 백테스트 결과 보고서: {args.ticker}")
        print("=" * 60)
        print(f"• 초기 자본금   : {res['initial_cash']:,} 원")
        print(f"• 최종 평가액   : {res['final_equity']:,.0f} 원")
        print(f"• 누적 수익률   : {res['total_return_pct']:+.2f} %")
        print(f"• 최대 낙폭(MDD): {res['max_drawdown_pct']:.2f} %")
        print(f"• 총 매도 횟수  : {res['total_trades']} 회")
        print(f"• 승률 (WinRate): {res['win_rate']:.1f} %")
        print("=" * 60)
        if not res["trades"].empty:
            print("\n[최근 매매 기록]")
            print(res["trades"].tail(10).to_string(index=False))
