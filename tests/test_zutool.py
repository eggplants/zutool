import pytest

from zutool import get_pain_status, get_weather_point, get_weather_status

HTTP_NOT_FOUND = 404
ZUTOOL_API_NOT_FOUND = 4004
ZUTOOL_API_INVALID_PARAMETER = 4002


def test_pain_status() -> None:
    get_pain_status("13")


def test_pain_status_invalid() -> None:
    with pytest.raises(ValueError) as e:  # noqa: PT011
        get_pain_status("1")
    err = e.value.args[0]
    assert err.error_code == ZUTOOL_API_INVALID_PARAMETER
    assert err.error_message == "存在しない都道府県コードです todofuken_code = 1"


def test_pain_status_empty() -> None:
    get_pain_status("")


def test_weather_point() -> None:
    get_weather_point("神戸市")


def test_weather_point_extra() -> None:
    res = get_weather_point("a")
    assert res.result.root == []


def test_weather_point_empty() -> None:
    with pytest.raises(ValueError) as e:  # noqa: PT011
        get_weather_point("")
    errs = e.value.args
    assert errs[0] == HTTP_NOT_FOUND
    assert "お探しのページは見つかりません" in errs[1]


def test_weather_status_invalid_code() -> None:
    with pytest.raises(ValueError) as e:  # noqa: PT011
        get_weather_status("aaaaa")
    err = e.value.args[0]
    assert err.error_code == ZUTOOL_API_NOT_FOUND
    assert err.error_message == "地点名称が取得できませんでした。 地点コード = aaaaa"


def test_weather_status_invalid_digit() -> None:
    with pytest.raises(ValueError) as e:  # noqa: PT011
        get_weather_status("13")
    err = e.value.args[0]
    assert err.error_code == ZUTOOL_API_INVALID_PARAMETER
    assert err.error_message == "地点コードの桁数が正しくありません。 地点コード = 13"


def test_weather_status_empty() -> None:
    get_weather_status("")
