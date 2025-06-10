from typing import List

from pydantic import BaseModel, Field

from app.models.common.common import TypeBox


class Btn(BaseModel):
    id: int | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    label: str
    href: str
    open_new_tab: bool = False
    color_in_background: bool = Field(description="Boolean that define if button must have a background color or none",
                                      default=True)


class Image(BaseModel):
    # id: int | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    src: str
    # width: int
    # height: int
    title: str
    caption: str
    btn: Btn | None = Field(description="If image is a link this prop is valued", default=None)


class HeaderText(BaseModel):
    id: int | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    title: str
    subtitle: str


class Background(BaseModel):
    id: int | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    is_image: bool
    image: Image | None
    color: str


class Item(BaseModel):
    id: int | None = None
    # last_modified: datetime
    # created_at: datetime
    # user_created: int
    # user_last_modified: int
    # END COMMON
    order: int = 0
    title: str
    subtitle: str
    brief: str
    content: str
    background: Background | None
    image: Image | None
    type_box: TypeBox
    subsection: List[str] | None
