from typing import Generator
from valuation import models


class FixedAsset:
    def __init__(self, param: models.FixedAsset, year: float = 1):
        self._param = param
        self.year = year

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, param: models.FixedAsset):
        self._param = param

    def remain_useful_life(self):
        return

    def depreciation(self) -> float:
        match self._param.depreciation_method:
            case "straight_line":
                depr = (
                               self._param.book_value
                               + self._param.accumulated_depreciation
                               - self._param.salvage_value
                       ) / self._param.useful_life
                remain_useful_life = self._param.useful_life - (
                        self._param.accumulated_depreciation / depr
                )
                if remain_useful_life > 0:
                    return depr * min(self.year, remain_useful_life)
                return 0.

    def book_value(self) -> float:
        return self._param.book_value - self.depreciation()

    def accumulated_depreciation(self) -> float:
        return self._param.accumulated_depreciation + self.depreciation()

    def generate(self) -> Generator[models.FixedAsset, None, None]:
        new_param = self._param.model_copy(
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
