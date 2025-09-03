from pydantic import BaseModel

from app.models.page import Btn, Image


class Sponsor(BaseModel):
    id: str | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    title: str
    subtitle: str | None = None
    brief: str | None = None
    level: int
    order: int | None = None
    image: Image | None = None
    btn: Btn | None = None
