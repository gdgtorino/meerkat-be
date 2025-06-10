from typing import List

from pydantic import BaseModel

from app.dto.page_elements import Image, Btn, HeaderText, Background, Item


class Menu(BaseModel):
    main_image: Image | None
    items: List[Btn]


class Header(BaseModel):
    main_image: Image | None
    background_image: Background
    header_text: HeaderText | None
    call_to_action: List[Btn]


class Homepage(BaseModel):
    menu: Menu
    header: Header
    body: List[Item]
    footer: List[Item]
