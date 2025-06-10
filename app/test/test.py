import unittest

import unittest
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
from fastapi import HTTPException
import logging

# Mock the EnvYAML and firebase_admin to prevent actual file system and network calls
patch_envyaml = patch('app.config.env.EnvYAML')
patch_firebase_admin = patch('app.database.firestore.firebase_admin')
patch_firestore = patch('app.database.firestore.firestore')


class TestConfigEnv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_EnvYAML = patch_envyaml.start()
        cls.mock_firebase_admin = patch_firebase_admin.start()
        cls.mock_firestore = patch_firestore.start()

    @classmethod
    def tearDownClass(cls):
        patch_envyaml.stop()
        patch_firebase_admin.stop()
        patch_firestore.stop()

    # def test_get_env(self):
    #     from app.config.env import get_env
    #     mock_env_instance = MagicMock()
    #     self.mock_EnvYAML.return_value = mock_env_instance
    #     result = get_env()
    #     self.mock_EnvYAML.assert_called_once_with("./config/resource/env.yaml")
    #     self.assertEqual(result, mock_env_instance)


class TestDatabaseFirestore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_EnvYAML = patch_envyaml.start()
        cls.mock_firebase_admin = patch_firebase_admin.start()
        cls.mock_firestore = patch_firestore.start()

    @classmethod
    def tearDownClass(cls):
        patch_envyaml.stop()
        patch_firebase_admin.stop()
        patch_firestore.stop()

    def test_get_firestore_client_with_prefix(self):
        from app.database.firestore import get_firestore_client

        # Configure the mock EnvYAML to return a prefix
        mock_env_instance = MagicMock()
        mock_env_instance.__getitem__.side_effect = lambda key: "devfest_test" if key == "firestore.prefix" else None
        self.mock_EnvYAML.return_value = mock_env_instance

        # Configure the mock firestore client and collection
        mock_collection = MagicMock()
        mock_client = MagicMock()
        mock_client.collection.return_value = mock_collection
        self.mock_firestore.client.return_value = mock_client

        result = get_firestore_client()

        self.mock_firestore.client.assert_called_once()
        mock_client.collection.assert_called_once_with("devfest_test")
        self.assertEqual(result, mock_collection)

    def test_get_firestore_client_without_prefix(self):
        from app.database.firestore import get_firestore_client

        # Configure the mock EnvYAML to return no prefix
        mock_env_instance = MagicMock()
        mock_env_instance.__getitem__.side_effect = lambda key: None if key == "firestore.prefix" else None
        self.mock_EnvYAML.return_value = mock_env_instance

        # Configure the mock firestore client (should not call .collection)
        mock_client = MagicMock()
        self.mock_firestore.client.return_value = mock_client

        result = get_firestore_client()

        self.mock_firestore.client.assert_called_once()
        mock_client.collection.assert_not_called()
        self.assertIsNone(result)


class TestDtoHomePage(unittest.TestCase):
    def test_homepage_dto_valid_data(self):
        from app.dto.home_page import Homepage, Menu, Header
        from app.dto.page_elements import Image, Btn, HeaderText, Background, Item, TypeBox, Subsection

        menu_data = {
            "main_image": {"src": "menu_img.jpg", "title": "Menu Image", "caption": "Menu Caption",
                           "btn": {"label": "Click", "href": "#"}},
            "items": [{"label": "Home", "href": "/"}, {"label": "About", "href": "/about"}]
        }
        header_data = {
            "main_image": {"src": "header_logo.png", "title": "Logo", "caption": "Company Logo"},
            "background_image": {"is_image": False, "color": "#FFFFFF", "image": {"src": "header_logo.png", "title": "Logo", "caption": "Company Logo"}},
            "header_text": {"title": "Welcome", "subtitle": "To our site"},
            "call_to_action": [{"label": "Learn More", "href": "/learn"}]
        }
        body_item_data = {
            "order": 1, "title": "Body Title", "subtitle": "Body Subtitle", "brief": "Brief", "content": "Content", "image": None,
            "background": {"is_image": False, "color": "#FFFFFF", "image": {"src": "header_logo.png", "title": "Logo", "caption": "Company Logo"}},
            "type_box": {"name": "Text"}, "subsection": []
        }
        footer_item_data = {
            "order": 1, "title": "Footer Title", "subtitle": "Footer Subtitle", "brief": "Brief", "content": "Content",
            "background": None, "image": None,
            "type_box": {"name": "Contact"}, "subsection": []
        }

        homepage_data = {
            "menu": menu_data,
            "header": header_data,
            "body": [body_item_data],
            "footer": [footer_item_data]
        }

        homepage = Homepage(**homepage_data)

        self.assertIsInstance(homepage.menu, Menu)
        self.assertIsInstance(homepage.header, Header)
        self.assertEqual(len(homepage.body), 1)
        self.assertIsInstance(homepage.body[0], Item)
        self.assertEqual(len(homepage.footer), 1)
        self.assertIsInstance(homepage.footer[0], Item)

    def test_homepage_dto_missing_required_fields(self):
        from app.dto.home_page import Homepage
        # Missing 'menu' and 'header' which are required
        with self.assertRaises(ValidationError):
            Homepage(body=[], footer=[])


