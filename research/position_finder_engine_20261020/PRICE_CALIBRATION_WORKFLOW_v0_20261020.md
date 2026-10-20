# Log-chart price calibration workflow

The source owner confirmed that the original position charts are **log-price
charts**. The previous visual classification based on apparent tick spacing was
wrong and is retained only as a documented failed inference.

The screen extractor stores line positions in `y_px`; it must not invent tick
prices. For each chart, record two visible right-axis tick anchors in
`results/chart_axis_calibration_pending_v0_20261020.csv`, then change
`calibration_status` to `READY`.

Run:

```powershell
python scripts/chart_axis_price_convert.py `
  --observations results/chart_band_observations_auto_draft_20261020.csv `
  --calibrations results/chart_axis_calibration_pending_v0_20261020.csv `
  --output results/chart_band_price_observations_draft_20261020.csv
```

For a log chart the converter uses log-price interpolation between the two
reviewed ticks. It leaves every uncalibrated row blank. It does not derive the
blogger's formula or use a future high as a runtime input.
