# Price-axis audit: first disconfirming result

## Finding

All 26 visible position-chart screens have now been reviewed. Twenty-five show
evenly spaced numeric price ticks and are recorded as **LINEAR_VERIFIED**.
PF030 (지니언스) instead has nonuniform tick intervals consistent with price-ratio
spacing and is recorded as **LOG_VERIFIED**. Four screens used for the initial relative-layout prior
(PF001, PF009, PF012, PF018) are included in that set.

This rejects the prior shortcut of treating screen-space `q` values as
log-price distances.

## Consequence for the finder

| Component | Permitted transformation | Not permitted |
|---|---|---|
| Original-chart relative layout | `price = top + q × (knee - top)` only after that chart's axis and independent anchors are audited | applying a log conversion merely because historical stages use logs |
| Historical 5/7 stages | `L × (H/L)^(j/k)` for completed historical cycles | treating it as an original-chart line equation or a live future-peak forecast |

The engine now requires an explicit `axis_scale` (`linear` or `log`) to
convert a chart-layout `q` into a price. `unknown` blocks conversion.

## Scope and remaining uncertainty

- The audit only establishes the rendered **price-axis geometry** of these
  screens. It does not establish the blogger's line-generation formula.
- The `top` and `knee` values in the engine must come from independent
  chart/cycle evidence; they are not inferred from a future high in live use.
- A per-image tick-price calibration is still required before a y-coordinate
  becomes a price. The current converter intentionally leaves all rows blank
  until those two audited tick anchors are entered.
