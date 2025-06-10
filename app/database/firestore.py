import firebase_admin
from firebase_admin import firestore, credentials

from app.config.env import get_env


def init_firestore_client_service_account() :
    if firebase_admin._apps:
        return firestore.client()
    else:
        # Use a service account.
        cred = credentials.Certificate(get_env()["firestore.path_credential_file"])
        firebase_admin.initialize_app(cred)
