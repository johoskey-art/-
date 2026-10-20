# Price-axis correction — source owner confirmation

## Corrected fact

The source owner confirmed that **all original position-chart screenshots use a
log-price axis**. The earlier classification of 25 linear and one log chart was
based only on apparent rendered tick spacing and was wrong. That inference is
retained in the work log as a failed QA step, but it is superseded by this
source-setting confirmation.

The authoritative status of all 26 screenshots is therefore
`LOG_USER_CONFIRMED`.

## Consequence for the finder

For an original-chart screen, with independently audited price anchors
(top, knee) and screen coordinate (q) from top (=0) to knee (=1):

[
P(q) = top 	imes (knee/top)^q
]

This is a coordinate conversion, not a discovery of the blogger's line
formula. It only converts a line already observed on a log chart into a price.

| Component | Valid use | Still not established |
|---|---|---|
| Screen-layout q | log-price conversion after two actual axis ticks are audited | why the original algorithm chose that q |
| Historical 5/7 stages | completed-cycle distribution and calibration | a live future high or the original formula |
| Named bands | compare multiple observed charts after time/axis calibration | fixed universal band constants |

## Required remaining evidence

Each screenshot still needs two reviewed right-axis tick values before any
pixel y-coordinate becomes a price. The converter leaves values blank until
that calibration is present.
