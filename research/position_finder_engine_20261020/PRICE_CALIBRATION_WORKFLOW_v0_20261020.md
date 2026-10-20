# Linear price calibration workflow

The screen extractor stores line positions in `y_px`; it must not invent the
price value from an image. For each audited linear chart, record two visible
right-axis labels in `chart_axis_calibration_pending_v0_20261020.csv`:

1. `tick1_y_px`, `tick1_price`
2. `tick2_y_px`, `tick2_price`
3. Change `calibration_status` to `READY` only after a reviewer checks both.

Then run:

```powershell
python scripts/linear_axis_price_convert.py `
  --observations results/chart_band_observations_auto_draft_20261020.csv `
  --calibrations results/chart_axis_calibration_pending_v0_20261020.csv `
  --output results/chart_band_price_observations_draft_20261020.csv
```

The converter applies only linear interpolation. It leaves rows blank with
`PENDING_CALIBRATION` rather than filling a made-up price. A future log-axis
screen must be separately audited and needs a dedicated log converter.
