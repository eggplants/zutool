from __future__ import annotations

from typing import TypeVar

import requests
from pydantic import BaseModel, ValidationError

from .models import (
    ErrorResponse,
    GetOtenkiASPResponse,
    GetPainStatusResponse,
    GetWeatherPointResponse,
    GetWeatherStatusResponse,
    SetWeatherPointResponse,
)
from .models.get_otenki_asp import _GetOtenkiASPRawResponse

BASE_URL = "https://zutool.jp/api"
TIMEOUT = 10
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

CONFIRMED_OTENKI_ASP_CITY_CODES = [
    "01101",
    "04101",
    "13101",
    "15103",
    "17201",
    "23106",
    "27128",
    "34101",
    "39201",
    "40133",
    "47201",
]

_TModel = TypeVar("_TModel", bound=BaseModel)


def __get(path: str, param: str, model: type[_TModel], *, set_weather_point: str | None = None) -> _TModel:
    ses = requests.Session()
    if model == GetPainStatusResponse and set_weather_point is not None:
        res = ses.get(f"{BASE_URL}/setweatherpoint/{set_weather_point}", timeout=TIMEOUT, headers={"User-Agent": UA})
        SetWeatherPointResponse.model_validate_json(res.text)
    res = ses.get(f"{BASE_URL}{path}/{param}", timeout=TIMEOUT, headers={"User-Agent": UA})
    if res.status_code == requests.codes.ok:
        try:
            return model.model_validate_json(res.text)
        except ValidationError as e:
            err_res = ErrorResponse.model_validate_json(res.text)
            raise ValueError(err_res) from e
    raise ValueError(res.status_code, res.text)


def get_pain_status(area_code: str, set_weather_point: str | None = None) -> GetPainStatusResponse:
    return __get("/getpainstatus", area_code, GetPainStatusResponse, set_weather_point=set_weather_point)


def get_weather_point(keyword: str) -> GetWeatherPointResponse:
    return __get("/getweatherpoint", keyword, GetWeatherPointResponse)


def get_weather_status(city_code: str) -> GetWeatherStatusResponse:
    return __get("/getweatherstatus", city_code, GetWeatherStatusResponse)


def get_otenki_asp(city_code: str) -> GetOtenkiASPResponse:
    params: dict[str, str] = {
        "csid": "mmcm",
        "contents_id": "day_tenki--day_pre--hight_temp--low_temp--day_wind_v--day_wind_d--zutu_level_day--low_humidity",
        "duration_yohoushi": "7",
        "where": f"CHITEN_{city_code}",
        "json": "on",
    }
    res = requests.get(
        "https://ap.otenki.com/OtenkiASP/asp/getElements",
        params=params,
        timeout=TIMEOUT,
        headers={"User-Agent": UA},
    )
    try:
        raw_res = _GetOtenkiASPRawResponse.model_validate_json(res.text)
        return GetOtenkiASPResponse(raw_res)
    except ValidationError as e:
        raise ValueError(res.text) from e
