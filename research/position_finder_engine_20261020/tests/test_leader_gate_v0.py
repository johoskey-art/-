from leader_gate_v0 import GateInput, evaluate_leader_gate


def test_confirmed() -> None:
    output = evaluate_leader_gate(
        GateInput(True, True, True, True, "accelerating", "supported", False)
    )
    assert output.status == "confirmed"
    assert output.evidence_coverage_pct == 100


def test_post_top_is_rejected() -> None:
    output = evaluate_leader_gate(
        GateInput(True, True, True, True, "accelerating", "supported", True)
    )
    assert output.status == "rejected"


def test_missing_essential_evidence_is_unknown() -> None:
    output = evaluate_leader_gate(
        GateInput(True, None, True, None, "unknown", "unknown", None)
    )
    assert output.status == "unknown"


if __name__ == "__main__":
    test_confirmed()
    test_post_top_is_rejected()
    test_missing_essential_evidence_is_unknown()
    print("PASS")

