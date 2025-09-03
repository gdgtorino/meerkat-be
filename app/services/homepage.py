from google.cloud.firestore_v1 import CollectionReference

from app.database.firestore import get_firestore_client
from app.dto.home_page import Header, Homepage, Menu
from app.dto.page_elements import Item
from app.models.page import (
    Btn as MBtn,
)
from app.models.page import (
    HeaderText as MHeader,
)
from app.models.page import (
    Image as MImage,
)
from app.models.page import (
    Item as MItem,
)


class HomePageService:
    def __init__(self) -> None:
        self.db = get_firestore_client()

    def _doc_to_homepage(self, homepage_doc: CollectionReference) -> Homepage:
        homepage = {}
        for hp_element in homepage_doc.get():
            homepage.update({hp_element.id: hp_element.to_dict()})

        menu_data = homepage.get("menu")
        header_data = homepage.get("header")
        out = Homepage(
            menu=Menu.model_validate(menu_data) if menu_data else None,
            header=Header.model_validate(header_data) if header_data else None,
            body=[],
            footer=[],
        )
        body_data = homepage.get("body")
        if body_data is not None and body_data.get("items") is not None:
            out.body.extend(Item.model_validate(item) for item in body_data["items"])
        footer_data = homepage.get("footer")
        if footer_data is not None and footer_data.get("items") is not None:
            out.footer.extend(
                Item.model_validate(item) for item in footer_data["items"]
            )
        return out

    def get_homepage(self) -> Homepage:
        homepage_doc = self.db.collection("homepage")
        return self._doc_to_homepage(homepage_doc)

    def put_menu(self, menu: Menu) -> None:
        main_image = None
        items_menu = []
        if menu.main_image is not None:
            main_image = MImage(
                src=menu.main_image.src,
                title=menu.main_image.title,
                caption=menu.main_image.caption,
                btn=MBtn(**menu.main_image.btn.model_dump())
                if menu.main_image.btn
                else None,
            )
            # if menu.main_image.btn is not None:
            #     main_image.btn = menu.main_image.btn

        if menu.items is not None and len(menu.items) > 0:
            items_menu.extend(item.model_dump() for item in menu.items)
        self.db.collection("homepage").document("menu").set(
            {
                "items": items_menu,
                "main_image": main_image.model_dump() if main_image else None,
            }
        )

    def put_header(self, header: Header) -> None:
        main_image = None
        header_text = None
        call_to_action = []
        if header.main_image is not None:
            main_image = MImage(
                src=header.main_image.src,
                title=header.main_image.title,
                caption=header.main_image.caption,
                btn=None,  # the logo of header isn't an ancor!
            )

        if header.header_text is not None:
            header_text = MHeader(**header.header_text.model_dump())

        if header.call_to_action is not None and len(header.call_to_action) > 0:
            call_to_action.extend(item.model_dump() for item in header.call_to_action)

        background_image = header.background_image

        self.db.collection("homepage").document("header").set(
            {
                "main_image": main_image.model_dump() if main_image else None,
                "background_image": background_image.model_dump()
                if background_image
                else None,
                "header_text": header_text.model_dump() if header_text else None,
                "call_to_action": call_to_action,
            }
        )

    def put_section(self, items: list[Item], sections: str) -> None:
        items_to_save = []
        if items is not None and len(items) > 0:
            items_to_save.extend(
                MItem(
                    **item.model_dump(exclude={"type_box", "subsection"}),
                    type_box=item.type_box,
                    subsection=None,
                ).model_dump()  # FIXME implement subsection
                for item in items
            )
        self.db.collection("homepage").document("body").set(
            {
                "items": items_to_save,
            }
        )
