import unittest
from edge_integrity import sample


class EdgeIntegrityTests(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(sample(), ['INTEGRITY_MISMATCH', 'ACCEPTED_FOR_FURTHER_VALIDATION', 'REPLAY'])
