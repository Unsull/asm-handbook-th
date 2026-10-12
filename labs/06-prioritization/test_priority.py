import unittest
from priority import calculate


class PriorityTests(unittest.TestCase):
    def test_full_score(self):
        self.assertEqual(calculate(dict.fromkeys(("business", "operational", "data", "dependency", "exposure"), "5")), 5)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            calculate(dict.fromkeys(("business", "operational", "data", "dependency", "exposure"), "9"))
