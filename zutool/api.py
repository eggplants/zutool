from __future__ import annotations

from typing import TypeVar

import requests
from pydantic import BaseModel, ValidationError

from .models import (
    ErrorResponse,
    GetPainStatusResponse,
    GetWeatherPointResponse,
    GetWeatherStatusResponse,
)

BASE_URL = "https://zutool.jp/api"
TIMEOUT = 10
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

_TModel = TypeVar("_TModel", bound=BaseModel)


def __get(path: str, param: str, model: type[_TModel]) -> _TModel:
    res = requests.get(f"{BASE_URL}{path}/{param}", timeout=TIMEOUT, headers={"User-Agent": UA})
    if res.status_code == requests.codes.ok:
        try:
            return model.model_validate_json(res.text)
        except ValidationError as e:
            err_res = ErrorResponse.model_validate_json(res.text)
            raise ValueError(err_res) from e
    raise ValueError(res.status_code, res.text)


def get_pain_status(area_code: str) -> GetPainStatusResponse:
    return __get("/getpainstatus", area_code, GetPainStatusResponse)


def get_weather_point(keyword: str) -> GetWeatherPointResponse:
    return __get("/getweatherpoint", keyword, GetWeatherPointResponse)


def get_weather_status(city_code: str) -> GetWeatherStatusResponse:
    return __get("/getweatherstatus", city_code, GetWeatherStatusResponse)
