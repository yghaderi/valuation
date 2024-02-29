import unittest
from valuation.models import CostAllocation, FixedAsset


class TestCostAllocation(unittest.TestCase):

    def setUp(self):
        self.base_instance = CostAllocation(
            cost_center_id=10, method="fixed", ratio=0.2
        )

    def test_simple_construct(self):
        self.assertEqual(self.base_instance.cost_center_id, 10)
        self.assertEqual(self.base_instance.method, "fixed")
        self.assertEqual(self.base_instance.ratio, 0.2)
        self.assertEqual(
            self.base_instance.model_dump(),
            {"cost_center_id": 10, "method": "fixed", "ratio": 0.2},
        )


class TestFixedAsset(unittest.TestCase):

    def setUp(self):
        self.base_instance = FixedAsset(
            id=1,
            name="car",
            book_value=1_000,
            useful_life=5,
            salvage_value=100,
            accumulated_depreciation=100,
            depreciation=0,
            maintenance=0,
            depreciation_method="straight_line",
            cost_allocation=[
                CostAllocation(cost_center_id=10, method="fixed", ratio=0.2),
                CostAllocation(cost_center_id=10, method="fixed", ratio=0.8),
            ],
        )

    def test_simple_construct(self):
        self.assertEqual(self.base_instance.id, 1)
        self.assertEqual(self.base_instance.name, "car")
        self.assertEqual(self.base_instance.book_value, 1_000)
        self.assertEqual(self.base_instance.useful_life, 5)
        self.assertEqual(self.base_instance.salvage_value, 100)
        self.assertEqual(self.base_instance.accumulated_depreciation, 100)
        self.assertEqual(self.base_instance.depreciation, 0)
        self.assertEqual(self.base_instance.maintenance, 0)
        self.assertEqual(self.base_instance.depreciation_method, "straight_line")
        self.assertEqual(
            self.base_instance.cost_allocation,
            [
                CostAllocation(cost_center_id=10, method="fixed", ratio=0.2),
                CostAllocation(cost_center_id=5, method="fixed", ratio=0.8),
            ],
        )


if __name__ == "__main__":
    unittest.main()
