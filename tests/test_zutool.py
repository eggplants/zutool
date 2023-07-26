import pytest

from zutool import get_pain_status, get_weather_point, get_weather_status
from zutool.main import main

HTTP_NOT_FOUND = 404
ZUTOOL_API_NOT_FOUND = 4004
ZUTOOL_API_INVALID_PARAMETER = 4002


def test_pain_status() -> None:
    area_code = "13"
    res = get_pain_status(area_code)
    assert res.painnoterate_status.area_name.value == area_code


def test_pain_status_invalid() -> None:
    with pytest.raises(ValueError) as e:  # noqa: PT011
        get_pain_status("1")
    err = e.value.args[0]
    assert err.error_code == ZUTOOL_API_INVALID_PARAMETER
    assert err.error_message == "存在しない都道府県コードです todofuken_code = 1"


def test_pain_status_empty() -> None:
    city_code_1 = "01101"
    res = get_pain_status("", set_weather_point=city_code_1)
    assert res.painnoterate_status.area_name.value == city_code_1[:2]

    city_code_2 = "13113"
    res = get_pain_status("", set_weather_point=city_code_2)
    assert res.painnoterate_status.area_name.value == city_code_2[:2]


def test_weather_point() -> None:
    keyword = "神戸市"
    res = get_weather_point(keyword)
    assert len(res.result.root) == 9  # noqa: PLR2004


def test_weather_point_extra() -> None:
    res = get_weather_point("a")
    assert res.result.root == []


def test_weather_point_empty() -> None:
    with pytest.raises(ValueError) as e:  # noqa: PT011
        get_weather_point("")
    errs = e.value.args
    assert errs[0] == HTTP_NOT_FOUND
    assert "お探しのページは見つかりません" in errs[1]


def test_weather_status() -> None:
    city_code = "13113"
    res = get_weather_status(city_code)
    assert res.prefectures_id.value + res.place_id == city_code


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
    default_city_code = "13113"
    res = get_weather_status("")
    assert res.prefectures_id.value == default_city_code[:2]
    assert res.place_id == default_city_code[2:]


def test_no_args(capfd: pytest.CaptureFixture[str]) -> None:
    main(test_args=[])
    captured = capfd.readouterr()
    assert "usage: zutool [-h] [-j] {" in captured.out
    assert not captured.err


def test_ps_empty(capfd: pytest.CaptureFixture[str]) -> None:
    default_area_code = "13113"
    main(test_args=["-j", "ps", ""])
    captured = capfd.readouterr()
    assert f'"area_name": "{default_area_code[:2]}"' in captured.out
    assert not captured.err


def test_ps_rich(capfd: pytest.CaptureFixture[str]) -> None:
    area_code = "13"
    main(test_args=["ps", area_code])
    captured = capfd.readouterr()
    assert f"今のみんなの体調は? <東京都|{area_code}>" in captured.out
    assert not captured.err


def test_wp_empty(capfd: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main(test_args=["-j", "wp", ""])
    assert e.value.args[0] == 1

    captured = capfd.readouterr()
    assert not captured.out
    assert "Error: (404, " in captured.err


def test_wp_rich(capfd: pytest.CaptureFixture[str]) -> None:
    keyword = "東京都港区"
    main(test_args=["wp", keyword])
    captured = capfd.readouterr()
    assert f"「{keyword}」の検索結" in captured.out
    assert not captured.err


def test_ws_empty(capfd: pytest.CaptureFixture[str]) -> None:
    default_city_code = "13113"
    main(test_args=["-j", "ws", ""])
    captured = capfd.readouterr()
    assert f'"prefectures_id": "{default_city_code[:2]}",' in captured.out
    assert f'"place_id": "{default_city_code[2:]}",' in captured.out
    assert not captured.err


def test_ws_rich(capfd: pytest.CaptureFixture[str]) -> None:
    city_code = "13113"
    main(test_args=["ws", city_code])
    captured = capfd.readouterr()
    assert "東京都渋谷区の気圧予報" in captured.out
    assert not captured.err
