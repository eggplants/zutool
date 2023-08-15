# zutool

[![PyPI version](
  <https://badge.fury.io/py/zutool.svg>
  )](
  <https://badge.fury.io/py/zutool>
) [![Maintainability](
  <https://api.codeclimate.com/v1/badges/b999c03e104b0629e426/maintainability>
  )](
  <https://codeclimate.com/github/eggplants/zutool/maintainability>
) [![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/zutool/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/zutool/master>
) [![Test Coverage](
  <https://api.codeclimate.com/v1/badges/b999c03e104b0629e426/test_coverage>
  )](
  <https://codeclimate.com/github/eggplants/zutool/test_coverage>
) [![Test](
  <https://github.com/eggplants/zutool/actions/workflows/test.yml/badge.svg>
  )](
  <https://github.com/eggplants/zutool/actions/workflows/test.yml>
) [![Release](
  <https://github.com/eggplants/zutool/actions/workflows/release.yml/badge.svg>
  )](
  <https://github.com/eggplants/zutool/actions/workflows/release.yml>
)

[![ghcr latest](
  <https://ghcr-badge.deta.dev/eggplants/zutool/latest_tag?trim=major&label=latest>
 ) ![ghcr size](
  <https://ghcr-badge.deta.dev/eggplants/zutool/size>
)](
  <https://github.com/eggplants/zutool/pkgs/container/zutool>
)

Unofficial zutool (頭痛ール: <https://zutool.jp/>) API Wrapper

## Install

```bash
pip install zutool
```

## As Library

```python
import zutool as z

# see: <https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html>
area_code = "13" # 東京都
z.get_pain_status(area_code)

keyword = "東京都"
z.get_weather_point(keyword)

# see: <https://geoshape.ex.nii.ac.jp/city/code/?13113>
city_code = "13113" # 東京都渋谷区
z.get_weather_status(city_code)

city_code = "13101" # 東京都千代田区
z.get_otenki_asp(city_code)
```

## As CLI

```shellsession
$ zutool -h
usage: zutool [-h] [-j] {pain_status,ps,weather_point,wp,weather_status,ws,otenki_asp,oa} ...

Get info of zutool <https://zutool.jp/>.

positional arguments:
  {pain_status,ps,weather_point,wp,weather_status,ws,otenki_asp,oa}
    pain_status (ps)          get pain status by prefecture
    weather_point (wp)        search weather point
    weather_status (ws)       get pain status by city
    otenki_asp (oa)           get weather infomations

optional arguments:
  -h, --help                  show this help message and exit
  -j, --json                  print as json (default: False)
```

### `pain_status (ps)`

```shellsession
$ zutool ps -h
usage: zutool pain_status [-h] [-s CODE] area_code

positional arguments:
  area_code   see: <https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html> (ex. `13`)

optional arguments:
  -h, --help  show this help message and exit
  -s CODE     set weather point code as default (ex. `13113`) (default: None)
```

```shellsession
$ zutool ps 01
             今のみんなの体調は？ <北海道|01>
                 (集計時間: 12時-18時台)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 😃😃😃😃😃😃😃😃 17.098445595855%                      ┃
┃ 😐😐😐😐😐😐😐😐😐😐😐😐😐😐😐 31.60621761658%         ┃
┃ 😞😞😞😞😞😞😞😞😞😞😞😞😞😞😞😞😞😞 37.823834196891%  ┃
┃ 🤯🤯🤯🤯🤯🤯 13.471502590674%                          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ [😃･･･普通, 😐･･･少し痛い, 😞･･･痛い, 🤯･･･かなり痛い] │
└────────────────────────────────────────────────────────┘
```

### `weather_point (wp)`

```shellsession
$ zutool wp -h
usage: zutool weather_point [-h] [-k] keyword

positional arguments:
  keyword     keyword for searching city_code (ex. `東京都`)

optional arguments:
  -h, --help  show this help message and exit
  -k, --kata  with kata column in non-json output (default: False)
```

```shellsession
$ zutool wp "港区"
        「港区」の検索結果
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ 地域コード ┃ 地域名             ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 13103      │ 東京都港区         │
│ 23111      │ 愛知県名古屋市港区 │
│ 27107      │ 大阪府大阪市港区   │
└────────────┴────────────────────┘
```

### `weather_status (ws)`

```shellsession
$ zutool ws -h
usage: zutool weather_status [-h] [-n N [N ...]] city_code

positional arguments:
  city_code     see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)

optional arguments:
  -h, --help    show this help message and exit
  -n N [N ...]  specify day number to show (default: [0])
```

```shellsession
$ zutool ws 13113
                                                   <東京都渋谷区|13113>の気圧予報
                                                  today = 2023-08-15 20:00:00+09:00 
┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ 0        ┃ 1        ┃ 2        ┃ 3        ┃ 4        ┃ 5        ┃ 6        ┃ 7        ┃ 8        ┃ 9        ┃ 10       ┃ 11       ┃
┡━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ ☁        │ ☁        │ ☔       │ ☔       │ ☁        │ ☔       │ ☁        │ ☁        │ ☔       │ ☔       │ ☁        │ ☁        │
│ 28.4℃    │ 27.5℃    │ 27.3℃    │ 26.5℃    │ 26.9℃    │ 26.7℃    │ 26.9℃    │ 27.9℃    │ 28.4℃    │ 28.4℃    │ 29.1℃    │ 30.7℃    │
│ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │ ↗        │
│ 1004.8   │ 1004.2   │ 1004.3   │ 1004.3   │ 1004.6   │ 1004.9   │ 1005.2   │ 1005.4   │ 1005.8   │ 1006.0   │ 1005.8   │ 1005.3   │
│ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │ やや警戒 │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ 12       ┃ 13       ┃ 14       ┃ 15     ┃ 16     ┃ 17     ┃ 18     ┃ 19     ┃ 20     ┃ 21       ┃ 22       ┃ 23       ┃
┡━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ ☁        │ ☀        │ ☀        │ ☀      │ ☀      │ ☔     │ ☁      │ ☁      │ ☔     │ ☔       │ ☔       │ ☔       │
│ 31.1℃    │ 32.2℃    │ 31.9℃    │ 31.6℃  │ 31.3℃  │ 29.9℃  │ 29.3℃  │ 29.2℃  │ 28.4℃  │ 27.9℃    │ 27.5℃    │ 27.2℃    │
│ ↗        │ ↗        │ ↗        │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗        │ ↗        │ ↗        │
│ 1005.1   │ 1004.9   │ 1004.9   │ 1004.6 │ 1004.7 │ 1004.8 │ 1005.2 │ 1005.7 │ 1006.3 │ 1006.5   │ 1006.5   │ 1006.4   │
│ やや警戒 │ やや警戒 │ やや警戒 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ やや警戒 │ やや警戒 │ やや警戒 │
└──────────┴──────────┴──────────┴────────┴────────┴────────┴────────┴────────┴────────┴──────────┴──────────┴──────────┘
```

### `otenki_asp (oa)`

```shellsession
$ zutool oa -h
usage: zutool otenki_asp [-h] [-n N [N ...]] {01101,04101,13101,15103,17201,23106,27128,34101,39201,40133,47201}

positional arguments:
  {01101,04101,13101,15103,17201,23106,27128,34101,39201,40133,47201}
                                                  see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)

optional arguments:
  -h, --help                                      show this help message and exit
  -n N [N ...]                                    specify day number to show (default: [0, 1, 2, 3, 4, 5, 6])
```

```shellsession
$ zutool oa 13101
                                            <東京|13101>の天気情報
┏━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ 日付  ┃ 天気       ┃ 降水確率 ┃ 最高気温 ┃ 最低気温 ┃ 最大風速 ┃ 最大風速時風向 ┃ 気圧予報レベル ┃ 最小湿度 ┃
┡━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 08/02 │ 晴れ       │ 10.0     │ 35.0     │ 26.0     │ 11.2     │ 8.0            │ 2.0            │ 60.5     │
│ 08/03 │ 晴れ       │ 10.0     │ 36.0     │ 26.0     │ 11.8     │ 8.0            │ 4.0            │ 63.6     │
│ 08/04 │ 晴れ       │ 0.0      │ 36.0     │ 26.0     │ 10.0     │ 8.0            │ 2.0            │ 59.6     │
│ 08/05 │ 晴れのち雨 │ 30.0     │ 36.0     │ 27.0     │ 11.8     │ 8.0            │ 1.0            │ 64.3     │
│ 08/06 │ 雨のち晴れ │ 30.0     │ 36.0     │ 27.0     │ 10.3     │ 8.0            │ 2.0            │ 61.9     │
│ 08/07 │ 晴れのち雨 │ 50.0     │ 33.0     │ 26.0     │ 7.2      │ 2.0            │ 2.0            │ 63.6     │
│ 08/08 │ 雨一時晴れ │ 80.0     │ 33.0     │ 26.0     │ 6.2      │ 6.0            │ 1.0            │ 79.5     │
└───────┴────────────┴──────────┴──────────┴──────────┴──────────┴────────────────┴────────────────┴──────────┘
```
