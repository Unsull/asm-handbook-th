import unittest
from pathlib import Path
from inventory_report import analyze


class InventoryTests(unittest.TestCase):
    def test_sample(self):
        n, missing, coverage = analyze(Path(__file__).with_name("asset_inventory.csv"))
        self.assertEqual(n, 4)
        self.assertEqual(missing, ["OPS-01"])
        self.assertEqual(coverage, 75)
