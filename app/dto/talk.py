from typing import List

from pydantic import BaseModel


class TalkDto(BaseModel):
    id: str | None = None
    title: str
    subtitle: str | None = None
    brief: str | None = None
    description: str | None = None
    level: str | None = None
    language: str | None = None
    speakers: List[str] | None
