from __future__ import annotations

from pydantic import BaseModel, Field, PositiveFloat, field_validator

from .enum import AreaEnum


class _GetPainStatus(BaseModel):
    area_name: AreaEnum
    time_start: int
    time_end: int
    rate_normal: PositiveFloat = Field(alias="普通", validation_alias="rate_0")
    rate_little: PositiveFloat = Field(alias="少し痛い", validation_alias="rate_1")
    rate_painful: PositiveFloat = Field(alias="痛い", validation_alias="rate_2")
    rate_bad: PositiveFloat = Field(alias="かなり痛い", validation_alias="rate_3")

    @field_validator("area_name", mode="before")
    def validate_area_name(cls, v: str) -> AreaEnum:
        try:
            return AreaEnum[v]
        except KeyError as e:
            msg = f"Error validating area_name {e}. Valid ones are: {[a.name for a in AreaEnum]}"
            raise ValueError(msg) from e


# https://zutool.jp/api/getpainstatus/:prefecture_id
class GetPainStatusResponse(BaseModel):
    painnoterate_status: _GetPainStatus
