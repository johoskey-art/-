# Formula identification audit v2 — within-screen anchor test

## Direct same-chart test: Samsung Electro-Mechanics

Source: `research/results/sem_009150_20261014_five_band_pixels_v1.csv`,
21 horizontal observations from one original position-chart screenshot.

| Quantity | n | mean q | min–max | standard deviation |
|---|---:|---:|---:|---:|
| shoulder | 21 | 0.212569 | 0.193878–0.230769 | 0.009370 |
| waist | 17 | 0.416206 | 0.405941–0.432099 | 0.007640 |
| thigh | 21 | 0.717255 | 0.708861–0.728395 | 0.004170 |

Over the same 21 x-positions, the measured top-to-knee screen span expands
from 78 to 103 pixels: **+32.05%**.

## Result

The internal bands retain nearly fixed normalized log positions while the
outer top-to-knee span changes materially. This falsifies a fixed absolute
price-line interpretation and supports the minimal two-anchor layout:

[
\log B_b(t)=(1-q_b)\log T(t)+q_b\log K(t).
]

Equivalently:

[
B_b(t)=T(t)^{1-q_b}K(t)^{q_b}.
]

The evidence is strongest for this **state-space geometry**:

- five displayed lines have two moving degrees of freedom, (T(t)) and
  (K(t));
- shoulder, waist and thigh use approximately stable q positions between them;
- the q observations remain compatible with both mixed 5/7 candidates already
  registered in `results/mixed_5_7_layout_candidate_registry_v1_20261020.csv`.

## Identification boundary

This result still does **not** identify the generator for (T(t)) or (K(t)).
For any observed pair of anchor paths, infinitely many hidden Fibonacci/state
functions can produce the same two paths.  The existing screenshots contain
the output geometry, not a labelled mapping from 5/7 historic records to the
two anchors.

Therefore the next valid formula test is not another fraction search. It is to
recover same-date numerical (T(t)) and (K(t)) at several dates for
SK하이닉스 and SK텔레콤, then test whether their log-ratio
(log(T/K)) is explained by a predeclared 5/7 historical-stage statistic.
Until that mapping is measured, an anchor-generator equation would be invented
rather than reverse-engineered.
