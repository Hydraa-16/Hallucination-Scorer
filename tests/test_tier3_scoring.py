
import unittest

from middleware.tier3.scoring import calculate_trust_score


class TestCalculateTrustScore(unittest.TestCase):

    def test_zero_risk_gives_full_trust(self):
        self.assertEqual(calculate_trust_score(0.0, 0.0), 1.0)

    def test_maximum_risk_gives_zero_trust(self):
        self.assertEqual(calculate_trust_score(1.0, 1.0), 0.0)

    def test_weighted_average(self):
        # Risk = (0.60 * 0.50) + (0.40 * 0.25) = 0.40
        # Trust = 1.00 - 0.40 = 0.60
        self.assertEqual(calculate_trust_score(0.50, 0.25), 0.60)

    def test_integer_inputs_are_accepted(self):
        self.assertEqual(calculate_trust_score(0, 0), 1.0)

    def test_risk_outside_range_is_rejected(self):
        for value in (-0.1, 1.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    calculate_trust_score(value, 0.5)

                with self.assertRaises(ValueError):
                    calculate_trust_score(0.5, value)

    def test_non_finite_values_are_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    calculate_trust_score(value, 0.5)

    def test_missing_or_non_numeric_values_are_rejected(self):
        for value in (None, "0.5", True):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    calculate_trust_score(value, 0.5)

    def test_missing_second_score_is_rejected(self):
        with self.assertRaises(TypeError):
            calculate_trust_score(0.5, None)


if __name__ == "__main__":
    unittest.main()
