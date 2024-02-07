from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Union

from pydantic import BaseModel, Field, field_validator

from .enum import WeatherEnum

_JTC = timezone(timedelta(hours=9))


class _RawHead(BaseModel):
    contents_id: str = Field(alias="contentsId")
    title: str
    date_time: datetime = Field(alias="dateTime")
    status: str

    @field_validator("date_time", mode="before")
    def validate_date_time(cls, v: str) -> datetime:
        return datetime.strptime(v, "%Y-%m-%d %H").replace(tzinfo=_JTC)


_Property = tuple[datetime, Union[WeatherEnum, float, None]]


class _RawProperty(BaseModel):
    property: _Property

    @field_validator("property", mode="before")
    def validate_property(cls, vs: tuple[str, ...]) -> _Property:
        dt = datetime.strptime(vs[0], "%Y%m%d").replace(tzinfo=_JTC)
        if len(vs) == 2:  # noqa: PLR2004
            return (dt, None if vs[1] == "-" else float(vs[1]))
        if len(vs) == 3:  # noqa: PLR2004
            return (dt, None if vs[2] == "-" else WeatherEnum(vs[2]))
        raise ValueError(vs)


class _RawRecord(BaseModel):
    record: list[_RawProperty]


class _RawElement(BaseModel):
    element: list[_RawRecord]


class _RawBody(BaseModel):
    location: _RawElement


class _GetOtenkiASPRawResponse(BaseModel):
    head: _RawHead
    body: _RawBody


class _Element(BaseModel):
    content_id: str
    title: str
    records: dict[datetime, Union[WeatherEnum, float, None]]  # noqa: UP007


class GetOtenkiASPResponse(BaseModel):
    status: str
    date_time: datetime
    elements: list[_Element]

    def __init__(self, raw_res: _GetOtenkiASPRawResponse) -> None:
        elements: list[_Element] = []
        for i, (content_id, title) in enumerate(
            zip(raw_res.head.contents_id.split("--"), raw_res.head.title.split("--")),
        ):
            records = {record.property[0]: record.property[1] for record in raw_res.body.location.element[i].record}
            elements.append(_Element(content_id=content_id, title=title, records=records))

        super().__init__(
            status=raw_res.head.status,
            date_time=raw_res.head.date_time,
            elements=elements,
        )
