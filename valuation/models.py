from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, PositiveInt, field_validator


class PydanticBaseModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class CostAllocation(PydanticBaseModel):
    cost_center_id: int
    method: Literal["fixed", "variable"]
    ratio: float


class FixedAsset(PydanticBaseModel):
    id: int
    name: str
    book_value: PositiveInt
    useful_life: PositiveInt
    salvage_value: PositiveInt
    accumulated_depreciation: int
    depreciation: int
    maintenance: int
    depreciation_method: Literal[
        "straight_line", "declining_balance", "double_declining_balance"
    ]
    cost_allocation: Optional[list[CostAllocation]] = None

    @field_validator("cost_allocation")
    @classmethod
    def passwords_match(
        cls, v: Optional[list[CostAllocation]]
    ) -> list[CostAllocation] | None:
        if v:
            sum_ratio = sum([i.ratio for i in v])
            if sum_ratio == 1:
                return v
            raise ValueError(f"Sum of 'ratio' should be '1' but is {sum_ratio!r}")
        return v
