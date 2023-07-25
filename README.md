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
usage: zutool [-h] {pain_status,ps,weather_point,wp,weather_status,ws} ...

Get info of zutool <https://zutool.jp/>.

positional arguments:
  {pain_status,ps,weather_point,wp,weather_status,ws}
    pain_status (ps)    get pain status by prefecture
    weather_point (wp)  search weather point
    weather_status (ws)
                        get pain status by city

optional arguments:
  -h, --help            show this help message and exit
```

```shellsession
$ zutool ps -h
usage: zutool pain_status [-h] area_code

positional arguments:
  area_code   see: <https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html>
              (ex. `13`)

optional arguments:
  -h, --help  show this help message and exit
```

```shellsession
$ zutool wp -h
usage: zutool weather_point [-h] keyword

positional arguments:
  keyword     keyword for searching city_code (ex. `東京都`)

optional arguments:
  -h, --help  show this help message and exit
```

```shellsession
$ zutool ws -h
usage: zutool weather_status [-h] city_code

positional arguments:
  city_code   see: <https://geoshape.ex.nii.ac.jp/city/code/> (ex. `13113`)

optional arguments:
  -h, --help  show this help message and exit
```
