from pydantic import BaseModel

from app.dto.page_elements import Image, Btn
from app.models.common.common import SponsorLevel


class SponsorDto(BaseModel):
    id: str | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    title: str
    subtitle: str | None = None
    brief: str | None = None
    level: SponsorLevel
    order: int | None = None
    image: Image | None = None
    btn: Btn | None = None
