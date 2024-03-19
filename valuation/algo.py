import datetime as dt
from typing import Generator
import numpy as np

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


class Product:
    def __init__(self, param: models.Product, year: dt.date):
        self.param = param
        self.year = year

    def handle_production_limits(self):
        """بیشینه مقدار تولید رو بر مبنایِ ورودی‌های محاسبه می‌کنه"""
        pass

    def improve_f(self):
        """نرخِ بهبودِ تولید رو برمی‌گردونه"""
        if self.param.improve:
            return [i.f for i in self.param.improve if i.year == self.year][0] + 1
        return 1

    def calc_sale_and_end_inv(self) -> list[float]:
        """
        .. raw:: html

            <div dir="rtl">
                مقدارِ موجودیِ پایانِ دوره و فروش/مصرف رو محاسبه می‌کنه
            </div>

        Equation
        InventoryTurnover * EndingInventory - UnitSales = 0
        EndingInventory + UnitSales = GoodsForSales


        Returns
        -------
        list[float, float]
            [0]: موجودیِ پایانِ دوره
            [1]: فروش/مصرف
        """
        goods_for_sales = self.param.inventory.beginning.qty + self.param.production
        a = np.array([[self.param.inventory.norm_ratio.target, -1], [1, 1]])
        b = np.array([0, goods_for_sales])
        x = np.linalg.solve(a, b).tolist()
        return x

    def calc_capacity(self):
        """
        ظرفیتِ تولید رو بر مبنای طرح‌هایِ توسعه محاسبه‌ می‌کنه
        """
        # TODO: بعد از توسعه‌یِ طرح‌هایِ توسعه این بخش تکمیل شه
        return self.param.capacity

    def calc_production(self):
        """
        مقدارِ تولید رو بر مبنایِ نرخِ بهبود و طرح‌هایِ توسعه محاسبه می‌کنه
        """

        # TODO: بعد از توسعه‌یِ طرح‌هایِ توسعه این بخش تکمیل شه
        return self.param.production * self.improve_f()

    def calc_consumption(self):
        """مقدار و مبلغِ مصرفِ از هر نهاده رو برمی‌گردونه"""
        pass

    def new(self):
        pass


class BaseRateChange:
    def __init__(self, param: models.BaseRateChange):
        self.param = param

    @property
    def base_rate_change(self):
        if isinstance(self.param.f, dict):
            return self.param
        return {i: i for i in range(5)}
