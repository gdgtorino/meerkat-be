from fastapi import HTTPException
from firebase_admin.auth import UserRecord, EmailAlreadyExistsError
from pydantic import ValidationError
from uvicorn.server import logger

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
        except auth.UserNotFoundError:
            #No user matching UID
            raise  HTTPException(status_code=404, detail= "User with given UID not found.")

    def _get_uid_claims(self, uid) -> dict:
        result = {}

        #FIXME Al momento non viene recuperato il dato dell'utente in maniera esatta, necessario a stabilirne il ruolo
        users =  self.db.collection("auth").document("users").collection(uid).limit(1).get()

        if users:
            result = users[0].to_dict().get("role")
        else :
            raise auth.UserNotFoundError("User witH given uid not found")

        return { "roles" : result }
    # </editor-fold>

    #<editor-fold desc="Registration">
    def register_user(self, user_obj) -> UserRecord:
        """Register a new user for the username/password authentication"""
        new_user = None
        try:
            # Step 1: Crea utente Firebase
            new_user = auth.create_user(
                display_name=user_obj.name,
                email=user_obj.email,
                password=user_obj.password
            )
            logger.info(f"Created Firebase user: {new_user.uid}")
            auth.set_custom_user_claims(new_user.uid, {'role': user_obj.role})
            logger.info("CREATED USER")
            user_record = User(
                uid=new_user.uid, name=new_user.display_name,
                email=new_user.email, disabled=new_user.disabled,
                role=user_obj.role
            )

            firestore_data = user_record.model_dump(mode='json', exclude_none=True, exclude={"uid"})
            self._save_user_into_firestore(user_record.uid, firestore_data)
            return new_user

        except EmailAlreadyExistsError:
            # Non fare cleanup per questo errore (l'utente non è stato creato)
            raise HTTPException(
                status_code=409,
                detail="A user with this email address already exists"
            )
        except Exception as e:
            # Auto-cleanup in caso di errore
            logger.error(e)
            if new_user:
                try:
                    auth.delete_user(new_user.uid)
                    logger.error(f"Rolled back: deleted user {new_user.uid}")
                except Exception as cleanup_error:
                    logger.error(f"Cleanup failed for {new_user.uid}: {cleanup_error}")

            # Re-raise con gestione errori specifica
            self._handle_registration_error(e)


    def _save_user_into_firestore(self, uid, firestore_data):
        logger.info("START Saving user to firestore")
        doc_ref = self.db.collection("auth").document("users")
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.update({uid: firestore_data})
        else:
            doc_ref.set({uid: firestore_data})

        logger.info("END Saving user to firestore")

    def _handle_registration_error(self, error):
        """Gestisce gli errori di registrazione con messaggi specifici"""
        if isinstance(error, ValidationError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid user data: {error.errors()[0]['msg']}"
            )
        elif "firestore" in str(error).lower():
            raise HTTPException(
                status_code=500,
                detail="Database error during user registration"
            )
        elif "custom_user_claims" in str(error).lower():
            raise HTTPException(
                status_code=500,
                detail="Error setting user role"
            )
        elif "email" in str(error).lower() and "invalid" in str(error).lower():
            raise HTTPException(
                status_code=400,
                detail="Invalid email format"
            )
        elif "password" in str(error).lower():
            raise HTTPException(
                status_code=400,
                detail="Password does not meet requirements"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Internal server error during user creation"
            )
    #</editor-fold>