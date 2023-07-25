from __future__ import annotations

from pydantic import BaseModel


# https://zutool.jp/api/getpainstatus/1
# https://zutool.jp/api/getpainstatus/99
# https://zutool.jp/api/getweatherstatus/1
# https://zutool.jp/api/getweatherstatus/00000
# https://zutool.jp/api/getweatherstatus/000000
class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
