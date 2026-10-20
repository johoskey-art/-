"""Convert extracted line pixels with an explicitly audited price-axis scale."""

from __future__ import annotations

import math


def axis_price(
    y_px: float,
    y1_px: float,
    price1: float,
    y2_px: float,
    price2: float,
    axis_scale: str,
) -> float:
    """Map y to price from two visible tick anchors without guessing either tick."""
    if y1_px == y2_px:
        raise ValueError("axis calibration y positions must differ")
    if price1 <= 0 or price2 <= 0:
        raise ValueError("price tick anchors must be positive")
    q = (y_px - y1_px) / (y2_px - y1_px)
    if axis_scale == "linear":
        return price1 + q * (price2 - price1)
    if axis_scale == "log":
        return math.exp(math.log(price1) + q * (math.log(price2) - math.log(price1)))
    raise ValueError("axis_scale must be 'linear' or 'log'")
