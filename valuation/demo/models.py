import datetime as dt
from valuation.models import BaseRateChange, RateChange

dollar = BaseRateChange(
    id="102",
    name="دلار",
    rate=[
        RateChange(year=dt.date(2023, 12, 29), f=0.25),
        RateChange(year=dt.date(2024, 12, 29), f=0.25),
        RateChange(year=dt.date(2024, 12, 29), f=0.2),
        RateChange(year=dt.date(2024, 12, 29), f=0.2),
    ]
)
