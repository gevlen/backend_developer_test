from pydantic import BaseModel, Field

from datetime import date
from typing import List


class UserResponseV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class UserAddRequestV1(BaseModel):
    id: int = Field(..., ge=1)
    login: str
    name: str


class StatsResponseV1(BaseModel):
    user_id: int = Field(..., ge=1)
    repo_id: int = Field(..., ge=1)
    date: date
    stargazers: int
    forks: int
    watchers: int


class UserStatsResponseV1(BaseModel):
    user: UserResponseV1
    stats: List[StatsResponseV1]