class TestDtoPageElements(unittest.TestCase):
    def test_btn_dto_valid_data(self):
        from app.dto.page_elements import Btn
        btn = Btn(label="Test Button", href="/test")
        self.assertEqual(btn.label, "Test Button")
        self.assertEqual(btn.href, "/test")
        self.assertTrue(btn.color_in_background)  # Default value

    def test_image_dto_valid_data(self):
        from app.dto.page_elements import Image, Btn
        image = Image(src="test.jpg", title="Test Image", caption="A test image",
                      btn={"label": "View", "href": "/view"})
        self.assertEqual(image.src, "test.jpg")
        self.assertIsInstance(image.btn, Btn)

    def test_header_text_dto_valid_data(self):
        from app.dto.page_elements import HeaderText
        header_text = HeaderText(title="Main Title", subtitle="Sub Title")
        self.assertEqual(header_text.title, "Main Title")

    def test_background_dto_valid_data(self):
        from app.dto.page_elements import Background, Image
        bg = Background(is_image=True, image={"src": "bg.jpg", "title": "BG", "caption": "Background", "color":"FFFFFF"}, color="FF5600")
        self.assertTrue(bg.is_image)
        self.assertIsInstance(bg.image, Image)
        self.assertIsNotNone(bg.color)

    def test_item_dto_valid_data(self):
        from app.dto.page_elements import Item, TypeBox
        item = Item(order=1, title="Item Title", subtitle="Item Subtitle", brief="Brief", content="Content",
                    type_box={"name": "Generic"},
                    background={"is_image": False, "color": "#FFFFFF", "image":None}, image=None, subsection=[])
        self.assertEqual(item.title, "Item Title")
        self.assertIsInstance(item.type_box, TypeBox)


class TestModelsCommon(unittest.TestCase):
    def test_type_box_model_valid_data(self):
        from app.models.common.common import TypeBox
        type_box = TypeBox(id=1, name="Category")
        self.assertEqual(type_box.id, 1)
        self.assertEqual(type_box.name, "Category")

    def test_type_box_model_missing_name(self):
        from app.models.common.common import TypeBox
        with self.assertRaises(ValidationError):
            TypeBox(id=1)


class TestModelsPage(unittest.TestCase):
    def test_btn_model_valid_data(self):
        from app.models.page import Btn
        btn = Btn(label="Model Button", href="/model")
        self.assertEqual(btn.label, "Model Button")

    def test_image_model_valid_data(self):
        from app.models.page import Image, Btn
        image = Image(src="model.jpg", title="Model Image", caption="Model Caption", btn={"label": "Link", "href": "#"})
        self.assertIsInstance(image.btn, Btn)

    def test_item_model_valid_data(self):
        from app.models.page import Item
        from app.models.common.common import TypeBox
        item = Item(order=1,
                    title="Model Item",
                    subtitle="Sub",
                    brief="Brief",
                    content="Content",
                    background=None,
                    image=None,
                    type_box={"name": "Info"},
                    subsection=None)
        self.assertIsInstance(item.type_box, TypeBox)


