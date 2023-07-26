from typing import Literal

from pydantic import BaseModel


class SetWeatherPointResponse(BaseModel):
    response: Literal["ok"]
