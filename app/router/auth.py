import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uvicorn.server import logger

from app.dto.user import User
from app.services.auth import AuthService

router_public = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(api_key_auth)]
)
security = HTTPBearer()

@router_public.post("/register", status_code=200, description="Register")
def register(request : User):
    logger.info("AUTH - Called Register")
    logger.info(request)
    try:
        auth_service = AuthService()
        return auth_service.register_user(request)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_auth.register() - ", e)
        raise HTTPException(status_code=500, detail="Opss, something wrong happend, try again later... ")

@router_public.post("/login", status_code=200, description="Sign In")
def login(credentials: HTTPAuthorizationCredentials = Depends(security)):
    logger.info("AUTH - Called Sign In")

    try:
        token = credentials.credentials
        auth_service = AuthService()
        return auth_service.verify_user_token(token)
    except HTTPException as e:
        logger.error(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_auth.login() - ", e)
        raise HTTPException(status_code=500, detail="Opss, something wrong happend, try again later... ")
