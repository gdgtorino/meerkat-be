from typing import List

from google.cloud.firestore_v1 import DocumentReference, CollectionReference

from app.database.firestore import get_firestore_client
from app.dto.home_page import Menu, Header, Homepage
from app.dto.page_elements import Item
from app.models.page import Image as MImage, Btn as MBtn, HeaderText as MHeader, Item as MItem


class HomePageService():
    def __init__(self):
        self.db = get_firestore_client()

    def _doc_to_homepage(self, homepage_doc: CollectionReference) -> Homepage:
        homepage = {}
        for hp_element in homepage_doc.get():
            homepage.update({hp_element.id: hp_element.to_dict()})


        out = Homepage(menu=Menu.model_validate(homepage.get("menu") if homepage.get("menu") else None),
                       header=Header.model_validate(homepage.get("header") if homepage.get("header") else None),
                       body=[],
                       footer=[])
        if homepage.get("body") is not None and homepage.get("body")["items"] is not None:
            out.body.extend(Item.model_validate(item) for item in homepage.get("body")["items"])
        if homepage.get("footer") is not None and homepage.get("footer")["items"] is not None:
            out.footer.extend(Item.model_validate(item) for item in homepage.get("footer")["items"])
        return out


    def get_homepage(self) -> Homepage:
        homepage_doc = self.db.collection('homepage')
        return self._doc_to_homepage(homepage_doc)

    def put_menu(self, menu: Menu):
        main_image = None
        items_menu = []
        if menu.main_image is not None:
            main_image = MImage(
                src=menu.main_image.src,
                title=menu.main_image.title,
                caption=menu.main_image.caption,
                btn=MBtn(**menu.main_image.btn.model_dump())
            )
            # if menu.main_image.btn is not None:
            #     main_image.btn = menu.main_image.btn

        if menu.items is not None and len(menu.items) > 0:
            items_menu.extend(
                item.model_dump() for item in menu.items
            )
        self.db.collection("homepage").document("menu").set({
            "items": items_menu,
            "main_image": main_image.model_dump(),
        })

    def put_header(self, header: Header):
        main_image = None
        header_text = None
        call_to_action = []
        if header.main_image is not None:
            main_image = MImage(
                src=header.main_image.src,
                title=header.main_image.title,
                caption=header.main_image.caption,
                btn=None  # the logo of header isn't an ancor!
            )

        if header.header_text is not None:
            header_text = MHeader(**header.header_text.model_dump())

        if header.call_to_action is not None and len(header.call_to_action) > 0:
            call_to_action.extend(
                item.model_dump() for item in header.call_to_action
            )

        background_image = header.background_image

        self.db.collection("homepage").document("header").set({
            "main_image": main_image.model_dump(),
            "background_image": background_image.model_dump(),
            "header_text": header_text.model_dump(),
            "call_to_action": call_to_action,
        })

    def put_section(self, items: List[Item], sections: str):
        items_to_save = []
        if items is not None and len(items) > 0:
            items_to_save.extend(
                MItem(**item.model_dump(exclude={"type_box", "subsection"}), type_box=item.type_box,
                      subsection=None)  # FIXME implement subsection
                .model_dump() for item in items
            )
        self.db.collection("homepage").document("body").set({
            "items": items_to_save,
        })
