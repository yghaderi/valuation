from valuation import models


class FixedAsset:
    def __init__(self, fixed_asset: models.FixedAsset, year: float = 1):
        self.fa = fixed_asset
        self.year = year

    def remain_useful_life(self):
        return

    def depreciation(self):
        match self.fa.depreciation_method:
            case "straight_line":
                depr = (
                               self.fa.book_value
                               + self.fa.accumulated_depreciation
                               - self.fa.salvage_value
                       ) / self.fa.useful_life
                remain_useful_life = self.fa.useful_life - (
                        self.fa.accumulated_depreciation / depr
                )
                if remain_useful_life > 0:
                    return depr * min(self.year, remain_useful_life)
                return 0

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
            },
            deep=True,
        )


class BaseRateChange:
    def __init__(self, param: models.BaseRateChange):
        self.param = param

    @property
    def base_rate_change(self):
        if isinstance(self.param.f, dict):
            return self.param
        return {i: i for i in range(5)}
