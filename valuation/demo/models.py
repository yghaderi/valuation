import datetime as dt
from valuation.models import BaseRateChange, RateChange, FinancialYear, Firm, BaseParam, CostCenter


def demo():
    base_rate_change = BaseRateChange(
        id="102",
        name="دلار",
        rate=[
            RateChange(year=dt.date(2023, 12, 29), f=0.25),
            RateChange(year=dt.date(2024, 12, 29), f=0.25),
            RateChange(year=dt.date(2024, 12, 29), f=0.2),
            RateChange(year=dt.date(2024, 12, 29), f=0.2),
        ],
    )
    financial_year = FinancialYear(
        date=dt.date(2023, 12, 29),
        length=5
    )

    base_param = BaseParam(
        financial_year=financial_year,
        base_rate_change=base_rate_change
    )
    cost_center0 = CostCenter(
        id="10",
        name="تولیدِ اوره",
        category="product",
        input=[],
        output=[],
    )
    firm = Firm(
        id="10",
        name="شپدیس",
        base_param=base_param,
        category="production",
        cost_centers=[cost_center0]
    )
