from __future__ import annotations

import argparse
from datetime import timedelta
from shutil import get_terminal_size
from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

from . import api
from .models.get_pain_status import _GetPainStatus

if TYPE_CHECKING:
    from .models.get_weather_status import _WeatherStatusByTime


class ZutoolFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def func_pain_status(ns: argparse.Namespace) -> None:
    res_raw = api.get_pain_status(ns.area_code, set_weather_point=ns.set_weather_point)
    if bool(ns.json):
        print(res_raw.model_dump_json(indent=4))
        return
    res = res_raw.painnoterate_status

    title_a = f"今のみんなの体調は? <{res.area_name.name}|{res.area_name.value}>"
    title_b = f"(集計時間: {res.time_start}時-{res.time_end}時台)"
    table = Table(title=f"{title_a}\n{title_b}")

    sickness_dic = {k: v.alias for k, v in _GetPainStatus.model_fields.items() if k.startswith("rate_")}
    sickness_emojies = ("😃", "😐", "😞", "🤯")

    data: list[str] = []
    for emoji, sickness_key in zip(sickness_emojies, sickness_dic):  # noqa: B905
        sickness_val = getattr(res, sickness_key)
        data.append(f"{emoji*int(sickness_val/2)} {sickness_val}%")
    table.add_column("\n".join(data))

    emoji_label_dic = zip(sickness_emojies, sickness_dic.values())  # noqa: B905
    table.add_row(
        "[" + ", ".join([f"{emoji}･･･{key}" for emoji, key in emoji_label_dic]) + "]",
    )
    Console().print(table)


def func_weather_point(ns: argparse.Namespace) -> None:
    res = api.get_weather_point(ns.keyword)
    if bool(ns.json):
        print(res.model_dump_json(indent=4))
        return
    table = Table(title=f"「{ns.keyword}」の検索結果")
    table.add_column("地域コード")
    table.add_column("地域名")
    if bool(ns.kata):
        table.add_column("地域カナ")
    for weather_point in res.result.root:
        fields = [weather_point.city_code, weather_point.name]
        if bool(ns.kata):
            fields.append(weather_point.name_kata)
        table.add_row(*fields)
    Console().print(table)


def func_weather_status(ns: argparse.Namespace) -> None:
    def __helper(res: list[_WeatherStatusByTime], n: int, prev_pressure: float, title: str) -> float:
        table = Table()
        for i in range(12 * n, 12 * (n + 1)):
            table.add_column(str(i))
        weathers, temps, pressures, pressure_levels = [], [], [], []
        for by_time in res[12 * n : 12 * (n + 1)]:
            weathers.append({"100": "☼", "200": "☁", "300": "☔", "400": "☃"}[by_time.weather.value])
            temps.append(f"{by_time.temp}℃")
            pressure = by_time.pressure
            pressures.append(
                f"↗\n{pressure}"
                if pressure > prev_pressure
                else f"↘\n{pressure}"
                if pressure < prev_pressure
                else f"→\n{pressure}",
            )
            pressure_levels.append(by_time.pressure_level.name)
        table.add_row(*weathers)
        table.add_row(*temps)
        table.add_row(*pressures)
        table.add_row(*pressure_levels)

        if n == 0:
            table.title = title
        Console().print(table)
        return prev_pressure

    res_raw = api.get_weather_status(ns.city_code)
    if bool(ns.json):
        print(res_raw.model_dump_json(indent=4))
        return
    for day_idx, day in enumerate(("yesterday", "today", "tomorrow", "dayaftertomorrow")):
        res: list[_WeatherStatusByTime] = getattr(res_raw, day)
        title = f"{res_raw.place_name}の気圧予報\n{res_raw.date_time+timedelta(days=day_idx-1)}"
        prev_pressure = __helper(res, 0, 0, title)
        __helper(res, 1, prev_pressure, title)


def parse(test_args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="zutool",
        formatter_class=(
            lambda prog: ZutoolFormatter(
                prog,
                width=get_terminal_size(fallback=(120, 50)).columns,
                max_help_position=50,
            )
        ),
        description="Get info of zutool <https://zutool.jp/>.",
    )

    parser.set_defaults(func=lambda _: parser.print_usage())
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="print as json",
    )

    subparsers = parser.add_subparsers()

    pain_status_parser = subparsers.add_parser("pain_status", aliases=["ps"], help="get pain status by prefecture")
    pain_status_parser.add_argument(
        "area_code",
        type=str,
        help="see: <https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html> (ex. `13`)",
    )
    pain_status_parser.add_argument(
        "-s",
        "--set-weather-point",
        dest="set_weather_point",
        metavar="Weather Point",
        type=str,
        help="set weather point code as default (ex. `13113`)",
    )
    pain_status_parser.set_defaults(func=func_pain_status)

    weather_point_parser = subparsers.add_parser("weather_point", aliases=["wp"], help="search weather point")
    weather_point_parser.add_argument(
        "keyword",
        type=str,
        help="keyword for searching city_code (ex. `東京都`)",
    )
    weather_point_parser.add_argument(
        "-k",
        "--kata",
        action="store_true",
        help="with kata column in non-json output",
    )
    weather_point_parser.set_defaults(func=func_weather_point)

    weather_status_parser = subparsers.add_parser("weather_status", aliases=["ws"], help="get pain status by city")
    weather_status_parser.add_argument(
        "city_code",
        type=str,
        help="see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)",
    )

    weather_status_parser.set_defaults(func=func_weather_status)

    if test_args is not None:
        return parser.parse_args(test_args)
    return parser.parse_args()


def main(test_args: list[str] | None = None) -> None:
    args = parse(test_args=test_args)
    args.func(args)


if __name__ == "__main__":
    main()
