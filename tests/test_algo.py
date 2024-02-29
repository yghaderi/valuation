import unittest
from valuation.algo import FixedAsset


class TestCostAllocation(unittest.TestCase):

    def setUp(self):
        self.ca = FixedAsset(cost_center_id=10, method="fixed", ratio=0.2)

    def test_simple_construct(self):
        self.assertEqual(self.ca.cost_center_id, 10)
        self.assertEqual(self.ca.method, "fixed")
        self.assertEqual(self.ca.ratio, 0.2)
        self.assertEqual(
            self.ca.model_dump(),
            {"cost_center_id": 10, "method": "fixed", "ratio": 0.2},
        )
