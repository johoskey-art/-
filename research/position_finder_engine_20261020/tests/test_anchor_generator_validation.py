import unittest

from src.anchor_generator_validation import audit_rows


class AnchorGeneratorValidationTest(unittest.TestCase):
    def row(self, **changes):
        base = {
            "capture_id": "PF000",
            "ticker": "000000",
            "observed_date": "2026-01-01",
            "source_image": "private.png",
            "axis_scale": "log",
            "top_price": "1000",
            "knee_price": "100",
            "top_anchor_definition": "screen top",
            "knee_anchor_definition": "screen knee",
            "top_uses_future_information": "no",
            "knee_uses_future_information": "no",
            "historical_5_7_state_label": "",
            "price_tick_evidence": "right-axis/cursor",
            "review_status": "reviewed",
        }
        base.update(changes)
        return base

    def test_measured_live_eligible_log_anchors(self):
        result = audit_rows([self.row()])[0]
        self.assertEqual(result["audit_status"], "READY_FOR_PREDECLARED_CANDIDATE_TEST")
        self.assertEqual(result["top_knee_ratio"], "10.0000000000")
        self.assertEqual(result["realtime_eligible"], "yes")

    def test_missing_price_is_not_imputed(self):
        result = audit_rows([self.row(top_price="")])[0]
        self.assertEqual(result["audit_status"], "PENDING_NUMERIC_ANCHORS")
        self.assertEqual(result["top_knee_ratio"], "")

    def test_future_anchor_is_blocked_from_live_use(self):
        result = audit_rows([self.row(top_uses_future_information="yes")])[0]
        self.assertEqual(result["audit_status"], "MEASURED_BUT_NOT_LIVE_ELIGIBLE")
        self.assertEqual(result["realtime_eligible"], "no")


if __name__ == "__main__":
    unittest.main()
