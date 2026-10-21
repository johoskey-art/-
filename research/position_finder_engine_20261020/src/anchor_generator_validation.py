"""Audit dynamic top/knee anchors without inventing a source formula.

Input values must be measured from the original chart's same-date price axis or
a documented chart cursor.  This module deliberately does not infer a missing
anchor, choose a Fibonacci stage, or use a future high as a live input.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

REQUIRED_COLUMNS = {
    "capture_id",
    "ticker",
    "observed_date",
    "source_image",
    "axis_scale",
    "top_price",
    "knee_price",
    "top_anchor_definition",
    "knee_anchor_definition",
    "top_uses_future_information",
    "knee_uses_future_information",
    "historical_5_7_state_label",
    "price_tick_evidence",
    "review_status",
}


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def audit_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return auditable derived spans; never impute absent prices."""
    if not rows:
        return []
    absent = REQUIRED_COLUMNS - set(rows[0])
    if absent:
        raise ValueError(f"missing required columns: {', '.join(sorted(absent))}")

    audited: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        try:
            top = float(row["top_price"])
            knee = float(row["knee_price"])
        except (TypeError, ValueError):
            item.update(
                audit_status="PENDING_NUMERIC_ANCHORS",
                top_knee_ratio="",
                log_top_knee_span="",
                realtime_eligible="no",
            )
            audited.append(item)
            continue

        if top <= knee or knee <= 0:
            item.update(
                audit_status="INVALID_ANCHOR_ORDER",
                top_knee_ratio="",
                log_top_knee_span="",
                realtime_eligible="no",
            )
            audited.append(item)
            continue

        uses_future = _as_bool(row["top_uses_future_information"]) or _as_bool(
            row["knee_uses_future_information"]
        )
        has_evidence = bool(row["price_tick_evidence"].strip())
        is_log_axis = row["axis_scale"].strip().lower() == "log"
        item.update(
            audit_status=(
                "READY_FOR_PREDECLARED_CANDIDATE_TEST"
                if has_evidence and is_log_axis and not uses_future
                else "MEASURED_BUT_NOT_LIVE_ELIGIBLE"
            ),
            top_knee_ratio=f"{top / knee:.10f}",
            log_top_knee_span=f"{math.log(top / knee):.10f}",
            realtime_eligible="yes" if has_evidence and is_log_axis and not uses_future else "no",
        )
        audited.append(item)
    return audited


def run(input_path: Path, output_path: Path) -> None:
    with input_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    audited = audit_rows(rows)
    fieldnames = list(rows[0].keys()) + [
        "audit_status",
        "top_knee_ratio",
        "log_top_knee_span",
        "realtime_eligible",
    ] if rows else sorted(REQUIRED_COLUMNS)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(audited)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    run(args.input_csv, args.output_csv)
