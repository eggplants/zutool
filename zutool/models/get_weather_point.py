from __future__ import annotations

from pydantic import BaseModel, Field, RootModel, field_validator


class _WeatherPoint(BaseModel):
    city_code: str = Field(pattern="^\\d{5}$")
    name_kata: str = Field(pattern="^[\uFF61-\uFF9F]+$")
    name: str


class _WeatherPoints(RootModel[list[_WeatherPoint]]):
    root: list[_WeatherPoint]


# https://zutool.jp/api/getweatherpoint/:keyword
class GetWeatherPointResponse(BaseModel):
    result: _WeatherPoints

    @field_validator("result", mode="before")
    def validate_result(cls, v: str) -> _WeatherPoints:
        return _WeatherPoints.model_validate_json(bytes(v, "utf-8").decode("unicode_escape"))
