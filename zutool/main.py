from __future__ import annotations

import argparse
from shutil import get_terminal_size

from . import api


class ZutoolFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def func_pain_status(ns: argparse.Namespace) -> None:
    print(api.get_pain_status(ns.area_code).model_dump_json(indent=4))


def func_weather_point(ns: argparse.Namespace) -> None:
    print(api.get_weather_point(ns.keyword).model_dump_json(indent=4))


def func_weather_status(ns: argparse.Namespace) -> None:
    print(api.get_weather_status(ns.city_code, set_weather_point=ns.set_weather_point).model_dump_json(indent=4))


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

    subparsers = parser.add_subparsers()

    pain_status_parser = subparsers.add_parser("pain_status", aliases=["ps"], help="get pain status by prefecture")
    pain_status_parser.add_argument(
        "area_code",
        type=str,
        help="see: <https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html> (ex. `13`)",
    )
    pain_status_parser.set_defaults(func=func_pain_status)

    weather_point_parser = subparsers.add_parser("weather_point", aliases=["wp"], help="search weather point")
    weather_point_parser.add_argument(
        "keyword",
        type=str,
        help="keyword for searching city_code (ex. `東京都`)",
    )
    weather_point_parser.set_defaults(func=func_weather_point)

    weather_status_parser = subparsers.add_parser("weather_status", aliases=["ws"], help="get pain status by city")
    weather_status_parser.add_argument(
        "city_code",
        type=str,
        help="see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)",
    )
    weather_status_parser.add_argument(
        "-s",
        "--set-weather-point",
        dest="set_weather_point",
        metavar="Weather Point",
        type=str,
        help="set weather point code as default. (ex. `13113`)",
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
