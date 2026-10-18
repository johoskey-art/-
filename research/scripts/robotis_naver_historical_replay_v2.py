#!/usr/bin/env python3
"""Robotis 108490: reproducible historical OHLCV lookup and breakout audit.

Research-only reconstruction. Never mix later-adjusted quotes with the 2025
raw 49,000 quote; the same-scale feed is the sole input to all prior-high
comparisons. Run --offline-file on a saved Naver XML for reproducibility.

Usage:
  python research/scripts/robotis_naver_historical_replay_v2.py --out-dir research/results/robotis_replay
  python research/scripts/robotis_naver_historical_replay_v2.py --offline-file saved_sise.xml --out-dir /tmp/check
Naver endpoint may block automated requests. Preserve the exception and do
NOT silently substitute guessed or monthly OHLCV records.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SYMBOL = "108490"
EVENT = "2025-05-14"
WINDOWS = (20, 60, 120, 240, 250, 252)
URL = ("https://fchart.stock.naver.com/sise.nhn?symbol=108490"
       "&timeframe=day&requestType=1&startTime=20220101&endTime=20250515")

def get_xml(url: str) -> bytes:
    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; historical-ohlcv-research/1.0)",
        "Accept": "application/xml,text/xml,*/*"
    })
    with urllib.request.urlopen(request, timeout=25) as r:
        return r.read()

def parse_bars(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    bars = []
    for elem in root.iter():
        if elem.tag.lower().split("}")[-1] != "item":
            continue
        fields = elem.attrib.get("data", "").split("|")
        if len(fields) != 6:
            continue
        try:
            d = datetime.strptime(fields[0], "%Y%m%d").date().isoformat()
            op, hi, lo, cl, vol = (int(v) for v in fields[1:])
        except (ValueError, TypeError):
            continue
        if op <= 0 or hi <= 0 or lo <= 0 or cl <= 0 or vol <= 0:
            continue
        if not lo <= op <= hi or not lo <= cl <= hi:
            raise ValueError("inconsistent OHLC adjustment basis on " + d)
        bars.append({"date": d, "open": op, "high": hi, "low": lo,
                     "close": cl, "volume": vol})
    bars.sort(key=lambda x: x["date"])
    if len({x["date"] for x in bars}) != len(bars):
        raise ValueError("duplicate positive-volume trading dates")
    return bars

def audit(bars: list[dict]) -> tuple[list[dict], dict]:
    dates = [r["date"] for r in bars]
    if EVENT not in dates:
        raise ValueError("source has no event bar for " + EVENT)
    event_i = dates.index(EVENT)
    event = bars[event_i]
    prior = bars[:event_i]
    fields = {"symbol": SYMBOL, "date": EVENT, **event,
              "prior_sessions": len(prior),
              "prior_date": prior[-1]["date"] if prior else None}
    if prior:
        fields["pct_from_prev_close"] = 100 * (event["close"] / prior[-1]["close"] - 1)
    fields["volume_to_prior20"] = (
        event["volume"] / (sum(r["volume"] for r in prior[-20:]) / 20)
        if len(prior) >= 20 else None
    )
    signal_rows = []
    for i in range(len(bars)):
        if i >= event_i:
            break
        r = bars[i]
        if i < 120 or i < 20:
            continue
        p120 = bars[i - 120:i]
        p20 = bars[i - 20:i]
        mc = max(x["close"] for x in p120)
        mh = max(x["high"] for x in p120)
        volume_ratio = r["volume"] / (sum(x["volume"] for x in p20) / 20)
        ret = 100 * (r["close"] / bars[i - 1]["close"] - 1)
        if r["close"] > mc and r["high"] > mh:
            signal_rows.append({
                "symbol": SYMBOL, "date": r["date"], "close": r["close"],
                "high": r["high"], "prior120maxclose": mc, "prior120maxhigh": mh,
                "change_pct": round(ret, 8), "vol20ratio": round(volume_ratio, 8),
                "posthoc_plus5_vol2": int(ret >= 5 and volume_ratio >= 2),
                "days_before_event": event_i - i
            })
    for window in WINDOWS:
        key = "prior" + str(window)
        if len(prior) < window:
            fields[key + "_close_max"] = None
            fields[key + "_high_max"] = None
            fields[key + "_break_close"] = None
            fields[key + "_break_high"] = None
        else:
            p = prior[-window:]
            mc = max(x["close"] for x in p)
            mh = max(x["high"] for x in p)
            fields[key + "_close_max"] = mc
            fields[key + "_high_max"] = mh
            fields[key + "_break_close"] = int(event["close"] > mc)
            fields[key + "_break_high"] = int(event["high"] > mh)
    return signal_rows, fields

def write_csv(path: Path, records: list[dict]) -> None:
    if not records:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline-file", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()
    if args.offline_file:
        raw = args.offline_file.read_bytes()
    else:
        raw = get_xml(URL)
    data = parse_bars(raw)
    if len(data) < 253:
        raise ValueError("too few sessions in retrieved feed for 252-day comparison")
    signals, event = audit(data)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "108490_naver_response.xml").write_bytes(raw)
    write_csv(args.out_dir / "108490_naver_daily_2022_2025.csv", data)
    write_csv(args.out_dir / "108490_prior_120day_simultaneous_signals.csv", signals)
    (args.out_dir / "108490_20250514_event.json").write_text(
        json.dumps(event, indent=2, ensure_ascii=False), encoding="utf-8")
    provenance = {
        "source": "Naver Finance historical chart XML, external secondary provider",
        "query_url": URL, "read_at_utc": datetime.now(timezone.utc).isoformat(),
        "sha256_xml": hashlib.sha256(raw).hexdigest(),
        "rows": len(data), "first_date": data[0]["date"],
        "last_date": data[-1]["date"],
        "basis": "same feed OHLCV, may be retrospectively corporate-action adjusted",
        "raw_2025_reported_close": 49000,
        "note": "Reported 49000 may differ from retrospectively adjusted close. Do not blend."
    }
    (args.out_dir / "source_audit.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(event, ensure_ascii=False, indent=2))
    print("Prior 120-session joint-high events:", len(signals))
    print("Saved rows:", len(data), "; XML SHA256:", provenance["sha256_xml"])
if __name__ == "__main__":
    main()
