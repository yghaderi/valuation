import unittest
from valuation import algo, models


class TestFixedAsset(unittest.TestCase):

    def setUp(self):
        # straight_line
        fa_straight_line_model = models.FixedAsset(
            id=1,
            name="car",
            book_value=1_000,
            useful_life=2,
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
        fixed_asset_algo = algo.FixedAsset(fa_straight_line_model)
        self.fixed_asset1 = fixed_asset_algo.fixed_asset
        self.fixed_asset2 = algo.FixedAsset(self.fixed_asset1).fixed_asset
        self.fixed_asset3 = algo.FixedAsset(self.fixed_asset2).fixed_asset

    def test_straight_line_methode_year1(self):
        self.assertEqual(self.fixed_asset1 .book_value, 500)
        self.assertEqual(self.fixed_asset1 .accumulated_depreciation, 600)
        self.assertEqual(self.fixed_asset1 .depreciation, 500)

    def test_straight_line_methode_year2(self):
        self.assertEqual(self.fixed_asset2 .book_value, 100)
        self.assertEqual(self.fixed_asset2 .accumulated_depreciation, 1000)
        self.assertEqual(self.fixed_asset2 .depreciation, 400)

    def test_straight_line_methode_year3(self):
        self.assertEqual(self.fixed_asset3 .book_value, 100)
        self.assertEqual(self.fixed_asset3 .accumulated_depreciation, 1000)
        self.assertEqual(self.fixed_asset3 .depreciation, 0)


