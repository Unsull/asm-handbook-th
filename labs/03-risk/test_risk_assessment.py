import unittest
from risk_assessment import Risk, annualized_loss


class RiskTests(unittest.TestCase):
    def test_score_and_tiers(self):
        self.assertEqual(Risk("x", 4, 5).tier, "critical")
        self.assertEqual(Risk("y", 2, 2).tier, "low")

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            Risk("x", 0, 4)

    def test_ale(self):
        self.assertEqual(annualized_loss(180_000, 0.4), 72_000)
