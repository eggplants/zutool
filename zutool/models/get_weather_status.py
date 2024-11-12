from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field, field_validator

from .enum import AreaEnum, PressureLevelEnum, WeatherEnum

_JTC = timezone(timedelta(hours=9))


class _WeatherStatusByTime(BaseModel):
    time: int = Field(ge=0, le=24)
    weather: WeatherEnum
    temp: float | None
    pressure: float
    pressure_level: PressureLevelEnum

    @field_validator("weather", mode="before")
    def validate_weather(cls, v: str) -> WeatherEnum:
        try:
            return WeatherEnum(v)
        except KeyError as e:
            msg = f"Error validating weather {e}. Valid ones are: {[w.name for w in WeatherEnum]}"
            raise ValueError(msg) from e

    @field_validator("temp", mode="before")
    def validate_temp(cls, v: str) -> float | None:
        return None if v == "#" else float(v)

    @field_validator("pressure_level", mode="before")
    def validate_pressure_level(cls, v: str) -> PressureLevelEnum:
        try:
            return PressureLevelEnum(v)
        except KeyError as e:
            msg = f"Error validating pressure_level {e}. Valid ones are: {[p.name for p in PressureLevelEnum]}"
            raise ValueError(msg) from e


# https://zutool.jp/api/getweatherstatus/:city_code
class GetWeatherStatusResponse(BaseModel):
    place_name: str
    place_id: str = Field(pattern=r"^\d{3}$")
    prefectures_id: AreaEnum
    date_time: datetime = Field(alias="dateTime")
    yesterday: list[_WeatherStatusByTime]
    today: list[_WeatherStatusByTime]
    tomorrow: list[_WeatherStatusByTime] = Field(validation_alias="tommorow")
    dayaftertomorrow: list[_WeatherStatusByTime]

    @field_validator("prefectures_id", mode="before")
    def validate_prefectures_id(cls, v: str) -> AreaEnum:
        try:
            return AreaEnum(v)
        except KeyError as e:
            msg = f"Error validating prefectures_id {e}. Valid ones are: {[a.name for a in AreaEnum]}"
            raise ValueError(msg) from e

    @field_validator("date_time", mode="before")
    def validate_date_time(cls, v: str) -> datetime:
        return datetime.strptime(v, "%Y-%m-%d %H").replace(tzinfo=_JTC)
