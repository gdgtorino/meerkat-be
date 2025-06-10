from typing import List

from pydantic import BaseModel, Field

from app.models.common.common import TypeBox


class Btn(BaseModel):
    id: int | None = None
    label: str
    href: str
    open_new_tab: bool = False
    color_in_background: bool = Field(description="Boolean that define if button must have a background color or none",
                                      default=True)


class Image(BaseModel):
    id: int | None = None
    src: str
    title: str
    caption: str
    btn: Btn | None = Field(description="If image is a link this prop is valued", default=None)


class HeaderText(BaseModel):
    id: int | None = None
    title: str
    subtitle: str


class Background(BaseModel):
    id: int | None = None
    is_image: bool
    image: Image | None
    color: str


class Subsection(BaseModel):
    id: int | None = None
    order: int = 0
    title: str
    subtitle: str
    brief: str
    content: str
    background: Background | None
    image: Image | None
    type_box: TypeBox


class Item(BaseModel):
    id: int | None = None
    order: int = 0
    title: str
    subtitle: str
    brief: str
    content: str
    background: Background | None
    image: Image | None
    type_box: TypeBox
    subsection: List[Subsection] | None
