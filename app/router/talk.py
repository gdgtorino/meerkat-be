import logging
from typing import List

from fastapi import APIRouter, HTTPException

from app.dto.talk import TalkDto
from app.services.talk import TalkService

router_public = APIRouter(
    prefix="/talk",
    tags=["talk"],
)


@router_public.get("/{id_talk}", status_code=200,
                    description="Get talk", )
def get_talk(id_talk: str) -> TalkDto:
    try:
        talk_service = TalkService()
        return talk_service.get_talk(id_talk=id_talk)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_talk.get_talk() - ", e)
        raise HTTPException(status_code=500, detail="Qualcosa è andato storto riprova più tardi")


@router_public.get("", status_code=200,
                    description="Get all talks", )
def get_talk() -> List[TalkDto]:
    try:
        talk_service = TalkService()
        return talk_service.get_all_talks()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_talk.get_talk() - ", e)
        raise HTTPException(status_code=500, detail="Qualcosa è andato storto riprova più tardi")


router_protected = APIRouter(
    prefix="/talk",
    tags=["talk"],
    # dependencies=[Depends(api_key_auth)]
)


@router_protected.put("", status_code=200,
                      description="Create or update talk")
def put_talk(talk: TalkDto) -> TalkDto:
    try:
        talk_service = TalkService()
        return talk_service.put_talk(talk=talk)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_talk.put_talk() - ", e)
        raise HTTPException(status_code=500, detail="Qualcosa è andato storto riprova più tardi")
