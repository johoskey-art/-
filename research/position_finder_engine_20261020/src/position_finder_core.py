"""Transparent v0 building blocks for the stock-position finder.

This module intentionally keeps two layers separate:
  1) historical 5/7-stage reference distributions; and
  2) screen-observed named-band layout between a supplied knee and top.

It does not claim that either layer is the original blogger formula, and it never
uses a future peak as a runtime input.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


@dataclass(frozen=True)
class ReferenceRange:
    stage: str
    low: float
    median: float
    high: float


@dataclass(frozen=True)
class NamedBandRange:
    band: str
    low: float
    median: float
    high: float
    source: str


def historical_stage_references(
    stage_rows: Iterable[Mapping[str, object]],
    cycle_low: float,
    k: int,
) -> list[ReferenceRange]:
    """Convert a stage-averages CSV subset into price reference ranges.

    Expected keys: k, j, stage_ratio_p25, stage_ratio_median,
    stage_ratio_p75.  Rows may contain other weightings/cohorts, so callers must
    pre-filter to one declared cohort and weighting.
    """
    if cycle_low <= 0:
        raise ValueError("cycle_low must be positive")
    ranges: list[ReferenceRange] = []
    for row in stage_rows:
        if int(float(row["k"])) != k:
            continue
        j = int(float(row["j"]))
        p25 = float(row["stage_ratio_p25"])
        median = float(row["stage_ratio_median"])
        p75 = float(row["stage_ratio_p75"])
        ranges.append(
            ReferenceRange(
                stage=f"grid_{k}_{j}",
                low=cycle_low * p25,
                median=cycle_low * median,
                high=cycle_low * p75,
            )
        )
    if not ranges:
        raise ValueError(f"no rows for k={k}")
    return sorted(ranges, key=lambda item: int(item.stage.rsplit("_", 1)[1]))


def named_layout_ranges(
    knee_price: float,
    top_price: float,
    q_ranges: Mapping[str, tuple[float, float, float]],
    axis_scale: str,
) -> list[NamedBandRange]:
    """Create named price ranges from independently supplied knee/top values.

    q is measured from top (0) to knee (1) in the chart's vertical coordinate.
    The price transformation must match the individually audited source chart:
    ``linear`` interpolates prices, while ``log`` interpolates log-prices.
    Log 5/7 historical reference stages are a separate calculation and do not
    imply that the source chart uses a log price axis.
    """
    if knee_price <= 0 or top_price <= 0:
        raise ValueError("knee_price and top_price must be positive")
    if top_price <= knee_price:
        raise ValueError("top_price must exceed knee_price")

    if axis_scale not in {"linear", "log"}:
        raise ValueError("axis_scale must be 'linear' or 'log'")

    if axis_scale == "log":
        log_top = __import__("math").log(top_price)
        log_knee = __import__("math").log(knee_price)
        transform = lambda q: __import__("math").exp(log_top + q * (log_knee - log_top))
    else:
        transform = lambda q: top_price + q * (knee_price - top_price)

    output: list[NamedBandRange] = []
    for band, (q_low, q_mid, q_high) in q_ranges.items():
        if not (0 <= q_low <= q_mid <= q_high <= 1):
            raise ValueError(f"invalid q range for {band}")
        values = tuple(transform(q) for q in (q_low, q_mid, q_high))
        # Higher q is closer to the lower knee price, hence price order reverses.
        output.append(NamedBandRange(band, min(values), values[1], max(values), f"screen_relative_layout_{axis_scale}"))
    return output


def classify_price(price: float, bands: Iterable[NamedBandRange]) -> str:
    """Return an ordered named position; uncertainty stays explicit in the caller."""
    ordered = sorted(bands, key=lambda item: item.median)
    if not ordered:
        return "unknown"
    if price < ordered[0].median:
        return f"below_{ordered[0].band}"
    for lower, upper in zip(ordered, ordered[1:]):
        if lower.median <= price < upper.median:
            return f"{lower.band}_to_{upper.band}"
    return f"above_{ordered[-1].band}"

