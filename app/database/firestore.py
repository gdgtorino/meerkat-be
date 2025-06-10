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


def get_firestore_client():
    '''
    This method is a bad trick to use a single db in firebase where multiple planners are saved
    '''
    collection_prefix = get_env()["firestore.prefix"]
    if collection_prefix:
        return firestore.client().collection(collection_prefix)
    else:
        return None #firestore.client()