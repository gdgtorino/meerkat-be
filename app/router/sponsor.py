import logging
from typing import List

from fastapi import APIRouter, HTTPException

from app.dto.sponsor import SponsorDto
from app.services.sponsor import SponsorService

router_public = APIRouter(
    prefix="/sponsor",
    tags=["sponsor"],
)


@router_public.get("/{id_sponsor}", status_code=200,
                    description="Get sponsor", )
def get_sponsor(id_sponsor: str) -> SponsorDto:
    try:
        sponsor_service = SponsorService()
        return sponsor_service.get_sponsor(id_sponsor=id_sponsor)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_sponsor.get_sponsor() - ", e)
        raise HTTPException(status_code=500, detail="Qualcosa è andato storto riprova più tardi")


@router_public.get("", status_code=200,
                    description="Get all sponsors", )
def get_sponsor() -> List[SponsorDto]:
    try:
        sponsor_service = SponsorService()
        return sponsor_service.get_all_sponsors()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_sponsor.get_sponsor() - ", e)
        raise HTTPException(status_code=500, detail="Qualcosa è andato storto riprova più tardi")


router_protected = APIRouter(
    prefix="/sponsor",
    tags=["sponsor"],
    # dependencies=[Depends(api_key_auth)]
)


@router_protected.put("", status_code=200,
                      description="Create or update sponsor. <br> WARNING: For sponsors the \"open_new_tab\" attribute of the btn object will always be set to true, regardless of the value received")
def put_sponsor(sponsor: SponsorDto) -> SponsorDto:
    try:
        sponsor_service = SponsorService()
        return sponsor_service.put_sponsor(sponsor=sponsor)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_sponsor.put_sponsor() - ", e)
        raise HTTPException(status_code=500, detail="Qualcosa è andato storto riprova più tardi")
