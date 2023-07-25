from __future__ import annotations

from enum import Enum


# https://zutool.jp/img/weatherpoint/map_kiatu_icon_lv{level}.png
class PressureLevelEnum(Enum):
    通常_0 = "0"
    通常_1 = "1"
    やや警戒 = "2"
    注意 = "3"
    警戒 = "4"
    超警戒 = "5"


# https://zutool.jp/img/weatherpoint/tenki_{code}.png
class WeatherEnum(Enum):
    sunny = "100"
    cloudy = "200"
    rainy = "300"
    snowy = "400"


# curl "https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html" |
# grep "</td><td>" | awk -F '[<>]' '$0="    "$7" = \""$3"\""' | sort -Vk2


# v->n: AreaEnum("01").name
# n->v: AreaEnum["北海道"].value
class AreaEnum(Enum):
    北海道 = "01"
    青森県 = "02"
    岩手県 = "03"
    宮城県 = "04"
    秋田県 = "05"
    山形県 = "06"
    福島県 = "07"
    茨城県 = "08"
    栃木県 = "09"
    群馬県 = "10"
    埼玉県 = "11"
    千葉県 = "12"
    東京都 = "13"
    神奈川県 = "14"
    新潟県 = "15"
    富山県 = "16"
    石川県 = "17"
    福井県 = "18"
    山梨県 = "19"
    長野県 = "20"
    岐阜県 = "21"
    静岡県 = "22"
    愛知県 = "23"
    三重県 = "24"
    滋賀県 = "25"
    大阪府 = "27"
    兵庫県 = "28"
    奈良県 = "29"
    和歌山県 = "30"
    鳥取県 = "31"
    島根県 = "32"
    岡山県 = "33"
    広島県 = "34"
    山口県 = "35"
    徳島県 = "36"
    香川県 = "37"
    愛媛県 = "38"
    高知県 = "39"
    福岡県 = "40"
    佐賀県 = "41"
    長崎県 = "42"
    熊本県 = "43"
    大分県 = "44"
    宮崎県 = "45"
    鹿児島県 = "46"
    沖縄県 = "47"