class TestHomePageService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_firestore_client = patch('app.services.homepage.get_firestore_client').start()
        cls.mock_db = MagicMock()
        cls.mock_firestore_client.return_value = cls.mock_db

    @classmethod
    def tearDownClass(cls):
        patch('app.services.homepage.get_firestore_client').stop()

    def setUp(self):
        # Reset mocks before each test
        self.mock_db.reset_mock()


    def test_get_homepage_not_exists(self):
        from app.services.homepage import HomePageService
        mock_doc = MagicMock()
        mock_doc.get.return_value.exists = False
        self.mock_db.document.return_value = mock_doc

        service = HomePageService()
        homepage = service.get_homepage()

        self.assertIsNone(homepage)
        mock_doc.get.assert_called_once()

    def test_put_menu(self):
        from app.services.homepage import HomePageService
        from app.dto.home_page import Menu
        from app.dto.page_elements import Image, Btn

        menu_data = Menu(
            main_image=Image(src="test.jpg", title="Test", caption="Cap", btn=Btn(label="Click", href="#")),
            items=[Btn(label="Item1", href="/item1")]
        )

        mock_document_ref = MagicMock()
        self.mock_db.document.return_value = mock_document_ref

        service = HomePageService()
        service.put_menu(menu_data)

        mock_document_ref.update.assert_called_once()
        args, kwargs = mock_document_ref.update.call_args
        self.assertIn("field_updates", kwargs)
        menu_update = kwargs["field_updates"]["menu"]
        self.assertIn("main_image", menu_update)
        self.assertIn("items", menu_update)
        self.assertEqual(menu_update["items"][0]["label"], "Item1")
        self.assertEqual(menu_update["main_image"]["title"], "Test")

    def test_put_header(self):
        from app.services.homepage import HomePageService
        from app.dto.home_page import Header
        from app.dto.page_elements import Image, Background, HeaderText, Btn

        header_data = Header(
            main_image=Image(src="logo.png", title="Logo", caption="App Logo"),
            background_image=Background(is_image=False, color="#123456", image=None),
            header_text=HeaderText(title="Great App", subtitle="Welcome"),
            call_to_action=[Btn(label="Download", href="/download")]
        )

        mock_document_ref = MagicMock()
        self.mock_db.document.return_value = mock_document_ref

        service = HomePageService()
        service.put_header(header_data)

        mock_document_ref.update.assert_called_once()
        args, kwargs = mock_document_ref.update.call_args
        self.assertIn("field_updates", kwargs)
        header_update = kwargs["field_updates"]["header"]
        self.assertIn("main_image", header_update)
        self.assertIn("background_image", header_update)
        self.assertIn("header_text", header_update)
        self.assertIn("call_to_action", header_update)
        self.assertEqual(header_update["header_text"]["title"], "Great App")
        self.assertEqual(header_update["call_to_action"][0]["label"], "Download")

    def test_put_section(self):
        from app.services.homepage import HomePageService
        from app.dto.page_elements import Item, TypeBox

        items_data = [
            Item(order=1, title="Section Item 1", subtitle="Sub1", brief="Brief1", content="Content1", background=None, image=None,
                 type_box=TypeBox(name="Feature"), subsection=[]),
            Item(order=2, title="Section Item 2", subtitle="Sub2", brief="Brief2", content="Content2", background=None, image=None,
                 type_box=TypeBox(name="Info"), subsection=[])
        ]
        section_name = "body"

        mock_document_ref = MagicMock()
        self.mock_db.document.return_value = mock_document_ref

        service = HomePageService()
        service.put_section(items_data, section_name)

        mock_document_ref.update.assert_called_once()
        args, kwargs = mock_document_ref.update.call_args
        self.assertIn("field_updates", kwargs)
        section_update = kwargs["field_updates"][section_name]
        self.assertIn("items", section_update)
        self.assertEqual(len(section_update["items"]), 2)
        self.assertEqual(section_update["items"][0]["title"], "Section Item 1")
        self.assertEqual(section_update["items"][1]["order"], 2)


class TestHomepageRouter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Patch HomePageService at the module level where it's imported in the router
        cls.patcher = patch('app.router.homepage.HomePageService')
        cls.mock_homepage_service_class = cls.patcher.start()
        cls.mock_homepage_service_instance = MagicMock()
        cls.mock_homepage_service_class.return_value = cls.mock_homepage_service_instance

        # Patch logging to prevent actual logging output during tests
        cls.patch_logging = patch('app.router.homepage.logging')
        cls.mock_logging = cls.patch_logging.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        cls.patch_logging.stop()

    def setUp(self):
        # Reset mocks before each test
        self.mock_homepage_service_instance.reset_mock()
        self.mock_logging.error.reset_mock()

    def test_get_homepage_http_exception(self):
        from app.router.homepage import get_homepage
        self.mock_homepage_service_instance.get_homepage.side_effect = HTTPException(status_code=404,
                                                                                     detail="Not found")

        with self.assertRaises(HTTPException) as cm:
            get_homepage()
        self.assertEqual(cm.exception.status_code, 404)
        self.assertEqual(cm.exception.detail, "Not found")
        self.mock_homepage_service_instance.get_homepage.assert_called_once()

    def test_get_homepage_generic_exception(self):
        from app.router.homepage import get_homepage
        self.mock_homepage_service_instance.get_homepage.side_effect = Exception("Something unexpected")

        with self.assertRaises(HTTPException) as cm:
            get_homepage()
        self.assertEqual(cm.exception.status_code, 500)
        self.assertEqual(cm.exception.detail, "Qualcosa è andato storto riprova più tardi")
        self.mock_homepage_service_instance.get_homepage.assert_called_once()
        self.mock_logging.error.assert_called_once()

    def test_put_header_success(self):
        from app.router.homepage import \
            put_menu as put_header_route  # Renamed in patch to put_menu, but logically it's put_header
        from app.dto.home_page import Header
        from app.dto.page_elements import Background

        header_data = Header(main_image=None, background_image=Background(is_image=False, color="#fff", image=None),
                             header_text=None, call_to_action=[])
        self.mock_homepage_service_instance.put_header.return_value = None

        response = put_header_route(header_data)  # Call using the actual function name in the router
        self.assertIsNone(response)
        self.mock_homepage_service_instance.put_header.assert_called_once_with(header=header_data)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
