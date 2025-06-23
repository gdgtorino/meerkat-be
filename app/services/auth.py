from logging import exception

import firebase_admin.exceptions
from fastapi import HTTPException
from firebase_admin.auth import UserRecord, EmailAlreadyExistsError
from google.cloud.firestore_v1 import FieldFilter
from pydantic import ValidationError

from app.auth.roles import Role
from app.dto.user import User
from app.database.firestore import get_firestore_client
from firebase_admin import auth


class AuthService:
    def __init__(self):
        self.db = get_firestore_client()

    # <editor-fold desc="Login">
    def verify_user_token(self, id_token : str) -> bytes:
        """Verifies the Firebase ID token and returns the user's UID.
           Should work for both username/password and Google Account login"""
        try:
            # Verify the ID token while checking if the token is revoked.
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            claims = self._get_uid_claims(uid)
            return auth.create_custom_token(uid, claims)
        except auth.ExpiredIdTokenError:
            # Token is expired.
            raise HTTPException(status_code=400, detail= "Expired ID token.")
        except auth.RevokedIdTokenError:
            # Token is revoked.
            raise  HTTPException(status_code=401, detail= "Revoked ID token.")
        except auth.InvalidIdTokenError:
            # Token is invalid.
            raise HTTPException(status_code=400, detail= "Invalid ID token.")
        except firebase_admin.exceptions.NOT_FOUND:
            #No user matching UID
            raise  HTTPException(status_code=404, detail= "User with given UID not found.")

    def _get_uid_claims(self, uid) -> dict:
        result = {}
        user =  self.db.collection("users").where(filter=FieldFilter("uid", "==", uid))

        if user is not None:
            result = user.roles
        else :
            raise firebase_admin.exceptions.NOT_FOUND

        return { "roles" : result }
    # </editor-fold>

    #<editor-fold desc="Registration">
    def register_user(self, user_obj) -> UserRecord:
        """Register a new user for the username/password authentication"""
        try:

            new_user = auth.create_user(
                display_name=user_obj.name,
                email=user_obj.email,
                password=user_obj.password
            )
            auth.set_custom_user_claims(new_user.uid, {'role': user_obj.role})
            print("CREATED USER")
            user_record = User(
                uid=new_user.uid, name = new_user.display_name,
                email=new_user.email, disabled=new_user.disabled,
                role=Role(new_user.custom_claims["role"])
            )
            self.db.collection("users").document().set(user_record)
            return new_user
        except ValidationError as exc:
            raise HTTPException(status_code=400, detail=exc.errors()[0]['msg'])
        except EmailAlreadyExistsError:
            raise HTTPException(status_code=409, detail="The user already exists")

    #</editor-fold>