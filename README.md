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
```

## As CLI

```shellsession
$ zutool -h
usage: zutool [-h] [-j] {pain_status,ps,weather_point,wp,weather_status,ws} ...

Get info of zutool <https://zutool.jp/>.

positional arguments:
  {pain_status,ps,weather_point,wp,weather_status,ws}
    pain_status (ps)          get pain status by prefecture
    weather_point (wp)        search weather point
    weather_status (ws)       get pain status by city

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
                                           東京都渋谷区の気圧予報
                                          2023-07-26 03:00:00+09:00
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ 0      ┃ 1      ┃ 2      ┃ 3      ┃ 4      ┃ 5      ┃ 6      ┃ 7      ┃ 8      ┃ 9      ┃ 10     ┃ 11     ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │
│ 27.8℃  │ 28.2℃  │ 26.3℃  │ 26.2℃  │ 26.2℃  │ 26.2℃  │ 26.5℃  │ 27.3℃  │ 28.6℃  │ 30.1℃  │ 31.7℃  │ 33.2℃  │
│ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │
│ 1015.6 │ 1015.5 │ 1015.7 │ 1015.5 │ 1015.4 │ 1015.6 │ 1015.8 │ 1016.0 │ 1016.1 │ 1016.3 │ 1016.2 │ 1015.9 │
│ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │
└────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ 12     ┃ 13     ┃ 14     ┃ 15     ┃ 16     ┃ 17     ┃ 18     ┃ 19     ┃ 20     ┃ 21     ┃ 22     ┃ 23     ┃
┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │ ☼      │
│ 34.5℃  │ 35.3℃  │ 35.7℃  │ 35.2℃  │ 33.9℃  │ 32.2℃  │ 30.4℃  │ 28.6℃  │ 27.2℃  │ 26.5℃  │ 26.3℃  │ 26.3℃  │
│ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │ ↗      │
│ 1015.5 │ 1014.9 │ 1014.3 │ 1013.9 │ 1013.8 │ 1013.8 │ 1014.2 │ 1014.7 │ 1015.4 │ 1016.0 │ 1015.8 │ 1015.9 │
│ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │ 通常_0 │
└────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
```
