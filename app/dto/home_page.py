from pydantic import BaseModel

from app.dto.page_elements import Background, Btn, HeaderText, Image, Item


class Menu(BaseModel):
    main_image: Image | None
    items: list[Btn]


class Header(BaseModel):
    main_image: Image | None
    background_image: Background
    header_text: HeaderText | None
    call_to_action: list[Btn]


class Homepage(BaseModel):
    menu: Menu | None
    header: Header | None
    body: list[Item]
    footer: list[Item]
