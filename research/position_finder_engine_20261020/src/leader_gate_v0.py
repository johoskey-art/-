"""Rule-transparent leader eligibility gate for the stock-position finder.

This is not an original blogger formula and it does not predict returns.  It
answers a narrower question: does the available contemporaneous evidence justify
interpreting the named position bands as an active leader-cycle candidate?
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EarningsState = Literal["accelerating", "turnaround", "flat", "deteriorating", "unknown"]
ValuationState = Literal["supported", "stretched", "unknown"]
GateStatus = Literal["confirmed", "candidate", "rejected", "unknown"]


@dataclass(frozen=True)
class GateInput:
    base_breakout: bool | None
    breakout_hold: bool | None
    turnover_expansion: bool | None
    peer_confirmation: bool | None
    earnings_state: EarningsState
    valuation_state: ValuationState
    post_top_risk: bool | None


@dataclass(frozen=True)
class GateOutput:
    status: GateStatus
    evidence_coverage_pct: int
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]


def _known(value: object) -> bool:
    return value is not None and value != "unknown"


def evaluate_leader_gate(input_: GateInput) -> GateOutput:
    """Apply a deliberately conservative, inspectable gate.

    Confirmed requires all of: price-structure evidence, peer confirmation,
    non-deteriorating earnings, and no post-top warning.  Turnarounds may be a
    candidate but are not automatically confirmed by forward EPS alone.
    """
    fields = (
        input_.base_breakout,
        input_.breakout_hold,
        input_.turnover_expansion,
        input_.peer_confirmation,
        input_.earnings_state,
        input_.valuation_state,
        input_.post_top_risk,
    )
    coverage = round(100 * sum(_known(value) for value in fields) / len(fields))
    reasons: list[str] = []
    warnings: list[str] = []

    if input_.post_top_risk is True:
        return GateOutput(
            "rejected",
            coverage,
            ("recent_first_top_or_post_top_risk",),
            ("position_lines_may_be_transitioned; no_new_entry_interpretation",),
        )
    if input_.earnings_state == "deteriorating":
        return GateOutput(
            "rejected",
            coverage,
            ("earnings_revision_deteriorating",),
            ("a_price_breakout_alone_is_not_leader_confirmation",),
        )

    structure_count = sum(value is True for value in (
        input_.base_breakout,
        input_.breakout_hold,
        input_.turnover_expansion,
    ))
    if input_.base_breakout is True:
        reasons.append("base_or_prior_high_breakout")
    if input_.breakout_hold is True:
        reasons.append("breakout_hold_confirmed")
    if input_.turnover_expansion is True:
        reasons.append("turnover_expansion")
    if input_.peer_confirmation is True:
        reasons.append("sector_peer_confirmation")
    if input_.earnings_state == "accelerating":
        reasons.append("earnings_revision_accelerating")
    elif input_.earnings_state == "turnaround":
        reasons.append("earnings_turnaround_candidate")
        warnings.append("turnaround_needs_realization_and_peer_confirmation")
    elif input_.earnings_state in {"flat", "unknown"}:
        warnings.append("earnings_confirmation_incomplete")

    if input_.valuation_state == "stretched":
        warnings.append("valuation_stretched_not_an_automatic_rejection")
    elif input_.valuation_state == "unknown":
        warnings.append("valuation_context_unknown")

    essential_unknown = (
        input_.base_breakout is None
        or input_.peer_confirmation is None
        or input_.earnings_state == "unknown"
        or input_.post_top_risk is None
    )
    if essential_unknown:
        return GateOutput("unknown", coverage, tuple(reasons), tuple(warnings + ["essential_gate_input_missing"]))

    if (
        structure_count >= 2
        and input_.peer_confirmation is True
        and input_.earnings_state == "accelerating"
    ):
        return GateOutput("confirmed", coverage, tuple(reasons), tuple(warnings))

    if structure_count >= 2 and input_.earnings_state in {"accelerating", "turnaround", "flat"}:
        return GateOutput("candidate", coverage, tuple(reasons), tuple(warnings))

    return GateOutput("rejected", coverage, tuple(reasons + ["insufficient_price_structure_evidence"]), tuple(warnings))

