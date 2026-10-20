# METHODOLOGY

This is a new research version. The old 38 stay as LEGACY_SELECTED_SAMPLE and are not called the full Korean leader population.

## Inclusion before returns
A company-cycle needs at least two pre-peak evidence classes: industry representation/relative strength; turnover/volume; persistent breakout; earnings-led versus theme-led character; peer leader role. Final return and any position-band touch are never entry conditions.

## Cycle and price rules
L is minimum adjusted close in a documented start window; H is maximum adjusted close after L and before a fixed end window. Intraday values are stored separately and never substituted. Ongoing cycles are RIGHT_CENSORED and excluded.

## Formula
P(j,k)=L*(H/L)^(j/k), k in {5,7}. Report same-stage means, medians, quartiles, adjacent step means, cycle-equal and company-equal weights. Do not exponentiate adjacent mean and call it a stage mean.

## Price QA
KRX daily data and corporate-action records are preferred. This run uses immutable external Yahoo adjusted-close snapshots and labels new rows PROVISIONAL_EXTERNAL_ADJCLOSE_PENDING_KRX.

## Boundary
Realized H is not blogger top line T(t) or super-top U(t). No Fibonacci formula is inferred.