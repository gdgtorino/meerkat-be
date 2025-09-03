import logging

from fastapi import APIRouter, HTTPException

from app.dto.home_page import Header, Homepage, Menu
from app.dto.page_elements import Item
from app.services.homepage import HomePageService

router_public = APIRouter(
    prefix="/homepage",
    tags=["homepage"],
)


@router_public.post(
    "",
    status_code=200,
    description="Get homepage",
)
def get_homepage() -> Homepage:
    try:
        homepage_service = HomePageService()
        return homepage_service.get_homepage()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        logging.error("Error in router_homepage.get_homepage() - ", e)
        raise HTTPException(
            status_code=500, detail="Qualcosa è andato storto riprova più tardi"
        ) from e


router_protected = APIRouter(
    prefix="/homepage",
    tags=["homepage"],
    # dependencies=[Depends(api_key_auth)]
)


@router_protected.put(
    "/menu",
    status_code=200,
    description="Create or update menu",
)
def put_menu(menu: Menu) -> None:
    try:
        homepage_service = HomePageService()
        homepage_service.put_menu(menu=menu)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        logging.error("Error in router_homepage.put_header() - ", e)
        raise HTTPException(
            status_code=500, detail="Qualcosa è andato storto riprova più tardi"
        ) from e


@router_protected.put(
    "/header",
    status_code=200,
    description="Create or update header",
)
def put_header(header: Header) -> None:
    try:
        homepage_service = HomePageService()
        homepage_service.put_header(header=header)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        logging.error("Error in router_homepage.put_header() - ", e)
        raise HTTPException(
            status_code=500, detail="Qualcosa è andato storto riprova più tardi"
        ) from e


@router_protected.put(
    "/body",
    status_code=200,
    description="Create or update body",
)
def put_body(items: list[Item]) -> None:
    try:
        homepage_service = HomePageService()
        homepage_service.put_section(items=items, sections="body")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        logging.error("Error in router_homepage.put_body() - ", e)
        raise HTTPException(
            status_code=500, detail="Qualcosa è andato storto riprova più tardi"
        ) from e


@router_protected.put(
    "/footer",
    status_code=200,
    description="Create or update footer",
)
def put_footer(items: list[Item]) -> None:
    try:
        homepage_service = HomePageService()
        homepage_service.put_section(items=items, sections="footer")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        logging.error("Error in router_homepage.put_footer() - ", e)
        raise HTTPException(
            status_code=500, detail="Qualcosa è andato storto riprova più tardi"
        ) from e
