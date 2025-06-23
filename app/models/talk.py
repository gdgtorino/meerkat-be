from typing import List

from pydantic import BaseModel


class Talk(BaseModel):
    id: str | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    title: str
    subtitle: str | None = None
    brief: str | None = None
    description: str | None = None
    level: str | None = None
    language: str | None = None
    speakers: List[str] | None  # FIXME : Add obj speaker
