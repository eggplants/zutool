from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from shutil import get_terminal_size
from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

from . import api
from .models.dict import CONFIRMED_OTENKI_ASP_CITY_CODE_DICT, WEATHER_EMOJI_DICT
from .models.get_pain_status import _GetPainStatus

if TYPE_CHECKING:
    from .models.get_weather_status import _WeatherStatusByTime


class _ZutoolFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def __get_formatter_class(prog: str, max_help_position: int = 50) -> _ZutoolFormatter:
    return _ZutoolFormatter(
        prog,
        width=get_terminal_size(fallback=(120, 50)).columns,
        max_help_position=max_help_position,
    )


def func_pain_status(ns: argparse.Namespace) -> None:
    try:
        res_raw = api.get_pain_status(ns.area_code, set_weather_point=ns.set_weather_point)
    except ValueError as e:
        print(f"{type(e).__name__}:", e, file=sys.stderr)
        sys.exit(1)
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
    for emoji, sickness_key in zip(sickness_emojies, sickness_dic):
        sickness_val = getattr(res, sickness_key)
        data.append(f"{emoji*int(sickness_val/2)} {sickness_val}%")
    table.add_column("\n".join(data))

    emoji_label_dic = zip(sickness_emojies, sickness_dic.values())
    table.add_row(
        "[" + ", ".join([f"{emoji}･･･{key}" for emoji, key in emoji_label_dic]) + "]",
    )
    Console().print(table)


def func_weather_point(ns: argparse.Namespace) -> None:
    try:
        res = api.get_weather_point(ns.keyword)
    except ValueError as e:
        print(f"{type(e).__name__}:", e, file=sys.stderr)
        sys.exit(1)
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


def __func_weather_status_helper(res: list[_WeatherStatusByTime], n: int, prev_pressure: float, title: str) -> float:
    table = Table()
    for i in range(12 * n, 12 * (n + 1)):
        table.add_column(str(i))
    weathers, temps, pressures, pressure_levels = [], [], [], []
    for by_time in res[12 * n : 12 * (n + 1)]:
        weathers.append(WEATHER_EMOJI_DICT[int(by_time.weather.value)])
        temps.append(f"{by_time.temp or '-'}℃")
        pressure = by_time.pressure
        pressures.append(
            (
                f"↗\n{pressure}"
                if pressure > prev_pressure
                else f"↘\n{pressure}" if pressure < prev_pressure else f"→\n{pressure}"
            ),
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


def func_weather_status(ns: argparse.Namespace) -> None:
    try:
        res_raw = api.get_weather_status(ns.city_code)
    except ValueError as e:
        print(f"{type(e).__name__}:", e, file=sys.stderr)
        sys.exit(1)
    if bool(ns.json):
        print(res_raw.model_dump_json(indent=4))
        return

    for day_idx, day in [(n, ("yesterday", "today", "tomorrow", "dayaftertomorrow")[n + 1]) for n in ns.n]:
        res: list[_WeatherStatusByTime] = getattr(res_raw, day)
        title = f"<{res_raw.place_name}|{ns.city_code}>の気圧予報\n{day} = {res_raw.date_time+timedelta(days=day_idx)}"
        prev_pressure = __func_weather_status_helper(res, 0, 0, title)
        __func_weather_status_helper(res, 1, prev_pressure, title)


def func_otenki_asp(ns: argparse.Namespace) -> None:
    try:
        res = api.get_otenki_asp(ns.city_code)
    except ValueError as e:
        print(f"{type(e).__name__}:", e, file=sys.stderr)
        sys.exit(1)
    if bool(ns.json):
        print(res.model_dump_json(indent=4))
        return
    table = Table(title=f"<{CONFIRMED_OTENKI_ASP_CITY_CODE_DICT[ns.city_code]}|{ns.city_code}>の天気情報")
    table.add_column("日付")
    for element in res.elements:
        table.add_column(element.title.replace("(日別)", ""))

    target_date_times = [date_time for i, date_time in enumerate(res.elements[0].records.keys()) if i in ns.n]
    for target_date_time in target_date_times:
        table.add_row(
            target_date_time.strftime("%m/%d"),
            *[getattr(v := element.records[target_date_time], "name", str(v)) for element in res.elements],
        )
    Console().print(table)


def parse(test_args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="zutool",
        formatter_class=lambda prog: __get_formatter_class(prog, 30),
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

    pain_status_parser = subparsers.add_parser(
        "pain_status",
        aliases=["ps"],
        formatter_class=lambda prog: __get_formatter_class(prog, 20),
        help="get pain status by prefecture",
    )
    pain_status_parser.add_argument(
        "area_code",
        type=str,
        help="see: <https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html> (ex. `13`)",
    )
    pain_status_parser.add_argument(
        "-s",
        dest="set_weather_point",
        metavar="CODE",
        type=str,
        help="set weather point code as default (ex. `13113`)",
    )
    pain_status_parser.set_defaults(func=func_pain_status)

    weather_point_parser = subparsers.add_parser(
        "weather_point",
        aliases=["wp"],
        formatter_class=lambda prog: __get_formatter_class(prog),
        help="search weather point",
    )
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

    weather_status_parser = subparsers.add_parser(
        "weather_status",
        aliases=["ws"],
        formatter_class=lambda prog: __get_formatter_class(prog),
        help="get pain status by city",
    )
    weather_status_parser.add_argument(
        "city_code",
        type=str,
        help="see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)",
    )
    weather_status_parser.add_argument(
        "-n",
        choices=range(-1, 3),
        default=[0],
        type=int,
        metavar="N",
        nargs="+",
        help="specify day number to show",
    )

    weather_status_parser.set_defaults(func=func_weather_status)

    otenki_asp_parser = subparsers.add_parser(
        "otenki_asp",
        aliases=["oa"],
        formatter_class=lambda prog: __get_formatter_class(prog),
        help="get weather infomations",
    )
    otenki_asp_parser.add_argument(
        "city_code",
        choices=CONFIRMED_OTENKI_ASP_CITY_CODE_DICT.keys(),
        type=str,
        help="see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)",
    )
    otenki_asp_parser.add_argument(
        "-n",
        choices=range(7),
        default=[*range(7)],
        type=int,
        metavar="N",
        nargs="+",
        help="specify day number to show",
    )

    otenki_asp_parser.set_defaults(func=func_otenki_asp)

    if test_args is not None:
        return parser.parse_args(test_args)
    return parser.parse_args()


def main(test_args: list[str] | None = None) -> None:
    args = parse(test_args=test_args)
    args.func(args)


if __name__ == "__main__":
    main()
