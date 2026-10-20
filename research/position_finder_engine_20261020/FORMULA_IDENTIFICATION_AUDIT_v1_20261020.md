# Formula identification audit v1 — what the original screenshots do and do not identify

## Scope

This audit uses all seven original-screen rows in
`research/results/original_5_companies_7_charts_commonalities_20261020.csv`.
The source owner has confirmed that these original charts use log-price axes;
an older per-row axis label is retained in the legacy file but is not used to
exclude its q geometry.  On such a chart, a screen coordinate (q), measured from
the upper top line (T(t)) at 0 to the lower knee line (K(t)) at 1, converts
to price as:

[
B(q,t)=T(t)\left(\frac{K(t)}{T(t)}\right)^q
      =T(t)^{1-q}K(t)^q.
]

This is now the **identified coordinate transformation**.  It is not yet the
unpublished algorithm that generates (T(t)), (K(t)), or the q values.

## Reproducible q test

| Quantity | Shoulder | Waist | Thigh |
|---|---:|---:|---:|
| Observed seven-screen mean q | 0.218693 | 0.415653 | 0.715304 |
| Observed range | 0.206089–0.237198 | 0.378450–0.437572 | 0.704169–0.723276 |

Predeclared candidates were scored against all 21 observed band coordinates.

| Candidate q (shoulder, waist, thigh) | MAE | RMSE | Result |
|---|---:|---:|---|
| (1/5, 2/5, 5/7) | 0.014981 | 0.018421 | compatible at screenshot precision |
| (1/5, 3/7, 5/7) | 0.012875 | 0.017700 | compatible at screenshot precision |
| Standard Fibonacci (0.236, 0.382, 0.618) | 0.049886 | 0.061429 | materially worse |
| Sample mean (descriptive only) | 0.007941 | 0.011868 | fit benchmark; not a formula |

The full machine-readable score file is
`results/original_log_q_formula_candidate_scores_v1_20261020.json`; the
reproducer is `scripts/screen_q_candidate_test.py`.

## What is ruled out, and what is not

- The usual three fixed Fibonacci retracement positions
  (0.236,0.382,0.618) are a poor direct explanation of the three observed
  internal lines.
- The two rational candidates are too close relative to screenshot/line-center
  error to choose between them.  Declaring either one the blogger's rule would
  be overfitting.
- The evidence supports a stable **geometric interpolation layout** while the
  displayed top-to-knee span itself changes materially across time.  Therefore
  the next unknown is the dynamic anchor generator (T(t),K(t)), not another
  arbitrary fixed multiplier.
- The blog sentence about a Fibonacci n-th function remains unidentifiable:
  it may generate anchors, state transitions, or a later transformation.  The
  q comparison alone cannot assign n.

## Formula status

[
\boxed{B_b(t)=T(t)^{1-q_b}K(t)^{q_b}}
]

is the current reproducible observation model for a **given chart state**.
The following remain explicitly unknown: (q_b) exact rational assignment,
(T(t)), (K(t)), the state-transition rule, and the original Fibonacci
function.  They must be tested against same-date original band prices, not
selected by minimum error.


## 5/7-stage interpretation of the two surviving rational candidates

Write (G(t)=T(t)/K(t)>1), so that the price position from the knee is
(K(t)G(t)^f).  Because this audit measures q from top down, (f=1-q).

The first candidate therefore has a concrete, predeclared mixed-stage form:

| Band | q from top | f from knee | Candidate price |
|---|---:|---:|---|
| knee | 1 | 0 | (K) |
| thigh | 5/7 | 2/7 | (K G^{2/7}) |
| waist | 2/5 | 3/5 | (K G^{3/5}) |
| shoulder | 1/5 | 4/5 | (K G^{4/5}) |
| top | 0 | 1 | (K G) |

The near-tied alternative replaces the waist by (f=4/7)
((q=3/7)).  Thus the current screenshots narrow the problem to a small
family of **mixed 5/7 log-stage layouts**; they do not select one member.

This is the first meaningful connection between the blog's stated 5/7
procedure and the observed line geometry.  It remains a *candidate* because
the mean absolute-error gap between the two layouts is only 0.001337 in q,
well below the uncertainty introduced by screenshots and line-center
measurement.

## What must be identified to turn this into the generator

A complete active formula needs a rule for the two dynamic anchors:

[
K(t), qquad G(t)=T(t)/K(t).
]

Once those are known, every candidate band above is determined without a
future realized high.  The screenshot evidence does not yet identify those
two functions, nor does it identify whether the blogger's Fibonacci
n-th-function produces (K), (G), a state switch, or something upstream of
all three.  Fitting an arbitrary time trend to (K,G) would only disguise
that missing evidence.
