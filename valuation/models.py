from typing import Literal, Optional
import datetime as dt
from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator


# class BaseModel(BaseModel):
#     model_config = ConfigDict(frozen=True)


class CostingMethod(BaseModel):
    method: Literal["variable", "absorption"]


class CostAllocation(BaseModel):
    method: Literal["fixed", "variable"]
    ratio: float


class FixedAsset(BaseModel):
    id: str
    name: str
    book_value: PositiveInt
    useful_life: PositiveInt
    salvage_value: PositiveInt
    accumulated_depreciation: int
    depreciation: int
    depreciation_method: Literal[
        "straight_line", "declining_balance", "double_declining_balance"
    ]
    cost_allocation: Optional[list[CostAllocation]] = None

    @field_validator("cost_allocation")
    @classmethod
    def cost_allocation_ratio(
        cls, v: Optional[list[CostAllocation]]
    ) -> list[CostAllocation] | None:
        if v:
            sum_ratio = sum([i.ratio for i in v])
            if sum_ratio == 1:
                return v
            raise ValueError(f"Sum of 'ratio' should be '1' but is {sum_ratio!r}")
        return v


class BaseRateChange(BaseModel):
    id: str
    f: dict | float


class Rate(BaseModel):
    id: str
    rate: int
    extra_change: Optional[dict] = None


class NormFinancialRatio(BaseModel):
    current: float
    target: float
    begin_improvement_year: int
    mature_year: int


class Inventory(BaseModel):
    qty: float
    management_approach: int
    norm_ratio: NormFinancialRatio


class RawMaterial(BaseModel):
    id: str
    name: str
    unit: int
    rate: Rate
    inventory: Inventory
    cost_allocation: int


class FinancialYear(BaseModel):
    date: dt.date
    length: PositiveInt


class Input(BaseModel):
    fixed_asses: Optional[list[FixedAsset]] = []


class Output(BaseModel):
    pass


class CostCenter(BaseModel):
    id: str
    name: str
    category: Literal["product", "service", "operational"]
    input: Optional[Input] = []
    output: Optional[Output] = []


class Valuation(BaseModel):
    id: str
    name: str
    financial_year: FinancialYear
    category: Literal["production"]
    cost_centers: list[CostCenter]


class GenFixedAsset(FixedAsset):
    year: int = 0


class GenInput(BaseModel):
    fixed_asses: Optional[list[list[GenFixedAsset]]] = []


class GenCostCenter(BaseModel):
    id: str
    inputs: Optional[GenInput] = []


class GenValuation(BaseModel):
    cost_centers: list[GenCostCenter] = []


########################################################################################################
# Financial Statements
#######################################################################################################
class BalanceSheet(BaseModel):
    fy: dt.date
    fixed_asset: int
