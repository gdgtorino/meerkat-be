import logging

from fastapi import APIRouter, HTTPException, Request

from app.dto.user import User
from app.services.auth import AuthService

router_public = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(api_key_auth)]
)

@router_public.post("/register", status_code=200, description="Register")
def register(request : User):
    print(request)
    try:
        auth_service = AuthService()
        return auth_service.register_user(request)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_auth.register() - ", e)
        raise HTTPException(status_code=500, detail="Opss, something wrong happend, try again later... ")

@router_public.post("/login", status_code=200, description="Sign In")
def login(request : Request):
    try:
        auth_service = AuthService()
        return auth_service.verify_user_token(request.auth)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error("Error in router_auth.login() - ", e)
        raise HTTPException(status_code=500, detail="Opss, something wrong happend, try again later... ")
