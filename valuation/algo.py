from valuation import models


class FixedAsset:
    def __init__(self, fixed_asset: models.FixedAsset):
        self.fa = fixed_asset

    def depreciation(self):
        match self.fa.depreciation_method:
            case "straight_line":
                return (
                    self.fa.book_value
                    + self.fa.accumulated_depreciation
                    - self.fa.salvage_value
                ) / self.fa.useful_life

    def book_value(self):
        return self.fa.book_value - self.depreciation()

    def accumulated_depreciation(self):
        return self.fa.accumulated_depreciation + self.depreciation()

    @property
    def fixed_asset(self):
        return self.fa.model_copy(
            update={
                "depreciation": self.depreciation(),
                "book_value": self.book_value(),
                "accumulated_depreciation": self.accumulated_depreciation(),
            }
        )
