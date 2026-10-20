"""Small candidate family implied by measured 5/7-style log layouts.

These functions are research candidates, not a claim about the original
blogger's unpublished formula.  They require independently supplied dynamic
knee and top anchors.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pow


@dataclass(frozen=True)
class MixedStageCandidate:
    candidate_id: str
    thigh_from_knee: float
    waist_from_knee: float
    shoulder_from_knee: float


CANDIDATES = {
    "MIXED_5_7_A": MixedStageCandidate("MIXED_5_7_A", 2 / 7, 3 / 5, 4 / 5),
    "MIXED_5_7_B": MixedStageCandidate("MIXED_5_7_B", 2 / 7, 4 / 7, 4 / 5),
}


def bands_from_anchors(knee: float, top: float, candidate_id: str) -> dict[str, float]:
    """Return log-price bands given independently audited anchors."""
    if knee <= 0 or top <= knee:
        raise ValueError("top must exceed positive knee")
    candidate = CANDIDATES[candidate_id]
    growth = top / knee
    return {
        "knee": knee,
        "thigh": knee * pow(growth, candidate.thigh_from_knee),
        "waist": knee * pow(growth, candidate.waist_from_knee),
        "shoulder": knee * pow(growth, candidate.shoulder_from_knee),
        "top": top,
    }
