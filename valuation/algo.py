import datetime as dt
from typing import Generator
from valuation import models


class FinancialYear:
    def __init__(self, param: models.FinancialYear):
        self.param = param

    def generate(self):
        date = self.param.date
        new_param = self.param.model_copy(
            update={"date": date.replace(year=date.year + 1)}
        )
        self.param = new_param
        yield new_param


class FixedAsset:
    def __init__(self, param: models.FixedAsset, year: float = 1):
        self.param = param
        self.year = year

    def remain_useful_life(self):
        return

    def depreciation(self) -> float:
        match self.param.depreciation_method:
            case "straight_line":
                depr = (
                    self.param.book_value
                    + self.param.accumulated_depreciation
                    - self.param.salvage_value
                ) / self.param.useful_life
                remain_useful_life = self.param.useful_life - (
                    self.param.accumulated_depreciation / depr
                )
                if remain_useful_life > 0:
                    return depr * min(self.year, remain_useful_life)
                return 0.0

    def book_value(self) -> float:
        return self.param.book_value - self.depreciation()

    def accumulated_depreciation(self) -> float:
        return self.param.accumulated_depreciation + self.depreciation()

    def generate(self) -> Generator[models.FixedAsset, None, None]:
        new_param = self.param.model_copy(
            update={
                "depreciation": self.depreciation(),
                "book_value": self.book_value(),
                "accumulated_depreciation": self.accumulated_depreciation(),
            },
            deep=True,
        )
        self.param = new_param
        yield new_param


class BaseRateChange:
    def __init__(self, param: models.BaseRateChange):
        self.param = param

    @property
    def base_rate_change(self):
        if isinstance(self.param.f, dict):
            return self.param
        return {i: i for i in range(5)}
