import unittest
from valuation import algo, models


class TestCostAllocation(unittest.TestCase):

    def setUp(self):
        self.fixed_asset_model = models.FixedAsset(
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
                models.CostAllocation(cost_center_id=10, method="fixed", ratio=0.2),
                models.CostAllocation(cost_center_id=10, method="fixed", ratio=0.8),
            ],
        )
        self.fixed_asset_algo = algo.FixedAsset(self.fixed_asset_model)

    def test_fixed_asset_year1(self):
        fixed_asset1 = self.fixed_asset_algo.fixed_asset
        self.assertEqual(fixed_asset1.book_value, 800)
        self.assertEqual(fixed_asset1.accumulated_depreciation, 300)
        self.assertEqual(fixed_asset1.depreciation, 200)

    def test_fixed_asset_year2(self):
        fixed_asset1 = self.fixed_asset_algo.fixed_asset
        fixed_asset2 = algo.FixedAsset(fixed_asset1).fixed_asset

        self.assertEqual(fixed_asset2.book_value, 600)
        self.assertEqual(fixed_asset2.accumulated_depreciation, 500)
        self.assertEqual(fixed_asset2.depreciation, 200)


